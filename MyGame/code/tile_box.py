import pygame
from tile_movingbox import MovingBox

def check_if_box(block):
    if type(block) is Box:
        return True
    elif type(block) is JumpBox:
        return True
    elif type(block) is MovingBox:
        return True
    return False
 
def static_boxes(box_list):
	for box in box_list.sprites():
         if box.state == 'AIR':
             return False
	return True
 
class Box(pygame.sprite.Sprite):
    spd_x = 0
    spd_y = 0
    def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load('images/tiles/box.png').convert()
		self.rect = self.image.get_rect()		
		self.rect.x = x
		self.rect.y = y
		self.state = 'STOP'
		
		self.init_x = x
		self.init_y = y
	
    def reboot(self, movement):
		self.rect.x = self.init_x
		self.rect.y = self.init_y
		self.spd_y = 0
		self.spd_x = 0
		self.state = 'STOP'
		
    def calc_movement(self, movement): 
		if movement == 'UP':
			if not self.touch_UP() and self.spd_y == 0:
				self.spd_y = -4
				self.state = 'AIR'
		elif movement == 'DN':
			if not self.touch_DN() and self.spd_y == 0:
				self.spd_y = 4
				self.state = 'AIR'
		elif movement == 'RI':
			if not self.touch_RI() and self.spd_y == 0:
				self.spd_x = 4
				self.state = 'AIR'
		elif movement == 'LE':
			if not self.touch_LE() and self.spd_y == 0:
				self.spd_x = -4
				self.state = 'AIR'
		
    def touch_UP(self):
		self.rect.y -=1
		hit_list = pygame.sprite.spritecollide(self, self.level, False)
		self.rect.y +=1
		if len(hit_list) <= 1:
			return False
		return True
    def touch_DN(self):
		self.rect.y +=1
		hit_list = pygame.sprite.spritecollide(self, self.level, False)
		self.rect.y -=1
		if len(hit_list) <= 1:
			return False
		return True
    def touch_RI(self):
		self.rect.x +=1
		hit_list = pygame.sprite.spritecollide(self, self.level, False)
		self.rect.x -=1
		if len(hit_list) <= 1:
			return False
		return True	
    def touch_LE(self):
		self.rect.x -=1
		hit_list = pygame.sprite.spritecollide(self, self.level, False)
		self.rect.x +=1
		if len(hit_list) <= 1:
			return False
		return True
	
    def collision_y(self):
		hit_list = pygame.sprite.spritecollide(self, self.level, False)
		for block in hit_list:
			if block.ID != self.ID:
				if self.spd_y > 0:
					self.rect.bottom = block.rect.top
				elif self.spd_y < 0:
					self.rect.top = block.rect.bottom
				self.spd_y = 0
				self.state = 'STOP'
    
    def collision_x(self):
		hit_list = pygame.sprite.spritecollide(self, self.level, False)
		for block in hit_list:
			if block.ID != self.ID:
				if self.spd_x > 0:
					self.rect.right = block.rect.left
				elif self.spd_x < 0:
					self.rect.left = block.rect.right
				self.spd_x = 0
				self.state = 'STOP'	
	
    def update(self, movement):
        if type(self) == JumpBox:
            pass
        elif self.state == 'STOP':
            self.calc_movement(movement)
        else:
		self.rect.y += self.spd_y          
		self.collision_y()
			
		self.rect.x += self.spd_x
		self.collision_x()

		
class JumpBox(Box):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load('images/tiles/jumpbox.png').convert()
		self.rect = self.image.get_rect()		
		self.rect.x = x
		self.rect.y = y
		self.state = 'STOP'
		
		self.init_x = x
		self.init_y = y

class Box_Stopper(pygame.sprite.Sprite):
	spd_x = 0
	spd_y = 0
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load('images/tiles/boxfilter.png').convert_alpha()
		self.rect = self.image.get_rect()		
		self.rect.y = y
		self.rect.x = x