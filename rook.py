from piece import Piece


def get_moves(board, piece_picked, neighbors=0):
    # Implemented: right-move, left-move, up-move, down-move, board-conflict,
    # Yet to implement: capture
    # print('rook move scan, neighbors = ', neighbors)
    available_moves = []
    directional_moves = []
    right_move, left_move, up_move, down_move = [], [], [], []
    x, y = piece_picked.loc if type(piece_picked) == Piece else (-1, -1)
    piece_color = piece_picked.color if type(piece_picked) == Piece else '-'  # unknown color, will raise exception

    for i in range(8 - y):  # right-move, going right on the board
        right_move.append((x, y + i))

    for i in range(0, y + 1):  # left-move, going left on the board
        left_move.append((x, y - i))

    for i in range(8 - x):  # down-move, going down the board
        down_move.append((x + i, y))

    for i in range(0, x + 1):  # up-move, going up the board
        up_move.append((x - i, y))

    directional_moves.append(right_move)
    directional_moves.append(left_move)
    directional_moves.append(up_move)
    directional_moves.append(down_move)
    # print('directional rook moves:', directional_moves)

    # board-conflict implementation
    for direction in directional_moves:
        # remove pick_pos from available_moves
        moves = [move for move in direction if move != (x, y)]
        neighbor_count = 0
        for (i, j) in moves:
            neighbor_count += 1
            # stop if you encounter a piece, after marking the opposite color piece as 'can-capture'
            if type(board[i][j]) == Piece:
                if board[i][j].color != piece_color:
                    board[i][j].can_capture = True
                    available_moves.append((i, j))
                break
            available_moves.append((i, j))
            # stop if max neighbor limit reached
            if (neighbors > 0) and (neighbor_count == neighbors):
                break

    available_moves = [(i, j) for (i, j) in available_moves if (0 <= i <= 7) and (0 <= j <= 7)]
    return available_moves
