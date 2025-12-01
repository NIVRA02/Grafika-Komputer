import cairo
import math
import pygame

def create_cairo_surface(width, height):
    """Fungsi untuk menggambar map menggunakan PyCairo."""
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(s)

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
    ctx.set_source_rgb(0.25, 0.45, 0.25) # Warna outline jalan
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

    # 6. Menggambar Rumah/Gedung
    houses = [
        (80, 375, 40, 50, (0.85, 0.75, 0.6), (0.6, 0.3, 0.2)),
        (180, 500, 35, 45, (0.7, 0.8, 0.85), (0.4, 0.3, 0.5)),
        (380, 80, 40, 50, (0.9, 0.7, 0.5), (0.5, 0.25, 0.3)),
        (580, 380, 40, 50, (0.8, 0.75, 0.65), (0.5, 0.35, 0.3)),
        (680, 500, 40, 50, (0.85, 0.75, 0.7), (0.6, 0.35, 0.3)),
        (880, 100, 40, 50, (0.8, 0.75, 0.65), (0.5, 0.35, 0.3)),
    ]

    for h in houses:
        draw_house(ctx, *h)

    # 7. Titik Finish
    ctx.set_source_rgb(0.9, 0.2, 0.2)
    ctx.arc(1150, 650, 25, 0, 2 * math.pi)
    ctx.fill()
    ctx.set_source_rgb(1, 1, 1)
    ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(12)
    ctx.move_to(1130, 655)
    ctx.show_text("FINISH")

    return s

def draw_house(ctx, x, y, w, h, c, roof):
    """Fungsi pembantu internal untuk menggambar satu rumah."""
    ctx.set_source_rgb(*c)
    ctx.rectangle(x, y + h * 0.3, w, h * 0.7)
    ctx.fill()
    ctx.set_source_rgb(*roof)
    ctx.new_path()
    ctx.move_to(x - w * 0.1, y + h * 0.3)
    ctx.line_to(x + w * 0.5, y)
    ctx.line_to(x + w * 1.1, y + h * 0.3)
    ctx.close_path()
    ctx.fill()
    ctx.set_source_rgb(0.6, 0.4, 0.25) # Pintu
    ctx.rectangle(x + w * 0.35, y + h * 0.6, w * 0.3, h * 0.4)
    ctx.fill()
    ctx.set_source_rgb(0.6, 0.75, 0.85) # Jendela
    ctx.rectangle(x + w * 0.1, y + h * 0.4, w * 0.2, h * 0.15)
    ctx.fill()
    ctx.set_source_rgb(0.6, 0.75, 0.85) # Jendela
    ctx.rectangle(x + w * 0.7, y + h * 0.4, w * 0.2, h * 0.15)
    ctx.fill()

def create_car_sprite(width, height, color):
    """Membuat sprite mobil yang lebih detail dengan PyCairo."""
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(s)
    
    # 1. Ban Mobil (Hitam)
    ctx.set_source_rgb(0.1, 0.1, 0.1)
    # Ban Kiri Depan & Belakang
    ctx.rectangle(4, 0, 4, 3); ctx.fill()
    ctx.rectangle(16, 0, 4, 3); ctx.fill()
    # Ban Kanan Depan & Belakang
    ctx.rectangle(4, height-3, 4, 3); ctx.fill()
    ctx.rectangle(16, height-3, 4, 3); ctx.fill()

    # 2. Body Mobil (Warna Pilihan)
    r, g, b = color[0]/255.0, color[1]/255.0, color[2]/255.0
    ctx.set_source_rgb(r, g, b)
    ctx.new_path()
    ctx.rectangle(0, 2, width, height-4) 
    ctx.fill()

    # 3. Atap/Kaca (Biru Gelap/Hitam)
    ctx.set_source_rgb(0.2, 0.2, 0.3)
    ctx.rectangle(6, 4, 12, height-8) 
    ctx.fill()

    # 4. Kaca Depan & Belakang (Biru Muda)
    ctx.set_source_rgb(0.6, 0.8, 0.9)
    ctx.rectangle(14, 5, 3, height-10) 
    ctx.fill()
    ctx.rectangle(7, 5, 2, height-10)
    ctx.fill()

    # 5. Lampu Depan (Kuning)
    ctx.set_source_rgb(1.0, 1.0, 0.2)
    ctx.arc(width-2, 4, 1.5, 0, 2*math.pi); ctx.fill() 
    ctx.arc(width-2, height-4, 1.5, 0, 2*math.pi); ctx.fill()

    # 6. Lampu Rem (Merah)
    ctx.set_source_rgb(0.8, 0.1, 0.1)
    ctx.rectangle(0, 3, 1, 2); ctx.fill()
    ctx.rectangle(0, height-5, 1, 2); ctx.fill()

    return cairo_surface_to_pygame(s)

def create_heart_sprite():
    """Membuat sprite hati dengan PyCairo (Ukuran 40x40)."""
    w, h = 40, 40 
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surface)
    
    # Gambar bentuk hati
    ctx.set_source_rgba(1, 0.2, 0.5, 1) # Warna Pink Kemerahan
    ctx.move_to(w * 0.5, h * 0.35)
    ctx.curve_to(w * 0.9, h * 0.1, w, h * 0.6, w * 0.5, h)
    ctx.curve_to(w * 0, h * 0.6, w * 0.1, h * 0.1, w * 0.5, h * 0.35)
    ctx.fill()
    
    # Outline putih
    ctx.set_source_rgba(1, 1, 1, 0.8)
    ctx.set_line_width(2.0)
    ctx.move_to(w * 0.5, h * 0.35)
    ctx.curve_to(w * 0.9, h * 0.1, w, h * 0.6, w * 0.5, h)
    ctx.curve_to(w * 0, h * 0.6, w * 0.1, h * 0.1, w * 0.5, h * 0.35)
    ctx.stroke()
    
    return cairo_surface_to_pygame(surface)

