import sys
import math
import pygame
import random
import game_assets  # Kita import file aset

# --- INISIALISASI ---
pygame.init()
try:
    pygame.mixer.quit()
except Exception:
    pass

WIDTH, HEIGHT = 1200, 700
FPS = 60

# --- WARNA ---
ROAD_RGB = (235, 235, 230)
BG_RGB = (89, 166, 89)
HUD_BG = (40, 40, 40, 180)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (241, 196, 15)
RED = (200, 50, 50)
GREEN = (89, 166, 89)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Maze - Road Only + Trees")
clock = pygame.time.Clock()

# --- PEMBUATAN MAP ---
# Map sekarang dibuat di game_assets.py agar kode utama lebih bersih
maze_surface = game_assets.generate_map_surface(WIDTH, HEIGHT)

# --- LOGIKA GAME ---
def is_on_road(x, y, surf):
    x, y = int(x), int(y)
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return False
    try:
        r, g, b, a = surf.get_at((x, y))
        # Logika deteksi jalan: Warna jalan adalah RGB > 150 (putih kekuningan)
        return r > 150 and g > 150 and b > 150
    except:
        return False

def generate_trees():
    trees = []
    random.seed(42)
    attempts = 0
    while len(trees) < 60 and attempts < 500:
        x = random.randint(20, WIDTH - 20)
        y = random.randint(20, HEIGHT - 20)
        # Jangan taruh pohon di jalan
        if is_on_road(x, y, maze_surface):
            attempts += 1
            continue
        # Jangan tumpuk pohon
        too_close = False
        for tx, ty, _ in trees:
            if math.hypot(x - tx, y - ty) < 30:
                too_close = True
                break
        if not too_close:
            size = random.choice([12, 14, 16, 18])
            trees.append((x, y, size))
        attempts += 1
    print(f"[INFO] Generated {len(trees)} trees")
    return trees

