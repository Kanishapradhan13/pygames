import pygame
import sys
import random 

class SnakeGame:
    def __init__(self):
        pygame.init()

        self.display_width = 700
        self.display_height = 500
        self.gamedisplays = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()

        self.snake = Snake(self)
        self.fruit = Fruit(self)
        self.obstacles = []

        self.score = 0
        self.level = 1

        self.game_over = False
        self.game_started = False

    def draw_button(self, text, x, y, w, h, color, hover_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.gamedisplays, hover_color, (x, y, w, h))
            if click[0] == 1 and action is not None:
                action()
        else:
            pygame.draw.rect(self.gamedisplays, color, (x, y, w, h))

        button_font = pygame.font.Font(None, 36)
        text_surface = button_font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(x + w / 2, y + h / 2))
        self.gamedisplays.blit(text_surface, text_rect)

    def generate_obstacle(self):
        x = random.randrange(1, (self.display_width // 10)) * 10
        y = random.randrange(1, (self.display_height // 10)) * 10
        return [x, y]

    def start_game(self):
        self.game_started = True

    def pause_game(self):
        self.game_started = not self.game_started

    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True

            if not self.game_started:
                self.gamedisplays.fill((0, 0, 0))
                self.draw_button("Start", self.display_width // 2 - 50, self.display_height // 2 - 20, 100, 40, (0, 255, 0), (0, 200, 0), self.start_game)
                pygame.display.update()
            else:
                self.snake.move()
                self.fruit.check_collision()
                self.check_obstacle_collision()

                self.gamedisplays.fill((0, 0, 0))
                self.snake.draw()
                self.fruit.draw()

                for obstacle in self.obstacles:
                    pygame.draw.rect(self.gamedisplays, (255, 255, 0), pygame.Rect(obstacle[0], obstacle[1], 10, 10))

                self.display_score()

                pygame.display.update()
                self.clock.tick(10)

        if self.game_over:
            self.display_game_over()
            pygame.quit()
            sys.exit()

    def check_obstacle_collision(self):
        for obstacle in self.obstacles:
            if self.snake.position == obstacle:
                self.game_over = True
                break

    def display_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: " + str(self.score), True, (255, 255, 255))
        

        self.gamedisplays.blit(score_text, (10, 10))
        

    def display_game_over(self):
        game_over_font = pygame.font.Font(None, 48)
        game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))

        self.gamedisplays.blit(game_over_text, (self.display_width // 2 - game_over_text.get_width() // 2, self.display_height // 2 - 48))
        pygame.display.update()
        pygame.time.wait(3000)

class Snake:
    def __init__(self, game):
        self.game = game
        self.position = [100, 50]
        self.body = [self.position]
        self.direction = 'RIGHT'

    def move(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and self.game.game_started:
                if event.key == pygame.K_UP and self.direction != 'DOWN':
                    self.direction = 'UP'
                elif event.key == pygame.K_DOWN and self.direction != 'UP':
                    self.direction = 'DOWN'
                elif event.key == pygame.K_LEFT and self.direction != 'RIGHT':
                    self.direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and self.direction != 'LEFT':
                    self.direction = 'RIGHT'

        if keys[pygame.K_UP] and self.direction != 'DOWN':
            self.direction = 'UP'
        elif keys[pygame.K_DOWN] and self.direction != 'UP':
            self.direction = 'DOWN'
        elif keys[pygame.K_LEFT] and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        elif keys[pygame.K_RIGHT] and self.direction != 'LEFT':
            self.direction = 'RIGHT'

        if self.direction == 'UP':
            self.position[1] -= 10
        elif self.direction == 'DOWN':
            self.position[1] += 10
        elif self.direction == 'LEFT':
            self.position[0] -= 10
        elif self.direction == 'RIGHT':
            self.position[0] += 10

        if self.position[0] < 0 or self.position[0] >= self.game.display_width or self.position[1] < 0 or self.position[1] >= self.game.display_height:
            self.game.game_over = True

        self.body.insert(0, list(self.position))
        if self.position == self.game.fruit.position:
            self.game.score += 1
            self.game.fruit.position = [random.randrange(1, (self.game.display_width // 10)) * 10, random.randrange(1, (self.game.display_height // 10)) * 10]
        else:
            self.body.pop()


    def draw(self):
        for position in self.body:
            pygame.draw.rect(self.game.gamedisplays, (0, 255, 0), pygame.Rect(position[0], position[1], 10, 10))

class Fruit:
    def __init__(self, game):
        self.game = game
        self.position = [random.randrange(1, (self.game.display_width // 10)) * 10, random.randrange(1, (self.game.display_height // 10)) * 10]

    def draw(self):
        pygame.draw.rect(self.game.gamedisplays, (255, 0, 0), pygame.Rect(self.position[0], self.position[1], 10, 10))

    def check_collision(self):
        if self.game.snake.position[0] == self.position[0] and self.game.snake.position[1] == self.position[1]:
            self.position = [random.randrange(1, (self.game.display_width // 10)) * 10, random.randrange(1, (self.game.display_height // 10)) * 10]
            self.game.score += 1
            if self.game.score % 10 == 0:
                self.game.level += 1
                self.game.clock.tick(15)
                self.game.obstacles.append(self.game.generate_obstacle())

if __name__ == "__main__":
    game = SnakeGame()
    game.run()