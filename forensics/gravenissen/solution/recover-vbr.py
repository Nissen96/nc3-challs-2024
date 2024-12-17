import struct

with open("../src/filgraven.raw", "rb") as f:
    data = list(f.read())

# File system is clearly NTFS but is missing a VBR
# Just a few fields are needed for other tools to recover the file automatically

# Sector and cluster size can be easily found through inspection
SECTOR_SIZE = 512
CLUSTER_SIZE = 512

# Fix sector size (default)
data[0xB:0xD] = struct.pack("<h", SECTOR_SIZE)

# Fix sectors per cluster
data[0xD] = CLUSTER_SIZE // SECTOR_SIZE

# Set sectors per MFT entry (default)
data[0x40] = 2

# Find and fix MFT entry cluster
mfts = []
for i in range(0, len(data), CLUSTER_SIZE):
    if data[i + 0xF2:i + 0xFC] == list("$MFT\x00".encode("utf-16-le")):
        mfts.append(i // CLUSTER_SIZE)

assert len(mfts) == 2  # There are two MFT copies, a mirror and the normal
data[0x30:0x38] = struct.pack("<q", mfts[1])  # Any of those two works here

# Fix signature
data[510:512] = [0x55, 0xAA]

# This is enough to recover the entire file system!
for i in range(32):
    print(bytes(data[i*16:(i+1)*16]).hex(" "), "\t", bytes(data[i*16:(i+1)*16]))


with open("recovered.raw", "wb") as f:
    f.write(bytes(data))
