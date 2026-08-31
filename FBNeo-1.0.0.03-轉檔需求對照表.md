# FBNeo 1.0.0.03 轉檔需求對照表

重建 kof-GOTVG_offline_pack 的 24 套所需的**全部**原版檔案。
共 14 個 zip / 117 個檔 / 549.5MB(SPLIT set),依 KOF 世代排列。

來源:`libretro/FBNeo` **`master` 分支** `dats/` 目錄下的官方 DAT,
`<version>1.0.0.03</version>`,**隨包附上**
`dats/FinalBurn Neo (ClrMame Pro XML, Neogeo only).dat`
(680 個條目 = 679 個 game + neogeo BIOS、KOF 系列 160 個,sha256 `90ef9278…8004b5`;該檔最後異動
commit `9f9c674c` / 2026-08-22,取得日期 2026-08-31)。可直接餵給
clrmamepro / RomVault 驗自己的 romset。

自行重抓的 URL(**必須百分號編碼**,檔名含空格與括號,直接貼會 404):

```
https://raw.githubusercontent.com/libretro/FBNeo/master/dats/FinalBurn%20Neo%20(ClrMame%20Pro%20XML%2C%20Neogeo%20only).dat
```

> **注意「1.0.0.03」不是凍結的發行物。** FBNeo 沒有 `v1.0.0.03` tag(最新
> tag 是 `v1.0.0.02`),該版號是 master 的開發中版本,DAT 內容會隨時間增長。
> 兩份都寫 1.0.0.03 但內容不同是正常的 —— **以 sha256 與 game 數為準**。
只列 SPLIT set 中**實際存在於該 zip** 的檔案(帶 `merge=` 的繼承項目已排除)。

> **對 DAT 實查過(2026-08-31)。** 下表 14 個 zip / 117 個檔的 CRC 拿去 DAT
> 裡逐一比對,**全數命中、零缺漏**;且 117 個檔**全部實體存在於自己的 zip,
> 沒有任何一個是 `merge=` 繼承**。所以 SPLIT romset 就足夠 —— `kof2002t`
> 與 `kof2k3fd` 雖然分別是 `kof2002` / `kof2003` 的 clone,**不需要**額外
> 準備那兩個母集 zip。

> **不必湊齊。** builder 依世代組裝 —— 備齊某一代要的 zip 就能產出那一代,
> 其餘會被跳過。`python3 build_kof-GOTVG_offline_pack.py kof96` 只做 KOF96。

## 總覽

| 世代 | 需要的 zip | 檔數 | 大小 |
|---|---|---|---|
| KOF94 | `kof94.zip` | 12 | 22.1MB |
| KOF94 | `kof94nr2.zip` | 1 | 2.0MB |
| KOF94 | `kof94rz.zip` | 1 | 0.1MB |
| KOF95 | `kof95.zip` | 12 | 29.1MB |
| KOF96 | `kof96.zip` | 13 | 44.1MB |
| KOF97 | `kof97.zip` | 12 | 56.2MB |
| KOF98 | `kof98.zip` | 12 | 64.4MB |
| KOF99 | `kof99.zip` | 5 | 14.1MB |
| KOF99 | `kof99fd.zip` | 9 | 68.0MB |
| KOF2000 | `kof2000.zip` | 4 | 16.0MB |
| KOF2001 | `kof2001.zip` | 4 | 16.0MB |
| KOF2001 | `kof2k1fd.zip` | 7 | 52.0MB |
| KOF2002 | `kof2002t.zip` | 13 | 84.2MB |
| KOF2003 | `kof2k3fd.zip` | 12 | 81.0MB |
| | **合計** | **117** | **549.5MB** |

> `kof94nr2.zip`(1 檔)與 `kof94rz.zip`(1 檔)都是 FBNeo DAT 內的正規
> clone set,完整 romset 裡就有,不需要另外找補充包。
>
> `kof2003t` 與 `kof2k3fd` 是等價來源 —— 兩者在 DAT 內都實體含有本包要的
> 12 個檔,有哪個用哪個(builder 只比對內容 CRC)。

---

# KOF94

