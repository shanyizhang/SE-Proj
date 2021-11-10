## ----------------------------------------
##   Software Engineering @ NYU
##   Course Project - Tetris Game
##   Ken S. Zhang & Qingyang Li
## ----------------------------------------


from config import *
import pygame


class UserInterface(object):
    def __init__(self, show_window=True):
        pygame.font.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags=0 if show_window else pygame.HIDDEN)
        pygame.display.set_caption('Tetris Game')

    def start(self):
        self.window.fill((0,0,0))
        self.draw_text_middle('Enter Username to Begin.', 60, (255, 255, 255))
        self.update()
    
    def update(self):
        pygame.display.update()

    def shutdown(self):
        pygame.display.quit()

    def draw_text_middle(self, text, size, color):
        font = pygame.font.SysFont('comicsans', size, bold=True)
        label = font.render(text, 1, color)
        self.window.blit(label, (TOP_LEFT_X + BOARD_WIDTH/2 - (label.get_width() / 2), TOP_LEFT_Y + BOARD_HEIGHT/2 - label.get_height()/2))

    def draw_grid(self):
        sx = TOP_LEFT_X
        sy = TOP_LEFT_Y
        for i in range(ROW):
            pygame.draw.line(self.window, (128,128,128), (sx, sy + i * BLOCK_SIZE), (sx + BOARD_WIDTH, sy + i * BLOCK_SIZE))  
            for j in range(COLUMN):
                pygame.draw.line(self.window, (128,128,128), (sx + j * BLOCK_SIZE, sy), (sx + j * BLOCK_SIZE, sy + BOARD_HEIGHT))  

    def draw_window(self, grid):
        self.window.fill((0,0,0))
        font = pygame.font.SysFont('comicsans', 60)
        label = font.render('TETRIS', 1, (255,255,255))
        self.window.blit(label, (TOP_LEFT_X + BOARD_WIDTH / 2 - (label.get_width() / 2), BLOCK_SIZE))
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(self.window, grid[i][j], (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
        self.draw_grid()
        pygame.draw.rect(self.window, (255, 0, 0), (TOP_LEFT_X, TOP_LEFT_Y, BOARD_WIDTH, BOARD_HEIGHT), 5)

    def draw_next_shape(self, shape):
        font = pygame.font.SysFont('comicsans', BLOCK_SIZE)
        label = font.render('Next Shape', 1, (255,255,255))
        sx = TOP_LEFT_X + BOARD_WIDTH + 50
        sy = TOP_LEFT_Y + BOARD_HEIGHT/2 - 100
        format = shape.shape[shape.rotation % len(shape.shape)]
        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(self.window, shape.color, (sx + j * BLOCK_SIZE, sy + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
        self.window.blit(label, (sx + 10, sy - BLOCK_SIZE))


class InputBox(object):
    def __init__(self, window):
        self.window = window
        self.rect = pygame.Rect(TOP_LEFT_X + BOARD_WIDTH/2, TOP_LEFT_Y + BOARD_HEIGHT/2 + 50, 140, 32)
        self.color = (255, 255, 255)
        self.text = ''
        self.txt_surface = pygame.font.Font(None, 32).render(self.text, True, self.color)
        self.complete = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.complete = True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.txt_surface = pygame.font.Font(None, 32).render(self.text, True, self.color)

    def update_display_text(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
        self.window.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))

    def draw_rect(self):
        pygame.draw.rect(self.window, self.color, self.rect, 2)

    def check_complete(self):
        return self.complete == True

    def dump_and_flush(self):
        text_temp = self.text
        self.text = ''
        self.complete = False
        self.txt_surface = pygame.font.Font(None, 32).render(self.text, True, self.color)
        return text_temp