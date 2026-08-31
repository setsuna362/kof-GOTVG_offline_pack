#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""從一堆雜亂的 romset 裡挑出本包真正需要的原版 zip,放進 originals/。

  python3 pick_originals.py                 掃 romset/ -> originals/
  python3 pick_originals.py --dry-run       只報告,不動檔案
  python3 pick_originals.py --src ~/roms    指定來源目錄
  python3 pick_originals.py --copy          強制複製(預設用硬連結,不佔空間)

把整包 KOF 相關的 rom 丟進 romset/ 就好,不用自己挑 —— 這支程式**完全依
內容比對**:讀每個 zip 內每個檔的 CRC32,對照 manifest.json 的 sources
反查誰是本包需要的。檔名叫什麼、romset 名對不對,一律不影響判斷。

挑選採最小覆蓋:同一個檔在多個 zip 裡都有時,只取貢獻最多的那個,避免把
重複的 zip 全搬過來。
"""
import argparse, binascii, json, os, re, shutil, sys, zipfile
from collections import defaultdict

H = os.path.dirname(os.path.abspath(__file__))
GEN_ORDER = ["KOF94", "KOF95", "KOF96", "KOF97", "KOF98",
             "KOF99", "KOF2000", "KOF2001", "KOF2002", "KOF2003"]

ap = argparse.ArgumentParser(add_help=True)
ap.add_argument("--src", default=os.path.join(H, "romset"))
ap.add_argument("--dst", default=os.path.join(H, "originals"))
ap.add_argument("--dry-run", action="store_true")
ap.add_argument("--copy", action="store_true", help="複製而非硬連結")
ap.add_argument("--verify", action="store_true",
                help="解壓重算 CRC 驗證(慢,預設信任 zip 檔頭的 CRC)")
ap.add_argument("--needed", action="store_true",
                help="只列出需要哪些原版 zip(不掃描),供 torrent 勾選用")
ap.add_argument("--checklist", action="store_true",
                help="印出 14 個 zip 的完整檔名 + CRC32 清單(依隨包 DAT 生成)")
a = ap.parse_args()

MAN = json.load(open(os.path.join(H, "manifest.json"), encoding="utf-8"))
if MAN.get("version") != 6:
    sys.exit("manifest 版本不符,請用隨附的 manifest.json")
SETS, SOURCES = MAN["sets"], MAN["sources"]

# 每個世代要從池取得的 CRC(在 sources 裡的,就是必須由原版供應的)
gen_need = defaultdict(set)
for name, e in SETS.items():
    for fn, c in e["files"].items():
        if c in SOURCES:
            gen_need[e["gen"]].add(c)
        elif c in MAN.get("split", {}):          # 切分:需要來源那顆大 ROM
            gen_need[e["gen"]].add(MAN["split"][c]["from"])
        elif "_dj" in dir() and os.path.isfile(_dj):
            _d2 = json.load(open(_dj, encoding="utf-8"))["deltas"]
            if c in _d2:
                gen_need[e["gen"]].add(_d2[c]["base"])
NEED = set(SOURCES)

# 差分的基準也必須湊到 —— 它們未必列在 sources(sources 只列 builder 直接
# 取用的檔),但少了就還原不出分片。不納入的話,最小覆蓋可能挑到「對
# sources 等價、卻不含某個基準」的替代 romset(例如用 kof2003t.zip 代替
# kof2k3fd.zip,前者就沒有 271-p1d.p1)。
_dj = os.path.join(H, "deltas.json")
if os.path.isfile(_dj):
    _bases = {e["base"] for e in
              json.load(open(_dj, encoding="utf-8"))["deltas"].values()}
    NEED |= _bases
# split 的來源同理
for _c, _e in MAN.get("split", {}).items():
    NEED.add(_e["from"])

# 唯一的真實來源:隨包附的 FBNeo 官方 DAT。刻意不提供改用他份 DAT 的選項,
# 避免不同來源的清單造成分歧 —— 要更新就直接換掉這個檔。
DAT = os.path.join(H, "dats", "FinalBurn Neo (ClrMame Pro XML, Neogeo only).dat")


def read_dat():
    """回傳 {set 名: (描述, [(檔名, crc, 大小)])};DAT 不在就回 None。"""
    if not os.path.exists(DAT):
        return None
    x = open(DAT, encoding="utf-8", errors="replace").read()
    out = {}
    # 屬性順序不固定(BIOS 條目是 <game isbios="yes" name="neogeo" ...>),
    # 所以先抓整段屬性再取 name,不能假設 name 排第一個。
    for attr, body in re.findall(r"<game\b([^>]*)>(.*?)</game>", x, re.S):
        name = dict(re.findall(r'(\w+)="([^"]*)"', attr)).get("name")
        if not name:
            continue
        desc = re.search(r"<description>(.*?)</description>", body)
        roms = []
        for r in re.findall(r"<rom\b([^>]*)/>", body):
            d = dict(re.findall(r'(\w+)="([^"]*)"', r))
            if "merge" in d:
                continue                     # SPLIT:繼承自母集,不在這個 zip
            roms.append((d.get("name", "?"), (d.get("crc") or "").lower(),
                         int(d.get("size", 0))))
        out[name] = (desc.group(1) if desc else "", roms)
    return out


# ── --checklist:完整檔名 + CRC 清單 ──────────────────────────────────
if a.checklist:
    dat = read_dat()
    if dat is None:
        sys.exit(f"找不到 DAT:{DAT}")
    want = defaultdict(set)
    for name, e in SETS.items():
        for fn, c in e["files"].items():
            if c in SOURCES:
                want[SOURCES[c]].add(c)
    ver = re.search(r"<version>(.*?)</version>",
                    open(DAT, encoding="utf-8", errors="replace").read(8192))
    print(f"FBNeo Neo Geo DAT v{ver.group(1) if ver else '?'} "
          f"({len(dat)} 個 game) —— 本包需要 {len(want)} 個 zip / "
          f"{sum(len(v) for v in want.values())} 個檔")
    print(f"DAT: {os.path.relpath(DAT, H)}\n")
    print("每個 zip 內只列本包用得到的檔。CRC32 是唯一判準,檔名僅供參考。\n")
    gi = {g: i for i, g in enumerate(GEN_ORDER)}
    serves = defaultdict(set)
    for name, e in SETS.items():
        for fn, c in e["files"].items():
            if c in SOURCES:
                serves[SOURCES[c]].add(e["gen"])
    grand = 0
    absent = []
    for R in sorted(want, key=lambda x: (min(gi[g] for g in serves[x]), x)):
        if R not in dat:
            absent.append(R)
            print(f"## {R}.zip — ⚠️ 這份 DAT 內沒有這個 set")
            print(f"   本包需要它的 {len(want[R])} 個檔:"
                  f"{', '.join(sorted(want[R]))}\n")
            continue
        desc, roms = dat[R]
        rows = [(n, c, sz) for n, c, sz in roms if c in want[R]]
        tot = sum(sz for _, _, sz in rows)
        grand += tot
        gs = ", ".join(g.replace("KOF", "") for g in sorted(serves[R], key=lambda g: gi[g]))
        print(f"## {R}.zip — {desc}")
        print(f"   {len(rows)} 檔 / {tot/1048576:.1f}MB   供應 KOF{gs}")
        for n, c, sz in sorted(rows):
            print(f"     {n:20} {c}  {sz//1024:>6}KB")
        print()
    print(f"合計 {sum(len(v) for v in want.values())} 檔 / {grand/1048576:.1f}MB"
          + (f"(不含上面 {len(absent)} 個缺席 set)" if absent else ""))
    if absent:
        print(f"\n⚠️ 這份 DAT 少了 {len(absent)} 個本包需要的 set:"
              f"{', '.join(absent)}")
        print("   隨包 DAT 應該要含有全部 14 個 —— 出現這行表示 dats/ 底下那份")
        print("   被換成了較舊或不同的版本,manifest 與它已經對不上。")
    print("\n驗證自己的 romset:把整包丟進 romset/ 後跑")
    print("  python3 pick_originals.py --dry-run --verify")
    sys.exit(0)


# ── --needed:不掃描,直接列出該抓哪些 zip ────────────────────────────
if a.needed:
    bysrc = defaultdict(set)
    for name, e in SETS.items():
        for fn, c in e["files"].items():
            if c in SOURCES:
                bysrc[SOURCES[c]].add(c)
    # 從對照表撈大小(有就用,沒有就略過)
    size = {}
    doc = os.path.join(H, "FBNeo-1.0.0.03-轉檔需求對照表.md")
    if os.path.exists(doc):
        cur = None
        for ln in open(doc, encoding="utf-8"):
            h = re.match(r"##\s+`(\S+?)\.zip`", ln)
            if h:
                cur = h.group(1); continue
            r = re.match(r"\|\s*`[^`]+`\s*\|\s*`([0-9a-f]{8})`\s*\|\s*(\d+)KB", ln)
            if r and cur:
                size[r.group(1)] = int(r.group(2)) * 1024
    serves = defaultdict(set)
    for name, e in SETS.items():
        for fn, c in e["files"].items():
            if c in SOURCES:
                serves[SOURCES[c]].add(e["gen"])
    print("本包需要的原版 zip —— 在 torrent 客戶端只勾這幾個就夠:\n")
    print(f"  {'zip':18} {'檔':>3} {'大小':>9}  供應世代")
    print("  " + "-" * 62)
    tot = 0
    gi = {g: i for i, g in enumerate(GEN_ORDER)}
    for r in sorted(bysrc, key=lambda x: (min(gi[g] for g in serves[x]), x)):
        mb = sum(size.get(c, 0) for c in bysrc[r]) / 1048576
        tot += mb
        gs = ", ".join(g.replace("KOF", "")
                       for g in sorted(serves[r], key=lambda g: gi[g]))
        print(f"  {r + '.zip':18} {len(bysrc[r]):>3} {mb:>8.1f}M  {gs}")
    print("  " + "-" * 62)
    print(f"  {'合計':18} {sum(len(v) for v in bysrc.values()):>3} {tot:>8.1f}M"
          f"  ({len(bysrc)} 個 zip)")
    print("\n注意:以上大小只算本包用得到的檔,SPLIT romset 的實際 zip 會更大。")
    print("下載後把整個目錄丟給本程式即可,不必自己挑:")
    print("  python3 pick_originals.py --src <你的下載目錄>")
    sys.exit(0)

if not os.path.isdir(a.src):
    sys.exit(f"來源目錄不存在:{a.src}\n把原版 zip 丟進去後再跑一次。")

# ── 掃描 ──────────────────────────────────────────────────────────────
print(f"掃描 {a.src} …")
zips = []
for root, _, files in os.walk(a.src):
    for fn in sorted(files):
        if fn.lower().endswith(".zip"):
            zips.append(os.path.join(root, fn))
other = sum(1 for root, _, fs in os.walk(a.src) for f in fs
            if f.lower().endswith((".7z", ".rar")))

hits = {}            # zip 路徑 -> {crc}
for p in zips:
    try:
        with zipfile.ZipFile(p) as z:
            if a.verify:
                got = {format(binascii.crc32(z.read(i.filename)) & 0xffffffff, "08x")
                       for i in z.infolist() if not i.is_dir()}
            else:
                got = {format(i.CRC & 0xffffffff, "08x")
                       for i in z.infolist() if not i.is_dir()}
        h = got & NEED
        if h:
            hits[p] = h
    except Exception as e:
        print(f"  略過 {os.path.basename(p)}(讀取失敗:{e})")

print(f"  {len(zips)} 個 zip,其中 {len(hits)} 個含本包需要的檔")
if other:
    print(f"  另有 {other} 個 .7z/.rar 未處理 —— 請先解成 .zip")

# ── 最小覆蓋 ──────────────────────────────────────────────────────────
chosen, covered = [], set()
pool = dict(hits)
while pool:
    p, h = max(pool.items(), key=lambda kv: (len(kv[1] - covered), -len(kv[1])))
    new = h - covered
    if not new:
        break
    chosen.append((p, new))
    covered |= new
    del pool[p]

missing = NEED - covered
print(f"\n覆蓋 {len(covered)}/{len(NEED)} 個必要檔,選中 {len(chosen)} 個 zip"
      + (f",缺 {len(missing)} 個" if missing else ",全數齊備"))

# ── 世代結論 ──────────────────────────────────────────────────────────
print(f"\n{'世代':10} {'需要':>4} {'齊備':>4}  狀態")
print("-" * 46)
ready = []
for g in GEN_ORDER:
    if g not in gen_need:
        continue
    n = gen_need[g]
    have = n & covered
    okg = len(have) == len(n)
    ready.append(g) if okg else None
    print(f"{g:10} {len(n):>4} {len(have):>4}  " + ("✅ 可組裝" if okg else
          f"❌ 缺 {len(n) - len(have)} 個"))

if missing:
    bysrc = defaultdict(list)
    for c in missing:
        # 差分基準與 split 來源不在 sources 裡(sources 只列 builder 直接
        # 取用的檔),歸到「差分/切分基準」一類報告。
        bysrc[SOURCES.get(c, "(差分/切分基準)")].append(c)
    print("\n缺料 —— 還少這些檔(依內容判定,檔名不拘):")
    for r, cs in sorted(bysrc.items(), key=lambda x: -len(x[1])):
        print(f"  manifest 標 {r + '.zip':14} 缺 {len(cs):>3} 個:"
              f"{', '.join(sorted(cs))}")

    # 查 DAT:同一個 CRC 還出現在哪些 set,給使用者替代選擇
    dat = read_dat()
    if dat:
        c2s = defaultdict(set)
        for gname, (gdesc, groms) in dat.items():
            for rn, rc, rsz in groms:
                c2s[rc].add(gname)
        cover = defaultdict(set)
        for c in missing:
            for g in c2s.get(c, ()):
                cover[g].add(c)
        if cover:
            print("\n  同樣內容也存在於這些 set —— 取得任何一個都算數:")
            left = set(missing)
            while left:
                canon = {SOURCES[c] for c in left if c in SOURCES}
                g, cs = max(cover.items(),
                            key=lambda kv: (len(kv[1] & left),
                                            kv[0] in canon,      # 平手時取正規來源
                                            -len(kv[1])))
                got = cs & left
                if not got:
                    break
                desc = dat[g][0][:44]
                print(f"    {g + '.zip':14} 補 {len(got)} 個  {desc}")
                left -= got
                del cover[g]
            if left:
                print(f"    (仍有 {len(left)} 個在 DAT 內找不到其他來源)")
            print("  ↑ 這是最少組合;每個檔的完整可用來源見 --checklist 與對照表。")

# ── 落地 ──────────────────────────────────────────────────────────────
if not chosen:
    sys.exit("\n沒有可搬的檔案。")
print(f"\n{'搬移計畫' if not a.dry_run else '搬移計畫(--dry-run,不會動檔案)'}:")
os.makedirs(a.dst, exist_ok=True) if not a.dry_run else None
done = 0
for p, new in chosen:
    dst = os.path.join(a.dst, os.path.basename(p))
    mark = "已存在" if os.path.exists(dst) else ""
    print(f"  {os.path.basename(p):28} 提供 {len(new):>3} 個檔  {mark}")
    if a.dry_run or os.path.exists(dst):
        continue
    try:
        if a.copy:
            raise OSError
        os.link(p, dst)                      # 同一檔案系統,不佔額外空間
    except OSError:
        shutil.copy2(p, dst)
    done += 1

if a.dry_run:
    print("\n(--dry-run:什麼都沒動)")
else:
    print(f"\n完成 —— {done} 個 zip 進入 {os.path.relpath(a.dst, H)}/")
    if ready:
        print("接著可以跑:")
        for g in ready:
            print(f"  python3 build_kof-GOTVG_offline_pack.py {g[3:].lower()}")
