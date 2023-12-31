import pygame
from pygame.locals import *
from pygame import mixer
import pickle
from os import path

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

# Define game variables
tile_size = 50
game_over = 0
main_menu = True
level = 0
max_levels = 2

# Load images
bg_img = pygame.image.load('img/blue.png')
restart_img = pygame.image.load('img/restart.png')
start_img = pygame.image.load('img/start.png')
exit_img = pygame.image.load('img/exit.png')

# Music and sounds
pygame.mixer.music.load('sound/music.wav')
pygame.mixer.music.play(-1, 0.0, 5000)
jump_fx = pygame.mixer.Sound('sound/jump.wav')
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound('sound/game_over.wav')
game_over_fx.set_volume(0.5)

# Function to reset level
def reset_level(level):
	'''
 	function:: reset_level(level)
   	Return the character, lava, exit to the beginning
   	:param level: The level to be reset
   	:return: world
 	'''
	# Return the character, lava, exit to the beginning
	player.reset(100, screen_height - 130)
	lava_group.empty()
	exit_group.empty()

	# Сhecking the existence of a file
	if path.exists(f'level{level}_data'):
	    pickle_in = open(f'level{level}_data', 'rb')
	    world_data = pickle.load(pickle_in)
		
	world = World(world_data)
	
	return world
	

class Button():
	'''
 	class:: Button
   	Button initialisation
   	This class represents a button in a GUI. It provides methods for drawing the button and detecting mouse clicks on it.
	:param x: The x-coordinate of the button
	:param y: The y-coordinate of the button
	:param image: The image to be displayed on the button
	:ivar image: The image to be displayed on the button
	:ivar rect: The rectangular area occupied by the button
	:ivar clicked: A boolean indicating whether the button has been clicked
	.. method:: draw()
      	Draws the button on the screen and detects mouse clicks on the button.
      	:return: action
 	'''
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False

	def draw(self):
		action = False

		# Get mouse position
		pos = pygame.mouse.get_pos()

		# Check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		# Draw button
		screen.blit(self.image, self.rect)

		return action


class Player():
	'''
	class:: Player
   	Player initialisation
   	This class represents the player character in the game. It provides methods for updating the player's position and resetting the player.
	:ivar images_right: List of images for the player character facing right
	:ivar images_left: List of images for the player character facing left
	:ivar index: Index of the current image in the player's animation
	:ivar counter: Counter for animating the player's walk cycle
	:ivar dead_image: Image to be displayed when the player character is dead
	:ivar image: The current image displayed for the player
	:ivar rect: The rectangular area occupied by the player
	:ivar width: Width of the player's image
	:ivar height: Height of the player's image
	:ivar vel_y: Vertical velocity of the player
	:ivar jumped: Boolean indicating whether the player has jumped
	:ivar direction: Direction the player is facing
	:ivar in_air: Boolean indicating whether the player is currently in the air
   	.. method:: __init__(x, y)
      	Initializes the player character with the specified x and y coordinates.
   	.. method:: update(game_over)
      	Updates the player's position and handles player movement based on keyboard input.
	:param game_over: The game over status
	:type game_over: int
	:return: game_over
	.. method:: reset(x, y)
      	Resets the player's properties and images to their initial state.
	:param x: The initial x-coordinate of the player
	:param y: The initial y-coordinate of the player
 	'''
	def __init__(self, x, y):
		self.reset(x, y)
		
	def update(self, game_over):
		dx = 0
		dy = 0
		walk_cooldown = 5
		
		if game_over == 0:
			# Get keypresses
			key = pygame.key.get_pressed()
			
			# Jump
			if key[pygame.K_UP] and self.jumped == False and self.in_air == False:
				jump_fx.play()
				self.vel_y = -15
				self.jumped = True
				
			if key[pygame.K_UP] == False:
				self.jumped = False
				
			# Move left	
			if key[pygame.K_LEFT]:
				dx -= 5
				self.counter += 1
				self.direction = -1

			# Move right
			if key[pygame.K_RIGHT]:
				dx += 5
				self.counter += 1
				self.direction = 1

			# Stop
			if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
				self.counter = 0
				self.index = 0
				
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]

			# Handle animation
			if self.counter > walk_cooldown:
				self.counter = 0	
				self.index += 1
				
				if self.index >= len(self.images_right):
					self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]

			# Add gravity
			self.vel_y += 1
			if self.vel_y > 10:
				self.vel_y = 10
			dy += self.vel_y
			# Check for collision
			self.in_air = True
			
			for tile in world.tile_list:
			# Check for collision in x direction
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				# Check for collision in y direction
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					
					# Check if below the ground i.e. jumping
					if self.vel_y < 0:
						dy = tile[1].bottom - self.rect.top
						self.vel_y = 0
					# Check if above the ground i.e. jumping
					elif self.vel_y >= 0:
						dy = tile[1].top - self.rect.bottom
						self.vel_y = 0
						self.in_air = False
						
			# Check for collision with lava
			if pygame.sprite.spritecollide(self, lava_group, False):
				game_over = -1
				game_over_fx.play()
			# Check for collision with exit
			if pygame.sprite.spritecollide(self, exit_group, False):
				game_over = 1
		
			# Update player coordinates
			self.rect.x += dx
			self.rect.y += dy
		# Players death
		elif game_over == -1:
			self.image = self.dead_image
			
			if self.rect.y > -50:
				self.rect.y -= 5
				
		# Draw player on the screen
		screen.blit(self.image, self.rect)

		return game_over

	def reset(self, x, y):
		self.images_right = []
		self.images_left = []
		self.index = 0
		self.counter = 0

		# Sprite
		for num in range(1, 5):
			img_right = pygame.image.load(f'img/frog{num}.png')
			img_right = pygame.transform.scale(img_right, (45, 50))
			img_left = pygame.transform.flip(img_right, True, False)
			self.images_right.append(img_right)
			self.images_left.append(img_left)

		self.dead_image = pygame.image.load('img/ghost.png')
		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.jumped = False
		self.direction = 0
		self.in_air = True


