import socket as s
import inou
from pywebio.input import input as pw_input
from pywebio.input import actions
from pywebio.output import clear, put_html

class TicTacToeMultiplayer:
    def __init__(self):
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.moves = 0
        self.player1 = "X"
        self.player2 = "O"

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

    def get_real_ip(self):
        try:
            dummy_socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
            dummy_socket.connect(("8.8.8.8", 80))
            real_ip = dummy_socket.getsockname()[0]
            dummy_socket.close()
            return real_ip
        except Exception:
            return "127.0.0.1"

    def show_waiting(self, msg):
        clear()
        put_html(f"<h2 style='text-align: center;'>{msg}</h2>")
        grid_html = '<div style="display: grid; grid-template-columns: repeat(3, 85px); gap: 5px; justify-content: center; width: max-content; margin: 20px auto;">'
        for r in range(3):
            for c in range(3):
                cell = self.board[r][c]
                text = str(cell) if cell != 0 else "&nbsp;"
                grid_html += f'<div style="width: 80px; height: 80px; border: 1px solid black; display: flex; align-items: center; justify-content: center; font-size: 24px;">{text}</div>'
        grid_html += '</div><br>'
        put_html(grid_html)

    def host_side(self, player2):
        while self.moves < 9:
            pos = inou.choise(self.board)
            self.board[(pos-1)//3][(pos-1)%3] = self.player1
            self.moves += 1

            win = self.check_winner()
            if win or self.moves == 9:
                status = win if win else "DRAW"
                player2.send(f"{pos}|1|{status}".encode("utf-8"))
                if win:
                    inou.show_result(self.board, "CONGRATULATIONS! YOU WIN!")
                else:
                    inou.show_result(self.board, "MATCH DRAW! (Keu jiteni)")
                return
            else:
                player2.send(f"{pos}|0|CONT".encode("utf-8"))

            self.show_waiting("WAITING FOR PLAYER 2 ('O') TO MOVE...")
            client_pos = int(player2.recv(1024).decode('utf-8'))
            self.board[(client_pos-1)//3][(client_pos-1)%3] = self.player2
            self.moves += 1

            win = self.check_winner()
            if win or self.moves == 9:
                status = win if win else "DRAW"
                player2.send(f"ACK|1|{status}".encode("utf-8"))
                if win:
                    inou.show_result(self.board, "PLAYER 2 WINS! YOU LOSE!")
                else:
                    inou.show_result(self.board, "MATCH DRAW! (Keu jiteni)")
                return
            else:
                player2.send(f"ACK|0|CONT".encode("utf-8"))

    def host(self):
        Family = s.AF_INET
        Type = s.SOCK_STREAM 
        server = s.socket(Family, Type)
        
        Ip = "0.0.0.0"
        Port = 5050
        server.bind((Ip, Port))
        server.listen(1)
        
        real_ip = self.get_real_ip()
        clear()
        put_html(f"<h2 style='text-align: center;'>SERVER STARTED!<br><br>SHARE THIS IP: <span style='color: blue;'>{real_ip}</span><br>PORT: {Port}<br><br>WAITING FOR PLAYER 2 TO JOIN...</h2>")

        player2, address = server.accept()

        self.host_side(player2)
        player2.close()  
        server.close()

    def recive_side(self, server):
        while self.moves < 9:
            self.show_waiting("WAITING FOR PLAYER 1 ('X') TO MOVE...")
            data = server.recv(1024).decode("utf-8").split("|")
            host_pos = int(data[0]) if data[0] != "ACK" else None
            flag = data[1]
            status = data[2]

            if host_pos:
                self.board[(host_pos-1)//3][(host_pos-1)%3] = self.player1
                self.moves += 1

            if flag == "1":
                if status == "X":
                    inou.show_result(self.board, "PLAYER 1 WINS! YOU LOSE!")
                else:
                    inou.show_result(self.board, "MATCH DRAW! (Keu jiteni)")
                return

            pos = inou.choise(self.board)
            self.board[(pos-1)//3][(pos-1)%3] = self.player2
            self.moves += 1
            server.send(str(pos).encode("utf-8"))

            data = server.recv(1024).decode("utf-8").split("|")
            flag = data[1]
            status = data[2]

            if flag == "1":
                if status == "O":
                    inou.show_result(self.board, "CONGRATULATIONS! YOU WIN!")
                else:
                    inou.show_result(self.board, "MATCH DRAW! (Keu jiteni)")
                return

    def recive(self):
        clear()
        put_html("<h2 style='text-align: center;'>JOIN A GAME</h2>")
        try:
            Ip = pw_input("ENTER PLAYER 1 IP ADDRESS: ").strip()
            Port = 5050 
            
            Family = s.AF_INET
            Type = s.SOCK_STREAM
            server = s.socket(Family, Type)
            server.connect((Ip, Port))
            
            self.recive_side(server)
            server.close()  
        except Exception as E:
            clear()
            put_html(f"<h2 style='text-align: center; color: red;'>CONNECTION ERROR:<br>{E}</h2>")
            actions(buttons=[{'label': 'Return to Menu', 'value': 'back'}])

def main():
    clear()
    put_html("<h2 style='text-align: center;'>MULTIPLAYER (LAN)</h2>")
    
    ch = actions(buttons=[
        {'label': '1. START A GAME (HOST)', 'value': 1},
        {'label': '2. JOIN A GAME (CLIENT)', 'value': 2},
        {'label': 'RETURN TO MAIN MENU', 'value': 3}
    ])
    
    if ch == 3:
        return
        
    game_servers = TicTacToeMultiplayer()
    if ch == 1:
        game_servers.host()
    elif ch == 2:
        game_servers.recive()

if __name__ == "__main__":
    main()