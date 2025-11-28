import turtle
import tekstur  
import math

# Pastikan fungsi ini mengembalikan string path gambar atau nama shape yang valid
Tembok = tekstur.buat_tekstur_tembok() 

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("TRAFFIC MAZE")
wn.setup(700, 700)
wn.tracer(0) # Mematikan update layar otomatis agar game lebih cepat (manual update di bawah)

wn.register_shape(Tembok)

class Pen(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape(Tembok) 
        self.penup()
        self.speed(0)

class Player(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square") 
        self.color("blue") 
        self.penup()
        self.speed(0)
        self.gold = 0  # PERBAIKAN 1: Menambahkan atribut gold awal

    def go_up(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() + 24  
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_down(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() - 24  
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_left(self):
        move_to_x = self.xcor() - 24
        move_to_y = self.ycor()   
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_right(self):
        move_to_x = self.xcor() + 24
        move_to_y = self.ycor()   
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def is_collision(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))
        if distance < 20: # PERBAIKAN: Jarak 5 terlalu kecil, perbesar jadi 20 biar gampang kena
            return True
        else:
            return False

class Treasure(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("circle")  
        self.color("gold")    
        self.penup()
        self.speed(0)
        self.gold = 100 
        self.goto(x, y)

    def destro(self):   
        self.goto(2000, 2000)
        self.hideturtle()

# --- DATA LEVEL ---
levels = [""]

level_1 = [
    "XXXXXXXXXXXXXXXXXXXXXXX X",
    "Xp  X   X     X   X   X X",
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
    "XXX X X X X X X X XTXXX X",
    "X   X X   X   X   X X   X",
    "X X X X XXXXXXXXX X X X X",
    "X X X X X   X   X X X X X",
    "X X X X X X X X X X X X X",
    "X   X   X X X X X XT  X X",
    "X X X X X X X X X X X X X",
    "X X   X     X   X   X   X",
    "X XXXXXXXXXXXXXXXXXXXXXXX"
]

levels.append(level_1)

# PERBAIKAN 2: Membuat List kosong untuk menampung harta karun
treasures = []

def setup_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]
            screen_x = -288 + (x * 24)
            screen_y = 288 - (y * 24)

            if character == "X":
                pen.goto(screen_x, screen_y)
                pen.stamp()
                walls.append((screen_x, screen_y))

            if character == "p":
                player.goto(screen_x, screen_y)

            if character == "T":
                # PERBAIKAN 3: Append ke list 'treasures', bukan ke Class 'Treasure'
                treasures.append(Treasure(screen_x, screen_y))

pen = Pen()
walls = []

player = Player()
setup_maze(levels[1])

turtle.listen()
turtle.onkey(player.go_left, "Left")
turtle.onkey(player.go_right, "Right")
turtle.onkey(player.go_up, "Up")  
turtle.onkey(player.go_down, "Down")

while True:
    # PERBAIKAN 4: Loop melalui list 'treasures'
    for treasure in treasures:
        if player.is_collision(treasure):
            player.gold += treasure.gold
            print(f"Goldmu: {player.gold}")
            treasure.destro()
            # PERBAIKAN 5: Remove dari list 'treasures'
            treasures.remove(treasure) 
    
    wn.update()