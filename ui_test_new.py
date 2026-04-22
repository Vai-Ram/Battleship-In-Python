import tkinter as tk
import tkmacosx
import random
from classPlayer_template import Player
from classAIOpponent_template import AIOpponent
from classBoard_template import *
from classShip_template import Ship


class ToolTip:
    """A simple tooltip implementation for Tkinter."""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip_window or not self.text:
            return
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + 25
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left',
                         background="#ffffe0", fg = 'black', relief='solid', borderwidth=1,
                         font=("tahoma", 8, "normal"))
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

class BattleshipApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Battleship vs AI")
        self.root.minsize(1000, 650)
        self.root.configure(bg="#f4f6f9")

        # Game State
        self.difficulty = tk.StringVar(value="Medium")
        self.selected_ship = tk.StringVar(value="Carrier (5)")
        self.orientation = tk.StringVar(value="Horizontal")
        
        self.player_buttons = {}
        self.target_buttons = {}
        self.ship_radio_btns = {}
        
        # Ship Data: Name -> Length
        self.ships_info = {
            "Carrier (5)": 5,
            "Battleship (4)": 4,
            "Cruiser (3)": 3,
            "Sub (3)": 3,
            "Destroyer (2)": 2
        }

        # Initialising objects

        self.human_player = Player("You, dumbass")
        self.AI_opp = AIOpponent()
        # self.human_board = Board()
        # self.AI_board = Board()

        # Tracking placed ships
        self.placed_ships = {}      # Format: {ship_name: [(r,c), (r,c)...]}
        self.board_cells = {}       # Format: {(r,c): ship_name}
        self.ship_tooltips = {}     # Keep track of tooltips to update/remove them
        self.selected_for_deletion = None

        # Container for screens
        self.main_container = tk.Frame(self.root, bg="#f4f6f9")
        self.main_container.pack(expand=True, fill="both")

        self.show_main_menu()
        self.player=None
        self.comp =None
        self.playerturn=True

    def clear_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    # --- Screen 1: Main Menu ---
    def show_main_menu(self):
        self.clear_container()
        
        menu_frame = tk.Frame(self.main_container, bg="#f4f6f9")
        menu_frame.place(relx=0.5, rely=0.4, anchor="center")

        # Minecraft style title (Big, Bold, Arial, Red)
        title_label = tk.Label(menu_frame, text="BATTLESHIP", font=("Arial", 64, "bold"), fg="#c0392b", bg="#f4f6f9")
        title_label.pack(pady=(0, 50))

        play_btn = tkmacosx.Button(menu_frame, text="Play", font=("Helvetica", 16, "bold"), width=300, 
                             bg="#3498db", fg="white", relief="groove", command=self.show_difficulty_menu)
        play_btn.pack(pady=10)

        # settings_btn = tkmacosx.Button(menu_frame, text="Settings", font=("Helvetica", 16, "bold"), width=15, 
        #                          bg="#7f8c8d", fg="white", relief="groove")
        # settings_btn.pack(pady=10)

    # --- Screen 2: Difficulty Selection ---
    def show_difficulty_menu(self):
        self.clear_container()
        
        diff_frame = tk.Frame(self.main_container, bg="#f4f6f9")
        diff_frame.place(relx=0.5, rely=0.4, anchor="center")

        tk.Label(diff_frame, text="Select Difficulty", font=("Arial", 32, "bold"), fg="#2c3e50", bg="#f4f6f9").pack(pady=(0, 40))

        colors = {"Easy": "#2ecc71", "Medium": "#f1c40f", "Hard": "#e74c3c", "Madhav": "#8f00be"}
        for level in ["Easy", "Medium", "Hard","Madhav"]:
            btn = tkmacosx.Button(diff_frame, text=level, font=("Helvetica", 14, "bold"), width=400,
                            bg=colors[level], fg="black" if level == "Medium" else "white", relief="groove",
                            command=lambda l=level: self.start_game_setup(l))
            btn.pack(pady=10)

    # --- Screen 3: Game Board & Placement ---
    def start_game_setup(self, difficulty_level):
        self.difficulty.set(difficulty_level)
        self.clear_container()
        self.setup_game_ui()

    def setup_game_ui(self):
        # 1. Top Status Frame (No difficulty selection here as requested)
        self.top_frame = tk.Frame(self.main_container, bg="#ffffff", bd=1, relief="solid")
        self.top_frame.pack(fill="x", padx=20, pady=15)
        
        self.status_label = tk.Label(self.top_frame, text="Status: Deploy your fleet. Click empty cells to place, click placed ships to select.", 
                                     font=("Helvetica", 12, "bold"), fg="#2c3e50", bg="#ffffff")
        self.status_label.pack(pady=10)

        # 2. Boards Frame
        self.boards_frame = tk.Frame(self.main_container, bg="#f4f6f9")
        self.boards_frame.pack(expand=True, pady=10)

        # Player Board
        left_frame = tk.Frame(self.boards_frame, bg="#f4f6f9")
        left_frame.grid(row=0, column=0, padx=40)
        tk.Label(left_frame, text="YOUR OCEAN", font=("Helvetica", 14, "bold"), fg="#2980b9", bg="#f4f6f9").pack(pady=(0, 10))
        self.build_grid(left_frame, self.player_buttons, is_player=True)

        # Opponent Board
        right_frame = tk.Frame(self.boards_frame, bg="#f4f6f9")
        right_frame.grid(row=0, column=1, padx=40)
        tk.Label(right_frame, text="TARGET RADAR", font=("Helvetica", 14, "bold"), fg="#c0392b", bg="#f4f6f9").pack(pady=(0, 10))
        self.build_grid(right_frame, self.target_buttons, is_player=False)

        # 3. Setup Controls (Bottom Frame)
        self.bottom_frame = tk.Frame(self.main_container, bg="#ffffff", bd=1, relief="solid")
        self.bottom_frame.pack(fill="x", side="bottom", padx=20, pady=20)
        
        # Change button (Bottom Left)
        self.change_btn = tkmacosx.Button(self.bottom_frame, text="Change (Delete Ship)", font=("Helvetica", 10, "bold"),
                                    bg="#e74c3c", fg="white", state="disabled", command=self.delete_selected_ship)
        self.change_btn.pack(side="left", padx=20, pady=15)

        # Container to center the selection elements
        center_bottom = tk.Frame(self.bottom_frame, bg="#ffffff")
        center_bottom.pack(side="left", expand=True)

        tk.Label(center_bottom, fg="#2c3e50", text="Select Ship:", font=("Helvetica", 12, "bold"), bg="#ffffff").grid(row=0, column=0, padx=10)
        
        ship_frame = tk.Frame(center_bottom, bg="#ffffff")
        ship_frame.grid(row=0, column=1, padx=10)
        
        for ship in self.ships_info.keys():
            rb = tk.Radiobutton(ship_frame, text=ship, variable=self.selected_ship, value=ship, 
                                font=("Helvetica", 10), bg="#ffffff", fg="#2c3e50", selectcolor="#ffffff", command=self.clear_delete_selection)
            rb.pack(side="left")
            self.ship_radio_btns[ship] = rb

        tk.Label(center_bottom, text=" | ", font=("Helvetica", 16), bg="#ffffff", fg="#2c3e50").grid(row=0, column=2, padx=5)
        
        self.orient_btn = tkmacosx.Button(center_bottom, textvariable=self.orientation, width=100, font=("Helvetica", 10, "bold"),
                                    bg="#ecf0f1", relief="groove", command=self.toggle_orientation)
        self.orient_btn.grid(row=0, column=3, padx=10)

        # Start button (Bottom Right)
        self.start_btn = tkmacosx.Button(self.bottom_frame, text="START GAME", width=200, font=("Helvetica", 11, "bold"),
                                   bg="#2ecc71", fg="black", relief="groove", state="disabled", command=self.on_start_game)
        self.start_btn.pack(side="right", padx=20, pady=15)

    def build_grid(self, parent_frame, button_dict, is_player):
        letters = "ABCDEFGHIJ"
        grid_container = tk.Frame(parent_frame, bg="#bdc3c7", padx=2, pady=2) 
        grid_container.pack()
        
        base_color = "#d6eaf8" if is_player else "#e5e7e9"
        
        for col in range(10):
            tk.Label(grid_container, text=str(col + 1), font=("Helvetica", 9, "bold"), bg="#bdc3c7").grid(row=0, column=col+1)
        for row in range(10):
            tk.Label(grid_container, text=letters[row], font=("Helvetica", 9, "bold"), bg="#bdc3c7").grid(row=row+1, column=0)
            for col in range(10):
                btn = tkmacosx.Button(grid_container, width = 40, height=40, bg=base_color, relief="flat")
                if is_player:
                    btn.config(command=lambda r=row, c=col: self.on_player_grid_clicked(r, c))
                else:
                    btn.config(state="disabled", command=lambda r=row, c=col: self.on_target_grid_clicked(r, c))
                btn.grid(row=row+1, column=col+1, padx=1, pady=1, sticky='nsew')
                button_dict[(row, col)] = btn

    # --- Game Logic: Placement Phase ---

    def toggle_orientation(self):
        current = self.orientation.get()
        self.orientation.set("Vertical" if current == "Horizontal" else "Horizontal")

    def clear_delete_selection(self):
        # Un-highlight the previously selected ship for deletion
        if self.selected_for_deletion:
            for (r, c) in self.placed_ships[self.selected_for_deletion]:
                self.player_buttons[(r, c)].config(bg="red")
            self.selected_for_deletion = None
            self.change_btn.config(state="disabled")

    def on_player_grid_clicked(self, row, col):
        # 1. Check if user clicked an existing ship (Select for deletion)
        if (row, col) in self.board_cells:
            self.clear_delete_selection()
            clicked_ship = self.board_cells[(row, col)]
            self.selected_for_deletion = clicked_ship
            
            # Highlight chosen ship to indicate it can be deleted
            for (r, c) in self.placed_ships[clicked_ship]:
                self.player_buttons[(r, c)].config(bg="#e67e22") # Orange selection
            
            self.change_btn.config(state="normal")
            self.status_label.config(text=f"Selected {clicked_ship}. Click 'Change' to remove it.")
            return

        # 2. Otherwise, attempt to place the currently selected ship
        ship_name = self.selected_ship.get()
        if ship_name in self.placed_ships:
            self.status_label.config(text=f"{ship_name} is already placed!")
            return

        length = self.ships_info[ship_name]
        orient = self.orientation.get()
        coords_to_place = []

        # Calculate coordinates
        for i in range(length):
            r = row + (i if orient == "Vertical" else 0)
            c = col + (i if orient == "Horizontal" else 0)
            if r > 9 or c > 9 or (r, c) in self.board_cells:
                self.status_label.config(text="Invalid placement! Ship goes out of bounds or overlaps.")
                return
            coords_to_place.append((r, c))

        

        # Placing the ship in the backend
        if orient == "Vertical":
            rep = 'V'
        else:
            rep = "H"

        ship_obj = Ship(ship_name, self.ships_info.get(ship_name))

        self.human_player.board.place_ship(ship_obj, row, col, rep)

        # Place the ship in the front end
        self.placed_ships[ship_name] = coords_to_place


        for (r, c) in coords_to_place:
            self.board_cells[(r, c)] = ship_name
            btn = self.player_buttons[(r, c)]
            btn.config(bg="red")
            # Bind tooltip
            self.ship_tooltips[(r, c)] = ToolTip(btn, ship_name)

        # Disable the radio button for this ship
        self.ship_radio_btns[ship_name].config(state="disabled")
        self.clear_delete_selection()
        
        # Check if all ships placed
        if len(self.placed_ships) == len(self.ships_info):
            self.start_btn.config(state="normal")
            self.status_label.config(text="All ships placed! You can now Start Game.")
        else:
            self.status_label.config(text=f"Placed {ship_name}. Select next ship.")
            # Auto-select the next available ship
            for s in self.ships_info.keys():
                if s not in self.placed_ships:
                    self.selected_ship.set(s)
                    break

    def delete_selected_ship(self):
        if not self.selected_for_deletion: return
        ship_name = self.selected_for_deletion
        
        # Remove from memory
        self.human_player.board.delete_ship(ship_name)

        # Remove from board
        for (r, c) in self.placed_ships[ship_name]:
            btn = self.player_buttons[(r, c)]
            btn.config(bg="#d6eaf8") # Reset to water color
            del self.board_cells[(r, c)]
            # Remove Tooltip
            if (r, c) in self.ship_tooltips:
                self.ship_tooltips[(r, c)].hide_tooltip()
                # Unbind events safely
                btn.unbind("<Enter>")
                btn.unbind("<Leave>")
                del self.ship_tooltips[(r, c)]

        del self.placed_ships[ship_name]
        
        # Reset UI controls
        self.ship_radio_btns[ship_name].config(state="normal")
        self.selected_ship.set(ship_name)
        self.selected_for_deletion = None
        self.change_btn.config(state="disabled")
        self.start_btn.config(state="disabled")
        self.status_label.config(text=f"Removed {ship_name}.")

    # --- Game Logic: Combat Phase ---

    def on_start_game(self):

        self.AI_opp.random_place_ships()
        # Disable own board clicks
        for btn in self.player_buttons.values():
            btn.config(command=lambda: None) 
        
        # Enable target board clicks
        for btn in self.target_buttons.values():
            btn.config(state="normal")
            
        # Hide the setup bars entirely
        self.top_frame.pack_forget()
        self.bottom_frame.pack_forget()
        self.battle_status = tk.Label(self.main_container, text="Your Turn! Fire at the Radar.", 
                                  font=("Helvetica", 14, "bold"), bg="#f4f6f9", fg="#2c3e50")
        self.battle_status.pack(pady=10)

    def on_target_grid_clicked(self, row, col):
        if not self.playerturn:
            return

        result = self.AI_opp.board.receive_attack(row,col)

        self.human_player.shots_fired.add((row,col))

        btn = self.target_buttons[(row, col)]
        btn.config(bg="#34495e", state="disabled") # Miss effect as placeholder

        if result in ("HIT", "SUNK"):
            btn.config(bg="#e74c3c", text="X", fg="white")
            if result=="SUNK":
                self.battle_status.config(text=f"You sunk an enemy the ship")
        else:
            btn.config(bg="#34495e", text="O", fg= "white")
        
        if self.AI_opp.board.all_ships_sunk():
            self.battle_status.config(text="YOU WIN", font=("Helvetica", 20, "bold"), fg="#c0392b")

            # for btn in self.target_buttons.values():
            #     btn.config(state="disabled")
            self.show_play_again()
            return
        
        self.playerturn=False
        if result=="SUNK":
            self.root.after(800, lambda: self.battle_status.config(text="Computer is calculating"))
            self.root.after(1600, self.ai_turn)
        else:
            self.battle_status.config(text="Computer is calculating")
            self.root.after(800, self.ai_turn)

    def ai_turn(self):

        if self.difficulty.get() == "Medium":
            result=self.AI_opp.attack(self.human_player.board)  
        elif self.difficulty.get() == "Hard":
            result=self.AI_opp.hm_attack(self.human_player.board)
        elif self.difficulty.get() == "Easy":
            result=self.AI_opp.easy_attack(self.human_player.board)
        elif self.difficulty.get() == "Madhav":
            result=self.AI_opp.impossible(self.human_player.board)    

        for (r,c), btn in self.player_buttons.items():
            cell_value= self.human_player.board.grid[r][c]
            if cell_value=="X":
                btn.config(bg="#8e44ad", text="X", fg="white")
            elif cell_value == "O":
                btn.config(bg="#2980b9", text="O", fg="white")
        if self.human_player.board.all_ships_sunk():
            self.battle_status.config(text="AI has WON", font=("Helvetica", 20, "bold"), fg="#c0392b")

            # for btn in self.target_buttons.values():
            #     btn.config(state="disabled")

            # for btn in self.player_buttons.values():
            #     btn.config(state="disabled")

            self.show_play_again()
            return
        
        self.playerturn=True
        self.battle_status.config(text="Your Turn!")

    def show_play_again(self):

        self.play_again_btn = tk.Button(
            self.main_container,
            text="Play Again",
            font=("Helvetica", 14, "bold"),
            bg="#2ecc71",
            fg="black",
            command=self.reset_and_restart
        )
        self.play_again_btn.pack(pady=20)

    def reset_and_restart(self):
    # Reset backend state
        self.human_player = Player("You, dumbass")
        self.AI_opp = AIOpponent()

        self.placed_ships.clear()
        self.board_cells.clear()
        self.ship_tooltips.clear()
        self.selected_for_deletion = None

        self.player_buttons.clear()
        self.target_buttons.clear()
        self.ship_radio_btns.clear()

        self.playerturn = True

        # Go back to main menu
        self.show_main_menu()

if __name__ == "__main__":
    root = tk.Tk()
    app = BattleshipApp(root)
    root.mainloop()