import pygame
import copy

import constants

import pawn
import king

import chessboard
import chessui
import evaluate
import chessmove

from piece import Piece

chess_notation = chessboard.chess_notation  # (0, 0) = a1
chess_notation_inverse = chessboard.chess_notation_inverse  # a1 = (0, 0)

# starting fen is 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
# starting_fen = '8/4Q3/3K4/8/8/2r3k1/8/5R2 w - - 0 0'  # end game position
# starting_fen = '6k1/5p2/6p1/8/7p/8/6PP/6K1 b - - 0 0'
# starting_fen = 'r7/4R2P/3p4/3k1K2/2p5/8/8/8 b - - 0 0'
starting_fen = 'R7/8/5rk1/5p2/1p5P/5KP1/P7/8 b - - 0 0'
# starting_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'  # starting position

WIDTH = constants.WIDTH

button_h = WIDTH / 16
button_w = WIDTH / 8
button1_x, button1_y = 0.2 * WIDTH / 8, 8.25 * WIDTH / 8
button2_x, button2_y = 1.3 * WIDTH / 8, 8.25 * WIDTH / 8
button3_x, button3_y = 5.0 * WIDTH / 8, 8.25 * WIDTH / 8
button4_x, button4_y = 6 * WIDTH / 8, 8 * WIDTH / 8
button5_x, button5_y = 2.4 * WIDTH / 8, 8.25 * WIDTH / 8

message_x, message_y = int(6.03 * WIDTH / 8), int(8.20 * WIDTH / 8)