def draw_tree(surf, x, y, size):
    trunk_w = size // 4
    trunk_h = size // 2
    trunk_rect = pygame.Rect(x - trunk_w // 2, y, trunk_w, trunk_h)
    pygame.draw.rect(surf, (101, 67, 33), trunk_rect)
    foliage_colors = [(34, 139, 34), (46, 125, 50), (27, 94, 32)]
    for i, color in enumerate(foliage_colors):
        offset = i * (size // 6)
        pygame.draw.circle(surf, color, (x, y - offset), size - i * 2)

# --- DATA KUIS ---
QUIZ_DATA = [
    {
        "pertanyaan": "Apa arti rambu segitiga dengan pinggir merah?",
        "pilihan": ["Perintah", "Larangan", "Peringatan", "Petunjuk"],
        "jawaban_benar": 2,
        "penjelasan": "Rambu segitiga mengandung peringatan."
    },
    {
        "pertanyaan": "Warna dasar rambu 'STOP' biasanya apa?",
        "pilihan": ["Hijau", "Merah", "Kuning", "Biru"],
        "jawaban_benar": 1,
        "penjelasan": "STOP berwarna merah."
    },
    {
        "pertanyaan": "Arti lampu kuning pada traffic light?",
        "pilihan": ["Stop langsung", "Persiapkan berhenti", "Jalan terus", "Mundur"],
        "jawaban_benar": 1,
        "penjelasan": "Kuning menandakan persiapan berhenti."
    },
]

QUIZ_POINTS = [
    (240, 250),
    (750, 260),
    (950, 360),
]

# --- CLASS PLAYER (DIPERBARUI) ---
class Player:
    def __init__(self, x, y):
        self.w = 24
        self.h = 14
        # MENGGUNAKAN GAMBAR BARU DARI GAME_ASSETS
        self.image = game_assets.create_car_sprite(self.w, self.h, RED)
        self.original_image = self.image # Simpan gambar asli jika nanti butuh rotasi
        
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3.0
        self.score = 0

    def move(self, dx, dy, road_surface):
        nx = self.rect.centerx + dx
        ny = self.rect.centery + dy
        # Cek tabrakan di 5 titik mobil
        check_points = [
            (nx, ny),
            (nx + self.w//2 - 2, ny),
            (nx - self.w//2 + 2, ny),
            (nx, ny - self.h//2 + 2),
            (nx, ny + self.h//2 - 2),
        ]
        all_valid = True
        for px, py in check_points:
            if not is_on_road(px, py, road_surface):
                all_valid = False
                break
        if all_valid:
            self.rect.centerx = int(nx)
            self.rect.centery = int(ny)
            return True
        return False

# --- UI HELPER ---
def wrap_text(font, text, max_w):
    words = text.split(" ")
    lines = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        if font.size(test)[0] <= max_w:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_quiz_popup(surface, quiz_item, selected_idx=None, result_msg=None):
    w = int(WIDTH * 0.7)
    h = int(HEIGHT * 0.6)
    x = (WIDTH - w) // 2
    y = (HEIGHT - h) // 2
    popup = pygame.Surface((w, h), pygame.SRCALPHA)
    popup.fill((20, 20, 20, 220))
    pygame.draw.rect(popup, WHITE, (0, 0, w, h), 2, border_radius=8)

    font_q = pygame.font.SysFont(None, 22)
    font_opt = pygame.font.SysFont(None, 20)
    font_small = pygame.font.SysFont(None, 18)

    lines = wrap_text(font_q, quiz_item["pertanyaan"], w - 40)
    yy = 18
    for line in lines:
        popup.blit(font_q.render(line, True, WHITE), (20, yy))
        yy += font_q.size(line)[1] + 6
    yy += 8
    for i, opt in enumerate(quiz_item["pilihan"]):
        box = pygame.Rect(20, yy, w - 40, 34)
        color = (60, 60, 60)
        if selected_idx == i:
            color = (90, 140, 200)
        pygame.draw.rect(popup, color, box, border_radius=6)
        popup.blit(font_opt.render(f"{chr(65+i)}. {opt}", True, WHITE), (30, yy + 6))
        yy += 40

    if result_msg:
        res_lines = wrap_text(font_small, result_msg, w - 40)
        yy += 6
        for line in res_lines:
            popup.blit(font_small.render(line, True, YELLOW), (20, yy))
            yy += font_small.size(line)[1] + 4

    surface.blit(popup, (x, y))

def run_quiz_loop(quiz_item, player):
    selected = 0
    result = None
    answered_correct = False
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_DOWN, pygame.K_s):
                    selected = (selected + 1) % len(quiz_item["pilihan"])
                elif ev.key in (pygame.K_UP, pygame.K_w):
                    selected = (selected - 1) % len(quiz_item["pilihan"])
                elif ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if selected == quiz_item["jawaban_benar"]:
                        result = "Jawaban benar! +10 poin"
                        player.score += 10
                        answered_correct = True
                    else:
                        result = "Salah. " + quiz_item.get("penjelasan", "")
                        player.score = max(0, player.score - 2)
                elif ev.key == pygame.K_ESCAPE:
                    return False

        screen.blit(maze_surface, (0, 0))
        for tx, ty, tsize in trees:
            draw_tree(screen, tx, ty, tsize)
        dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dim.fill((0,0,0,140))
        screen.blit(dim, (0,0))
        draw_quiz_popup(screen, quiz_item, selected_idx=selected, result_msg=result)
        pygame.display.flip()
        clock.tick(30)
        if result:
            pygame.time.delay(1200)
            return answered_correct

# --- SETUP SPRITES ---
quiz_sprites = []
for i, (qx, qy) in enumerate(QUIZ_POINTS):
    rect = pygame.Rect(0,0,28,28)
    rect.center = (qx, qy)
    quiz_sprites.append({"rect": rect, "index": i, "active": True})

trees = generate_trees()

def draw_hud(player):
    font = pygame.font.SysFont(None, 20)
    bg = pygame.Surface((280, 36), pygame.SRCALPHA)
    bg.fill(HUD_BG)
    screen.blit(bg, (8, 8))
    screen.blit(font.render(f"Score: {player.score}", True, WHITE), (14, 12))
    remaining = sum(1 for q in quiz_sprites if q["active"])
    screen.blit(font.render(f"Quiz tersisa: {remaining}/3", True, WHITE), (140, 12))

def draw_quiz_points():
    for q in quiz_sprites:
        cx, cy = q["rect"].center
        if not q["active"]:
            s = pygame.Surface((28*2, 28*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (0,0,0,140), (28,28), 14)
            screen.blit(s, (cx-28, cy-28))
            continue
        pygame.draw.circle(screen, (245, 230, 100), (cx, cy), 14)
        pygame.draw.circle(screen, BLACK, (cx, cy), 14, 2)
        fnt = pygame.font.SysFont(None, 22, bold=True)
        screen.blit(fnt.render("!", True, BLACK), (cx-6, cy-12))

# --- MAIN LOOP ---
def main():
    player = Player(50, 650)
    running = True

    print("=== KONTROL ===")
    print("  WASD atau Arrow Keys = Gerak")
    print("  ESC = Keluar")
    print("  Mobil HANYA bisa jalan di jalan!")
    print("  Kumpulkan 3 quiz untuk finish!")

    while running:
        dt = clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                running = False
        
        # Gerakan Player
        keys = pygame.key.get_pressed()
        vx = vy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            vx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            vx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            vy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            vy += 1
        
        if vx != 0 or vy != 0:
            mag = math.hypot(vx, vy)
            dx = vx / mag * player.speed
            dy = vy / mag * player.speed
            player.move(dx, dy, maze_surface)

        # Cek Quiz
        for q in quiz_sprites:
            if q["active"] and player.rect.colliderect(q["rect"]):
                idx = q["index"] % len(QUIZ_DATA)
                ok = run_quiz_loop(QUIZ_DATA[idx], player)
                if ok:
                    q["active"] = False
                else:
                    player.rect.center = (50, 650) # Hukuman balik ke start

        # Cek Finish
        finish_rect = pygame.Rect(1125, 625, 50, 50)
        if player.rect.colliderect(finish_rect):
            if all(not q["active"] for q in quiz_sprites):
                screen.fill(BG_RGB)
                fnt = pygame.font.SysFont(None, 40, bold=True)
                txt = fnt.render("SELAMAT! Kamu Menang!", True, WHITE)
                screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 - 40))
                sub = pygame.font.SysFont(None, 28).render(f"Score akhir: {player.score}", True, YELLOW)
                screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2 + 10))
                pygame.display.flip()
                pygame.time.delay(3000)
                running = False
                continue

        # Draw Semuanya
        screen.blit(maze_surface, (0, 0))
        for tx, ty, tsize in trees:
            draw_tree(screen, tx, ty, tsize)
        draw_quiz_points()
        screen.blit(player.image, player.rect.topleft)
        draw_hud(player)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()