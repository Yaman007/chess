from piece import Piece
import rook
import bishop


def get_moves(board, piece_picked, neighbors=0):
    available_moves = []
    rook_moves = rook.get_moves(board, piece_picked, neighbors)
    bishop_moves = bishop.get_moves(board, piece_picked, neighbors)
    # print('rook like moves', rook_moves)
    # print('bishop like moves', bishop_moves)
    available_moves.append(rook_moves)
    available_moves.append(bishop_moves)
    # flatten list and remove [] moves
    available_moves = [move for sublist in available_moves for move in sublist if move]

    available_moves = [(i, j) for (i, j) in available_moves if (0 <= i <= 7) and (0 <= j <= 7)]
    return available_moves


