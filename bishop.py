from piece import Piece


def get_moves(board, piece_picked, neighbors=0):
    # Yet to implement: q1-move, q2-move, q3-move, q4-move, board-conflict, capture
    # print('bishop move scan, neighbors = ', neighbors)
    available_moves = []
    directional_moves = []
    quad1_move, quad2_move, quad3_move, quad4_move = [], [], [], []
    x, y = piece_picked.loc if type(piece_picked) == Piece else (-1, -1)
    piece_color = piece_picked.color if type(piece_picked) == Piece else '-'  # unknown color, will raise exception

    for i in range(8 - y):  # quadrant 1-move
        if 0 <= x - i < 8 and 0 <= y + i < 8:
            quad1_move.append((x - i, y + i))
        else:
            break

    for i in range(0, y + 1):  # quadrant 3-move
        if 0 <= x + i < 8 and 0 <= y - i < 8:
            quad3_move.append((x + i, y - i))
        else:
            break

    for i in range(8 - x):  # quadrant 2-move
        if 0 <= x + i < 8 and 0 <= y + i < 8:
            quad2_move.append((x + i, y + i))
        else:
            break

    for i in range(0, x + 1):  # quadrant 4-move
        if 0 <= x - i < 8 and 0 <= y - i < 8:
            quad4_move.append((x - i, y - i))
        else:
            break

    directional_moves.append(quad1_move)
    directional_moves.append(quad3_move)
    directional_moves.append(quad2_move)
    directional_moves.append(quad4_move)
    # print('directional bishop moves:', directional_moves)

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


