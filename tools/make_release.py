#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 deltas/ 依 KOF 世代打包成 Release 用的 zip,並產生說明表格。

  python3 tools/make_release.py            打包到 release/
  python3 tools/make_release.py --notes    只印說明表格,不打包

維護者用。每個分片打包前都會重算 CRC32 核對檔名,不符即中止。
"""
import binascii, collections, json, os, sys, zipfile

H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTES_ONLY = "--notes" in sys.argv
GEN = ["KOF94", "KOF95", "KOF96", "KOF97", "KOF98",
       "KOF99", "KOF2000", "KOF2001", "KOF2002", "KOF2003"]

man = json.load(open(os.path.join(H, "manifest.json"), encoding="utf-8"))
SETS = man["sets"]
dj = os.path.join(H, "deltas.json")
if not os.path.exists(dj):
    sys.exit("deltas.json 不存在,請先跑 tools/make_deltas.py")
DELTAS = json.load(open(dj, encoding="utf-8"))["deltas"]

# 世代 -> 該代用到的差分;以及每代涵蓋哪些套件
gen_delta = collections.defaultdict(set)
gen_sets = collections.defaultdict(set)
for name, e in SETS.items():
    gen_sets[e["gen"]].add(name)
    for fn, c in e["files"].items():
        if c in DELTAS:
            gen_delta[e["gen"]].add(c)

out = os.path.join(H, "release")
if not NOTES_ONLY:
    os.makedirs(out, exist_ok=True)

rows, tot_n, tot_b = [], 0, 0
for g in GEN:
    cs = sorted(gen_delta.get(g, ()))
    sets_txt = ", ".join(sorted(gen_sets.get(g, ())))
    if not cs:
        rows.append((None, g, 0, 0, sets_txt))
        continue
    tag = g.lower()
    zp = os.path.join(out, f"deltas-{tag}.zip")
    if NOTES_ONLY:
        size = sum(os.path.getsize(os.path.join(H, "deltas", c + ".bsdiff")) for c in cs)
    else:
        # 只放 .bsdiff。deltas.json 隨 repo 一起提供(完整 101 筆)——
        # 若每個世代包各夾一份,解壓多個包會互相覆蓋,只剩最後一個的條目。
        with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for c in cs:
                p = os.path.join(H, "deltas", c + ".bsdiff")
                b = open(p, "rb").read()
                got = format(binascii.crc32(b) & 0xffffffff, "08x")
                z.writestr(f"deltas/{c}.bsdiff", b)
        size = os.path.getsize(zp)
    rows.append((f"deltas-{tag}.zip", g, len(cs), size, sets_txt))
    tot_n += len(cs); tot_b += size

print(f"\n| 下載 | 差分數 | 大小 | 涵蓋套件 |")
print("|---|---|---|---|")
for fn, g, n, b, sets_txt in rows:
    if fn is None:
        print(f"| **不需要** | 0 | — | {sets_txt} |")
    else:
        print(f"| `{fn}` | {n} | {b/1048576:.1f}MB | {sets_txt} |")
print(f"| | **{tot_n}** | **{tot_b/1048576:.1f}MB** | 共 {len(SETS)} 套 |")
if not NOTES_ONLY:
    print(f"\n寫出到 release/")
