import cairo

def buat_rumah():
    w, h = 40, 50
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surface)
    
    # Warna Dasar Tembok
    ctx.set_source_rgb(0.85, 0.75, 0.6) 
    ctx.rectangle(0, h * 0.3, w, h * 0.7)
    ctx.fill()
    
    # Atap
    ctx.set_source_rgb(0.6, 0.3, 0.2)
    ctx.new_path()
    ctx.move_to(0 - w * 0.1, h * 0.3)
    ctx.line_to(w * 0.5, 0)
    ctx.line_to(w * 1.1, h * 0.3)
    ctx.close_path()
    ctx.fill()
    
    # Pintu
    ctx.set_source_rgb(0.4, 0.2, 0.1)
    ctx.rectangle(w * 0.35, h * 0.6, w * 0.3, h * 0.4)
    ctx.fill()
    
    # Jendela
    ctx.set_source_rgb(0.6, 0.8, 0.9)
    ctx.rectangle(w * 0.1, h * 0.45, w * 0.2, h * 0.15)
    ctx.rectangle(w * 0.7, h * 0.45, w * 0.2, h * 0.15)
    ctx.fill()

    surface.write_to_png("rumah.png")
    print("Berhasil membuat: rumah.png")

if __name__ == "__main__":
    buat_rumah()