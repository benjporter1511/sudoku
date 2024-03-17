import sys, pygame as pg
import requests
import copy
import math
from settings import *

class Game:
    """
    Game class
    """

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SCREEN_SIZE)
        self.font = pg.font.SysFont(None, int(SCALE * (7/9)))

        self.response = requests.get("https://sudoku-api.vercel.app/api/dosuku")
        self.difficulty = self.response.json()['newboard']['grids'][0]['difficulty']
        self.grid = self.response.json()['newboard']['grids'][0]['value']
        self.solution = self.response.json()['newboard']['grids'][0]['solution']
        self.original_grid = copy.deepcopy(self.grid)


    def draw_background(self):
        ## blank screen
        self.screen.fill(pg.Color('White'))

        # We need 11 lines horizonallty and vertically to build the grid
        for i in range(10):
            ## draw vertical lines means x value changes by scale value each time
            ## horizonal means y changes and x stays the same
            ## everything third line is thicker and darker in order to get box sections and borders
            line_width = 2 if i % 3 > 0 else 4
            line_colour = "Gray" if i % 3 > 0 else "Black"

            ## line takes values (screen, colour, start x,y coord, end x,y coord, width) and we use Vector2 to get x,y coords

            # vertical lines
            pg.draw.line(self.screen, pg.Color(line_colour), pg.Vector2((SCALE * i) + X_BORDER, Y_BORDER), pg.Vector2((SCALE * i) + X_BORDER, SCREEN_SIZE_Y - Y_BORDER), line_width)

            # horizontal lines
            pg.draw.line(self.screen, pg.Color(line_colour), pg.Vector2(X_BORDER, (SCALE * i) + Y_BORDER), pg.Vector2(SCREEN_SIZE_X - X_BORDER, (SCALE * i) + Y_BORDER), line_width)

    def draw_numbers(self):
        ## loop through rows and columns to iterate through all squares on the grid

        # print difficulty
        difficulty_text = self.font.render(f"Difficulty: {self.difficulty}", True, pg.Color("Black"))
        self.screen.blit(difficulty_text, pg.Vector2(SCALE * 1, SCALE * 0.3))

        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                output = self.grid[row][col]
                if output in list(range(1,10)):
                ## only want to write numbers 1 - 9
                    value = self.font.render(str(output), True, pg.Color("Black"))
                    self.screen.blit(value, pg.Vector2(((col + 1) * SCALE) + X_TEXT_BUFFER, ((row + 1) * SCALE) + Y_TEXT_BUFFER))


    def is_board_full(self):
        ## checks if any entry in the grid is 0 which corresponds to blank value
        for row in self.grid:
            for cell in row:
                if cell == 0:
                    return False
        return True
    
    def is_board_correct(self):
        ## if any value in grid does not equal solution then returns false
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] != self.solution[i][j]:
                    return False
        return True
    
    def reset_grid(self):
        self.grid = copy.deepcopy(self.original_grid)


    def highlight_cell(self, position):
        x_buffer = y_buffer = SCALE/10
        # translucent_yellow = (255, 255, 0, 20)
        pg.draw.rect(self.screen, pg.Color('Red'), ((position[0]*SCALE) + x_buffer, (position[1]*SCALE) + y_buffer, SCALE - 2*x_buffer, SCALE - 2*y_buffer), math.ceil(SCALE*(1/40)))
        pg.display.update()


    def insert_values(self, screen: pg.display, position):
        ## so every time there is a click we will wait for a number input

        ## so i is our y coordinate, e.g. squares horizontally across
        ## and j out x coord as in squares vertically up
        i, j = position[1], position[0]

        # add a buffer here so that when we dreaw rectangle for input we dont overwrite the grid lines we have drawn already
        x_buffer = y_buffer = SCALE/10

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                if event.type == pg.KEYDOWN:
                    ## 1: dont want to let user change the values already populated by API
                    ## 2: we want to allow edits to existing numbers that user has typed
                    ## 3: we also want to allow to add numbers to blank spaces
                    
                    ## -1 due to 0th index
                    ## checking if original grid cell is already poplated with a value 1:
                    if self.original_grid[i-1][j-1] != 0:
                        return
                    
                    elif (event.key == 48):  # 0 is 48 in ascii so check for 0 input here
                        self.grid[i-1][j-1] = event.key - 48 # just making value 0 in grid to check solution

                        ## draw recxt has inputs (screen, colour, [x, y. width, height])
                        ## below draws a a blank box, so basically if input from keyboard is 0 we just draw a blank box, the same as no input
                        pg.draw.rect(screen, pg.Color('White'), ((position[0]*SCALE) + x_buffer, (position[1]*SCALE) + y_buffer, SCALE - 2*x_buffer, SCALE - 2*y_buffer))
                        pg.display.update()
                        return

                    elif (event.key - 48) in list(range(1, 10)): ## check for valid input

                        # Update the grid with the new value
                        self.grid[i-1][j-1] = event.key - 48

                        # Clear the cell by drawing a white rectangle
                        pg.draw.rect(screen, pg.Color('White'), ((position[0]*SCALE) + x_buffer, (position[1]*SCALE) + y_buffer, SCALE - 2*x_buffer, SCALE - 2*y_buffer))

                        # Draw the new value
                        value = self.font.render(str(event.key - 48), True, pg.Color("Black"))
                        screen.blit(value, pg.Vector2((position[0] * SCALE) + X_TEXT_BUFFER, (position[1] * SCALE) + Y_TEXT_BUFFER))

                        pg.display.update()
                        return

                    return           


    def game_loop(self):
        for event in pg.event.get():
            ## checking for mouse click to input a value
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                pos = pg.mouse.get_pos()
                self.highlight_cell((pos[0]//SCALE, pos[1]//SCALE))
                ## we then call insert value function, x and y values for grid box will be x,y position above / SCALE
                self.insert_values(self.screen, (pos[0]//SCALE, pos[1]//SCALE))
            if event.type == pg.QUIT: sys.exit()

        """
        NEXT STEP IS TO ADD LOGIC TO CHECK FOR A WIN STATE, OR TO RESTART THE GAME IF WANTED
        """

        self.draw_background()
        self.draw_numbers()
        # flip() the display to put your work on screen
        pg.display.flip()