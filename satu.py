import sys
import math
import pygame
import random

# --- INISIALISASI ---
pygame.init()
try:
    pygame.mixer.quit()
except Exception:
    pass

WIDTH, HEIGHT = 1200, 700
FPS = 60

# --- WARNA ---
HUD_BG = (40, 40, 40, 180)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (241, 196, 15)
RED = (200, 50, 50)
PINK = (255, 105, 180)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 149, 237)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Maze - Traffic Sign Edition (All PNG)")
clock = pygame.time.Clock()

# --- LOAD GAMBAR DARI FILE PNG ---
try:
    maze_surface = pygame.image.load("peta.png").convert()
    car_img_original = pygame.image.load("mobil.png").convert_alpha()
    heart_image = pygame.image.load("hati.png").convert_alpha()
    house_image = pygame.image.load("rumah.png").convert_alpha()
    tree_image = pygame.image.load("pohon.png").convert_alpha()  # NEW: Load Pohon
    
    # Load Rambu
    SIGN_ASSETS = {
        "STOP": pygame.image.load("rambu_stop.png").convert_alpha(),
        "WARNING": pygame.image.load("rambu_warning.png").convert_alpha(),
        "NO_PARKING": pygame.image.load("rambu_no_parking.png").convert_alpha(),
        "BLUE": pygame.image.load("rambu_blue.png").convert_alpha(),
        "SPEED": pygame.image.load("rambu_speed.png").convert_alpha(),
        "GENERIC": pygame.image.load("rambu_generic.png").convert_alpha()
    }
except FileNotFoundError as e:
    print(f"ERROR: File gambar tidak ditemukan! ({e})")
    print("Pastikan sudah menjalankan: buat_peta.py, buat_pohon.py, dll.")
    sys.exit()

# --- LOGIKA GAME ---
def is_on_road(x, y, surf):
    x, y = int(x), int(y)
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return False
    try:
        r, g, b, a = surf.get_at((x, y))
        # Logika: Jalan itu warnanya abu-abu/putih, bukan hijau rumput
        return not (r < 100 and g > 150 and b < 100)
    except:
        return False

# Mapping indeks kuis ke tipe rambu
QUIZ_SIGN_MAPPING = {
    0: "WARNING", 1: "STOP", 2: "GENERIC", 3: "BLUE",
    4: "BLUE", 5: "NO_PARKING", 6: "SPEED", 7: "BLUE"
}

# --- DAFTAR LOKASI ---

# 1. POSISI RUMAH (X, Y)
HOUSE_POSITIONS = [
    (80, 375), (180, 500), (380, 80), (580, 380), (680, 500), (880, 100)
]

# 2. LOKASI POHON (FIXED)
FIXED_TREE_POSITIONS = [
    (80, 80), (200, 600), (1000, 100), (1100, 600),
    (300, 400), (600, 50), (700, 600), (900, 300),
    (50, 300), (1150, 50), (400, 600), (500, 100),
    (250, 150), (850, 500), (950, 50), (150, 50),
    (600, 300), (750, 100), (350, 550), (1050, 550),
    (450, 200), (120, 480), (980, 620), (20, 350),
    (1100, 300), (800, 650), (550, 450), (320, 120),
    (680, 380), (920, 180)
]

# 3. KANDIDAT LOKASI HATI
HEART_CANDIDATES = [
    (50, 600), (50, 500), (50, 400), (100, 550), (100, 450), (100, 350), 
    (150, 300), (150, 200), (150, 100), (200, 250), (250, 50), (350, 50), 
    (350, 200), (350, 300), (350, 450), (350, 550), (450, 150), (450, 250), 
    (450, 450), (550, 150), (550, 300), (550, 600), (650, 150), (650, 300), 
    (650, 500), (750, 200), (750, 300), (750, 500), (850, 200), (850, 300), 
    (850, 400), (850, 550), (950, 200), (950, 300), (950, 500), (1050, 200), 
    (1050, 300), (1050, 400), (1050, 500), (1150, 300), (1150, 400), (1150, 500), (1150, 600)
]

# 4. KANDIDAT LOKASI KUIS
QUIZ_CANDIDATES = [
    (150, 450), (200, 250), (400, 50), (450, 350), 
    (500, 550), (700, 250), (1050, 350), (1100, 550),
    (600, 150), (850, 450), (300, 550), (950, 250),
    (120, 150), (900, 550), (250, 350), (1050, 150)
]

