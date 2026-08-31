#!/usr/bin/env python3
"""
kof95sp P3 relocator
====================
Moves the 128KB extra program ROM (084-p3sp.p3, mapped by FBNeo/HBMAME at
$900000 in the memory-card address window) into a zero-filled hole GSC2007
left inside P2 at $283000, producing a *standard* 2MB Neo Geo P-ROM layout
that needs no custom mapping (real cart / NeoSD / MiSTer compatible).

Also applies the two FBNeo kof95PatchCallback() fixes so the ROM does not
depend on the GOTVG platform's illegal-opcode hooks:
  1. lone 4E7C word in P1 -> 4E75 (RTS)
  2. `jmp $901750` @ $03E750 -> 2B7C 0003 E7FA
     (= move.l #$3E7FA,$500(a5), consuming the orphan 0500 word at $3E756,
      byte-identical to what FBNeo executes)

Usage: relocate_p3.py <sp_dir> <out_dir>
  sp_dir must contain 084-p1sp.p1 / 084-p2d.sp2 / 084-p3sp.p3 (word-swapped,
  as stored in kof95sp.zip).
"""
import sys, struct, pathlib, zlib
from capstone import Cs, CS_ARCH_M68K, CS_MODE_M68K_000

OLD_BASE   = 0x900000
NEW_BASE   = 0x283000            # inside the zeroed hole $282FFA-$289000 of P2
P3_USED    = 0x2660              # payload really ends at 0x2641; round to 0x20
DELTA      = NEW_BASE - OLD_BASE
HOLE_END   = 0x289000
HOOK_SITE  = 0x03E750            # jmp $901750 in P1
FBNEO_STUB = bytes.fromhex("2B7C0003E7FA")

EXPECT_CRC = {'084-p1sp.p1': 0xb3c26333, '084-p2d.sp2': 0x5cb1af9e,
              '084-p3sp.p3': 0x7eddc5d8}

md = Cs(CS_ARCH_M68K, CS_MODE_M68K_000)

def bswap16(d: bytes) -> bytes:
    a = bytearray(d); a[0::2], a[1::2] = d[1::2], d[0::2]; return bytes(a)

def ref_opcode(op: int) -> bool:
    if op in (0x4EB9, 0x4EF9, 0x4879, 0x23FC): return True      # JSR/JMP/PEA/MOVE.L #,abs.l
    if (op & 0xF1FF) == 0x41F9: return True                      # LEA abs.l,An
    if (op & 0xF1FF) == 0x207C: return True                      # MOVEA.L #,An
    if (op >> 12) == 0x2 and (op & 0x3F) == 0x3C: return True    # MOVE.L #,<ea>
    return False

def verified_refs(img: bytes, base: int, lo=OLD_BASE, hi=OLD_BASE + 0x20000):
    """word-aligned scan + capstone confirmation that the 32-bit value is a
    genuine operand of a reference-class instruction."""
    out = []
    for i in range(0, len(img) - 3, 2):
        v = struct.unpack_from('>I', img, i)[0]
        if not (lo <= v < hi):
            continue
        op = struct.unpack_from('>H', img, i - 2)[0] if i >= 2 else 0
        if not ref_opcode(op):
            continue
        ins = next(md.disasm(img[i - 2:i + 8], base + i - 2, count=1), None)
        if ins and ins.size >= 6 and f"{v:x}" in ins.op_str.replace('$', ''):
            out.append((i, v, f"{ins.mnemonic} {ins.op_str}"))
    return out

