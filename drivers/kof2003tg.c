// 素材全為解密版,故用 NeoInit;s1 由 C 產生故需 ALTERNATE_TEXT
// V 拆成 4 顆 4MB —— PROGBK1 的 V 槽位放不下 8MB。資料排列不變(V ROM 是
// 連續的 ADPCM 位址空間),由 builder 從原版那兩顆 8MB 直接切出。
static struct BurnRomInfo kof2003tgRomDesc[] = {
	{ "271-p1t.p1",		0x100000, 0xcadb0a2f, 1 | BRF_ESS | BRF_PRG },
	{ "271-p2d.p2",		0x400000, 0x92ed6ee3, 1 | BRF_ESS | BRF_PRG },
	{ "271-p3d.p3",		0x200000, 0x0d0a5861, 1 | BRF_ESS | BRF_PRG },

	{ "271-s1d.s1",		0x080000, 0x3230e10f, 2 | BRF_GRA },

	{ "271-c1d.c1",		0x800000, 0xe42fc226, 3 | BRF_GRA },
	{ "271-c2d.c2",		0x800000, 0x1b5e3b58, 3 | BRF_GRA },
	{ "271-c3d.c3",		0x800000, 0xd334fdd9, 3 | BRF_GRA },
	{ "271-c4d.c4",		0x800000, 0x0d457699, 3 | BRF_GRA },
	{ "271-c5d.c5",		0x800000, 0x8a91aae4, 3 | BRF_GRA },
	{ "271-c6d.c6",		0x800000, 0x9f8674b8, 3 | BRF_GRA },
	{ "271-c7d.c7",		0x800000, 0x8ee6b43c, 3 | BRF_GRA },
	{ "271-c8d.c8",		0x800000, 0x6d8d2d60, 3 | BRF_GRA },

	{ "271-m1d.m1",		0x080000, 0xcc8b54c0, 4 | BRF_ESS | BRF_PRG },

	{ "271-v1d.v1",		0x400000, 0xdba0b938, 5 | BRF_SND },
	{ "271-v2d.v2",		0x400000, 0x71956ee2, 5 | BRF_SND },
	{ "271-v3d.v3",		0x400000, 0xddbbb199, 5 | BRF_SND },
	{ "271-v4d.v4",		0x400000, 0x01b90c4f, 5 | BRF_SND },
};

STDROMPICKEXT(kof2003tg, kof2003tg, neogeo)
STD_ROM_FN(kof2003tg)

struct BurnDriver BurnDrvKof2003tg = {
	"kof2003tg", "kof2003", "neogeo", NULL, "2003",
	"The King of Fighters 2003 (Optimized, GOTVG)\0", NULL, "bootleg", "Neo Geo MVS",
	NULL, NULL, NULL, NULL,
	BDF_GAME_WORKING | BDF_CLONE | BDF_HACK, 2, HARDWARE_PREFIX_CARTRIDGE | HARDWARE_SNK_NEOGEO | HARDWARE_SNK_ALTERNATE_TEXT, GBF_VSFIGHT, FBF_KOF,
	NULL, kof2003tgRomInfo, kof2003tgRomName, NULL, NULL, NULL, NULL, neogeoInputInfo, neogeoDIPInfo,
	NeoInit, NeoExit, NeoFrame, NeoRender, NeoScan, &NeoRecalcPalette,
	0x1000, 304, 224, 4, 3
};