## `kof94.zip` — 12 檔 / 22.1MB

| 檔名 | CRC32 | 大小 | 用於 |
|---|---|---|---|
| `055-c1.c1` | `b96ef460` | 2048KB | kof94ru |
| `055-c2.c2` | `15e096a7` | 2048KB | kof94ru |
| `055-c3.c3` | `54f66254` | 2048KB | kof94ru |
| `055-c4.c4` | `0b01765f` | 2048KB | kof94ru |
| `055-c5.c5` | `ee759363` | 2048KB | kof94ru |
| `055-c6.c6` | `498da52c` | 2048KB | kof94ru |
| `055-c7.c7` | `62f66888` | 2048KB | kof94ru |
| `055-c8.c8` | `fe0a235d` | 2048KB | kof94ru |
| `055-m1.m1` | `f6e77cf5` | 128KB | kof94ru |
| `055-v1.v1` | `8889596d` | 2048KB | kof94ru |
| `055-v2.v2` | `25022b27` | 2048KB | kof94ru |
| `055-v3.v3` | `83cf32c0` | 2048KB | kof94ru |

## `kof94nr2.zip` — 1 檔 / 2.0MB

| 檔名 | CRC32 | 大小 | 用於 |
|---|---|---|---|
| `055-p1nr2.p1` | `f4c60559` | 2048KB | kof94ru |

## `kof94rz.zip` — 1 檔 / 0.1MB

| 檔名 | CRC32 | 大小 | 用於 |
|---|---|---|---|
| `055-s1rz.s1` | `286ab67d` | 128KB | kof94ru |

---

# KOF95

## `kof95.zip` — 12 檔 / 29.1MB

| 檔名 | CRC32 | 大小 | 用於 |
|---|---|---|---|
| `084-c1.c1` | `fe087e32` | 4096KB | kof95sp |
| `084-c2.c2` | `07864e09` | 4096KB | kof95sp |
| `084-c3.c3` | `a4e65d1b` | 4096KB | kof95sp |
| `084-c4.c4` | `c1ace468` | 4096KB | kof95sp |
| `084-c5.c5` | `8a2c1edc` | 2048KB | kof95sp |
| `084-c6.c6` | `f593ac35` | 2048KB | kof95sp |
| `084-c7.c7` | `9904025f` | 1024KB | kof95sp |
| `084-c8.c8` | `78eb0f9b` | 1024KB | kof95sp |
| `084-m1.m1` | `6f2d7429` | 128KB | kof95sp |
| `084-v1.v1` | `84861b56` | 4096KB | kof95sp |
| `084-v2.v2` | `b38a2803` | 2048KB | kof95sp |
| `084-v3.v3` | `d683a338` | 1024KB | kof95sp |

---

# KOF96

## `kof96.zip` — 13 檔 / 44.1MB

| 檔名 | CRC32 | 大小 | 用於 |
|---|---|---|---|
| `214-c1.c1` | `7ecf4aa2` | 4096KB | kof96c, kof96rss |
| `214-c2.c2` | `05b54f37` | 4096KB | kof96c, kof96rss |
| `214-c3.c3` | `64989a65` | 4096KB | kof96c, kof96rss |
| `214-c4.c4` | `afbea515` | 4096KB | kof96c, kof96rss |
| `214-c5.c5` | `2a3bbd26` | 4096KB | kof96c, kof96rss |
| `214-c6.c6` | `44d30dc7` | 4096KB | kof96c, kof96rss |
| `214-c7.c7` | `3687331b` | 4096KB | kof96c, kof96rss |
| `214-c8.c8` | `fa1461ad` | 4096KB | kof96c, kof96rss |
| `214-m1.m1` | `dabc427c` | 128KB | kof96c, kof96rss |
| `214-p2.sp2` | `002ccb73` | 2048KB | kof96rss |
| `214-v1.v1` | `63f7b045` | 4096KB | kof96ae, kof96c, kof96rss |
| `214-v2.v2` | `25929059` | 4096KB | kof96ae, kof96c, kof96rss |
| `214-v3.v3` | `92a2257d` | 2048KB | kof96c, kof96rss |

