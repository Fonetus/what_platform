import pygame
from pygame.locals import *
import pickle
from os import path

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
level = 1
max_levels = 7

# Load images
bg_img = pygame.image.load('img/blue.png')
restart_img = pygame.image.load('img/restart.png')
start_img = pygame.image.load('img/start.png')
exit_img = pygame.image.load('img/exit.png')

# Function to reset level
def reset_level(level):
	player.reset(100, screen_height - 130)
	lava_group.empty()
	exit_group.empty()
	
	if path.exists(f'level{level}_data'):
	    pickle_in = open(f'level{level}_data', 'rb')
	    world_data = pickle.load(pickle_in)
		
	world = World(world_data)
	
	return world
	

class Button():
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
	def __init__(self, x, y):
		self.reset(x, y)
		
	def update(self, game_over):
		dx = 0
		dy = 0
		walk_cooldown = 5
		
		if game_over == 0:
			# Get keypresses
			key = pygame.key.get_pressed()
			
			if key[pygame.K_UP] and self.jumped == False and self.in_air == False:
				self.vel_y = -15
				self.jumped = True
				
			if key[pygame.K_UP] == False:
				self.jumped = False
				
			if key[pygame.K_LEFT]:
				dx -= 5
				self.counter += 1
				self.direction = -1
				
			if key[pygame.K_RIGHT]:
				dx += 5
				self.counter += 1
				self.direction = 1
				
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
			# Check for collision with exit
			if pygame.sprite.spritecollide(self, exit_group, False):
				game_over = 1
		
			# Update player coordinates
			self.rect.x += dx
			self.rect.y += dy

		elif game_over == -1:
			self.image = self.dead_image
			
			if self.rect.y > -50:
				self.rect.y -= 5
				
		# Draw player onto screen
		screen.blit(self.image, self.rect)
		pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

		return game_over

	def reset(self, x, y):
		self.images_right = []
		self.images_left = []
		self.index = 0
		self.counter = 0
		
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
	def __init__(self, data):
		self.tile_list = []

		# Load images
		dirt_img = pygame.image.load('img/block.png')
		grass_img = pygame.image.load('img/block_snow.png')

		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1: #block
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
					
				if tile == 2: #block_snow
					img = pygame.transform.scale(grass_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
					
				if tile == 6: #lava
					lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
					lava_group.add(lava)
					
				if tile == 8: 
					exit = Exit(col_count * tile_size, row_count * tile_size)
					exit_group.add(exit)
				
				col_count += 1
			row_count += 1

	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])
			pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)


class Lava(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/lava.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


class Exit(pygame.sprite.Sprite):
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
'''заимств'''
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

	if main_menu == True:
		if exit_button.draw():
			run = False
		if start_button.draw():
			main_menu = False
			
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
					level = 1 
					# Reset level
					world_data = []
					world = reset_level(level)
					game_over = 0 
				
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()
