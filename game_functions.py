# game_functions.py

import pygame
from random import randint

def set_difficulty_clues(difficulty):
    """Set the number of clues based on the difficulty level."""
    if difficulty == 'easy':
        return randint(36, 49)
    elif difficulty == 'medium':
        return randint(32, 35)
    elif difficulty == 'hard':
        return randint(28, 31)
    else:
        raise ValueError("Unknown difficulty level")


def initialize_grid():
    """Create and return a valid initial Sudoku grid."""
    return [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [7, 8, 9, 1, 2, 3, 4, 5, 6],
        [2, 3, 4, 5, 6, 7, 8, 9, 1],
        [5, 6, 7, 8, 9, 1, 2, 3, 4],
        [8, 9, 1, 2, 3, 4, 5, 6, 7],
        [3, 4, 5, 6, 7, 8, 9, 1, 2],
        [6, 7, 8, 9, 1, 2, 3, 4, 5],
        [9, 1, 2, 3, 4, 5, 6, 7, 8]
    ]

def swap_rows_within_blocks(sudoku_grid):
    """Randomly swap rows within each 3-row block in the Sudoku grid."""
    low, high = 0, 2
    for _ in range(3):  # Three blocks of rows
        row1, row2 = randint(low, high), randint(low, high)
        while row1 == row2:
            row2 = randint(low, high)  # Ensure row1 and row2 are different
        sudoku_grid[row1], sudoku_grid[row2] = sudoku_grid[row2], sudoku_grid[row1]
        low += 3
        high += 3

def swap_columns_within_blocks(sudoku_grid):
    """Randomly swap columns within each 3-column block in the Sudoku grid."""
    low, high = 0, 2
    for _ in range(3):  # Three blocks of columns
        col1, col2 = randint(low, high), randint(low, high)
        while col1 == col2:
            col2 = randint(low, high)  # Ensure col1 and col2 are different
        for row in sudoku_grid:
            row[col1], row[col2] = row[col2], row[col1]
        low += 3
        high += 3

def remove_cells_for_clues(sudoku_grid, clues):
    """Remove cells to leave the desired number of clues in the grid."""
    cells_to_remove = 81 - clues
    empty_cells = set()
    while cells_to_remove > 0:
        x, y = randint(0, 8), randint(0, 8)
        if (y, x) not in empty_cells:  # Only remove if not already empty
            sudoku_grid[y][x] = 0
            empty_cells.add((y, x))
            cells_to_remove -= 1

def create_mat(difficulty):
    """Generate a Sudoku grid with the specified difficulty."""
    clues = set_difficulty_clues(difficulty)
    sudoku_grid = initialize_grid()
    swap_rows_within_blocks(sudoku_grid)
    swap_columns_within_blocks(sudoku_grid)
    key = [row[:] for row in sudoku_grid]
    remove_cells_for_clues(sudoku_grid, clues)

    return sudoku_grid, key


def handle_number_input(key, selected_cell, mat, default_mat, mistakes, ans, score):
    """Handle key input for number entry in the Sudoku board."""
    if selected_cell:
        row, col = selected_cell
        if default_mat[row][col] == 0:  # Only allow input in empty cells
            if pygame.K_1 <= key <= pygame.K_9:
                entered_number = key - pygame.K_0
                mat[row][col] = entered_number

                # Check if the entry is correct
                if entered_number == ans[row][col]:  # Correct position
                    score[0] += 45  # Add 45 points to the score
                else:
                    # Deduct 5 points for a mistake, but ensure score doesn't go below 0
                    score[0] -= 5
                    score[0] = max(0, score[0])  # Ensure score doesn't go negative
                    mistakes[0] += 1  # Increment mistakes for incorrect entry
            elif key == pygame.K_BACKSPACE or key == pygame.K_DELETE:
                mat[row][col] = 0  # Allow clearing the cell without checking if it's already 0


def game_state(tries, mat):
    """Check if the game is won or lost."""
    if tries[0] >= 3:
        return 'LOST'
    
    # Check if the board is fully and correctly filled
    for row in mat:
        if 0 in row:  # If there are still empty cells, the game isn't won
            return 'playing'
    
    return 'WON'


def hint(ans, mat, default, hints):
    if hints[0] <= 0:
        return
    x = randint(0,8)
    y = randint(0,8)

    while mat[x][y] != 0:
        x = randint(0,8)
        y = randint(0,8)

    mat[x][y] = ans[x][y]
    default[x][y] = ans[x][y]
    hints[0] -= 1


def solve():
    return
