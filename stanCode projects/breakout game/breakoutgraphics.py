"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao

this define class BreakoutGraphics to include game layout and functions  
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40       # Height of a brick (in pixels).
BRICK_HEIGHT = 15      # Height of a brick (in pixels).
BRICK_ROWS = 10        # Number of rows of bricks.
BRICK_COLS = 10        # Number of columns of bricks.
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 10       # Radius of the ball (in pixels).
PADDLE_WIDTH = 75      # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels).
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels).

INITIAL_Y_SPEED = 7.0  # Initial vertical speed for the ball.
MAX_X_SPEED = 5      # Maximum initial horizontal speed for the ball.


class BreakoutGraphics:

    def __init__(self, ball_radius = BALL_RADIUS, paddle_width = PADDLE_WIDTH,
                 paddle_height = PADDLE_HEIGHT, paddle_offset = PADDLE_OFFSET,
                 brick_rows = BRICK_ROWS, brick_cols = BRICK_COLS,
                 brick_width = BRICK_WIDTH, brick_height = BRICK_HEIGHT,
                 brick_offset = BRICK_OFFSET, brick_spacing = BRICK_SPACING,
                 title='Breakout'):

        # Create a graphical window, with some extra space.
        self.window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        self.window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=self.window_width, height=self.window_height, title=title)

        # Create a paddle.
        self.paddle = GRect(width=paddle_width, height=paddle_height, x=(self.window_width-paddle_width)/2,\
                            y=self.window_height-paddle_offset)
        self.paddle.filled = True
        self.window.add(self.paddle)

        # Center a filled ball in the graphical window.
        self.ball_radius = ball_radius
        self.ball = GOval(self.ball_radius*2, self.ball_radius*2)
        self.ball.filled = True
        self.set_ball()
        self.window.add(self.ball)

        # Default initial velocity for the ball.
        self.__dx = random.randint(0, MAX_X_SPEED)
        self.__dy = INITIAL_Y_SPEED
        if random.random() > 0.5:
            self.__dx = - self.__dx

        # Initialize our mouse listeners.
        onmousemoved(self.move_paddle)
        self.switch = False
        onmouseclicked(self.start)

        # Draw bricks.
        x_b = 0
        y_b = 0
        self.brick = None
        self.brick_cols = brick_cols
        self.brick_rows = brick_rows
        self.brick_width = brick_width
        self.brick_height = brick_height
        self.brick_spacing = brick_spacing
        change_color = brick_rows / 5
        for i in range(self.brick_rows):
            for j in range(self.brick_cols):
                r_b = GRect(brick_width, brick_height)
                r_b.filled = True
                r_b.fill_color = 'red'
                o_b = GRect(self.brick_width, self.brick_height)
                o_b.filled = True
                o_b.fill_color = 'orange'
                ye_b = GRect(self.brick_width, self.brick_height)
                ye_b.filled = True
                ye_b.fill_color = 'yellow'
                g_b = GRect(self.brick_width, self.brick_height)
                g_b.filled = True
                g_b.fill_color = 'green'
                b_b = GRect(self.brick_width, self.brick_height)
                b_b.filled = True
                b_b.fill_color = 'blue'
                brick = r_b
                # place red bricks on first one five of the rows
                if i < change_color:
                    self.brick = r_b
                # place orange bricks on rows between one five and two five
                elif change_color <= i < change_color*2:
                    self.brick = o_b
                # place yellow bricks on rows between two five and three five
                elif change_color*2 <= i < change_color*3:
                    self.brick = ye_b
                # place green bricks on rows between two five and three five
                elif change_color*3 <= i < change_color*4:
                    self.brick = g_b
                # place blue bricks on rest of the rows
                else:
                    self.brick = b_b
                # set the x for the columns after column 1
                if j > 0:
                    x_b = x_b + self.brick_width + self.brick_spacing
                #  change row and start with column 1
                else:
                    x_b = 0
                    y_b = y_b + self.brick_height + self.brick_spacing
                self.window.add(self.brick, x_b, y_b)

    # set up the (x, y) of the ball at the center of the window
    def set_ball(self):
        self.ball.x = (self.window_width-self.ball_radius*2)/2
        self.ball.y = (self.window_height-self.ball_radius*2)/2

    # link the paddle with movement of mouse
    def move_paddle(self, event):
        if self.paddle.width / 2 <= event.x - self.paddle.width / 2 <= self.window_width - self.paddle.width:
            self.paddle.x = event.x - self.paddle.width / 2
        elif event.x - self.paddle.width / 2 < self.paddle.width / 2:
            self.paddle.x = 0
        else:
            self.paddle.x = self.window_width - self.paddle.width

    # let user can get the velocity of the ball
    def get_dx(self):
        return self.__dx

    def get_dy(self):
        return self.__dy

    # start the game after clicking
    def start(self, event):
        if self.ball.x == (self.window_width-self.ball_radius*2)/2 and \
                self.ball.y == (self.window_height-self.ball_radius*2)/2:
            if 0 <= event.x <= self.window_width and 0 <= event.y <= self.window_height:
                self.switch = True

    # check if ball hit anything
    def check_hit(self):
        self.obj = self.window.get_object_at(self.ball.x, self.ball.y)
        if self.obj is None:
            self.obj = self.window.get_object_at(self.ball.x, self.ball.y + self.ball_radius * 2)
            if self.obj is None:
                self.obj = self.window.get_object_at(self.ball.x + self.ball_radius * 2, self.ball.y)
                if self. obj is None:
                    self.obj = self.window.get_object_at(self.ball.x + self.ball_radius * 2, self.ball.y + self.ball_radius * 2)
                    if self.obj is None:
                        return False
        return True

    # check if ball hit brick
    def hit(self):
        if self.obj is not self.paddle:
            return True
        else:
            return False








