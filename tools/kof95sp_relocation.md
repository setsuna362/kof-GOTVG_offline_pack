# KOF '95 Special 2017 — P3 重定位版（標準硬體相容）

## 這是什麼
GSC2007 的 kof95sp（Ver 1.2.0222 / GOTVG 20200303）原本把 128KB 的
084-p3sp.p3 映射在 68K 位址 $900000–$91FFFF——即記憶卡插槽的位址窗口，
只有 FBNeo / HBMAME 以特製 mapping 支援，實機、NeoSD、MiSTer 都跑不了。

分析發現 P3 實際 payload 只有 0x2641 bytes（其餘全零），且 GSC2007 在
P2 的 $282FFA–$289000 留了一段清零的空洞。本工具把 payload 搬到
**$283000**，並修正全部 131 處絕對參照（P1 61 處 + P3 內部 70 處，
capstone 逐一反組譯驗證，P2 經確認零參照），同時內建 FBNeo
kof95PatchCallback 的兩個平台鉤子中和補丁：

1. P1 $03E79C:`4E7C`（GOTVG 非法指令鉤子）→ `4E75` RTS
2. P1 $03E750:`jmp $901750` → `move.l #$3E7FA,$500(a5)`（與 FBNeo 位元組一致）

結果：P ROM 收斂為標準 2MB 佈局（與原版 kof95 相同形狀），不需任何
自訂記憶體映射。

## 檔案
- `kof95sp2017r.neo` — MiSTer NeoGeo core / NeoSD 直接可用
- `084-p1sp2017r.p1` — 2MB 合併 P ROM，採 MAME 2MB 慣例
  （檔案前半 = $200000 那一 MB，後半 = $000000 那一 MB，向量表在偏移 0x100000）
- `084-p1sp.p1` / `084-p2d.sp2` — 拆分版（word-swapped，各 1MB），
  供自訂 FBNeo/HBMAME driver 使用；S1 沿用原 `084-s1sp.s1`，C/M/V 沿用 kof95 母板
- `relocate_p3.py` — 可重現整個流程的腳本（需 capstone）

## 驗證狀態
靜態驗證全數通過：重定位後掃描零殘留 $90xxxx 參照、入口點反組譯
逐指令比對一致、PC 相對分支位元組不變。（進戰鬥、連擊計數、隱藏組隊順序、小跳等 P3 相關功能）。

CRC32:
- 084-p1sp2017r.p1 (2MB): b948e6fb
- 084-p1sp.p1: e4bc0bc3 / 084-p2d.sp2: e4a8c4eb

GSC2007 在 P3 開頭（現在位於 $283000）留有橫幅：

> THIS HACK IS ONLY FOR STUDY AND COMMUNICATION. ALL COPYRIGHT OWNED BY SNK.
> REFUSE ANY SECONDARY MODIFICATIONS AND COMMERCIAL PROFIT BEHAVIOR.

## 全部 131+2 處補丁的完整稽核紀錄

