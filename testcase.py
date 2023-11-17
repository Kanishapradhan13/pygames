import unittest
import pygame
from Game import SnakeGame, Snake, Fruit

class TestSnakeGame(unittest.TestCase):

   def setUp(self):
       pygame.init()
       self.game = SnakeGame()

   def test_snake_initialization(self):
       snake = Snake(self.game)
       self.assertEqual(len(snake.body), 1) # The snake should have one segment initially
       self.assertEqual(snake.direction, 'RIGHT') # Snake should move to the right initially

   def test_snake_movement(self):
    snake = Snake(self.game)
    initial_head = snake.get_head_position()
    snake.move()  # Assuming there's a move method to update the snake's position
    new_head = snake.get_head_position()
    self.assertEqual(new_head[0], initial_head[0])

   def test_snake_collision(self):
    self.game.snake.body = [(100, 100), (90, 100), (100, 100)]  # Sample snake body
    self.assertTrue(self.game.snake.check_snake_collision(), "Collision not detected as expected.")


   def test_snake_growth(self):
    snake = Snake(self.game)
    initial_length = len(snake.body)
    snake.grow()
    final_length = len(snake.body)
    self.assertEqual(final_length, initial_length + 1, "Snake did not grow as expected.")



class TestFruit(unittest.TestCase):
    def setUp(self):
        self.game = SnakeGame()  # Assuming Game is your game class
        self.fruit = Fruit(self.game)

    def test_check_collision(self):
        # Set the snake and fruit positions to the same coordinates
        self.game.snake.position = [100, 100]
        self.fruit.position = [100, 100]

        # Check if a collision is detected
        self.assertTrue(self.fruit.check_collision())

        # Set the snake and fruit positions to different coordinates
        self.game.snake.position = [100, 100]
        self.fruit.position = [200, 200]

        # Check if no collision is detected
        self.assertFalse(self.fruit.check_collision())

if __name__ == '__main__':
    unittest.main()

def tearDown(self):
    pygame.quit()   

if __name__ == '__main__':
   unittest.main()
