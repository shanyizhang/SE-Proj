## ----------------------------------------
##   Software Engineering @ NYU
##   Course Project - Tetris Game
##   Ken S. Zhang & Qingyang Li
## ----------------------------------------


from config import *
import pygame


class UserInterface(object):
    def __init__(self, show_window=True):
        """
        Init the UserInterface
        Input: Boolean indicating if window is displayed
        Output: None
        """
        pygame.font.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags=0 if show_window else pygame.HIDDEN)
        pygame.display.set_caption('Tetris Game')
        self.inputbox = InputBox(window=self.window)
        self.checkbox = CheckBoxArray(window=self.window, num=3, text=["Easy", "Medium", "Hard"])

    def start(self):
        """
        Display instruction, inputbox and checkbox
        Input: None
        Output: None        
        """
        self.window.fill((0,0,0))
        self.draw_text_middle('Enter Game Settings to Begin.', 40, (255, 255, 255))  # make it smaller
        self.inputbox.update_inputbox()
        self.checkbox.update_checkbox_array()
        self.update()

    def update(self):
        """ Update new component to the interface """
        pygame.display.update()

    def shutdown(self):
        """ Quit the game """
        pygame.display.quit()

    def draw_text_middle(self, text, size, color):
        """
        Draw text in the middle of the interface
        Input: Text, the font size of text and the color
        Output: None
        """
        font = pygame.font.SysFont('comicsans', size, bold=True)
        label = font.render(text, 1, color)
        self.window.blit(label, (TOP_LEFT_X + BOARD_WIDTH/2 - (label.get_width() / 2), TOP_LEFT_Y + BOARD_HEIGHT/2 - label.get_height()/2 - 100))

    def draw_grid(self):
        """
        Draw grid for tetris game
        Input: None
        Output: None
        """
        sx = TOP_LEFT_X
        sy = TOP_LEFT_Y
        for i in range(ROW):
            pygame.draw.line(self.window, (128,128,128), (sx, sy + i * BLOCK_SIZE), (sx + BOARD_WIDTH, sy + i * BLOCK_SIZE))  
            for j in range(COLUMN):
                pygame.draw.line(self.window, (128,128,128), (sx + j * BLOCK_SIZE, sy), (sx + j * BLOCK_SIZE, sy + BOARD_HEIGHT))  

    def draw_window(self, grid):
        """
        Draw grid and tetrominos on the fly for tetris game
        Input: Curremt state of grid
        Output: None
        """
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
        """
        Draw the upcoming next tetromino for tetris game
        Input: The shape of next tetromino
        Output: None
        """
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
    
    def draw_text_upper(self, text, size, color, loc):
        """
        Draw a line of text, location is specified by the caller
        Input: Text, the font size of text, the color and the location
        Output: None
        """        
        font = pygame.font.SysFont('comicsans', size, bold=True)
        label = font.render(text, 1, color)
        self.window.blit(label,
            (TOP_LEFT_X + BOARD_WIDTH/2 - (label.get_width() / 2), loc))

    def draw_leader_board(self, rows):
        """
        Display the leaderboard
        Input: Rows of lines for display
        Output: None
        """
        # flush the current window
        self.window.fill((0, 0, 0))  # fill with black
        self.draw_text_upper("Leader Board", 60, (255, 255, 255), 30)  # Title
        self.draw_text_upper("Press any key to exit.", 15, (255, 255, 255), 600)  # comment
        # display each record in a line
        l = len(rows)
        for i in range(l):
            row_str = "No.%d    %s    %s" % (i + 1, rows[i][0], rows[i][1])
            self.draw_text_upper(row_str, 30, (255, 255, 255), 130 + 100 * i)
        self.update()
        # press any key to quit
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    return None


