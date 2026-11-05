import struct
from pathlib import Path

pmx_path = Path("SARA/resources/app/assets/characters/evelyn/model.pmx")
data = pmx_path.read_bytes()

offset = 0
sig = data[offset:offset+4]; offset += 4
ver = struct.unpack_from('<f', data, offset)[0]; offset += 4
info_len = data[offset]; offset += 1
info = data[offset:offset+info_len]; offset += info_len

encoding_idx = info[0] # 0 = UTF16LE, 1 = UTF8
encoding = 'utf-16le' if encoding_idx == 0 else 'utf-8'

def read_text():
    global offset
    t_len = struct.unpack_from('<I', data, offset)[0]; offset += 4
    t = data[offset:offset+t_len].decode(encoding, errors='ignore'); offset += t_len
    return t

model_name = read_text()
model_name_en = read_text()
comment = read_text()
comment_en = read_text()

print(f"Model Name: {model_name} | {model_name_en}")

# Vertex Count
vert_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
print(f"Vertex Count: {vert_count}")

# Skip vertices:
# Vertex format depends on info flags:
add_vec4_count = info[1]
weight_type_info = info[2]
bone_index_size = info[5]

# Vertex size:
# Pos(12) + Normal(12) + UV(8) + add_vec4(16*count) + weight + edge_scale(4)
# Let's inspect vertices
for _ in range(vert_count):
    offset += 12 + 12 + 8 + (16 * add_vec4_count)
    w_type = data[offset]; offset += 1
    if w_type == 0: # BDEF1
        offset += bone_index_size
    elif w_type == 1: # BDEF2
        offset += bone_index_size * 2 + 4
    elif w_type == 2: # BDEF4
        offset += bone_index_size * 4 + 16
    elif w_type == 3: # SDEF
        offset += bone_index_size * 2 + 4 + 12 + 12 + 12
    elif w_type == 4: # QDEF
        offset += bone_index_size * 4 + 16
    offset += 4 # edge scale

# Surface / Face Count
face_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
vert_index_size = info[3]
offset += face_count * vert_index_size
print(f"Face Indices Count: {face_count}")

# Textures
tex_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
textures = []
for _ in range(tex_count):
    textures.append(read_text())
print("Textures in PMX:", textures)

# Materials
mat_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
materials = []
tex_index_size = info[4]
for _ in range(mat_count):
    m_name = read_text()
    m_name_en = read_text()
    diffuse = struct.unpack_from('<4f', data, offset); offset += 16
    specular = struct.unpack_from('<3f', data, offset); offset += 12
    specular_strength = struct.unpack_from('<f', data, offset)[0]; offset += 4
    ambient = struct.unpack_from('<3f', data, offset); offset += 12
    flag = data[offset]; offset += 1
    edge_color = struct.unpack_from('<4f', data, offset); offset += 16
    edge_size = struct.unpack_from('<f', data, offset)[0]; offset += 4
    tex_idx = struct.unpack_from('<b' if tex_index_size==1 else ('<h' if tex_index_size==2 else '<i'), data, offset)[0]; offset += tex_index_size
    sphere_tex_idx = struct.unpack_from('<b' if tex_index_size==1 else ('<h' if tex_index_size==2 else '<i'), data, offset)[0]; offset += tex_index_size
    sphere_mode = data[offset]; offset += 1
    toon_flag = data[offset]; offset += 1
    if toon_flag == 0:
        offset += tex_index_size
    else:
        offset += 1
    memo = read_text()
    elem_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
    materials.append((m_name, m_name_en, elem_count, tex_idx, sphere_tex_idx))

print("\nMaterials in PMX:")
for idx, m in enumerate(materials):
    tex_str = textures[m[3]] if 0 <= m[3] < len(textures) else "none"
    print(f"  [{idx}] {m[0]} ({m[1]}) - Faces: {m[2]} - Texture: {tex_str}")

# Bones
bone_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
bones = []
for b_i in range(bone_count):
    b_name = read_text()
    b_name_en = read_text()
    b_pos = struct.unpack_from('<3f', data, offset); offset += 12
    parent_idx = struct.unpack_from('<b' if bone_index_size==1 else ('<h' if bone_index_size==2 else '<i'), data, offset)[0]; offset += bone_index_size
    transform_layer = struct.unpack_from('<i', data, offset)[0]; offset += 4
    bone_flags = struct.unpack_from('<H', data, offset)[0]; offset += 2
    # handle flags
    if bone_flags & 0x0001: # indexed connection
        offset += bone_index_size
    else:
        offset += 12 # position offset
    if bone_flags & (0x0100 | 0x0200): # rotate/translate parent
        offset += bone_index_size + 4
    if bone_flags & 0x0400: # fixed axis
        offset += 12
    if bone_flags & 0x0800: # local axis
        offset += 24
    if bone_flags & 0x2000: # deform outside
        offset += 4
    if bone_flags & 0x0020: # IK
        offset += bone_index_size
        loop_cnt = struct.unpack_from('<i', data, offset)[0]; offset += 4
        limit_rad = struct.unpack_from('<f', data, offset)[0]; offset += 4
        link_cnt = struct.unpack_from('<i', data, offset)[0]; offset += 4
        for _ in range(link_cnt):
            offset += bone_index_size
            has_limit = data[offset]; offset += 1
            if has_limit:
                offset += 24
    bones.append((b_name, b_name_en, b_pos, parent_idx))

print(f"\nTotal Bones: {len(bones)}")
hair_bones = [b for b in bones if any(k in b[0].lower() or k in b[1].lower() for k in ['hair', '髪', 'ツイン', '前髪', '後髪'])]
print(f"Hair Bones ({len(hair_bones)}):")
for hb in hair_bones[:20]:
    print(f"  Bone: {hb[0]} ({hb[1]}) - Pos: {hb[2]}")
