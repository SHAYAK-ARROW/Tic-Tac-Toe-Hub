import tic_tac_toe_hard as hard_bot
import tic_tac_toe_mid as mid_bot
import tic_tac_toe_easy as easy_bot
import tic_tac_toe_multty as player
import os
from pywebio.input import actions
from pywebio.output import put_html, clear
from pywebio import start_server
from pywebio.session import set_env

def main():
    while True:
        clear()
        set_env(title=" TIC TAC TOE ")
        put_html("<h1>PROJECT BY SHAYAK </h1>")
        put_html("""
        <h1>
            <br><br> 
            <hr style="border: 0; height: 2px; background-color: #38bdf8; width: 80%;"> 
            <br><br>
        </h1>
        """)
        put_html("<h1>WELCOME <br> TO<br> TIC-TAC-TOE</h1>")
        put_html("<h4>MAIN MENU</h4>")
        
        dict_of_menu=[
            {'label': 'BOT: EASY', 'value': 1},
            {'label': 'BOT: MID', 'value': 2},
            {'label': 'BOT :(CHALENGES YOU)', 'value': 3},
            {'label': 'MULTY PLAYER', 'value': 4},
            {'label': 'EXIT', 'value': 5}
        ]
        
        choice = actions(buttons=dict_of_menu)
        
        if choice == 1:
            easy_bot.main()
        elif choice == 2:
            mid_bot.main()
        elif choice == 3:
            clear()
            game = hard_bot.TicTacToe()
            game.play()
        elif choice == 4:
            player.main()
        elif choice == 5:
            exit()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    start_server(main, port=port, host='0.0.0.0')
