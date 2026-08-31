// KOF2002 系 GOTVG 改版共用槽位(kf2k2pp / kof2002kai / kof2002prsp)。
// 與 FBNeo 現成的 kof2k2fd 差別只在 V:PROGBK1 的 V 槽位放不下 8MB,所以
// 拆成 4 顆 4MB。資料排列不變(V ROM 是連續的 ADPCM 位址空間),由 builder
// 從原版 kof2002t 那兩顆 8MB 直接切出,不佔任何分發量。
//
// 三套共用這一個槽位,所以下表的 p1 / p2d / c1d / c2d 只對得上其中一套
// (這裡取 kf2k2pp)。載入另外兩套時請關閉 CRC 檢查,或放到
// <system>/fbneo/patched/ 由檔名比對載入 —— 與本包其餘共用槽位的做法一致。
static struct BurnRomInfo kof2k2gRomDesc[] = {
	{ "265-p1.p1",		0x100000, 0x9c805b4e, 1 | BRF_ESS | BRF_PRG },
	{ "265-p2d.sp2",		0x400000, 0x0a189c94, 1 | BRF_ESS | BRF_PRG },

	{ "265-s1d.s1",		0x020000, 0xe0eaaba3, 2 | BRF_GRA },

	{ "265-c1d.c1",		0x800000, 0x7efa6ef7, 3 | BRF_GRA },
	{ "265-c2d.c2",		0x800000, 0xaa82948b, 3 | BRF_GRA },
	{ "265-c3d.c3",		0x800000, 0x959fad0b, 3 | BRF_GRA },
	{ "265-c4d.c4",		0x800000, 0xefe6a468, 3 | BRF_GRA },
	{ "265-c5d.c5",		0x800000, 0x74bba7c6, 3 | BRF_GRA },
	{ "265-c6d.c6",		0x800000, 0xe20d2216, 3 | BRF_GRA },
	{ "265-c7d.c7",		0x800000, 0x8a5b561c, 3 | BRF_GRA },
	{ "265-c8d.c8",		0x800000, 0xbef667a3, 3 | BRF_GRA },

	{ "265-m1.m1",		0x020000, 0x1c661a4b, 4 | BRF_ESS | BRF_PRG },

	{ "265-v1d.v1",		0x400000, 0x13d98607, 5 | BRF_SND },
	{ "265-v2d.v2",		0x400000, 0x9cf74677, 5 | BRF_SND },
	{ "265-v3d.v3",		0x400000, 0x8e9448b5, 5 | BRF_SND },
	{ "265-v4d.v4",		0x400000, 0x067271b5, 5 | BRF_SND },
};

STDROMPICKEXT(kof2k2g, kof2k2g, neogeo)
STD_ROM_FN(kof2k2g)

struct BurnDriver BurnDrvKof2k2g = {
	"kof2k2g", "kof2002", "neogeo", NULL, "2002",
	"The King of Fighters 2002 (GOTVG, 4x4MB V)\0", NULL, "hack", "Neo Geo MVS",
	NULL, NULL, NULL, NULL,
	BDF_GAME_WORKING | BDF_CLONE | BDF_HACK, 2, HARDWARE_PREFIX_CARTRIDGE | HARDWARE_SNK_NEOGEO, GBF_VSFIGHT, FBF_KOF,
	NULL, kof2k2gRomInfo, kof2k2gRomName, NULL, NULL, NULL, NULL, neogeoInputInfo, neogeoDIPInfo,
	NeoInit, NeoExit, NeoFrame, NeoRender, NeoScan, &NeoRecalcPalette,
	0x1000, 304, 224, 4, 3
};
