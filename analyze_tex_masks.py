import numpy as np
from PIL import Image
from scipy.ndimage import label

img0 = Image.open('sara_app_backup/assets/characters/evelyn/textures/tex_0.png').convert('RGBA')
arr0 = np.array(img0, dtype=np.float32)

r, g, b, a = arr0[:,:,0], arr0[:,:,1], arr0[:,:,2], arr0[:,:,3]
max_c = np.maximum(np.maximum(r, g), b)
cloth_mask = (max_c < 110) & (a > 50)

# Let's inspect where cloth is across Y coordinates (top=0, bottom=2048)
y_profile = cloth_mask.sum(axis=1)
for i in range(0, 2048, 256):
    print(f"Y [{i}:{i+256}]: {cloth_mask[i:i+256, :].sum()} cloth pixels")

x_profile = cloth_mask.sum(axis=0)
for i in range(0, 2048, 256):
    print(f"X [{i}:{i+256}]: {cloth_mask[:, i:i+256].sum()} cloth pixels")
