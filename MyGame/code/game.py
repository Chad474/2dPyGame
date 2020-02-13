import pygame
import constants as F
import menu
from player import *
from level_map import get_level
from tile_box import static_boxes
		

def Play(curr_level):
    CHEAT_DEATH = False
    F.SCREEN.blit(pygame.image.load('images/background/main_screen.png'),(0,0))
    pygame.display.flip()
    print "current level: " + str(curr_level) 
    levelInfo, levelList = get_level('level_' + str(curr_level) + '.txt')
    
    pos_ID = levelInfo[0]
    pos_initial = levelInfo[1]
    bg = levelInfo[2]
    background = pygame.image.load('images/background/' + bg).convert()
    col_list = levelList[0]
    box_list = levelList[1]
    carrot_list = levelList[3]
    updateable_list = levelList[4]
    sprite_list = levelList[5]
    stopper_list = levelList[6]
    moving_list = levelList[7]
    checkpoint_list = levelList[8]
    
    PAUSE_SCREEN = pygame.image.load('images/background/main_screen.png').convert()
    win_screen = pygame.image.load('images/menu/win_screen.png').convert()
    win_screen.set_colorkey(F.COLOR_KEY)
    win_rect = win_screen.get_rect()
    win_pos = (F.SCREEN_WIDTH/2 - win_rect.w/2, F.SCREEN_HEIGHT/2 - win_rect.h/2)
    final_win_screen = pygame.image.load('images/menu/final_win_screen.png').convert()
    final_win_screen.set_colorkey(F.COLOR_KEY)
    final_win_rect = final_win_screen.get_rect()
    final_win_pos = (F.SCREEN_WIDTH/2 - final_win_rect.w/2, F.SCREEN_HEIGHT/2 - final_win_rect.h/2)
    
    pos_x, pos_y = pos_initial
    player = Player(pos_x, pos_y)
    player.ID = pos_ID
    player.level = col_list
    player.carrots = carrot_list
    player.moving = moving_list
    player.checkpoints = checkpoint_list

    for box in box_list.sprites():
		box.level = stopper_list
		for col in col_list.sprites():
			box.level.add(col)
		box.boxes = box_list
		box.player = player
  
    for moving_box in moving_list.sprites():
		moving_box.level = stopper_list
		for colx in col_list.sprites():
			moving_box.level.add(colx)

    updateable_list.add(player)
    gravity = 'S'
 
    EXIT_LEVEL = False
    clock = pygame.time.Clock()
    
    while not EXIT_LEVEL:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True, False, False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    curr_level += 1
                    return False, False, False, curr_level
                if event.key == pygame.K_c:
                    CHEAT_DEATH = True
                elif event.key == pygame.K_ESCAPE:
                    PAUSE = menu.pause_menu(PAUSE_SCREEN)
                    if PAUSE == 'Continue':
                        pass
                    elif PAUSE == False:
                        pass
                    elif PAUSE == 'Main':
                        return False, False, True, curr_level
                    
                elif event.key == pygame.K_q or event.key == pygame.K_a and not player.bounce:
                    player.go_left() 
                elif event.key == pygame.K_e or event.key == pygame.K_d and not player.bounce:
                    player.go_right()
                elif event.key == pygame.K_w or event.key == pygame.K_SPACE and player.touch_S(0):
                    player.jump()
                if event.key == pygame.K_LEFT:
                        if static_boxes(box_list):
                            gravity = 'LE'
                elif event.key == pygame.K_UP:
                        if static_boxes(box_list):
                            gravity = 'UP'
                elif event.key == pygame.K_RIGHT:
                        if static_boxes(box_list):
					gravity = 'RI'
                elif event.key == pygame.K_DOWN:
                        if static_boxes(box_list):
                            gravity = 'DN'
                            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_q or event.key == pygame.K_a and player.spd_x < 0:
                    player.stop()
                elif event.key == pygame.K_e or event.key == pygame.K_d and player.spd_x > 0:
                    player.stop()
        #rof
                        
        #for k in moving_list.sprites():
            #move = k.update_dir()
        moving_list.update()
        box_list.update(gravity)
        player.update()
        checkpoint_list.update()
        
        if player.dead:
            player.image = player.dead_image
            if player.direction == 'Left':
			player.image = pygame.transform.flip(player.image, True, False)
            F.SCREEN.blit(background, (0,0))
            carrot_list.draw(F.SCREEN)
            moving_list.draw(F.SCREEN)
            checkpoint_list.draw(F.SCREEN)
            F.SCREEN.blit(player.image, (player.rect.x - 8, player.rect.y -4))
            sprite_list.draw(F.SCREEN)
            stopper_list.draw(F.SCREEN)
            pygame.display.flip()
            PAUSE_SCREEN.blit(F.SCREEN, (0,0))
            
            if not CHEAT_DEATH:
                death_3= pygame.image.load('images/menu/countdown3.png').convert()
                death_3.set_colorkey(F.COLOR_KEY)
                death_rect = death_3.get_rect()
                death_pos = (F.SCREEN_WIDTH/2 - death_rect.w/2, F.SCREEN_HEIGHT/2 - death_rect.h/2)
                F.SCREEN.blit(death_3, death_pos)
                pygame.display.flip()
                pygame.time.wait(1000)
                death_2= pygame.image.load('images/menu/countdown2.png').convert()
                death_2.set_colorkey(F.COLOR_KEY)
                F.SCREEN.blit(death_2, death_pos)
                pygame.display.flip()
                pygame.time.wait(1000)
                death_1= pygame.image.load('images/menu/countdown1.png').convert()
                death_1.set_colorkey(F.COLOR_KEY)
                F.SCREEN.blit(death_1, death_pos)
                pygame.display.flip()
                pygame.time.wait(1000)
            
            F.SCREEN.blit(PAUSE_SCREEN, (0,0))
            pygame.display.flip()
            clock.tick(F.MAX_FPS)
            for obj in updateable_list.sprites():
    				gravity = 'S'
    				obj.reboot(gravity)
    			
        elif player.win:
            curr_level += 1
            if curr_level == 9:
                while True:
                       F.SCREEN.blit(final_win_screen, final_win_pos)
                       pygame.display.flip()
                       pygame.time.wait(500)
                       for event in pygame.event.get():
                            return False, False, True, curr_level
    						
            else:
                F.SCREEN.blit(win_screen, win_pos)
                pygame.display.flip()
                pygame.time.wait(500)
                return False, False, False, curr_level
  
        else: 
            F.SCREEN.blit(background, (0,0))
            carrot_list.draw(F.SCREEN)
            checkpoint_list.draw(F.SCREEN)
            F.SCREEN.blit(player.image, (player.rect.x - 8, player.rect.y -4))
            sprite_list.draw(F.SCREEN)
            stopper_list.draw(F.SCREEN)
			
            PAUSE_SCREEN.blit(F.SCREEN, (0,0))
            pygame.display.flip()
        
        clock.tick(F.MAX_FPS)