def generate_objects(count, obj_type="tree", occupied_positions=[]):
    objects = []
    if obj_type == "heart":
        candidates = HEART_CANDIDATES[:]
        random.shuffle(candidates)
        for cx, cy in candidates:
            if len(objects) >= count: break
            if not is_on_road(cx, cy, maze_surface): continue 
            too_close = False
            for (ox, oy) in occupied_positions:
                 if math.hypot(cx - ox, cy - oy) < 60:
                     too_close = True; break
            if not too_close:
                rect = heart_image.get_rect(center=(cx, cy))
                objects.append({"rect": rect, "active": True})
        return objects
    elif obj_type == "tree":
        for pos in FIXED_TREE_POSITIONS: objects.append(pos)
        return objects
    return objects

# --- DATA KUIS ---
QUIZ_DATA = [
    {"pertanyaan": "Apa arti rambu segitiga dengan pinggir merah?", "pilihan": ["Perintah", "Larangan", "Peringatan", "Petunjuk"], "jawaban_benar": 2, "penjelasan": "Rambu segitiga mengandung peringatan."},
    {"pertanyaan": "Warna dasar rambu 'STOP' biasanya apa?", "pilihan": ["Hijau", "Merah", "Kuning", "Biru"], "jawaban_benar": 1, "penjelasan": "STOP berwarna merah."},
    {"pertanyaan": "Arti lampu kuning pada traffic light?", "pilihan": ["Stop langsung", "Persiapkan berhenti", "Jalan terus", "Mundur"], "jawaban_benar": 1, "penjelasan": "Kuning menandakan persiapan berhenti."},
    {"pertanyaan": "Marka jalan garis putih tidak putus artinya?", "pilihan": ["Boleh menyalip", "Dilarang menyalip", "Boleh parkir", "Jalan searah"], "jawaban_benar": 1, "penjelasan": "Garis utuh (solid) dilarang menyalip."},
    {"pertanyaan": "Apa kepanjangan dari SIM?", "pilihan": ["Surat Izin Mengemudi", "Surat Identitas Mobil", "Sistem Info Motor", "Surat Izin Masuk"], "jawaban_benar": 0, "penjelasan": "SIM adalah Surat Izin Mengemudi."},
    {"pertanyaan": "Rambu huruf 'P' dicoret merah artinya?", "pilihan": ["Parkir Gratis", "Tempat Parkir", "Dilarang Parkir", "Dilarang Putar Balik"], "jawaban_benar": 2, "penjelasan": "P dicoret berarti Dilarang Parkir."},
    {"pertanyaan": "Batas kecepatan di area perumahan biasanya?", "pilihan": ["100 km/jam", "60 km/jam", "30-40 km/jam", "10 km/jam"], "jawaban_benar": 2, "penjelasan": "Di pemukiman kecepatan harus rendah (30-40 km/jam)."},
    {"pertanyaan": "Fungsi utama helm saat berkendara adalah?", "pilihan": ["Gaya-gayaan", "Melindungi Kepala", "Agar tidak panas", "Menghindari tilang"], "jawaban_benar": 1, "penjelasan": "Helm berfungsi melindungi kepala dari benturan."},
]

