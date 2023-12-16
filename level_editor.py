import pygame
import pickle
from os import path

'''
Pygame needs to be initialized using the command pygame.init().
'''
pygame.init()

'''
The frame rate of the game is set to 60 frames per second (fps) using the command:
:clock: pygame.time.Clock()
:fps: 60 
'''
clock = pygame.time.Clock()
fps = 60

'''
The game window is set up with the following parametrs:
:tile size: 50
:number of columns -- cols: 20
:margin: 100
:screen width: tile_size * columns
:screen height: (tile size * columns) + margin 
'''
tile_size = 50
cols = 20
margin = 100
screen_width = tile_size * cols
screen_height = (tile_size * cols) + margin

'''
The game window is displayed using the command:
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Level Editor')
'''
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Level Editor')


'''
Images are loaded and transformed for use in the game as follows:
:background Image: loaded from 'img/blue.png' and scaled to the game window size using pygame.transform.scale.
:dirt Image: loaded from 'img/block.png'.
:grass Image: loaded from 'img/block_snow.png'.
:lava Image: loaded from 'img/lava.png'.
:exit Image: loaded from 'img/portal.png'.
:save Image: loaded from 'img/save_btn.png'.
:load Image: loaded from 'img/load_btn.png'.
'''
bg_img = pygame.image.load('img/blue.png')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height - margin))
dirt_img = pygame.image.load('img/block.png')
grass_img = pygame.image.load('img/block_snow.png')
lava_img = pygame.image.load('img/lava.png')
exit_img = pygame.image.load('img/portal.png')
save_img = pygame.image.load('img/save_btn.png')
load_img = pygame.image.load('img/load_btn.png')

'''
The following game variables are defined:
:clicked: a boolean variable that indicates whether the mouse button has been clicked.
:level: an integer variable representing the current level of the game.
'''
clicked = False
level = 0

'''
The following colours are defined using RGB values:
:white: (255, 255, 255)
:green: (144, 201, 120)
'''
white = (255, 255, 255)
green = (144, 201, 120)

'''
A font is defined for use in the game with the following parameters:
:font type: 'Futura'
"font size: 30
'''
font = pygame.font.SysFont('Futura', 30)

'''
An empty tile list, named world_data, is created and initialized 
as a 20x20 grid with all elements set to 0.
'''
world_data = []
for row in range(20):
	r = [0] * 20
	world_data.append(r)

'''
The boundary of the game world is defined by setting specific tiles to different values as follows:
:the bottom row (row 19) is set to 2.
:the top row (row 0) is set to 1.
:the leftmost column (column 0) is set to 1.
:the rightmost column (column 19) is set to 1.
'''
for tile in range(0, 20):
	world_data[19][tile] = 2
	world_data[0][tile] = 1
	world_data[tile][0] = 1
	world_data[tile][19] = 1

'''
A function named draw_text is defined for outputting text onto the screen with the following parameters:
:text: Text to be displayed
:font: Font type and size
:text_col: Colour of the text
:params x, y: Coordinates for positioning the text.
'''
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

'''
The draw_grid function is defined to draw grid lines on the game window:
:vertical Lines: Drawn at intervals of tile_size from the left side to the right side of the screen.
:horizontal Lines: Drawn at intervals of tile_size from the top to the bottom of the screen, excluding the margin.
'''
def draw_grid():
	for c in range(21):
		pygame.draw.line(screen, white, (c * tile_size, 0), (c * tile_size, screen_height - margin))
		pygame.draw.line(screen, white, (0, c * tile_size), (screen_width, c * tile_size))