def create_sign_sprite(sign_type):
    """
    Membuat sprite rambu lalu lintas berdasarkan tipe.
    Tipe: 'STOP', 'WARNING', 'NO_PARKING', 'BLUE', 'SPEED', 'GENERIC'
    """
    w, h = 32, 32  # Ukuran sprite
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surface)
    
    cx, cy = w / 2, h / 2

    if sign_type == "STOP":
        # Rambu STOP: Octagon Merah
        ctx.set_source_rgb(0.8, 0, 0)
        # Menggambar Octagon sederhana
        ctx.move_to(cx - 10, cy - 15)
        ctx.line_to(cx + 10, cy - 15)
        ctx.line_to(cx + 15, cy - 10)
        ctx.line_to(cx + 15, cy + 10)
        ctx.line_to(cx + 10, cy + 15)
        ctx.line_to(cx - 10, cy + 15)
        ctx.line_to(cx - 15, cy + 10)
        ctx.line_to(cx - 15, cy - 10)
        ctx.close_path()
        ctx.fill()
        
        # Tulisan Putih (Garis saja karena kecil)
        ctx.set_source_rgb(1, 1, 1)
        ctx.set_line_width(2)
        ctx.move_to(cx - 5, cy); ctx.line_to(cx + 5, cy) # Garis tengah
        ctx.stroke()

    elif sign_type == "WARNING":
        # Rambu Peringatan: Segitiga Putih List Merah
        ctx.set_source_rgb(1, 1, 1) # Putih
        ctx.move_to(cx, cy - 15)
        ctx.line_to(cx + 14, cy + 12)
        ctx.line_to(cx - 14, cy + 12)
        ctx.close_path()
        ctx.fill_preserve()
        
        ctx.set_source_rgb(0.9, 0, 0) # Merah
        ctx.set_line_width(3)
        ctx.stroke()
        
        # Tanda Seru
        ctx.set_source_rgb(0, 0, 0)
        ctx.move_to(cx, cy - 5); ctx.line_to(cx, cy + 2); ctx.stroke()
        ctx.arc(cx, cy + 6, 1, 0, 2*math.pi); ctx.fill()

    elif sign_type == "NO_PARKING":
        # Dilarang Parkir: Lingkaran Putih, List Merah, Huruf P dicoret
        ctx.set_source_rgb(1, 1, 1)
        ctx.arc(cx, cy, 14, 0, 2 * math.pi)
        ctx.fill_preserve()
        ctx.set_source_rgb(0.8, 0, 0)
        ctx.set_line_width(3)
        ctx.stroke()
        
        # Huruf P (Hitam)
        ctx.set_source_rgb(0, 0, 0)
        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(14)
        # Posisi manual agar pas di tengah
        ctx.move_to(cx - 4, cy + 5) 
        ctx.show_text("P")
        
        # Coretan Merah
        ctx.set_source_rgb(0.8, 0, 0)
        ctx.set_line_width(3)
        ctx.move_to(cx - 8, cy - 8)
        ctx.line_to(cx + 8, cy + 8)
        ctx.stroke()

    elif sign_type == "BLUE":
        # Rambu Perintah/Info: Lingkaran Biru
        ctx.set_source_rgb(0, 0.3, 0.8)
        ctx.arc(cx, cy, 14, 0, 2 * math.pi)
        ctx.fill()
        ctx.set_source_rgb(1, 1, 1)
        ctx.set_line_width(2)
        # Panah sederhana
        ctx.move_to(cx - 5, cy); ctx.line_to(cx + 5, cy)
        ctx.move_to(cx + 2, cy - 3); ctx.line_to(cx + 5, cy); ctx.line_to(cx + 2, cy + 3)
        ctx.stroke()

    elif sign_type == "SPEED":
        # Batas Kecepatan: Lingkaran Putih List Merah
        ctx.set_source_rgb(1, 1, 1)
        ctx.arc(cx, cy, 14, 0, 2 * math.pi)
        ctx.fill_preserve()
        ctx.set_source_rgb(0.8, 0, 0)
        ctx.set_line_width(3)
        ctx.stroke()
        
        ctx.set_source_rgb(0, 0, 0)
        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(10)
        ctx.move_to(cx - 6, cy + 4)
        ctx.show_text("40")

    else:
        # Default (Kuning)
        ctx.set_source_rgb(1, 0.8, 0.2)
        ctx.rectangle(4, 4, 24, 24)
        ctx.fill()

    return cairo_surface_to_pygame(surface)

def cairo_surface_to_pygame(surface):
    """Mengubah surface Cairo menjadi surface Pygame."""
    buf = surface.get_data()
    try:
        arr = buf.tobytes()
    except AttributeError:
        arr = bytes(buf)
    
    for fmt in ("BGRA", "ARGB", "RGBA"):
        try:
            img = pygame.image.frombuffer(arr, (surface.get_width(), surface.get_height()), fmt)
            return img.convert_alpha()
        except Exception:
            continue
    img = pygame.image.frombuffer(arr, (surface.get_width(), surface.get_height()), "RGBA")
    return img.convert_alpha()

def generate_map_surface(width, height):
    """Fungsi utama yang dipanggil oleh file lain untuk mendapatkan gambar map jadi."""
    cairo_surf = create_cairo_surface(width, height)
    return cairo_surface_to_pygame(cairo_surf)