def main(sp_dir: str, out_dir: str):
    sp, out = pathlib.Path(sp_dir), pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    raw = {}
    for n, exp in EXPECT_CRC.items():
        d = (sp / n).read_bytes()
        c = zlib.crc32(d) & 0xFFFFFFFF
        assert c == exp, f"{n}: crc {c:08x} != expected {exp:08x} (wrong romset version?)"
        raw[n] = d

    p1 = bytearray(bswap16(raw['084-p1sp.p1']))
    p2 = bytearray(bswap16(raw['084-p2d.sp2']))
    p3 = bytearray(bswap16(raw['084-p3sp.p3']))

    # sanity: destination hole must be zero
    assert set(p2[NEW_BASE - 0x200000:HOLE_END - 0x200000]) == {0}, "hole not clean"
    assert NEW_BASE + P3_USED <= HOLE_END
    assert set(p3[P3_USED:]) == {0}, "P3 payload larger than expected"

    log = []

    # --- FBNeo patch 1: illegal-opcode hook words --------------------------
    n7c = 0
    for img, nm in ((p1, 'P1'), (p3, 'P3')):
        for i in range(0, len(img), 2):
            w = struct.unpack_from('>H', img, i)[0]
            assert w != 0x4E7D, "unexpected 4E7D hook"
            if w == 0x4E7C:
                struct.pack_into('>H', img, i, 0x4E75)
                log.append(f"hook  {nm} ${i:06X}: 4E7C -> 4E75 (RTS)")
                n7c += 1
    assert n7c == 1, f"expected exactly one 4E7C, found {n7c}"

    # --- FBNeo patch 2: stub the GOTVG registration jump -------------------
    assert p1[HOOK_SITE:HOOK_SITE + 6] == bytes.fromhex("4EF900901750")
    p1[HOOK_SITE:HOOK_SITE + 6] = FBNEO_STUB
    log.append(f"hook  P1 ${HOOK_SITE:06X}: jmp $901750 -> move.l #$3E7FA,$500(a5)")

    # --- collect & retarget cross references -------------------------------
    refs1 = verified_refs(p1, 0x000000)
    refs2 = verified_refs(p2, 0x200000)
    refs3 = verified_refs(p3, OLD_BASE)
    assert not refs2, f"unexpected P2 refs: {refs2}"

    for off, v, txt in refs1:
        struct.pack_into('>I', p1, off, v + DELTA)
        log.append(f"p1ref ${off:06X}: {txt:34s} -> ${v + DELTA:06X}")
    for off, v, txt in refs3:
        struct.pack_into('>I', p3, off, v + DELTA)
        log.append(f"p3ref ${OLD_BASE + off:06X}: {txt:34s} -> ${v + DELTA:06X}")

    # --- move payload into P2 ---------------------------------------------
    dst = NEW_BASE - 0x200000
    p2[dst:dst + P3_USED] = p3[:P3_USED]
    log.append(f"blob  P3[0:{P3_USED:#x}] -> P2+{dst:#x} (68K ${NEW_BASE:06X})")

    # --- post-verification -------------------------------------------------
    leftover = verified_refs(p1, 0) + verified_refs(p2, 0x200000)
    assert not leftover, f"stale $90xxxx refs remain: {leftover}"
    moved = verified_refs(p2, 0x200000, NEW_BASE, NEW_BASE + P3_USED)
    log.append(f"check 0 refs to $900000 window remain; {len(moved)} internal refs live at new base")

    # --- emit files ---------------------------------------------------------
    (out / '084-p1sp.p1').write_bytes(bswap16(bytes(p1)))
    (out / '084-p2d.sp2').write_bytes(bswap16(bytes(p2)))
    # MAME 2MB p1 convention (like parent 084-p1.p1): file = [$200000 MB][$000000 MB]
    merged = bswap16(bytes(p2)) + bswap16(bytes(p1))
    (out / '084-p1sp2017r.p1').write_bytes(merged)
    for f in out.iterdir():
        d = f.read_bytes()
        log.append(f"out   {f.name}: {len(d):#x} bytes crc32={zlib.crc32(d) & 0xFFFFFFFF:08x}")
    (out / 'relocation.log').write_text('\n'.join(log) + '\n')
    print('\n'.join(log))
    print(f"\n{len(refs1)} P1 refs + {len(refs3)} P3 refs retargeted, delta {DELTA:+#x}")

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
