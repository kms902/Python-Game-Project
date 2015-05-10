# game_class_example.py
# CURRENT - player box can move with arrow keys!
# Working on - create bullet/arrow sprite that
# fires linearly towards the mouse.
# Problem: The good: Arrow fires away from the player and on a line towards the
# mouse cursor. The bad: the arrow's speed changes based on the distance between
# the mouse and the player, and the arrow even changes directions if the player
# moves.

import pygame
import random

# Global Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500

# Classes

class Block(pygame.sprite.Sprite):
	""" This class represents a simple block the player collects. """
	def __init__(self):
		super().__init__()
		self.image = pygame.Surface([20,20])
		self.image.fill(BLACK)
		self.rect = self.image.get_rect()

	def reset_pos(self):
		""" Called when the block is 'collected' or falls off the screen. """
		self.rect.y = random.randrange(-300, -20)
		self.rect.x = random.randrange(SCREEN_WIDTH)

	def update(self):
		""" Automatically called when we need to move the block. """
		self.rect.y += 1

		if self.rect.y > SCREEN_HEIGHT + self.rect.height:
			self.reset_pos()

class Player(pygame.sprite.Sprite):
	""" This class represents the player. """
	def __init__(self):
		super().__init__()
		self.image = pygame.Surface([20,20])
		self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.change_x = 0
		self.change_y = 0

	def update(self):
		""" Update player location """
		self.rect.x += self.change_x
		self.rect.y += self.change_y

	# Player-controlled movement:
	def go_left(self):
		""" Called when the user hits the left arrow. """
		self.change_x = -3

	def go_right(self):
		self.change_x = 3

	def go_up(self):
		self.change_y = -3

	def go_down(self):
		self.change_y = 3

	def stop_x(self):
		""" Called when the user lets off the keyboard. """
		self.change_x = 0
	
	def stop_y(self):
		self.change_y = 0

class Arrow(pygame.sprite.Sprite):
	""" This class represents the bullet. """
	def __init__(self):
		# Call the parent class (Sprite) constructor
		super().__init__()

		self.image = pygame.Surface([4,5])
		self.image.fill(BLACK)

		self.rect = self.image.get_rect()

		# Get the current mouse position. This returns the position
		# as a list of two numbers
		self.pos = pygame.mouse.get_pos()

		self.change_x = 0
		self.change_y = 0

	def update(self):
		""" Move the bullet. """
		self.change_y = self.pos[1] - Game.player.rect.y
		self.change_x = self.pos[0] - Game.player.rect.x 
		self.rect.x += self.change_x
		self.rect.y += self.change_y

class Game(object):
	""" This class represents an instance of the game. If we need to reset
	the game, we'd just need to create a new instance of this class.  """
	def __init__(self):
		self.score = 0
		self.game_over = False

		# Create sprite lists
		self.block_list = pygame.sprite.Group()
		self.all_sprites_list = pygame.sprite.Group()
		self.arrow_list = pygame.sprite.Group()

		# Create the block sprites
		for i in range(50):
			block = Block()

			block.rect.x = random.randrange(SCREEN_WIDTH)
			block.rect.y = random.randrange(-300, SCREEN_HEIGHT)

			self.block_list.add(block)
			self.all_sprites_list.add(block)

		# Create the player
		"""
		# Huge problem was solved here
		# Used to say:
		self.player = Player()
		but this was creating the player object on a scope too small to
		use in other methods. I believe the scope became instance.
		Whereas with Game.player = Player(), the scope became static variable. 
		"""
		Game.player = Player()
		self.all_sprites_list.add(self.player)
		self.arrow = Arrow()

	def process_events(self):
		""" Process all of the events. Return a "True" if we need to close the window. """

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					same.player.go_left()
				if event.key == pygame.K_RIGHT:
					self.player.go_right()
				if event.key == pygame.K_UP:
					self.player.go_up()
				if event.key == pygame.K_DOWN:
					self.player.go_down()
			if event.type == pygame.KEYUP:
			# If it is an arrow key, reset vector back to zero
				if event.key == pygame.K_LEFT:
					self.player.stop_x()
				if event.key == pygame.K_RIGHT:
					self.player.stop_x()
				if event.key == pygame.K_UP:
					self.player.stop_y()
				if event.key == pygame.K_DOWN:
					self.player.stop_y()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.game_over:
					self.__init__()
				else:
					self.arrow = Arrow()
					# Set the arrow so it is where the player is
					self.arrow.rect.x = self.player.rect.x
					self.arrow.rect.y = self.player.rect.y
					# Add the bullet to the lists
					self.all_sprites_list.add(self.arrow)
					self.arrow_list.add(self.arrow)
					#arrow_list.add(arrow)

		return False

	def run_logic(self):
		"""
		This method is run each time through the frame. It 
		updates positions and checks for collisions.
		"""
		if not self.game_over:
			# Move all the sprites
			self.all_sprites_list.update()

			# See if the arrow block has collided with anything and add collided 
			# blocks to a list. The dokill argument is a bool. If set to True, all 
			# sprites that collide will be removed from the Group.
			blocks_hit_list = pygame.sprite.spritecollide(self.arrow, self.block_list, True)

			# Check the list of collisions.
			for block in blocks_hit_list:
				self.arrow_list.remove(self.arrow)
				self.all_sprites_list.remove(self.arrow)
				self.score += 1
				print(self.score)
				# You can do something with "block" here

			if len(self.block_list) == 0:
				self.game_over = True

	def display_frame(self, screen):
		""" Display everything to the screen for the game. """
		screen.fill(WHITE)

		if self.game_over:
			# font = pygame.font.Font("Serif", 25)
			font = pygame.font.SysFont("serif", 25)
			text = font.render("Game Over, click to restart", True, BLACK)
			center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
			center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
			screen.blit(text, [center_x, center_y])

		if not self.game_over:
			self.all_sprites_list.draw(screen)

		pygame.display.flip()

def main():
	""" Main program function. """
	# Initialize Pygame and set up the window
	pygame.init()

	size = [SCREEN_WIDTH, SCREEN_HEIGHT]
	screen = pygame.display.set_mode(size)

	pygame.display.set_caption("Simple RPG")
	pygame.mouse.set_visible(True)

	# Create our objects and set the data
	done = False
	clock = pygame.time.Clock()

	# Create an instance of the Game class
	game = Game()

	# Main game loop
	while not done:

		# Process events (keystrokes, mouse clicks, etc)
		done = game.process_events()

		# Update object positions, check for collisions
		game.run_logic()

		# Draw the current frame
		game.display_frame(screen)

		# Pause for the next frame
		clock.tick(30)

	# Close window and exit
	pygame.quit()

# Call the main function, start up the game
if __name__ == "__main__":
	main()

