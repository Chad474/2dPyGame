import pygame

class MovingBox(pygame.sprite.Sprite):
    spd_x = 0
    spd_y = 0
    def __init__(self, x, y, typebox):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/tiles/rock.png').convert_alpha()
        self.rect = self.image.get_rect()		
        self.rect.y = y
        self.rect.x = x
        self.init_x = x
        self.init_y = y
        self.state = 'STOP'
        self.move_spd = 60
        self.frame = 0
        self.switch = 'LE'
        if typebox == 'H':
            self.move_type = 'H'
            self.move_dir = ['LE','RI']
            self.move_frame = [0,2]
        elif typebox == 'V':
            self.move_type = 'V'
            self.move_dir = ['DN','UP']
            self.move_frame = [3,1]
                      
    def update(self):
            if self.state == 'STOP':
                self.switch = self.update_dir()
                if self.move_type == 'H':
                    self.calc_movement_H(self.switch)
                elif self.move_type == 'V':
                    self.calc_movement_V(self.switch)
                    
            self.rect.y += self.spd_y
            self.collision_y()
            self.rect.x += self.spd_x
            self.collision_x()
    
    def update_dir(self):
        self.frame += 1
        #print self.frame
        for i in range(len(self.move_frame)):
            if self.frame % (self.move_spd * len(self.move_frame)) == i*self.move_spd:
                return self.move_dir[i]
        
        #if self.frame % 2 == 0:
         #       return self.move_dir[0]
        #else:
         #       return self.move_dir[1]
        
            
        
    def collision_x(self):
		hit_list = pygame.sprite.spritecollide(self, self.level, False)
		for moving_block in hit_list:
			if moving_block.ID != self.ID:
				if self.spd_x > 0:
					self.rect.right = moving_block.rect.left
				elif self.spd_x < 0:
					self.rect.left = moving_block.rect.right
				self.spd_x = 0
				self.state = 'STOP'
    
    def collision_y(self):
		hit_list = pygame.sprite.spritecollide(self, self.level, False)
		for moving_block in hit_list:
			if moving_block.ID != self.ID:
				if self.spd_y > 0:
					self.rect.bottom = moving_block.rect.top
				elif self.spd_y < 0:
					self.rect.top = moving_block.rect.bottom
				self.spd_y = 0
				self.state = 'STOP'

    def reboot(self, nothing):
		self.rect.x = self.init_x
		self.rect.y = self.init_y
		self.spd_y = 0
		self.spd_x = 0
		self.state = 'STOP'
		self.frame = 0
  
    def calc_movement_H(self, movement): 
		if movement == 'RI':
			if not self.touch_RI() and self.spd_x == 0:
				self.spd_x = 4
				self.state = 'AIR'
		elif movement == 'LE':
			if not self.touch_LE() and self.spd_x == 0:
				self.spd_x = -4
				self.state = 'AIR'
    
    def calc_movement_V(self, movement):
		if movement == 'UP':
			if not self.touch_UP() and self.spd_y == 0:
				self.spd_y = -4
				self.state = 'AIR'
		elif movement == 'DN':
			if not self.touch_DN() and self.spd_y == 0:
				self.spd_y = 4
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