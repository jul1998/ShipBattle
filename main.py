import random
import time
from turtle import *

wn = Screen()
wn.title("Ship Game")
wn.setup(width=470, height=500)
wn.bgcolor("black")
wn.tracer(0)
wn.listen()

#Set up bullet state
is_bullet_ready = True
is_bullet_ready_for_pc = True

#Set up all pc and user positions
USER_POSITIONS =(-125, -100, -75, -50, -25, 25, 50, 75, 100, 125)
PC_POSITIONS =(-125,-100,-75,-50,-25,25,50,75,100,125)


#Set bullet position for user and pc
USER_BULLET_POSITION = (0, -165)
PC_BULLET_POSITION = (0, 165)

#Bullet speed
BULLET_DISTANCE = 25

#Coordenates for pc and user ships
x_pc_pos = -200
y_pc_pos = 200
x_user_pos = -200
y_user_pos = -150

# Draw space for computer ships. Ships will be within this rectangle
def draw_spaces(x_pos, y_pos):
    rectangle_figure = Turtle()
    rectangle_figure.hideturtle()
    rectangle_figure.sety(y_pos)
    rectangle_figure.setx(x_pos)
    rectangle_figure.color("white")
    rectangle_figure.penup()
    rectangle_figure.speed(0)
    for _ in range(2):
        rectangle_figure.pendown()
        rectangle_figure.forward(400)
        rectangle_figure.right(90)
        for _ in range(1):
            rectangle_figure.forward(50)
            rectangle_figure.right(90)

ships = [] # List for every ship so they can be used later
#Set ships for players
def set_ships(player_ship_positions, heading_angle, color, y_pos):
    pc_ships = [Turtle() for _ in range(10)]
    position = 0
    for ship in pc_ships:
        ship.speed(0)
        ship.penup()
        ship.color(color)
        ship.shape("arrow")
        ship.seth(heading_angle)
        ship.sety(y_pos)#-140
        ship.setx(player_ship_positions[position])
        ships.append(ship)
        position += 1

#Set bullet state for user to be fired when called
def prepare_bullet():
    global is_bullet_ready
    is_bullet_ready = True

#Move bullet among ships to be fired
def move_bullet_right():
    x_bullet = bullet.xcor() + BULLET_DISTANCE
    bullet.setx(x_bullet)
    if bullet.xcor() == 0:
        bullet.setx(25)
    if bullet.xcor() > 125:
        bullet.setx(125)
def move_bullet_left():
    x_bullet = bullet.xcor() - BULLET_DISTANCE
    bullet.setx(x_bullet)
    if bullet.xcor() == 0:
        bullet.setx(-25)
    if bullet.xcor() < -125:
        bullet.setx(-125)



true_ships_pc = [] # # List for every ship that will count as a real ship for players to gather points,
# so they can be used later

#Positions for user ships
def set_positions_for_ships(player_positions, heading, y_pos):
    """If position is already in list TRUE_POSITIONS, then it will select another number from list of positions. Hence,
    No position will be repeated"""
    TRUE_POSITIONS = []
    position =0
    while len(TRUE_POSITIONS) < 3:
        random_pos = random.choice(player_positions)
        if random_pos in TRUE_POSITIONS:
            pass
        else:
            TRUE_POSITIONS.append(random_pos)
            new_true_positon = Turtle()
            new_true_positon.penup()
            new_true_positon.color("green")
            new_true_positon.seth(heading)
            new_true_positon.goto(TRUE_POSITIONS[position], y_pos)
            true_ships_pc.append(new_true_positon)
            position += 1


# Create bullet for user
bullet = Turtle()
bullet.shape("arrow")
bullet.color("yellow")
bullet.penup()
bullet.goto(USER_BULLET_POSITION)
bullet.seth(90)
bullet.hideturtle()
bullet.shapesize(stretch_wid= 0.5, stretch_len = 0.5)

# Create bullet for pc
bullet_pc = Turtle()
bullet_pc.shape("arrow")
bullet_pc.color("yellow")
bullet_pc.penup()
bullet_pc.goto(PC_BULLET_POSITION)
bullet_pc.seth(270)
bullet_pc.shapesize(stretch_wid= 0.5, stretch_len = 0.5)


# Listen for keystrokes
wn.onkeypress(prepare_bullet, "space")
wn.onkeypress(move_bullet_right, "Right")
wn.onkeypress(move_bullet_left, "Left")

#Draw space for pc ships
draw_spaces(x_pc_pos, y_pc_pos)
#Draw space for user ships
draw_spaces(x_user_pos, y_user_pos)

#Ship positions for user
set_ships(USER_POSITIONS, 90, "red", -180)

#Ship positions for pc
set_ships(PC_POSITIONS, 270, "blue", 180)

#True Ships for pc
set_positions_for_ships(PC_POSITIONS, 270, 150)

#True ships for user
set_positions_for_ships(PC_POSITIONS, 90, -200)

# Set scores and positions for both player and user
user_points = 0
user_turns = 0
pc_turns = 0
pc_points = 0
game_on = True
while game_on:
    wn.update()
    time.sleep(0.01)
    #Every time we press the space key, bullet state for user will be True. Then, user can shoot
    if bullet.ycor() < 490 and is_bullet_ready:
        y_bullet = bullet.ycor() + 10
        bullet.sety(y_bullet)

    #Once bullet has reached the top of screen, its position will be the initial one
    if bullet.ycor() > 480:
        bullet.showturtle()
        bullet.goto(USER_BULLET_POSITION)
        is_bullet_ready = False

    #From here, user will start shooting. Once turns are equal to 6, it will pc's turn to attack
    user_attacking = True
    if user_turns < 6 and user_attacking:
        for pc_true_ship in true_ships_pc:
            if bullet.distance(pc_true_ship) < 10:
                print("Boom")
                user_turns += 1
                user_points += 1
                print(user_turns)
                print(user_points)
        for ship in ships:
            if bullet.distance(ship)<10:
                print("Missed")
                user_turns += 1
                user_turns-=1
                print(user_turns)



    #Pc's turn to attack randomly
    else:
        user_attacking = False
        if pc_turns < 6 and not user_attacking:
            x_random_pos_pc = random.choice(PC_POSITIONS)
            bullet.hideturtle()

            if bullet_pc.ycor() > -480 and is_bullet_ready_for_pc:
                bullet_pc.setx(x_random_pos_pc)
                y_bullet_pc = bullet_pc.ycor() - 10
                bullet_pc.sety(y_bullet_pc)
            if bullet_pc.ycor() < -480:
                bullet_pc.showturtle()
                bullet_pc.goto(PC_BULLET_POSITION)
                #is_bullet_ready_for_pc = False

            for user_true_ship in true_ships_pc:
                if bullet_pc.distance(user_true_ship) < 10:
                    print("Boom for pc")
                    pc_turns += 1
                    pc_points += 1
                    print(pc_turns)
                    print(pc_points)

wn.exitonclick()