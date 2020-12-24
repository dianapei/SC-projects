"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao

YOUR DESCRIPTION HERE
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics

FRAME_RATE = 1000/120 # 120 frames per second.
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
                    if graphics.check_hit():
                        if graphics.hit():
                            graphics.window.remove(graphics.obj)
                            num_brick -= 1
                        dy *= -1
                    pause(FRAME_RATE)



if __name__ == '__main__':
    main()
