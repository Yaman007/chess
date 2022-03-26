import pygame
import constants
from piece import Piece

pygame.init()

WIDTH = constants.WIDTH
button_h = WIDTH/16
button_w = WIDTH/8
button1_x, button1_y = 0.2 * WIDTH / 8, 8.25 * WIDTH / 8
button2_x, button2_y = 1.3 * WIDTH / 8, 8.25 * WIDTH / 8
button3_x, button3_y = 5.0 * WIDTH / 8, 8.25 * WIDTH / 8
button4_x, button4_y = 6 * WIDTH / 8, 8 * WIDTH / 8
button5_x, button5_y = 2.4 * WIDTH / 8, 8.25 * WIDTH / 8

text1_x, text1_y = int(0.35 * WIDTH / 8), int(8.38 * WIDTH / 8)
text2_x, text2_y = int(1.45 * WIDTH / 8), int(8.38 * WIDTH / 8)
text3_x, text3_y = int(5.15 * WIDTH / 8), int(8.38 * WIDTH / 8)
text4_x, text4_y = int(6.03 * WIDTH / 8), int(8.03 * WIDTH / 8)
message_x, message_y = int(6.03 * WIDTH / 8), int(8.20 * WIDTH / 8)
text5_x, text5_y = int(2.55 * WIDTH / 8), int(8.38 * WIDTH / 8)

font = pygame.font.Font(pygame.font.get_default_font(), 15)
large_font = pygame.font.Font(pygame.font.get_default_font(), 35)
medium_font = pygame.font.Font(pygame.font.get_default_font(), 25)
debug_font = pygame.font.Font(pygame.font.get_default_font(), 12)


def add_rectangle(screen, color, top_x, top_y, width, height, border=0):
    pygame.draw.rect(screen, constants.ACTIVE_BUTTON_COLOR, (top_x, top_y, width, height), border)


def add_text(screen, label, top_x, top_y, text_font, color=constants.ACTIVE_TEXT_COLOR):
    text_surface = text_font.render(label, True, color)
    screen.blit(text_surface, (top_x, top_y))


def draw_board_on_screen(board, screen, game_message=None, highlight_squares=None, highlight_color=constants.RED, highlight_border=2):
    for i in range(8):
        for j in range(8):
            color = constants.WHITE if (i + j) % 2 == 0 else constants.GREY  # even square i.e. WHITE
            pygame.draw.rect(screen, color, (i * WIDTH / 8, j * WIDTH / 8, WIDTH / 8, WIDTH / 8))
    for i in range(8):
        for j in range(8):
            piece_obj = board[i][j]
            if type(piece_obj) == Piece:
                surface = pygame.image.load(piece_obj.img)
                surface = pygame.transform.scale(surface, constants.PIECE_SIZE_SCALE)
                screen.blit(surface, (int(j * WIDTH / 8), int(i * WIDTH / 8)))

    # display key game messages
    if game_message is not None:
        add_text(screen, game_message, 2.5 * WIDTH / 8, 3.5 * WIDTH / 8, large_font, color=constants.BLUE)

    # highlight selected squares on the board
    if highlight_squares is not None:
        highlight_board_squares(screen, highlight_squares, highlight_color, highlight_border)


def draw_promotion_options_on_screen(screen, x_starting, y_starting, y_gap):
    add_text(screen, 'Queen', x_starting * constants.WIDTH / 8, (y_starting + y_gap * 0) * constants.WIDTH / 8, font,
                     color=constants.BLUE)
    add_text(screen, 'Rook', x_starting * constants.WIDTH / 8, (y_starting + y_gap * 1) * constants.WIDTH / 8, font,
                     color=constants.BLUE)
    add_text(screen, 'Bishop', x_starting * constants.WIDTH / 8, (y_starting + y_gap * 2) * constants.WIDTH / 8, font,
                     color=constants.BLUE)
    add_text(screen, 'Knight', x_starting * constants.WIDTH / 8, (y_starting + y_gap * 3) * constants.WIDTH / 8, font,
                     color=constants.BLUE)