class InputBox(object):
    def __init__(self, window):
        """
        Init the inputbox
        Input: Window object for display
        Output: None
        """
        self.window = window
        self.rect = pygame.Rect(TOP_LEFT_X + BOARD_WIDTH/2, TOP_LEFT_Y + BOARD_HEIGHT/2 - 55, 140, 32)
        self.color = (255, 255, 255)
        self.text = ''
        self.txt_surface = pygame.font.Font(None, 32).render(self.text, True, self.color)
        self.complete = False

    def handle_event(self, event):
        """
        Handle events related to inputbox
        Input: event object captured by pygame framework
        Output: None
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.complete = True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            
    def update_display_text(self):
        """
        Update the input text from the user
        Input: None
        Output: None
        """
        self.txt_surface = pygame.font.Font(None, 32).render(self.text, True, self.color)
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
        self.window.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))

    def draw_rect(self):
        """
        Draw the rectangle that surrounds the text
        Input: None
        Output: None
        """
        font = pygame.font.SysFont('comicsans', 40, bold=False)
        label = font.render('Username:', 1, (255, 255, 255))
        self.window.blit(label, (TOP_LEFT_X + BOARD_WIDTH/2 - 153, TOP_LEFT_Y + BOARD_HEIGHT/2 - 55))
        pygame.draw.rect(self.window, self.color, self.rect, 2)

    def update_inputbox(self):
        """ Update both the text and the rectangle to the interface """
        self.update_display_text()
        self.draw_rect()

    def check_complete(self):
        """ Check if the user has finished inputting the text """
        return self.complete == True

    def dump_and_flush(self):
        """
        Output the text held by the inputbox
        Input: None
        Output: The text        
        """
        text_temp = self.text
        self.complete = False
        self.txt_surface = pygame.font.Font(None, 32).render(self.text, True, self.color)
        return text_temp

    
class CheckBox(object):
    def __init__(self, surface, x, y, color=(230, 230, 230), caption="", outline_color=(0, 0, 0),
                 check_color=(0, 0, 0), font_size=32, font_color=(255, 255, 255), text_offset=(40, 1)):
        """
        Init the checkbox
        Input: Window object for display, coordinates, color, prefix caption, outline color, check color,
            font size of the text, color of the text and the text offset for display
        Output: None        
        """
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
        self.checkbox_obj = pygame.Rect(self.x, self.y, 12, 12)
        self.checkbox_outline = self.checkbox_obj.copy()
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
        """
        Render the checkbox including rectangles, check signs etc.
        Input: None
        Output: None
        """
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
        """
        Handle events related to checkbox
        Input: event object captured by pygame framework
        Output: None
        """
        if event_object.type == pygame.MOUSEBUTTONDOWN:
            self.click = True
        if event_object.type == pygame.MOUSEBUTTONUP:
            self._mouse_up()
        if event_object.type == pygame.MOUSEMOTION:
            self._update(event_object)

    def is_checked(self):
        """ Return a boolean indicating if the user has checked the checkbox """
        if self.checked is True:
            return True
        else:
            return False

    def is_unchecked(self):
        """ Return a boolean indicating if the user hasn't checked the checkbox """
        if self.checked is False:
            return True
        else:
            return False


class CheckBoxArray(object):
    def __init__(self, window, num, text):
        """
        Init the CheckBoxArray
        Input: Window object for display, number of checkboxes and corresponding texts
        Output: None
        """
        self.num = num
        self.window = window
        self.checkbox_array = list()
        for _ in range(self.num):
            self.checkbox_array.append(CheckBox(surface=window, x=405, y=405+_*30, caption=text[_]))

    def handle_event(self, event):
        """
        Handle events related to checkbox
        Input: event object captured by pygame framework
        Output: None
        """
        for cb in self.checkbox_array:
            cb.handle_event(event)

    def update_checkbox_array(self):
        """
        Update all checkboxes including rectangles, check signs etc.
        Input: None
        Output: None
        """
        font = pygame.font.SysFont('comicsans', 40, bold=False)
        label = font.render('Degree of Difficulty:', 1, (255, 255, 255))
        self.window.blit(label, (TOP_LEFT_X + BOARD_WIDTH/2 - 276, TOP_LEFT_Y + BOARD_HEIGHT/2))
        for cb in self.checkbox_array:
            cb.render_checkbox()       

    def check_complete(self):
        """ Return a boolean indicating if the user has checked any of the checkboxes """
        result = list()
        for cb in self.checkbox_array:
            result.append(cb.checked)
        return any(result)
        
    def dump_and_flush(self):
        """
        Output the index of the signed checkbox
        Input: None
        Output: The index        
        """
        result = list()
        for cb in self.checkbox_array:
            result.append(cb.checked)
        return result.index(True)