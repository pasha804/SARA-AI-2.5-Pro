import struct
import math
from pathlib import Path

def add_halo_to_pmx(src_path: Path, dst_path: Path):
    data = src_path.read_bytes()
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
        nonlocal offset
        t_len = struct.unpack_from('<I', data, offset)[0]; offset += 4
        t = data[offset:offset+t_len].decode(encoding, errors='ignore'); offset += t_len
        return t

    def encode_text(t: str) -> bytes:
        raw = t.encode(encoding)
        return struct.pack('<I', len(raw)) + raw

    # Header texts
    header_offset = offset
    model_name = read_text()
    model_name_en = read_text()
    comment = read_text()
    comment_en = read_text()
    header_bytes = data[:offset]

    # Vertices
    vert_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
    vert_data_start = offset
    for _ in range(vert_count):
        offset += 12 + 12 + 8 + (16 * add_vec4_count)
        w_type = data[offset]; offset += 1
        if w_type == 0: offset += bone_index_size
        elif w_type == 1: offset += bone_index_size * 2 + 4
        elif w_type in [2, 4]: offset += bone_index_size * 4 + 16
        elif w_type == 3: offset += bone_index_size * 2 + 4 + 36
        offset += 4 # edge
    vert_data = data[vert_data_start:offset]

    # Face indices
    face_idx_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
    face_data_start = offset
    offset += face_idx_count * vert_index_size
    face_data = data[face_data_start:offset]

    # Textures
    tex_start = offset
    tex_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
    for _ in range(tex_count): read_text()
    tex_data = data[tex_start:offset]

    # Materials
    mat_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
    mat_data_start = offset
    materials = []
    for _ in range(mat_count):
        m_start = offset
        m_name = read_text(); m_name_en = read_text()
        offset += 16 + 12 + 4 + 12 + 1 + 16 + 4 + tex_index_size + tex_index_size + 1 + 1
        toon_flag = data[offset - 1]
        if toon_flag == 0: offset += tex_index_size
        else: offset += 1
        read_text()
        elem_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
        materials.append(data[m_start:offset])

    # Rest of data (Bones, Morphs, Frames, RigidBodies, Constraints)
    rest_data = data[offset:]

    # Find Head Bone index [16] 頭
    # Head bone is at index 16
    head_bone_idx = 16

    # Generate Halo Torus Geometry
    # Major radius R = 1.05, Minor radius r = 0.045
    # Center = (0.0, 23.15, 0.45), tilted ~10 degrees forward (around X axis)
    R = 1.05
    r = 0.045
    cx, cy, cz = 0.0, 23.15, 0.45
    tilt_rad = math.radians(10.0)

    n_seg = 48  # around the ring
    n_rad = 12  # around the tube

    new_vertices = []
    halo_verts_bytes = bytearray()

    for i in range(n_seg):
        theta = (2.0 * math.pi * i) / n_seg
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)

        for j in range(n_rad):
            phi = (2.0 * math.pi * j) / n_rad
            cos_p = math.cos(phi)
            sin_p = math.sin(phi)

            # Untilted Torus coordinates
            px = (R + r * cos_p) * cos_t
            py = r * sin_p
            pz = (R + r * cos_p) * sin_t

            # Apply tilt around X axis
            # y' = y*cos - z*sin
            # z' = y*sin + z*cos
            t_py = py * math.cos(tilt_rad) - pz * math.sin(tilt_rad)
            t_pz = py * math.sin(tilt_rad) + pz * math.cos(tilt_rad)

            # Final world position
            vx = cx + px
            vy = cy + t_py
            vz = cz + t_pz

            # Normal vector
            nx = cos_p * cos_t
            ny = sin_p * math.cos(tilt_rad) - (cos_p * sin_t) * math.sin(tilt_rad)
            nz = sin_p * math.sin(tilt_rad) + (cos_p * sin_t) * math.cos(tilt_rad)

            # UV coordinates
            u = i / n_seg
            v = j / n_rad

            # Pack vertex
            v_bytes = bytearray()
            v_bytes += struct.pack('<3f', vx, vy, vz)
            v_bytes += struct.pack('<3f', nx, ny, nz)
            v_bytes += struct.pack('<2f', u, v)
            if add_vec4_count > 0:
                v_bytes += b'\x00' * (16 * add_vec4_count)
            # Bone weight: BDEF1 attached 100% to head_bone_idx
            v_bytes += b'\x00' # w_type = 0 (BDEF1)
            if bone_index_size == 1:
                v_bytes += struct.pack('<b', head_bone_idx)
            elif bone_index_size == 2:
                v_bytes += struct.pack('<h', head_bone_idx)
            else:
                v_bytes += struct.pack('<i', head_bone_idx)
            v_bytes += struct.pack('<f', 1.0) # edge scale

            halo_verts_bytes += v_bytes

    # Generate Faces (triangles)
    halo_faces_bytes = bytearray()
    face_count = 0
    base_vert_idx = vert_count

    for i in range(n_seg):
        next_i = (i + 1) % n_seg
        for j in range(n_rad):
            next_j = (j + 1) % n_rad

            # 4 vertices of the quad
            v0 = base_vert_idx + (i * n_rad + j)
            v1 = base_vert_idx + (next_i * n_rad + j)
            v2 = base_vert_idx + (next_i * n_rad + next_j)
            v3 = base_vert_idx + (i * n_rad + next_j)

            # Two triangles: (v0, v1, v2) and (v0, v2, v3)
            for vi in [v0, v1, v2, v0, v2, v3]:
                if vert_index_size == 1:
                    halo_faces_bytes += struct.pack('<B', vi)
                elif vert_index_size == 2:
                    halo_faces_bytes += struct.pack('<H', vi)
                else:
                    halo_faces_bytes += struct.pack('<I', vi)
                face_count += 1

    # Create Halo Material
    # Radiant white/cyan glow
    halo_mat_bytes = bytearray()
    halo_mat_bytes += encode_text("光环")
    halo_mat_bytes += encode_text("Halo")
    halo_mat_bytes += struct.pack('<4f', 1.0, 1.0, 1.0, 1.0) # diffuse RGBA
    halo_mat_bytes += struct.pack('<3f', 1.0, 1.0, 1.0)       # specular RGB
    halo_mat_bytes += struct.pack('<f', 40.0)                 # shininess
    halo_mat_bytes += struct.pack('<3f', 0.9, 0.95, 1.0)      # ambient (glowing white-blue)
    halo_mat_bytes += b'\x01'                                 # flags (both faces)
    halo_mat_bytes += struct.pack('<4f', 0.7, 0.9, 1.0, 1.0) # edge color (cyan glow)
    halo_mat_bytes += struct.pack('<f', 1.5)                  # edge size
    # Texture index: -1 (no texture, pure material color)
    if tex_index_size == 1: halo_mat_bytes += struct.pack('<b', -1)
    elif tex_index_size == 2: halo_mat_bytes += struct.pack('<h', -1)
    else: halo_mat_bytes += struct.pack('<i', -1)
    # Sphere texture index: -1
    if tex_index_size == 1: halo_mat_bytes += struct.pack('<b', -1)
    elif tex_index_size == 2: halo_mat_bytes += struct.pack('<h', -1)
    else: halo_mat_bytes += struct.pack('<i', -1)
    halo_mat_bytes += b'\x00' # sphere mode 0 (none)
    halo_mat_bytes += b'\x01' # toon flag 1 (internal toon)
    halo_mat_bytes += b'\x00' # toon 0
    halo_mat_bytes += encode_text("SARA 3D Celestial Halo Ring") # memo
    halo_mat_bytes += struct.pack('<I', face_count) # element count

    # Assemble new PMX file
    out = bytearray()
    out += header_bytes

    # New vertices
    total_verts = vert_count + (n_seg * n_rad)
    out += struct.pack('<I', total_verts)
    out += vert_data
    out += halo_verts_bytes

    # New face indices
    total_faces = face_idx_count + face_count
    out += struct.pack('<I', total_faces)
    out += face_data
    out += halo_faces_bytes

    # Textures (unchanged)
    out += tex_data

    # Materials
    total_mats = mat_count + 1
    out += struct.pack('<I', total_mats)
    for m in materials:
        out += m
    out += halo_mat_bytes

    # Rest of data (bones, morphs, etc.)
    out += rest_data

    dst_path.write_bytes(out)
    print(f"Successfully injected Halo into PMX: {total_verts} verts, {total_faces} face indices, {total_mats} materials.")

if __name__ == "__main__":
    src = Path("sara_app_backup/assets/characters/evelyn/model.pmx")
    dst1 = Path("SARA/resources/app/assets/characters/evelyn/model.pmx")
    dst2 = Path("SARA/resources/app/dist/assets/characters/evelyn/model.pmx")
    add_halo_to_pmx(src, dst1)
    add_halo_to_pmx(src, dst2)
