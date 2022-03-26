import copy

import pygame

import chessui
import constants

import pawn
import rook
import bishop
import knight
import queen
import king

import chessboard
from piece import Piece

w_short_castle_rook = Piece('w', 'R', './images/default/w/R.png', (7, 5))
w_long_castle_rook = Piece('w', 'R', './images/default/w/R.png', (7, 3))
b_short_castle_rook = Piece('b', 'r', './images/default/b/r.png', (0, 5))
b_long_castle_rook = Piece('b', 'r', './images/default/b/r.png', (0, 3))

font = pygame.font.Font(pygame.font.get_default_font(), 15)
large_font = pygame.font.Font(pygame.font.get_default_font(), 35)
medium_font = pygame.font.Font(pygame.font.get_default_font(), 25)
debug_font = pygame.font.Font(pygame.font.get_default_font(), 12)


def is_capture_or_pawn_advance(board, piece_picked, drop_position):
    result = False
    (x, y) = drop_position
    if type(piece_picked) == Piece:
        if piece_picked.name.casefold() == 'p':  # pawn is selected for move
            result = True
        elif type(board[x][y]) == Piece:  # drop square already has another piece, signifying capture move
            result = True
    # print('is_capture_or_pawn_advance = ', result)
    return result


def get_moves(board, piece_picked, check_castling=False, move_type='push'):  # push or capture moves

    available_moves = []
    if piece_picked.name.casefold() == 'p':
        # print('finding pawn moves')
        available_moves = pawn.get_moves(board, piece_picked, move_type)

    if piece_picked.name.casefold() == 'r':
        # print('finding rook moves')
        available_moves = rook.get_moves(board, piece_picked)

    if piece_picked.name.casefold() == 'b':
        # print('finding bishop moves')
        available_moves = bishop.get_moves(board, piece_picked)

    if piece_picked.name.casefold() == 'n':
        # print('finding knight moves')
        available_moves = knight.get_moves(board, piece_picked)

    if piece_picked.name.casefold() == 'q':
        # print('finding queen moves')
        available_moves = queen.get_moves(board, piece_picked)

    if piece_picked.name.casefold() == 'k':
        # print('finding king moves')
        available_moves = king.get_moves(board, piece_picked, check_castling, move_type)

    return available_moves


def get_all_valid_moves(board, player_color):  # only non-capture moves
    all_available_moves = []
    pieces = chessboard.get_all_pieces(board, piece_color=player_color)
    for each_piece in pieces:
        each_piece_available_moves = get_moves(board, each_piece, check_castling=False)
        # print(each_piece.__dict__, 'available moves: ', each_piece_available_moves)
        all_available_moves.append(each_piece_available_moves)
    # flatten list and remove [] moves
    all_available_moves = [move for sublist in all_available_moves for move in sublist if move]
    all_available_moves = list(set(all_available_moves))  # removing duplicates
    return all_available_moves


def get_all_capture_moves(board, player_color):  # only capture moves, pawn and king behave differently
    capture_moves = []
    pieces = chessboard.get_all_pieces(board, piece_color=player_color)
    for each_piece in pieces:
        each_piece_available_moves = get_moves(board, each_piece,  check_castling=False, move_type='capture')
        # print(each_piece.__dict__, 'available moves: ', each_piece_available_moves)
        capture_moves.append(each_piece_available_moves)
    # flatten list and remove [] moves
    all_available_moves = [move for sublist in capture_moves for move in sublist if move]
    all_available_moves = list(set(all_available_moves))  # removing duplicates
    return all_available_moves


def make_move(board, piece, drop_position):
    (drop_i, drop_j), (pick_i, pick_j) = drop_position, piece.loc
    # print('inside making move...')
    # print('drop pos = ', drop_position)
    # print('piece = ', piece.name, piece.loc, piece.color)

    # find castle type, so that in case of king castle, rook needs to be moved too
    castle_type = king.get_castling_type(piece, (drop_i, drop_j))

    # Reset Pick Square
    board[pick_i][pick_j] = ''

    # Assign Drop Square
    piece.loc = (drop_i, drop_j)  # update piece location
    piece.move_count += 1  # increment the piece move count, useful in case of determining castling status
    board[drop_i][drop_j] = piece  # assign piece to board

    # Move the rook too, in case of castle
    # print('inside make_move. castle type = ', castle_type)
    if castle_type == 'k':  # black short / king-side castle (rook to 0, 5)
        board[0][7] = ''
        board[0][5] = copy.deepcopy(b_short_castle_rook)
    if castle_type == 'q':  # black long / queen-side castle (rook to 0, 2)
        board[0][0] = ''
        board[0][3] = copy.deepcopy(b_long_castle_rook)
    if castle_type == 'K':  # white short / king-side castle (rook to 7, 5)
        board[7][7] = ''
        board[7][5] = copy.deepcopy(w_short_castle_rook)
    if castle_type == 'Q':  # white long / queen-side castle (rook to 7, 2)
        board[7][0] = ''
        board[7][3] = copy.deepcopy(w_long_castle_rook)

    player_to_move_color = 'w' if piece.color == 'b' else 'b'
    fen = chessboard.get_fen_from_board(board, player_to_move_color)
    # print('FEN after making the move = ', fen)


# this function is not being used yet
def make_pgn_move(board, pgn_move, player_color):
    if len(pgn_move) != 4:
        print('can\'t make this move. ', pgn_move, 'exiting')
        return
    else:
        pick_position = chessboard.chess_notation_inverse[pgn_move[0:2]]
        drop_position = chessboard.chess_notation_inverse[pgn_move[2:4]]
        piece = chessboard.get_piece_by_location(board, pick_position, player_color)
        castle_type = king.get_castling_type(piece, drop_position)
        make_move(board, piece, drop_position)