def draw_user_panels_on_screen(screen):
    # draw black rectangle background first (0, 700) to (700, 800) i.e. (0, width) to (width, height)
    pygame.draw.rect(screen, constants.BLACK, (0, constants.WIDTH, constants.WIDTH, constants.HEIGHT-constants.WIDTH), 0)

    # rectangle definition: x from left, y from top, width, height, border
    pygame.draw.rect(screen, constants.ACTIVE_BUTTON_COLOR, (button1_x, button1_y, button_w, button_h), 0)
    add_text(screen, 'Previous', text1_x, text1_y, font, color=constants.ACTIVE_TEXT_COLOR)
    pygame.draw.rect(screen, constants.ACTIVE_BUTTON_COLOR, (button2_x, button2_y, button_w, button_h), 0)
    add_text(screen, '  Next  ', text2_x, text2_y, font, color=constants.ACTIVE_TEXT_COLOR)
    pygame.draw.rect(screen, constants.ACTIVE_BUTTON_COLOR, (button3_x, button3_y, button_w, button_h), 0)
    add_text(screen, '  Reset   ', text3_x, text3_y, font, color=constants.ACTIVE_TEXT_COLOR)

    pygame.draw.rect(screen, constants.SANDBOX_AREA_COLOR, (button4_x, button4_y, button_w*2, button_h*2), 0)
    add_text(screen, '  Debug Area   ', text4_x, text4_y, debug_font, color=constants.ACTIVE_TEXT_COLOR)

    pygame.draw.rect(screen, constants.ACTIVE_BUTTON_COLOR, (button5_x, button5_y, button_w, button_h/2), 0)
    add_text(screen, 'Human White', text5_x-7, text5_y-7, debug_font, color=constants.ACTIVE_TEXT_COLOR)

    pygame.draw.rect(screen, constants.ACTIVE_BUTTON_COLOR, (button5_x, button5_y+30, button_w, button_h/2), 0)
    add_text(screen, 'Human Black', text5_x-7, text5_y-7+30, debug_font, color=constants.ACTIVE_TEXT_COLOR)

    pygame.draw.rect(screen, constants.ACTIVE_BUTTON_COLOR, (button5_x + 100, button5_y, button_w, button_h/2), 0)
    add_text(screen, 'Human Both', text5_x-7+100, text5_y-7, debug_font, color=constants.ACTIVE_TEXT_COLOR)

    pygame.draw.rect(screen, constants.ACTIVE_BUTTON_COLOR, (button5_x + 100, button5_y+30, button_w, button_h/2), 0)
    add_text(screen, 'Human None', text5_x-7+100, text5_y-7+30, debug_font, color=constants.ACTIVE_TEXT_COLOR)


def draw_board_from_pieces(screen, pieces):
    for i in range(8):
        for j in range(8):
            color = constants.WHITE if (i + j) % 2 == 0 else constants.GREY  # even square i.e. WHITE
            pygame.draw.rect(screen, color, (i * WIDTH / 8, j * WIDTH / 8, WIDTH / 8, WIDTH / 8))
    for piece in pieces:
        i, j = piece.loc
        surface = pygame.image.load(piece.img)
        surface = pygame.transform.scale(surface, constants.PIECE_SIZE_SCALE)
        screen.blit(surface, (int(j * WIDTH / 8), int(i * WIDTH / 8)))
    return None


def highlight_move_squares(screen, move_squares, piece_picked):
    # overwrite any red circles with circle of cell background (Grey or White)
    (pick_i, pick_j) = piece_picked.loc
    cell_color = constants.WHITE if (pick_i + pick_j) % 2 == 0 else constants.GREY  # even square i.e. WHITE
    pygame.draw.circle(screen, cell_color, (pick_j * WIDTH / 8 + WIDTH / 16, pick_i * WIDTH / 8 + WIDTH / 16),
                       constants.MOVE_CIRCLE_RADIUS, constants.MOVE_CIRCLE_BORDER)

    for (i, j) in move_squares:
        # highlight available move squares with Dark Grey circle
        pygame.draw.circle(screen, constants.DARKGREY, (j * WIDTH / 8 + WIDTH / 16, i * WIDTH / 8 + WIDTH / 16),
                           constants.AVAILABLE_MOVE_CIRCLE_RADIUS, constants.AVAILABLE_MOVE_CIRCLE_BORDER)

        # highlight picked piece with Blue circle
        pygame.draw.circle(screen, constants.BLUE, (pick_j * WIDTH / 8 + WIDTH / 16, pick_i * WIDTH / 8 + WIDTH / 16), 10, 10)


def highlight_danger_squares(screen, danger_squares, highlight_color=constants.RED):
    for (i, j) in danger_squares:
        pygame.draw.circle(screen, highlight_color, (j * WIDTH / 8 + WIDTH / 16, i * WIDTH / 8 + WIDTH / 16), 20, 20)


def highlight_board_squares(screen, squares, highlight_color=constants.RED, border_width=0):
    for square in squares:
        i, j = square
        pygame.draw.rect(screen, highlight_color, (j * WIDTH / 8, i * WIDTH / 8, WIDTH / 8, WIDTH / 8), border_width)



