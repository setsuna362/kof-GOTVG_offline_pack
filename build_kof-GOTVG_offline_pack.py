#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把原版 romset 放進 originals/ 後執行,產生 24 套 GOTVG 改版。

  python3 build_kof-GOTVG_offline_pack.py              組裝所有湊得齊的套件
  python3 build_kof-GOTVG_offline_pack.py kof96        只做 KOF96 那一代
  python3 build_kof-GOTVG_offline_pack.py 97 2002      可指定多代
  python3 build_kof-GOTVG_offline_pack.py --check      只檢查,不寫檔

**不需要湊齊全部原版。** 丟 kof95 需要的東西就會產出 kof95 的套件,
丟 kof96 就產出 kof96 的,依此類推。缺料的世代會被跳過並告訴你缺哪個 zip。

v5 ─ 全零填充區(kof98c2025 的 sp2b / p3)改由 builder 生成,不再佔 parts/。
v4 ─ 依世代分組;manifest 每套帶 gen 與 needs。
v3 ─ 池只從 originals/ 建,並排除與套件同名的 zip(修自我去重缺陷)。
"""
import zipfile, os, sys, json, binascii, bz2
from collections import defaultdict

H = os.path.dirname(os.path.abspath(__file__))
args = [a for a in sys.argv[1:] if not a.startswith("-")]
CHECK_ONLY = "--check" in sys.argv

GEN_ORDER = ["KOF94", "KOF95", "KOF96", "KOF97", "KOF98",
             "KOF99", "KOF2000", "KOF2001", "KOF2002", "KOF2003"]


def crc(b):
    return format(binascii.crc32(b) & 0xffffffff, "08x")


MAN = json.load(open(os.path.join(H, "manifest.json"), encoding="utf-8"))
if MAN.get("version") != 5:
    sys.exit("manifest 版本不符,請用隨附的 manifest.json")
SETS, SOURCES = MAN["sets"], MAN["sources"]
ZEROFILL = MAN.get("zerofill", {})   # crc -> 長度。純填充,不佔 parts/

# deltas.json 有的話就啟用差分模式:分片改以「對原版 ROM 的 bsdiff 差分」
# 分發,基準以 CRC 記錄,由 POOL 依內容反查。沒有 deltas.json 就完全照舊。
DELTAS, DELTADIR = {}, os.path.join(H, "deltas")
_dj = os.path.join(H, "deltas.json")
if os.path.isfile(_dj):
    _d = json.load(open(_dj, encoding="utf-8"))
    if _d.get("version") != 1:
        sys.exit("deltas.json 版本不符,請用隨附的 deltas.json")
    DELTAS = _d["deltas"]


def _off(b):
    """bsdiff 的 int64:最高位元是符號位,其餘是絕對值(小端)。"""
    v = int.from_bytes(b[:8], "little") & 0x7fffffffffffffff
    return -v if b[7] & 0x80 else v


def bspatch(old, delta):
    """純 Python 的 BSDIFF40 還原,只用標準庫 —— 使用者不必安裝 bsdiff4。"""
    if delta[:8] != b"BSDIFF40":
        raise ValueError("不是 BSDIFF40 格式")
    clen, dlen, nlen = _off(delta[8:16]), _off(delta[16:24]), _off(delta[24:32])
    p = 32
    ctrl = bz2.decompress(delta[p:p + clen]); p += clen
    dif = bz2.decompress(delta[p:p + dlen]); p += dlen
    ext = bz2.decompress(delta[p:])
    new = bytearray(nlen)
    op = npos = ci = di = ei = 0
    while npos < nlen:
        x, y, z = (_off(ctrl[ci:ci + 8]), _off(ctrl[ci + 8:ci + 16]),
                   _off(ctrl[ci + 16:ci + 24]))
        ci += 24
        # 逐位元組相加。改版通常只改少數位元組,所以差分段幾乎全是 0 ——
        # 以 64KB 為單位檢查,全零的區塊直接整段複製,只有含變動的才逐位元組
        # 算。少了這個最佳化,8MB 的 C ROM 會慢上兩個數量級。
        for st in range(0, x, 65536):
            n = min(65536, x - st)
            dseg = dif[di + st:di + st + n]
            oseg = old[op + st:op + st + n]
            if len(oseg) < n:                       # 舊檔較短,超出部分視為 0
                oseg = oseg + bytes(n - len(oseg))
            if dseg.count(0) == n:
                new[npos + st:npos + st + n] = oseg
            else:
                new[npos + st:npos + st + n] = bytes(
                    (o + d) & 0xff for o, d in zip(oseg, dseg))
        npos += x; op += x; di += x
        new[npos:npos + y] = ext[ei:ei + y]
        npos += y; ei += y
        op += z
    return bytes(new)


def delta_ready(c):
    """這個 CRC 能不能靠差分還原:要有差分檔,且基準在池裡。"""
    e = DELTAS.get(c)
    return bool(e) and e["base"] in POOL and \
        os.path.isfile(os.path.join(DELTADIR, c + ".bsdiff"))

want_gen = None
if args:
    want_gen = set()
    for a in args:
        key = a.upper().replace("KOF", "").strip()
        hit = [g for g in GEN_ORDER if g[3:] == key]
        if not hit:
            sys.exit(f"認不得的世代:{a}(可用:{', '.join(g[3:] for g in GEN_ORDER)})")
        want_gen.add(hit[0])

FORBID = set(SETS)      # 與本包套件同名的 zip 一律不進池

# 為什麼不用「必要原版檔名白名單」:原版的檔名並不固定 —— 例如解密版的
# kof99 可能就叫 kof99.zip,內含的卻是 152-*.bin。用檔名過濾只會誤殺。
# 而池被多掃到東西並不會污染輸出:組裝時 parts/ 永遠優先於池。

SRCDIR = os.path.join(H, "originals")
USE_SUBDIR = os.path.isdir(SRCDIR)
if not USE_SUBDIR:
    SRCDIR = H

POOL, used_zip, ignored = {}, [], []
for fn in sorted(os.listdir(SRCDIR)):
    if not fn.lower().endswith(".zip"):
        continue
    if not USE_SUBDIR and fn[:-4] in FORBID:
        ignored.append(fn)
        continue
    try:
        with zipfile.ZipFile(os.path.join(SRCDIR, fn)) as z:
            n = 0
            for i in z.infolist():
                if i.is_dir():
                    continue
                c = crc(z.read(i.filename))
                if c not in POOL:
                    POOL[c] = (fn, i.filename)
                    n += 1
            if n:
                used_zip.append(fn)
    except Exception as e:
        ignored.append(f"{fn} (讀取失敗: {e})")

print(f"池來源: {'originals/' if USE_SUBDIR else '本目錄'} — "
      + (", ".join(used_zip) if used_zip else "(無 zip)"))
if ignored:
    print("略過  :", ", ".join(ignored))
if DELTAS:
    _n = sum(1 for c in DELTAS if delta_ready(c))
    print(f"差分  : deltas/ 可用 {_n}/{len(DELTAS)} 個"
          + ("" if _n == len(DELTAS) else " —— 其餘缺差分檔或基準"))

OUT = os.path.join(H, "out")
if not CHECK_ONLY:
    os.makedirs(OUT, exist_ok=True)

bygen = defaultdict(list)
for name, e in SETS.items():
    bygen[e["gen"]].append(name)

_ZCACHE = {}
ok = skip = 0
for gen in GEN_ORDER:
    names = sorted(bygen.get(gen, []))
    if not names or (want_gen and gen not in want_gen):
        continue

    gap = set()
    for name in names:
        for c in SETS[name]["files"].values():
            if (c not in POOL and c not in ZEROFILL
                    and not os.path.isfile(os.path.join(H, "parts", c + ".bin"))
                    and not delta_ready(c)):
                gap.add(c)
    lack = sorted({SOURCES[c] for c in gap if c in SOURCES})

    print(f"\n== {gen} — {len(names)} 套 ==")
    if lack:
        print(f"   缺原版:{', '.join(x + '.zip' for x in lack)}({len(gap)} 個檔)")

    for name in names:
        e = SETS[name]
        data, missing = {}, []
        for fn, c in e["files"].items():
            fp = os.path.join(H, "parts", c + ".bin")
            if os.path.isfile(fp):
                b = open(fp, "rb").read()
                if crc(b) == c:
                    data[fn] = b
                else:
                    missing.append(f"parts/{c}.bin 損毀")
            elif delta_ready(c):
                bc = DELTAS[c]["base"]
                zn, inner = POOL[bc]
                if zn not in _ZCACHE:
                    _ZCACHE[zn] = zipfile.ZipFile(os.path.join(SRCDIR, zn))
                base = _ZCACHE[zn].read(inner)
                d = open(os.path.join(DELTADIR, c + ".bsdiff"), "rb").read()
                b = bspatch(base, d)
                # 還原後一定要驗:差分檔或基準有任何問題都會在這裡擋下來
                if crc(b) == c and len(b) == DELTAS[c]["size"]:
                    data[fn] = b
                else:
                    missing.append(f"deltas/{c}.bsdiff 還原後不符")
            elif c in ZEROFILL:
                data[fn] = bytes(ZEROFILL[c])      # 槽位要求但實際無資料的填充區
            elif c in POOL:
                zn, inner = POOL[c]
                if zn not in _ZCACHE:
                    _ZCACHE[zn] = zipfile.ZipFile(os.path.join(SRCDIR, zn))
                data[fn] = _ZCACHE[zn].read(inner)
            else:
                missing.append(SOURCES.get(c, f"crc {c} 無已知來源"))
        if missing:
            print(f"   {name:12} 略過 — 缺 {len(missing)} 檔")
            skip += 1
            continue
        if CHECK_ONLY:
            print(f"   {name:12} 可組裝     載入名稱: {e['host']}.zip")
        else:
            with zipfile.ZipFile(os.path.join(OUT, name + ".zip"), "w",
                                 zipfile.ZIP_DEFLATED, compresslevel=6) as z:
                for fn in sorted(data):
                    z.writestr(fn, data[fn])
            print(f"   {name:12} -> out/{name}.zip     載入名稱: {e['host']}.zip")
        ok += 1

print(f"\n{'可組裝' if CHECK_ONLY else '完成'} {ok} 套,略過 {skip} 套。")
print("需 neogeo.zip(BIOS)。把某套改名為上表的『載入名稱』後載入該遊戲。")
print("FBNeo 請放到 <system>/fbneo/patched/ 內。")
print("kof96ae / kof2003t 需自建驅動,定義見 drivers/ 目錄。")
