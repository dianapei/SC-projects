"""
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.

This program will show the rank line chart of the names from 1900 to 2010 searched by user
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt'
]
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index of the current year in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                              with the specified year.
    """
    space = (width - GRAPH_MARGIN_SIZE * 2)//len(YEARS)
    x_coordinate = GRAPH_MARGIN_SIZE + year_index * space
    return x_coordinate


def draw_fixed_lines(canvas):
    """
    Erases all existing information on the given canvas and then
    draws the fixed background lines on it.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.

    Returns:
        This function does not return any value.
    """
    canvas.delete('all')            # delete all existing lines from the canvas

    # Write your code below this line
    #################################
    # draw the upper horizontal line
    canvas.create_line(GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE, CANVAS_WIDTH-GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE, \
                       width=LINE_WIDTH)
    # draw the lower horizontal line
    canvas.create_line(GRAPH_MARGIN_SIZE, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, CANVAS_WIDTH-GRAPH_MARGIN_SIZE,\
                       CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, width=LINE_WIDTH)
    # draw the vertical lines and place the year next to each line
    for year in YEARS:
        x = get_x_coordinate(CANVAS_WIDTH, YEARS.index(year))
        canvas.create_line(x, 0, x, CANVAS_HEIGHT, width=LINE_WIDTH)
        canvas.create_text(x, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, text=year, anchor=tkinter.NW)



def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # draw the fixed background grid

    # Write your code below this line
    #################################
    rank_space = (CANVAS_HEIGHT-GRAPH_MARGIN_SIZE*2)/MAX_RANK
    x = GRAPH_MARGIN_SIZE
    y = 0
    text = ''
    # check which color should the line and text be
    c_index = 0
    for name in lookup_names:
        # draw line if name in name_data
        if name in name_data:
            # dictionary to store the rank data x, y to draw line and text to add text next to data point
            draw_data = {}
            for year in YEARS:
                # rank of the year out of 1000: y equals the lowest point and text is name with rank replaced by *
                if str(year) not in name_data[name]:
                    y = CANVAS_HEIGHT - GRAPH_MARGIN_SIZE
                    text = str(name + '*')
                # rank within 1000: y changes with the ranking and text goes with the rank number
                else:
                    y = int(GRAPH_MARGIN_SIZE + int(name_data[name][str(year)]) * rank_space)
                    text = name + ' ' + name_data[name][str(year)]
                # get x of each year which align with the vertical lines
                x = get_x_coordinate(CANVAS_WIDTH, YEARS.index(year))
                # add list of year to draw_data
                draw_data[year] = [x, y, text]
            # add lines and text to the canvas
            for year in draw_data:
                # other than 1900, each year will draw a line to link its data point with previous year
                if year != YEARS[0]:
                    # get index of current year from YEAR
                    year_index = YEARS.index(year)
                    # use year_index to know previous year and get the data point within draw_data
                    canvas.create_line(draw_data[YEARS[int(year_index)-1]][0], draw_data[YEARS[int(year_index)-1]][1],\
                                       draw_data[year][0], draw_data[year][1], width=LINE_WIDTH, fill=COLORS[c_index])
                # add text next to every data point
                canvas.create_text(draw_data[year][0] + TEXT_DX, draw_data[year][1], text=draw_data[year][2],\
                                   anchor=tkinter.SW, fill=COLORS[c_index])
            # change color for next line and if already use all colors, start all over
            c_index += 1
            if c_index + 1 > len(COLORS):
                c_index = 0


# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
