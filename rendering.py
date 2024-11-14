# rendering.py

import pygame
import sys

from game_functions import solve, hint

# Window settings and offsets
WINDOW_WIDTH, WINDOW_HEIGHT = 500, 600
GRID_SIZE, GRID_WIDTH = 9, 405
CELL_SIZE = GRID_WIDTH // GRID_SIZE
offset_x = (WINDOW_WIDTH - GRID_WIDTH) // 2
offset_y = (WINDOW_HEIGHT - GRID_WIDTH) // 3

# Screen setup
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Colors
BACKGROUND_COLOR = (250, 250, 250)
LINE_COLOR = (0, 0, 0)
THICK_LINE_COLOR = (0, 0, 0)
HIGHLIGHT_COLOR = (170, 215, 245)
WRONG_HIGHLIGHT_COLOR = (245, 130, 130)
IDENTICAL_HIGHLIGHT_COLOR = (135, 206, 235)
LINE_HIGHLIGHT_COLOR = (220, 235, 245)
TITLE_COLOR = (0, 0, 0)
BOTTOM_GRAY = (150, 150, 150)
BOTTOM_BLUE = (100, 150, 255)

def load_fonts():
    """Loads fonts after pygame.init()"""
    global font, title_font, title_surface, button_font, little_font
    font_path = "Sudoku/assets/Poppins-Regular.ttf"
    font = pygame.font.Font(font_path, 25)
    title_font = pygame.font.Font(font_path, 36)
    title_text = "SUDOKU"
    title_surface = title_font.render(title_text, True, TITLE_COLOR)
    button_font = pygame.font.Font(font_path, 30)
    little_font = pygame.font.Font(None, 28)
    return title_surface

def draw_button(text, rect, color):
    pygame.draw.rect(screen, color, rect)
    text_surf = button_font.render(text, True, (250, 250, 250))
    text_rect = text_surf.get_rect(center= rect.center)
    screen.blit(text_surf, text_rect)

