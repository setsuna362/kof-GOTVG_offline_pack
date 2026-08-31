"""GOTVG 的 P 位址置換解密。
適用:kof2000s、kof2003t(兩者用同一支平台回呼 0x10218400 / 0x1022A290)
本質即 FBNeo kof98Decrypt 的位址置換部分。
輸入:快取的 2MB P1 區塊(原序,未做 word swap)
輸出:1MB 明文 pg1

驗證基準:
              kof2000s              kof2003t
  輸入 CRC    1e863428              f06326d1
  輸出 CRC    d39ebe18              cadb0a2f
  SP/PC       0x0010F300/0x00C00402 同左
  0x100       "NEO-GEO"             "NEO-GEO"
"""

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

def decrypt_p(raw2mb):
    tmp = bytearray(0x100000)
    for i in range(0x100000):
        tmp[i] = raw2mb[jmap(i)]
    out = bytearray(raw2mb[:0x100000])
    out[0x800:0x100000] = tmp[0x800:0x100000]   # 前 0x800 保留原始檔頭
    return bytes(out)