'''
The draw_world function displays the game world on the screen. It uses data from world_data to determine which blocks to display and in which location.
'''
def draw_world():
	'''
 	The work process:
 	:for each row in the range from 0 to 19:
	:for each column in the range from 0 to 19:
 	:if the value in world_data for this row and column is greater than 0:
  	:if the value is 1 - create a dirt_img image in size (tile_size, tile_size), display the image on the screen in position (col * tile_size, row * tile_size)
   	:if the value is 2 - create a grass_img image in size (tile_size, tile_size), display the image on the screen in position (col * tile_size, row * tile_size)
	:if the value is 6 - create a lava_img image with the size (tile_size, tile_size // 2), display the image on the screen at the position (col * tile_size, row * tile_size + (tile_size // 2))
 	:if the value is 8 - create an exit_img image with the size (tile_size, int(tile_size * 1.5)), display the image on the screen at the position (col * tile_size, row * tile_size - (tile_size // 2))
 	'''
	for row in range(20):
		for col in range(20):
			if world_data[row][col] > 0:
				if world_data[row][col] == 1:
					#block
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 2:
					#block_snow
					img = pygame.transform.scale(grass_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))

				if world_data[row][col] == 6:
					#lava
					img = pygame.transform.scale(lava_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size, row * tile_size + (tile_size // 2)))

				if world_data[row][col] == 8:
					#exit
					img = pygame.transform.scale(exit_img, (tile_size, int(tile_size * 1.5)))
					screen.blit(img, (col * tile_size, row * tile_size - (tile_size // 2)))
				
'''
py:class:: Button
Represents a button with a specific image and behavior.
'''
class Button():
	'''
 	:py:method:: __init__(x, y, image)

        Initialize the Button.

        :param x: The x-coordinate of the button
        :type x: int
        :param y: The y-coordinate of the button
        :type y: int
        :param image: The image of the button
        :type image: pygame.Surface
 	'''
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	'''
 	:py:method:: draw()

        Draw the button and handle the user's actions.

        :return: action - Indicates if the button has been clicked
        :rtype: boolean
 	'''
	def draw(self):
		action = False

		'''
  		Mouse's position
  		'''
		pos = pygame.mouse.get_pos()

		'''
		check mouseover and clicked conditions
  		'''
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		'''
 		draw button
  		'''
		screen.blit(self.image, (self.rect.x, self.rect.y))

		return action

'''
create and save buttons
'''
save_button = Button(screen_width // 2 - 150, screen_height - 80, save_img)
load_button = Button(screen_width // 2 + 50, screen_height - 80, load_img)

'''
Main game loop
'''
run = True
while run:

	clock.tick(fps)

	'''
 	:background
 	'''
	screen.fill(green)
	screen.blit(bg_img, (0, 0))

	'''
	load and save level
	'''
	if save_button.draw():
		
		'''
  		save level data
  		'''
		pickle_out = open(f'level{level}_data', 'wb')
		pickle.dump(world_data, pickle_out)
		pickle_out.close()
		
	if load_button.draw():
		
		'''
		load in level data
		'''
		if path.exists(f'level{level}_data'):
			pickle_in = open(f'level{level}_data', 'rb')
			world_data = pickle.load(pickle_in)

	'''
	show the grid and draw the level tiles
	'''
	draw_grid()
	draw_world()


	'''
	text showing current level
	'''
	draw_text(f'Level: {level}', font, white, tile_size, screen_height - 60)
	draw_text('Press UP or DOWN to change level', font, white, tile_size, screen_height - 40)

	'''
	event handler
	'''
	for event in pygame.event.get():
		
		'''
  		quit game
  		'''
		if event.type == pygame.QUIT:
			run = False
			
		'''
  		mouseclicks to change tiles
  		'''
		if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
			clicked = True
			pos = pygame.mouse.get_pos()
			x = pos[0] // tile_size
			y = pos[1] // tile_size

			'''
   			check that the coordinates are within the tile area
   			'''
			if x < 20 and y < 20:

				'''
				update tile value
				'''
				if pygame.mouse.get_pressed()[0] == 1:
					world_data[y][x] += 1
					if world_data[y][x] > 8:
						world_data[y][x] = 0
				elif pygame.mouse.get_pressed()[2] == 1:
					world_data[y][x] -= 1
					if world_data[y][x] < 0:
						world_data[y][x] = 8
		if event.type == pygame.MOUSEBUTTONUP:
			clicked = False
		'''
  		up and down key presses to change level number
  		'''
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			elif event.key == pygame.K_DOWN and level > 1:
				level -= 1

	'''
 	update game display window
 	'''
	pygame.display.update()

pygame.quit()
