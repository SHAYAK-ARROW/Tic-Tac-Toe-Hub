import random
import inou

board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
x = 0
compu = "O"
user = "X"

def check_winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != 0:
            return board[i][0]
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != 0:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != 0:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != 0:
        return board[0][2]
    return None

def main_func():
    global x
    empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        board[r][c] = compu
        x += 1

def reset_game():
    global board, x
    board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    x = 0
def main():
    global x
    reset_game()
    
    while x < 9:
        pos = inou.choise(board)
        
        r = (pos - 1) // 3
        c = (pos - 1) % 3
        board[r][c] = user
        x += 1
        
        winner = check_winner()
        if winner:
            if winner == user:
                inou.show_result(board, "CONGRATULATIONS! YOU WIN!")
            else:
                inou.show_result(board, "BOT WINS! YOU LOSE!")
            return
            
        if x >= 9:
            inou.show_result(board, "MATCH DRAW! (Keu Jiteni)")
            return
            
        main_func()  
        
        winner = check_winner()
        if winner:
            if winner == compu:
                inou.show_result(board, "BOT WINS! YOU LOSE! (Compu Jitechhe!)")
            else:
                inou.show_result(board, "CONGRATULATIONS! YOU WIN!")
            return

        if not check_winner() and x >= 9:
            inou.show_result(board, "MATCH DRAW! (Keu Jiteni)")
            return