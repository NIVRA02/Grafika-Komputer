import sys
import math
import pygame
import random
import game_assets  

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
PINK = (255, 105, 180)
GREEN = (89, 166, 89)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 149, 237)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Maze - Checkpoint System")
clock = pygame.time.Clock()

# --- PEMBUATAN MAP ---
maze_surface = game_assets.generate_map_surface(WIDTH, HEIGHT)

# --- LOGIKA GAME ---
def is_on_road(x, y, surf):
    x, y = int(x), int(y)
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return False
    try:
        r, g, b, a = surf.get_at((x, y))
        return r > 150 and g > 150 and b > 150
    except:
        return False

# --- GAMBAR HATI DIAMBIL DARI GAME_ASSETS ---
# Fungsi create_heart_sprite() sudah dihapus dari sini
heart_image = game_assets.create_heart_sprite()

# --- TITIK SPAWN HATI (SAFE SPOTS) ---
HEART_CANDIDATES = [
    (50, 600), (50, 500), (50, 400), 
    (100, 550), (100, 450), (100, 350), 
    (150, 300), (150, 200), (150, 100), 
    (200, 250), (250, 50), (350, 50), 
    (350, 200), (350, 300), (350, 450), (350, 550), 
    (450, 150), (450, 250), (450, 450), 
    (550, 150), (550, 300), (550, 600), 
    (650, 150), (650, 300), (650, 500), 
    (750, 200), (750, 300), (750, 500), 
    (850, 200), (850, 300), (850, 400), (850, 550),
    (950, 200), (950, 300), (950, 500),
    (1050, 200), (1050, 300), (1050, 400), (1050, 500),
    (1150, 300), (1150, 400), (1150, 500), (1150, 600)
]

def generate_objects(count, obj_type="tree"):
    objects = []
    attempts = 0
    
    if obj_type == "heart":
        candidates = HEART_CANDIDATES[:]
        random.shuffle(candidates)
        for cx, cy in candidates:
            if len(objects) >= count: break
            if not is_on_road(cx, cy, maze_surface): continue # Safety check warna

            too_close_quiz = False
            for q in QUIZ_POINTS:
                if math.hypot(cx - q[0], cy - q[1]) < 60:
                    too_close_quiz = True
                    break
            
            if not too_close_quiz:
                rect = heart_image.get_rect(center=(cx, cy))
                objects.append({"rect": rect, "active": True})
        return objects

    while len(objects) < count and attempts < 1000:
        x = random.randint(30, WIDTH - 30)
        y = random.randint(30, HEIGHT - 30)
        if not is_on_road(x, y, maze_surface):
            too_close = False
            for obj in objects:
                ox, oy = obj[0], obj[1]
                if math.hypot(x - ox, y - oy) < 30:
                    too_close = True; break
            if not too_close:
                size = random.choice([12, 14, 16, 18])
                objects.append((x, y, size))
        attempts += 1
    return objects

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
    {"pertanyaan": "Apa arti rambu segitiga dengan pinggir merah?", "pilihan": ["Perintah", "Larangan", "Peringatan", "Petunjuk"], "jawaban_benar": 2, "penjelasan": "Rambu segitiga mengandung peringatan."},
    {"pertanyaan": "Warna dasar rambu 'STOP' biasanya apa?", "pilihan": ["Hijau", "Merah", "Kuning", "Biru"], "jawaban_benar": 1, "penjelasan": "STOP berwarna merah."},
    {"pertanyaan": "Arti lampu kuning pada traffic light?", "pilihan": ["Stop langsung", "Persiapkan berhenti", "Jalan terus", "Mundur"], "jawaban_benar": 1, "penjelasan": "Kuning menandakan persiapan berhenti."},
    {"pertanyaan": "Marka jalan garis putih tidak putus artinya?", "pilihan": ["Boleh menyalip", "Dilarang menyalip", "Boleh parkir", "Jalan searah"], "jawaban_benar": 1, "penjelasan": "Garis utuh (solid) dilarang menyalip."},
    {"pertanyaan": "Apa kepanjangan dari SIM?", "pilihan": ["Surat Izin Mengemudi", "Surat Identitas Mobil", "Sistem Info Motor", "Surat Izin Masuk"], "jawaban_benar": 0, "penjelasan": "SIM adalah Surat Izin Mengemudi."},
    {"pertanyaan": "Rambu huruf 'P' dicoret merah artinya?", "pilihan": ["Parkir Gratis", "Tempat Parkir", "Dilarang Parkir", "Dilarang Putar Balik"], "jawaban_benar": 2, "penjelasan": "P dicoret berarti Dilarang Parkir."},
    {"pertanyaan": "Batas kecepatan di area perumahan biasanya?", "pilihan": ["100 km/jam", "60 km/jam", "30-40 km/jam", "10 km/jam"], "jawaban_benar": 2, "penjelasan": "Di pemukiman kecepatan harus rendah (30-40 km/jam)."},
    {"pertanyaan": "Fungsi utama helm saat berkendara adalah?", "pilihan": ["Gaya-gayaan", "Melindungi Kepala", "Agar tidak panas", "Menghindari tilang"], "jawaban_benar": 1, "penjelasan": "Helm berfungsi melindungi kepala dari benturan."},
]

