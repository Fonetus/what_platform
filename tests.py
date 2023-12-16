import unittest
from unittest.mock import patch
import pygame
from level_editor import *
from game import *


    # Add more player tests as needed...

class TestWorld(unittest.TestCase):

    def test_world_init(self):
        # Test the initialization of the World class with mock data
        world_data = [[1, 0], [0, 2]]
        world = World(world_data)

        # Assuming that the first element is a block and the second is empty
        self.assertEqual(len(world.tile_list), 2)

    # Add more world tests as needed...

class TestLava(unittest.TestCase):

    def test_lava_init(self):
        # Test the initialization of the Lava class
        lava = Lava(100, 100)

        self.assertIsNotNone(lava.image)
        self.assertIsNotNone(lava.rect)

    # Add more lava tests as needed...

class TestExit(unittest.TestCase):

    def test_exit_init(self):
        # Test the initialization of the Exit class
        exit = Exit(100, 100)

        self.assertIsNotNone(exit.image)
        self.assertIsNotNone(exit.rect)

    # Add more exit tests as needed...

class TestButton(unittest.TestCase):

    def test_button_init(self):
        # Test the initialization of the Button class
        button_image = pygame.Surface((50, 50))  # Mock button image
        button = Button(100, 100, button_image)

        self.assertEqual(button.rect.x, 100)
        self.assertEqual(button.rect.y, 100)

    # Add more button tests as needed...

if __name__ == '__main__':
    unittest.main()