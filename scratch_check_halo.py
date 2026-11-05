import struct
from pathlib import Path

pmx_path = Path("SARA/resources/app/assets/characters/evelyn/model.pmx")
data = pmx_path.read_bytes()
offset = 0
sig = data[offset:offset+4]; offset += 4
ver = struct.unpack_from('<f', data, offset)[0]; offset += 4
info_len = data[offset]; offset += 1
info = data[offset:offset+info_len]; offset += info_len
encoding = 'utf-16le' if info[0] == 0 else 'utf-8'
add_vec4_count = info[1]
vert_index_size = info[2]
tex_index_size = info[3]
mat_index_size = info[4]
bone_index_size = info[5]
morph_index_size = info[6]
rigid_index_size = info[7]

def read_text():
    global offset
    t_len = struct.unpack_from('<I', data, offset)[0]; offset += 4
    t = data[offset:offset+t_len].decode(encoding, errors='ignore'); offset += t_len
    return t

for _ in range(4): read_text()
vert_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
verts = []
for _ in range(vert_count):
    p = struct.unpack_from('<3f', data, offset); offset += 12
    normal = struct.unpack_from('<3f', data, offset); offset += 12
    uv = struct.unpack_from('<2f', data, offset); offset += 8
    offset += (16 * add_vec4_count)
    w_type = data[offset]; offset += 1
    if w_type == 0: offset += bone_index_size
    elif w_type == 1: offset += bone_index_size * 2 + 4
    elif w_type in [2, 4]: offset += bone_index_size * 4 + 16
    elif w_type == 3: offset += bone_index_size * 2 + 4 + 36
    offset += 4
    verts.append(p)

face_idx_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
face_indices = []
for _ in range(face_idx_count):
    idx = struct.unpack_from('<H' if vert_index_size==2 else ('<B' if vert_index_size==1 else '<I'), data, offset)[0]
    offset += vert_index_size
    face_indices.append(idx)

tex_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
textures = [read_text() for _ in range(tex_count)]

mat_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
materials = []
for _ in range(mat_count):
    m_name = read_text(); m_name_en = read_text()
    offset += 16 + 12 + 4 + 12 + 1 + 16 + 4
    tex_idx = struct.unpack_from('<b' if tex_index_size==1 else ('<h' if tex_index_size==2 else '<i'), data, offset)[0]; offset += tex_index_size
    offset += tex_index_size + 1
    toon_flag = data[offset]; offset += 1
    if toon_flag == 0: offset += tex_index_size
    else: offset += 1
    read_text()
    elem_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
    materials.append({"name": m_name, "name_en": m_name_en, "elem_count": elem_count, "tex_idx": tex_idx})

ys = [v[1] for v in verts]
print(f"Total vertices: {len(verts)}, Y range: [{min(ys):.2f}, {max(ys):.2f}]")

# Check bone names to see if halo bone exists
bone_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
bones = []
for _ in range(bone_count):
    b_name = read_text(); b_name_en = read_text()
    b_pos = struct.unpack_from('<3f', data, offset); offset += 12
    parent_idx = struct.unpack_from('<b' if bone_index_size==1 else ('<h' if bone_index_size==2 else '<i'), data, offset)[0]; offset += bone_index_size
    transform_layer = struct.unpack_from('<i', data, offset)[0]; offset += 4
    bone_flags = struct.unpack_from('<H', data, offset)[0]; offset += 2
    if bone_flags & 0x0001: offset += bone_index_size
    else: offset += 12
    if bone_flags & (0x0100 | 0x0200): offset += bone_index_size + 4
    if bone_flags & 0x0400: offset += 12
    if bone_flags & 0x0800: offset += 24
    if bone_flags & 0x2000: offset += 4
    if bone_flags & 0x0020:
        offset += bone_index_size + 8
        cnt = struct.unpack_from('<i', data, offset)[0]; offset += 4
        for _ in range(cnt):
            offset += bone_index_size
            if data[offset]: offset += 25
            else: offset += 1
    bones.append({"name": b_name, "name_en": b_name_en, "pos": b_pos, "parent": parent_idx})

print(f"Total bones: {len(bones)}")
head_bones = [b for b in bones if b["pos"][1] > 18.0]
for b in head_bones[:10]:
    print(f"  Bone: {b['name']} ({b['name_en']}) pos={b['pos']}")
