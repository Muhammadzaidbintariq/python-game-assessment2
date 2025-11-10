import tkinter as tk
import random

root = tk.Tk()
root.title("Color Catcher")
root.geometry("400x600")
root.configure(bg="black")

canvas = tk.Canvas(root, width=400, height=500, bg="black", highlightthickness=0)
canvas.pack()

colors = ["red", "green", "blue", "yellow", "purple"]
score = tk.IntVar(value=0)
game_over = False
speed = 100

score_label = tk.Label(root, text="Score: 0", font=("Arial", 16), fg="white", bg="black")
score_label.pack()

restart_button = None
paddle = None
bubble = None
bubble_color = None
bubble_y = 0

def setup_game():
    global paddle, bubble, bubble_color, bubble_y, score, speed, game_over
    canvas.delete("all")
    score.set(0)
    speed = 100
    game_over = False
    score_label.config(text="Score: 0")

    paddle_color = random.choice(colors)
    paddle = canvas.create_rectangle(170, 470, 230, 490, fill=paddle_color)

    spawn_bubble()
    move_bubble()

def spawn_bubble():
    global bubble, bubble_color, bubble_y
    bubble_color = random.choice(colors)
    x = random.randint(50, 350)
    bubble_y = 0
    bubble = canvas.create_oval(x-15, bubble_y, x+15, bubble_y+30, fill=bubble_color)

def move_bubble():
    global bubble_y, game_over
    if game_over:
        return
    bubble_y += 10
    canvas.move(bubble, 0, 10)
    if bubble_y >= 470:
        check_collision()
    else:
        root.after(speed, move_bubble)

def check_collision():
    global game_over, speed, restart_button
    paddle_coords = canvas.coords(paddle)
    bubble_coords = canvas.coords(bubble)
    px1, py1, px2, py2 = paddle_coords
    bx1, by1, bx2, by2 = bubble_coords

    if bx2 >= px1 and bx1 <= px2:
        if bubble_color == canvas.itemcget(paddle, "fill"):
            score.set(score.get() + 10)
            score_label.config(text=f"Score: {score.get()}")
            if score.get() % 30 == 0 and speed > 30:
                speed -= 10
        else:
            canvas.create_text(200, 250, text="Game Over", fill="white", font=("Arial", 24))
            game_over = True
            restart_button = tk.Button(root, text="Restart Game", font=("Arial", 14), command=restart_game)
            restart_button.pack(pady=10)
            return
    canvas.delete(bubble)
    spawn_bubble()
    move_bubble()

def restart_game():
    global restart_button
    if restart_button:
        restart_button.destroy()
        restart_button = None
    setup_game()

def move_left(event):
    if not game_over:
        canvas.move(paddle, -20, 0)

def move_right(event):
    if not game_over:
        canvas.move(paddle, 20, 0)

def change_color(event):
    if not game_over:
        new_color = random.choice(colors)
        canvas.itemconfig(paddle, fill=new_color)

root.bind("<Left>", move_left)
root.bind("<Right>", move_right)
root.bind("<Up>", change_color)

setup_game()
root.mainloop()