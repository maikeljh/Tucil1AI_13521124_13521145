# Michael Jonathan Halim 13521124
# Kenneth Dave Bahana 13521145
import tkinter as tk
from tkinter import messagebox

# Tucil 1 AI Application
class XOGame(tk.Tk):
    def __init__(self):
        # Constructor
        super().__init__()

        # Set application configuration
        self.title("XOGame")
        self.geometry("800x550")
        self.configure(bg="#222222")
        self.resizable(False, False)

        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the position for the center of the screen
        window_width = 800
        window_height = 550
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Set the initial position of the application window
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Initialize attributes
        self.board = [["" for _ in range(8)] for _ in range(8)]
        self.player = ""
        self.bot = ""
        self.alpha = float("-inf")
        self.beta = float("inf")

        # Create widgets
        self.create_widgets()

    def set_symbol(self, symbol):
        # Set player symbol
        self.player = symbol

        # Set bot symbol
        if symbol == "O":
            self.bot = "X"
            # Bot plays first
            self.bot_move()
        else:
            self.bot = "O"
            # Player plays first

    def initialize_board(self):
        # Bottom Left Corner
        for i in range(6, 8):
            for j in range(0, 2):
                self.board[i][j] = "X"
                self.buttons[i][j]["text"] = "X"
        
        # Upper Right Corner
        for i in range(0, 2):
            for j in range(6, 8):
                self.board[i][j] = "O"
                self.buttons[i][j]["text"] = "O"

    def choose_symbol(self):
        # Set button disabled when opening popup
        self.play_button.config(state="disabled")

        # Calculate the center coordinates of the main window
        main_window_x = self.winfo_x()
        main_window_y = self.winfo_y()
        main_window_width = self.winfo_width()
        main_window_height = self.winfo_height()
        center_x = main_window_x + main_window_width // 2
        center_y = main_window_y + main_window_height // 2

        # Create popup to choose symbol for player
        popup = tk.Toplevel(self)

        # Set popup configuration
        popup.title("Choose Symbol")
        popup.geometry("300x100")
        popup.configure(bg="#222222")

        # Calculate the position for the center of the popup window
        popup_width = popup.winfo_width()
        popup_height = popup.winfo_height()
        popup_x = center_x - popup_width // 2
        popup_y = center_y - popup_height // 2

        # Set the initial position of the popup window
        popup.geometry(f"+{popup_x - 150}+{popup_y - 100}")

        # Function to enable play button
        def enable_play_button():
            self.play_button.config(state="normal")

        # Bind the destroy event of the popup to enable the symbol button
        popup.bind("<Destroy>", lambda event: enable_play_button())

        # Create function for buttons
        def choose(symbol):
            # Create board
            self.create_board()

            # Create scoreboard
            self.create_score_board()

            # Set symbol
            self.set_symbol(symbol)

            # Initialize board
            self.initialize_board()

            # Destroy popup
            popup.destroy()

            # Set button disabled after choosing symbol
            self.play_button.config(state="disabled")

        # Create buttons for popup
        button_o = tk.Button(popup, text="O", command=lambda: choose("O"), bg="#333333", fg="#FFFFFF")
        button_o.pack(side=tk.LEFT, padx=10, pady=10, anchor="center", expand=True)

        button_x = tk.Button(popup, text="X", command=lambda: choose("X"), bg="#333333", fg="#FFFFFF")
        button_x.pack(side=tk.LEFT, padx=10, pady=10, anchor="center", expand=True)

    def create_widgets(self):
        # Create widgets
        label = tk.Label(self, text="XOGame\n\nby Michael Jonathan Halim | 13521124\n   Kenneth Dave Bahana | 13521145", bg="#222222", fg="#FFFFFF")
        label.grid(row=0, column=0, columnspan=10, pady=10, sticky='n')

        cont = tk.Label(self, text='', bg="#222222", fg="#FFFFFF")
        cont.grid(row=1, column=0, columnspan=10, sticky='n')

        # Create button to play
        self.play_button = tk.Button(self, text="Play", command=self.choose_symbol, bg="#333333", fg="#FFFFFF")
        self.play_button.grid(row=1, column=0, columnspan=10, pady=10)

        # Center widgets
        self.grid_columnconfigure(0, weight=1)

    def create_board(self):
        # Create board display
        # Save buttons to list
        self.buttons = []

        # Create a frame for the board
        self.board_frame = tk.Frame(self)
        self.board_frame.grid(row=2, column=0, columnspan=8, pady=10)

        # Create buttons
        for row in range(8):
            button_row = []
            for col in range(8):
                button = tk.Button(self.board_frame, text="", width=6, height=2,
                                command=lambda r=row, c=col: self.button_click(r, c), bg="#333333", fg="#FFFFFF")
                button.grid(row=row, column=col)
                button_row.append(button)
            self.buttons.append(button_row)

    def create_score_board(self):
        # Create score for player and bot
        self.score_player = tk.StringVar()
        self.score_player.set("Player: 4")
        self.score_bot = tk.StringVar()
        self.score_bot.set("Bot: 4")

        # Create frame for score board
        self.score_frame = tk.Frame(self, bg="#222222")
        self.score_frame.grid(row=3, column=0, pady=10)

        # Create a label for the score and set its textvariable
        self.score_label_player = tk.Label(self.score_frame, textvariable=self.score_player, bg="#333333", fg="#FFFFFF", padx=5, pady=5)
        self.score_label_player.grid(row=0, column=0, padx=(5,10))
        self.score_label_bot = tk.Label(self.score_frame, textvariable=self.score_bot, bg="#333333", fg="#FFFFFF", padx=5, pady=5)
        self.score_label_bot.grid(row=0, column=1)

    def update_score(self):
        # Function to update score player and bot
        score_player = 0
        score_bot = 0

        for row in self.board:
            for col in row:
                if col == self.player:
                    score_player += 1
                elif col == self.bot:
                    score_bot += 1

        # Set new score
        self.score_player.set("Player: " + str(score_player))
        self.score_bot.set("Bot: " + str(score_bot))

    def button_click(self, row, col):
        # Get clicked button
        button = self.buttons[row][col]

        # Check if box valid or not
        if button["text"] == "":
            # Assign box to player
            button["text"] = self.player
            self.board[row][col] = self.player
            
            # Assign 4 adjacent tiles
            self.adjacent(row, col, "Player")

            # Update score
            self.update_score()

            # Check if player wins or not
            if self.check_winner():
                if self.winner == "Player":
                    messagebox.showinfo("Game Over", "Player wins!")
                else:
                    messagebox.showinfo("Game Over", "Bot wins!")
                self.reset_game()
            elif self.check_draw():
                # Check if game draws or not
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_game()
            else:
                # Bot moves
                self.bot_move()

    def assign_winner(self, winner):
        # Assign winner
        self.winner = winner

    def check_winner(self):
        # Check if all boards already filled
        for row in self.board:
            for col in row:
                if col == "":
                    # Game continues
                    return False
        
        # All boards already filled, decide who is the winner
        # Get number
        player_score = int(self.score_player.get().split(":")[1].strip())
        bot_score = int(self.score_bot.get().split(":")[1].strip())

        # Check Draw
        if player_score == bot_score:
            return False

        # Check winner
        if player_score > bot_score:
            self.assign_winner("Player")
        elif player_score < bot_score:
            self.assign_winner("Bot")
        
        return True
    
    def check_draw(self):
        # Check if game draws or not
        for row in self.board:
            for box in row:
                if box == "":
                    # Game continues
                    return False
        
        # No empty box, game draws
        return True

    def objective_function(self):
        # Function to evaluate board state
        score_player = 0
        score_bot = 0

        for row in self.board:
            for col in row:
                if col == self.player:
                    score_player += 1
                elif col == self.bot:
                    score_bot += 1
        
        return score_bot - score_player

    def minimax(self, depth, bot_turn, alpha, beta):
        # Minimax algorithm
        # Evaluate board
        if self.check_winner() or self.check_draw:
            return self.objective_function()

        # Maximizer
        if bot_turn:
            # Set best to negative infinity
            best = float("-inf")

            # Check every possible moves
            for i, row in enumerate(self.board):
                for j, box in enumerate(row):
                    if box == "" and self.check_adjacent(i, j, self.bot):
                        # Assign box to bot
                        self.board[i][j] = self.bot

                        # Assign 4 adjacent tiles
                        changes = self.adjacent(i, j, "Bot")

                        # Update score
                        self.update_score()

                        # Find best value
                        best = max(best, self.minimax(depth + 1, not bot_turn, alpha, beta))

                        # Redo bot's move
                        self.board[i][j] = ""

                        # Redo adjacent
                        if len(changes):
                            for coor in changes:
                                self.board[coor[0]][coor[1]] = self.player
                                self.buttons[coor[0]][coor[1]]["text"] = self.player

                        # Update score
                        self.update_score()

                        # Find Best Alpha
                        alpha = max(alpha, best)

                        # Beta cutoff
                        if alpha >= beta:
                            return best

            # Return best value
            return best
        else:
            # Minimizer

            # Set best to positive infinity
            best = float("inf")

            # Check every possible moves
            for i, row in enumerate(self.board):
                for j, box in enumerate(row):
                    if box == "" and self.check_adjacent(i, j, self.player):
                        # Assign box to player
                        self.board[i][j] = self.player

                        # Assign 4 adjacent tiles
                        changes = self.adjacent(i, j, "Player")

                        # Update score
                        self.update_score()

                        # Find min value
                        best = min(best, self.minimax(depth + 1, not bot_turn, alpha, beta))

                        # Redo player's move
                        self.board[i][j] = ""

                        # Redo adjacent
                        if len(changes):
                            for coor in changes:
                                self.board[coor[0]][coor[1]] = self.bot
                                self.buttons[coor[0]][coor[1]]["text"] = self.bot

                        # Update score
                        self.update_score()

                        # Find Best Beta
                        beta = min(beta, best)

                        # Alpha cutoff
                        if alpha >= beta:
                            return best
            
            # Return best value
            return best

    def check_adjacent(self, row, col, symbol):
        # Under
        if self.border_check(row-1, col) and self.board[row - 1][col] != symbol:
            return True

        # Above
        if self.border_check(row+1, col) and self.board[row + 1][col] != symbol:
            return True

        # Left
        if self.border_check(row, col-1) and self.board[row][col - 1] != symbol:
            return True

        # Right
        if self.border_check(row, col+1) and self.board[row][col + 1] != symbol:
            return True

        return False

    def bot_move(self):
        # Bot's turn

        # Initialize bot variables
        best_value = float("-inf")
        best_move = (-1, -1)

        # Find best move for bot
        for i, row in enumerate(self.board):
            for j, box in enumerate(row):
                if box == "" and self.check_adjacent(i, j, self.bot):
                    # Assign box to bot
                    self.board[i][j] = self.bot

                    # Assign 4 adjacent tiles
                    changes = self.adjacent(i, j, "Bot")

                    # Update score
                    self.update_score()

                    # Reset alpha and beta
                    self.alpha = float("-inf")
                    self.beta = float("inf")

                    # Calculate move value
                    move_value = self.minimax(0, False, self.alpha, self.beta)

                    # Redo bot's move
                    self.board[i][j] = ""

                    # Redo adjacent
                    if len(changes):
                        for coor in changes:
                            self.board[coor[0]][coor[1]] = self.player
                            self.buttons[coor[0]][coor[1]]["text"] = self.player

                    # Update score
                    self.update_score()

                    # Save best move
                    if move_value > best_value:
                        best_move = (i, j)
                        best_value = move_value
        
        # Bot move
        self.board[best_move[0]][best_move[1]] = self.bot
        button = self.buttons[best_move[0]][best_move[1]]
        button["text"] = self.bot
        
        # Assign 4 adjacent tiles
        self.adjacent(best_move[0], best_move[1], "Bot")

        # Update score
        self.update_score()
        
        # Check winner or draw
        if self.check_winner():
            if self.winner == "Player":
                messagebox.showinfo("Game Over", "Player wins!")
            else:
                messagebox.showinfo("Game Over", "Bot wins!")
            self.reset_game()
        elif self.check_draw():
            messagebox.showinfo("Game Over", "It's a draw!")
            self.reset_game()

    def border_check(self, row, col):
        if row >= 0 and row < 8 and col >= 0 and col < 8:
            return True
        else:
            return False

    def adjacent(self, row, col, role):
        # Function to replace adjacent enemy symbols
        # Checking if adjacent tiles are out of the map
        changes = []

        # Checking 4 adjacent tiles (Under, Above, Left, Right)
        # For Player
        if role == "Player":
            # Under
            if self.border_check(row-1, col):
                button = self.buttons[row-1][col]
                if button["text"] == self.bot:
                    button["text"] = self.player
                    self.board[row-1][col] = self.player
                    changes.append((row-1, col))

            # Above
            if self.border_check(row+1, col):
                button = self.buttons[row+1][col]
                if button["text"] == self.bot:
                    button["text"] = self.player
                    self.board[row+1][col] = self.player
                    changes.append((row+1, col))
            
            # Left
            if self.border_check(row, col-1):
                button = self.buttons[row][col-1]
                if button["text"] == self.bot:
                    button["text"] = self.player
                    self.board[row][col-1] = self.player
                    changes.append((row, col-1))

            # Right
            if self.border_check(row, col+1):
                button = self.buttons[row][col+1]
                if button["text"] == self.bot:
                    button["text"] = self.player
                    self.board[row][col+1] = self.player
                    changes.append((row, col+1))
        else:
            # For Bot
            # Under
            if self.border_check(row-1, col):
                button = self.buttons[row-1][col]
                if button["text"] == self.player:
                    button["text"] = self.bot
                    self.board[row-1][col] = self.bot
                    changes.append((row-1, col))
                    
            # Above
            if self.border_check(row+1, col):
                button = self.buttons[row+1][col]
                if button["text"] == self.player:
                    button["text"] = self.bot
                    self.board[row+1][col] = self.bot
                    changes.append((row+1, col))
            
            # Left
            if self.border_check(row, col-1):
                button = self.buttons[row][col-1]
                if button["text"] == self.player:
                    button["text"] = self.bot
                    self.board[row][col-1] = self.bot
                    changes.append((row, col-1))
                    
            # Right
            if self.border_check(row, col+1):
                button = self.buttons[row][col+1]
                if button["text"] == self.player:
                    button["text"] = self.bot
                    self.board[row][col+1] = self.bot
                    changes.append((row, col+1))

        return changes

    def reset_game(self):
        # Reset board
        self.board = [["" for _ in range(8)] for _ in range(8)]

        # Enable play button
        self.play_button.config(state="normal")

        # Reset attributes
        self.player = ""
        self.bot = ""
        self.winner = ""
        self.alpha = float("-inf")
        self.beta = float("inf")
        
        # Destroy board
        for button_row in self.buttons:
            for button in button_row:
                button.destroy()

        # Destory widgets
        self.board_frame.destroy()
        self.score_label_player.destroy()
        self.score_label_bot.destroy()

        # Reset buttons
        self.buttons = []

# Run application
if __name__ == "__main__":
    app = XOGame()
    app.mainloop()