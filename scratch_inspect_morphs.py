import struct, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

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

model_name = read_text(); read_text(); read_text(); read_text()
vert_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
for _ in range(vert_count):
    offset += 12 + 12 + 8 + (16 * add_vec4_count)
    w_type = data[offset]; offset += 1
    if w_type == 0: offset += bone_index_size
    elif w_type == 1: offset += bone_index_size * 2 + 4
    elif w_type in [2, 4]: offset += bone_index_size * 4 + 16
    elif w_type == 3: offset += bone_index_size * 2 + 4 + 36
    offset += 4

face_idx_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
offset += face_idx_count * vert_index_size

tex_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
for _ in range(tex_count): read_text()

mat_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
for _ in range(mat_count):
    read_text(); read_text()
    offset += 16 + 12 + 4 + 12 + 1 + 16 + 4 + tex_index_size + tex_index_size + 1 + 1
    toon_flag = data[offset - 1]
    if toon_flag == 0: offset += tex_index_size
    else: offset += 1
    read_text()
    offset += 4

bone_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
for _ in range(bone_count):
    read_text(); read_text()
    offset += 12 + bone_index_size + 4
    flags = struct.unpack_from('<H', data, offset)[0]; offset += 2
    if flags & 0x0001: offset += bone_index_size
    else: offset += 12
    if flags & (0x0100 | 0x0200): offset += bone_index_size + 4
    if flags & 0x0400: offset += 12
    if flags & 0x0800: offset += 24
    if flags & 0x2000: offset += 4
    if flags & 0x0020:
        offset += bone_index_size + 8
        cnt = struct.unpack_from('<i', data, offset)[0]; offset += 4
        for _ in range(cnt):
            offset += bone_index_size
            if data[offset]: offset += 25
            else: offset += 1

morph_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
print('Total morphs:', morph_count)
for i in range(morph_count):
    m_name = read_text()
    m_name_en = read_text()
    panel = data[offset]; offset += 1
    m_type = data[offset]; offset += 1
    elem_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
    for _ in range(elem_count):
        if m_type == 0: offset += morph_index_size + 4
        elif m_type == 1: offset += vert_index_size + 12
        elif m_type == 2: offset += bone_index_size + 12 + 16
        elif m_type == 3: offset += vert_index_size + 16
        elif m_type == 8: offset += mat_index_size + 1 + 16 + 12 + 4 + 12 + 16 + 4 + 16 + 16 + 16
    print(f'[{i:02d}] name="{m_name}" en="{m_name_en}" panel={panel} type={m_type} elems={elem_count}')
