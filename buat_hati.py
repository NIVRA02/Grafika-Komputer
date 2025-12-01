import cairo

def buat_hati():
    w, h = 40, 40
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surface)
    
    ctx.set_source_rgba(1, 0.2, 0.5, 1) # Pink
    ctx.move_to(w * 0.5, h * 0.35)
    ctx.curve_to(w * 0.9, h * 0.1, w, h * 0.6, w * 0.5, h)
    ctx.curve_to(w * 0, h * 0.6, w * 0.1, h * 0.1, w * 0.5, h * 0.35)
    ctx.fill_preserve()
    
    # Outline Putih
    ctx.set_source_rgba(1, 1, 1, 0.8)
    ctx.set_line_width(2.0)
    ctx.stroke()

    surface.write_to_png("hati.png")
    print("Berhasil membuat: hati.png")

if __name__ == "__main__":
    buat_hati()