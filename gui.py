# import tkinter as tk 
# from PIL import Image, ImageTk

# root = tk.Tk()
# root.title("Chutes and Ladders")

# board_image = Image.open("OIP.jpg")
# board_image = board_image.resize((600, 600))
# board_photo = ImageTk.PhotoImage(board_image)

# canvas = tk.Canvas(root, width=600, height=600)
# canvas.pack()

# canvas.create_image(0, 0, anchor=tk.NW, image=board_photo)

# num_of_players = input("How many Players are involved?")
# nOP = int(num_of_players)
# players = []

# for player in range(0,nOP):
#     names = input(f'What is Player {player + 1} name?')
#     players.append(names)
# default_colors = ["red", "blue", "green", "orange", "purple", "cyan", "magenta", "yellow"]
# colors = default_colors[:len(players)]

# tokens = []
# for i in range(len(players)):
#     token = canvas.create_oval(0, 0, 0, 0, fill=colors[i], outline="black")
#     tokens.append(token)
# # player_token = canvas.create_oval(50, 550, 70, 570, fill="red", outline="black")

# def move_token_to_square(square_number):

#     square_coords = {
#         1: (30, 580), 20: (30, 520), 21: (30, 460), 40: (30, 400), 41: (30, 340), 60: (30, 280), 61: (30, 220), 80: (30, 160), 81: (30, 100), 100: (30, 40),
#         2: (90, 580), 19: (90, 520), 22: (90, 460), 39: (90, 400), 42: (90, 340), 59: (90, 280), 62: (90, 220), 79: (90, 160), 82: (90, 100), 99: (90, 40),
#         3: (150, 580), 18: (150, 520), 23: (150, 460), 38: (150, 400), 43: (150, 340), 58: (150, 280), 63: (150, 220), 78: (150, 160), 83: (150, 100), 98: (150, 40),
#         4: (210, 580), 17: (210, 520), 24: (210, 460), 37: (210, 400), 44: (210, 340), 57: (210, 280), 64: (210, 220), 77: (210, 160), 84: (210, 100), 97: (210, 40),
#         5: (270, 580), 16: (270, 520), 25: (270, 460), 36: (270, 400), 45: (270, 340), 56: (270, 280), 65: (270, 220), 76: (270, 160), 85: (270, 100), 96: (270, 40),
#         6: (330, 580), 15: (330, 520), 26: (330, 460), 35: (330, 400), 46: (330, 340), 55: (330, 280), 66: (330, 220), 75: (330, 160), 86: (330, 100), 95: (330, 40),
#         7: (390, 580), 14: (390, 520), 27: (390, 460), 34: (390, 400), 47: (390, 340), 54: (390, 280), 67: (390, 220), 74: (390, 160), 87: (390, 100), 94: (390, 40),
#         8: (450, 580), 13: (450, 520), 28: (450, 460), 33: (450, 400), 48: (450, 340), 53: (450, 280), 68: (450, 220), 73: (450, 160), 88: (450, 100), 93: (450, 40),
#         9: (510, 580), 12: (510, 520), 29: (510, 460), 32: (510, 400), 49: (510, 340), 52: (510, 280), 69: (510, 220), 72: (510, 160), 89: (510, 100), 92: (510, 40),
#         10: (570, 580), 11: (570, 520), 30: (570, 460), 31: (570, 400), 50: (570, 340), 51: (570, 280), 70: (570, 220), 71: (570, 160), 90: (570, 100), 91: (570, 40),
#     }

#     x, y = square_coords.get(square_number, (50,550))

#     r = 10
#     canvas.coords(player_token, x - r, y - r, x + r, y + r)

# move_token_to_square(50)

# root.mainloop()

# # Example for a 10x10 board, zigzag layout
# def get_square_coordinates(square):
#     row = (square - 1) // 10
#     col = (square - 1) % 10
#     if row % 2 == 1:
#         col = 9 - col  # Reverse direction every other row

#     x = 60 * col + 30   # Adjust based on your image scale
#     y = 600 - (row * 60 + 30)
#     return (x, y)
import tkinter as tk
from PIL import Image, ImageTk
import random

# --- Game Settings ---
BOARD_SIZE = 600
GRID_SIZE = 10
CELL_SIZE = BOARD_SIZE // GRID_SIZE
PLAYER_RADIUS = 10

chutes_and_ladders = {
    # ladder
    1 : 38, 4: 14, 9 : 31, 28 : 84, 36 : 44, 40 : 42, 51 : 67, 71 : 91, 80 : 100,
    # chutes
    16 : 6, 49 : 11, 62: 19, 87 : 24, 47 : 26, 56 : 53, 64 : 60, 93 : 73, 95: 75, 98 : 78,
}

default_colors = ["red", "blue", "green", "orange", "purple", "cyan", "magenta", "yellow"]

# --- Global Game Variables ---
players = []
positions = []
colors = []
tokens = []
current_player = 0

# --- Tkinter Setup ---
root = tk.Tk()
root.title("Chutes and Ladders")