class Player:
    def __init__(self, x, y):
        self.w, self.h = 24, 14
        self.original_image = car_img_original
        self.image = self.original_image
        self.angle = 0 
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3.0
        self.score = 0

    def rotate(self, angle):
        if self.angle != angle:
            self.angle = angle
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
            if angle == 90 or angle == 270: self.w, self.h = 14, 24 
            else: self.w, self.h = 24, 14

    def move(self, dx, dy, road_surface):
        nx = self.rect.centerx + dx
        ny = self.rect.centery + dy
        check_points = [
            (nx, ny),
            (nx + self.w//2 - 2, ny), (nx - self.w//2 + 2, ny),
            (nx, ny - self.h//2 + 2), (nx, ny + self.h//2 - 2),
        ]
        all_valid = True
        for px, py in check_points:
            if not is_on_road(px, py, road_surface):
                all_valid = False; break
        if all_valid:
            self.rect.centerx = int(nx); self.rect.centery = int(ny)
            return True
        return False

# --- UI HELPER ---
def wrap_text(font, text, max_w):
    words = text.split(" ")
    lines = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        if font.size(test)[0] <= max_w: cur = test
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def draw_quiz_popup(surface, quiz_item, selected_idx=None, result_msg=None):
    w, h = int(WIDTH * 0.7), int(HEIGHT * 0.6)
    x, y = (WIDTH - w) // 2, (HEIGHT - h) // 2
    popup = pygame.Surface((w, h), pygame.SRCALPHA)
    popup.fill((20, 20, 20, 220))
    pygame.draw.rect(popup, WHITE, (0, 0, w, h), 2, border_radius=8)
    font_q = pygame.font.SysFont(None, 22)
    font_opt = pygame.font.SysFont(None, 20)
    
    lines = wrap_text(font_q, quiz_item["pertanyaan"], w - 40)
    yy = 18
    for line in lines:
        popup.blit(font_q.render(line, True, WHITE), (20, yy))
        yy += 28
    yy += 8
    for i, opt in enumerate(quiz_item["pilihan"]):
        box = pygame.Rect(20, yy, w - 40, 34)
        color = (90, 140, 200) if selected_idx == i else (60, 60, 60)
        pygame.draw.rect(popup, color, box, border_radius=6)
        popup.blit(font_opt.render(f"{chr(65+i)}. {opt}", True, WHITE), (30, yy + 6))
        yy += 40
    if result_msg:
        surface.blit(popup, (x, y))
        res_lines = wrap_text(font_opt, result_msg, w - 40)
        yy_res = y + h - 60
        for line in res_lines:
            txt = font_opt.render(line, True, YELLOW)
            surface.blit(txt, (x + 20, yy_res)); yy_res += 20
    else:
        surface.blit(popup, (x, y))

def run_quiz_loop(quiz_item, player):
    selected = 0
    result = None
    answered_correct = False
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_DOWN, pygame.K_s): selected = (selected + 1) % len(quiz_item["pilihan"])
                elif ev.key in (pygame.K_UP, pygame.K_w): selected = (selected - 1) % len(quiz_item["pilihan"])
                elif ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if selected == quiz_item["jawaban_benar"]:
                        result = "Jawaban benar! +10 poin"; player.score += 10; answered_correct = True
                    else:
                        result = "Salah. " + quiz_item.get("penjelasan", ""); player.score = max(0, player.score - 2)
                elif ev.key == pygame.K_ESCAPE: return False
        
        # Render Ulang Scene
        screen.blit(maze_surface, (0, 0))
        for hx, hy in HOUSE_POSITIONS: screen.blit(house_image, (hx, hy))
        for tx, ty in trees: 
             # Gambar Pohon di-center sedikit ke atas
             screen.blit(tree_image, (tx - 20, ty - 50)) 
        
        dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dim.fill((0,0,0,140))
        screen.blit(dim, (0,0))
        draw_quiz_popup(screen, quiz_item, selected_idx=selected, result_msg=result)
        pygame.display.flip()
        clock.tick(30)
        if result: pygame.time.delay(1500); return answered_correct

def draw_hud(player, time_left):
    font = pygame.font.SysFont(None, 20)
    bg = pygame.Surface((380, 36), pygame.SRCALPHA)
    bg.fill(HUD_BG); screen.blit(bg, (8, 8))
    screen.blit(font.render(f"Score: {player.score}", True, WHITE), (14, 12))
    remaining = sum(1 for q in quiz_sprites if q["active"])
    screen.blit(font.render(f"Quiz tersisa: {remaining}/{len(quiz_sprites)}", True, WHITE), (120, 12))
    minutes = int(time_left // 60); seconds = int(time_left % 60)
    color = RED if time_left < 30 else WHITE
    screen.blit(font.render(f"Waktu: {minutes:02}:{seconds:02}", True, color), (260, 12))

def draw_quiz_points():
    for q in quiz_sprites:
        cx, cy = q["rect"].center
        if not q["active"]:
            s = pygame.Surface((32, 32), pygame.SRCALPHA)
            pygame.draw.circle(s, (0,0,0,50), (16,16), 10)
            screen.blit(s, (cx-16, cy-16))
            continue
        soal_idx = q["index"] % len(QUIZ_DATA)
        sign_type = QUIZ_SIGN_MAPPING.get(soal_idx, "GENERIC")
        sprite = SIGN_ASSETS[sign_type]
        rect = sprite.get_rect(center=(cx, cy))
        screen.blit(sprite, rect)

def draw_button(rect, text, mouse_pos):
    color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=10)
    font = pygame.font.SysFont(None, 30, bold=True)
    txt = font.render(text, True, WHITE)
    screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))

# --- GLOBAL GAME STATE ---
quiz_sprites = []
trees = []
hearts = []
bonus_texts = []