---

# KOF97

## `kof97.zip` — 12 檔 / 56.2MB

| 檔名 | CRC32 | 大小 | 用於 |
|---|---|---|---|
| `232-c1.c1` | `5f8bf0a1` | 8192KB | kof971v1, kof97s |
| `232-c2.c2` | `e4d45c81` | 8192KB | kof971v1, kof97s |
| `232-c3.c3` | `581d6618` | 8192KB | kof971v1, kof97jhph, kof97orh, kof97s |
| `232-c4.c4` | `49bb1e68` | 8192KB | kof971v1, kof97jhph, kof97orh, kof97s |
| `232-c5.c5` | `34fc4e51` | 4096KB | kof971v1, kof97jhph, kof97s |
| `232-c6.c6` | `4ff4d47b` | 4096KB | kof971v1, kof97jhph, kof97s |
| `232-m1.m1` | `45348747` | 128KB | kof971v1, kof97jhph, kof97orh, kof97s |
| `232-p2.sp2` | `158b23f6` | 4096KB | kof971v1, kof97s |
| `232-s1.s1` | `8514ecf5` | 128KB | kof971v1, kof97jhph, kof97s |
| `232-v1.v1` | `22a2b5b5` | 4096KB | kof971v1, kof97jhph, kof97orh, kof97s |
| `232-v2.v2` | `2304e744` | 4096KB | kof971v1, kof97jhph, kof97orh, kof97s |
| `232-v3.v3` | `759eb954` | 4096KB | kof971v1, kof97jhph, kof97orh, kof97s |

---

# KOF98

## `kof98.zip` — 12 檔 / 64.4MB

| 檔名 | CRC32 | 大小 | 用於 |
|---|---|---|---|
| `242-c3.c3` | `22127b4f` | 8192KB | kof98h, kof98king, kof98pls, kof98s |
| `242-c4.c4` | `0b4fa044` | 8192KB | kof98h, kof98king, kof98pls, kof98s |
| `242-c5.c5` | `9d10bed3` | 8192KB | kof98c2025, kof98h, kof98king, kof98pls, kof98plsc, kof98s |
| `242-c6.c6` | `da07b6a2` | 8192KB | kof98c2025, kof98h, kof98king, kof98pls, kof98plsc, kof98s |
| `242-c7.c7` | `f6d7a38a` | 8192KB | kof98c2025 |
| `242-c8.c8` | `c823e045` | 8192KB | kof98c2025 |
| `242-m1.m1` | `4ef7016b` | 256KB | kof98h, kof98king, kof98pls, kof98plsc, kof98s |
| `242-s1.s1` | `7f7b4805` | 128KB | kof98s |
| `242-v1.v1` | `b9ea8051` | 4096KB | kof98c2025, kof98h, kof98king, kof98pls, kof98plsc, kof98s |
| `242-v2.v2` | `cc11106e` | 4096KB | kof98c2025, kof98h, kof98king, kof98pls, kof98plsc, kof98s |
| `242-v3.v3` | `044ea4e1` | 4096KB | kof98c2025, kof98h, kof98king, kof98pls, kof98plsc, kof98s |
| `242-v4.v4` | `7985ea30` | 4096KB | kof98c2025, kof98h, kof98king, kof98pls, kof98plsc, kof98s |

---

# KOF99

## `kof99.zip` — 5 檔 / 14.1MB

| 檔名 | CRC32 | 大小 | 用於 |
|---|---|---|---|
| `251-m1.m1` | `5e74539c` | 128KB | kof99t |
| `251-v1.v1` | `ef2eecc8` | 4096KB | kof99t |
| `251-v2.v2` | `73e211ca` | 4096KB | kof99t |
| `251-v3.v3` | `821901da` | 4096KB | kof99t |
| `251-v4.v4` | `b49e6178` | 2048KB | kof99t |

## `kof99fd.zip` — 9 檔 / 68.0MB

