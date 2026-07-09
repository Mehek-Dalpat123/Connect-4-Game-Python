import pygame
import sys
import math

pygame.init()

# Board settings
ROW_COUNT = 6
COLUMN_COUNT = 7

SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)

WIDTH = COLUMN_COUNT * SQUARESIZE
HEIGHT = (ROW_COUNT + 1) * SQUARESIZE
SIZE = (WIDTH, HEIGHT)
# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Connect 4")
myfont = pygame.font.SysFont("monospace", 50)

board = [[0 for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]
turn = 0
def draw_board():
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(
                screen,
                BLUE,
                (c * SQUARESIZE, (r + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE),
            )

            color = BLACK
            if board[r][c] == 1:
                color = RED
            elif board[r][c] == 2:
                color = YELLOW

            pygame.draw.circle(
                screen,
                color,
                (
                    int(c * SQUARESIZE + SQUARESIZE / 2),
                    int((r + 1) * SQUARESIZE + SQUARESIZE / 2),
                ),
                RADIUS,
            )

    pygame.display.update()


def get_next_open_row(col):
    for r in range(ROW_COUNT - 1, -1, -1):
        if board[r][col] == 0:
            return r
    return None


def drop_piece(row, col, piece):
    board[row][col] = piece
    draw_board()
def winning_move(piece):

    # Horizontal
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Positive diagonal (/)
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Negative diagonal (\)
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    return False

def reset_board():
    global board, turn
    board = [[0 for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]
    turn = 0
    draw_board()

draw_board()

running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))

            if turn == 0:
                pygame.draw.circle(screen, RED, (event.pos[0], SQUARESIZE // 2), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (event.pos[0], SQUARESIZE // 2), RADIUS)

            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))

            col = event.pos[0] // SQUARESIZE

            if 0 <= col < COLUMN_COUNT:
                row = get_next_open_row(col)

                if row is not None:
                    if turn == 0:
                        drop_piece(row, col, 1)

                        if winning_move(1):
                            label = myfont.render("Player 1 Wins!", True, RED)
                            screen.blit(label, (40, 10))
                            pygame.display.update()
                            pygame.time.wait(3000)
                            reset_board()

                        turn = 1

                    else:
                        drop_piece(row, col, 2)

                        if winning_move(2):
                            label = myfont.render("Player 2 Wins!", True, YELLOW)
                            screen.blit(label, (40, 10))
                            pygame.display.update()
                            pygame.time.wait(3000)
                            reset_board()

                        turn = 0

                    draw_board()

pygame.quit()
sys.exit()