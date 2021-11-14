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
        self.inputbox = InputBox(window=self.window)
        self.checkbox = CheckBoxArray(window=self.window, num=3, text=["Easy", "Medium", "Hard"])

    def start(self):
        self.window.fill((0,0,0))
        self.draw_text_middle('Enter Game Settings to Begin.', 60, (255, 255, 255))
        self.inputbox.update_inputbox()
        self.checkbox.update_checkbox_array()
        self.update()

    def update(self):
        pygame.display.update()

    def shutdown(self):
        pygame.display.quit()

    def draw_text_middle(self, text, size, color):
        font = pygame.font.SysFont('comicsans', size, bold=True)
        label = font.render(text, 1, color)
        self.window.blit(label, (TOP_LEFT_X + BOARD_WIDTH/2 - (label.get_width() / 2), TOP_LEFT_Y + BOARD_HEIGHT/2 - label.get_height()/2 - 100))

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
        self.rect = pygame.Rect(TOP_LEFT_X + BOARD_WIDTH/2, TOP_LEFT_Y + BOARD_HEIGHT/2 - 55, 140, 32)
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
            
    def update_display_text(self):
        self.txt_surface = pygame.font.Font(None, 32).render(self.text, True, self.color)
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
        self.window.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))

    def draw_rect(self):
        font = pygame.font.SysFont('comicsans', 40, bold=False)
        label = font.render('Username:', 1, (255, 255, 255))
        self.window.blit(label, (TOP_LEFT_X + BOARD_WIDTH/2 - 153, TOP_LEFT_Y + BOARD_HEIGHT/2 - 55))
        pygame.draw.rect(self.window, self.color, self.rect, 2)

    def update_inputbox(self):
        self.update_display_text()
        self.draw_rect()

    def check_complete(self):
        return self.complete == True

    def dump_and_flush(self):
        text_temp = self.text
        self.complete = False
        self.txt_surface = pygame.font.Font(None, 32).render(self.text, True, self.color)
        return text_temp

    
class CheckBox(object):
    def __init__(self, surface, x, y, color=(230, 230, 230), caption="", outline_color=(0, 0, 0),
                 check_color=(0, 0, 0), font_size=32, font_color=(255, 255, 255), text_offset=(40, 1)):
        self.surface = surface
        self.x = x
        self.y = y
        self.color = color
        self.caption = caption
        self.oc = outline_color
        self.cc = check_color
        self.fs = font_size
        self.fc = font_color
        self.to = text_offset
        # checkbox object
        self.checkbox_obj = pygame.Rect(self.x, self.y, 12, 12)
        self.checkbox_outline = self.checkbox_obj.copy()
        # variables to test the different states of the checkbox
        self.checked = False
        self.active = False
        self.unchecked = True
        self.click = False

    def _draw_button_text(self):
        self.font = pygame.font.Font(None, self.fs)
        self.font_surf = self.font.render(self.caption, True, self.fc)
        w, h = self.font.size(self.caption)
        self.font_pos = (self.x + 40 / 2 - w / 2 + self.to[0], self.y + 12 / 2 - h / 2 + self.to[1])
        self.surface.blit(self.font_surf, self.font_pos)

    def render_checkbox(self):
        if self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
            pygame.draw.circle(self.surface, self.cc, (self.x + 6, self.y + 6), 4)

        elif self.unchecked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
        self._draw_button_text()

    def _update(self, event_object):
        x, y = event_object.pos
        # self.x, self.y, 12, 12
        px, py, w, h = self.checkbox_obj  # getting check box dimensions
        if px < x < px + w and py < y < py + h:
            self.active = True
        else:
            self.active = False

    def _mouse_up(self):
            if self.active and not self.checked and self.click:
                self.checked = True
            elif self.checked:
                self.checked = False
                self.unchecked = True

            if self.click is True and self.active is False:
                if self.checked:
                    self.checked = True
                if self.unchecked:
                    self.unchecked = True
                self.active = False

    def handle_event(self, event_object):
        if event_object.type == pygame.MOUSEBUTTONDOWN:
            self.click = True
        if event_object.type == pygame.MOUSEBUTTONUP:
            self._mouse_up()
        if event_object.type == pygame.MOUSEMOTION:
            self._update(event_object)

    def is_checked(self):
        if self.checked is True:
            return True
        else:
            return False

    def is_unchecked(self):
        if self.checked is False:
            return True
        else:
            return False


class CheckBoxArray(object):
    def __init__(self, window, num, text):
        self.num = num
        self.window = window
        self.checkbox_array = list()
        for _ in range(self.num):
            self.checkbox_array.append(CheckBox(surface=window, x=405, y=405+_*30, caption=text[_]))

    def handle_event(self, event):
        for cb in self.checkbox_array:
            cb.handle_event(event)

    def update_checkbox_array(self):
        font = pygame.font.SysFont('comicsans', 40, bold=False)
        label = font.render('Degree of Difficulty:', 1, (255, 255, 255))
        self.window.blit(label, (TOP_LEFT_X + BOARD_WIDTH/2 - 276, TOP_LEFT_Y + BOARD_HEIGHT/2))
        for cb in self.checkbox_array:
            cb.render_checkbox()       

    def check_complete(self):
        result = list()
        for cb in self.checkbox_array:
            result.append(cb.checked)
        return any(result)
        
    def dump_and_flush(self):
        result = list()
        for cb in self.checkbox_array:
            result.append(cb.checked)
        return result.index(True)