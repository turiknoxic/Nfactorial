import random
import pygame
import copy
from solver import solve_sudoku


DIFFICULTY = {'EASY': 30, 'MEDIUM': 50, 'HARD': 70}


def choose_difficulty(level):
    if level == 1:
        return DIFFICULTY['EASY']
    elif level == 2:
        return DIFFICULTY['MEDIUM']
    elif level == 3:
        return DIFFICULTY['HARD']


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color(255, 255, 255),
                                 (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                  self.cell_size,
                                  self.cell_size), 1)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def on_click(self, cell):
        pass

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)


class Sudoku(Board):
    def __init__(self, n):
        super().__init__(n, n)
        self.n = n
        self.board = [
            [((i * n + i // n + j) % (n * n) + 1) for j in range(n * n)]
            for i in range(n * n)]
        self.difficulty = DIFFICULTY['EASY']

    def transposing(self):
        """ Transposing the whole grid """
        self.board = list(map(list, zip(*self.board)))

    def swap_rows_small(self):
        """ Swap the two rows """
        area = random.randrange(0, self.n, 1)
        line1 = random.randrange(0, self.n, 1)
        # получение случайного района и случайной строки
        N1 = area * self.n + line1
        # номер 1 строки для обмена

        line2 = random.randrange(0, self.n, 1)
        # случайная строка, но не та же самая
        while (line1 == line2):
            line2 = random.randrange(0, self.n, 1)

        N2 = area * self.n + line2
        # номер 2 строки для обмена

        self.board[N1], self.board[N2] = self.board[N2], self.board[N1]

    def swap_colums_small(self):
        Sudoku.transposing(self)
        Sudoku.swap_rows_small(self)
        Sudoku.transposing(self)

    def swap_rows_area(self):
        """ Swap the two area horizon """
        area1 = random.randrange(0, self.n, 1)
        # получение случайного района

        area2 = random.randrange(0, self.n, 1)
        # ещё район, но не такой же самый
        while (area1 == area2):
            area2 = random.randrange(0, self.n, 1)

        for i in range(0, self.n):
            N1, N2 = area1 * self.n + i, area2 * self.n + i
            self.board[N1], self.board[N2] = self.board[N2], self.board[N1]

    def swap_colums_area(self):
        Sudoku.transposing(self)
        Sudoku.swap_rows_area(self)
        Sudoku.transposing(self)

    def mix(self, amt=100):
        mix_func = ['self.transposing()',
                    'self.swap_rows_small()',
                    'self.swap_colums_small()',
                    'self.swap_rows_area()',
                    'self.swap_colums_area()']
        for i in range(1, amt):
            id_func = random.randrange(0, len(mix_func), 1)
            eval(mix_func[id_func])

    # def on_click(self, cell):
    #     self.open_cell(cell)

    def render(self, screen):
        for y in range(len(self.board)):
            for x in range(len(self.board)):
                font = pygame.font.Font(None, self.cell_size)
                text = font.render(str(self.board[y][x]), True, (100, 255, 100))
                if self.board[y][x] != 0:
                    screen.blit(text, (x * self.cell_size + self.left + 3,
                                       y * self.cell_size + self.top + 3))
                pygame.draw.rect(screen, pygame.Color(255, 255, 255),
                                 (x * self.cell_size + self.left,
                                  y * self.cell_size + self.top,
                                  self.cell_size, self.cell_size), 1)

    def prepare_table(self):
        self.mix()
        self.complete_board = copy.deepcopy(self.board)

    def show_solution(self, screen):
        self.board = self.complete_board

    def delete_cells(self):
        complete = 0
        flook = [[0 for j in range(self.n * self.n)] for i in
                 range(self.n * self.n)]

        while complete < self.difficulty:
            i, j = random.randrange(0, self.n * self.n, 1),\
                random.randrange(0, self.n * self.n, 1)  # Выбираем
                                                         # случайную ячейку
            if flook[i][j] == 0:  # Если её не смотрели
                flook[i][j] = 1  # Посмотрим

                temp = self.board[i][j]
                self.board[i][j] = 0

                table_solution = copy.deepcopy(self.board)  # Скопируем доску

                has_solution = False
                if solve_sudoku(table_solution):
                    complete += 1
                    has_solution = True  # Проверяем, есть ли решения

                if not has_solution:  # если решения нет, то вернуть на место
                    self.board[i][j] = temp
                    complete -= 1


def main():
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
    FONT = pygame.font.SysFont('comicsans', 20)
    size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Судоку')
    clock = pygame.time.Clock()
    board = Sudoku(3)
    board.prepare_table()
    board.delete_cells()
    board.set_view(50, 50, 50)
    print(board.board)
    game_on = False
    ticks = 0
    running = True
    cells_set = False
    while running:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        if keys[pygame.K_SPACE] and game_on:
            board.show_solution(screen)
        if not game_on:  # если игра еще не запущена
            text = "Выберите режим: 1 - легкий / 2 - средний / 3 - сложный"
            show_text = FONT.render(text, True, pygame.Color('red'))
            screen.blit(show_text,
                        (SCREEN_WIDTH // 2 - show_text.get_width() // 2,
                         SCREEN_HEIGHT // 2 - show_text.get_height() // 2))
            pygame.display.update()
        if keys[pygame.K_1]:  # выбираем легкий режим
            # board.difficulty = choose_difficulty(1)
            game_on = True
        if keys[pygame.K_2]:  # выбираем средний режим
            # board.difficulty = choose_difficulty(2)
            game_on = True
        if keys[pygame.K_3]:  # выбираем сложный режим
            # board.difficulty = choose_difficulty(3)
            game_on = True
        if game_on:
            screen.fill((0, 0, 0))
            board.render(screen)

        pygame.display.flip()
        clock.tick(50)
        ticks += 1
    pygame.quit()

if __name__ == '__main__':
    main()
