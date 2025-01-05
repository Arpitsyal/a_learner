import turtle
import random

# Screen Initialization
SCREEN_SIZE = 600
BORDER_SIZE = 300
turtle.setup(SCREEN_SIZE, SCREEN_SIZE)
turtle.bgcolor("black")
turtle.bgpic("D://animated-flying-through-the-stars-and-blue-nebula-in-space-suitable-for-background-or-others-free-video.gif")
turtle.title("Spacewar")
turtle.tracer(0)
turtle.hideturtle()

# Base Sprite Class
class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, color, startx, starty):
        super().__init__(shape=spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.goto(startx, starty)
        self.move_speed = 1

    def move(self):
        self.fd(self.move_speed)
        if self.xcor() > BORDER_SIZE:
            self.setx(BORDER_SIZE)
            self.rt(60)
        if self.xcor() < -BORDER_SIZE:
            self.setx(-BORDER_SIZE)
            self.rt(60)
        if self.ycor() > BORDER_SIZE:
            self.sety(BORDER_SIZE)
            self.rt(60)
        if self.ycor() < -BORDER_SIZE:
            self.sety(-BORDER_SIZE)
            self.rt(60)

    def is_collision(self, other):
        return self.distance(other) < 20  # Collision threshold

# Player Class
class Player(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        super().__init__(spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.6, stretch_len=1.1, outline=None)
        self.move_speed = 4
        self.lives = 3

    def turn_left(self):
        self.lt(45)

    def turn_right(self):
        self.rt(45)

    def accelerate(self):
        self.move_speed += 1

    def decelerate(self):
        if self.move_speed > 1:  # Prevent negative speed
            self.move_speed -= 1

# Enemy Class
class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        super().__init__(spriteshape, color, startx, starty)
        self.move_speed = 6
        self.setheading(random.randint(0, 360))

# Ally Class
class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        super().__init__(spriteshape, color, startx, starty)
        self.move_speed = 8
        self.setheading(random.randint(0, 360))

# Particle Class for Explosion
class Particle(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        super().__init__(spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.2, stretch_len=0.2, outline=None)
        self.goto(-1000, -1000)
        self.frame = 0

    def explode(self, startx, starty):
        self.goto(startx, starty)
        self.setheading(random.randint(0, 360))
        self.frame = 1

    def move(self):
        if self.frame > 0:
            self.fd(5)
            self.frame += 1
            self.color("orange")
        if self.frame > 20:
            self.frame = 0
            self.goto(-1000, -1000)

# Missile Class
class Missile(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        super().__init__(spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.3, stretch_len=0.4)
        self.speed = 20
        self.status = "ready"
        self.goto(-1000, 1000)

    def fire(self):
        if self.status == "ready":
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.status = "firing"

    def move(self):
        if self.status == "firing":
            self.fd(self.speed)
            if abs(self.xcor()) > BORDER_SIZE or abs(self.ycor()) > BORDER_SIZE:
                self.reset_missile()

    def reset_missile(self):
        self.status = "ready"
        self.goto(-1000, 1000)

# Game Class
class Game:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.level = 1
        self.border_pen = turtle.Turtle()
        self.status_pen = turtle.Turtle()
        self.border_pen.speed(0)
        self.border_pen.color("white")
        self.border_pen.penup()
        self.border_pen.ht()
        self.status_pen.speed(0)
        self.status_pen.color("white")
        self.status_pen.penup()
        self.status_pen.ht()
        self.draw_border()
        self.update_status()

    def draw_border(self):
        self.border_pen.goto(-BORDER_SIZE, BORDER_SIZE)
        self.border_pen.pendown()
        for _ in range(4):
            self.border_pen.fd(2 * BORDER_SIZE)
            self.border_pen.rt(90)
        self.border_pen.penup()

    def update_status(self):
        self.status_pen.clear()
        self.status_pen.goto(-290, 260)
        self.status_pen.write(f"Score: {self.score}  Lives: {self.lives}  Level: {self.level}",
                              font=("Arial", 16, "normal"))

# Create Game Components
game = Game()
player = Player("triangle", "white", 0, 0)
missile = Missile("triangle", "yellow", 0, 0)
enemies = [Enemy("circle", "red", -100, 0) for _ in range(6)]
allies = [Ally("square", "blue", 100, 0) for _ in range(6)]
particles = [Particle("circle", "orange", 0, 0) for _ in range(20)]

# Bind Keyboard Events
turtle.listen()
turtle.onkey(player.turn_left, "Left")
turtle.onkey(player.turn_right, "Right")
turtle.onkey(player.accelerate, "Up")
turtle.onkey(player.decelerate, "Down")
turtle.onkey(missile.fire, "space")

# Game Loop
def game_loop():
    turtle.update()
    player.move()
    missile.move()

    for enemy in enemies:
        enemy.move()
        if player.is_collision(enemy):
            player.lives -= 1
            game.lives = player.lives
            game.update_status()
            enemy.goto(random.randint(-BORDER_SIZE + 50, BORDER_SIZE - 50),
                       random.randint(-BORDER_SIZE + 50, BORDER_SIZE - 50))

        if missile.is_collision(enemy):
            game.score += 10
            game.update_status()
            enemy.goto(random.randint(-BORDER_SIZE + 50, BORDER_SIZE - 50),
                       random.randint(-BORDER_SIZE + 50, BORDER_SIZE - 50))
            missile.reset_missile()
            for particle in particles:
                particle.explode(enemy.xcor(), enemy.ycor())

    for ally in allies:
        ally.move()
        if missile.is_collision(ally):
            game.score -= 5
            game.update_status()
            ally.goto(random.randint(-BORDER_SIZE + 50, BORDER_SIZE - 50),
                      random.randint(-BORDER_SIZE + 50, BORDER_SIZE - 50))
            missile.reset_missile()
            for particle in particles:
                particle.explode(ally.xcor(), ally.ycor())

    for particle in particles:
        particle.move()

    if player.lives <= 0:
        game.status_pen.goto(0, 0)
        game.status_pen.write("Game Over!", align="center", font=("Arial", 24, "bold"))
        return

    turtle.ontimer(game_loop, 20)

# Start the Game Loop
game_loop()
turtle.done()
