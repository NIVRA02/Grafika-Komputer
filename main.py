
import pygame
import time
import cairo 


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 50 

# Warna 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (231, 76, 60)
YELLOW = (241, 196, 15)

# --- DATA LABIRIN & KUIS ---
# 0: Jalan, 1: Dinding, 2: Mulai, 3: Selesai, 4: Pos Kuis

MAZE_MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 0, 0, 0, 1, 0, 0, 4, 0, 0, 0, 0, 0, 3, 1],
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 4, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

QUIZ_DATA = [
    {
        "pertanyaan": "Rambu segitiga dengan warna dasar kuning melambangkan kategori rambu apa?",
        "pilihan": ["Perintah", "Larangan", "Peringatan", "Petunjuk"],
        "jawaban_benar": "Peringatan",
        "penjelasan": "Rambu peringatan selalu berbentuk dasar segitiga berwarna kuning."
    },
    # Tambahkan data kuis lain di sini
]

# --- KELAS GAME OBJECTS ---

class Player(pygame.sprite.Sprite):
    """Mengelola posisi, kecepatan, skor, dan waktu pemain."""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([TILE_SIZE - 10, TILE_SIZE - 10])
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
        self.score = 0
        self.start_time = time.time()

    def update(self, keys, walls, quiz_points):
        """Memproses input, pergerakan, dan cek trigger kuis/finish."""
        # 1. Logika Input dan Perhitungan dx, dy
        
        # 2. Cek Collision X (Pindah rect.x, panggil _check_collision)
        
        # 3. Cek Collision Y (Pindah rect.y, panggil _check_collision)

        # 4. Cek QuizPoint. Jika ya, kembalikan "QUIZ" dan index.
        
        return "MOVE", None

    def _check_collision(self, walls):
        """Logika AABB Collision Detection."""
        # Implementasikan logika untuk menggeser kembali rect pemain
        pass

class Wall(pygame.sprite.Sprite):
    """Representasi visual dan fisik dinding labirin."""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([TILE_SIZE, TILE_SIZE])
        self.image.fill(WHITE) # Dinding
        self.rect = self.image.get_rect(topleft=(x, y))

class QuizPoint(pygame.sprite.Sprite):
    """Titik di labirin yang memicu kuis. Wajib menggunakan Cairo."""
    def __init__(self, x, y, index):
        super().__init__()
        # 1. Inisialisasi Surface Pygame
        self.image = pygame.Surface([TILE_SIZE, TILE_SIZE], flags=pygame.SRCALPHA)

        # 2. Logika Rendering Cairo 
        #    - Buat cairo.ImageSurface dan Context
        #    - Gambar ikon rambu
        #    - Konversi cairo buffer ke Pygame Surface

        self.rect = self.image.get_rect(topleft=(x, y))
        self.index = index
        self.is_active = True

# --- FUNGSI UTAMA GAME ---

def setup_maze(map_data):
    """Membuat objek Sprite dari MAZE_MAP dan menentukan posisi start/finish."""
    walls = pygame.sprite.Group()
    quiz_points = []
    start_pos = None
    finish_rect = None
    quiz_counter = 0

    # Lakukan iterasi pada map_data untuk inisialisasi objek.

    return walls, quiz_points, start_pos, finish_rect

def draw_quiz_popup(screen, quiz_data_item):
    """Menggambar pop-up kuis di tengah layar."""
    # 1. Gambar kotak dialog
    # 2. Render dan tampilkan teks pertanyaan dan pilihan
    pass

def run_quiz(screen, clock, quiz_item, player):
    """Menjalankan loop kuis: menunggu input jawaban."""
    is_quizzing = True
    result_message = ""

    # Loop while is_quizzing:
        # 1. Proses event input keyboard (tombol A, B, C, D, ENTER)
        # 2. Cek jawaban, update result_message dan player.score
        # 3. Panggil draw_quiz_popup(screen, quiz_item)

    # return True jika kuis berhasil dijawab

def main():
    """Fungsi utama untuk menjalankan game loop."""
    pygame.init()

    # Inisialisasi layar, clock, dan font
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Setup Labirin dan Player
    walls, quiz_points_sprites, start_pos, finish_rect = setup_maze(MAZE_MAP)
    player = Player(start_pos[0], start_pos[1])
    all_sprites = pygame.sprite.Group(player, walls)

    # State Game: RUNNING, QUIZZING, FINISHED
    game_state = "RUNNING"
    start_time = time.time()

    # --- GAME LOOP UTAMA ---
    while True:
        # Hitung waktu & Proses Event (QUIT)

        if game_state == "RUNNING":
            # 1. Update posisi pemain (panggil player.update)
            # 2. Drawing: fill screen, gambar labirin, gambar sprites, gambar HUD 

        elif game_state == "QUIZZING":
            # Panggil run_quiz() dan tangani hasilnya

        elif game_state == "FINISHED":
            # Tampilkan Layar Akhir
            pass

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()