import struct
from pathlib import Path

pmx_path = Path("SARA/resources/app/assets/characters/evelyn/model.pmx")
data = bytearray(pmx_path.read_bytes())

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

def read_text():
    global offset
    t_len = struct.unpack_from('<I', data, offset)[0]; offset += 4
    t = data[offset:offset+t_len].decode(encoding, errors='ignore'); offset += t_len
    return t

read_text(); read_text(); read_text(); read_text()

vert_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
vert_start_offset = offset

# Read vertex positions
vert_positions = []
vert_offsets = []

for v_i in range(vert_count):
    v_off = offset
    pos = struct.unpack_from('<3f', data, offset)
    vert_offsets.append(v_off)
    vert_positions.append(pos)
    offset += 12 + 12 + 8 + (16 * add_vec4_count)
    w_type = data[offset]; offset += 1
    if w_type == 0: offset += bone_index_size
    elif w_type == 1: offset += bone_index_size * 2 + 4
    elif w_type in [2, 4]: offset += bone_index_size * 4 + 16
    elif w_type == 3: offset += bone_index_size * 2 + 4 + 12 + 12 + 12
    offset += 4

face_idx_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
face_indices = []
for _ in range(face_idx_count):
    idx = struct.unpack_from('<H' if vert_index_size==2 else ('<B' if vert_index_size==1 else '<I'), data, offset)[0]
    offset += vert_index_size
    face_indices.append(idx)

tex_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
for _ in range(tex_count): read_text()

mat_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
face_offset = 0

for m_i in range(mat_count):
    m_name = read_text()
    m_name_en = read_text()
    offset += 16 + 12 + 4 + 12 + 1 + 16 + 4 + tex_index_size + tex_index_size + 1
    toon_flag = data[offset]; offset += 1
    if toon_flag == 0: offset += tex_index_size
    else: offset += 1
    read_text() # memo
    elem_count = struct.unpack_from('<I', data, offset)[0]; offset += 4

    if m_i in [28, 29, 30]:
        mat_indices = face_indices[face_offset:face_offset + elem_count]
        unique_v = set(mat_indices)
        ys = [vert_positions[vi][1] for vi in unique_v]
        zs = [vert_positions[vi][2] for vi in unique_v]
        xs = [vert_positions[vi][0] for vi in unique_v]
        print(f"Material {m_i}: {m_name_en} - {len(unique_v)} verts:")
        print(f"  Y: [{min(ys):.2f}, {max(ys):.2f}] | Z: [{min(zs):.2f}, {max(zs):.2f}] | X: [{min(xs):.2f}, {max(xs):.2f}]")

    face_offset += elem_count
