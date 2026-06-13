from pywebio import start_server
from pywebio.input import input, NUMBER, actions
from pywebio.output import put_html, clear
from pywebio.session import defer_call
import time
import random

active_rooms = {}

def on_disconnect(room_code):
    if room_code in active_rooms:
        active_rooms[room_code]['left'] = True

def get_move(board, room_code, my_symbol):
    clear()
    put_html(f"<h3 style='text-align:center;'>Room: {room_code} | You: {my_symbol}</h3>")
    put_html("""
    <style>
        .webio-actions form, .webio-btns, div.form-group, form {
            display: grid !important;
            grid-template-columns: repeat(3, 85px) !important;
            justify-content: center !important;
            gap: 5px !important;
            width: max-content !important;
            margin: 20px auto !important;
        }
        button.btn {
            width: 80px !important;
            height: 80px !important;
            margin: 0 !important;
            font-size: 24px !important;
        }
    </style>
    """)
    
    btns = []
    for r in range(3):
        for c in range(3):
            pos = (r * 3) + c + 1
            if board[r][c] == ' ':
                btns.append({'label': ' ', 'value': pos})
            else:
                btns.append({'label': str(board[r][c]), 'value': pos, 'disabled': True})
    
    return actions(buttons=btns)

def show_board_waiting(board, room_code, my_symbol):
    clear()
    put_html(f"<h3 style='text-align:center;'>Room: {room_code} | You: {my_symbol}</h3>")
    put_html("<h4 style='text-align:center; color:grey;'>Waiting for opponent...</h4>")
    
    grid_html = '<div style="display: grid; grid-template-columns: repeat(3, 85px); gap: 5px; justify-content: center; width: max-content; margin: 20px auto;">'
    for r in range(3):
        for c in range(3):
            cell = board[r][c]
            text = str(cell) if cell != ' ' else "&nbsp;"
            grid_html += f'<div style="width: 80px; height: 80px; border: 1px solid black; display: flex; align-items: center; justify-content: center; font-size: 24px;">{text}</div>'
    grid_html += '</div><br>'
    put_html(grid_html)

def check_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ': return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != ' ': return board[0][i]
    
    if board[0][0] == board[1][1] == board[2][2] != ' ': return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ': return board[0][2]
    
    for row in board:
        if ' ' in row: return None
    return 'Draw'

def main():
    clear()
    put_html("<h1 style='text-align:center;'>Tic-Tac-Toe Multiplayer</h1>")
    
    choice = actions(buttons=[{'label': 'HOST GAME', 'value': 1}, {'label': 'JOIN GAME', 'value': 2}])
    
    if choice == 1:
        room_code = str(random.randint(1000, 9999))
        
        host_sym = random.choice(['X', 'O'])
        joiner_sym = 'O' if host_sym == 'X' else 'X'
        
        active_rooms[room_code] = {
            'board': [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']],
            'turn': 'X',
            'player2_joined': False,
            'winner': None,
            'host_symbol': host_sym,
            'joiner_symbol': joiner_sym,
            'play_again_ready': set(),
            'left': False
        }
        my_symbol = host_sym
        
        defer_call(lambda: on_disconnect(room_code))
        
        clear()
        put_html(f"<h2 style='text-align:center;'>Room Code: {room_code}</h2>")
        put_html(f"<h3 style='text-align:center; color:blue;'>You are: {my_symbol}</h3>")
        put_html("<h4 style='text-align:center; color:grey;'>Waiting for player 2...</h4>")
        
        while not active_rooms[room_code]['player2_joined']:
            if active_rooms[room_code]['left']: return
            time.sleep(1)
            
    else:
        room_code = input("Enter 4-digit Room Code:", type=NUMBER)
        room_code = str(room_code)
        
        if room_code in active_rooms and not active_rooms[room_code]['player2_joined']:
            active_rooms[room_code]['player2_joined'] = True
            my_symbol = active_rooms[room_code]['joiner_symbol']
            
            defer_call(lambda: on_disconnect(room_code))
        else:
            clear()
            put_html("<h2 style='color:red; text-align:center;'>Invalid Room!</h2>")
            actions(buttons=[{'label': 'EXIT', 'value': 'exit'}])
            return

    while True:
        if active_rooms[room_code]['left']:
            clear()
            put_html("<h1 style='color:red; text-align:center;'>Opponent left the match!</h1>")
            actions(buttons=[{'label': 'Main Menu', 'value': 'back'}])
            main()
            return

        if my_symbol != active_rooms[room_code]['host_symbol'] and my_symbol != active_rooms[room_code]['joiner_symbol']:
            pass
        else:
            if choice == 1:
                my_symbol = active_rooms[room_code]['host_symbol']
            else:
                my_symbol = active_rooms[room_code]['joiner_symbol']

        winner = active_rooms[room_code]['winner']
        if not winner:
            winner = check_winner(active_rooms[room_code]['board'])
            if winner:
                active_rooms[room_code]['winner'] = winner
                
        if winner:
            show_board_waiting(active_rooms[room_code]['board'], room_code, my_symbol)
            if winner == 'Draw':
                put_html("<h2 style='color:orange; text-align:center;'>MATCH DRAW!</h2>")
            elif winner == my_symbol:
                put_html("<h2 style='color:green; text-align:center;'>YOU WIN!</h2>")
            else:
                put_html("<h2 style='color:red; text-align:center;'>YOU LOSE!</h2>")
            
            end_choice = actions(buttons=[{'label': 'Play Again', 'value': 'again'}, {'label': 'Leave Room', 'value': 'leave'}])
            
            if end_choice == 'leave':
                active_rooms[room_code]['left'] = True
                main()
                return
            else:
                active_rooms[room_code]['play_again_ready'].add(my_symbol)
                clear()
                put_html("<h3 style='text-align:center;'>Waiting for opponent to accept...</h3>")
                
                while len(active_rooms[room_code]['play_again_ready']) < 2:
                    if active_rooms[room_code]['left']:
                        clear()
                        put_html("<h1 style='color:red; text-align:center;'>Opponent left the match!</h1>")
                        actions(buttons=[{'label': 'Main Menu', 'value': 'back'}])
                        main()
                        return
                    time.sleep(1)
                
                if choice == 1:
                    new_host_sym = random.choice(['X', 'O'])
                    new_joiner_sym = 'O' if new_host_sym == 'X' else 'X'
                    
                    active_rooms[room_code]['host_symbol'] = new_host_sym
                    active_rooms[room_code]['joiner_symbol'] = new_joiner_sym
                    active_rooms[room_code]['board'] = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
                    active_rooms[room_code]['winner'] = None
                    active_rooms[room_code]['turn'] = 'X'
                    time.sleep(0.5)
                    active_rooms[room_code]['play_again_ready'].clear()
                else:
                    while active_rooms[room_code]['winner'] is not None:
                        time.sleep(0.2)
                
                continue
            
        if active_rooms[room_code]['turn'] == my_symbol:
            pos = get_move(active_rooms[room_code]['board'], room_code, my_symbol)
            r = (pos - 1) // 3
            c = (pos - 1) % 3
            
            active_rooms[room_code]['board'][r][c] = my_symbol
            active_rooms[room_code]['turn'] = 'O' if my_symbol == 'X' else 'X'
        else:
            show_board_waiting(active_rooms[room_code]['board'], room_code, my_symbol)
            while active_rooms[room_code]['turn'] != my_symbol and active_rooms[room_code]['winner'] is None:
                if active_rooms[room_code]['left']: break
                time.sleep(1)

if __name__ == '__main__':
    start_server(main, port=8080)