# --- Game Frame (Created Later) ---
game_frame = None
canvas = None
roll_button = None
status_label = None
board_photo = None

# --- Step 1: Player Setup Form ---
def show_player_setup():
    setup_frame = tk.Frame(root)
    setup_frame.pack(padx=20, pady=20)

    tk.Label(setup_frame, text="Enter number of players (2–8):").pack()
    num_entry = tk.Entry(setup_frame)
    num_entry.pack()

    def submit_num():
        try:
            num = int(num_entry.get())
            if 2 <= num <= 8:
                setup_frame.destroy()
                enter_player_names(num)
            else:
                tk.Label(setup_frame, text="Please enter 2–8 players").pack()
        except ValueError:
            tk.Label(setup_frame, text="Invalid number").pack()

    tk.Button(setup_frame, text="Next", command=submit_num).pack(pady=5)

# --- Step 2: Enter Player Names ---
def enter_player_names(count):
    name_frame = tk.Frame(root)
    name_frame.pack(padx=20, pady=20)

    entries = []
    for i in range(count):
        tk.Label(name_frame, text=f"Player {i + 1} name:").pack()
        e = tk.Entry(name_frame)
        e.pack()
        entries.append(e)

    def start_game():
        global players, colors, positions
        for e in entries:
            name = e.get().strip()
            if name:
                players.append(name)
        if len(players) >= 2:
            colors.extend(default_colors[:len(players)])
            positions.extend([0] * len(players))
            name_frame.destroy()
            launch_game()
        else:
            tk.Label(name_frame, text="Enter at least 2 valid names").pack()

    tk.Button(name_frame, text="Start Game", command=start_game).pack(pady=10)

# --- Step 3: Launch Game ---
def launch_game():
    global game_frame, canvas, roll_button, status_label, board_photo, tokens, dice_label

    game_frame = tk.Frame(root)
    game_frame.pack()

    canvas = tk.Canvas(game_frame, width=BOARD_SIZE, height=BOARD_SIZE)
    canvas.grid(row=0, column=0, columnspan=2)

    # Load and draw board image
    img = Image.open("OIP.jpg").resize((BOARD_SIZE, BOARD_SIZE))
    board_photo = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, anchor=tk.NW, image=board_photo)

    # Create player tokens
    tokens.clear()
    for i in range(len(players)):
        token = canvas.create_oval(0, 0, 0, 0, fill=colors[i], outline="black")
        tokens.append(token)
        move_token(i)  # Start at position 0

    #showing dice roll
    dice_label = tk.Label(game_frame, text="Last roll: -")
    dice_label.grid(row=2, column=0, columnspan=2)
    # Controls
    roll_button = tk.Button(game_frame, text="Roll Dice", command=take_turn)
    roll_button.grid(row=1, column=0, pady=10)

    status_label = tk.Label(game_frame, text=f"{players[0]}'s turn")
    status_label.grid(row=1, column=1, pady=10)

# --- Utility Functions ---
def get_square_coordinates(square):
    square = max(1, min(square, 100))
    row = (square - 1) // GRID_SIZE
    col = (square - 1) % GRID_SIZE
    if row % 2 == 1:
        col = GRID_SIZE - 1 - col
    x = col * CELL_SIZE + CELL_SIZE // 2
    y = BOARD_SIZE - (row * CELL_SIZE + CELL_SIZE // 2)
    return x, y

def move_token(player_index):
    square = positions[player_index]
    x, y = get_square_coordinates(square if square > 0 else 1)
    # Offset overlapping tokens
    offset = (player_index % 3) * 5
    x += offset
    y -= offset
    r = PLAYER_RADIUS
    canvas.coords(tokens[player_index], x - r, y - r, x + r, y + r)

def roll_dice():
    return random.randint(1, 6)

def update_position(player_index, roll):
    # pos = positions[player_index] + roll
    # if pos <= 100:
    #     positions[player_index] = chutes_and_ladders.get(pos, pos)
    start = positions[player_index] + roll
    if start > 100:
        return None
    final = chutes_and_ladders.get(start, start)
    positions[player_index] = final

    if start != final:
        if final > start:
            return f"Ladder! Climbed from {start} to {final}"
        else:
            return f"Chute! Slid from [start] to {final}"
    return None
def take_turn():
    global current_player
    player_name = players[current_player]
    roll = roll_dice()

    dice_label.config(text=f"Last roll: {roll}")
    status_label.config(text=f"{player_name} rolled a {roll}")

    # update_position(current_player, roll)
    # move_token(current_player)

    special_msg = update_position(current_player, roll)
    move_token(current_player)

    if positions[current_player] == 100:
        status_label.config(text=f"{player_name} wins!")
        roll_button.config(state=tk.DISABLED)
    else:
        # current_player = (current_player + 1) % len(players)
        # status_label.config(text=f"{players[current_player]}'s turn")
        msg = f"{player_name} is now on square {positions[current_player]}"
        if special_msg:
            msg += f" - {special_msg}"
        status_label.config(text=msg)

        current_player = (current_player + 1) % len(players)
# --- Start the UI ---
show_player_setup()
root.mainloop()