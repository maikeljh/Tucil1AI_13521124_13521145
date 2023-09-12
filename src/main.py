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
        self.geometry("800x600")
        self.configure(bg="#222222")
        self.resizable(False, False)

        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the position for the center of the screen
        window_width = 800
        window_height = 600
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Set the initial position of the application window
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Initialize attributes
        self.board = [["" for _ in range(3)] for _ in range(3)]
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
        board_frame = tk.Frame(self)
        board_frame.grid(row=2, column=0, columnspan=8, pady=10)

        # Create buttons
        for row in range(8):
            button_row = []
            for col in range(8):
                button = tk.Button(board_frame, text="", width=6, height=2,
                                command=lambda r=row, c=col: self.button_click(r, c), bg="#333333", fg="#FFFFFF")
                button.grid(row=row, column=col)
                button_row.append(button)
            self.buttons.append(button_row)

    def create_score_board(self):
        # Create score for player and bot
        self.score_player = tk.StringVar()
        self.score_player.set("Player: 0")
        self.score_bot = tk.StringVar()
        self.score_bot.set("Bot: 0")

        # Create frame for score board
        score_frame = tk.Frame(self, bg="#222222")
        score_frame.grid(row=3, column=0, pady=10)

        # Create a label for the score and set its textvariable
        self.score_label_player = tk.Label(score_frame, textvariable=self.score_player, bg="#333333", fg="#FFFFFF", padx=5, pady=5)
        self.score_label_player.grid(row=0, column=0, padx=(5,10))

        self.score_label_bot = tk.Label(score_frame, textvariable=self.score_bot, bg="#333333", fg="#FFFFFF", padx=5, pady=5)
        self.score_label_bot.grid(row=0, column=1)

    def button_click(self, row, col):
        # Get clicked button
        button = self.buttons[row][col]

        # Check if box valid or not
        if button["text"] == "":
            # Assign box to player
            button["text"] = self.player
            self.board[row][col] = self.player
            
            # Assign 4 adjacent tiles
            self.adjacent(row, col)

            # Check if player wins or not
            if self.check_winner():
                messagebox.showinfo("Game Over", "Player wins!")
                self.reset_game()
            elif self.check_draw():
                # Check if game draws or not
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_game()
            else:
                # Bot moves
                self.bot_move()

    def assign_winner(self, symbol):
        # Assign winner
        if symbol == self.player:
            self.winner = "Player"
        else:
            self.winner = "Bot"

    def check_winner(self):
        # Check for rows
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] != "":
                # Assign winner
                self.assign_winner(row[0])
                return True
        
        # Check for cols
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != "":
                # Assign winner
                self.assign_winner(self.board[0][col])
                return True
        
        # Check for diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != "":
            # Assign winner
            self.assign_winner(self.board[1][1])
            return True
        elif self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != "":
            # Assign winner
            self.assign_winner(self.board[1][1])
            return True
        
        # No winner
        return False
    
    def check_draw(self):
        # Check if game draws or not
        for row in self.board:
            for box in row:
                if box == "":
                    # Game still ongoing
                    return False
        
        # No empty box, game draws
        return True

    def minimax(self, depth, bot_turn, alpha, beta):
        # Minimax algorithm

        # Evaluate board
        if self.check_winner():
            # If player wins
            if self.winner == "Player":
                return -10
            else:
                # If bot wins
                return 10
        
        if self.check_draw():
            # If game draws
            return 0
        
        # Maximizer
        if bot_turn:
            # Set best to negative infinity
            best = float("-inf")

            # Check every possible moves
            for i, row in enumerate(self.board):
                for j, box in enumerate(row):
                    if box == "":
                        # Assign box to bot
                        self.board[i][j] = self.bot

                        # Find best value
                        best = max(best, self.minimax(depth + 1, not bot_turn, alpha, beta))

                        # Redo bot's move
                        self.board[i][j] = ""

                        # Find Best Alpha
                        alpha = max(alpha, best)

                        # Beta cutoff
                        if alpha > beta:
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
                    if box == "":
                        # Assign box to player
                        self.board[i][j] = self.player

                        # Find min value
                        best = min(best, self.minimax(depth + 1, not bot_turn, alpha, beta))

                        # Redo player's move
                        self.board[i][j] = ""

                        # Find Best Beta
                        beta = min(beta, best)

                        # Alpha cutoff
                        if alpha > beta:
                            return best
            
            # Return best value
            return best

    def bot_move(self):
        # Bot's turn

        # Initialize bot variables
        best_value = float("-inf")
        best_move = (-1, -1)

        # Find best move for bot
        for i, row in enumerate(self.board):
            for j, box in enumerate(row):
                if box == "":
                    # Assign box to bot
                    self.board[i][j] = self.bot

                    # Reset alpha and beta
                    self.alpha = float("-inf")
                    self.beta = float("inf")

                    # Calculate move value
                    move_value = self.minimax(0, False, self.alpha, self.beta)

                    # Redo bot's move
                    self.board[i][j] = ""

                    # Save best move
                    if move_value > best_value:
                        best_move = (i, j)
                        best_value = move_value
        
        # Bot move
        self.board[best_move[0]][best_move[1]] = self.bot
        button = self.buttons[best_move[0]][best_move[1]]
        button["text"] = self.bot

        # Check winner or draw
        if self.check_winner():
            messagebox.showinfo("Game Over", "Bot wins!")
            self.reset_game()
        elif self.check_draw():
            messagebox.showinfo("Game Over", "It's a draw!")
            self.reset_game()
### Algo gw
    def adjacent(self, row, col):
        # Checking if adjacent tiles are out of the map
        def Border_check(row, col):
            if row > 9 | row < 2 | col > 8 | col < 1:
                return True
            else:
                return False
        # Checking 4 adjacent tiles
        #  Under
        if Border_check(row-1, col):
            button = self.button[row-1][col]
            if button["text"] == self.bot:
                # Replace if tile was owned by the bot with the player
                button["text"] = self.player
                self.board[row-1][col] = self.player
                
        # Above
        if Border_check(row+1, col):
            button = self.button[row+1][col]
            if button["text"] == self.bot:
                # Replace if tile was owned by the bot with the player
                button["text"] = self.player
                self.board[row+1][col] = self.player
        
        # Left
        if Border_check(row, col-1):
            button = self.button[row][col-1]
            if button["text"] == self.bot:
                # Replace if tile was owned by the bot with the player
                button["text"] = self.player
                self.board[row][col-1] = self.player
                
        # Right
        if Border_check(row, col+1):
            button = self.button[row][col+1]
            if button["text"] == self.bot:
                # Replace if tile was owned by the bot with the player
                button["text"] = self.player
                self.board[row][col+1] = self.player

    def reset_game(self):
        # Reset board
        self.board = [["" for _ in range(3)] for _ in range(3)]

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
        
        # Reset buttons
        self.buttons = []

# Run application
if __name__ == "__main__":
    app = XOGame()
    app.mainloop()