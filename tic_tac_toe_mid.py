import random
import inou

board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
table = board
x = 0
compu = "O"
user = "X"

def index_cheek(r, c, mark, count=0):
    if r > 2 or c > 2:
        return count, mark, None, None
    else:
        if r < 3 and c < 3:
            if board[r][c] == mark:
                count += 1
                if count == 3:
                    return "win", mark, None, None
                return index_cheek(r + 1, c + 1, mark, count)
            elif board[r][c] == 0:
                res = index_cheek(r + 1, c + 1, mark, 0)
                c1 = res[0]
                if c1 + count >= 2:
                    return 2, mark, r, c
                else:
                    return index_cheek(r + 1, c + 1, mark, 0)
            elif board[r][c] != mark:
                return 0, mark, None, None
    return 0, mark, None, None

def index_cheek_horizontal(r, c, mark, count=0):
    if c > 2:  
        return count, mark, None, None
    if board[r][c] == mark:
        count += 1
        if count == 3:
            return "win", mark, None, None
        return index_cheek_horizontal(r, c + 1, mark, count)  
    elif board[r][c] == 0:
        res = index_cheek_horizontal(r, c + 1, mark, 0)
        c1 = res[0]
        if c1 + count >= 2:
            return 2, mark, r, c  
        else:
            return index_cheek_horizontal(r, c + 1, mark, 0)
    return 0, mark, None, None

def index_cheek_vertical(r, c, mark, count=0):
    if r > 2:  
        return count, mark, None, None
    if board[r][c] == mark:
        count += 1
        if count == 3:
            return "win", mark, None, None
        return index_cheek_vertical(r + 1, c, mark, count)  
    elif board[r][c] == 0:
        res = index_cheek_vertical(r + 1, c, mark, 0)
        c1 = res[0]
        if c1 + count >= 2:
            return 2, mark, r, c  
        else:
            return index_cheek_vertical(r + 1, c, mark, 0)
    return 0, mark, None, None

def disision(count, mark, r, c, compu, user):
    if count == 2 and r is not None:
        if table[r][c] == 0:
            return compu, r, c
    if table[1][1] == 0:
        return compu, 1, 1
    while True:
        g = random.randint(0, 2)
        h = random.randint(0, 2)
        if table[g][h] == 0:
            return compu, g, h

def check_winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != 0:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != 0:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != 0:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != 0:
        return board[0][2]
    return None

def main_func():
    global x
    move_made = False
    targets = [index_cheek_horizontal, index_cheek_vertical, index_cheek]
    
    for func in targets:
        for r in range(3):
            for c in range(3):
                if x < 9:
                    count, mk, r1, c1 = func(r, c, compu)
                    if count == 2 and r1 is not None and board[r1][c1] == 0:
                        board[r1][c1] = compu
                        x += 1
                        move_made = True
                        break
            if move_made: break
        if move_made: break

    if not move_made:
        for func in targets:
            for r in range(3):
                for c in range(3):
                    if x < 9:
                        count, mk, r1, c1 = func(r, c, user)
                        if count == 2 and r1 is not None and board[r1][c1] == 0:
                            board[r1][c1] = compu
                            x += 1
                            move_made = True
                            break
                if move_made: break
            if move_made: break

    if not move_made and x < 9:
        insert, g, h = disision(0, None, None, None, compu, user)
        if board[g][h] == 0:
            board[g][h] = insert
            x += 1
            move_made = True

def reset_game():
    global board, table, x
    board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    table = board
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