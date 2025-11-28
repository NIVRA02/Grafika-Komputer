import sys
import math
import pygame
import cairo
import random

pygame.init()
try:
    pygame.mixer.quit()
except Exception:
    pass

WIDTH, HEIGHT = 1200, 700
FPS = 60

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

def create_cairo_surface():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(s)

    ctx.set_source_rgb(0.35, 0.65, 0.35)
    ctx.rectangle(0, 0, WIDTH, HEIGHT)
    ctx.fill()

    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
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

    ctx.set_source_rgb(0.25, 0.45, 0.25)
    ctx.set_line_width(50)
    for path in paths:
        ctx.new_path()
        ctx.move_to(path[0][0], path[0][1])
        for p in path[1:]:
            ctx.line_to(p[0], p[1])
        ctx.stroke()

    ctx.set_source_rgb(0.92, 0.92, 0.90)
    ctx.set_line_width(45)
    for path in paths:
        ctx.new_path()
        ctx.move_to(path[0][0], path[0][1])
        for p in path[1:]:
            ctx.line_to(p[0], p[1])
        ctx.stroke()

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

    def draw_house(x, y, w, h, c, roof):
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
        ctx.set_source_rgb(0.6, 0.4, 0.25)
        ctx.rectangle(x + w * 0.35, y + h * 0.6, w * 0.3, h * 0.4)
        ctx.fill()
        ctx.set_source_rgb(0.6, 0.75, 0.85)
        ctx.rectangle(x + w * 0.1, y + h * 0.4, w * 0.2, h * 0.15)
        ctx.fill()
        ctx.rectangle(x + w * 0.7, y + h * 0.4, w * 0.2, h * 0.15)
        ctx.fill()

    houses = [
        (80, 375, 40, 50, (0.85, 0.75, 0.6), (0.6, 0.3, 0.2)),
        (180, 500, 35, 45, (0.7, 0.8, 0.85), (0.4, 0.3, 0.5)),
        (380, 80, 40, 50, (0.9, 0.7, 0.5), (0.5, 0.25, 0.3)),
        (580, 380, 40, 50, (0.8, 0.75, 0.65), (0.5, 0.35, 0.3)),
        (680, 500, 40, 50, (0.85, 0.75, 0.7), (0.6, 0.35, 0.3)),
        (880, 100, 40, 50, (0.8, 0.75, 0.65), (0.5, 0.35, 0.3)),
    ]
    for h in houses:
        draw_house(*h)

    ctx.set_source_rgb(0.9, 0.2, 0.2)
    ctx.arc(1150, 650, 25, 0, 2 * math.pi)
    ctx.fill()
    ctx.set_source_rgb(1, 1, 1)
    ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(12)
    ctx.move_to(1130, 655)
    ctx.show_text("FINISH")

    return s

def cairo_surface_to_pygame(surface):
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

cairo_surf = create_cairo_surface()
maze_surface = cairo_surface_to_pygame(cairo_surf).convert_alpha()

def is_on_road(x, y, surf):
    x, y = int(x), int(y)
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return False
    try:
        r, g, b, a = surf.get_at((x, y))
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
        if is_on_road(x, y, maze_surface):
            attempts += 1
            continue
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

class Player:
    def _init_(self, x, y):
        self.w = 24
        self.h = 14
        self.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        self._draw_car()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3.0
        self.score = 0

    def _draw_car(self):
        self.image.fill((0, 0, 0, 0))
        body = pygame.Rect(0, 3, self.w, self.h - 5)
        pygame.draw.rect(self.image, RED, body, border_radius=3)
        pygame.draw.rect(self.image, (0, 0, 0), body, 2, border_radius=3)
        pygame.draw.circle(self.image, BLACK, (6, self.h - 2), 2)
        pygame.draw.circle(self.image, BLACK, (self.w - 6, self.h - 2), 2)

    def move(self, dx, dy, road_surface):
        nx = self.rect.centerx + dx
        ny = self.rect.centery + dy
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

def main():
    player = Player(50, 650)
    running = True

    print("🎮 KONTROL:")
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
        for q in quiz_sprites:
            if q["active"] and player.rect.colliderect(q["rect"]):
                idx = q["index"] % len(QUIZ_DATA)
                ok = run_quiz_loop(QUIZ_DATA[idx], player)
                if ok:
                    q["active"] = False
                else:
                    player.rect.center = (50, 650)
        finish_rect = pygame.Rect(1125, 625, 50, 50)
        if player.rect.colliderect(finish_rect):
            if all(not q["active"] for q in quiz_sprites):
                screen.fill(BG_RGB)
                fnt = pygame.font.SysFont(None, 40, bold=True)
                txt = fnt.render("🎉 SELAMAT! Kamu Menang! 🎉", True, WHITE)
                screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 - 40))
                sub = pygame.font.SysFont(None, 28).render(f"Score akhir: {player.score}", True, YELLOW)
                screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2 + 10))
                pygame.display.flip()
                pygame.time.delay(3000)
                running = False
                continue
        screen.blit(maze_surface, (0, 0))
        for tx, ty, tsize in trees:
            draw_tree(screen, tx, ty, tsize)
        draw_quiz_points()
        screen.blit(player.image, player.rect.topleft)
        draw_hud(player)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if _name_ == "_main_":
    main()