```text
hook  P1 $03E79C: 4E7C -> 4E75 (RTS)
hook  P1 $03E750: jmp $901750 -> move.l #$3E7FA,$500(a5)
p1ref $004C9A: jsr $901e80.l                      -> $284E80
p1ref $0055D0: jsr $901ec8.l                      -> $284EC8
p1ref $005A46: jsr $9010ea.l                      -> $2840EA
p1ref $005A68: jmp $9013fc.l                      -> $2843FC
p1ref $007AEC: jsr $901eae.l                      -> $284EAE
p1ref $007C66: jsr $901da8.l                      -> $284DA8
p1ref $007C92: jmp $901018.l                      -> $284018
p1ref $007CC2: jsr $90202a.l                      -> $28502A
p1ref $008D06: jsr $901e8e.l                      -> $284E8E
p1ref $009520: jsr $901e6e.l                      -> $284E6E
p1ref $0096BE: jsr $9022de.l                      -> $2852DE
p1ref $0096DA: jsr $901e9e.l                      -> $284E9E
p1ref $009DF4: jsr $902526.l                      -> $285526
p1ref $00AD2C: jsr $90147a.l                      -> $28447A
p1ref $00B576: jsr $901f0e.l                      -> $284F0E
p1ref $00D310: jmp $901e4c.l                      -> $284E4C
p1ref $00EB66: jsr $9022aa.l                      -> $2852AA
p1ref $014504: jsr $9025cc.l                      -> $2855CC
p1ref $016B10: jsr $902292.l                      -> $285292
p1ref $017F6C: jsr $9022b8.l                      -> $2852B8
p1ref $021828: jsr $9025cc.l                      -> $2855CC
p1ref $02648A: jsr $90227c.l                      -> $28527C
p1ref $0368CA: jsr $9025cc.l                      -> $2855CC
p1ref $039AF4: jsr $901274.l                      -> $284274
p1ref $039B30: jsr $9013e8.l                      -> $2843E8
p1ref $039B94: jsr $9013e8.l                      -> $2843E8
p1ref $039C40: jmp $9012ce.l                      -> $2842CE
p1ref $03B3F4: jmp $90234e.l                      -> $28534E
p1ref $03B552: lea.l $901108.l, a0                -> $284108
p1ref $03D7E8: jmp $901000.l                      -> $284000
p1ref $03E0D2: lea.l $901248.l, a0                -> $284248
p1ref $03E0FC: jsr $901222.l                      -> $284222
p1ref $03E10A: jsr $9011d0.l                      -> $2841D0
p1ref $03E140: jmp $901198.l                      -> $284198
p1ref $03EAEE: jsr $90205a.l                      -> $28505A
p1ref $03EDBA: jsr $90212a.l                      -> $28512A
p1ref $03EDD0: move.l #$90236c, (a4)              -> $28536C
p1ref $03EDDC: jmp $90150a.l                      -> $28450A
p1ref $03EF06: jsr $902146.l                      -> $285146
p1ref $03EF4E: jsr $9021a4.l                      -> $2851A4
p1ref $03EF58: lea.l $9021fa.l, a0                -> $2851FA
p1ref $03EFE2: jsr $902138.l                      -> $285138
p1ref $03F01E: move.l #$90236c, (a4)              -> $28536C
p1ref $03F02A: jmp $90150a.l                      -> $28450A
p1ref $03F12E: jsr $902146.l                      -> $285146
p1ref $03F14C: jmp $90211e.l                      -> $28511E
p1ref $03F15C: lea.l $9021fa.l, a0                -> $2851FA
p1ref $03F740: jmp $901c88.l                      -> $284C88
p1ref $03F770: jmp $901c9e.l                      -> $284C9E
p1ref $03F7BE: jmp $901cbe.l                      -> $284CBE
p1ref $03F8C0: jsr $90205a.l                      -> $28505A
p1ref $03F94A: jsr $901738.l                      -> $284738
p1ref $03FBC4: jmp $901a58.l                      -> $284A58
p1ref $03FC7E: jmp $901c04.l                      -> $284C04
p1ref $03FCC4: jmp $901986.l                      -> $284986
p1ref $03FDB4: jsr $901c68.l                      -> $284C68
p1ref $03FE00: jsr $901c68.l                      -> $284C68
p1ref $03FE8A: jsr $901c34.l                      -> $284C34
p1ref $03FE96: jmp $901c18.l                      -> $284C18
p1ref $0401AE: jsr $902098.l                      -> $285098
p1ref $0439EA: jmp $901048.l                      -> $284048
p3ref $90104A: move.l #$901058, $500(a5)          -> $284058
p3ref $901098: lea.l $9010b2.l, a0                -> $2840B2
p3ref $9010A4: lea.l $9010ce.l, a0                -> $2840CE
p3ref $901146: lea.l $9000c0.l, a3                -> $2830C0
p3ref $901172: lea.l $9000c0.l, a3                -> $2830C0
p3ref $9011D2: lea.l $9011f2.l, a0                -> $2841F2
p3ref $9011DE: lea.l $901202.l, a0                -> $284202
p3ref $9011EC: lea.l $901212.l, a0                -> $284212
p3ref $9012DE: movea.l #$9013cc, a0               -> $2843CC
p3ref $9014C8: move.l #$9014ce, (a4)              -> $2844CE
p3ref $9014EC: move.l #$9014f0, (a4)              -> $2844F0
p3ref $901536: lea.l $9021fa.l, a0                -> $2851FA
p3ref $90154E: move.l #$901552, (a4)              -> $284552
p3ref $901562: move.l #$901568, (a4)              -> $284568
p3ref $9015D2: lea.l $901678.l, a0                -> $284678
p3ref $9015FA: lea.l $901686.l, a0                -> $284686
p3ref $901606: lea.l $901690.l, a0                -> $284690
p3ref $90162E: lea.l $90169a.l, a0                -> $28469A
p3ref $901756: move.l #$90175e, $500(a5)          -> $28475E
p3ref $901766: move.l #$901778, (a4)              -> $284778
p3ref $901772: move.l #$901776, (a4)              -> $284776
p3ref $901786: move.l #$90178a, (a4)              -> $28478A
p3ref $9017C8: lea.l $9017da.l, a0                -> $2847DA
p3ref $901810: lea.l $901864.l, a0                -> $284864
p3ref $901824: lea.l $90188c.l, a0                -> $28488C
p3ref $901838: lea.l $901856.l, a0                -> $284856
p3ref $90184C: lea.l $900000.l, a0                -> $283000
p3ref $901926: lea.l $900000.l, a0                -> $283000
p3ref $9019AA: move.l #$9019ae, (a4)              -> $2849AE
p3ref $9019E6: move.l #$9019ea, (a4)              -> $2849EA
p3ref $901A2A: lea.l $901a00.l, a0                -> $284A00
p3ref $901A36: lea.l $901a0a.l, a0                -> $284A0A
p3ref $901A42: lea.l $901a14.l, a0                -> $284A14
p3ref $901A4E: lea.l $901a1e.l, a0                -> $284A1E
p3ref $901A8A: move.l #$901a8e, (a4)              -> $284A8E
p3ref $901B62: move.l #$901b58, (a4)              -> $284B58
p3ref $901B7C: move.l #$901b80, (a4)              -> $284B80
p3ref $901C0A: move.l #$901c0e, (a4)              -> $284C0E
p3ref $901C3A: lea.l $901c4c.l, a0                -> $284C4C
p3ref $901C74: lea.l $901c84.l, a0                -> $284C84
p3ref $901CDE: move.l #$901ce2, (a4)              -> $284CE2
p3ref $901D16: move.l #$901d1a, (a4)              -> $284D1A
p3ref $901DC4: lea.l $901dea.l, a0                -> $284DEA
p3ref $901DF6: movea.l #$901e46, a0               -> $284E46
p3ref $901E00: movea.l #$901e40, a0               -> $284E40
p3ref $901E0A: move.l #$901e0e, (a4)              -> $284E0E
p3ref $901E18: movea.l #$901e46, a0               -> $284E46
p3ref $901F74: lea.l $901f9e.l, a0                -> $284F9E
p3ref $901FF6: lea.l $902012.l, a0                -> $285012
p3ref $902004: lea.l $90201e.l, a0                -> $28501E
p3ref $902042: lea.l $902012.l, a0                -> $285012
p3ref $90204C: lea.l $90201e.l, a0                -> $28501E
p3ref $90209A: lea.l $9020ca.l, a0                -> $2850CA
p3ref $9020AE: lea.l $9020d0.l, a0                -> $2850D0
p3ref $9020BA: lea.l $9020de.l, a0                -> $2850DE
p3ref $9021C0: lea.l $9021da.l, a0                -> $2851DA
p3ref $9021D0: lea.l $9021ea.l, a0                -> $2851EA
p3ref $902316: lea.l $902342.l, a0                -> $285342
p3ref $902324: lea.l $902346.l, a0                -> $285346
p3ref $902330: lea.l $90234a.l, a0                -> $28534A
p3ref $902384: move.l #$90238a, (a4)              -> $28538A
p3ref $9023EA: lea.l $902490.l, a0                -> $285490
p3ref $902412: lea.l $90249c.l, a0                -> $28549C
p3ref $90241E: lea.l $9024a8.l, a0                -> $2854A8
p3ref $902446: lea.l $9024b4.l, a0                -> $2854B4
p3ref $902536: move.l #$90253c, (a4)              -> $28553C
p3ref $902578: move.l #$90257c, (a4)              -> $28557C
p3ref $902590: move.l #$902594, (a4)              -> $285594
p3ref $902616: lea.l $902622.l, a0                -> $285622
p3ref $90262A: lea.l $90263a.l, a0                -> $28563A
blob  P3[0:0x2660] -> P2+0x83000 (68K $283000)
check 0 refs to $900000 window remain; 70 internal refs live at new base
out   relocation.log: 0x20a5 bytes crc32=490d0d8c
out   084-p2d.sp2: 0x100000 bytes crc32=e4a8c4eb
out   kof95sp2017r.neo: 0x1f41000 bytes crc32=72b094f4
out   084-p1sp2017r.p1: 0x200000 bytes crc32=b948e6fb
out   084-p1sp.p1: 0x100000 bytes crc32=e4bc0bc3
```
