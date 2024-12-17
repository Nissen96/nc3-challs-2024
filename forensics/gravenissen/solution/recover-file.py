import struct

with open("../src/filgraven.raw", "rb") as f:
    data = f.read()

# File system is clearly NTFS but is missing a VBR
# File can be recovered directly through parsing the file system manually

def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val

# Sector and cluster size can be easily found through inspection
SECTOR_SIZE = 512
CLUSTER_SIZE = 512

class MFTEntry:
    def __init__(self, raw_data: bytes):
        self.raw_entry = self.fixup(raw_data)
        self.filename = ""
        self.filesize = 0
        self.data_runs = []
        self.parse_attributes()

    def fixup(self, data):
        fixup_offset = struct.unpack("<h", data[4:6])[0]
        fixup_entries = struct.unpack("<h", data[6:8])[0]
        fixup_signature = data[fixup_offset:fixup_offset + 2]
        for i in range(fixup_entries - 1):
            assert data[i * 512 + 510:(i + 1) * 512] == fixup_signature
            fixup_entry = data[fixup_offset + 2 * (i + 1):fixup_offset + 2 * (i + 2)]
            data = data[:i * 512 + 510] + fixup_entry + data[(i + 1) * 512:]
        return data

    def parse_attributes(self):
        offset = struct.unpack("<h", self.raw_entry[0x14:0x16])[0]
        while True:
            attr_type = self.raw_entry[offset:offset + 4]
            if attr_type == b"\xFF\xFF\xFF\xFF":
                break

            attr_size = struct.unpack("<i", self.raw_entry[offset + 4:offset + 8])[0]

            if attr_type == b"\x30\x00\x00\x00":
                # Filename attribute
                assert self.raw_entry[offset + 8] == 0  # Assume resident filename
                content_offset = offset + struct.unpack("<h", self.raw_entry[offset + 0x14: offset + 0x16])[0]
                name_len = self.raw_entry[content_offset + 64]
                name = self.raw_entry[content_offset + 66:content_offset + 66 + name_len * 2]

                self.filename = name.decode("utf-16-le")
            elif attr_type == b"\x80\x00\00\x00":
                # Data attribute
                assert self.raw_entry[offset + 8] == 1  # Only handle non-resident

                runlist_offset = struct.unpack("<h", self.raw_entry[offset + 32:offset + 34])[0]
                self.filesize = struct.unpack("<q", self.raw_entry[offset + 48:offset + 56])[0]

                ptr = offset + runlist_offset
                while (lengths := self.raw_entry[ptr]) != 0:
                    size_length, offset_length = lengths & 0xf, (lengths >> 4)
                    ptr += 1

                    n_clusters = self.raw_entry[ptr:ptr + size_length]
                    n_clusters = int(n_clusters[::-1].hex(), 16)
                    ptr += size_length

                    cluster_offset = self.raw_entry[ptr:ptr + offset_length]
                    # Cluster offset is relative to previous, in two's complement
                    cluster_offset = twos_comp(int(cluster_offset[::-1].hex(), 16), offset_length * 8)
                    ptr += offset_length

                    self.data_runs.append((cluster_offset, n_clusters))

            offset += attr_size

        assert self.filename != ""


# Parse file MFT entries
entries = {}
for i in range(0, len(data), CLUSTER_SIZE):
    if data[i:i + 4] != b"FILE":
        continue

    try:
        mft = MFTEntry(data[i:i + 1024])
    except AssertionError:
        continue

    entries[mft.filename] = mft

# Let's see if any file seems interesting
print(list(entries.keys()))

# Recover the interesting file from its data runs
image = entries["gravenissen.png"]
content = b""
pos = 0
for offset, length in image.data_runs:
    pos += offset
    content += data[pos * CLUSTER_SIZE:(pos + length) * CLUSTER_SIZE]
    #print(offset * CLUSTER_SIZE, length, (offset + length) * CLUSTER_SIZE, len(content))

content = content[:image.filesize]

with open("gravenissen.png", "wb") as f:
    f.write(content)
