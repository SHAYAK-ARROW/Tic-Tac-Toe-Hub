import random
import inou

class TicTacToe:
    def __init__(self):
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.x = 0
        self.compu = "O"
        self.user = "X"

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != 0:
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != 0:
                return self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
            return self.board[0][2]
        return None

    def minimax(self, is_maximizing):
        winner = self.check_winner()
        if winner == self.compu:
            return 10
        if winner == self.user:
            return -10

        is_full = True
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == 0:
                    is_full = False
        if is_full == True:
            return 0

        if is_maximizing == True:
            best_score = -100
            for r in range(3):
                for c in range(3):
                    if self.board[r][c] == 0:
                        self.board[r][c] = self.compu
                        score = self.minimax(False)
                        self.board[r][c] = 0
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = 100
            for r in range(3):
                for c in range(3):
                    if self.board[r][c] == 0:
                        self.board[r][c] = self.user
                        score = self.minimax(True)
                        self.board[r][c] = 0
                        best_score = min(score, best_score)
            return best_score

    def compu_move(self):
        best_score = -100
        best_r = None
        best_c = None
        
        if self.x == 0:
            best_r = random.randint(0, 2)
            best_c = random.randint(0, 2)
        else:
            for r in range(3):
                for c in range(3):
                    if self.board[r][c] == 0:
                        self.board[r][c] = self.compu
                        score = self.minimax(False)
                        self.board[r][c] = 0
                        
                        if score > best_score:
                            best_score = score
                            best_r = r
                            best_c = c
        
        if best_r != None and best_c != None:
            self.board[best_r][best_c] = self.compu
            self.x += 1

    def play(self):
        while self.x < 9:
            pos = inou.choise(self.board)
            
            r = (pos - 1) // 3
            c = (pos - 1) % 3
            self.board[r][c] = self.user
            self.x += 1
            
            winner = self.check_winner()
            if winner:
                if winner == self.user:
                    inou.show_result(self.board, "CONGRATULATIONS! YOU WIN!")
                return
            
            if self.x >= 9:
                inou.show_result(self.board, "MATCH DRAW! (Keu jiteni)")
                return
            
            self.compu_move()  
            
            winner = self.check_winner()
            if winner:
                if winner == self.compu:
                    inou.show_result(self.board, "BOT WINS! YOU LOSE!  (Compu Jitechhe!)")
                return

        if not self.check_winner() and self.x >= 9:
            inou.show_result(self.board, "MATCH DRAW! (Keu jiteni)")
            return