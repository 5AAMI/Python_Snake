import turtle  # pylint: disable=no-member
import random
import time

delay = 0.1
score = 0
high_score = 0

# Create the window and set the height and width
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("green")
wn.setup(width=700, height=700)
wn.tracer(0)

def draw_checkered_background():
    checkered = turtle.Turtle()
    checkered.speed(0)
    checkered.penup()
    checkered.hideturtle()

    colors = ['green', 'dark green']
    square_size = 20
    
    # Adjusted start positions to ensure the grid is centered and within the borders
    start_x = -300  # Original grid starting position
    start_y = 250   # Original grid starting position
    
    for y in range(start_y, -start_y, -square_size):
        for x in range(start_x, -start_x, square_size):
            color = colors[((x - start_x) // square_size + (y - start_y) // square_size) % 2]
            checkered.goto(x, y)
            checkered.fillcolor(color)
            checkered.begin_fill()
            for _ in range(4):
                checkered.forward(square_size)
                checkered.right(90)
            checkered.end_fill()

draw_checkered_background()

# Create a smaller border for the game
border = turtle.Turtle()
border.speed(5)
border.pensize(4)
border.penup()
border.goto(-300, 250)  # Adjusted to match the grid size
border.pendown()
border.color('yellow')
border.forward(600)  # Top border
border.right(90)
border.forward(500)  # Right border
border.right(90)
border.forward(600)  # Bottom border
border.right(90)
border.forward(500)  # Left border
border.penup()
border.hideturtle()

# Create the head of the snake
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("pink")
head.penup()
head.goto(0, 0)
head.direction = "Stop"

# Create food in the game
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

# Create space to show score and high score
scoreBoard = turtle.Turtle()
scoreBoard.speed(0)
scoreBoard.shape("square")
scoreBoard.color("white")
scoreBoard.penup()
scoreBoard.hideturtle()
scoreBoard.goto(0, 250)
scoreBoard.write("Score : 0  High Score : 0", align="center", font=("Courier", 25, "bold"))

# Create and display the title
title = turtle.Turtle()
title.speed(0)
title.color("white")
title.penup()
title.hideturtle()
title.goto(0, 290)
title.write("Saami's Awesome Snake", align="center", font=("Courier", 30, "bold"))

# Assign key directions
def move_up():
    if head.direction != "down":
        head.direction = "up"

def move_down():
    if head.direction != "up":
        head.direction = "down"

def move_left():
    if head.direction != "right":
        head.direction = "left"

def move_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

wn.listen()
wn.onkeypress(move_up, "Up")
wn.onkeypress(move_down, "Down")
wn.onkeypress(move_left, "Left")
wn.onkeypress(move_right, "Right")

segments = []

def reset_game():
    global score, delay
    time.sleep(1)
    head.goto(0, 0)
    head.direction = "Stop"
    for segment in segments:
        segment.goto(1000, 1000)  # Move segments off-screen
    segments.clear()
    score = 0
    delay = 0.1
    scoreBoard.clear()
    scoreBoard.write("Score : {}  High Score : {}".format(score, high_score), align="center", font=("Courier", 25, "bold"))

def generate_food():
    while True:
        x_cord = random.randint(-290, 270)
        y_cord = random.randint(-240, 240)
        if not any(segment.distance(x_cord, y_cord) < 20 for segment in segments):
            break
    food.goto(x_cord, y_cord)

# Main game loop
while True:
    wn.update()

    if head.xcor() > 280 or head.xcor() < -280 or head.ycor() > 240 or head.ycor() < -240:
        reset_game()

    # If snake collects food
    if head.distance(food) < 20:
        score += 10
        if score > high_score:
            high_score = score
        scoreBoard.clear()
        scoreBoard.write("Score : {}  High Score : {}".format(score, high_score), align="center", font=("Courier", 25, "bold"))
        
        generate_food()

        # Add a new segment to the snake
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("white smoke")
        new_segment.penup()
        segments.append(new_segment)

    # Move the snake segments
    for i in range(len(segments) - 1, 0, -1):
        x = segments[i - 1].xcor()
        y = segments[i - 1].ycor()
        segments[i].goto(x, y)
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move()

    # Check for collisions with the snake's own body
    for segment in segments:
        if segment.distance(head) < 20:
            reset_game()

    time.sleep(delay)

turtle.done()
