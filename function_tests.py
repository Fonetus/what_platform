import unittest
import pygame
from level_editor import draw_grid, draw_text, draw_world

class TestLevelEditorFunctions(unittest.TestCase):


    def test_draw_grid_invalid_screen(self):
        with self.assertRaises(TypeError):
            draw_grid("invalid_screen", 50, 600, 100)


    def test_draw_text_invalid_font(self):
        screen = pygame.Surface((800, 600))
        with self.assertRaises(TypeError):
            draw_text(screen, "Hello", "invalid_font", (255, 255, 255), 100, 200)



    def test_draw_world_invalid_data(self):
        screen = pygame.Surface((800, 600))
        with self.assertRaises(TypeError):
            draw_world(screen, "invalid_data")

    def test_draw_world_invalid_data_structure(self):
        screen = pygame.Surface((800, 600))
        world_data = [[1, 0], [0, 2, 3]]  # Некорректная структура данных
        with self.assertRaises(TypeError):
            draw_world(screen, world_data)

    def test_draw_world_invalid_screen(self):
        world_data = [[1, 0], [0, 2]]
        with self.assertRaises(TypeError):
            draw_world("invalid_screen", world_data)

if __name__ == '__main__':
    unittest.main()