def loading_screen():
    color = 90, 123, 192

    easy_button = pygame.Rect(150, 200, 200, 50)
    medium_button = pygame.Rect(150, 300, 200, 50)
    hard_button = pygame.Rect(150, 400, 200, 50)

    while True:
        screen.fill(BACKGROUND_COLOR)
        screen.blit(title_surface, ((WINDOW_WIDTH - title_surface.get_width()) // 2, 50))
        # Draw buttons
        draw_button("Easy", easy_button, color)
        draw_button("Medium", medium_button, color)
        draw_button("Hard", hard_button, color)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.collidepoint(event.pos):
                    return 'easy'
                elif medium_button.collidepoint(event.pos):
                    return 'medium'
                elif hard_button.collidepoint(event.pos):
                    return 'hard'
        pygame.display.flip()

def draw_grid(mat, selected_cell, ans):
    draw_help(selected_cell, mat, ans)
    draw_selected_cell(selected_cell, ans, mat)
    draw_lines()
    draw_numbers(mat)

def draw_help(selected_cell, mat, ans):
    if selected_cell:
        row, col = selected_cell
        # Draw vertical and horizontal helper lines
        for i in range(9):
            pygame.draw.rect(
                screen, LINE_HIGHLIGHT_COLOR, 
                (offset_x + col * CELL_SIZE, offset_y + i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )
            pygame.draw.rect(
                screen, LINE_HIGHLIGHT_COLOR, 
                (offset_x + i * CELL_SIZE, offset_y + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )
        # Highlight selected 3x3 box
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                pygame.draw.rect(
                    screen, LINE_HIGHLIGHT_COLOR, 
                    (offset_x + (start_col + j) * CELL_SIZE, offset_y + (start_row + i) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )
        # Highlight identical numbers and wrong numbers
        for i in range(9):
            for j in range(9):
                if mat[i][j] != 0 and mat[i][j] == mat[row][col]:
                    pygame.draw.rect(
                        screen, IDENTICAL_HIGHLIGHT_COLOR, 
                        (offset_x + j * CELL_SIZE, offset_y + i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    )
                if mat[i][j] != 0 and mat[i][j] != ans[i][j]:
                    pygame.draw.rect(
                        screen, WRONG_HIGHLIGHT_COLOR, 
                        (offset_x + j * CELL_SIZE, offset_y + i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    )

def draw_lines():
    for i in range(GRID_SIZE + 1):
        line_thickness = 3 if i % 3 == 0 else 1
        color = THICK_LINE_COLOR if i % 3 == 0 else LINE_COLOR

        pygame.draw.line(
            screen, color,
            (offset_x + i * CELL_SIZE, offset_y),
            (offset_x + i * CELL_SIZE, offset_y + GRID_WIDTH),
            line_thickness
        )
        pygame.draw.line(
            screen, color,
            (offset_x, offset_y + i * CELL_SIZE),
            (offset_x + GRID_WIDTH, offset_y + i * CELL_SIZE),
            line_thickness
        )

def draw_numbers(mat):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            num = mat[row][col]
            if num != 0:
                text_surface = font.render(str(num), True, (0, 0, 0))
                text_x = offset_x + (col * CELL_SIZE) + (CELL_SIZE - text_surface.get_width()) // 2
                text_y = offset_y + (row * CELL_SIZE) + (CELL_SIZE - text_surface.get_height()) // 2
                screen.blit(text_surface, (text_x, text_y))

def draw_selected_cell(selected_cell, ans, mat):
    if selected_cell:
        row, col = selected_cell
        color = WRONG_HIGHLIGHT_COLOR if ans[row][col] != mat[row][col] and mat[row][col] != 0 else HIGHLIGHT_COLOR
        pygame.draw.rect(
            screen, color, 
            (offset_x + col * CELL_SIZE, offset_y + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )

def timer(time):
    # Calculate and display the timer
        elapsed_ticks = pygame.time.get_ticks() - time
        minutes = elapsed_ticks // 60000  # Convert ticks to minutes
        seconds = (elapsed_ticks % 60000) // 1000  # Convert ticks to seconds
        timer_text = f"{minutes:02}:{seconds:02}"
        timer_surface = little_font.render(timer_text, True, (0, 0, 0))  # Black color
        # Position timer in the upper-right corner of the grid
        timer_x = offset_x + GRID_WIDTH - timer_surface.get_width()  # Align to the right edge of the grid
        timer_y = offset_y - 20
        screen.blit(timer_surface, (timer_x, timer_y))
        return seconds

def display_score(score):
    """Render the score in the top left corner of the screen."""
    score_surface = little_font.render(f"Score: {score[0]}", True, (0, 0, 0))  # Black color
    score_x = offset_x
    score_y = offset_y - 20
    screen.blit(score_surface, (score_x, score_y))

def num_counter(mat):
    nums = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0
    }
    for row in range(9):
        for num in mat[row]:
            if num in nums:
                nums[num] += 1
    return nums

def bottom_numbers(nums):
    for num in nums:
        # Choose color based on the condition
        color = BOTTOM_GRAY if nums[num] == 9 else BOTTOM_BLUE
        
        # Render the text surface
        text_surface = font.render(str(num), True, color)
        
        # Calculate x position to center each number under each column
        text_x = offset_x + ((num - 1) * CELL_SIZE) + (CELL_SIZE - text_surface.get_width()) // 2
        
        # Position y below the grid
        text_y = offset_y + GRID_WIDTH + 10  # 10 pixels below the bottom edge of the grid
        
        # Draw the number on the screen
        screen.blit(text_surface, (text_x, text_y))


def game_over_screen(result, time, score):
    """Display the game over screen with the result and options to exit or start a new game."""
    color = 90, 123, 192
    elapsed_ticks = pygame.time.get_ticks() - time
    minutes = elapsed_ticks // 60000  # Convert ticks to minutes
    seconds = (elapsed_ticks % 60000) // 1000  # Convert ticks to seconds
    timer_text = f"{minutes:02}:{seconds:02}"

    # Render the result text ("Game Over" or "You Won!")
    result_font = pygame.font.Font(None, 60)
    result_surface = result_font.render(result, True, TITLE_COLOR)
    result_x = (WINDOW_WIDTH - result_surface.get_width()) // 2
    result_y = offset_y

    # Render the score and timer text
    info_font = pygame.font.Font(None, 40)
    score_text = f"Score: {score[0]}"
    timer_surface = info_font.render(f"Time: {timer_text}", True, TITLE_COLOR)
    score_surface = info_font.render(score_text, True, TITLE_COLOR)

    # Calculate positions for score and timer below the result
    score_x = (WINDOW_WIDTH - score_surface.get_width()) // 2
    score_y = result_y + 70  # Position below the result
    timer_x = (WINDOW_WIDTH - timer_surface.get_width()) // 2
    timer_y = score_y + 40  # Position below the score

    # Create buttons
    exit_button = pygame.Rect(150, 250, 200, 50)
    new_game_button = pygame.Rect(150, 350, 200, 50)

    while True:
        screen.fill(BACKGROUND_COLOR)
        screen.blit(result_surface, (result_x, result_y))
        screen.blit(score_surface, (score_x, score_y))
        screen.blit(timer_surface, (timer_x, timer_y))

        # Draw buttons
        draw_button("Exit", exit_button, color)
        draw_button("New Game", new_game_button, color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    return False  # Exit the game
                elif new_game_button.collidepoint(event.pos):
                    return True  # Start a new game

        pygame.display.flip()