import turtle
import tekstur  # <--- Ini memanggil file tekstur.py yang kita buat tadi

# --- 1. GENERATE GAMBAR DULU ---
# Kita panggil fungsi dari file sebelah untuk memastikan gambar tembok sudah ada
nama_file_tembok = tekstur.buat_tekstur_tembok()

# --- 2. SETUP LAYAR ---
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("TRAFFIC MAZE")
wn.setup(700, 700)
wn.tracer(0) # Matikan animasi loading agar cepat

# Daftarkan gambar yang baru dibuat ke dalam Turtle
wn.register_shape(nama_file_tembok)

# --- 3. KELAS PEN (TEMBOK) ---
class Pen(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape(nama_file_tembok) # Gunakan gambar tembok dari cairo
        self.penup()
        self.speed(0)

# --- 4. DATA LEVEL ---
levels = [""]

level_1 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "X S X   X     X   X   X X",
    "X X X X X XXX X X X X X X",
    "X   X   X   X X X   X X X",
    "X XXX XXXXX X X X XXX X X",
    "X X   X     X   X X   X X",
    "X X X X XXXXXXXXX X X X X",
    "X X X X X   X   X X X X X",
    "X X X X X X X X X X X X X",
    "X   X   X X X X X X   X X",
    "XXX X X X X X X X X XXX X",
    "X   X X   X   X   X X   X",
    "X X X X XXXXXXXXX X X X X",
    "X X X X X   X   X X X X X",
    "X X X X X X X X X X X X X",
    "X   X   X X X X X X   X X",
    "XXX X X X X X X X X XXX X",
    "X   X X   X   X   X X   X",
    "X X X X XXXXXXXXX X X X X",
    "X X X X X   X   X X X X X",
    "X X X X X X X X X X X X X",
    "X   X   X X X X X X   X X",
    "X X X X X X X X X X X X X",
    "X X   X     X E X   X   X",
    "XXXXXXXXXXXXXXXXXXXXXXXXX"
]

levels.append(level_1)

# --- 5. FUNGSI SETUP MAZE ---
def setup_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]
            
            # Rumus posisi koordinat
            screen_x = -288 + (x * 24)
            screen_y = 288 - (y * 24)

            if character == "X":
                pen.goto(screen_x, screen_y)
                pen.stamp()
            
            # Nanti bisa tambah logika Player (S) dan Enemy (E) di sini

# --- 6. EKSEKUSI UTAMA ---
pen = Pen()
setup_maze(levels[1])

while True:
    wn.update()