def main():
    global en_passant_square

    white_player = 'human'
    black_player = 'human'

    en_passant_square = '-'
    game_moves_queue = []
    move_navigator_counter = 0
    last_navigated_game_move = None
    pawn_promotion_flag = False
    pawn_promotion_loc = None
    game_message = None  # used for displaying key in-game messages on the screen

    # initialize board and set pieces
    board = chessboard.get_board_from_fen(starting_fen)  # starting fen
    chessboard.print_board(board)

    player_color = chessboard.get_move_color_from_fen(starting_fen)
    half_moves = chessboard.get_half_moves_from_fen(starting_fen)  # moves since pawn advance or piece capture

    action = 'PICK'
    running = True

    legal_drop_squares = []
    pick_position = None

    is_human_turn = True if (player_color == 'w' and white_player == 'human') or \
                            (player_color == 'b' and black_player == 'human') else False

    pygame.init()
    pygame.display.set_caption("Yaman Chess")
    screen = pygame.display.set_mode(constants.WINDOW)
    chessui.draw_board_on_screen(board, screen)
    chessui.draw_user_panels_on_screen(screen)
    # --- alternate way to draw the board ---
    # chessui.draw_board_from_pieces(screen, chessboard.get_all_pieces(board, piece_color='all'))

    while running:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif is_human_turn and event.type == pygame.MOUSEBUTTONDOWN:
                print(
                    f'START OF LOOP: player_color={player_color}, action={action}, en_passant_square={en_passant_square}')
                fen = chessboard.get_fen_from_board(board, player_color, en_passant_square, half_moves=half_moves,
                                                    full_moves=len(game_moves_queue) // 2)
                print('FEN = ', fen)

                chessui.draw_board_on_screen(board, screen, game_message)
                cursor_pos = pygame.mouse.get_pos()
                x, y = chessboard.return_cell(cursor_pos)  # get the position selected

                message = 'cursor=' + cursor_pos.__str__()
                chessui.add_text(screen, message, message_x, message_y, chessui.debug_font)

                if (x > 7 or y > 7) and not pawn_promotion_flag:
                    #  Previous button
                    button1_clicked = True if button1_x < cursor_pos[0] < button1_x + button_w \
                                              and button1_y < cursor_pos[1] < button1_y + button_h else False
                    #  Next button
                    button2_clicked = True if button2_x < cursor_pos[0] < button2_x + button_w \
                                              and button2_y < cursor_pos[1] < button2_y + button_h else False
                    #  Reset button
                    button3_clicked = True if button3_x < cursor_pos[0] < button3_x + button_w \
                                              and button3_y < cursor_pos[1] < button3_y + button_h else False
                    #  Human = White
                    button5_clicked = True if button5_x < cursor_pos[0] < button5_x + button_w \
                                              and button5_y < cursor_pos[1] < button5_y + button_h / 2 else False

                    #  Human = Black
                    button6_clicked = True if button5_x < cursor_pos[0] < button5_x + button_w \
                                              and button5_y + 30 < cursor_pos[
                                                  1] < button5_y + 30 + button_h / 2 else False

                    #  Human = Both
                    button7_clicked = True if button5_x + 100 < cursor_pos[0] < button5_x + 100 + button_w \
                                              and button5_y < cursor_pos[1] < button5_y + button_h / 2 else False

                    #  Human = None
                    button8_clicked = True if button5_x + 100 < cursor_pos[0] < button5_x + 100 + button_w and \
                                              button5_y + 30 < cursor_pos[1] < button5_y + 30 + button_h / 2 else False

                    message = str(button1_clicked) + ',' + str(button2_clicked) + ',' + str(button3_clicked)
                    message_1 = str(button5_clicked) + ',' + str(button6_clicked) + ',' + str(
                        button7_clicked) + ',' + str(button8_clicked)
                    chessui.add_text(screen, message, message_x, message_y + 15, chessui.debug_font)
                    chessui.add_text(screen, message_1, message_x, message_y + 30, chessui.debug_font)

                    #  Previous move button clicked
                    if button1_clicked:
                        if move_navigator_counter > 0:
                            last_navigated_game_move = game_moves_queue[move_navigator_counter - 1]
                            move_navigator_counter -= 1
                            print('move counter=', move_navigator_counter, 'navigating down to move #',
                                  last_navigated_game_move)
                            chessui.draw_board_on_screen(last_navigated_game_move[4], screen, game_message)
                        else:
                            print('at the first game move')

                    #  Next move button clicked
                    elif button2_clicked:
                        if move_navigator_counter < len(game_moves_queue) - 1:
                            last_navigated_game_move = game_moves_queue[move_navigator_counter + 1]
                            move_navigator_counter += 1
                            print('move counter=', move_navigator_counter, 'navigating up to move #',
                                  last_navigated_game_move)
                            chessui.draw_board_on_screen(last_navigated_game_move[4], screen, game_message)
                        else:
                            print('at the last game move')
                            if last_navigated_game_move is not None and type(last_navigated_game_move) == tuple:
                                chessui.draw_board_on_screen(last_navigated_game_move[5], screen,
                                                             game_message)  # show final board position
                                move_navigator_counter = len(game_moves_queue)

                    #  Reset board when Reset button clicked
                    elif button3_clicked:
                        game_moves_queue = []
                        en_passant_square = '-'
                        move_navigator_counter = 0
                        last_navigated_game_move = None
                        action = 'PICK'
                        pick_position = None
                        piece_picked = None
                        available_moves = []
                        legal_drop_squares = []
                        castle_type = ''
                        board = chessboard.get_board_from_fen(starting_fen)  # reset board
                        player_color = chessboard.get_move_color_from_fen(starting_fen)
                        half_moves = chessboard.get_half_moves_from_fen(starting_fen)
                        game_message = None
                        pawn_promotion_flag = False
                        pawn_promotion_loc = None
                        chessui.draw_board_on_screen(board, screen, game_message)

                    #  Human as White button clicked
                    elif button5_clicked:
                        white_player = 'human'
                        black_player = 'computer'

                    #  Human as Black button clicked
                    elif button6_clicked:
                        white_player = 'computer'
                        black_player = 'human'

                    #  Human as Both button clicked
                    elif button7_clicked:
                        white_player = 'human'
                        black_player = 'human'

                    #  Human as None button clicked
                    elif button8_clicked:
                        white_player = 'computer'
                        black_player = 'computer'

                    is_human_turn = True if (player_color == 'w' and white_player == 'human') or \
                                            (player_color == 'b' and black_player == 'human') else False
                # x < 7 and y < 7
                elif is_human_turn and not pawn_promotion_flag:  # unnecessary condition
                    if action == 'PICK':
                        message = 'cell=' + str(x) + ',' + str(y)
                        chessui.add_text(screen, message, message_x, message_y + 15, chessui.debug_font)

                        print('+++++ picking piece')
                        pick_position = (x, y)
                        piece_picked = chessboard.get_piece_by_location(board, (x, y),
                                                                        player_color)  # get the piece picked

                        if piece_picked is not None:
                            print('+++++ piece picked = ', piece_picked.name, piece_picked.color, pick_position)

                            available_moves = chessmove.get_moves(board, piece_picked,
                                                                  check_castling=True)  # get legal moves

                            available_moves = [move for move in available_moves if move]  # filter out [] / empty move
                            print('For player', player_color, ', picked ', piece_picked.img, ' at position = ',
                                  pick_position, '. Available moves = ',
                                  available_moves)
                            if not available_moves:
                                continue

                            chessui.highlight_move_squares(screen, available_moves, piece_picked)
                            legal_drop_squares = available_moves
                            # best_move = evaluate_board(copy.deepcopy(board), screen, fen)
                            action = 'DROP'
                        else:
                            print('nothing to pick here')

                    elif action == 'DROP':
                        print('***** dropping piece')
                        board_squares_to_highlight = []

                        if (x, y) in legal_drop_squares:
                            piece_picked = chessboard.get_piece_by_location(board, pick_position,
                                                                            player_color)  # get the piece picked
                            print('evaluating move of', piece_picked.name, 'from', piece_picked.loc, 'to', (x, y))
                            if king.is_safe_after_move(board, piece_picked, (x, y)):
                                print('make_move: Selecting', piece_picked.img, 'from', piece_picked.loc,
                                      'and dropping at', (x, y))
                                ''' Get en-passant square for pawn capture evaluation and fen'''
                                en_passant_square = pawn.get_enpassant_square(piece_picked, drop_position=(x, y))

                                ''' Check if this move is a pawn advance or capture'''
                                if chessmove.is_capture_or_pawn_advance(board, piece_picked, drop_position=(x, y)):
                                    half_moves = 0
                                else:
                                    half_moves += 1

                                ''' CHECK IF ITS PAWN PROMOTION MOVE'''
                                if (piece_picked.name == 'P' and piece_picked.color == 'w' and x == 0) or \
                                        (piece_picked.name == 'p' and piece_picked.color == 'b' and x == 7):
                                    # 8th rank for a white pawn or 1st rank for a black pawn
                                    print(f'time to promote {piece_picked.color} pawn')
                                    # remove pawn from the board
                                    pick_x, pick_y = pick_position
                                    board[pick_x][pick_y] = ''

                                    screen = pygame.display.set_mode(constants.WINDOW)
                                    chessui.add_text(screen, 'Promote ' + piece_picked.color + ' pawn to',
                                                     0.5 * constants.WIDTH / 8,
                                                     8.05 * constants.WIDTH / 8, chessui.font, color=constants.BLUE)
                                    chessui.draw_board_on_screen(board, screen, highlight_squares=[(x, y)])
                                    chessui.draw_promotion_options_on_screen(screen, x_starting=3, y_starting=8.05, y_gap=0.25)

                                    pawn_promotion_flag = True
                                    pawn_promotion_loc = (x, y)
                                    continue

                                ''' MAKING MOVE '''
                                board_before_move = copy.deepcopy(board)
                                chessmove.make_move(board, piece_picked, drop_position=(x, y))
                                board_after_move = copy.deepcopy(board)

                                ''' UPDATING GAME MOVES LIST '''
                                ''' (move_count, piece_moved, pick_pos, drop_pos, board_before, board_after) '''
                                game_moves_queue.append((len(game_moves_queue), copy.deepcopy(piece_picked),
                                                         pick_position, (x, y), board_before_move, board_after_move))
                                move_navigator_counter = len(game_moves_queue)

                                ''' EVALUATE CHECKMATE i.e. opponent king is checkmated, and you win'''
                                game_over = king.is_opponent_checkmated(board, player_color)
                                if game_over:
                                    player_color_full = 'White' if player_color == 'w' else 'Black'
                                    game_message = 'Checkmate!! ' + player_color_full + ' won.'
                                    # running = not king.is_opponent_checkmated(board, player_color)  # exit the program

                                ''' TOGGLE PLAYER COLOR '''
                                player_color = 'b' if player_color == 'w' else 'w'  # toggle player color

                                ''' Highlight opponent's King if it is under check '''
                                if king.is_under_check(board, player_color):
                                    piece_list = chessboard.get_piece_list_by_name(board, 'k', color=player_color)
                                    piece = piece_list[0] if piece_list else None
                                    print('opponent', piece.color, 'king under check. highlighting king at', piece.loc)
                                    board_squares_to_highlight.append(piece.loc)
                            else:
                                piece_list = chessboard.get_piece_list_by_name(board, 'k', color=player_color)
                                piece = piece_list[0] if piece_list else None
                                print('Invalid move', (x, y), '. King at', piece.loc,
                                      'still under attack after the move')
                                board_squares_to_highlight.append(piece.loc)
                        else:
                            print('Invalid move', (x, y))

                        chessui.draw_board_on_screen(board, screen, game_message)
                        chessui.highlight_board_squares(screen, board_squares_to_highlight, highlight_color=constants.RED,
                                                        border_width=3)
                        action = 'PICK'
                        is_human_turn = True if (player_color == 'w' and white_player == 'human') or \
                                                (player_color == 'b' and black_player == 'human') else False
                elif is_human_turn and pawn_promotion_flag:
                    print('inside human turn and pawn promotion flag is TRUE, and old player_color=', player_color)
                    # still on the old player turn, so toggle color
                    promotion_piece = get_pawn_promotion_piece(cursor_pos, player_color, pawn_promotion_loc)
                    print('promotion_piece for color', player_color, '=', promotion_piece.name,
                          'piece color~', promotion_piece.color, 'drop loc~', pawn_promotion_loc, 'pick_loc~',
                          pick_position)

                    ''' MAKING PROMOTION MOVE '''
                    board_before_move = copy.deepcopy(board)
                    chessmove.make_move(board, promotion_piece, drop_position=pawn_promotion_loc)
                    board_after_move = copy.deepcopy(board)

                    ''' UPDATING GAME MOVES LIST FOR PROMOTION MOVE'''
                    ''' (move_count, piece_moved, pick_pos, drop_pos, board_before, board_after) '''
                    # game_moves_queue = game_moves_queue[:-1]  # slice to remove last element (which was pawn move)
                    game_moves_queue.append((len(game_moves_queue), copy.deepcopy(promotion_piece),
                                             pick_position, (x, y), board_before_move, board_after_move))
                    move_navigator_counter = len(game_moves_queue)

                    ''' EVALUATE CHECKMATE i.e. opponent king is checkmated, and you win FOR PROMOTION MOVE'''
                    game_over = king.is_opponent_checkmated(board, player_color)
                    if game_over:
                        player_color_full = 'White' if player_color == 'w' else 'Black'
                        game_message = 'Checkmate!! ' + player_color_full + ' won.'
                        # running = not king.is_opponent_checkmated(board, player_color)  # exit the program

                    ''' TOGGLE PLAYER COLOR FOR PROMOTION MOVE'''
                    player_color = 'b' if player_color == 'w' else 'w'  # toggle player color

                    ''' Highlight opponent's King if it is under check FOR PROMOTION MOVE'''
                    board_squares_to_highlight = []
                    if king.is_under_check(board, player_color):
                        piece_list = chessboard.get_piece_list_by_name(board, 'k', color=player_color)
                        piece = piece_list[0] if piece_list else None
                        print('opponent', piece.color, 'king under check. highlighting king at', piece.loc)
                        board_squares_to_highlight.append(piece.loc)

                    chessui.draw_board_on_screen(board, screen, game_message)
                    chessui.highlight_board_squares(screen, board_squares_to_highlight, highlight_color=constants.RED,
                                                    border_width=3)
                    chessui.draw_user_panels_on_screen(screen)  # restore the bottom panel

                    action = 'PICK'
                    pawn_promotion_flag = False
                    pawn_promotion_loc = None
                    is_human_turn = True if (player_color == 'w' and white_player == 'human') or \
                                            (player_color == 'b' and black_player == 'human') else False
                    print('inside human turn and pawn promotion flag is TRUE, and player_color at the end =',
                          player_color)

                else:
                    pass

            elif not is_human_turn:
                fen = chessboard.get_fen_from_board(board, player_color, en_passant_square, half_moves=half_moves,
                                                    full_moves=len(game_moves_queue) // 2)
                print('it is computer\'s turn as', player_color, ' and fen=', fen)
                best_move = evaluate.get_current_position_score(fen)
                pygame.time.delay(1000)
                print('best move: ', best_move)
                if len(best_move) != 4:
                    print('can\'t make this move. ', best_move, 'exiting')
                    continue
                pick_position = chess_notation_inverse[best_move[0:2]]
                drop_position = chess_notation_inverse[best_move[2:4]]
                computer_piece = chessboard.get_piece_by_location(board, pick_position, player_color)
                castle_type = king.get_castling_type(computer_piece, drop_position)

                print('make_move: Computer selected', computer_piece.name, 'from', pick_position, 'and dropping at',
                      drop_position)
                ''' Get en-passant square for pawn capture evaluation and fen'''
                en_passant_square = pawn.get_enpassant_square(computer_piece, drop_position)

                ''' Check if this move is a pawn advance or capture'''
                if chessmove.is_capture_or_pawn_advance(board, computer_piece, drop_position):
                    half_moves = 0
                else:
                    half_moves += 1

                ''' MAKING COMPUTER MOVE '''
                board_before_move = copy.deepcopy(board)
                chessmove.make_move(board, computer_piece, drop_position)
                board_after_move = copy.deepcopy(board)

                ''' UPDATING GAME MOVES LIST (move_count, piece_moved, pick_pos, drop_pos) '''
                game_moves_queue.append((len(game_moves_queue), copy.deepcopy(computer_piece),
                                         pick_position, drop_position, board_before_move, board_after_move))
                move_navigator_counter = len(game_moves_queue)

                ''' TOGGLE PLAYER COLOR '''
                player_color = 'b' if player_color == 'w' else 'w'  # toggle player color

                ''' Highlight opponent's King if it is under check '''
                if king.is_under_check(board, player_color):
                    piece_list = chessboard.get_piece_list_by_name(board, 'k', color=player_color)
                    piece = piece_list[0] if piece_list else None
                    print('opponent', piece.color, 'king under check. highlighting king at', piece.loc)
                    chessui.highlight_danger_squares(screen, [piece.loc])

                is_human_turn = True if (player_color == 'w' and white_player == 'human') or \
                                        (player_color == 'b' and black_player == 'human') else False
                chessui.draw_board_on_screen(board, screen, game_message)

            elif event.type == pygame.MOUSEBUTTONUP:
                pass

            elif event.type == pygame.KEYDOWN:
                #  left or up key pressed
                if event.key == pygame.K_LEFT or event.key == pygame.K_UP:
                    if move_navigator_counter > 0:
                        last_navigated_game_move = game_moves_queue[move_navigator_counter - 1]
                        move_navigator_counter -= 1
                        print('move counter=', move_navigator_counter, 'navigating down to move #',
                              last_navigated_game_move)
                        chessui.draw_board_on_screen(last_navigated_game_move[4], screen, game_message)
                    else:
                        print('at the first game move')

                #  right or down key pressed
                if event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN:
                    if move_navigator_counter < len(game_moves_queue) - 1:
                        last_navigated_game_move = game_moves_queue[move_navigator_counter + 1]
                        move_navigator_counter += 1
                        print('move counter=', move_navigator_counter, 'navigating up to move #',
                              last_navigated_game_move)
                        chessui.draw_board_on_screen(last_navigated_game_move[4], screen, game_message)
                    else:
                        print('at the last game move')
                        if last_navigated_game_move is not None and type(last_navigated_game_move) == tuple:
                            chessui.draw_board_on_screen(last_navigated_game_move[5], screen,
                                                         game_message)  # show final board position
                            move_navigator_counter = len(game_moves_queue)

            pygame.display.update()


def get_pawn_promotion_piece(cursor_pos, color, drop_pos):
    piece_name = ''
    print('inside get_pawn_promotion_piece')
    print('cursor position when clicked = ', cursor_pos)
    cursor_x, cursor_y = cursor_pos
    y_gap = 20
    if 3 * constants.WIDTH / 8 <= cursor_x <= 4 * constants.WIDTH / 8 + 10 and \
            8.05 * constants.WIDTH / 8 <= cursor_y < 8.05 * constants.WIDTH / 8 + y_gap:
        # print('Queen selected')
        piece_name = 'Q' if color == 'w' else 'q'

    if 3 * constants.WIDTH / 8 <= cursor_x <= 4 * constants.WIDTH / 8 + 10 and \
            8.05 * constants.WIDTH / 8 + y_gap <= cursor_y < 8.05 * constants.WIDTH / 8 + y_gap * 2:
        # print('Rook selected')
        piece_name = 'R' if color == 'w' else 'r'

    if 3 * constants.WIDTH / 8 <= cursor_x <= 4 * constants.WIDTH / 8 + 10 and \
            8.05 * constants.WIDTH / 8 + y_gap * 2 <= cursor_y < 8.05 * constants.WIDTH / 8 + y_gap * 3:
        # print('Bishop selected')
        piece_name = 'B' if color == 'w' else 'b'

    if 3 * constants.WIDTH / 8 <= cursor_x <= 4 * constants.WIDTH / 8 + 10 and \
            8.05 * constants.WIDTH / 8 + y_gap * 3 <= cursor_y < 8.05 * constants.WIDTH / 8 + y_gap * 4:
        # print('Knight selected')
        piece_name = 'N' if color == 'w' else 'n'

    promotion_piece = Piece(color, piece_name, './images/default/' + color + '/' + piece_name + '.png', drop_pos)

    return promotion_piece


main()