def reset_game(player):
    player.rect.center = (50, 650); player.score = 0; player.rotate(0)
    global quiz_sprites, trees, hearts
    quiz_sprites = []
    
    current_quiz_points = random.sample(QUIZ_CANDIDATES, 8)
    for i, (qx, qy) in enumerate(current_quiz_points):
        rect = pygame.Rect(0,0,28,28); rect.center = (qx, qy)
        quiz_sprites.append({"rect": rect, "index": i, "active": True})
    
    occupied_by_quiz = [(q["rect"].centerx, q["rect"].centery) for q in quiz_sprites]
    trees = generate_objects(60, "tree")
    hearts = generate_objects(5, "heart", occupied_positions=occupied_by_quiz)
    return pygame.time.get_ticks()

def main():
    player = Player(50, 650)
    TIME_LIMIT = 90
    start_ticks = reset_game(player) 
    last_checkpoint = (50, 650)
    running = True; game_over = False; win_status = False

    print("=== GAME START (Mode PNG) ===")

    while running:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        current_time = pygame.time.get_ticks()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: running = False
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE: running = False
            if game_over:
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 100, 200, 50).collidepoint(mouse_pos):
                        start_ticks = reset_game(player); last_checkpoint = (50, 650); game_over = False
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_r:
                    start_ticks = reset_game(player); last_checkpoint = (50, 650); game_over = False

        if game_over:
            screen.fill(BLACK)
            fnt_big = pygame.font.SysFont(None, 60, bold=True)
            txt = fnt_big.render("SELAMAT! KAMU MENANG!", True, YELLOW) if win_status else fnt_big.render("GAME OVER", True, RED)
            screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 - 50))
            score_txt = pygame.font.SysFont(None, 35).render(f"Skor Akhir: {player.score}", True, WHITE)
            screen.blit(score_txt, (WIDTH//2 - score_txt.get_width()//2, HEIGHT//2 + 10))
            draw_button(pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 100, 200, 50), "MAIN LAGI", mouse_pos)
            pygame.display.flip()
            continue

        # Logic
        time_left = max(0, TIME_LIMIT - (current_time - start_ticks) / 1000)
        if time_left == 0: game_over = True; win_status = False

        keys = pygame.key.get_pressed()
        vx = vy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: vx -= 1; player.rotate(180) 
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]: vx += 1; player.rotate(0)   
        if keys[pygame.K_UP] or keys[pygame.K_w]: vy -= 1; player.rotate(90)  
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]: vy += 1; player.rotate(270) 
        if vx or vy:
            mag = math.hypot(vx, vy)
            player.move(vx/mag * player.speed, vy/mag * player.speed, maze_surface)

        for q in quiz_sprites:
            if q["active"] and player.rect.colliderect(q["rect"]):
                idx = q["index"] % len(QUIZ_DATA)
                t_start = pygame.time.get_ticks()
                if run_quiz_loop(QUIZ_DATA[idx], player):
                    q["active"] = False; last_checkpoint = q["rect"].center
                else:
                    player.rect.center = last_checkpoint
                start_ticks += (pygame.time.get_ticks() - t_start)

        for h in hearts[:]:
            if h["active"] and player.rect.colliderect(h["rect"]):
                h["active"] = False; hearts.remove(h); start_ticks += 10000 
                bonus_texts.append({"text": "+10s", "pos": list(player.rect.midtop), "timer": 60})

        if player.rect.colliderect(pygame.Rect(1125, 625, 50, 50)):
            if all(not q["active"] for q in quiz_sprites): game_over = True; win_status = True

        # Drawing
        screen.blit(maze_surface, (0, 0))
        for hx, hy in HOUSE_POSITIONS: screen.blit(house_image, (hx, hy))
        for tx, ty in trees: 
             # Gambar Pohon di-center sedikit ke atas
             screen.blit(tree_image, (tx - 20, ty - 50)) 
        for h in hearts: 
            if h["active"]: screen.blit(heart_image, h["rect"])
        draw_quiz_points()
        screen.blit(player.image, player.rect.topleft)
        
        for b in bonus_texts[:]:
            b["pos"][1] -= 1; b["timer"] -= 1
            txt = pygame.font.SysFont(None, 24, bold=True).render(b["text"], True, PINK)
            screen.blit(txt, b["pos"])
            if b["timer"] <= 0: bonus_texts.remove(b)

        draw_hud(player, time_left)
        pygame.display.flip()

    pygame.quit(); sys.exit()

if __name__ == "__main__":
    main()