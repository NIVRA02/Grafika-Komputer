import cairo
import math

def buat_pohon():
    # Ukuran kanvas
    w, h = 40, 60
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surface)
    
    # Titik tengah bawah (batang)
    cx, cy = w / 2, h * 0.8 

    # 1. Batang Pohon (Coklat)
    ctx.set_source_rgb(0.4, 0.26, 0.13) # Coklat Kayu
    trunk_w, trunk_h = 10, 20
    ctx.rectangle(cx - trunk_w/2, cy - trunk_h, trunk_w, trunk_h)
    ctx.fill()

    # 2. Daun (Hijau) - Tumpuk 3 lingkaran biar rimbun
    colors = [(0.13, 0.55, 0.13), (0.18, 0.49, 0.2), (0.1, 0.37, 0.12)]
    radii = [18, 14, 10]
    offsets = [20, 30, 40] # Tinggi tumpukan daun dari bawah

    for i in range(3):
        ctx.set_source_rgb(*colors[i])
        ctx.arc(cx, cy - offsets[i], radii[i], 0, 2 * math.pi)
        ctx.fill()

    surface.write_to_png("pohon.png")
    print("Berhasil membuat: pohon.png")

if __name__ == "__main__":
    buat_pohon()