| 檔名 | CRC32 | 大小 | 用於 |
|---|---|---|---|
| `152-p2.sp2` | `274ef47a` | 4096KB | kof99t |
| `251-c1d.c1` | `b3d88546` | 8192KB | kof99t |
| `251-c2d.c2` | `915c8634` | 8192KB | kof99t |
| `251-c3d.c3` | `b047c9d5` | 8192KB | kof99t |
| `251-c4d.c4` | `6bc8e4b1` | 8192KB | kof99t |
| `251-c5d.c5` | `9746268c` | 8192KB | kof99t |
| `251-c6d.c6` | `238b3e71` | 8192KB | kof99t |
| `251-c7d.c7` | `2f68fdeb` | 8192KB | kof99t |
| `251-c8d.c8` | `4c2fad1e` | 8192KB | kof99t |

---

# KOF2000

## `kof2000.zip` — 4 檔 / 16.0MB

| 檔名 | CRC32 | 大小 | 用於 |
|---|---|---|---|
| `257-v1.v1` | `17cde847` | 4096KB | kof2000s, kof2000sp, kof2000t |
| `257-v2.v2` | `1afb20ff` | 4096KB | kof2000s, kof2000sp, kof2000t |
| `257-v3.v3` | `4605036a` | 4096KB | kof2000s, kof2000sp, kof2000t |
| `257-v4.v4` | `764bbd6b` | 4096KB | kof2000s, kof2000sp, kof2000t |

---

# KOF2001

## `kof2001.zip` — 4 檔 / 16.0MB

| 檔名 | CRC32 | 大小 | 用於 |
|---|---|---|---|
| `262-v1-08-e0.v1` | `83d49ecf` | 4096KB | kof2001s |
| `262-v2-08-e0.v2` | `003f1843` | 4096KB | kof2001s |
| `262-v3-08-e0.v3` | `2ae38dbe` | 4096KB | kof2001s |
| `262-v4-08-e0.v4` | `26ec4dd9` | 4096KB | kof2001s, kof96ae |

## `kof2k1fd.zip` — 7 檔 / 52.0MB

| 檔名 | CRC32 | 大小 | 用於 |
|---|---|---|---|
| `262-c2d.c2` | `f9d05d99` | 8192KB | kof2001s |
| `262-c3d.c3` | `4c7ec427` | 8192KB | kof2001s |
| `262-c4d.c4` | `1d237aa6` | 8192KB | kof2001s |
| `262-c5d.c5` | `c2256db5` | 8192KB | kof2001s |
| `262-c6d.c6` | `8d6565a9` | 8192KB | kof2001s |
| `262-c8d.c8` | `954d0e16` | 8192KB | kof2001s |
| `262-pg2.sp2` | `91eea062` | 4096KB | kof2001s |

---

# KOF2002

## `kof2002t.zip` — 13 檔 / 84.2MB

| 檔名 | CRC32 | 大小 | 用於 |
|---|---|---|---|
| `265-c1d.c1` | `7efa6ef7` | 8192KB | kf2k2pp |
| `265-c2d.c2` | `aa82948b` | 8192KB | kf2k2pp |
| `265-c3d.c3` | `959fad0b` | 8192KB | kf2k2pp, kof2002kai, kof2002prsp |
| `265-c4d.c4` | `efe6a468` | 8192KB | kf2k2pp, kof2002kai, kof2002prsp |
| `265-c5d.c5` | `74bba7c6` | 8192KB | kf2k2pp, kof2002kai, kof2002prsp |
| `265-c6d.c6` | `e20d2216` | 8192KB | kf2k2pp, kof2002kai, kof2002prsp |
| `265-c7d.c7` | `8a5b561c` | 8192KB | kf2k2pp, kof2002kai, kof2002prsp |
| `265-c8d.c8` | `bef667a3` | 8192KB | kf2k2pp, kof2002kai, kof2002prsp |
| `265-m1d.m1` | `1c661a4b` | 128KB | kf2k2pp, kof2002kai, kof2002prsp |
| `265-p2t.sp2` | `0a189c94` | 4096KB | kf2k2pp |
| `265-s1d.s1` | `e0eaaba3` | 128KB | kf2k2pp, kof2002kai, kof2002prsp |
| `265-v1d.v1` | `0fc9a58d` | 8192KB | kf2k2pp, kof2002kai, kof2002prsp |
| `265-v2d.v2` | `b8c475a4` | 8192KB | kf2k2pp, kof2002kai, kof2002prsp |

