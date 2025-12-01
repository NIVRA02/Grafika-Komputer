import cairo
import math

def gambar_rambu(nama_file, tipe):
    w, h = 32, 32
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surface)
    cx, cy = w / 2, h / 2

    if tipe == "STOP":
        ctx.set_source_rgb(0.8, 0, 0)
        # Octagon
        ctx.move_to(cx - 10, cy - 15); ctx.line_to(cx + 10, cy - 15)
        ctx.line_to(cx + 15, cy - 10); ctx.line_to(cx + 15, cy + 10)
        ctx.line_to(cx + 10, cy + 15); ctx.line_to(cx - 10, cy + 15)
        ctx.line_to(cx - 15, cy + 10); ctx.line_to(cx - 15, cy - 10)
        ctx.close_path(); ctx.fill()
        # Garis Putih
        ctx.set_source_rgb(1, 1, 1); ctx.set_line_width(2)
        ctx.move_to(cx - 5, cy); ctx.line_to(cx + 5, cy); ctx.stroke()

    elif tipe == "WARNING":
        ctx.set_source_rgb(1, 1, 1)
        ctx.move_to(cx, cy - 15)
        ctx.line_to(cx + 14, cy + 12); ctx.line_to(cx - 14, cy + 12)
        ctx.close_path(); ctx.fill_preserve()
        ctx.set_source_rgb(0.9, 0, 0); ctx.set_line_width(3); ctx.stroke()
        # Tanda Seru
        ctx.set_source_rgb(0, 0, 0); ctx.set_line_width(2)
        ctx.move_to(cx, cy - 5); ctx.line_to(cx, cy + 2); ctx.stroke()
        ctx.arc(cx, cy + 6, 1, 0, 2*math.pi); ctx.fill()

    elif tipe == "NO_PARKING":
        ctx.set_source_rgb(1, 1, 1); ctx.arc(cx, cy, 14, 0, 2*math.pi); ctx.fill_preserve()
        ctx.set_source_rgb(0.8, 0, 0); ctx.set_line_width(3); ctx.stroke()
        # Huruf P
        ctx.set_source_rgb(0, 0, 0)
        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(14); ctx.move_to(cx - 4, cy + 5); ctx.show_text("P")
        # Coret
        ctx.set_source_rgb(0.8, 0, 0); ctx.set_line_width(3)
        ctx.move_to(cx - 8, cy - 8); ctx.line_to(cx + 8, cy + 8); ctx.stroke()

    elif tipe == "BLUE":
        ctx.set_source_rgb(0, 0.3, 0.8); ctx.arc(cx, cy, 14, 0, 2*math.pi); ctx.fill()
        ctx.set_source_rgb(1, 1, 1); ctx.set_line_width(2)
        ctx.move_to(cx - 5, cy); ctx.line_to(cx + 5, cy); ctx.stroke() # Panah

    elif tipe == "SPEED":
        ctx.set_source_rgb(1, 1, 1); ctx.arc(cx, cy, 14, 0, 2*math.pi); ctx.fill_preserve()
        ctx.set_source_rgb(0.8, 0, 0); ctx.set_line_width(3); ctx.stroke()
        ctx.set_source_rgb(0, 0, 0)
        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(10); ctx.move_to(cx - 6, cy + 4); ctx.show_text("40")

    else: # Generic
        ctx.set_source_rgb(1, 0.8, 0.2); ctx.rectangle(4, 4, 24, 24); ctx.fill()

    surface.write_to_png(nama_file)
    print(f"Berhasil membuat: {nama_file}")

if __name__ == "__main__":
    gambar_rambu("rambu_stop.png", "STOP")
    gambar_rambu("rambu_warning.png", "WARNING")
    gambar_rambu("rambu_no_parking.png", "NO_PARKING")
    gambar_rambu("rambu_blue.png", "BLUE")
    gambar_rambu("rambu_speed.png", "SPEED")
    gambar_rambu("rambu_generic.png", "GENERIC")