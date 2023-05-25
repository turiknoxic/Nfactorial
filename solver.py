def solve_sudoku(board):
    return solve(board)


def solve(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                for digit in range(1, 10):
                    if is_valid(board, i, j, digit):
                        board[i][j] = digit

                        if solve(board):
                            return True
                        else:
                            board[i][j] = 0

                return False

    return True


def is_valid(board, row, col, number):
    for i in range(9):
        if board[i][col] == number:
            return False

        if board[row][i] == number:
            return False
        if board[int(3 * int(row / 3) + i / 3)][
                int(3 * int(col / 3) + i % 3)] == number:
            return False

    return True


grid = [[0, 0, 0, 7, 1, 0, 0, 6, 0],
        [7, 0, 4, 9, 0, 0, 0, 0, 0],
        [0, 0, 3, 8, 0, 5, 4, 0, 0],
        [0, 0, 0, 6, 0, 0, 2, 5, 0],
        [0, 0, 8, 0, 7, 1, 0, 3, 0],
        [0, 0, 9, 5, 8, 0, 1, 0, 0],
        [0, 0, 0, 0, 5, 0, 7, 0, 4],
        [0, 0, 5, 0, 0, 0, 0, 0, 3],
        [1, 0, 7, 3, 6, 9, 0, 0, 0]]

print(solve_sudoku(grid))