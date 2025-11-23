import turtle

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("TRAFFIC MAZE")
wn.setup(700, 700)


class Pen(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)

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

def setup_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]
            
            screen_x = -288 + (x * 24)
            screen_y = 288 - (y * 24)

            if character == "X":
                pen.goto(screen_x, screen_y)
                pen.stamp()
            
pen = Pen()


setup_maze(levels[1])

while True:
    wn.update() # Update the screen continuously