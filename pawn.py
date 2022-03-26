from piece import Piece
import chessboard


def get_moves(board, piece_picked, move_type='push'):
    # Implemented: 1-step-move, 2-step-move, board-conflict
    # Yet to implement: Capture, En-passant
    if type(piece_picked) != Piece:
        return []

    x, y = piece_picked.loc
    piece_color = piece_picked.color

    available_moves = []
    moves_to_consider = []
    captures_to_consider = []

    if piece_color == 'b' and move_type == 'push':
        moves_to_consider = [(x + 1, y), (x + 2, y)] if x == 1 or x == 6 else [(x + 1, y)]
        captures_to_consider = [(x + 1, y + 1), (x + 1, y-1)]
    if piece_color == 'w' and move_type == 'push':
        moves_to_consider = [(x - 1, y), (x - 2, y)] if x == 1 or x == 6 else [(x - 1, y)]
        captures_to_consider = [(x - 1, y + 1), (x - 1, y-1)]

    if piece_color == 'b' and move_type == 'capture':
        moves_to_consider = [(x + 1, y + 1), (x + 1, y-1)]
    if piece_color == 'w' and move_type == 'capture':
        moves_to_consider = [(x - 1, y + 1), (x - 1, y-1)]

    moves_to_consider = [(i, j) for (i, j) in moves_to_consider if (0 <= i <= 7) and (0 <= j <= 7)]
    captures_to_consider = [(i, j) for (i, j) in captures_to_consider if (0 <= i <= 7) and (0 <= j <= 7)]

    if move_type == 'capture':
        available_moves = moves_to_consider
    elif move_type == 'push':
        for (i, j) in moves_to_consider:
            if type(board[i][j]) == Piece:  # board-conflict
                break
            available_moves.append((i, j))
        for (i, j) in captures_to_consider:
            if type(board[i][j]) == Piece and board[i][j].color != piece_color:  # board-conflict
                available_moves.append((i, j))
    return available_moves


def get_enpassant_square(piece, drop_position):
    result_square = None
    result_notation = '-'
    (drop_i, drop_j), (pick_i, pick_j) = drop_position, piece.loc

    # Check if it is initial pawn position. If yes, set en-passant square
    if piece.name == 'p' and pick_i == 1 and drop_i == 3:
        # print('en passant possible with this black move. marking square', (pick_i + 1, pick_j))
        result_square = (pick_i + 1, pick_j)

    if piece.name == 'P' and pick_i == 6 and drop_i == 4:
        # print('en passant possible with this white move. marking square', (pick_i - 1, pick_j))
        result_square = (pick_i - 1, pick_j)

    if result_square is not None:
        result_notation = chessboard.chess_notation[result_square]

    return result_notation
