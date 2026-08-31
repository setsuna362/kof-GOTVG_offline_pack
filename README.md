# KOF GOTVG 離線包 v5.1

26 套游聚(GOTVG)KOF 改版,**全部經 FBNeo 實測可執行**。

**目標是做出實體卡**(PROGBK1 + CHA512Y),FBNeo 只是驗證與試玩的手段 ——
所以 ROM 配置一律以實體板子的限制為準,不是以模擬器方便為準。

**26 套全部可組裝**,已逐檔 CRC 驗證(401 個檔),無來源 CRC 為零。

## 先取得 `deltas/`

改版獨有的內容**不在 repo 內**,以「**對原版 ROM 的 bsdiff 差分**」形式依
世代分包,放在
[Releases](https://github.com/setsuna362/kof-GOTVG_offline_pack/releases)。
只下載你要組的那幾代即可,解壓到本目錄後會併進同一個 `deltas/`:

| 下載 | 差分數 | 大小 | 涵蓋套件 |
|---|---|---|---|
| **不需要** | 0 | — | kof94ru |
| `deltas-kof95.zip` | 2 | 20KB | kof95sp |
| `deltas-kof96.zip` | 16 | 16.5MB | kof96ae, kof96c, kof96rss |
| `deltas-kof97.zip` | 13 | 2.1MB | kof971v1, kof97jhph, kof97orh, kof97s |
| `deltas-kof98.zip` | 36 | 10.4MB | kof98c2025, kof98h, kof98king, kof98pls, kof98plsc, kof98s |
| `deltas-kof99.zip` | 12 | 2.4MB | kof99ae, kof99t |
| `deltas-kof2000.zip` | 17 | 18.1MB | kof2000s, kof2000sp, kof2000t |
| `deltas-kof2001.zip` | 5 | 50KB | kof2001s |
| `deltas-kof2002.zip` | 17 | 86KB | kf2k2pp, kof2002kai, kof2002p33, kof2002prsp |
| `deltas-kof2003.zip` | 3 | 1.3MB | kof2003t |
| | **121** | **51.0MB** | 共 26 套 |

```bash
unzip -o deltas-kof98.zip    # 解出 deltas/<crc>.bsdiff,重複執行不會互相覆蓋錯
```

> **差分本身不含任何可獨立使用的遊戲資料。** 每個 `.bsdiff` 都是「改版相對
> 於某顆原版 ROM 的差異」,沒有那顆原版就還原不出任何東西。基準以 **CRC**
> 記錄在 `deltas.json`(隨 repo 提供),組建時由 builder 在你的原版池裡依
> **內容**反查 —— 所以你的原版 zip 叫什麼、是 SPLIT 還是 MERGED 都無所謂。
>
> 還原後 builder 會**重驗 CRC 與長度**,差分檔或基準有任何問題都會當場擋下。
> 還原用的 bspatch 是純 Python 實作(只用標準庫的 `bz2`),**不需要安裝
> `bsdiff4` 或任何套件**。

> **KOF94 不需要下載任何東西。** `kof94ru` 的獨有內容是 **0 bytes** —— 它是
> kof94nr2 的 p1 + kof94rz 的 s1 + 原版 kof94 的 C/M/V 這個**組合**,每個
> 位元組都已登錄於 FBNeo。備妥那三個原版後,
> `python3 build_kof-GOTVG_offline_pack.py 94` 就會產出 `kof94ru.zip`。

各世代之間**零共用差分**,所以下載哪幾包就只能組哪幾代,不會有跨包相依。

## 使用方式

### 1. 取得原版 romset

需要 **FBNeo 1.0.0.03** 的 Neo Geo romset,**SPLIT 就夠**。

**這裡不指名任何下載來源。** 原版 ROM 請自備 —— 本包只提供改版相對於原版的
差異。要判斷「我手上這包對不對」,唯一的判準是 **CRC32**,不是 torrent 的
名字、不是壓縮檔的檔名、也不是 romset 的名稱。

**romset 的身分由這份 DAT 定義**(隨包附上):

| | |
|---|---|
| 檔案 | `dats/FinalBurn Neo (ClrMame Pro XML, Neogeo only).dat` |
| 版號 | `<version>1.0.0.03</version>`(680 個條目 = 679 個 game + `neogeo` BIOS,其中 KOF 系列 160 個) |
| sha256 | `90ef9278b179e67a86d8ad0e6ddfaf45a58926cb63e2eb43fb09f13bce8004b5` |
| 來源 | `libretro/FBNeo` 的 **`master` 分支** `dats/` 目錄 |
| 該檔最後異動 | commit `9f9c674c`(2026-08-22) |
| 取得日期 | 2026-08-31 |

拿它餵給 clrmamepro / RomVault,可以直接驗自己的 romset 對不對版。

**本包的 rom 就是依這份 DAT 過濾出來的。** 要自己重抓或查閱:

| 用途 | 連結 |
|---|---|
| 下載(curl / wget) | `https://raw.githubusercontent.com/libretro/FBNeo/master/dats/FinalBurn%20Neo%20(ClrMame%20Pro%20XML%2C%20Neogeo%20only).dat` |
| 瀏覽器看這個檔 | `https://github.com/libretro/FBNeo/blob/master/dats/FinalBurn%20Neo%20(ClrMame%20Pro%20XML%2C%20Neogeo%20only).dat` |
| 瀏覽器看目錄 | <https://github.com/libretro/FBNeo/tree/master/dats> |

> **URL 必須百分號編碼。** 檔名含空格、括號與逗號,未編碼的形式(直接把
> 檔名貼上去)會失敗;檔案頁要用 `blob` 不是 `tree`。目錄頁點進去最省事。

> **ROM 管理器只認 `.xml` 的話,直接改副檔名就好。** 這個檔雖然叫 `.dat`,
> 內容本來就是標準的 Logiqx XML(開頭有 `<?xml version="1.0"?>`、
> `<!DOCTYPE datafile …>`,根元素 `<datafile>`,header 裡還有
> `<clrmamepro forcenodump="ignore"/>`)。不需要任何轉換,複製成
> `….xml` 即可,內容一個位元組都不用動。
>
> 另外注意版本:Logiqx XML datfile 要**現代的 ClrMamePro(4.x)**或
> RomVault 才吃得下。很舊的 ClrMame 用的是自家的舊格式,改副檔名也沒用。

> **「1.0.0.03」不是一個凍結的發行物。** FBNeo 沒有 `v1.0.0.03` 這個 tag
> (repo 上最新的 tag 是 `v1.0.0.02`);`1.0.0.03` 是 master 上的開發中版號。
> 開發期間任何時間點建出來的 FBNeo,DAT 都會寫 `1.0.0.03`,**但 game 清單
> 會隨 `(libretro) update files` 之類的 commit 增長**。
>
> 所以兩份 DAT 都寫 1.0.0.03、內容卻不同,是正常的,不代表誰拿錯。**以
> sha256 和 game 數為準**,不要只看版號。本包的所有結論都是對上表那份
> 特定快照驗出來的;若你的 DAT 較舊,可能不含本包需要的某些 set。

**要哪些檔、CRC 是多少 —— 完整清單直接產出來看:**

```bash
python3 pick_originals.py --checklist    # 14 個 zip / 117 個檔,含檔名與 CRC32
python3 pick_originals.py --needed       # 精簡版:只有 zip 名、大小、供應世代
```

`--checklist` 是**從隨包 DAT 即時生成**的,不是手抄,所以不會與 DAT 脫節。

> **本包統一以上表那份 DAT 為準,不接受換成別份。** 拿自己的 FBNeo 產生
> DAT 再用 RomCenter / cmpro 整理雖然也可行,但那份的內容取決於你那顆執行
> 檔的建置日期 —— 較舊的版本不含 `kof2k3fd` / `kof2002t` / `kof99fd` /
> `kof94nr2` 這類後來才加入的 set,於是 RomCenter 從頭到尾不會叫你去補,
> 照著整理仍然會缺料。統一用同一份,才不會各人算出不同的需求清單。
>
> 要更新基準時,直接換掉 `dats/` 底下那個檔並更新上表的 sha256 與 game 數,
> 全專案跟著一起走。
每個 zip 只列本包用得到的檔(SPLIT 中帶 `merge=` 的繼承項目已排除)。同一份
清單也記在 `FBNeo-1.0.0.03-轉檔需求對照表.md`,方便直接閱讀。

整包 FBNeo romset 有幾十 GB,本包只用得到其中 **14 個 zip / 117 個檔 /
549.5MB**,可以照 `--needed` 的輸出在 torrent 客戶端先勾選再下載。

要的 14 個:`kof94` `kof94nr2` `kof94rz` `kof95` `kof96` `kof97` `kof98`
`kof99` `kof99fd` `kof2000` `kof2001` `kof2k1fd` `kof2002t` `kof2k3fd`

> **`fd` / `t` 結尾的是「解密版」set,不是換個檔名而已。** `kof99fd` /
> `kof2k1fd` / `kof2002t` / `kof2k3fd` 裡的 C ROM 與加密版母集是**不同的
> 檔案、不同的 CRC**(例如 `271-c1c.c1` vs `271-c1d.c1`)。本包產出全部是
> 解密態,加密版母集代替不了這四個。
>
> 這四個都是 FBNeo 1.0.0.03 DAT 內的正規 set(clone),而且要用的檔**全部
> 實體存在於自己的 zip、零 `merge=` 繼承**,所以 SPLIT romset 就足夠,
> **不必**額外準備 `kof2002` / `kof2003` 母集。
>
> 跨世代相依要留意:`kof96ae` 借用 `kof2001` 的 `262-v4` 當自己的
> `214-v4aeg.v4`,所以做 KOF96 也要 `kof2001.zip`。`--needed` 會標出來。

### 2. 挑出需要的原版

把整包 romset 丟進 `romset/`(或任何目錄),然後:

```bash
python3 pick_originals.py                 # romset/ -> originals/
python3 pick_originals.py --src ~/roms    # 指定來源目錄
python3 pick_originals.py --dry-run       # 只報告,不動檔案
python3 pick_originals.py --verify        # 解壓重算 CRC(慢,更嚴謹)
```

不必自己對照表逐個挑 —— 它**完全依內容 CRC 比對**,不看檔名、不看 romset
名,SPLIT / MERGED / NON-MERGED 都吃得下。挑選走最小覆蓋,同一個檔在多個
zip 都有時只取貢獻最多的那個。選中的 zip 以**硬連結**進 `originals/`,
不佔額外空間。跑完會告訴你哪幾代已經湊齊、還缺的檔該去哪個原版拿。

> **檔名不重要,內容才重要。** 你的解密版叫 `kof99.zip` 還是 `kof99fd.zip`
> 都可以。`manifest.json` 的 `sources` 用 FBNeo 正規 set 名當座標,只是用來
> 指出「該去哪找這份內容」,不是要求檔名相符。

### 3. 重組

```bash
python3 build_kof-GOTVG_offline_pack.py            組裝所有湊得齊的
python3 build_kof-GOTVG_offline_pack.py kof96      只做 KOF96 那一代
python3 build_kof-GOTVG_offline_pack.py 97 2002    可指定多代
python3 build_kof-GOTVG_offline_pack.py --check    只檢查,不寫檔
```

**不必湊齊全部原版。** 備齊 kof95 要的東西就會產出 kof95 的套件,依此類推;
缺料的世代會被跳過並告訴你缺哪個 zip。

### 4. 產出

在 `out/`。另需自備 `neogeo.zip`(BIOS)。

> **名稱衝突:`kof98h`。** 本包有一套叫 `kof98h`(KOF98 plus),FBNeo 也有
> 一個真實 romset 叫 `kof98h`。在扁平目錄模式下,真的 `kof98h.zip` 會被當成
> 改版擋在池外 —— 目前無害(沒有任何檔案需要從它取),但用 `originals/`
> 子目錄就完全沒這個問題。另外 `out/kof98h.zip` 的載入名稱也是 `kof98h`,
> 別和原版放在同一處。

原理:與原版相同的區塊直接從原版取,只有改版特有的內容才以差分形式收在
`deltas/`(121 個差分,還原後共 556.0MB,差分本身 51.0MB)。
槽位要求把原版一顆大 ROM 切成數顆小的(PROGBK1 的 V 放不下 8MB),由
builder 依 manifest 的 `split` 直接從池裡切出,同樣不佔分發量。
槽位要求但實際無資料的填充區(kof98c2025 的 `sp2b` / `p3`)由 builder 直接生成,不佔任何空間。

> **kof2002 的 p2 要挑對。** `265-p2d.sp2` 需要 CRC `0a189c94`(FBNeo 名
> `265-p2t.sp2`,見於 `kof2002t` / `kof2k2jq` / `kof2k2ly`)。一般的
> `kof2k2fd` 自己那顆是 `432fdf53`,對不上。所以清單指名 `kof2002t`,
> 不是隨便一個 kof2002 解密版都行。`pick_originals.py` 依 CRC 比對,
> 挑錯的它不會誤收。

> **不要把 `out/` 產生的改版 zip 留在本目錄再跑一次。** builder 會硬性排除
> 與套件同名的 zip,但仍建議保持目錄乾淨,原因見下方「v3 修正」。

---

## 套件清單

### 直接可用(掛現成 FBNeo 槽位)

| 套件 | 中文名 | 載入名稱 | 驗證 |
|---|---|---|---|
| kof95sp | KOF95 Special 2017(P3 重定位版) | `kof95` | 73/73、435 色 ※ |
| kof94ru | KOF94 RU | `kof94` | 73/73、347 色 |
| kof96c | KOF96 連擊版 | `kof96` | 73/73、500 色 |
| kof96rss | KOF96 RSS | `kof96` | 73/73、452 色 |
| kof97s | KOF97 練習版 | `kof97` | 73/73、533 色 |
| kof97jhph | KOF97 進化平衡版 | `kof97` | 73/73、553 色 |
| kof971v1 | KOF97 1v1 專區版 | `kof97` | 73/73、529 色 |
| kof98pls | KOF98 風雲再起 | `kof98h` | 73/73、381 色 |
| kof98s | KOF98 練習版 | `kof98h` | 73/73、382 色 |
| kof98h | KOF98 plus | `kof98h` | 73/73、381 色 |
| kof98plsc | KOF98 風雲再起中文化 | `kof98h` | 73/73、416 色 |
| kof98king | KOF98 King | `kof98h` | 73/73、414 色 |
| kof98c2025 | KOF98 COMBO 2025 | `kof98cp` | 73/73、428 色 ※ |
| kof99t | KOF99 PLUS | `kof99fd` | 71/73、411 色 |
| kof2000sp | KOF2000 SP | `kof2ksp` | 11/12、205 色 |
| kof2001s | KOF2001 練習版 | `kof98h` | 73/73、305 色 |



### 需自建驅動

以下的 ROM 配置與 FBNeo 現成 romset 不符,需自行加入驅動定義。定義見 `drivers/`。

| 套件 | 中文名 | 驅動名 | 原因 |
|---|---|---|---|
| kof96ae | KOF96 AE 版 | `kof96aeg` | C 為 6×8MB;原 `kof96ae` 槽位帶 IPS 版本切換機制,不適用 |
| kof97orh | KOF97 天國神族 | `kof97ubp` | C 為 6×8MB(標準 kof97 為 4×8M+2×4M) |
| kof2000t / kof2000s | KOF2000 优化版 / 練習版 | `kof2000t` | 現成槽位可用,但 kof2000s 的 p1 需先解密(見下) |
| kof2003t | KOF2003 优化版 | `kof2003tg` | PROGBK3S 佈局(1M+4M+2M);V 拆成 4×4MB |
| kof2002prsp / kf2k2pp / kof2002kai / kof2002p33 | KOF2002 UR / PP / 改 / CopyMix | `kof2k2g` | 四套共用。與現成的 `kof2k2fd` 只差在 V:PROGBK1 放不下 8MB,拆成 4×4MB |
| kof99ae | KOF99 AE 版 | `kof99aeg` | 砍到 8 顆 C(64MB);官方 `kof99ae` 是 12 顆 96MB,做不成實體卡 |

> **`kof2003tg` 這個名字不是筆誤。** FBNeo 本身已有一個叫 `kof2003t` 的
> set(p1 為單顆 8MB 的 `271-p1t.p1`),與本包的 kof2003t 同名不同物,
> 故自建驅動改名為 `kof2003tg` 以免衝突。

---

## v3 新增

### kof95sp — P3 重定位版

原版把 128KB 的 `084-p3sp.p3` 映射在 `$900000`(記憶卡位址窗口),只有
FBNeo / HBMAME 支援,實機、NeoSD、MiSTer 都跑不了。本包收的是重定位後
的成品:payload 搬進 P2 於 `$282FFA–$289000` 的清零空洞(新基底
`$283000`),131 處絕對參照全部修正(P1 61 處 + P3 內部 70 處,capstone
逐一反組譯驗證),另中和兩個 GOTVG 平台鉤子:

- `$03E79C`:`4E7C` → `4E75`(RTS)
- `$03E750`:`jmp $901750` → `move.l #$3E7FA,$500(a5)`

結果收斂為**標準 2MB 單檔 P**,與原版 kof95 同形,不需任何自訂映射。
完整稽核紀錄與可重現腳本見 `tools/relocate_p3.py` 與
`tools/kof95sp_relocation.md`。

`084-p1.p1`(CRC `b948e6fb`)採 **MAME 2MB 慣例**:檔案前半 = `$200000`
那一 MB、後半 = `$000000` 那一 MB、向量表在偏移 `0x100000`。
先前 kof2001s、kof2000s 出現的「2M p1 掛不上」都是這個慣例沒對上。

### kof96rss

`214-p1.p1`(CRC `72ace3c1`,1MB)未登錄於 FBNeo。注意 FBNeo 另有一個
`kof96rss` set,用的是 **3MB** 的 `214-p1rss.p1` — 那是不同的建置。
本包這版是 **p1 1M + p2 2M** 的標準佈局,可直接上 PROGBK1。

### kof98king

獨有 5 檔 21.1MB:`242-c7.c7`、`242-c8.c8`、`242-p2.sp2`、`242-pn1.p1`、
`242-s1.s1`。c1/c2 取自 kof98pfe,c3–c6 為原版。P 佈局為
**p1 1M + p2 4M**,即 PROGBK1 目標配置。

> **C 合計 8×8MB = 64MB,剛好貼齊 CHA512Y 上限,零餘裕。** 之後若要再動
> C 就沒有空間了。

### v3.5 新增:kof94ru

`kof94ru` 的 14 個檔案 **CRC 全部已登錄於 FBNeo,零獨有內容**:

| 檔案 | CRC | 出處 |
|---|---|---|
| `055-p1.p1` | `f4c60559` | `055-p1nr2.p1`,僅見於 `kof94nr2` |
| `055-s1.s1` | `286ab67d` | `055-s1rz.s1`,僅見於 `kof94rz` |
| 其餘 12 檔 | — | 原版 `kof94.zip` |

所以它是 **kof94nr2 的 p1 + kof94rz 的 s1 + 原版 kof94 的 C/M/V**,這個組合
不存在於任何單一 FBNeo set。收錄成本是 `parts/` **0 bytes** —— 記下的是
組合本身,不是任何新的位元組。佈局為單檔 2MB p1,與原版 kof94 同形。

### v3.5 新增:kof2002kai

獨有內容只有 `265-p1.p1`(`364f485d`)與解密後的 `265-p2d.sp2`
(`819839e3`),共 5MB。佈局 p1 1M + p2 4M、C 8×8MB,符合 PROGBK1 +
CHA512Y。

**這套的 C 需要 CMC50 離線解密**,解密後 8 顆全部是已公開資料
(c1d/c2d 與 kof2002prsp 同組,c3d–c8d 為原版),s1 亦然。P2 另需
`PCM2DecryptP` 的區塊重排。兩者的做法與驗證見下節。

---

## 兩套需要離線解密的 P

**kof2000s** 與 **kof2003t** 的 p1 在游聚快取中是「位址擾動」形式,
本包收錄的已是解密後的成品,可直接使用。解密方式記錄如下供查驗:

```python
def jmap(i):
    j = i
    if (i & 0x0000FC) == 0x000000: j ^= 0x000100
    if (i & 0x0C0000) != 0x080000: j ^= 0x000100
    if (i & 0x0C0008) == 0x080008: j ^= 0x000100
    if (i & 0x0C00FE) == 0x080000: j ^= 0x000100
    if (i & 0x0C0002) == 0x080002: j ^= 0x000100
    if (i & 0x100000) == 0x100000: j ^= 0x000102
    if (i & 0x000002) == 0x000002: j ^= 0x100002
    if (i & 0x000008) == 0x000008: j ^= 0x100002
    return j

tmp = bytes(raw2MB[jmap(i)] for i in range(0x100000))
pg1 = raw2MB[:0x800] + tmp[0x800:]        # 保留原始檔頭
```

此即 FBNeo `kof98Decrypt` 的位址置換部分。驗證結果:

| | kof2000s | kof2003t |
|---|---|---|
| 輸出 CRC | `d39ebe18` | `cadb0a2f` |
| SP / PC | `0x0010F300` / `0x00C00402` | 同左 |
| `0x100` 標頭 | `NEO-GEO` | `NEO-GEO` |

kof2000s 的結果與原版 `257-pg1.p1` 相符 99%(差 270 bytes,即練習版的修改)。

---

## v3 修正

### builder 的自我去重缺陷

v2 的 builder 是「掃描同目錄所有 zip 建池」。若把 GOTVG 改版 zip 和原版
放在同一個目錄,改版自己的獨有內容會在池中被自己命中,被判定為「與原版
相同」而排除出 `parts/`。**kof2001s 就是這樣掉了 4 個檔案。**

v3 改為:池只接受 `manifest.json` 的 `sources` 指名的原版,並硬性排除所有
與套件同名的 zip。

### manifest 格式

改為 v3 結構:

```json
{ "version": 3,
  "sets":    { "<套件>": { "host": "<載入名稱>", "files": { "<檔名>": "<crc>" } } },
  "sources": { "<crc>": "<提供該檔的原版 romset>" } }
```

`sources` 是新增的:記錄每個非 `parts/` 檔案該從哪個原版 zip 取。分割式
romset 的 parent 繼承已扣除,所以指名的就是實際含有該檔的那個 zip。
builder 缺料時會直接報出需要哪個 `.zip`,不必再自己反查。

### kof2003t 的 s1 來源更正

v2 README 寫「取自 `kof2003.zip` 的 `127-s1.bin`」,這是錯的。該檔 CRC
`3230e10f` 實為 `271-s1d.s1`(512KB),來源是 kof2003 的**解密版**,
加密版母集裡沒有。

---

## v3.1 修正

### kof2001s 已修復

從 kof2001s 的原始來源快取取回 v2 打包時被誤排除的 4 個檔案,CRC 逐一
核對相符,已收進 `parts/`:

| 檔案 | CRC | 大小 |
|---|---|---|
| `242-c1.c1` | `f298b87b` | 8MB |
| `242-c7.c7` | `ef682ed2` | 8MB |
| `242-m1.m1` | `dfb908ca` | 256KB |
| `242-s1.s1` | `de828076` | 128KB |

`fourplay.zip` 的依賴隨之消失。kof2001s 現在只差解密版 kof2001 的
6 個 `262-c*d` C 檔。

### builder 不再用檔名白名單

v3 的扁平目錄模式會把不在白名單上的 zip 當「非必要原版」丟掉。原版的
檔名並不固定(解密版的 kof99 可能就叫 `kof99.zip`,內含卻是 `152-*.bin`),
用檔名過濾只會誤殺。

而且池被多掃到東西**不會污染輸出** —— 組裝時 `parts/` 永遠優先於池。
所以 v3.1 只保留一條排除規則:與本包套件同名的 zip 不進池。

「缺什麼」的判定也改為完全依內容 CRC,不依檔名。

---

## v3.3 / v3.4:三套新加者的實測結果

kof95sp / kof96rss / kof98king 原為靜態驗證,現已補跑完整流程
(投幣 → START → 選角 → 對戰,73 個取樣點)。以下為**官方 BIOS**
(`neogeo.zip`,39 檔)下的結果:

| 套件 | 槽位 | 相異畫面 | 最高色數 |
|---|---|---|---|
| kof95sp | `kof95` | 73/73 | 435 ※ |
| kof96rss | `kof96` | 73/73 | 452 |
| kof98king | `kof98h` | 73/73 | 414 |

畫面已逐一目視確認為正常對戰(精靈、fix 層、調色盤、背景皆正確),
不是高色數的花屏。kof95sp 的 P3 重定位在執行期成立。

**※ kof95sp 需要調整輸入時序。** 標準腳本(START 在 f3400 按一次、
12 幀)在 kof95sp 上沒被吃到,畫面停在 attract,得到 70/73、374 色 ——
仍然通過門檻,但那是 demo 畫面不是對戰。把 START 改為 f3200–5000
間連按、每次 20 幀之後就正常進入對戰,得到上表數字。**這是測試腳本的
按鍵時機問題,不是 ROM 的問題。** 交接文件記的「BIOS 連打需按住
≥20 幀」對 START 同樣適用,標準腳本的 12 幀是不夠的。

### 對照組驗證

重寫 harness 後,先跑已知結果的 kof98pls 當參照(天條 1),再測新的三套:

| BIOS | kof98pls 結果 | 交接文件記錄 |
|---|---|---|
| 自組(5 檔,取自 GOTVG 快取) | 72/73、383 色 | 73/73、381 色 |
| 官方 `neogeo.zip`(39 檔) | **73/73、381 色** | 73/73、381 色 |

官方 BIOS 下與舊記錄一字不差,確認重寫的 harness 正確,且先前的落差
來自 BIOS 而非 ROM。

測試環境:FBNeo libretro fork(`libretro/FBNeo`);像素格式 RGB565;
解析度 304×224 @ 59.18fps。

> **注意:`finalburnneo/FBNeo` 已不含 libretro port。** 現行 upstream
> 的 `src/burner/libretro` 不存在,要編 libretro core 得改用
> `libretro/FBNeo` 這個 fork(有 `Makefile.neogeo`)。

---

## 燒錄到實機(PROGBK1 / CHA512Y)

**v4.1 起,`out/` 的產出全部是解密態,沒有任何一套需要模擬器在載入時
做解密。** 26 套的槽位逐一查過 `HARDWARE_*` 旗標與 Init 函式:

| 世代 | 套件 | 槽位 | 槽位載入時做什麼 |
|---|---|---|---|
| KOF94 | kof94ru | `kof94` | `NeoInit`,無轉換 |
| KOF95 | kof95sp | `kof95` | `NeoInit`,無轉換 |
| KOF96 | kof96c / kof96rss | `kof96` | `NeoInit`,無轉換 |
| KOF96 | kof96ae | `kof96aeg` | `NeoInit`,無轉換 |
| KOF97 | kof97s / kof97jhph / kof971v1 | `kof97` | `NeoInit`,無轉換 |
| KOF97 | kof97orh | `kof97ubp` | 一個位元組補丁,見下 |
| KOF98 | kof98pls / s / h / plsc / king | `kof98h` | `NeoInit`,無轉換 |
| KOF98 | kof98c2025 | `kof98cp` | 額外映射,見下 |
| KOF99 | kof99t | `kof99fd` | `NeoInit`,無轉換 |
| KOF2000 | kof2000t / kof2000s | `kof2000t` | `NeoInit`,無轉換 |
| KOF2000 | kof2000sp | `kof2ksp` | `NeoInit`,無轉換 |
| KOF2001 | kof2001s | `kof98h` | `NeoInit`,無轉換 |
| KOF2002 | kf2k2pp / prsp / kai / p33 | `kof2k2g` | `NeoInit`,無轉換 |
| KOF99 | kof99ae | `kof99aeg` | `NeoInit`,無轉換 |
| KOF2003 | kof2003t | `kof2003tg` | `NeoInit`,無轉換 |

所有槽位的加密旗標(CMC42 / CMC50 / ENCRYPTED_M1 / SMA / PVC)**全部是
空的**,C / M1 / S1 / V 都是解密態。KOF2002 三套的 V 用 PCM2 解密後的
`0fc9a58d` / `b8c475a4`;KOF2002 的 C 是 CMC50 離線解密後的 `265-c*d`。

### v4.1 修正:kof2001s 從擾動態改為解密態

v4.0 以前 kof2001s 掛 `kof98` 槽位,而 `kof98Init` 會裝上 `kof98Decrypt`
—— 那正是交接文件 §2.4 記的同一個位址置換(連保留前 `0x800` 檔頭的處理
都一樣)。所以它的 `242-p1.p1` 在包裡是**擾動態**,燒到實機不會動。

v4.1 改為:離線反擾動成 1MB 明文,改掛 `kof98h`(不做任何轉換),
`242-p1.p1`(2MB,`23b75d9f`)→ `242-pn1.p1`(1MB,`cd6b12eb`),
`242-m1.m1` 改名 `242-mg1.m1` 以符合槽位。實測 73/73,畫面正常。
`parts/` 也因此少 1MB。

**這裡有個會騙人的地方:** 擾動刻意保留前 `0x800`,所以 SP / PC /
`NEO-GEO` 標記在擾動前後完全相同,單看檔頭永遠判成「明文」。可靠指標是
指令密度 —— 反擾動前常見 opcode 佔 38%,反擾動後 77%。反擾動工具見
`tools/decrypt_p.py`(與 kof2000s / kof2003t 用的是同一支)。

### v4.2 更正:kof98c2025 不需要重定位

v4.1 曾寫「`kof98cp` 槽位會 `NeoMapExtraRom(0x900000, 0x40000)`,P3 落在
記憶卡窗口,要比照 kof95sp 重定位」—— **這是錯的**。

實際查證:kof98c2025 的來源快取裡**根本沒有 sp2b 也沒有 p3**,只有
p1(1MB)與 p2(4MB)。包裡那兩個檔是為了滿足 `kof98cp` 的 RomDesc 而
補的全零填充:

| 檔案 | CRC | 內容 |
|---|---|---|
| `242-p2cp.sp2b` | `1147406a` | 4MB 全 `0x00`(= 4MB 零的 CRC32) |
| `242-p3cp.p3` | `e20eea22` | 256KB 全 `0x00` |

它的 p2(4MB)正好落在 image `0x100000`–`0x4FFFFF`,與 `sp2a` 的位置
完全一致,所以掛 `kof98cp` 就行。`$900000` 映射到的是 256KB 的零 ——
沒有東西要重定位。

v4.2 起這兩個填充區改由 builder 生成,`parts/` 少 4.25MB;它們不是改版
獨有內容,本來就不該當成資料收藏。

### ※ kof98c2025 超出 CHA512Y 規格

真正擋住它上實機的不是 P3,是 **C ROM 有 12 顆共 96MB**,超過 CHA512Y
的 8×8MiB = 64MB 上限(V 也有 5 顆 20MB)。

| | C 顆數 / 總量 | 可上 CHA512Y |
|---|---|---|
| kof98c2025 | 12 顆 / 96MB | ✗ |
| 其餘 25 套 | ≤ 8 顆 / ≤ 64MB | ✓ |

依「能否在 PCB 上重現」的判準,這一套只供模擬器使用。

### v4.3:kof97orh 的計時器 bug 已修正

`kof97ubp` 槽位的 Init 會執行 `Neo68KROMActive[0x0263bb] = 0x65`。查證後
確認那是**修 bug**,不是改遊戲設計,所以 v4.3 起直接套進 `parts/`,
燒到實機也能得到正確行為。

`Neo68KROMActive` 存的是**檔案序(字組交換)**,所以該索引打的是 68K
`$0263BA` 的**運算碼**,不是位移量:

```
0x6B = 0110 1011b   條件碼 1011 = MI
0x65 = 0110 0101b   條件碼 0101 = CS

$0263B4: 122d283a   move.b $283a(a5), d1     ; 讀計時器(BCD)
$0263B8: 8300       sbcd.b d0, d1            ; BCD 減 1
$0263BA: 6b1a       bmi.b $263d6             ; GOTVG 原始
$0263BA: 651a       bcs.b $263d6             ; 修正後
```

分支目標不變(都是 `$263D6`,即「時間到」處理:設旗標、`clr.b $283a(a5)`
清計時器、起 300 幀倒數),變的只有判斷條件。

**為什麼 `bmi` 是錯的:** M68000 手冊定義 `SBCD` 之後 `C` 是十進位借位、
而 `N` 是 **Undefined**。實作上 N 取結果的 bit 7,於是:

| 計時 | 減 1 後 | N | C | `bmi` | `bcs` |
|---|---|---|---|---|---|
| 99 | 98 | 1 | 0 | **會跳** | 不會跳 |
| 90 | 89 | 1 | 0 | **會跳** | 不會跳 |
| 80 | 79 | 0 | 0 | 不會跳 | 不會跳 |
| 00 | 99 | 1 | 1 | 會跳 | 會跳 |

用 `bmi`,計時器只要落在 81–99 就立刻誤判成時間到 —— 99 秒制的回合第一個
tick 就結束。`bcs` 只在真正借位(`00` → `99`)時才跳,才是正確的。

`232-p1ubp.p1` 的 CRC 因此從 `a7e3ba54` 變為 `159aef93`(單一位元組差異)。
FBNeo 之後仍會寫入同一個值,冪等,模擬器行為完全不變 —— 重測 kof97orh
仍是 73/73、541 色,與修正前一致。

**尚未處理的相關問題:** `sbcd` 會連 X 旗標一起減,而 `$0263A0`–`$0263B8`
之間沒有任何指令清 X(`cmpi` / `moveq` / `move` 都不碰 X),X 是從先前
流程帶過來的,理論上偶爾會減 2。FBNeo 也沒補這個,實測沒觀察到問題,
但上實機值得留意。

---

## v3.5:CMC50 / PCM2 離線解密

kof2002kai 出貨時 C 是 CMC50 加密、p2 是 `PCM2DecryptP` 重排。兩者都在
離線處理完才收錄,做法照 FBNeo `neo_decrypt.cpp` / `d_neogeo.cpp` 逐行實作。

**驗證方式:拿原版 kof2002 當對照組。** 手邊同時有加密的 `kof2002.zip`
與已知正確的解密結果,可以完全比對:

| 對象 | 輸入 | 輸出 | 期望 | 結果 |
|---|---|---|---|---|
| CMC50 C(8 顆) | `265-c1..c8` | — | `265-c1d`~`c8d` | 8/8 相符 |
| S1 抽取 | 解密後 C | — | `e0eaaba3` | 相符 |
| PCM2DecryptP | `327266b8` | `432fdf53` | `432fdf53` | 相符 |

CMC50 的 `extra_xor` 是 **`0xb0`** 不是 `0xec`。原始碼註解
`CMC50 -- 32, b0, 2b, a9 -- ec` 的欄位是「計算值四項 -- OLDXOR」,
`2b`/`a9` 是 CMC50 的識別常數,所以第二欄 `b0` 才是 `nNeoProtectionXor`;
`ec` 是 OLDXOR,關係為 `0xec ^ 0x5c = 0xb0`。取錯欄會得到 0/8。

### 重要:加密態的 C ROM CRC 不能用來判斷獨有性

kof2002kai 的加密 c1–c8 **CRC 全部未登錄**,看起來像 8 顆獨有的 8MB。
但解密後 6 顆是原版、2 顆是已知的公開檔。

原因是 CMC50 的位址 XOR 影響 bit 0–23,會把資料散佈到**整個 64MB
sprite 空間**,不受單顆 ROM 邊界限制。只要 c1/c2 的內容改了,加密後的
位元組就會散進全部八顆檔案。

**所以對 CMC42 / CMC50 加密的套件,必須先解密才能判斷有沒有獨有內容。**
若照加密態的 CRC 收錄,kof2002kai 會多佔 `parts/` 64MB —— 實際只需 5MB。

---

## v5.1:V ROM 一律 4MB、新增兩套

**核心目標是做出實體卡(PROGBK1 + CHA512Y),FBNeo 只是驗證手段。** 這一版
把配置全面對齊實體板子的限制。

### V ROM 拆成 4MB —— PROGBK1 放不下 8MB

有四套的 V 是 8MB:`kf2k2pp` / `kof2002kai` / `kof2002prsp`(各 2 顆)與
`kof2003t`(同)。其餘世代原本就都在 4MB 以內。

新增 manifest 的 **`split`** 欄位(`crc -> {from, offset, length}`),由
builder 從池裡的來源檔直接切出,**不佔任何分發量** —— 思路同既有的
`zerofill`:能生成的就不進分發物。V ROM 是連續的 ADPCM 位址空間,切幾顆不
影響資料排列,已用 md5 驗證 `4×4MB 串接 == 2×8MB 串接`。manifest 版本
因此由 5 升為 6。

代價是驅動:那三套 KOF2002 原本掛 FBNeo 現成的 `kof2k2fd`(宣告 2 顆 8MB
V),拆完就對不上,改為自建的 `kof2k2g`;`kof2003tg.c` 的 V 宣告也由
`2×0x800000` 改為 `4×0x400000`。也就是說這四套從「改名即可」變成「必須
自己編 FBNeo」——**但實體卡本來就不經過 FBNeo,這個代價只影響試玩。**

### 新增 kof2002p33(KOF2002 CopyMix,8C 版)

原本因「10 顆 8MB C = 80MB,PCB 做不了」而未收錄。實測 c9 / c10 未被引用,
砍成 8 顆後是 64MB,**剛好貼齊 CHA512Y 上限**,硬體理由不再成立。

差分成本 **75KB**,且不需要新的原版 romset:c1/c2 與 `kof2002t` 相同;
c3~c8 / p1 / p2d / s1d / m1 對 `kof2002t` 做差分(各 0.6~17KB);**V1~V4
正好就是拆 8MB V 時產生的那四個 `split` 半塊**,成本為零。ROM 配置與
`kof2k2g` 完全一致,所以共用同一個槽位,不必再建驅動。

> 順帶更正一個說法:這套的 8 顆 C **並非**與官方解密版 `kof2k2fd` 相同 ——
> 逐顆比對只有 c1/c2 吻合,串接後的 64MB sprite 空間有 142,039 個位元組
> (0.21%)不同,集中在第 7、8 顆(各約 4.5%)。差異很小,但確實存在,
> 這也是差分只要 75KB 的原因。

### 新增 kof99ae(KOF99 AE 版,8C 版)

官方 `kof99ae` 是 12 顆 C(96MB)加一顆 p3,超過 CHA512Y 上限。本包收的是
砍到 8 顆 C(64MB)、且不含 p3 的版本 —— 來源檔裡 c9~c12 本來就是整片
`0x00`(各 8MB,CRC 都是 `1ad2bc45`),原本在那裡的圖素已搬進 c7/c8,所以
`c7ae` / `c8ae` 的差分特別大(1.2MB / 0.8MB)。

差分成本 **2.47MB**,同樣不需要新的原版:基準全部落在已必備的 `kof99` 與
`kof99fd`。自建驅動 `kof99aeg`。

### 順帶修掉 pick_originals.py 的一個真實缺陷

它的最小覆蓋只保證 `sources` 的 CRC,**沒把差分基準與 `split` 來源算進
需求**,於是可能挑到「對 `sources` 等價、卻不含某個基準」的替代 romset。
實際踩到了:它挑 `kof2003t.zip` 代替 `kof2k3fd.zip`,但前者沒有
`271-p1d.p1`(`0d0a5861` 的差分基準),導致 kof2003t 組不出來。已修正。

### 驗證

把 `parts/` 完全移開、只靠 `deltas/`、`split`、`zerofill` 與自備原版組建:

```
26 套 / 401 個檔   CRC 全部正確,零錯誤
V ROM >4MB : 無
C ROM >64MB: 僅 kof98c2025(96MB,已知且已記載)
```

| 世代 | 差分數 | 還原後 | 差分後 | 省 |
|---|---:|---:|---:|---:|
| KOF95 | 2 | 2.1MB | 0.02MB | 99.1% |
| KOF96 | 16 | 61.5MB | 16.52MB | 73.1% |
| KOF97 | 13 | 60.1MB | 2.09MB | 96.5% |
| KOF98 | 36 | 189.8MB | 10.42MB | 94.5% |
| KOF99 | 12 | 46.4MB | 2.41MB | 94.8% |
| KOF2000 | 17 | 91.5MB | 18.12MB | 80.2% |
| KOF2001 | 5 | 17.4MB | 0.05MB | 99.7% |
| KOF2002 | 17 | 80.2MB | 0.08MB | 99.9% |
| KOF2003 | 3 | 7.0MB | 1.27MB | 81.9% |
| **合計** | **121** | **556.0MB** | **50.98MB** | **90.8%** |

---

## v5:分片改以對原版的 bsdiff 差分分發

原本 `parts/` 收的是改版獨有的**原始二進位區塊**(101 個檔 / 457.5MB)——
那些是可以獨立存在的 ROM 資料。v5 改成只收「改版相對於原版 ROM 的差異」,
沒有原版就還原不出任何東西。

**體積:457.5MB -> 48.5MB,省 89.4%。** 分世代打包後最大的是
`deltas-kof2000.zip` 18.1MB,最小的 `deltas-kof99.zip` 只有 639 bytes。

| 世代 | 差分數 | 還原後 | 差分後 | 省 |
|---|---:|---:|---:|---:|
| KOF95 | 2 | 2.1MB | 0.02MB | 99.1% |
| KOF96 | 16 | 61.5MB | 16.52MB | 73.1% |
| KOF97 | 13 | 60.1MB | 2.09MB | 96.5% |
| KOF98 | 36 | 189.8MB | 10.42MB | 94.5% |
| KOF99 | 2 | 1.1MB | 0.00MB | 100.0% |
| KOF2000 | 17 | 91.5MB | 18.12MB | 80.2% |
| KOF2001 | 5 | 17.4MB | 0.05MB | 99.7% |
| KOF2002 | 7 | 27.0MB | 0.01MB | 100.0% |
| KOF2003 | 3 | 7.0MB | 1.27MB | 81.9% |
| **合計** | **101** | **457.5MB** | **48.50MB** | **89.4%** |

差距的原因明確:KOF99 / 2001 / 2002 的基準是直系的解密版原版(`kof99fd`、
`kof2k1fd`、`kof2002t`),幾乎逐位元組相同;KOF97 / 98 的原版是明文,改版
只改少數位元組;KOF96 與 KOF2000 差得多,是因為基準為 **CMC 加密態**而分片
是解密態,位址被打散,只能靠位元組值的統計結構壓。

> **已知未最佳化:基準選得不是最好。** `make_deltas.py` 的候選策略是
> 「同副檔名且同大小 → 同副檔名 → 同族同大小 → 任意同大小」,取到就停,
> 不會再去看跨槽位的更好選擇。最明顯的是 KOF2003:那三個分片其實是原版
> 那顆 8MB `271-p1d.p1` 的切片,拿它當基準可以趨近 100%,但只有 `p3` 選中
> 了,`p1` / `p2` 仍停在 81.9%。
>
> 全池搜尋(對每個分片試更多候選再取最小)實測可再省約 7.7MB,但在樹莓派
> 上要跑數小時,**目前刻意不做** —— 48.5MB 已經夠小,而且這不影響正確性,
> 每個差分都驗過 CRC。要自己跑的話,把候選策略改成不提前停止即可。

**基準以 CRC 記錄,不記檔名或 romset 名。** 還原時由 builder 在 POOL 裡依
內容反查,和專案其餘部分一致 —— `kof2k3fd` 與 `kof2003t` 這種等價來源自然
就通用。基準不限同槽位:`kof98c2025` 的 `c9`~`c12` 原版沒有對應槽位,拿
kof98 的 `c3`~`c6` 當基準仍有 56~93%;`kof2003t` 的 p1/p2/p3 其實是原版
那顆 8MB `271-p1d.p1` 的切片,差分趨近於零。

**還原不新增相依套件。** BSDIFF40 格式只是 magic 加三個 bzip2 區塊,所以
builder 內建純 Python 的 bspatch,只用標準庫。效能關鍵是 64KB 分塊:
bsdiff 的 add 段要逐位元組相加,但改版通常只改少數位元組、整段幾乎全是 0,
以 64KB 為單位檢查、全零區塊直接整段複製 —— 8MB 的 C ROM 因此從數十秒降到
0.2~1.7 秒。

**順帶修掉一個收錄缺陷。** 產生差分時發現有三個分片的最佳基準 CRC 與自己
相同,也就是那些「改版獨有區塊」其實與原版逐位元組相同:`265-v1.v1`、
`265-v2.v2`(= kof2002t 的 v1d/v2d)、`242-p2.sp2`(= kof2k1fd 的 pg2)。
當初建 manifest 時手邊沒有 kof2002t / kof2k1fd,所以看起來像獨有內容。
已登錄進 `sources`,分片數 104 -> 101、還原後體積 477.5 -> 457.5MB。

**驗證:** 把 `parts/` 完全移開、只靠 `deltas/` 與 `originals/` 組建,
26 套 / 401 個檔的 CRC **全部正確,零錯誤**。

---

## v4.4:改走完整 FBNeo romset + `pick_originals.py`

取得原版的流程從「自己照著對照表一個一個挑」改成「整包丟進去,程式挑」。

**新增 `pick_originals.py`。** 掃 `romset/`(或指定目錄)內每個 zip 的每個
檔,依 CRC32 對照 `manifest.json` 的 `sources`,挑出需要的 zip 硬連結進
`originals/`。與 builder 同樣**完全依內容比對,不看檔名、不看 romset 名**,
所以 SPLIT / MERGED / NON-MERGED 都吃得下。挑選走最小覆蓋,同一個檔在多個
zip 都有時只取貢獻最多的那個。`--needed` 不掃描,直接列出該準備哪 14 個
zip 與大小,供 torrent 客戶端先勾選,不必為了 549.5MB 下載整包幾十 GB。

**對官方 DAT 做了完整校驗。** 隨包附上 `dats/FinalBurn Neo (ClrMame Pro
XML, Neogeo only).dat`(`<version>1.0.0.03</version>`,680 個條目)。拿
`manifest.json` 的 CRC 逐一比對的結果:

- 14 個來源 set **全部存在於 DAT**,全部 CRC **命中、零缺漏**
- 每個檔**都實體存在於自己的 zip,零 `merge=` 繼承** —— 所以 **SPLIT
  romset 就足夠**,`kof2002t` / `kof2k3fd` 雖是 `kof2002` / `kof2003` 的
  clone,**不需要**額外準備那兩個母集 zip
- `kof2003t` 與 `kof2k3fd` 是等價來源,兩者都實體含有要用的 12 個檔

**取消三個從未發布的補充包。** 詳見下一節。

**順帶記錄一個跨世代相依。** `kof96ae` 借用 `kof2001` 的 `262-v4` 當自己的
`214-v4aeg.v4`,所以組 KOF96 也要 `kof2001.zip`。這種相依光看套件名或檔名
都推不出來,`--needed` 會在「供應世代」欄標成 `96, 2001`。

---

## v3.2 的母集補充包 —— v4.4 起取消

v3.2 曾規劃三個補充包(`kof94-extra.zip`、`kof2001-decrypted.zip`、
`kof2002-decrypted.zip`),理由是 kof94 / 2001 / 2002 缺的檔雖然是 FBNeo
已登錄的公開資料、照去重原則不進 `parts/`,但一般發行的加密版母集裡也沒有。

**這三包實際上從未隨包發布過** —— repo、Releases、磁碟上都沒有,文件卻一直
寫著「隨附」,使用者照著找只會撲空。v4.4 把這個承諾整個移除,原因有二:

1. **不需要。** 對 FBNeo 1.0.0.03 官方 DAT 實查過,`kof94nr2`、`kof2k1fd`、
   `kof2002t` 全都是 DAT 內的正規 set,完整 romset 裡本來就有;而且要用的
   檔全部實體存在於自己的 zip、零 `merge=` 繼承,SPLIT romset 就拿得到。
2. **不該做。** 那三包的內容純粹是原版 ROM 資料的重新封裝,與本包「只收改版
   獨有內容」的收錄原則相衝突。

改由 `pick_originals.py` 從使用者自有的完整 romset 裡挑,見「使用方式」。

---

## 已知問題

### 無

26 套全部可組裝並通過逐檔 CRC 驗證。`manifest.json` 裡每一個 CRC 都有
出處:不在 `parts/` 的,`sources` 都指得出來源 romset。v3 曾有 4 個無來源
的檔案(kof2001s),v3.1 已修復。

### 其他

- 部分套件的 CRC 與 FBNeo 驅動定義不同,載入時需關閉 CRC 檢查,
  或放在 `<system>/fbneo/patched/` 由檔名比對載入。
- 未收錄:kf2k1allboss(16 顆 8MB C = 128MB,PCB 做不了)、
  kof2002p33(10 顆 8MB C = 80MB,同上)、kovplus(PGM 平台)。
