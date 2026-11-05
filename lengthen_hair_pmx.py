import struct
from pathlib import Path

def lengthen_hair(pmx_path: Path):
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
        nonlocal offset
        t_len = struct.unpack_from('<I', data, offset)[0]; offset += 4
        t = data[offset:offset+t_len].decode(encoding, errors='ignore'); offset += t_len
        return t

    read_text(); read_text(); read_text(); read_text()

    vert_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
    vert_start_offset = offset

    # Collect vertex positions and offsets
    vert_offsets = []
    vert_positions = []
    for _ in range(vert_count):
        v_off = offset
        pos = struct.unpack_from('<3f', data, offset)
        vert_offsets.append(v_off)
        vert_positions.append(list(pos))
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

    back_hair_verts = set()
    side_hair_verts = set()

    for m_i in range(mat_count):
        read_text(); read_text()
        offset += 16 + 12 + 4 + 12 + 1 + 16 + 4 + tex_index_size + tex_index_size + 1
        toon_flag = data[offset]; offset += 1
        if toon_flag == 0: offset += tex_index_size
        else: offset += 1
        read_text()
        elem_count = struct.unpack_from('<I', data, offset)[0]; offset += 4

        if m_i == 28: # Back hair
            back_hair_verts.update(face_indices[face_offset:face_offset + elem_count])
        elif m_i == 29: # Side hair
            side_hair_verts.update(face_indices[face_offset:face_offset + elem_count])

        face_offset += elem_count

    # Transform Material 28 (Back hair) -> Waist-length flowing locks (down to Y ~ 12.8)
    back_count = 0
    for vi in back_hair_verts:
        x, y, z = vert_positions[vi]
        if y < 20.8:
            # Normalized progression from upper hair (20.8) to tip (18.72)
            t = (20.8 - y) / (20.8 - 18.72)
            t = min(1.0, max(0.0, t))
            # Smooth quadratic curve for organic drape
            curve = t * t * 0.4 + t * 0.6
            new_y = y - (curve * 5.92) # drops lowest tips right to 12.80 (waist!)
            new_z = z + (curve * 0.32) # flows outward gently over back armor
            new_x = x * (1.0 + curve * 0.15) # graceful fan-out of strands
            vert_positions[vi] = [new_x, new_y, new_z]
            struct.pack_into('<3f', data, vert_offsets[vi], new_x, new_y, new_z)
            back_count += 1

    # Transform Material 29 (Side hair) -> Flowing side locks framing ribs/waist (down to Y ~ 14.6)
    side_count = 0
    for vi in side_hair_verts:
        x, y, z = vert_positions[vi]
        if y < 20.5:
            t = (20.5 - y) / (20.5 - 18.19)
            t = min(1.0, max(0.0, t))
            curve = t * t * 0.3 + t * 0.7
            new_y = y - (curve * 3.65) # drops tips to ~14.54
            new_z = z + (curve * 0.12)
            new_x = x * (1.0 + curve * 0.10)
            vert_positions[vi] = [new_x, new_y, new_z]
            struct.pack_into('<3f', data, vert_offsets[vi], new_x, new_y, new_z)
            side_count += 1

    pmx_path.write_bytes(data)
    print(f"[{pmx_path.name}] Lengthened {back_count} back hair verts to waist (Y~12.80) and {side_count} side hair verts!")

p1 = Path("SARA/resources/app/assets/characters/evelyn/model.pmx")
p2 = Path("SARA/resources/app/dist/assets/characters/evelyn/model.pmx")
lengthen_hair(p1)
if p2.exists():
    lengthen_hair(p2)
