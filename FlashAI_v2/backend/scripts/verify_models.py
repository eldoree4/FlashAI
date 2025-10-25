#!/usr/bin/env python3
from pathlib import Path
models = {
    "wav2lip": ("../models/wav2lip/wav2lip_gan.pth", 50_000_000),
    "midas": ("../models/midas/midas_v21_small.pt", 10_000_000),
    "realesrgan_x4": ("../models/realesrgan/realesrgan_x4plus.pth", 50_000_000),
    "rife": ("../models/rife/rife_model.pth", 10_000_000),
    "video_diffusion": ("../models/video/video_checkpoint.pt", 100_000_000)
}
root = Path(__file__).parent
ok = True
for name, (relpath, minsize) in models.items():
    p = (root / relpath).resolve()
    if not p.exists():
        print(f"[MISSING] {name}: {p}")
        ok = False
    else:
        size = p.stat().st_size
        status = 'OK' if size > minsize else f'TOO_SMALL ({size} bytes)'
        print(f"[FOUND] {name}: {p} size={size:,} -> {status}")
print('\nIf any are missing, place them into backend/models/ as shown.')
if not ok:
    raise SystemExit(2)
