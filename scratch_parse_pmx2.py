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

print(f"vert_idx: {vert_index_size}, tex_idx: {tex_index_size}, bone_idx: {bone_index_size}")

def read_text():
    global offset
    t_len = struct.unpack_from('<I', data, offset)[0]; offset += 4
    t = data[offset:offset+t_len].decode(encoding, errors='ignore'); offset += t_len
    return t

model_name = read_text()
model_name_en = read_text()
comment = read_text()
comment_en = read_text()
print(f"Model: {model_name}")

vert_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
print(f"Vertex Count: {vert_count}")

# Skip vertices
for _ in range(vert_count):
    offset += 12 + 12 + 8 + (16 * add_vec4_count)
    w_type = data[offset]; offset += 1
    if w_type == 0: offset += bone_index_size
    elif w_type == 1: offset += bone_index_size * 2 + 4
    elif w_type == 2: offset += bone_index_size * 4 + 16
    elif w_type == 3: offset += bone_index_size * 2 + 4 + 12 + 12 + 12
    elif w_type == 4: offset += bone_index_size * 4 + 16
    offset += 4 # edge scale

face_idx_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
offset += face_idx_count * vert_index_size
print(f"Face Indices Count: {face_idx_count}")

tex_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
textures = []
for _ in range(tex_count):
    textures.append(read_text())
print("Textures:", textures)

mat_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
materials = []
for m_i in range(mat_count):
    m_name = read_text()
    m_name_en = read_text()
    diffuse = struct.unpack_from('<4f', data, offset); offset += 16
    specular = struct.unpack_from('<3f', data, offset); offset += 12
    spec_strength = struct.unpack_from('<f', data, offset)[0]; offset += 4
    ambient = struct.unpack_from('<3f', data, offset); offset += 12
    flag = data[offset]; offset += 1
    edge_color = struct.unpack_from('<4f', data, offset); offset += 16
    edge_size = struct.unpack_from('<f', data, offset)[0]; offset += 4
    tex_idx = struct.unpack_from('<b' if tex_index_size==1 else ('<h' if tex_index_size==2 else '<i'), data, offset)[0]; offset += tex_index_size
    sphere_tex_idx = struct.unpack_from('<b' if tex_index_size==1 else ('<h' if tex_index_size==2 else '<i'), data, offset)[0]; offset += tex_index_size
    sphere_mode = data[offset]; offset += 1
    toon_flag = data[offset]; offset += 1
    if toon_flag == 0: offset += tex_index_size
    else: offset += 1
    memo = read_text()
    elem_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
    materials.append((m_name, m_name_en, elem_count, tex_idx, sphere_tex_idx))

print("\nMaterials:")
for idx, m in enumerate(materials):
    tex_str = textures[m[3]] if 0 <= m[3] < len(textures) else "none"
    print(f"  [{idx}] {m[0]} ({m[1]}) - Faces: {m[2]} - Tex: {tex_str}")
