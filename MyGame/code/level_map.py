import pygame
from constants import BLOCK_SIZE
from tile_wall import Wall
from tile_box import Box, JumpBox, Box_Stopper
from tile_spike import Spike
from tile_carrot import Carrot
from tile_movingbox import MovingBox
from tile_checkpoint import Checkpoint

def get_level(name):
     map_layout, bg, wall_img = Read_File(name)
	
     sprite_list = pygame.sprite.Group()
     updatable_list = pygame.sprite.Group()
     wall_list = pygame.sprite.Group()
     box_list = pygame.sprite.Group()
     col_list = pygame.sprite.Group()
     carrot_list = pygame.sprite.Group()
     stopper_list = pygame.sprite.Group()
     moving_list = pygame.sprite.Group()
     checkpoint_list = pygame.sprite.Group()
	
     id_given = 0
     carrot_id = 0
     pos_y = 0
     spike_pos = []
 
     for line in map_layout:
         pos_x = 0
         for letter in line:
             spike_pos.append(letter)
             if (spike_pos[pos_x - 1] == 'T') and (pos_x - 1 > 0):
                   if spike_pos[pos_x - 2] == 'W' and spike_pos[pos_x] == 'W':
                           spike = Spike((pos_x - 1)*BLOCK_SIZE, pos_y*BLOCK_SIZE, 'up')
                   elif spike_pos[pos_x] == 'W':
                           spike = Spike((pos_x - 1)*BLOCK_SIZE, pos_y*BLOCK_SIZE, 'left')
                   elif spike_pos[pos_x - 2] == 'W':
                           spike = Spike((pos_x - 1)*BLOCK_SIZE, pos_y*BLOCK_SIZE, 'right')
                   else:
                       spike = Spike((pos_x -1)*BLOCK_SIZE, pos_y*BLOCK_SIZE, 'up')
                   sprite_list.add(spike)
                   col_list.add(spike)
                   spike.ID = id_given
                   id_given += 1
             elif (spike_pos[pos_x - 1] == 'U') and (pos_x - 1 > 0):
                   spike = Spike((pos_x - 1)*BLOCK_SIZE, pos_y*BLOCK_SIZE, 'down')
                   sprite_list.add(spike)
                   col_list.add(spike)
                   spike.ID = id_given
                   id_given += 1                 
             if letter == 'W':
                   wall = Wall(pos_x*BLOCK_SIZE, pos_y*BLOCK_SIZE, wall_img)
                   sprite_list.add(wall)
                   col_list.add(wall)
                   wall_list.add(wall)
                   wall.ID = id_given
                   id_given += 1 
             elif letter == 'P':
                   pos_initial = (pos_x*BLOCK_SIZE, pos_y*BLOCK_SIZE)
                   pos_ID = id_given
                   id_given += 1
             elif letter == 'B':
                   box = Box(pos_x*BLOCK_SIZE, pos_y*BLOCK_SIZE)
                   sprite_list.add(box)
                   col_list.add(box)
                   updatable_list.add(box)
                   box_list.add(box)
                   box.ID = id_given
                   id_given += 1
             elif letter == 'H' or letter == 'V':
                   moving_box = MovingBox(pos_x*BLOCK_SIZE, pos_y*BLOCK_SIZE, letter)
                   sprite_list.add(moving_box)
                   col_list.add(moving_box)
                   updatable_list.add(moving_box)
                   moving_list.add(moving_box)
                   moving_box.ID = id_given
                   id_given += 1
             elif letter == 'J':
                   box = JumpBox(pos_x*BLOCK_SIZE, pos_y*BLOCK_SIZE)
                   sprite_list.add(box)
                   col_list.add(box)
                   updatable_list.add(box)
                   box_list.add(box)
                   box.ID = id_given
                   id_given += 1
             elif letter == 'C':
			  carrot = Carrot(pos_x*BLOCK_SIZE, pos_y*BLOCK_SIZE)
			  carrot.exitID = carrot_id
			  carrot_list.add(carrot)
			  carrot_id += 1
             elif letter == 'F':
			  stopper = Box_Stopper(pos_x*BLOCK_SIZE, pos_y*BLOCK_SIZE)
			  stopper_list.add(stopper)
			  stopper.ID = id_given
			  id_given += 1
             elif letter == 'G':
                   wall = Wall(pos_x*BLOCK_SIZE, pos_y*BLOCK_SIZE, 'grass.png')
                   sprite_list.add(wall)
                   col_list.add(wall)
                   wall_list.add(wall)
                   wall.ID = id_given
                   id_given += 1 
             elif letter == 'S':
                   checkpoint = Checkpoint(pos_x*BLOCK_SIZE, pos_y*BLOCK_SIZE)
                   checkpoint_list.add(checkpoint)
                   checkpoint.ID = id_given
                   id_given += 1                   
             pos_x += 1
         pos_y += 1
         spike_pos = []
     levelList =[col_list, box_list, wall_list, carrot_list, updatable_list, sprite_list, stopper_list, moving_list, checkpoint_list]
     levelInfo = [pos_ID, pos_initial, bg, wall]
     return (levelInfo, levelList)

def Read_File(name):
    archive = open("maps/" + name)
    map_layout = []
    bg = 'sky1.png'
    wall = 'rock.png'
	
    for line in archive:
        if len(line) == 0 or line[0] == '#':
			continue
        line = line.strip("\n")
        if line[0] != ':':
			map_layout.append(line)
        else:
            line = line.split(' ')
            if line[0] == ':bg':
				bg = line[1]
            elif line[0] == ':wall':
                       wall = line[1]				
    archive.close()
    return map_layout, bg, wall