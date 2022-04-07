import chess
import chess.engine
import chessboard

kingWt = 200
queenWt = 9
rookWt = 5
bishopWt = 3.2
knightWt = 3
pawnWt = 1
mobilityWt = 0.1
wK = bK = wQ = bQ = wB = bB = wN = bN = wP = bP = 0  # piece count
wM = bM = 0  # piece mobility


def get_stockfish_score(fen):
    time_limit = 0.100
    engine = chess.engine.SimpleEngine.popen_uci("/usr/local/Cellar/stockfish/14.1/bin/stockfish")
    result = engine.analyse(chess.Board(fen), chess.engine.Limit(time=time_limit))
    engine.quit()
    print('engine eval: ', result['score'])
    best_move = str(result['pv'][0])
    return best_move


def get_material_score_from_fen(fen):
    board = chessboard.get_board_from_fen(fen)
    score = get_material_score_from_board(board)
    return score


def get_material_score_from_board(board):
    print('*** inside get_material_score_from_board ***')
    print('board = ', board)
    for piece in chessboard.get_piece_list_by_name(board, 'R', 'w'):
        print(piece.__dict__)

    score = '10'
    print('score = ', score)
    print('### exiting ###')
    return score


def main():
    starting_fen = 'R7/8/5rk1/5p2/1p5P/5KP1/P7/8 b - - 0 0'
    board = chessboard.get_board_from_fen(starting_fen)
    chessboard.print_board(board)
    score = get_material_score_from_board(board)


main()