from piece import Piece


def get_moves(board, piece_picked):
    # Implemented: board-conflict,
    # Yet to implement: capture
    if type(piece_picked) != Piece:
        return []

    available_moves = []
    x, y = piece_picked.loc
    piece_color = piece_picked.color

    moves_to_consider = [(x, y), (x + 2, y + 1), (x + 2, y - 1), (x - 2, y + 1), (x - 2, y - 1),
                         (x + 1, y + 2), (x + 1, y - 2), (x - 1, y + 2), (x - 1, y - 2)]
    moves_to_consider = [(i, j) for (i, j) in moves_to_consider if (0 <= i <= 7) and (0 <= j <= 7)]
    for move in moves_to_consider:
        i, j = move
        if type(board[i][j]) == Piece and board[i][j].color == piece_color:  # board-conflict
            continue
        available_moves.append(move)

    available_moves = [(i, j) for (i, j) in available_moves if (0 <= i <= 7) and (0 <= j <= 7)]
    return available_moves


