import cairo
import math

def buat_peta():
    width, height = 1200, 700
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)

    # 1. Background Rumput
    ctx.set_source_rgb(0.35, 0.65, 0.35)
    ctx.rectangle(0, 0, width, height)
    ctx.fill()

    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    
    # 2. Definisi Jalur Jalan
    paths = [
        [(50, 650), (50, 550), (150, 550), (150, 450), (50, 450), (50, 350), (150, 350)],
        [(150, 350), (150, 250), (50, 250), (50, 150), (150, 150), (150, 50), (250, 50)],
        [(150, 250), (250, 250), (250, 350), (350, 350)],
        [(250, 250), (250, 150), (350, 150), (350, 50), (450, 50)],
        [(350, 150), (350, 250), (450, 250)],
        [(350, 350), (350, 450), (250, 450), (250, 550), (350, 550)],
        [(350, 450), (450, 450), (450, 350)],
        [(450, 250), (550, 250), (550, 150), (650, 150)],
        [(550, 250), (550, 350), (650, 350), (650, 250)],
        [(450, 350), (450, 550), (550, 550), (550, 650)],
        [(550, 550), (650, 550), (650, 450), (750, 450)],
        [(650, 150), (750, 150), (750, 250), (850, 250)],
        [(750, 250), (750, 350), (850, 350)],
        [(750, 450), (750, 550), (850, 550), (850, 650)],
        [(850, 550), (950, 550), (950, 450), (1050, 450)],
        [(850, 250), (950, 250), (950, 150), (1050, 150)],
        [(950, 250), (950, 350), (1050, 350)],
        [(850, 350), (850, 450), (950, 450)],
        [(1050, 150), (1050, 250), (1150, 250)],
        [(1050, 250), (1050, 350), (950, 350)],
        [(1050, 350), (1150, 350), (1150, 450), (1050, 450)],
        [(1050, 450), (1050, 550), (1150, 550), (1150, 650)],
        [(450, 50), (550, 50), (550, 150)],
        [(250, 450), (150, 450), (150, 550)],
        [(650, 250), (750, 250)],
        [(650, 450), (650, 350)],
    ]

    # 3. Gambar Aspal (Layer Bawah)
    ctx.set_source_rgb(0.25, 0.45, 0.25)
    ctx.set_line_width(50)
    for path in paths:
        ctx.new_path()
        ctx.move_to(path[0][0], path[0][1])
        for p in path[1:]:
            ctx.line_to(p[0], p[1])
        ctx.stroke()

    # 4. Gambar Jalan Utama
    ctx.set_source_rgb(0.92, 0.92, 0.90)
    ctx.set_line_width(45)
    for path in paths:
        ctx.new_path()
        ctx.move_to(path[0][0], path[0][1])
        for p in path[1:]:
            ctx.line_to(p[0], p[1])
        ctx.stroke()

    # 5. Gambar Garis Putus-putus
    ctx.set_source_rgb(0.85, 0.85, 0.83)
    ctx.set_line_width(2)
    ctx.set_dash([10, 10])
    for path in paths:
        ctx.new_path()
        ctx.move_to(path[0][0], path[0][1])
        for p in path[1:]:
            ctx.line_to(p[0], p[1])
        ctx.stroke()
    ctx.set_dash([])

    # 6. Titik Finish
    ctx.set_source_rgb(0.9, 0.2, 0.2)
    ctx.arc(1150, 650, 25, 0, 2 * math.pi)
    ctx.fill()
    ctx.set_source_rgb(1, 1, 1)
    ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(12)
    ctx.move_to(1130, 655)
    ctx.show_text("FINISH")

    surface.write_to_png("peta.png")
    print("Berhasil membuat: peta.png")

if __name__ == "__main__":
    buat_peta()