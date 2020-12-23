"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao

YOUR DESCRIPTION HERE
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics

FRAME_RATE = 1000 / 120 # 120 frames per second.
NUM_LIVES = 3


def main():
    graphics = BreakoutGraphics(paddle_width=100)
    # time of fail start with 0
    out = 0
    num_brick = graphics.brick_rows * graphics.brick_cols
    # let program constant to check if user starts the game
    while True:
        pause(FRAME_RATE)
        # ball start to move after user clicks the mouse
        if graphics.switch:
            dx = graphics.get_dx()
            dy = graphics.get_dy()
            while True:
                up_left = graphics.window.get_object_at(graphics.ball.x, graphics.ball.y)
                down_left = graphics.window.get_object_at(graphics.ball.x, graphics.ball.y + graphics.ball_radius * 2)
                up_right = graphics.window.get_object_at(graphics.ball.x + graphics.ball_radius * 2, graphics.ball.y)
                down_right = graphics.window.get_object_at(graphics.ball.x + graphics.ball_radius * 2, \
                                                           graphics.ball.y + graphics.ball_radius * 2)
                graphics.ball.move(dx, dy)
                # game over when user runs out of lives and break all the bricks
                if num_brick == 0 or out == NUM_LIVES:
                    graphics.set_ball()
                    graphics.switch = False
                    break
                else:
                    # if the ball hits the left, up and right wall, it will bounce back
                    if graphics.ball.x <= 0 or graphics.ball.x + graphics.ball.width >= graphics.window_width:
                        dx = -dx
                    if graphics.ball.y <= 0:
                        dy = -dy
                    # if ball drops out of the window, increase failure by 1, reset ball to start over
                    if graphics.ball.y + graphics.ball.height > graphics.window_height:
                        out += 1
                        # ball will not move till the user clicks the mouse
                        graphics.set_ball()
                        graphics.switch = False
                        break
                    # check if the ball hits anything. If yes, will remove the object if it's a brick.
                    if up_left is not None:
                        if up_left is not graphics.paddle:
                            graphics.window.remove(up_left)
                            num_brick -= 1
                            dy = -dy
                        else:
                            if dy > 0:
                                dy = -dy
                    elif down_left is not None:
                        if down_left is not graphics.paddle:
                            graphics.window.remove(down_left)
                            num_brick -= 1
                            dy = -dy
                        else:
                            if dy > 0:
                                dy = -dy
                    elif up_right is not None:
                        if up_right is not graphics.paddle:
                            graphics.window.remove(up_right)
                            num_brick -= 1
                            dy = -dy
                        else:
                            if dy > 0:
                                dy = -dy
                    elif down_right is not None:
                        if down_right is not graphics.paddle:
                            graphics.window.remove(down_right)
                            num_brick -= 1
                            dy = -dy
                        else:
                            if dy > 0:
                                dy = -dy
                    pause(FRAME_RATE)



if __name__ == '__main__':
    main()
