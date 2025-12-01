import cairo
import math

def buat_mobil():
    w, h = 24, 14
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surface)
    
    # Ban
    ctx.set_source_rgb(0.1, 0.1, 0.1)
    ctx.rectangle(4, 0, 4, 3); ctx.fill()
    ctx.rectangle(16, 0, 4, 3); ctx.fill()
    ctx.rectangle(4, h-3, 4, 3); ctx.fill()
    ctx.rectangle(16, h-3, 4, 3); ctx.fill()

    # Body Merah
    ctx.set_source_rgb(0.8, 0.2, 0.2) 
    ctx.rectangle(0, 2, w, h-4); ctx.fill()

    # Kaca
    ctx.set_source_rgb(0.6, 0.8, 0.9)
    ctx.rectangle(14, 5, 3, h-10); ctx.fill()
    ctx.rectangle(7, 5, 2, h-10); ctx.fill()

    # Atap
    ctx.set_source_rgb(0.2, 0.2, 0.3)
    ctx.rectangle(6, 4, 12, h-8); ctx.fill()

    # Lampu
    ctx.set_source_rgb(1.0, 1.0, 0.2)
    ctx.arc(w-2, 4, 1.5, 0, 2*math.pi); ctx.fill() 
    ctx.arc(w-2, h-4, 1.5, 0, 2*math.pi); ctx.fill()

    surface.write_to_png("mobil.png")
    print("Berhasil membuat: mobil.png")

if __name__ == "__main__":
    buat_mobil()