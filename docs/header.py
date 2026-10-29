"""README header for the brigade mod: a glowing wireframe chef's toque beside the title (FXPC header style).

Run: python3 docs/header.py docs/header.png (numpy, Pillow, the B612 fonts in ~/.local/share/fonts/b612)."""
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

W, H, SS = 2400, 900, 2
FONTS = Path.home() / ".local/share/fonts/b612/fonts/Orig"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("header.png")

CREAM = np.array([255, 222, 180])
EMBER = np.array([255, 140, 70])
CLAUDE = (217, 119, 87)


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size * SS)


# --- the toque: a pleated surface of revolution with a puffed crown -----------------------------
# (height, radius, pleat weight) along the profile, bottom to top
PROFILE = [
    (0.00, 1.00, 0.0), (0.36, 1.00, 0.0),            # the band
    (0.40, 1.03, 0.6), (1.1, 1.08, 1.0), (1.75, 1.15, 1.0),  # pleated body
    (1.92, 1.36, 1.0), (2.12, 1.50, 0.9), (2.34, 1.46, 0.7),  # puffed crown
    (2.50, 1.24, 0.5), (2.62, 0.90, 0.3), (2.69, 0.48, 0.15), (2.71, 0.0, 0.0),
]
PLEATS, NTH, NS = 14, 140, 60


def profile(s):
    hs = np.array([p[0] for p in PROFILE])
    # arc-length-ish parameter: interpolate on the profile's own point index, smoothed
    k = s * (len(PROFILE) - 1)
    i = np.clip(np.floor(k).astype(int), 0, len(PROFILE) - 2)
    t = k - i
    t = t * t * (3 - 2 * t)
    a, b = np.array(PROFILE)[i], np.array(PROFILE)[i + 1]
    return a + (b - a) * t[..., None]


s = np.linspace(0, 1, NS)
th = np.linspace(0, 2 * math.pi, NTH, endpoint=False)
P = profile(s)                                         # NS x 3
hh, rr, pw = P[:, 0][:, None], P[:, 1][:, None], P[:, 2][:, None]
puff = (0.5 + 0.5 * np.cos(PLEATS * th))[None, :] ** 1.6
R = rr * (1 + 0.075 * pw * puff)
X, Z, Y = R * np.cos(th)[None, :], R * np.sin(th)[None, :], np.broadcast_to(hh, R.shape)
V = np.stack([X, Y - 1.30, Z], -1)                     # NS x NTH x 3, centred on its height

yaw, pitch = math.radians(18), math.radians(20)
Ry = np.array([[math.cos(yaw), 0, math.sin(yaw)], [0, 1, 0], [-math.sin(yaw), 0, math.cos(yaw)]])
Rx = np.array([[1, 0, 0], [0, math.cos(pitch), -math.sin(pitch)], [0, math.sin(pitch), math.cos(pitch)]])
V = V @ (Rx @ Ry).T

scale = H * 0.255
cx, cy = W * 0.235, H * 0.5
SX = (V[..., 0] * scale + cx) * SS
SY = (-V[..., 1] * scale + cy) * SS
D = (V[..., 2] - V[..., 2].min()) / np.ptp(V[..., 2])   # 0 back .. 1 front

segs = []  # (depth, x0, y0, x1, y1, weight)
for i in range(NS):                                    # rings
    if i % 2 and not (0.36 < hh[i, 0] < 0.40):
        continue
    for j in range(NTH):
        k = (j + 1) % NTH
        segs.append(((D[i, j] + D[i, k]) / 2, SX[i, j], SY[i, j], SX[i, k], SY[i, k], 1.0))
for j in range(0, NTH, 2):                             # meridians, brighter on pleat ridges
    ridge = 1.0 if j % (NTH // PLEATS) < 2 else 0.55
    for i in range(NS - 1):
        segs.append(((D[i, j] + D[i + 1, j]) / 2, SX[i, j], SY[i, j], SX[i + 1, j], SY[i + 1, j], ridge))
segs.sort()

wire = Image.new("RGB", (W * SS, H * SS))
dw = ImageDraw.Draw(wire)
for d, x0, y0, x1, y1, wgt in segs:
    c = (EMBER + (CREAM - EMBER) * d) * (0.18 + 0.82 * d ** 1.5) * wgt
    dw.line([(x0, y0), (x1, y1)], fill=tuple(int(v) for v in c), width=SS + (1 if d > 0.6 else 0))

# --- background: night-kitchen gradient with a stove glow under the hat -------------------------
yy, xx = np.mgrid[0:H * SS, 0:W * SS].astype(np.float32)
t = (yy / (H * SS))[..., None]
top, bot = np.array([13, 15, 28]), np.array([52, 24, 18])
bg = top + (bot - top) * t ** 1.3
r2 = ((xx - cx * SS) / (W * SS * 0.30)) ** 2 + ((yy - (cy + scale * 1.05) * SS) / (H * SS * 0.42)) ** 2
bg += np.exp(-r2)[..., None] * np.array([120, 50, 20])
bg = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8))

glow = wire.filter(ImageFilter.GaussianBlur(12 * SS))
img = ImageChops.add(ImageChops.add(bg, glow), wire)

# --- text --------------------------------------------------------------------------------------
text = Image.new("RGB", img.size)
dt = ImageDraw.Draw(text)
x0 = int(W * 0.47 * SS)
dt.text((x0, 150 * SS), "brigade", font=font("B612-Bold.otf", 150), fill=tuple(CREAM))
dt.text((x0 + 6 * SS, 340 * SS), "a model-routing kitchen for Claude Code", font=font("B612-Regular.otf", 46),
        fill=(235, 190, 150))

mono, mono_b = font("B612Mono-Regular.otf", 33), font("B612Mono-Bold.otf", 33)
rows = [("HEAD CHEF", "opus  ", "writes recipes, decides gates"),
        ("COOK     ", "sonnet", "code, tests, one commit per item"),
        ("PREP     ", "haiku ", "exact commands, short reports")]
y = 455 * SS
for role, model, does in rows:
    dt.ellipse([x0 + 6 * SS, y + 14 * SS, x0 + 20 * SS, y + 28 * SS], fill=CLAUDE)
    dt.text((x0 + 42 * SS, y), role, font=mono_b, fill=CLAUDE)
    dt.text((x0 + 262 * SS, y), model, font=mono, fill=(250, 214, 170))
    dt.text((x0 + 420 * SS, y), does, font=mono, fill=(200, 165, 140))
    y += 62 * SS

# the status line the mod draws, as a pill
pill = "brigade: cook 05 · prep 10"
pf = font("B612Mono-Regular.otf", 28)
pw_ = dt.textlength(pill, font=pf)
py = 690 * SS
dt.rounded_rectangle([x0 + 4 * SS, py - 14 * SS, x0 + 4 * SS + pw_ + 48 * SS, py + 50 * SS], radius=32 * SS,
                     outline=(150, 90, 66), width=2 * SS)
dt.text((x0 + 28 * SS, py), pill, font=pf, fill=(235, 190, 150))

img = ImageChops.add(img, ImageChops.multiply(text.filter(ImageFilter.GaussianBlur(9 * SS)),
                                              Image.new("RGB", img.size, (110, 110, 110))))
img = ImageChops.lighter(img, text)
img = img.resize((W, H), Image.LANCZOS)
OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT, optimize=True)
print("wrote", OUT, f"{len(segs)} segments")
