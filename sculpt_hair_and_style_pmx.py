import struct
import math
from pathlib import Path

def sculpt_and_style_model(pmx_path: Path):
    print(f"Sculpting hair & styling PMX for: {pmx_path}")
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

    # Model info strings
    model_name_jp = read_text()
    model_name_en = read_text()
    comment_jp = read_text()
    comment_en = read_text()

    # Vertices
    vert_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
    vert_offsets = []
    vert_positions = []
    vert_normals = []

    for _ in range(vert_count):
        v_off = offset
        pos = struct.unpack_from('<3f', data, offset); offset += 12
        normal = struct.unpack_from('<3f', data, offset); offset += 12
        uv = struct.unpack_from('<2f', data, offset); offset += 8
        offset += (16 * add_vec4_count)
        w_type = data[offset]; offset += 1
        if w_type == 0: offset += bone_index_size
        elif w_type == 1: offset += bone_index_size * 2 + 4
        elif w_type in [2, 4]: offset += bone_index_size * 4 + 16
        elif w_type == 3: offset += bone_index_size * 2 + 4 + 12 + 12 + 12
        offset += 4  # edge scale

        vert_offsets.append(v_off)
        vert_positions.append(list(pos))
        vert_normals.append(list(normal))

    # Face indices
    face_idx_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
    face_indices = []
    for _ in range(face_idx_count):
        idx = struct.unpack_from('<H' if vert_index_size==2 else ('<B' if vert_index_size==1 else '<I'), data, offset)[0]
        offset += vert_index_size
        face_indices.append(idx)

    # Textures
    tex_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
    for _ in range(tex_count): read_text()

    # Materials
    mat_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
    face_offset = 0

    back_hair_verts = set()
    side_hair_verts = set()
    front_hair_verts = set()

    for m_i in range(mat_count):
        m_name = read_text(); read_text()
        offset += 16 + 12 + 4 + 12 + 1 + 16 + 4 + tex_index_size + tex_index_size + 2
        toon_flag = data[offset-1]
        if toon_flag == 0: offset += tex_index_size
        else: offset += 1
        read_text()
        elem_count = struct.unpack_from('<I', data, offset)[0]; offset += 4

        if m_i == 28: # Back hair
            back_hair_verts.update(face_indices[face_offset:face_offset + elem_count])
        elif m_i == 29: # Side hair
            side_hair_verts.update(face_indices[face_offset:face_offset + elem_count])
        elif m_i == 30: # Front hair
            front_hair_verts.update(face_indices[face_offset:face_offset + elem_count])

        face_offset += elem_count

    # 1. SCULPT MATERIAL 28 (BACK HAIR) -> WAIST / HIP LENGTH FLOWING SILKY CASCADES
    # Natural hair length: from original tips (y=18.72) down to waistline (y=12.10)
    # Total drop = ~6.6 units.
    # Fans out laterally to X ~ +-2.20 with gentle natural waves.
    # Curves outward over back armor: Z += 0.38.
    sculpted_back = 0
    for vi in back_hair_verts:
        x, y, z = vert_positions[vi]
        if y < 21.0: # from lower crown down to the tips
            t = (21.0 - y) / (21.0 - 18.72)
            t = min(1.0, max(0.0, t))
            # Smooth cubic easing for silky natural drape
            curve = t * t * (3.0 - 2.0 * t) # smoothstep
            curve_ext = t * t * 0.4 + t * 0.6
            
            # Extension downwards
            new_y = y - (curve_ext * 6.62) # tips drop cleanly to Y ~ 12.10 (waist level)
            
            # Fan out laterally (fuller anime mane)
            fan = 1.0 + (curve * 0.38)
            new_x = x * fan
            
            # Gentle silky micro-wave based on height and lateral position
            wave = math.sin((y - 12.0) * 1.8 + abs(x) * 1.5) * 0.04 * curve
            
            # Drape backward over upper back and waist
            new_z = z + (curve * 0.42) + wave
            
            vert_positions[vi] = [new_x, new_y, new_z]
            struct.pack_into('<3f', data, vert_offsets[vi], new_x, new_y, new_z)
            sculpted_back += 1

    # 2. SCULPT MATERIAL 29 (SIDE HAIR) -> FLOWING BREAST/RIB LEVEL STRANDS
    # Lengthen side framing locks down to Y ~ 13.9 (rib level), curving softly inward
    sculpted_side = 0
    for vi in side_hair_verts:
        x, y, z = vert_positions[vi]
        if y < 20.8:
            t = (20.8 - y) / (20.8 - 18.19)
            t = min(1.0, max(0.0, t))
            curve = t * t * 0.35 + t * 0.65
            
            new_y = y - (curve * 4.25) # drops tips to Y ~ 13.94
            # Gentle framing inward toward chest
            new_x = x * (1.0 + curve * 0.12)
            new_z = z - (curve * 0.08) # drapes gracefully along chest
            
            vert_positions[vi] = [new_x, new_y, new_z]
            struct.pack_into('<3f', data, vert_offsets[vi], new_x, new_y, new_z)
            sculpted_side += 1

    # 3. SCULPT MATERIAL 30 (FRONT HAIR & CROWN AHOGE)
    # Crown cowlick loop arching gracefully upward towards the floating halo
    sculpted_ahoge = 0
    for vi in front_hair_verts:
        x, y, z = vert_positions[vi]
        # Detect crown top center vertices near Z front
        if y > 20.9 and abs(x) < 0.28 and z < -0.15:
            # Lift upward into a cute anime ahoge loop!
            loft = (y - 20.9) / (21.27 - 20.9)
            loft = min(1.0, max(0.0, loft))
            new_y = y + (loft * 0.72) # elevates top strand right towards halo
            new_z = z - (loft * 0.14) # gentle forward curve
            vert_positions[vi] = [x, new_y, new_z]
            struct.pack_into('<3f', data, vert_offsets[vi], x, new_y, new_z)
            sculpted_ahoge += 1

    pmx_path.write_bytes(data)
    print(f"Successfully sculpted {pmx_path.name}:")
    print(f"  - Back hair: {sculpted_back} vertices lengthened to waist (Y~12.10)")
    print(f"  - Side hair: {sculpted_side} vertices lengthened to ribs (Y~13.94)")
    print(f"  - Ahoge loop: {sculpted_ahoge} crown vertices lofted towards halo")

if __name__ == '__main__':
    p1 = Path("D:/MARAA AI/SARA/resources/app/assets/characters/evelyn/model.pmx")
    p2 = Path("D:/MARAA AI/SARA/resources/app/dist/assets/characters/evelyn/model.pmx")
    sculpt_and_style_model(p1)
    if p2.exists():
        sculpt_and_style_model(p2)

