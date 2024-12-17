import struct
import random

CLUSTER_SIZE = 512

with open("original.raw", "rb") as f:
    data = list(f.read())

# Extract image
img_offset = 0x23c1 * CLUSTER_SIZE
img_size = 0x11a1 * CLUSTER_SIZE
img = data[img_offset:img_offset + img_size].copy()

# Remove original image
data[img_offset:img_offset + img_size] = [0] * img_size

# Split image in random chunk sizes
i = 1
n = 0
runlist = [(n, i)]
chunks = [img[:CLUSTER_SIZE]]
while i < img_size // CLUSTER_SIZE:
    n += 1
    if img_size // CLUSTER_SIZE - i < 128:
        size = img_size // CLUSTER_SIZE - i
    else:
        size = random.randint(1, 127)

    runlist.append((n, size))
    chunks.append(img[i * CLUSTER_SIZE:(i + size) * CLUSTER_SIZE])
    i += size

# Shuffle ordering
random.shuffle(runlist)

# Make offset absolute (sum cummulatively) and add in random gaps
offset = 0x378200 // CLUSTER_SIZE
for i, (pos, size) in enumerate(runlist):
    offset += random.randint(30, 45)
    runlist[i] = (pos, offset, size)
    offset += size

# Stay in bounds
print(hex((runlist[-1][1] + runlist[-1][2]) * CLUSTER_SIZE))
assert (runlist[-1][1] + runlist[-1][2]) * CLUSTER_SIZE < 0x6ffe00

# Insert image chunks according to runlist
runlist.sort(key=lambda x: x[0])
runlist_bytes = b""
prev = 0
for pos, offset, size in runlist:
    data[offset * CLUSTER_SIZE:(offset + size) * CLUSTER_SIZE] = chunks[pos]

    relative_offset = offset - prev
    runlist_bytes += b"\x21" + bytes([size]) + struct.pack("<h", relative_offset)
    prev = offset

# Padding and end of attributes marker
runlist_bytes += b"\x00" * (16 - (len(runlist_bytes) % 16))
runlist_bytes += b"\xff\xff\xff\xff\x82\x79\x47\x11"

# Update MFT runlist
mft_offset = 0x25e400
data[mft_offset + 0x150:mft_offset + 0x150 + len(runlist_bytes)] = list(runlist_bytes)

# Update MFT entry size
data[mft_offset + 0x18:mft_offset + 0x1a] = struct.pack("<h", 0x150 + len(runlist_bytes))

# Update attribute length
attr_len = 64 + len(runlist_bytes) - 8
data[mft_offset + 0x114:mft_offset + 0x118] = struct.pack("<i", attr_len)

# Update fixup array
signature = data[mft_offset + 0x30:mft_offset + 0x32]
fixup_val = data[mft_offset + 0x1fe:mft_offset + 0x200]
data[mft_offset + 0x32:mft_offset + 0x34] = fixup_val
fixup_val = data[mft_offset + 0x1fe:mft_offset + 0x200] = signature

# Replace the VBR with diggy diggy
data[:113 * 72] = list(b"I'm a dwarf and I'm digging a hole, diggy diggy hole, diggy diggy hole. ") * 113

# Replace backup VBR with song
poem = b"""
Hun er en ny filsystems-(dum dum dum dum)-teknologi,
VBR i toppen med en backup om' bagi,
512 bytes per cluster, MFT saa sej,
Min NTFS, uhh, jeg elsker dig.

Jeg graved i dig foerste gang i starten af '90.
Du var federe end FAT, ja intet mig ku brems'.
Men jeg fik hakket lidt for vildt, fik smadret VBRs.
Data Run recovery, der' meget der skal laeres.

Hun er en ny filsystems-(dum dum dum dum)-teknologi,
VBR i toppen med en backup om' bagi,
512 bytes per cluster, MFT saa sej,
Min NTFS, uhh, jeg elsker dig.
"""
data[-CLUSTER_SIZE:] = list(poem)

with open("filgraven.raw", "wb") as f:
    f.write(bytes(data))
