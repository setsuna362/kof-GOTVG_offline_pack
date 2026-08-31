drivers/ —— 給 FBNeo 用的驅動定義,builder 不會碰這裡
================================================================

本包產出的 zip 是靠「改名成某個 FBNeo 已有的 romset 名稱」來掛載的,借用
該 romset 的 ROM 配置(manifest.json 裡每套的 host 欄)。24 套裡有 22 套
借得到現成槽位,直接改名即可。

有五套借不到 —— FBNeo 裡沒有配置相符的 romset,必須自行加驅動並重建 FBNeo:

  kof96aeg.c    給 kof96ae 用
  kof2003tg.c   給 kof2003t 用
  kof2k2g.c     給 kf2k2pp / kof2002kai / kof2002prsp 三套共用

沒有編進去的話,那幾套組出來也載不進 FBNeo;其餘 19 套不受影響。

本包的核心目標是做出實體卡(PROGBK1 + CHA512Y),FBNeo 驅動是用來驗證與
試玩的;所以配置一律以實體板子的限制為準,不是以模擬器方便為準。


為什麼配置對不上
----------------------------------------------------------------

kof96ae
  C ROM 是 6 顆 8MB,而原版 kof96 是 8 顆 4MB;sp2 也是 4MB(原版 2MB)。
  這是 CHA512Y 那類大容量板子的佈局,FBNeo 裡沒有現成的 kof96 變體長這樣。
  那 6 個 8MB 區塊就是 PCB 的燒錄單位,內部已做好奇偶配對(c1+c3 / c2+c4…)。

kf2k2pp / kof2002kai / kof2002prsp
  ROM 配置與 FBNeo 現成的 kof2k2fd 只差在 V:kof2k2fd 宣告 2 顆 8MB,而
  PROGBK1 的 V 槽位放不下 8MB,必須拆成 4 顆 4MB。資料排列完全不變 ——
  V ROM 是連續的 ADPCM 位址空間,切幾顆不影響內容(已用 md5 驗證 4x4MB
  串接等於 2x8MB 串接),由 builder 從原版直接切出,不佔任何分發量。

  三套共用同一個槽位,所以驅動表裡的 p1 / p2d / c1d / c2d 只對得上其中
  一套。載入另外兩套要關閉 CRC 檢查,或放到 <system>/fbneo/patched/ 由
  檔名比對載入 —— 與本包其餘共用槽位的做法一致。

kof2003t
  程式 ROM 拆成 p1(1MB)+ p2(4MB)+ p3(2MB),全部是解密態,而且自帶 s1。
  V 同樣拆成 4 顆 4MB(原因同上)。
  原版 kof2003 走 PVC 加密、s1 由 C ROM 即時生成,兩者完全不同。
  驅動用 NeoInit(不做任何解密轉換),並加上 HARDWARE_SNK_ALTERNATE_TEXT
  告訴 FBNeo「這套有自己的 s1,不要從 C 生成」。

  用 NeoInit 而非會解密的 init,是本包「產出全部為解密態、載入時不做任何
  轉換」這條原則的一部分 —— 詳見 README.md 的「產出狀態」。


怎麼編進去
----------------------------------------------------------------

把 .c 的內容併進 FBNeo 的 Neo Geo 驅動原始碼(src/burn/drv/neogeo/ 底下,
一般是 d_neogeo.cpp),再重新建置 FBNeo 執行檔。

編好之後把產出的 zip 改名成對應的載入名稱再載入:

  out/kof96ae.zip      -> kof96aeg.zip
  out/kof2003t.zip     -> kof2003tg.zip
  out/kf2k2pp.zip      -> kof2k2g.zip
  out/kof2002kai.zip   -> kof2k2g.zip
  out/kof2002prsp.zip  -> kof2k2g.zip

載入名稱一律以 build_kof-GOTVG_offline_pack.py 的輸出為準,它會在結尾列出
哪幾套需要自建驅動。
