import math
import constants
from piece import Piece

chess_notation = dict()
chess_notation_inverse = dict()

# set chess notation and inverse dictionary
for i in range(8):
    for j in range(8):
        chess_notation[(j, i)] = constants.CHESS_FILES[i] + str(8 - j)
        chess_notation_inverse[chess_notation[(j, i)]] = (j, i)

print('chess_notation = ', chess_notation)
print('chess_notation_inverse = ', chess_notation_inverse)


def return_cell(cursor_pos):
    y, x = cursor_pos
    return math.floor(x / (constants.WIDTH / 8)), math.floor(y / (constants.WIDTH / 8))


def get_half_moves_from_fen(fen):
    half_moves = 0
    if fen is None:
        fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'  # starting position
    fen_items = fen.split(' ')
    if len(fen_items) > 4:
        half_moves = int(fen_items[4])
    return half_moves


def get_full_moves_from_fen(fen):
    full_moves = 0
    if fen is None:
        fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'  # starting position
    fen_items = fen.split(' ')
    if len(fen_items) > 5:
        full_moves = int(fen_items[5])
    return full_moves


def get_enpassant_square_from_fen(fen):
    enpassant_square = 0
    if fen is None:
        fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'  # starting position
    fen_items = fen.split(' ')
    if len(fen_items) > 3:
        enpassant_square = int(fen_items[3])
    return chess_notation_inverse[enpassant_square]


def get_move_color_from_fen(fen):
    move_color = 'w'
    if fen is None:
        fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'  # starting position
    fen_items = fen.split(' ')
    if len(fen_items) > 1:
        move_color = fen_items[1]
    return move_color


def get_castle_moves_from_fen(fen):
    castle_moves = 0
    if fen is None:
        fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'  # starting position
    fen_items = fen.split(' ')
    if len(fen_items) > 2:
        castle_moves = fen_items[2]
    return castle_moves


def get_board_from_fen(fen):
    # fen = 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1'  # after 1. e4
    # fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2'  # after 1.. c5
    # fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2'  # after 2. Nf3
    if fen is None:
        fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'  # starting position
    fen_items = fen.split(' ')
    fen_pieces = fen_items[0]
    fen_ranks = fen_pieces.split('/')
    ranks = ['' for i in range(8)]
    board = [['' for i in range(8)] for j in range(8)]

    for index, item in enumerate(fen_ranks):
        row_elements = list(item)
        curated_row_elements = []
        for row_count, row_item in enumerate(row_elements):
            if not row_item.isnumeric():
                curated_row_elements.append(row_item)
            else:
                for i in range(int(row_item)):
                    curated_row_elements.append('')
        ranks[index] = curated_row_elements

    # print('ranks = ', ranks)
    for i in range(8):
        for j in range(8):
            item = ranks[i][j]
            if item == '':  # empty square
                pass
            else:
                color = 'w' if item.isupper() else 'b'
                board[i][j] = Piece(color, item, './images/default/' + color + '/' + item + '.png', (i, j))

    return board


