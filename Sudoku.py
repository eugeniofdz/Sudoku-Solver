# Sudoku.py

import pygame
import sys
from game_functions import create_mat, handle_number_input, game_state, solve, hint
from rendering import screen, BACKGROUND_COLOR, WINDOW_WIDTH, GRID_WIDTH, draw_grid, display_score, load_fonts, loading_screen, offset_x, offset_y, CELL_SIZE, timer, bottom_numbers, num_counter, game_over_screen, draw_button

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Sudoku Game")
title_surface = load_fonts()

def initialize_game():
    """Set up game variables for a new game."""
    difficulty = loading_screen()
    mat, ans = create_mat(difficulty)
    default_mat = [row[:] for row in mat]
    selected_cell = None
    mistakes = [0]
    score = [0]
    hints = [3]
    start_ticks = pygame.time.get_ticks()
    return mat, ans, default_mat, selected_cell, mistakes, start_ticks, score, hints

def main():
    mat, ans, default_mat, selected_cell, mistakes, start_ticks, score, hints = initialize_game()
    running = True

    # Define button rectangles for hint and solve
    hint_button = pygame.Rect(offset_x + 25, offset_y + GRID_WIDTH + 50, 150, 50)
    solve_button = pygame.Rect(offset_x + GRID_WIDTH - 175, offset_y + GRID_WIDTH + 50, 150, 50)

    while running:
        # Check game state
        state = game_state(mistakes, mat)
        if state in ['LOST', 'WON']:
            if game_over_screen(state, start_ticks, score):
                mat, ans, default_mat, selected_cell, mistakes, start_ticks, score, hints = initialize_game()
            else:
                break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # Check if click is on hint or solve buttons
                if hint_button.collidepoint(x, y):
                    hint(ans, mat, default_mat, hints)
                elif solve_button.collidepoint(x, y):
                    solve()  # Call the solve function here
                # Otherwise, check if it's within the grid
                elif offset_x <= x < offset_x + GRID_WIDTH and offset_y <= y < offset_y + GRID_WIDTH:
                    row = (y - offset_y) // CELL_SIZE
                    col = (x - offset_x) // CELL_SIZE
                    selected_cell = (row, col)
            elif event.type == pygame.KEYDOWN:
                handle_number_input(event.key, selected_cell, mat, default_mat, mistakes, ans, score)

        # Draw everything on the screen
        screen.fill(BACKGROUND_COLOR)
        screen.blit(title_surface, ((WINDOW_WIDTH - title_surface.get_width()) // 2, 0))
        time = timer(start_ticks)
        display_score(score)
        bottom_numbers(num_counter(mat))
        draw_grid(mat, selected_cell, ans)

        # Draw buttons on the screen
        draw_button("Hint", hint_button, (90, 123, 192))
        draw_button("Solve", solve_button, (90, 123, 192))

        pygame.display.flip()

if __name__ == "__main__":
    main()
