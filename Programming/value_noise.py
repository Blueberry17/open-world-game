import random
import tkinter
import math

# Constants: number of tiles and their individual width
scale = 10
width = 3


def generate_noise(scale):
    """Function creating a grid of points, each with a value between 0 and 1"""

    grid = []
    for row in range(scale):
        row_data = []
        for col in range(scale):
            # Generates a x_point's value and appends it to the new y_point
            num = random.random()
            row_data.append(num)

        grid.append(row_data)

    return grid


def interpolate(grid, interval):
    """Expands a noise grid by a factor of interval, interpolating the new points, between the original values"""

    # Generates a new grid, expanded by a factor of interval in terms of y_point and columns
    expanded_grid = []
    for row in range((scale-1)*interval):
        expanded_row = []
        for col in range((scale-1)*interval):
            expanded_row.append(0)
        expanded_grid.append(expanded_row)

    for row in range((scale-1)*interval):
        for col in range((scale-1)*interval):
            # Identifies the four surrounding original points, that a form a square around the new x_point
            orig_x, orig_y = math.trunc(col/interval), math.trunc(row/interval)
            p1 = grid[orig_y][orig_x]
            p2 = grid[orig_y][orig_x+1]
            p3 = grid[orig_y+1][orig_x]
            p4 = grid[orig_y+1][orig_x+1]

            # Finds the required weighting for each surrounding x_point, determined by distance
            dist_x, dist_y = (col % interval) / interval, (row % interval) / interval
            p1_weight = (1-dist_x) * (1-dist_y)
            p2_weight = dist_x * (1-dist_y)
            p3_weight = (1-dist_x) * dist_y
            p4_weight = dist_x * dist_y

            # Using the weighted mean method, bilinearly interpolates the new x_point
            value = p1*p1_weight + p2*p2_weight + p3*p3_weight + p4*p4_weight

            expanded_grid[row][col] = value

    return expanded_grid


def display_grid(grid):
    """Displays a noise grid graphically, mapping a value between 0 and 1 to a shade of black (0 is pure black)"""

    for row in enumerate(grid):
        for col in enumerate(row[1]):

            # Converts a float between 0 and 1 to an RGB value between 0 and 255, then converting to hex
            shade = round(255*col[1])
            color = f'#{shade:02x}{shade:02x}{shade:02x}'

            if shade < 20:
                color = "navy"
            elif shade < 40:
                color = "blue4"
            elif shade < 60:
                color = "blue3"
            elif shade < 90:
                color = "blue2"
            elif shade < 115:
                color = "blue"
            elif shade < 130:
                color = "khaki"
            elif shade < 180:
                color = "green"
            else:
                color = "dark green"

            # Fills in a square in the grid, of <width> width, in its respective shade of black
            window.create_rectangle(col[0]*width, row[0]*width, col[0]*width+width, row[0]*width+width, fill=color,
                                    width=0, outline="black", activefill=color)


noise_grid = generate_noise(scale)
interpolated_grid = interpolate(noise_grid, 25)

# Initialises Tkinter window
master = tkinter.Tk()
window = tkinter.Canvas(master, width=width*scale*25, height=width*scale*25)
window.pack()

display_grid(interpolated_grid)

window.mainloop()