def get_fen_from_board(board, player_to_move_color, en_passant_square='-', half_moves=0, full_moves=0):
    fen = ''
    previous_cell_piece = ''
    castle_type = ''

    #  add board position
    for row_counter, row in enumerate(board):
        continuous_empty_cells = 0
        for cell_counter, cell in enumerate(row):
            if type(cell) != Piece:
                continuous_empty_cells += 1
                previous_cell_piece = ''
                continue
            elif type(cell) == Piece:
                if continuous_empty_cells > 0:
                    fen = fen + str(continuous_empty_cells) + board[row_counter][cell_counter].name
                    continuous_empty_cells = 0
                else:
                    fen = fen + board[row_counter][cell_counter].name
                previous_cell_piece = board[row_counter][cell_counter].name

        if previous_cell_piece == '':
            fen = fen + str(continuous_empty_cells)
        fen += '/' if row_counter < len(board)-1 else ' '

    #  add next move color
    fen += player_to_move_color + ' '

    # add castling available KQkq
    white_king_list = get_piece_list_by_name(board, 'K', 'w')
    white_rook_list = get_piece_list_by_name(board, 'R', 'w')
    w_king = white_king_list[0] if white_king_list else None
    w_rook_1 = white_rook_list[0] if white_rook_list and len(white_rook_list) > 0 else None
    w_rook_2 = white_rook_list[1] if white_rook_list and len(white_rook_list) > 1 else None
    w_king_moved = True if w_king is None or w_king.move_count > 0 or w_king.loc != (7, 5) else False
    w_rook_1_moved = True if w_rook_1 is None or w_rook_1.move_count > 0 else False
    w_rook_1_loc = w_rook_1.loc if w_rook_1 is not None else None
    w_rook_2_moved = True if w_rook_2 is None or w_rook_2.move_count > 0 else False
    w_rook_2_loc = w_rook_2.loc if w_rook_2 is not None else None
    # print('w_king_moved=', w_king_moved, 'w_rook_1_moved=', w_rook_1_moved, 'w_rook_1_loc=', w_rook_1_loc, 'w_rook_2_moved=', w_rook_2_moved, 'w_rook_2_loc=', w_rook_2_loc)
    if not w_king_moved and ((not w_rook_1_moved and w_rook_1_loc == (7, 7)) or (not w_rook_2_moved and w_rook_2_loc == (7, 7))):
        castle_type += 'K'
    if not w_king_moved and ((not w_rook_1_moved and w_rook_1_loc == (7, 0)) or (not w_rook_2_moved and w_rook_2_loc == (7, 0))):
        castle_type += 'Q'

    black_king_list = get_piece_list_by_name(board, 'K', 'b')
    black_rook_list = get_piece_list_by_name(board, 'R', 'b')
    b_king = black_king_list[0] if black_king_list else None
    b_rook_1 = black_rook_list[0] if black_rook_list and len(black_rook_list) > 0 else None
    b_rook_2 = black_rook_list[1] if black_rook_list and len(black_rook_list) > 1 else None
    b_king_moved = True if b_king is None or b_king.move_count > 0 or b_king.loc != (0, 5)else False
    b_rook_1_moved = True if b_rook_1 is None or b_rook_1.move_count > 0 else False
    b_rook_1_loc = b_rook_1.loc if b_rook_1 is not None else None
    b_rook_2_moved = True if b_rook_2 is None or b_rook_2.move_count > 0 else False
    b_rook_2_loc = b_rook_2.loc if b_rook_2 is not None else None
    if not b_king_moved and ((not b_rook_1_moved and b_rook_1_loc == (0, 7)) or (not b_rook_2_moved and b_rook_2_loc == (0, 7))):
        castle_type += 'k'
    if not b_king_moved and ((not b_rook_1_moved and b_rook_1_loc == (0, 0)) or (not b_rook_2_moved and b_rook_2_loc == (0, 0))):
        castle_type += 'q'

    if (w_king_moved or (w_rook_1_moved and w_rook_2_moved)) and (b_king_moved or (b_rook_1_moved and b_rook_2_moved)):
        castle_type += '-'

    # print(f'w_king_moved={w_king_moved}, w_rook_1_moved={w_rook_1_moved}, w_rook_1_loc={w_rook_1_loc},  w_rook_2_moved={w_rook_2_moved}, w_rook_1_loc={w_rook_1_loc}')
    # print(f'b_king_moved={b_king_moved}, b_rook_1_moved={b_rook_1_moved}, b_rook_1_loc={b_rook_1_loc}, b_rook_2_moved={b_rook_2_moved}, b_rook_2_loc={b_rook_2_loc}')
    # print('finding castle type, adding to FEN...', castle_type)

    fen += castle_type+' '

    # add en-passant square
    fen += en_passant_square+' '

    # add half-moves since last capture
    fen += str(half_moves) + ' '

    # add number of full-moves for the game
    fen += str(full_moves + 1)

    return fen


def get_piece_by_location(board, location, player_color='w'):
    x, y = location
    if type(board[x][y]) == Piece and board[x][y].color == player_color:
        return board[x][y]
    return None


def get_piece_list_by_name(board, name, color='w'):
    piece_list = []
    for x in range(0, 8):
        for y in range(0, 8):
            if type(board[x][y]) == Piece and board[x][y].name.casefold() == name.casefold() and board[x][y].color == color:
                piece_list.append(board[x][y])
    return piece_list


def get_all_pieces(board, piece_color):  # piece_color = 'w', 'b', 'all'
    piece_list = []
    # print('getting all pieces of color:', piece_color)
    for x in range(0, 8):
        for y in range(0, 8):
            if type(board[x][y]) == Piece:
                if piece_color == 'all' or board[x][y].color == piece_color:
                    # print('found ', (x, y), ' and properties = ', board[x][y].__dict__)
                    piece_list.append(board[x][y])
                else:
                    # print('skipping', (x, y), '. Opposite color piece')
                    pass
            else:
                # print('skipped ', (x, y), 'of type', type(board[x][y]))
                pass
    return piece_list


def print_board(board):
    all_pieces = get_all_pieces(board, piece_color='all')
    grid = [[' ' for i in range(8)] for j in range(8)]
    for piece in all_pieces:
        i, j = piece.loc
        grid[i][j] = piece.name
    for i in range(8):
        print(grid[i])
    return None

