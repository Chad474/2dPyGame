import pygame
class Carrot(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('images/tiles/carrot.png').convert_alpha()
		self.rect = self.image.get_rect()		
		self.rect.y = y
		self.rect.x = x
