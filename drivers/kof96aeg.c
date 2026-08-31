// 快取的 6 個 8MB 區塊即 PCB 燒錄單位(內部已是奇偶配對:c1+c3 / c2+c4 ...)
static struct BurnRomInfo kof96aegRomDesc[] = {
	{ "214-p1aeg.p1",	0x100000, 0x0de08cc3, 1 | BRF_ESS | BRF_PRG },
	{ "214-p2aeg.sp2",	0x400000, 0x221d1d54, 1 | BRF_ESS | BRF_PRG },

	{ "214-s1aeg.s1",	0x020000, 0xb9626494, 2 | BRF_GRA },

	{ "214-c1aeg.c1",	0x800000, 0xa7466eea, 3 | BRF_GRA },
	{ "214-c2aeg.c2",	0x800000, 0x6ff22256, 3 | BRF_GRA },
	{ "214-c3aeg.c3",	0x800000, 0x48d81318, 3 | BRF_GRA },
	{ "214-c4aeg.c4",	0x800000, 0xd69836e6, 3 | BRF_GRA },
	{ "214-c5aeg.c5",	0x800000, 0x8bb710f2, 3 | BRF_GRA },
	{ "214-c6aeg.c6",	0x800000, 0xfc99d445, 3 | BRF_GRA },

	{ "214-m1ae.m1",	0x020000, 0x3a4a7c21, 4 | BRF_ESS | BRF_PRG },

	{ "214-v1.v1",		0x400000, 0x63f7b045, 5 | BRF_SND },
	{ "214-v2.v2",		0x400000, 0x25929059, 5 | BRF_SND },
	{ "214-v3aeg.v3",	0x400000, 0xf85673b0, 5 | BRF_SND },
	{ "214-v4aeg.v4",	0x400000, 0x26ec4dd9, 5 | BRF_SND },
};

STDROMPICKEXT(kof96aeg, kof96aeg, neogeo)
STD_ROM_FN(kof96aeg)

struct BurnDriver BurnDrvKof96aeg = {
	"kof96aeg", "kof96", "neogeo", NULL, "2007-2020",
	"The King of Fighters '96 (Anniversary, GOTVG, 512Y)\0", NULL, "hack", "Neo Geo MVS",
	NULL, NULL, NULL, NULL,
	BDF_GAME_WORKING | BDF_CLONE | BDF_HACK, 2, HARDWARE_PREFIX_CARTRIDGE | HARDWARE_SNK_NEOGEO, GBF_VSFIGHT, FBF_KOF,
	NULL, kof96aegRomInfo, kof96aegRomName, NULL, NULL, NULL, NULL, neogeoInputInfo, neogeoDIPInfo,
	NeoInit, NeoExit, NeoFrame, NeoRender, NeoScan, &NeoRecalcPalette,
	0x1000, 304, 224, 4, 3
};
