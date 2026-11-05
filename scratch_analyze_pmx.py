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

model_name = read_text()
model_name_en = read_text()
comment = read_text()
comment_en = read_text()

vert_count = struct.unpack_from('<I', data, offset)[0]; offset += 4

# Vertices
vertices = []
for v_i in range(vert_count):
    pos = struct.unpack_from('<3f', data, offset); offset += 12
    normal = struct.unpack_from('<3f', data, offset); offset += 12
    uv = struct.unpack_from('<2f', data, offset); offset += 8
    offset += (16 * add_vec4_count)
    w_type = data[offset]; offset += 1
    if w_type == 0:
        bones = [struct.unpack_from('<b' if bone_index_size==1 else ('<h' if bone_index_size==2 else '<i'), data, offset)[0]]
        offset += bone_index_size
        weights = [1.0]
    elif w_type == 1:
        b1 = struct.unpack_from('<b' if bone_index_size==1 else ('<h' if bone_index_size==2 else '<i'), data, offset)[0]; offset += bone_index_size
        b2 = struct.unpack_from('<b' if bone_index_size==1 else ('<h' if bone_index_size==2 else '<i'), data, offset)[0]; offset += bone_index_size
        w1 = struct.unpack_from('<f', data, offset)[0]; offset += 4
        bones = [b1, b2]; weights = [w1, 1.0 - w1]
    elif w_type in [2, 4]:
        bs = [struct.unpack_from('<b' if bone_index_size==1 else ('<h' if bone_index_size==2 else '<i'), data, offset + k*bone_index_size)[0] for k in range(4)]
        offset += bone_index_size * 4
        ws = struct.unpack_from('<4f', data, offset); offset += 16
        bones = bs; weights = ws
    elif w_type == 3:
        b1 = struct.unpack_from('<b' if bone_index_size==1 else ('<h' if bone_index_size==2 else '<i'), data, offset)[0]; offset += bone_index_size
        b2 = struct.unpack_from('<b' if bone_index_size==1 else ('<h' if bone_index_size==2 else '<i'), data, offset)[0]; offset += bone_index_size
        w1 = struct.unpack_from('<f', data, offset)[0]; offset += 4
        offset += 12 + 12 + 12 # SDEF params
        bones = [b1, b2]; weights = [w1, 1.0 - w1]
    offset += 4 # edge scale
    vertices.append((pos, normal, uv, bones, weights))

face_idx_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
face_indices = []
for _ in range(face_idx_count):
    idx = struct.unpack_from('<H' if vert_index_size==2 else ('<B' if vert_index_size==1 else '<I'), data, offset)[0]
    offset += vert_index_size
    face_indices.append(idx)

tex_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
textures = []
for _ in range(tex_count):
    textures.append(read_text())

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
    materials.append({
        "name": m_name, "name_en": m_name_en, "elem_count": elem_count,
        "tex_idx": tex_idx, "tex_name": textures[tex_idx] if 0 <= tex_idx < len(textures) else ""
    })

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
    if bone_flags & 0x0001: offset += bone_index_size
    else: offset += 12
    if bone_flags & (0x0100 | 0x0200): offset += bone_index_size + 4
    if bone_flags & 0x0400: offset += 12
    if bone_flags & 0x0800: offset += 24
    if bone_flags & 0x2000: offset += 4
    if bone_flags & 0x0020:
        offset += bone_index_size
        offset += 4 + 4
        link_cnt = struct.unpack_from('<i', data, offset)[0]; offset += 4
        for _ in range(link_cnt):
            offset += bone_index_size
            has_limit = data[offset]; offset += 1
            if has_limit: offset += 24
    bones.append({"name": b_name, "name_en": b_name_en, "pos": b_pos, "parent": parent_idx})

out = []
out.append(f"Model Name: {model_name}")
out.append(f"Vertex Count: {len(vertices)}, Face Indices: {len(face_indices)}")
out.append("\nTextures:")
for i, t in enumerate(textures):
    out.append(f"  [{i}] {t}")
out.append("\nMaterials:")
face_offset = 0
for idx, m in enumerate(materials):
    mat_indices = face_indices[face_offset:face_offset + m["elem_count"]]
    mat_verts = set(mat_indices)
    ys = [vertices[vi][0][1] for vi in mat_verts]
    min_y = min(ys) if ys else 0
    max_y = max(ys) if ys else 0
    out.append(f"  [{idx}] {m['name']} ({m['name_en']}) - Faces: {m['elem_count']} - Tex: {m['tex_name']} - Y range: [{min_y:.2f}, {max_y:.2f}]")
    face_offset += m["elem_count"]

out.append(f"\nBones ({len(bones)}):")
for b_i, b in enumerate(bones):
    if any(k in b["name"] or k in b["name_en"].lower() for k in ['hair', '髪', '頭', 'neck', 'waist', '腰']):
        out.append(f"  [{b_i}] {b['name']} ({b['name_en']}) pos={b['pos']}")

Path("pmx_info.txt").write_text("\n".join(out), encoding="utf-8")
print("Saved PMX analysis to pmx_info.txt")
