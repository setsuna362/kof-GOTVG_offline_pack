// kof99ae(Anniversary Edition,GOTVG)—— FBNeo 現成的 kof99ae 配置對不上:
// 官方那套是 12 顆 C(96MB)加一顆 p3,超過 CHA512Y 的 8x8MB 上限,做不成
// 實體卡。本包收的是砍到 8 顆 C(64MB,剛好貼齊上限)、且不含 p3 的版本 ——
// 原本在 c9~c12 的圖素已搬進 c7/c8,那四顆在來源檔裡本來就是整片 0x00。
//
// 素材全為解密態,故用 NeoInit,不做任何載入時轉換;s1 隨包提供而非由 C
// 生成,所以需要 ALTERNATE_TEXT(與 kof99fd 槽位同樣的處理)。
static struct BurnRomInfo kof99aegRomDesc[] = {
	{ "152-p1ae.p1",		0x100000, 0x549f3184, 1 | BRF_ESS | BRF_PRG },
	{ "152-p2ae.sp2",		0x400000, 0xcdde0ad4, 1 | BRF_ESS | BRF_PRG },

	{ "251-s1ae.s1",		0x020000, 0x3c31ee43, 2 | BRF_GRA },

	{ "251-c1ae.c1",		0x800000, 0x7eabea6c, 3 | BRF_GRA },
	{ "251-c2ae.c2",		0x800000, 0xe5a5bc5c, 3 | BRF_GRA },
	{ "251-c3d.c3",		0x800000, 0xb047c9d5, 3 | BRF_GRA },
	{ "251-c4d.c4",		0x800000, 0x6bc8e4b1, 3 | BRF_GRA },
	{ "251-c5d.c5",		0x800000, 0x9746268c, 3 | BRF_GRA },
	{ "251-c6d.c6",		0x800000, 0x238b3e71, 3 | BRF_GRA },
	{ "251-c7ae.c7",		0x800000, 0xcd40fe9b, 3 | BRF_GRA },
	{ "251-c8ae.c8",		0x800000, 0x9e3b8fe3, 3 | BRF_GRA },

	{ "251-m1ae.m1",		0x020000, 0xf847e188, 4 | BRF_ESS | BRF_PRG },

	{ "251-v1ae.v1",		0x400000, 0xceaa3bae, 5 | BRF_SND },
	{ "251-v2ae.v2",		0x400000, 0x07d70650, 5 | BRF_SND },
	{ "251-v3.v3",		0x400000, 0x821901da, 5 | BRF_SND },
	{ "251-v4.v4",		0x200000, 0xb49e6178, 5 | BRF_SND },
};

STDROMPICKEXT(kof99aeg, kof99aeg, neogeo)
STD_ROM_FN(kof99aeg)

struct BurnDriver BurnDrvKof99aeg = {
	"kof99aeg", "kof99", "neogeo", NULL, "1999",
	"The King of Fighters '99 (Anniversary, GOTVG, 8C)\0", NULL, "hack", "Neo Geo MVS",
	NULL, NULL, NULL, NULL,
	BDF_GAME_WORKING | BDF_CLONE | BDF_HACK, 2, HARDWARE_PREFIX_CARTRIDGE | HARDWARE_SNK_NEOGEO | HARDWARE_SNK_ALTERNATE_TEXT, GBF_VSFIGHT, FBF_KOF,
	NULL, kof99aegRomInfo, kof99aegRomName, NULL, NULL, NULL, NULL, neogeoInputInfo, neogeoDIPInfo,
	NeoInit, NeoExit, NeoFrame, NeoRender, NeoScan, &NeoRecalcPalette,
	0x1000, 304, 224, 4, 3
};
