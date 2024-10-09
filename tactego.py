
import random

def draw_board(pieces_file, length, width):
    """
    Draws the game board based on provided parameters.
    Parameters:
    - pieces_file: str - Name of the file containing pieces information.
    - length: int - Length of the game board.
    - width: int - Width of the game board.
    Returns:
    - board: list - Game board with the pieces placed in it.
    """
    with open(pieces_file, 'r') as file:
        lines = file.readlines()

    red_pieces = {}
    blue_pieces = {}
    for i in lines:
        stripped = i.strip()
        split_items = stripped.split()
        item = split_items[0]
        quantity = split_items[1]
        blue_pieces["B" + item] = int(quantity)
        red_pieces["R" + item] = int(quantity)

    red_keys = list(red_pieces.keys())
    blue_keys = list(blue_pieces.keys())
    random.shuffle(red_keys)
    random.shuffle(blue_keys)
    board = [['  ' for _ in range(width)] for _ in range(length)]
    max_area = (length * width) // 2

    # Fill the board with items from red_pieces starting from the top
    counter_red = 0
    for i in red_keys:
        value = red_pieces[i]
        for j in range(value):
                        if counter_red < max_area:
                row = counter_red // width
                col = counter_red % width
                board[row][col] = i
                counter_red += 1
            else:
                return print ("Invalid dimensions")

    # Fill the board with items from blue_pieces starting from the bottom
    counter_blue = 0
    for i in blue_keys:
        value = blue_pieces[i]
        for j in range(value):
            if counter_blue < max_area:
                row = length - 1 - (counter_blue // width)
                col = width - 1 - (counter_blue % width)
                board[row][col] = i
                counter_blue += 1
            else:
                return print("Invalid dimensions")
    return board

def is_valid_move(board, from_row, from_col, to_row, to_col, player):
    """
        Checks if a move is valid on the game board.
    Parameters:
    - board: list - Game board with pieces.
    - from_row: int - Starting row of the piece.
    - from_col: int - Starting column of the piece.
    - to_row: int - Destination row of the piece.
    - to_col: int - Destination column of the piece.
    - player: str - Current player ('Red' or 'Blue').
    Returns:
    - bool - Indicates if the move is valid or not.
    - string - Message explaining why they cannot move their piece to the given cordinates.
    """
    if 0 <= from_row < len(board) and 0 <= from_col < len(board[0]) and 0 <= to_row < len(board) and 0 <= to_col < len(board[0]):
        from_piece = board[from_row][from_col]
        to_piece = board[to_row][to_col]

        # Check if it's the player's piece
        if from_piece[0] != player[0]:
            return False, "You can only move your own piece."

        # Check if the move is valid (within one space in any direction)
        if abs(from_row - to_row) <= 1 and abs(from_col - to_col) <= 1:
            if from_piece[1] == 'F':
                return False, "You can't move your flag."
            elif to_piece == '  ':
                #if it's empty space move the piece
                return True, ""
            else:
                # Check if it's an opponent's piece
                if from_piece[0] != to_piece[0]:
                    if to_piece[1] == 'F':
                        board[to_row][to_col] = '  '
                        board[from_row][from_col] = from_piece
                        return True, ""
                    else:
                        from_num = int(from_piece[1:])
                        to_num = int(to_piece[1:])

                        if from_num > to_num:
                            board[to_row][to_col] = '  '
                            board[from_row][from_col] = from_piece
                            return True, ""
                        elif from_num == to_num:
                            board[to_row][to_col] = '  '
                            board[from_row][from_col] = from_piece
                            return True, ""
                        else:
                                                        board[to_row][to_col] = '  '
                            board[from_row][from_col] = to_piece
                            return True, ""
                else:
                    return False, "You can't move to a space occupied by your own piece."
        else:
            return False, "Invalid move. You can only move one space in any direction."
    else:
        return False, "Invalid coordinates. Coordinates should be within the board."

def player_turn(board, player):
    """
    This is a helper function that manages the turn for a player.
    Parameters:
    - board: list - Game board with pieces.
    - player: string - Current player ('Red' or 'Blue').
    """
    playing = True
    while playing:
        print(f"It's {player}'s turn")
        move_from = input("Enter coordinates (row column) to move from: ").split()
        move_to = input("Enter coordinates (row column) to move to: ").split()
        # making sure the inputs are valid if not then keep player in loop until valid input is provided
                if len(move_from) != 2 or len(move_to) != 2 or not move_from[0].isdigit() or not move_from[1].isdigit() or not move_to[0].isdigit() or not move_to[1].isdigit():
            print("Invalid input. Please enter valid coordinates as two numbers separated by a space.")
            user_input = False
            while not user_input:
                move_from = input("Enter coordinates (row column) to move from: ").split()
                move_to = input("Enter coordinates (row column) to move to: ").split()
                if len(move_from) != 2 or len(move_to) != 2 or not move_from[0].isdigit() or not move_from[1].isdigit() or not move_to[0].isdigit() or not move_to[1].isdigit():
                    print("Invalid input. Please enter valid coordinates as two numbers separated by a space.")
                else:
                    user_input = True

        from_row = int(move_from[0])
        from_col = int(move_from[1])
        to_row = int(move_to[0])
        to_col = int(move_to[1])

        is_valid = is_valid_move(board, from_row, from_col, to_row, to_col, player)
        valid = is_valid[0]
        message = is_valid[1]
        if valid:
            from_piece = board[from_row][from_col]
            board[to_row][to_col] = from_piece
            board[from_row][from_col] = '  '
            return

        print(message)

def display_board(board):
    """
    This is a helper function that displays the game board.
    Parameters:
    - board: list - Game board with pieces.
    """
    max_piece_length = max(len(piece) for row in board for piece in row) + 1
    max_index_length = len(str(len(board) - 1))

    print(' ' * (max_index_length + 1), end='')
    for i in range(len(board[0])):
        print(f'{i:<{max_piece_length}}', end=' ')
    print('\n')

    counter = 0
    for i in board:
        print(f'{counter:<{max_index_length}}', end=' ')
        counter += 1
        for j in i:
            print(f'{j:<{max_piece_length}}', end=' ')
        print()
        
def game_over(board):
    """
    This is a helper function taht checks if the game is over.
    Parameters:
    - board: list - Game board with pieces.
    Returns:
    - bool - Indicates if the game has ended or not.
    """
    red_flag_remaining = False
    blue_flag_remaining = False

    # Check the board for remaining flag pieces
    for i in board:
        for j in i:
            if j == 'RF':
                red_flag_remaining = True
            elif j == 'BF':
                blue_flag_remaining = True

    if not red_flag_remaining:
        print("B has won the game")
        return True
    elif not blue_flag_remaining:
        print("R has won the game")
        return True
    return False

def tactego():
    """
    Main function where the game runs.
    """
    random.seed = input('What is the seed? ')
    file_name = input('What is the filename for the pieces? ')
    length = int(input('What is the length? '))
    width = int(input('What is the width? '))
    board = draw_board(file_name, length, width)
    player = 'Red'
    game_running = True

    while game_running:
        display_board(board)
        player_turn(board, player)

        if game_over(board):
            display_board(board)
            game_running = False
        if player == 'Red':
                        player = 'Blue'
        else:
            player = 'Red'

if __name__ == '__main__':
    tactego()