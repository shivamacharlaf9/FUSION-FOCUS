import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Fusion Focus')

# Set up the clock for controlling the frame rate
timer = pygame.time.Clock()
fps = 60

# Set up fonts
font = pygame.font.Font('freesansbold.ttf', 24)

# Color library for the game
colors = {
    0: (204, 192, 179),
    1: (238, 228, 218),
    2: (237, 224, 200),
    3: (242, 177, 121),
    4: (245, 149, 99),
    5: (246, 124, 95),
    6: (246, 94, 59),
    7: (237, 207, 114),
    8: (237, 204, 97),
    9: (237, 200, 80),
    10: (237, 197, 63),
    11: (237, 194, 46),
    'light text': (249, 246, 242),
    'dark text': (119, 110, 101),
    'other': (0, 0, 0),
    'bg': (187, 173, 160)
}

# Game variables
board_values = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
spawn_new = True
init_count = 0
direction = ''
score = 0

try:
    with open('high_score', 'r') as file:
        init_high_str = file.readline().strip()
        init_high = int(init_high_str) if init_high_str else 0
except (ValueError, FileNotFoundError):
    init_high = 0

high_score = init_high

# Draw "Game Over" and restart text
def draw_over():
    pygame.draw.rect(screen, 'black', [50, 50, 300, 100], 0, 10)
    game_over_text1 = font.render('Game Over!', True, 'white')
    game_over_text2 = font.render('Press Enter to Restart', True, 'white')
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (70, 105))

# Handle player movement
def take_turn(direc, board):
    global score
    merged = [[False for _ in range(4)] for _ in range(4)]

    if direc == 'UP':
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if i - shift - 1 >= 0 and board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] and not merged[i - shift - 1][j]:
                        board[i - shift - 1][j] += 1
                        score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True

    elif direc == 'RIGHT':
        for i in range(4):
            for j in range(3, -1, -1):  # Start from the right
                shift = 0
                if j < 3:
                    for q in range(j + 1, 4):
                        if board[i][q] == 0:
                            shift += 1
                    if shift > 0:
                        board[i][j + shift] = board[i][j]
                        board[i][j] = 0
                    if j + shift + 1 <= 3 and board[i][j + shift + 1] == board[i][j + shift] and not merged[i][j + shift] and not merged[i][j + shift + 1]:
                        board[i][j + shift + 1] += 1
                        score += board[i][j + shift + 1]
                        board[i][j + shift] = 0
                        merged[i][j + shift + 1] = True

    elif direc == 'DOWN':
        for i in range(3, -1, -1):  # Start from the bottom
            for j in range(4):
                shift = 0
                if i < 3:
                    for q in range(i + 1, 4):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i + shift][j] = board[i][j]
                        board[i][j] = 0
                    if i + shift + 1 <= 3 and board[i + shift + 1][j] == board[i + shift][j] and not merged[i + shift][j] and not merged[i + shift + 1][j]:
                        board[i + shift + 1][j] += 1
                        score += board[i + shift + 1][j]
                        board[i + shift][j] = 0
                        merged[i + shift + 1][j] = True

    elif direc == 'LEFT':
        for i in range(4):
            for j in range(4):
                shift = 0
                if j > 0:
                    for q in range(j):
                        if board[i][q] == 0:
                            shift += 1
                    if shift > 0:
                        board[i][j - shift] = board[i][j]
                        board[i][j] = 0
                    if j - shift - 1 >= 0 and board[i][j - shift - 1] == board[i][j - shift] and not merged[i][j - shift] and not merged[i][j - shift - 1]:
                        board[i][j - shift - 1] += 1
                        score += board[i][j - shift - 1]
                        board[i][j - shift] = 0
                        merged[i][j - shift - 1] = True
    
    return board

# Spawn new pieces
def new_pieces(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 2
            else:
                board[row][col] = 1
    if count < 1:
        full = True
    return board, full

# Draw the background for the board
def draw_board():
    pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)
    score_text = font.render(f'Score: {score}', True, 'black')
    high_score_text = font.render(f'High Score: {high_score}', True, 'black')
    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 450))

# Draw the tiles on the board
def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 4:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 11:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font_size = 48 - (5 * value_len)
                value_font = pygame.font.Font('freesansbold.ttf', font_size)
                value_text = value_font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                screen.blit(value_text, text_rect)
            pygame.draw.rect(screen, 'black', [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)

# Main game loop
run = True
while run:
    timer.tick(fps)
    screen.fill('gray')
    draw_board()
    draw_pieces(board_values)
    
    if spawn_new or init_count < 1:
        board_values, game_over = new_pieces(board_values)
        spawn_new = False
        init_count += 1
    
    if direction != '':
        board_values = take_turn(direction, board_values)
        direction = ''
        spawn_new = True
    
    if game_over:
        draw_over()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                direction = 'UP'
            if event.key == pygame.K_RIGHT:
                direction = 'RIGHT'
            if event.key == pygame.K_DOWN:
                direction = 'DOWN'
            if event.key == pygame.K_LEFT:
                direction = 'LEFT'
            if event.key == pygame.K_RETURN:
                board_values = [[0 for _ in range(4)] for _ in range(4)]
                spawn_new = True
                init_count = 0
                score = 0
                direction = ''
                game_over = False

    if score > high_score:
        high_score = score

    pygame.display.flip()

pygame.quit()
