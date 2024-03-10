import sys, pygame as pg
import requests

pg.init()
## create screen
## scale value used to scale screen size so everything will be in proportion
SCALE = 80
SCREEN_SIZE_X = 11 * SCALE
SCREEN_SIZE_Y = 11 * SCALE
X_BORDER = SCALE
Y_BORDER = SCALE
screen_size = SCREEN_SIZE_X, SCREEN_SIZE_Y
screen = pg.display.set_mode(screen_size)
font = pg.font.SysFont(None, int(SCALE * (7/9)))

## making API call to get sudoku board
response = requests.get("https://sudoku-api.vercel.app/api/dosuku")
difficulty = response.json()['newboard']['grids'][0]['difficulty']
grid = response.json()['newboard']['grids'][0]['value']
original_grid = grid.copy()

def draw_background():
    ## blank screen
    screen.fill(pg.Color('White'))

    # We need 11 lines horizonallty and vertically to build the grid
    for i in range(10):
        ## draw vertical lines means x value changes by scale value each time
        ## horizonal means y changes and x stays the same
        ## everything third line is thicker and darker in order to get box sections and borders
        line_width = 2 if i % 3 > 0 else 4
        line_colour = "Gray" if i % 3 > 0 else "Black"

        ## line takes values (screen, colour, start x,y coord, end x,y coord, width) and we use Vector2 to get x,y coords

        # vertical lines
        pg.draw.line(screen, pg.Color(line_colour), pg.Vector2((SCALE * i) + X_BORDER, Y_BORDER), pg.Vector2((SCALE * i) + X_BORDER, SCREEN_SIZE_Y - Y_BORDER), line_width)

        # horizontal lines
        pg.draw.line(screen, pg.Color(line_colour), pg.Vector2(X_BORDER, (SCALE * i) + Y_BORDER), pg.Vector2(SCREEN_SIZE_X - X_BORDER, (SCALE * i) + Y_BORDER), line_width)


def draw_numbers():
    ## loop through rows and columns to iterate through all squares on the grid

    # print difficulty
    difficulty_text = font.render(f"Difficulty: {difficulty}", True, pg.Color("Black"))
    screen.blit(difficulty_text, pg.Vector2(SCALE * 1, SCALE * 0.3))

    ## we need a buffer to movbe it centrally in the grid square
    x_buffer = (32/90) * SCALE
    y_buffer = (25/90) * SCALE

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            output = grid[row][col]
            if output in list(range(1,10)):
            ## only want to write numbers 1 - 9
                value = font.render(str(output), True, pg.Color("Black"))
                screen.blit(value, pg.Vector2(((col + 1) * SCALE) + x_buffer, ((row + 1) * SCALE) + y_buffer)) 


def game_loop():
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit()

    draw_background()
    draw_numbers()
    # flip() the display to put your work on screen
    pg.display.flip()

while True:
    game_loop()