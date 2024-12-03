# Team: Vansh Joshi, Om Patel, Mathew Phan, Sarvvesh Vindokumar

import pygame
import random
import math

pygame.init()

class Ball:
    MAX_VEL = 5  # Maximum velocity of the ball
    RADIUS = 7   # Ball radius in pixels

    def __init__(self, x, y):
        # Initialize ball with starting position and random direction
        self.x = self.original_x = x
        self.y = self.original_y = y

        # Set initial trajectory between -30 and 30 degrees
        angle = self._get_random_angle(-30, 30, [0])
        pos = 1 if random.random() < 0.5 else -1  # Randomly choose initial direction

        # Calculate velocity components using trigonometry
        self.x_vel = pos * abs(math.cos(angle) * self.MAX_VEL)
        self.y_vel = math.sin(angle) * self.MAX_VEL

    def _get_random_angle(self, min_angle, max_angle, excluded):
        # Generate random angle in radians, avoiding excluded angles
        angle = 0
        while angle in excluded:
            angle = math.radians(random.randrange(min_angle, max_angle))
        return angle

    def draw(self, win):
        # Draw ball on the game window
        pygame.draw.circle(win, (255, 255, 255), (self.x, self.y), self.RADIUS)

    def move(self):
        # Update ball position based on velocity
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        # Reset ball to starting position with new random trajectory
        self.x = self.original_x
        self.y = self.original_y
        angle = self._get_random_angle(-30, 30, [0])
        x_vel = abs(math.cos(angle) * self.MAX_VEL)
        y_vel = math.sin(angle) * self.MAX_VEL
        self.y_vel = y_vel
        self.x_vel *= -1

class Paddle:
    VEL = 4      # Paddle movement speed
    WIDTH = 20   # Paddle width in pixels
    HEIGHT = 100 # Paddle height in pixels

    def __init__(self, x, y):

        self.x = self.original_x = x
        self.y = self.original_y = y

    def draw(self, win):
        # Draw paddle on game window.
        pygame.draw.rect(
            win, (255, 255, 255), (self.x, self.y, self.WIDTH, self.HEIGHT))

    def move(self, up=True):
        # Move paddle up or down
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        # Reset paddle to starting position
        self.x = self.original_x
        self.y = self.original_y

class GameInformation:
    # Stores game state information for score tracking and AI training
    def __init__(self, left_hits, right_hits, left_score, right_score):
        self.left_hits = left_hits
        self.right_hits = right_hits
        self.left_score = left_score
        self.right_score = right_score

class Game:
    SCORE_FONT = pygame.font.SysFont("comicsans", 50)
    COLOR_PALETTE = {
        "WHITE": (255, 255, 255),
        "BLACK": (0, 0, 0),
        "RED": (255, 0, 0)
    }

    def __init__(self, window, window_width, window_height):
        # Initialize game window and objects
        self.window_width = window_width
        self.window_height = window_height

        # Create paddles and ball
        self.left_paddle = Paddle(10, self.window_height // 2 - Paddle.HEIGHT // 2)
        self.right_paddle = Paddle(self.window_width - 10 - Paddle.WIDTH, self.window_height // 2 - Paddle.HEIGHT // 2)
        self.ball = Ball(self.window_width // 2, self.window_height // 2)

        # Initialize score tracking
        self.scores = {
            "left_score": 0,
            "right_score": 0
        }
        self.hits = {
            "left_hits": 0,
            "right_hits": 0
        }
        self.window = window

    def _draw_score(self):
        # Render score display.
        left_score_text = self.SCORE_FONT.render(f"{self.scores['left_score']}", 1, self.COLOR_PALETTE["WHITE"])
        right_score_text = self.SCORE_FONT.render(f"{self.scores['right_score']}", 1, self.COLOR_PALETTE["WHITE"])
        self.window.blit(left_score_text, (self.window_width // 4 - left_score_text.get_width()//2, 20))
        self.window.blit(right_score_text, (self.window_width * (3/4) - right_score_text.get_width()//2, 20))

    def _draw_hits(self):
        # Render total hits counter
        hits_text = self.SCORE_FONT.render(f"{self.hits['left_hits'] + self.hits['right_hits']}", 1, self.COLOR_PALETTE["RED"])
        self.window.blit(hits_text, (self.window_width // 2 - hits_text.get_width()//2, 10))

    def _draw_divider(self):
        # Draw center line divider.
        for i in range(10, self.window_height, self.window_height//20):
            if i % 2 == 1:
                continue
            pygame.draw.rect(self.window, self.COLOR_PALETTE["WHITE"], (self.window_width//2 - 5, i, 10, self.window_height//20))

    def _handle_collision(self):
        # Handle ball collisions with walls and paddles
        ball = self.ball
        left_paddle = self.left_paddle
        right_paddle = self.right_paddle

        # Wall collisions
        if ball.y + ball.RADIUS >= self.window_height:
            ball.y_vel *= -1
        elif ball.y - ball.RADIUS <= 0:
            ball.y_vel *= -1

        # Left paddle collision
        if ball.x_vel < 0:
            if ball.y >= left_paddle.y and ball.y <= left_paddle.y + Paddle.HEIGHT:
                if ball.x - ball.RADIUS <= left_paddle.x + Paddle.WIDTH:
                    ball.x_vel *= -1
                    # Calculate new y velocity based on hit position
                    middle_y = left_paddle.y + Paddle.HEIGHT / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (Paddle.HEIGHT / 2) / ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel
                    self.hits["left_hits"] += 1

        # Right paddle collision
        else:
            if ball.y >= right_paddle.y and ball.y <= right_paddle.y + Paddle.HEIGHT:
                if ball.x + ball.RADIUS >= right_paddle.x:
                    ball.x_vel *= -1
                    # Calculate new y velocity based on hit position
                    middle_y = right_paddle.y + Paddle.HEIGHT / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (Paddle.HEIGHT / 2) / ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel
                    self.hits["right_hits"] += 1

    def draw(self, draw_score=True, draw_hits=False):
        self.window.fill(self.COLOR_PALETTE["BLACK"])
        self._draw_divider()
        if draw_score:
            self._draw_score()
        if draw_hits:
            self._draw_hits()
        for paddle in [self.left_paddle, self.right_paddle]:
            paddle.draw(self.window)
        self.ball.draw(self.window)

    def move_paddle(self, left=True, up=True):
        # Move specified paddle, preventing out-of-bounds movement
        if left:
            if up and self.left_paddle.y - Paddle.VEL < 0:
                return False
            if not up and self.left_paddle.y + Paddle.HEIGHT > self.window_height:
                return False
            self.left_paddle.move(up)
        else:
            if up and self.right_paddle.y - Paddle.VEL < 0:
                return False
            if not up and self.right_paddle.y + Paddle.HEIGHT > self.window_height:
                return False
            self.right_paddle.move(up)
        return True

    def loop(self):
        self.ball.move()
        self._handle_collision()

        # Score points and reset ball
        if self.ball.x < 0:
            self.ball.reset()
            self.scores["right_score"] += 1
        elif self.ball.x > self.window_width:
            self.ball.reset()
            self.scores["left_score"] += 1

        return GameInformation(
            self.hits["left_hits"], 
            self.hits["right_hits"], 
            self.scores["left_score"], 
            self.scores["right_score"]
        )

    def reset(self):
        # Reset game state to initial conditions
        self.ball.reset()
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.scores["left_score"] = 0
        self.scores["right_score"] = 0
        self.hits["left_hits"] = 0
        self.hits["right_hits"] = 0