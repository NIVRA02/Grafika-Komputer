import cairo

def buat_tekstur_tembok():
    """
    Fungsi ini menggambar tekstur tembok bata menggunakan Pycairo
    dan menyimpannya sebagai file gambar.
    """
    filename = "wall.gif"  # Kita pakai ekstensi .gif agar Turtle lebih mudah membacanya
    width, height = 24, 24 # Ukuran 24x24 pixel sesuai grid game
    
    # 1. Siapkan Kanvas
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)
    
    # 2. Gambar Background (Warna Bata)
    ctx.set_source_rgb(0.6, 0.2, 0.1) # Merah bata
    ctx.rectangle(0, 0, width, height)
    ctx.fill()
    
    # 3. Gambar Garis Semen (Mortar)
    ctx.set_source_rgb(0.8, 0.8, 0.8) # Abu-abu muda
    ctx.set_line_width(2)
    
    # Garis Horizontal Tengah
    ctx.move_to(0, 12)
    ctx.line_to(24, 12)
    ctx.stroke()
    
    # Garis Vertikal (Selang-seling agar seperti bata)
    ctx.move_to(12, 0)
    ctx.line_to(12, 12)
    ctx.stroke()
    
    ctx.move_to(6, 12)
    ctx.line_to(6, 24)
    ctx.stroke()
    
    ctx.move_to(18, 12)
    ctx.line_to(18, 24)
    ctx.stroke()

    # 4. Border Luar
    ctx.set_source_rgb(0.3, 0.1, 0.05) # Coklat tua
    ctx.rectangle(0, 0, width, height)
    ctx.set_line_width(1)
    ctx.stroke()

    # 5. Simpan Gambar
    # Trik: Kita simpan data PNG tapi namakan .gif agar Turtle tidak bingung
    surface.write_to_png(filename) 
    print(f"[INFO] Tekstur berhasil dibuat: {filename}")
    
    return filename

# Jika file ini dijalankan langsung (bukan di-import), dia akan test membuat gambar
if __name__ == "__main__":
    buat_tekstur_tembok()