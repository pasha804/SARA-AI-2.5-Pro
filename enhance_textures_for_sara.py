import struct
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path

def generate_silky_hair_pattern(width, height):
    """
    Generates a high-resolution procedural anisotropic silky hair texture.
    Contains:
    - Base pure platinum white (#f5f8fe)
    - High-frequency anisotropic vertical micro-fibers (silky hair strands)
    - Silky 'Angel Ring' (tenshi-no-wa) horizontal specular highlight bands
    - Ambient celestial periwinkle/lavender undertones in crevices
    """
    print(f"Generating silky hair pattern ({width}x{height})...")
    np.random.seed(42)

    # Base gradient: slightly deeper lavender-blue at roots/tips, bright platinum in middle
    y_coords = np.linspace(0, 1, height)[:, None]
    x_coords = np.linspace(0, 1, width)[None, :]

    # Base color: 245, 248, 255 (Platinum)
    base_r = np.full((height, width), 244.0)
    base_g = np.full((height, width), 248.0)
    base_b = np.full((height, width), 255.0)

    # Vertical hair strands (high frequency variation along X)
    # 1D noise along X stretched vertically
    x_strands_1 = np.sin(x_coords * 2500.0) * 0.5 + 0.5
    x_strands_2 = np.sin(x_coords * 5100.0 + 1.2) * 0.5 + 0.5
    x_strands_3 = np.sin(x_coords * 800.0 + 0.7) * 0.5 + 0.5
    strands = (x_strands_1 * 0.4 + x_strands_2 * 0.35 + x_strands_3 * 0.25)
    
    # Anisotropic horizontal specular band ('angel ring' hair shine)
    # Two soft horizontal shine bands across V = 0.28 and V = 0.62
    shine_band_1 = np.exp(-((y_coords - 0.28) ** 2) / 0.008)
    shine_band_2 = np.exp(-((y_coords - 0.65) ** 2) / 0.012)
    specular_sheen = np.maximum(shine_band_1, shine_band_2 * 0.7)

    # Shadow crevices (subtle periwinkle blue #d0def4)
    shadow_depth = (1.0 - strands) * 0.18 * (1.0 - specular_sheen * 0.8)

    # Combine channels
    r = base_r * (1.0 - shadow_depth) + (255.0 - base_r) * specular_sheen * 0.95
    g = base_g * (1.0 - shadow_depth * 0.85) + (255.0 - base_g) * specular_sheen * 0.95
    b = base_b * (1.0 - shadow_depth * 0.5) + (255.0 - base_b) * specular_sheen * 1.0

    r = np.clip(r, 210, 255).astype(np.uint8)
    g = np.clip(g, 220, 255).astype(np.uint8)
    b = np.clip(b, 235, 255).astype(np.uint8)
    a = np.full((height, width), 255, dtype=np.uint8)

    hair_rgba = np.dstack([r, g, b, a])
    return Image.fromarray(hair_rgba, mode='RGBA')

def generate_royal_cobalt_lining(width, height):
    """
    Generates rich royal cobalt blue silk lining texture matching reference turnaround:
    - Base: Deep royal cobalt blue (#1a4db8 / [26, 77, 184])
    - Drape highlights: Luminous sapphire glow (#2d6ee6 / [45, 110, 230])
    - Subtle fabric weave / satin sheen
    """
    y_coords = np.linspace(0, 1, height)[:, None]
    x_coords = np.linspace(0, 1, width)[None, :]

    # Smooth drape wave
    drape = np.sin(x_coords * 8.0 + y_coords * 4.0) * 0.5 + 0.5
    
    r = 20.0 + drape * 28.0
    g = 65.0 + drape * 52.0
    b = 165.0 + drape * 75.0
    
    r = np.clip(r, 15, 60).astype(np.uint8)
    g = np.clip(g, 55, 130).astype(np.uint8)
    b = np.clip(b, 150, 245).astype(np.uint8)
    a = np.full((height, width), 255, dtype=np.uint8)

    lining_rgba = np.dstack([r, g, b, a])
    return Image.fromarray(lining_rgba, mode='RGBA')