---

# KOF2003

## `kof2k3fd.zip` — 12 檔 / 81.0MB

| 檔名 | CRC32 | 大小 | 用於 |
|---|---|---|---|
| `271-c1d.c1` | `e42fc226` | 8192KB | kof2003t |
| `271-c2d.c2` | `1b5e3b58` | 8192KB | kof2003t |
| `271-c3d.c3` | `d334fdd9` | 8192KB | kof2003t |
| `271-c4d.c4` | `0d457699` | 8192KB | kof2003t |
| `271-c5d.c5` | `8a91aae4` | 8192KB | kof2003t |
| `271-c6d.c6` | `9f8674b8` | 8192KB | kof2003t |
| `271-c7d.c7` | `8ee6b43c` | 8192KB | kof2003t |
| `271-c8d.c8` | `6d8d2d60` | 8192KB | kof2003t |
| `271-m1d.m1` | `cc8b54c0` | 512KB | kof2003t |
| `271-s1d.s1` | `3230e10f` | 512KB | kof2003t |
| `271-v1d.v1` | `dd6c6a85` | 8192KB | kof2003t |
| `271-v2d.v2` | `0e84f8c1` | 8192KB | kof2003t |

---

# 備註

- builder 只比對**內容 CRC**,不看檔名也不看 romset 名。zip 名只是 1.0.0.03
  DAT 裡的座標;你的檔案叫什麼都行,CRC 對上就會被採用。
- 「FBNeo 1.0.0.03」是跨多年 nightly 共用的版號,同版號的集合彼此未必相同。
  真正釘得住的是上表的 CRC。
- KOF96 需要 `kof2001.zip`:`kof96ae` 的 `214-v4aeg.v4` 用的是 KOF2001 的
  `262-v4-08-e0.v4`(`26ec4dd9`),那個 hack 借了 2001 的音源。
- `kof2k2ly.zip` / `kof2002t.zip` 的 `265-p2t.sp2`(`0a189c94`)是 kf2k2pp
  唯一的來源;`kof2k2fd.zip` 自己那顆 p2d 是 `432fdf53`,對不上。

---

# 三個替代用的補充包

上表 14 個 zip **全部是 FBNeo 1.0.0.03 DAT 內的正規 set**,取得完整的
FBNeo Neo Geo romset 就都有,不需要任何額外的補充包。

其中 6 個是 clone,但要用的檔都實體存在於自己的 zip:

| clone | cloneof | 要用的檔 | 是否需要母集 |
|---|---|---|---|
| `kof94nr2` | `kof94` | 1 檔 | 否(kof94 另有自己的 12 檔要用) |
| `kof94rz` | `kof94` | 1 檔 | 否(同上) |
| `kof99fd` | `kof99` | 9 檔 | 否(kof99 另有自己的 5 檔要用) |
| `kof2k1fd` | `kof2001` | 6 檔 | 否(kof2001 另有自己的 4 檔要用) |
| `kof2002t` | `kof2002` | 11 檔 | **否 —— `kof2002.zip` 完全不需要** |
| `kof2k3fd` | `kof2003` | 12 檔 | **否 —— `kof2003.zip` 完全不需要** |

不必自己比對這張表 —— 把整包 romset 丟進 `romset/` 後跑
`python3 pick_originals.py`,它會依內容 CRC 挑出需要的 zip 放進
`originals/`,並報出還缺什麼。下載前先跑 `--needed` 可以知道該勾哪幾個。

> **v3.2 曾規劃的三個補充包**(`kof94-extra.zip`、`kof2001-decrypted.zip`、
> `kof2002-decrypted.zip`)**從未發布,v4.4 起取消。** 它們是原版 ROM 資料的
> 重新封裝,與本包只收改版獨有內容的原則衝突;而且完整 romset 裡本來就有
> 對應的正規 set,不需要。

