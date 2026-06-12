from pywebio.input import actions
from pywebio.output import clear, put_html

def choise(board):
    clear()
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
            if board[r][c] == 0:
                btns.append({'label': ' ', 'value': pos})
            else:
                btns.append({'label': str(board[r][c]), 'value': pos, 'disabled': True})
    
    return actions(buttons=btns)

def show_result(board, msg):
    clear()
    put_html(f"<h2 style='text-align: center;'>{msg}</h2>")
    
    grid_html = '<div style="display: grid; grid-template-columns: repeat(3, 85px); gap: 5px; justify-content: center; width: max-content; margin: 20px auto;">'
    for r in range(3):
        for c in range(3):
            cell = board[r][c]
            text = str(cell) if cell != 0 else "&nbsp;"
            grid_html += f'<div style="width: 80px; height: 80px; border: 1px solid black; display: flex; align-items: center; justify-content: center; font-size: 24px;">{text}</div>'
    grid_html += '</div><br>'
    
    put_html(grid_html)
    
    actions(buttons=[{'label': 'Return to Menu', 'value': 'back'}])