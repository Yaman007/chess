import copy

from piece import Piece
import chessmove
import chessboard

import queen


def get_moves(board, piece_picked, check_castling=False, move_type='push'):
    # print('get_king_moves: king color=', king_color, 'king pos=', pick_pos, 'check_castling=', check_castling)
    # Yet to implement: Castling completely, king capturing another king
    if type(piece_picked) != Piece:
        return []

    piece_color = piece_picked.color

    opponent_capture_squares = []

    available_moves = [queen.get_moves(board, piece_picked, neighbors=1)]

    if check_castling or move_type == 'Capture':
        opponent_color = 'w' if piece_color == 'b' else 'b'
        opponent_capture_squares = chessmove.get_all_capture_moves(board, player_color=opponent_color)
        castling_moves = get_castling_moves(board, piece_color, opponent_moves=opponent_capture_squares)
        available_moves.append(castling_moves)
    # flatten list and remove [] moves and moves in opponent capture squares
    available_moves = [move for sublist in available_moves for move in sublist if move and move not in opponent_capture_squares]
    # print('available king moves =', available_moves)

    available_moves = [(i, j) for (i, j) in available_moves if (0 <= i <= 7) and (0 <= j <= 7)]
    return available_moves


def get_castling_moves(board, king_color, opponent_moves=[]):
    castling_moves = []
    fen = chessboard.get_fen_from_board(board, king_color)
    fen_castle_moves = chessboard.get_castle_moves_from_fen(fen)

    if king_color == 'w' and 'K' in fen_castle_moves and castling_route_clear(board, [(7, 5), (7, 6)], opponent_moves=opponent_moves):
        print('white king side castle possible with no interfering pieces or checks')
        castling_moves.append((7, 6))

    if king_color == 'w' and 'Q' in fen_castle_moves and castling_route_clear(board, [(7, 3), (7, 2)], opponent_moves=opponent_moves):
        print('white queen side castle possible with no interfering pieces or checks')
        castling_moves.append((7, 2))

    if king_color == 'b' and 'k' in fen_castle_moves and castling_route_clear(board, [(0, 5), (0, 6)], opponent_moves=opponent_moves):
        print('black king side castle possible with no interfering pieces or checks')
        castling_moves.append((0, 6))

    if king_color == 'b' and 'q' in fen_castle_moves and castling_route_clear(board, [(0, 3), (0, 2)], opponent_moves=opponent_moves):
        print('black queen side castle possible with no interfering pieces or checks')
        castling_moves.append((0, 2))

    return castling_moves


def castling_route_clear(board, castle_route, opponent_moves=[]):
    # No interfering pieces and no checks along castling squares
    pieces_clear = True
    checks_clear = True

    # print('opponent_available_moves = ', opponent_moves)
    for (x, y) in castle_route:
        if board[x][y] != '':
            pieces_clear = False
            print('no castling allowed on', castle_route, 'Pieces in the way')
            break
        if (x, y) in opponent_moves:
            checks_clear = False
            print('no castling allowed on', castle_route, 'King will come under check')
            break

    return pieces_clear and checks_clear


def get_castling_type(piece_picked, drop_position):
    # print('get_castling_type debug: ', piece_picked.name, piece_picked.loc, piece_picked.color, drop_position)
    pick_position = piece_picked.loc
    piece_color = piece_picked.color
    castle_type = '-'  # possible values k(b-king side), q(b-queen side), K(w-king side), Q(w-queen side)
    if piece_picked.name == 'k' and pick_position == (0, 4) and piece_color == 'b' and drop_position == (0, 6):
        castle_type = 'k'
    if piece_picked.name == 'k' and pick_position == (0, 4) and piece_color == 'b' and drop_position == (0, 2):
        castle_type = 'q'
    if piece_picked.name == 'K' and pick_position == (7, 4) and piece_color == 'w' and drop_position == (7, 6):
        castle_type = 'K'
    if piece_picked.name == 'K' and pick_position == (7, 4) and piece_color == 'w' and drop_position == (7, 2):
        castle_type = 'Q'
    # print('returning castle type = ', castle_type)
    return castle_type


def is_under_check(board, color='w'):
    flag = False
    king_list = chessboard.get_piece_list_by_name(board, 'k', color)
    king = king_list[0] if king_list else None
    opponent_color = 'w' if color == 'b' else 'b'
    opponent_capture_squares = chessmove.get_all_capture_moves(board, player_color=opponent_color)
    if (king is not None) and (king.loc in opponent_capture_squares):
        flag = True
    # print(color, 'king under check? ', flag)
    return flag


def is_safe_after_move(board, piece_picked, drop_position):
    board = copy.deepcopy(board)
    piece = copy.deepcopy(piece_picked)
    player_color = piece_picked.color
    chessmove.make_move(board, piece, drop_position)
    safety_flag = not is_under_check(board, player_color)
    return safety_flag


def is_opponent_checkmated(board, player_color):
    # print('****** evaluating opponent checkmate!')
    checkmate = True
    opponent_color = 'b' if player_color == 'w' else 'w'  # toggle player color
    opponent_pieces = chessboard.get_all_pieces(board, opponent_color)
    for piece in opponent_pieces:
        # checking available moves for every opponent piece
        # print('** Checking moves for', piece.color, '-', piece.name, 'at loc', piece.loc)
        available_moves = chessmove.get_moves(board, piece, check_castling=False)  # get legal moves
        available_moves = [move for move in available_moves if move]  # filter out [] / empty move
        # print('Available moves:', available_moves)
        for move in available_moves:
            # checking king safety for each available move. if safety found, then no checkmate possible
            is_king_safe = is_safe_after_move(board, piece, move)
            # print('Is king safe with move', move, '?', is_king_safe)

            if is_king_safe:
                return False

    print('*** Checkmate for ', opponent_color, ' king =', checkmate)
    return checkmate