def process_textures():
    pmx_path = Path("D:/MARAA AI/SARA/resources/app/assets/characters/evelyn/model.pmx")
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

    def read_text():
        nonlocal offset
        t_len = struct.unpack_from('<I', data, offset)[0]; offset += 4
        t = data[offset:offset+t_len].decode(encoding, errors='ignore'); offset += t_len
        return t

    read_text(); read_text(); read_text(); read_text()

    vert_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
    vert_uvs = []
    for _ in range(vert_count):
        offset += 12 + 12
        uv = struct.unpack_from('<2f', data, offset); offset += 8
        vert_uvs.append(uv)
        offset += (16 * add_vec4_count)
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
        face_indices.append(idx)
        offset += vert_index_size

    tex_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
    for _ in range(tex_count): read_text()

    mat_count = struct.unpack_from('<I', data, offset)[0]; offset += 4
    face_offset = 0

    W, H = 2048, 2048

    # Masks for tex_5
    mask_hair = Image.new('L', (W, H), 0)
    draw_hair = ImageDraw.Draw(mask_hair)

    mask_lining = Image.new('L', (W, H), 0)
    draw_lining = ImageDraw.Draw(mask_lining)

    for m_i in range(mat_count):
        m_name = read_text(); read_text()
        offset += 16 + 12 + 4 + 12 + 1 + 16 + 4 + tex_index_size + tex_index_size + 2
        toon_flag = data[offset-1]
        if toon_flag == 0: offset += tex_index_size
        else: offset += 1
        read_text()
        elem_count = struct.unpack_from('<I', data, offset)[0]; offset += 4

        # Materials 28, 29, 30 are Hair on tex_5
        if m_i in [28, 29, 30]:
            for f in range(0, elem_count, 3):
                v0, v1, v2 = face_indices[face_offset + f], face_indices[face_offset + f + 1], face_indices[face_offset + f + 2]
                p0 = (int(vert_uvs[v0][0] * (W - 1)), int(vert_uvs[v0][1] * (H - 1)))
                p1 = (int(vert_uvs[v1][0] * (W - 1)), int(vert_uvs[v1][1] * (H - 1)))
                p2 = (int(vert_uvs[v2][0] * (W - 1)), int(vert_uvs[v2][1] * (H - 1)))
                draw_hair.polygon([p0, p1, p2], fill=255)

        # Material 15 is Coat Inside Lining on tex_5
        elif m_i == 15:
            for f in range(0, elem_count, 3):
                v0, v1, v2 = face_indices[face_offset + f], face_indices[face_offset + f + 1], face_indices[face_offset + f + 2]
                p0 = (int(vert_uvs[v0][0] * (W - 1)), int(vert_uvs[v0][1] * (H - 1)))
                p1 = (int(vert_uvs[v1][0] * (W - 1)), int(vert_uvs[v1][1] * (H - 1)))
                p2 = (int(vert_uvs[v2][0] * (W - 1)), int(vert_uvs[v2][1] * (H - 1)))
                draw_lining.polygon([p0, p1, p2], fill=255)

        face_offset += elem_count

    # Expand masks slightly to eliminate seam bleeding
    mask_hair_dilated = mask_hair.filter(ImageFilter.MaxFilter(7))
    mask_lining_dilated = mask_lining.filter(ImageFilter.MaxFilter(7))

    # Generate procedural textures
    silky_hair = generate_silky_hair_pattern(W, H)
    royal_lining = generate_royal_cobalt_lining(W, H)

    # 1. Update tex_5.png
    tex5_paths = [
        Path("D:/MARAA AI/SARA/resources/app/assets/characters/evelyn/textures/tex_5.png"),
        Path("D:/MARAA AI/SARA/resources/app/dist/assets/characters/evelyn/textures/tex_5.png")
    ]

    for t5_path in tex5_paths:
        if not t5_path.exists():
            continue
        base_tex5 = Image.open(t5_path).convert('RGBA')

        # Composite royal cobalt lining into Material 15
        base_tex5.paste(royal_lining, (0, 0), mask_lining_dilated)

        # Composite silky hair pattern into Materials 28, 29, 30
        base_tex5.paste(silky_hair, (0, 0), mask_hair_dilated)

        base_tex5.save(t5_path, "PNG")
        print(f"Updated {t5_path} with silky hair + royal cobalt cape lining!")

    # 2. Update tex_0.png for porcelain white dress, gold buttons, and royal blue accents
    tex0_paths = [
        Path("D:/MARAA AI/SARA/resources/app/assets/characters/evelyn/textures/tex_0.png"),
        Path("D:/MARAA AI/SARA/resources/app/dist/assets/characters/evelyn/textures/tex_0.png")
    ]

    for t0_path in tex0_paths:
        if not t0_path.exists():
            continue
        im0 = Image.open(t0_path).convert('RGBA')
        arr0 = np.array(im0).astype(np.float32)

        # Accentuate bright porcelain white on dress areas while preserving dark trim and blue corset
        # Pixels with RGB > 180 get gently boosted towards pure silk porcelain [245, 248, 255]
        bright_mask = (arr0[:, :, 0] > 180) & (arr0[:, :, 1] > 180) & (arr0[:, :, 2] > 180)
        arr0[bright_mask, 0] = np.clip(arr0[bright_mask, 0] * 1.05 + 10, 0, 255)
        arr0[bright_mask, 1] = np.clip(arr0[bright_mask, 1] * 1.05 + 12, 0, 255)
        arr0[bright_mask, 2] = np.clip(arr0[bright_mask, 2] * 1.06 + 15, 0, 255)

        # Accentuate blue tones (royal blue corset & boots)
        blue_mask = (arr0[:, :, 2] > arr0[:, :, 0] + 30) & (arr0[:, :, 2] > arr0[:, :, 1] + 20)
        arr0[blue_mask, 0] = np.clip(arr0[blue_mask, 0] * 0.9, 0, 255)
        arr0[blue_mask, 1] = np.clip(arr0[blue_mask, 1] * 0.95, 0, 255)
        arr0[blue_mask, 2] = np.clip(arr0[blue_mask, 2] * 1.15 + 15, 0, 255)

        im0_new = Image.fromarray(arr0.astype(np.uint8), mode='RGBA')
        im0_new.save(t0_path, "PNG")
        print(f"Updated {t0_path} with enhanced porcelain white dress & deep royal blue corset!")

if __name__ == '__main__':
    process_textures()

