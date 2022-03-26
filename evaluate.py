import chess
import chess.engine


def get_current_position_score(fen):
    time_limit = 0.100
    engine = chess.engine.SimpleEngine.popen_uci("/usr/local/Cellar/stockfish/14.1/bin/stockfish")
    result = engine.analyse(chess.Board(fen), chess.engine.Limit(time=time_limit))
    engine.quit()
    print('engine eval: ', result['score'])
    best_move = str(result['pv'][0])
    return best_move


