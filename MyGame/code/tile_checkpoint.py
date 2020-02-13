import pygame
from constants import COLOR_KEY

class Checkpoint(pygame.sprite.Sprite):
	spd_x = 0
	spd_y = 0
	def __init__(self, x, y):
          pygame.sprite.Sprite.__init__(self)
		
          self.on = False
          self.off_img = pygame.image.load('images/tiles/checkpoint1.png').convert()
          self.off_img.set_colorkey(COLOR_KEY)
          self.on_img = pygame.image.load('images/tiles/checkpoint2.png').convert()
          self.on_img.set_colorkey(COLOR_KEY)
          self.image = self.off_img
          self.rect = self.image.get_rect()		
          self.rect.y = y
          self.rect.x = x
		
	def reboot(self):
		self.on = False
		self.image = self.off_img

	def update(self):
         if self.on:
            self.image = self.on_img
			