QUIZ_POINTS = [
    (150, 450), (200, 250), (400, 50), (450, 350), 
    (500, 550), (700, 250), (950, 350), (1100, 550),
]

# --- CLASS PLAYER ---
class Player:
    def __init__(self, x, y):
        self.w = 24
        self.h = 14
        self.image = game_assets.create_car_sprite(self.w, self.h, RED)
        self.original_image = self.image 
        self.angle = 0 
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3.0
        self.score = 0

    def rotate(self, angle):
        if self.angle != angle:
            self.angle = angle
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
            if angle == 90 or angle == 270: 
                self.w, self.h = 14, 24 
            else: 
                self.w, self.h = 24, 14

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

def draw_hud(player, time_left):
    font = pygame.font.SysFont(None, 20)
    bg = pygame.Surface((380, 36), pygame.SRCALPHA)
    bg.fill(HUD_BG)
    screen.blit(bg, (8, 8))
    screen.blit(font.render(f"Score: {player.score}", True, WHITE), (14, 12))
    remaining = sum(1 for q in quiz_sprites if q["active"])
    total_quiz = len(quiz_sprites)
    screen.blit(font.render(f"Quiz tersisa: {remaining}/{total_quiz}", True, WHITE), (120, 12))
    
    minutes = int(time_left // 60)
    seconds = int(time_left % 60)
    timer_text = f"Waktu: {minutes:02}:{seconds:02}"
    timer_color = WHITE if time_left >= 30 else RED
    screen.blit(font.render(timer_text, True, timer_color), (260, 12))

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

def draw_button(rect, text, mouse_pos):
    color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=10)
    font = pygame.font.SysFont(None, 30, bold=True)
    txt_surf = font.render(text, True, WHITE)
    screen.blit(txt_surf, (rect.centerx - txt_surf.get_width()//2, rect.centery - txt_surf.get_height()//2))
    return rect.collidepoint(mouse_pos)

# --- GLOBAL GAME STATE ---
quiz_sprites = []
trees = []
hearts = []
bonus_texts = []

def reset_game(player):
    """Mengembalikan semua variabel game ke kondisi awal"""
    random.seed(42) 
    
    player.rect.center = (50, 650)
    player.score = 0
    player.rotate(0)
    
    global quiz_sprites
    quiz_sprites = []
    for i, (qx, qy) in enumerate(QUIZ_POINTS):
        rect = pygame.Rect(0,0,28,28)
        rect.center = (qx, qy)
        quiz_sprites.append({"rect": rect, "index": i, "active": True})
        
    global trees
    trees = generate_objects(60, "tree")
    
    global hearts
    hearts = generate_objects(5, "heart")
    
    return pygame.time.get_ticks()

# --- MAIN LOOP ---
def main():
    player = Player(50, 650)
    
    TIME_LIMIT = 90 # 1 Menit 30 Detik
    start_ticks = reset_game(player) 
    
    # SYSTEM CHECKPOINT
    last_checkpoint = (50, 650) # Inisialisasi checkpoint awal di Start
    
    running = True
    game_over = False
    win_status = False

    print("=== KONTROL ===")
    print("  WASD / Panah = Gerak")
    print("  ESC = Keluar")
    print("  R = Reset di Game Over")
    print("  Ambil HATI untuk +10 Detik!")

    while running:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        current_time = pygame.time.get_ticks()
        
        # --- EVENT HANDLING ---
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                running = False
            
            if game_over:
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    btn_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 100, 200, 50)
                    if btn_rect.collidepoint(mouse_pos):
                        start_ticks = reset_game(player)
                        last_checkpoint = (50, 650) # Reset checkpoint saat game reset
                        game_over = False
                        win_status = False
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_r:
                    start_ticks = reset_game(player)
                    last_checkpoint = (50, 650)
                    game_over = False
                    win_status = False

        if game_over:
            screen.fill(BLACK)
            fnt_big = pygame.font.SysFont(None, 60, bold=True)
            if win_status:
                txt = fnt_big.render("SELAMAT! KAMU MENANG!", True, YELLOW)
            else:
                txt = fnt_big.render("GAME OVER - WAKTU HABIS!", True, RED)
            screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 - 50))
            
            fnt_small = pygame.font.SysFont(None, 35)
            score_txt = fnt_small.render(f"Skor Akhir: {player.score}", True, WHITE)
            screen.blit(score_txt, (WIDTH//2 - score_txt.get_width()//2, HEIGHT//2 + 10))
            
            btn_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 100, 200, 50)
            draw_button(btn_rect, "MAIN LAGI", mouse_pos)
            pygame.display.flip()
            continue

        # --- LOGIKA GAMEPLAY ---
        
        # 1. Timer
        seconds_passed = (current_time - start_ticks) / 1000
        time_left = TIME_LIMIT - seconds_passed
        
        if time_left <= 0:
            time_left = 0
            game_over = True
            win_status = False
            
        # 2. Gerakan Player
        keys = pygame.key.get_pressed()
        vx = vy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            vx -= 1; player.rotate(180) 
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            vx += 1; player.rotate(0)   
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            vy -= 1; player.rotate(90)  
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            vy += 1; player.rotate(270) 
        
        if vx != 0 or vy != 0:
            mag = math.hypot(vx, vy)
            dx = vx / mag * player.speed
            dy = vy / mag * player.speed
            player.move(dx, dy, maze_surface)

        # 3. Cek Quiz (DENGAN LOGIKA CHECKPOINT)
        for q in quiz_sprites:
            if q["active"] and player.rect.colliderect(q["rect"]):
                idx = q["index"] % len(QUIZ_DATA)
                t_start_quiz = pygame.time.get_ticks()
                
                # Jalankan Kuis
                ok = run_quiz_loop(QUIZ_DATA[idx], player)
                
                t_end_quiz = pygame.time.get_ticks()
                start_ticks += (t_end_quiz - t_start_quiz) 
                
                if ok: 
                    q["active"] = False
                    # Jika benar, jadikan lokasi ini checkpoint baru
                    last_checkpoint = q["rect"].center
                else: 
                    # Jika salah, kembalikan ke checkpoint terakhir
                    player.rect.center = last_checkpoint
                    
        # 4. Cek Hati (Bonus Waktu)
        for h in hearts[:]:
            if h["active"] and player.rect.colliderect(h["rect"]):
                h["active"] = False
                hearts.remove(h)
                start_ticks += 10000 
                bonus_texts.append({"text": "+10s", "pos": list(player.rect.midtop), "timer": 60})

        # 5. Cek Finish
        finish_rect = pygame.Rect(1125, 625, 50, 50)
        if player.rect.colliderect(finish_rect):
            if all(not q["active"] for q in quiz_sprites):
                game_over = True
                win_status = True

        # 6. Drawing
        screen.blit(maze_surface, (0, 0))
        for tx, ty, tsize in trees:
            draw_tree(screen, tx, ty, tsize)
            
        for h in hearts:
            if h["active"]:
                screen.blit(heart_image, h["rect"])

        draw_quiz_points()
        screen.blit(player.image, player.rect.topleft)
        
        for b in bonus_texts[:]:
            b["pos"][1] -= 1 # Animasi teks ke atas
            b["timer"] -= 1
            fnt = pygame.font.SysFont(None, 24, bold=True)
            txt = fnt.render(b["text"], True, PINK)
            screen.blit(txt, b["pos"])
            if b["timer"] <= 0:
                bonus_texts.remove(b)

        draw_hud(player, time_left)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()