#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 parts/ 的分片改成對原版 ROM 的 bsdiff 差分,產生 deltas/ 與 deltas.json。

  python3 tools/make_deltas.py            產生 deltas/ 並驗證
  python3 tools/make_deltas.py --verify   只驗證現有的 deltas/,不重算

維護者用,不在使用者的組建路徑上。需要 bsdiff4(pip install bsdiff4),
所以刻意放在 tools/ 而非根目錄。

**基準以 CRC 記錄,不記檔名或 romset 名。** 還原時由 builder 在 POOL 裡依
CRC 反查,與專案其餘部分同樣完全依內容比對。deltas.json:

  { "version": 1,
    "deltas": { "<目標 crc>": {"base": "<基準 crc>", "size": <目標長度>} } }

差分本身不含可獨立使用的遊戲資料 —— 沒有原版就還原不出任何東西。
"""
import binascii, json, os, sys, zipfile, collections

try:
    import bsdiff4
except ImportError:
    sys.exit("需要 bsdiff4:pip install bsdiff4(建議用 venv)")

H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERIFY_ONLY = "--verify" in sys.argv
PARTS, DELTAS = os.path.join(H, "parts"), os.path.join(H, "deltas")
MANIFEST = os.path.join(H, "deltas.json")


def crc(b):
    return format(binascii.crc32(b) & 0xffffffff, "08x")


man = json.load(open(os.path.join(H, "manifest.json"), encoding="utf-8"))
SETS, SOURCES = man["sets"], man["sources"]
parts = sorted(f[:-4] for f in os.listdir(PARTS) if f.endswith(".bin"))

# ── POOL:originals/ 內每個檔,依 CRC 索引(內容按需讀取)────────────────
loc = {}                                   # crc -> (zip 路徑, 成員名, 長度)
used_zip, zip_crcs = [], {}
for z in sorted(os.listdir(os.path.join(H, "originals"))):
    if not z.endswith(".zip"):
        continue
    p = os.path.join(H, "originals", z)
    used_zip.append(z); zip_crcs[z] = set()
    with zipfile.ZipFile(p) as zf:
        for i in zf.infolist():
            if i.is_dir():
                continue
            c = format(i.CRC & 0xffffffff, "08x")
            zip_crcs[z].add(c)
            if c not in loc:
                loc[c] = (p, i.filename, i.file_size)
print(f"POOL: {len(loc)} 個原版檔(來自 originals/ 的 {len(used_zip)} 個 zip)", flush=True)

# 守衛:差分的基準必須是使用者保證會有的檔。使用者照文件只會取得
# manifest sources 指名的那些原版 romset,所以 originals/ 裡若混進沒有貢獻
# 任何 sources CRC 的 zip,拿它當基準會產出使用者還原不了的差分。
extra = [z for z in used_zip if not (zip_crcs[z] & set(SOURCES))]
if extra:
    sys.exit("originals/ 混入了非必要的 zip,請先移除再重跑(否則差分可能"
             "以使用者不會擁有的檔為基準):\n  " + "\n  ".join(extra))

_cache = {}
def read(c):
    if c not in _cache:
        p, fn, _ = loc[c]
        with zipfile.ZipFile(p) as zf:
            _cache[c] = zf.read(fn)
    return _cache[c]


ext = lambda f: f.rsplit(".", 1)[-1].lower()
fam = lambda e: e.rstrip("abcd") or e

# 每個分片的槽位(取第一個用到它的 set 的檔名)
slot = {}
for n, e in SETS.items():
    for fn, c in e["files"].items():
        if c in parts:
            slot.setdefault(c, ext(fn))

if VERIFY_ONLY:
    if not os.path.exists(MANIFEST):
        sys.exit("deltas.json 不存在,請先不帶 --verify 執行一次")
    dm = json.load(open(MANIFEST, encoding="utf-8"))
    ok = bad = 0
    for tc, e in sorted(dm["deltas"].items()):
        bc = e["base"]
        if bc not in loc:
            print(f"  ✗ {tc}: 基準 {bc} 不在 POOL"); bad += 1; continue
        d = open(os.path.join(DELTAS, tc + ".bsdiff"), "rb").read()
        got = bsdiff4.patch(read(bc), d)
        if crc(got) == tc and len(got) == e["size"]:
            ok += 1
        else:
            print(f"  ✗ {tc}: 還原後 CRC={crc(got)} 長度={len(got)}"); bad += 1
    print(f"\n驗證:{ok} 個正確,{bad} 個失敗")
    sys.exit(1 if bad else 0)

os.makedirs(DELTAS, exist_ok=True)
out, tot_raw, tot_d, nobase = {}, 0, 0, []
print(f"\n{'分片':10}{'槽位':6}{'原始':>9}{'差分':>10}{'省':>7}  基準")
print("-" * 72)
for tc in parts:
    t = open(os.path.join(PARTS, tc + ".bin"), "rb").read()
    e = slot.get(tc, "?")
    # 候選:同副檔名且同大小 -> 同副檔名 -> 同族同大小 -> 任意同大小。
    # 全部只看內容,不看 romset 名 —— sources 標的名稱與使用者實際持有的
    # zip 未必相同(例如 kof2k3fd 與 kof2003t 等價,內容相同)。
    cand = [c for c, (p, fn, s) in loc.items() if ext(fn) == e and s == len(t)]
    if not cand:
        cand = [c for c, (p, fn, s) in loc.items() if ext(fn) == e]
    if not cand:
        cand = [c for c, (p, fn, s) in loc.items()
                if fam(ext(fn)) == fam(e) and s == len(t)]
    if not cand:
        cand = [c for c, (p, fn, s) in loc.items() if s == len(t)]
    if not cand:
        nobase.append(tc)
        print(f"{tc}  {e:5}{len(t)/1048576:>8.2f}M {'—':>9} {'—':>6}  (無基準)", flush=True)
        continue
    # bsdiff 很貴,候選多時先用「對齊取樣相同率」便宜地排序,只對前 2 名
    # 實跑。改版多半是在原版上原地改幾個位元組,對齊取樣抓得很準。
    if len(cand) > 2:
        def score(c):
            b = read(c); n = min(len(b), len(t))
            step = max(1, n // 4096)
            return sum(b[i] == t[i] for i in range(0, n, step))
        cand = sorted(cand, key=score, reverse=True)[:2]
    ds, bc = min(((len(bsdiff4.diff(read(c), t)), c) for c in cand), key=lambda x: x[0])
    d = bsdiff4.diff(read(bc), t)
    # 立刻自我驗證:還原回來必須位元組相同
    assert crc(bsdiff4.patch(read(bc), d)) == tc, f"{tc} 差分還原不符"
    open(os.path.join(DELTAS, tc + ".bsdiff"), "wb").write(d)
    out[tc] = {"base": bc, "size": len(t)}
    tot_raw += len(t); tot_d += ds
    _, bfn, _ = loc[bc]
    print(f"{tc}  {e:5}{len(t)/1048576:>8.2f}M {ds/1048576:>9.3f}M "
          f"{100*(1-ds/len(t)):>5.1f}%  {bc} {bfn}", flush=True)

json.dump({"version": 1, "deltas": out}, open(MANIFEST, "w", encoding="utf-8"),
          indent=1, ensure_ascii=False, sort_keys=True)
print("-" * 72)
print(f"{len(out)} 個差分:{tot_raw/1048576:.1f}MB -> {tot_d/1048576:.2f}MB "
      f"(省 {100*(1-tot_d/tot_raw):.1f}%)")
if nobase:
    print(f"無基準 {len(nobase)} 個:{', '.join(nobase)}")
print(f"寫出 deltas/ 與 deltas.json")