class World():
	'''
 	.. class:: World
   	A class for the level editor.
   	.. method:: init(data)
      	Initializes the World object with the given data.
      	:param data: The data for the level.
      	:type data: list of lists
   	.. method:: draw()
      	Draws the level.
 	'''
	def __init__(self, data):
		self.tile_list = []

		# Load images
		dirt_img = pygame.image.load('img/block.png')
		grass_img = pygame.image.load('img/block_snow.png')

		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				# Block
				if tile == 1: 
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)

				# Block with snow
				if tile == 2: 
					img = pygame.transform.scale(grass_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)

				# Lava
				if tile == 6: 
					lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
					lava_group.add(lava)

				# Exit
				if tile == 8: 
					exit = Exit(col_count * tile_size, row_count * tile_size)
					exit_group.add(exit)
				
				col_count += 1
			row_count += 1

	# Draw level
	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])


class Lava(pygame.sprite.Sprite):
	'''
 	.. class:: Lava
   	A class for representing lava sprite.
   	.. method:: init(x, y)
      	Initializes the Lava object with the given coordinates.
      	:param x: The x-coordinate of the lava.
      	:type x: int
      	:param y: The y-coordinate of the lava.
      	:type y: int
 	'''
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/lava.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


class Exit(pygame.sprite.Sprite):
	'''
 	.. class:: Exit
   	A class for representing the exit sprite.
   	.. method:: init(x, y)
      	Initializes the Exit object with the given coordinates.
      	:param x: The x-coordinate of the exit.
      	:type x: int
      	:param y: The y-coordinate of the exit.
      	:type y: int
 	'''
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/portal.png')
		self.image = pygame.transform.scale(img, (tile_size, int(tile_size)))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

player = Player(100, screen_height - 130)

lava_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

# Load in level data and create world 
if path.exists(f'level{level}_data'):
    pickle_in = open(f'level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)

world = World(world_data)

#Create buttons
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 - 350, screen_height // 2.5, start_img)
exit_button = Button(screen_width // 2 + 150, screen_height // 2.5, exit_img)

run = True
while run:
	clock.tick(fps)
	screen.blit(bg_img, (0, 0))

	# Start main menu
	if main_menu == True:
		if exit_button.draw():
			run = False
		if start_button.draw():
			main_menu = False

	# Start level
	else:
		world.draw()
		lava_group.draw(screen)
		exit_group.draw(screen)
		game_over = player.update(game_over)
		
		# If player has died
		if game_over == -1:
			if restart_button.draw():
				world_data = []
				world = reset_level(level)
				game_over = 0

		# If player has completed the level
		if game_over == 1:
			# Reset game and go to next level 
			level += 1
			if level <= max_levels:
				# Reset level
				world_data = []
				world = reset_level(level)
				game_over = 0
				
			else:
				if restart_button.draw():
					level = 0 
					# Reset level
					world_data = []
					world = reset_level(level)
					game_over = 0 
				
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()
