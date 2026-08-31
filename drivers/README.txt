drivers/ —— 給 FBNeo 用的驅動定義,builder 不會碰這裡
================================================================

本包產出的 zip 是靠「改名成某個 FBNeo 已有的 romset 名稱」來掛載的,借用
該 romset 的 ROM 配置(manifest.json 裡每套的 host 欄)。24 套裡有 22 套
借得到現成槽位,直接改名即可。

有兩套借不到 —— FBNeo 裡沒有配置相符的 romset,必須自行加驅動並重建 FBNeo:

  kof96aeg.c    給 kof96ae 用
  kof2003tg.c   給 kof2003t 用

沒有編進去的話,那兩套組出來也載不進 FBNeo;其餘 22 套不受影響。


為什麼配置對不上
----------------------------------------------------------------

kof96ae
  C ROM 是 6 顆 8MB,而原版 kof96 是 8 顆 4MB;sp2 也是 4MB(原版 2MB)。
  這是 CHA512Y 那類大容量板子的佈局,FBNeo 裡沒有現成的 kof96 變體長這樣。
  那 6 個 8MB 區塊就是 PCB 的燒錄單位,內部已做好奇偶配對(c1+c3 / c2+c4…)。

kof2003t
  程式 ROM 拆成 p1(1MB)+ p2(4MB)+ p3(2MB),全部是解密態,而且自帶 s1。
  原版 kof2003 走 PVC 加密、s1 由 C ROM 即時生成,兩者完全不同。
  驅動用 NeoInit(不做任何解密轉換),並加上 HARDWARE_SNK_ALTERNATE_TEXT
  告訴 FBNeo「這套有自己的 s1,不要從 C 生成」。

  用 NeoInit 而非會解密的 init,是本包「產出全部為解密態、載入時不做任何
  轉換」這條原則的一部分 —— 詳見 README.md 的「產出狀態」。


怎麼編進去
----------------------------------------------------------------

把 .c 的內容併進 FBNeo 的 Neo Geo 驅動原始碼(src/burn/drv/neogeo/ 底下,
一般是 d_neogeo.cpp),再重新建置 FBNeo 執行檔。

編好之後,把 out/kof96ae.zip 改名為 kof96aeg.zip、out/kof2003t.zip 改名為
kof2003tg.zip 再載入。載入名稱一律以 build_kof-GOTVG_offline_pack.py 的
輸出為準。
