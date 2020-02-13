import pygame
import constants as F
import tile_box as box
import tile_spike as spike
import tile_carrot as Carrot
import tile_checkpoint as Checkpoint
import tile_movingbox as moving_box

class Player(pygame.sprite.Sprite):
    spd_x = 0
    spd_y = 0
    level = None
    
    def __init__(self, x_init, y_init):
        pygame.sprite.Sprite.__init__(self)
        
        self.load_images()
        self.set_states()
        
        self.image = pygame.image.load('images/player/placeholder.png').convert()
        self.rect = self.image.get_rect()
        self.image = self.jump_ani[4]
        self.jump_ani_frame = 25
        
        self.rect.x = x_init + 8
        self.rect.y = y_init
        
        self.init_x = self.rect.x
        self.init_y = self.rect.y
    
    def set_states(self):
        self.state = 'Stand'
        self.air = True
        self.direction = 'Right'
        self.dead = False
        self.win = False
        self.bounce = False
        
    def load_images(self):
        sheet = pygame.image.load('images/player/monkeybot.png').convert()
		
        self.stand_image = F.split(sheet, 0, 0, 32, 32)
        self.stand_image.set_colorkey(F.COLOR_KEY)

        self.dead_image = F.split(sheet, 0, 104, 32, 32)
        self.dead_image.set_colorkey(F.COLOR_KEY)
        self.walk_ani = []
        self.walk_ani_frame = 0   
        img1 = (F.split(sheet, 32, 0, 32, 32).convert())
        img1.set_colorkey(F.COLOR_KEY)
        self.walk_ani.append(img1)
        img2 = (F.split(sheet, 64, 0, 32, 32).convert())
        img2.set_colorkey(F.COLOR_KEY)
        self.walk_ani.append(img2)
        img3 = (F.split(sheet, 96, 0, 32, 32).convert())
        img3.set_colorkey(F.COLOR_KEY)
        self.walk_ani.append(img3)
        img4 = (F.split(sheet, 32, 32, 32, 32).convert())
        img4.set_colorkey(F.COLOR_KEY)        
        self.walk_ani.append(img4)
        img5 = (F.split(sheet, 64, 32, 32, 32).convert())
        img5.set_colorkey(F.COLOR_KEY)
        self.walk_ani.append(img5)
        img6 = (F.split(sheet, 96, 32, 32, 32).convert())
        img6.set_colorkey(F.COLOR_KEY)
        self.walk_ani.append(img6)        

        self.jump_ani = self.walk_ani
        self.jump_ani_frame = 0
        img1 = (F.split(sheet, 32, 72, 32, 32).convert())
        img1.set_colorkey(F.COLOR_KEY)
        self.jump_ani.append(img1)  
        img2 = (F.split(sheet, 64, 72, 32, 32).convert())
        img2.set_colorkey(F.COLOR_KEY)
        self.jump_ani.append(img2)
        self.jump_ani.append(img2)
        img3 = (F.split(sheet, 96, 72, 32, 32).convert())
        img3.set_colorkey(F.COLOR_KEY)
        self.jump_ani.append(img3)
        self.jump_ani.append(img3)
           
    def reboot(self, grav):
        self.dead = False
        self.bounce = False
        self.image = self.stand_image
        self.direction = 'Right'
        self.state = 'Stand'
        self.image = self.jump_ani[4]
        self.jump_ani_frame = 25
        self.spd_y = 0
        self.spd_x = 0
        self.rect.x = self.init_x
        self.rect.y = self.init_y
    		
    def touch_N(self, colis):
    	self.rect.y -=1
    	hit_list = pygame.sprite.spritecollide(self, self.level, False)
    	self.rect.y +=1
    	if len(hit_list) == colis:
    		return False
    	return True
     
    def touch_S(self, colis):
        self.rect.y +=1
        hit_list = pygame.sprite.spritecollide(self, self.level, False)
        self.rect.y -=1
        if len(hit_list) == colis:
            return False		
        return True
        
    def touch_E(self, colis):
    	self.rect.x +=1
    	hit_list = pygame.sprite.spritecollide(self, self.level, False)
    	self.rect.x -=1
    	if len(hit_list) == colis:
    		return False
    	return True	
     
    def touch_O(self, colis):
    	self.rect.x -=1
    	hit_list = pygame.sprite.spritecollide(self, self.level, False)
    	self.rect.x +=1
    	if len(hit_list) == colis:
    		return False
    	return True

    def crush(self):
	hit_list = pygame.sprite.spritecollide(self, self.level, False)
	colis = len(hit_list)
	if colis >= 3:
		self.dead = True
		return True
	elif colis == 2:
		if box.check_if_box(hit_list[0]) and box.check_if_box(hit_list[1]):
			bloxy = hit_list[1]
			if bloxy.spd_x > 0:
				self.rect.left = bloxy.rect.right
			elif bloxy.spd_x < 0:
				self.rect.right = bloxy.rect.left
			elif bloxy.spd_y > 0:
				self.spd_y = 0
				self.rect.top = bloxy.rect.bottom
			elif bloxy.spd_y < 0:
				self.spd_y = 0
				self.rect.bottom = bloxy.rect.top
				self.air = False
				self.walk_ani_frame = 0
				self.image = self.stand_image
				if self.direction == 'Left':
					self.image = pygame.transform.flip(self.image, True, False)
				
		else:
			self.dead = True
			return True
	elif colis == 1:
		bloxy = hit_list[0]
		if bloxy.spd_x > 0 and not self.touch_E(colis):
			self.rect.left = bloxy.rect.right
		elif bloxy.spd_x < 0 and not self.touch_O(colis):
			self.rect.right = bloxy.rect.left	
		elif bloxy.spd_y > 0 and not self.touch_S(colis):
			self.spd_y = 0
			self.rect.top = bloxy.rect.bottom
		elif bloxy.spd_y < 0 and not self.touch_N(colis):
			self.spd_y = 0
			self.rect.bottom = bloxy.rect.top
			self.air = False
			self.walk_ani_frame = 0
			self.image = self.stand_image
			if self.direction == 'Left':
				self.image = pygame.transform.flip(self.image, True, False)
		elif bloxy.spd_y < 0 and self.spd_y > 0:
			self.spd_y = 0
			self.rect.bottom = bloxy.rect.top
			self.air = False
			self.walk_ani_frame = 0
			self.image = self.stand_image
			if self.direction == 'Left':
				self.image = pygame.transform.flip(self.image, True, False)
		elif bloxy.spd_y > 0 and self.spd_y < 0:
			self.spd_y = 0
			self.rect.top = bloxy.rect.bottom
		elif bloxy.spd_y < 0 and self.spd_y < 0:
			self.spd_y = 0
			if bloxy.rect.y > self.rect.y:
				self.rect.bottom = bloxy.rect.top
			else:
				self.rect.top = bloxy.rect.bottom
		
		else:
			self.dead = True
			return True
			
    	return False
     
    def touch_death(self):
    	self.rect.y -=1
    	hit_list = pygame.sprite.spritecollide(self, self.level, False)
    	self.rect.y +=1
    	if len(hit_list) > 0:
    		for hit in hit_list:
    			if type(hit) is spike.Spike:
    				return True
    	self.rect.y +=1
	hit_list = pygame.sprite.spritecollide(self, self.level, False)
	self.rect.y -=1
	if len(hit_list) > 0:
		for hit in hit_list:
			if type(hit) is spike.Spike:
				return True
	self.rect.x -=1
	hit_list = pygame.sprite.spritecollide(self, self.level, False)
	self.rect.x +=1
	if len(hit_list) > 0:
		for hit in hit_list:
			if type(hit) is spike.Spike:
				return True
	self.rect.x +=1
	hit_list = pygame.sprite.spritecollide(self, self.level, False)
	self.rect.x -=1
	if len(hit_list) > 0:
		for hit in hit_list:
			if type(hit) is spike.Spike:
				return True 
    
    def out_screen_death(self):
    	if self.rect.top >= F.SCREEN_HEIGHT:
    		return True
    	elif self.rect.bottom <= 0:
    		return True
    	elif self.rect.left >= F.SCREEN_WIDTH:
    		return True
    	elif self.rect.right <= 0:
    		return True
    	return False
     
    def death(self):
    	if self.crush() or self.touch_death() or self.out_screen_death():
    		self.dead = True

    
    def jumpbox(self):
    	self.rect.y -=1
    	hit_list = pygame.sprite.spritecollide(self, self.level, False)
    	self.rect.y +=1
    	if len(hit_list) > 0:
		for hit in hit_list:
			if type(hit) is box.JumpBox:
				self.spd_y = 6
				self.air = True
				self.jump_ani_frame = 24
	self.rect.y +=1
	hit_list = pygame.sprite.spritecollide(self, self.level, False)
	self.rect.y -=1
	if len(hit_list) > 0:
		for hit in hit_list:
			if type(hit) is box.JumpBox:
				self.spd_y = -6
				self.air = True
				self.jump_ani_frame = 0
	self.rect.x -=1
	hit_list = pygame.sprite.spritecollide(self, self.level, False)
	self.rect.x +=1
	if len(hit_list) > 0:
		for hit in hit_list:
			if type(hit) is box.JumpBox:
				self.bounce = True
				self.spd_x = 4
				self.air = True
				self.jump_ani_frame = 24
	self.rect.x +=1
	hit_list = pygame.sprite.spritecollide(self, self.level, False)
	self.rect.x -=1
	if len(hit_list) > 0:
		for hit in hit_list:
			if type(hit) is box.JumpBox:
				self.bounce = True
				self.spd_x = -4
				self.air = True
				self.jump_ani_frame = 24
    
    def carrot(self):
    	hit_list = pygame.sprite.spritecollide(self, self.carrots, False)
    	for hit in hit_list:
		if type(hit) is Carrot.Carrot:
			if (hit.rect.left + 10 < self.rect.centerx < hit.rect.right - 10) and (hit.rect.bottom == self.rect.bottom):
				self.win = True
    				
    def box_ride(self):
    	self.rect.y += 1
    	hit_list = pygame.sprite.spritecollide(self, self.level, False)
    	self.rect.y -= 1
	for hit in hit_list:
           if type(hit) is moving_box.MovingBox:
               self.rect.x += hit.spd_x
           elif type(hit) is box.Box:
               self.rect.x += hit.spd_x
    
    def collision_y(self):
    	hit_list = pygame.sprite.spritecollide(self, self.level, False)
    	for block in hit_list:
    		if block.ID != self.ID:
			if self.spd_y > 0 or block.spd_y < 0:
				self.rect.bottom = block.rect.top
				self.air = False
				self.walk_ani_frame = 0
				self.image = self.stand_image
				if self.direction == 'Left':
					self.image = pygame.transform.flip(self.image, True, False)
			elif self.spd_y < 0 or block.spd_y > 0:
				self.rect.top = block.rect.bottom
			self.spd_y = 0
    			
    def collision_x(self):
    	hit_list = pygame.sprite.spritecollide(self, self.level, False)
    	for block in hit_list:
    		if block.ID != self.ID:
    			if self.spd_x > 0:
				self.rect.right = block.rect.left
			elif self.spd_x < 0:
				self.rect.left = block.rect.right
			
    def update(self):
        self.death()
        if self.dead:
    		return
        self.carrot()
        self.checkpoint()
        self.ani_update()
        self.jumpbox()
        self.box_ride()
	
        self.rect.x += self.spd_x
        self.collision_x()

        self.rect.y += self.spd_y         
        self.collision_y()
	
        if not self.touch_S(0):
		self.spd_y += .15
        if self.bounce:
		self.image = self.jump_ani[4]
		if self.spd_x > 0.3:
			self.spd_x -= .09
		elif self.spd_x < -0.3:
			self.spd_x += .09
		else:
			self.spd_x = 0
    			self.bounce = False
    			
    def ani_update(self):
    	if self.state == 'Walk' and not self.air:
		if self.walk_ani_frame % 5 == 0:
			self.image = self.walk_ani[self.walk_ani_frame / 5]
			if self.direction == 'Left':
				self.image = pygame.transform.flip(self.image, True, False)
				
			if self.walk_ani_frame == 20:
				self.walk_ani_frame = 1
		
		self.walk_ani_frame += 1
	
	elif self.air:
		if self.jump_ani_frame < 30:
			if self.jump_ani_frame % 6 == 0:
				self.image = self.jump_ani[self.jump_ani_frame / 6]
				if self.direction == 'Left':
					self.image = pygame.transform.flip(self.image, True, False)
    			self.jump_ani_frame += 1
    	
    def go_left(self):
    	self.state = 'Walk'
    	self.spd_x = -2
    	if self.direction == 'Right':
    		self.direction = 'Left'
  
    def go_right(self):
    	self.state = 'Walk'
    	self.spd_x = 2
    	if self.direction == 'Left':
		self.direction = 'Right'
      
    def stop(self):
    	self.spd_x = 0
    	self.state = 'Stand'
    	if not self.air:
		self.image = self.stand_image
	if self.direction == 'Left':
		self.image = pygame.transform.flip(self.image, True, False)
	self.walk_ani_frame = 0
    	
    def jump(self):
    	self.rect.y +=2
    	hit_list = pygame.sprite.spritecollide(self, self.level, False)
    	self.rect.y -=2
    	self.air = True
    	self.jump_ani_frame = 0
	for i in hit_list:
		if i.ID != self.ID:
			self.spd_y = -3
   
    def checkpoint(self):
	hit_list = pygame.sprite.spritecollide(self, self.checkpoints, False)
	for hit in hit_list:
		if type(hit) is Checkpoint.Checkpoint:
			if hit.rect.left + 1 < self.rect.centerx < hit.rect.right - 1 and not hit.on:
				self.init_x = hit.rect.x + 8
				self.init_y = hit.rect.y
				hit.on = True
        
