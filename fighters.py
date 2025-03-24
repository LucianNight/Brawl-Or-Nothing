from asyncio import shield
import pygame
import extra_classes 

#Creates fighter class
class Fighter():
    def __init__ (self, player, x, y, flip, data, sprite_sheet, animation_steps, sound, joysticks):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.update_time = pygame.time.get_ticks()
        #will determine animation #0:idle 1:Run 2:Jump 3:Attack1 4:Attack2 5:TakeHit 6:Death 7:Block
        self.action = 0
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect((x, y, 80, 180))
        self.spear_rect = None
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.blocking = False
        self.block_sphere_timer = 175
        self.shield_regen_timer = 0
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_sound = sound
        self.hit = False
        self.health = 100
        self.alive = True
        self.special_meter = 100
        self.can_use_special = False
        self.spear = None
        self.lightning_bolt = None
        self.blast = None
        self.is_teleporting = False
        self.being_hit_by_teleport = False
        self.teleport_attack_time = 1
        self.teleport_time = pygame.time.get_ticks()
        self.joystick = joysticks
        
    def load_images(self, sprite_sheet, animation_steps):
        #extract images from sprite sheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img,(self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list
        
    def move(self, screen_width, screen_height, surface, target, round_over, character, controller):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.blocking = False
        self.attack_type = 0
          
        #get keypresses
        key = pygame.key.get_pressed()
        
        #can only do if not attacking, if they are alive, and the round is not over
        if self.attacking == False and self.alive == True and round_over == False:
            #check player1 controls
            if self.player == 1:
                if controller[0] == "":
                   #movement
                    if key[pygame.K_a]:
                        dx = -SPEED
                        self.running = True
                    if key[pygame.K_d]:
                        dx = SPEED
                        self.running = True    
                    if key[pygame.K_s] and self.block_sphere_timer > 0:
                        self.blocking = True
                        dx = 0
                        dy = 0
                    else:
                        self.blocking = False
                        #jump
                        if key[pygame.K_w]  and self.jump == False:
                            self.vel_y = -30
                            self.jump = True
                        #deteremine which attack type was used
                        if key[pygame.K_r]:
                            self.attack(target, 1, character, surface)
                        elif key[pygame.K_t]:
                            self.attack(target, 2, character, surface)
                        elif key[pygame.K_f] and self.special_meter <= 0:
                            self.attack(target, 3, character, surface)
                
                #movement
                            
                elif controller[0] == "xbox" or controller[0] == "ps4":            
                    if key[pygame.K_a] or self.joystick.get_axis(0) < -0.2:
                        dx = -SPEED
                        self.running = True
                    if key[pygame.K_d] or self.joystick.get_axis(0) > 0.2:
                        dx = SPEED
                        self.running = True
                    #blocking
                    if controller[0] == "xbox":    
                        if (key[pygame.K_s] or self.joystick.get_button(4)) and self.block_sphere_timer > 0:
                            self.blocking = True
                            dx = 0
                            dy = 0
                        else:
                            self.blocking = False
                            #jump
                            if (key[pygame.K_w]  or self.joystick.get_button(0))  and self.jump == False:
                                self.vel_y = -30
                                self.jump = True
                            #deteremine which attack type was used
                            if key[pygame.K_r] or self.joystick.get_button(3):
                                self.attack(target, 1, character, surface)
                            elif key[pygame.K_t] or self.joystick.get_button(2):
                                self.attack(target, 2, character, surface)
                            elif (key[pygame.K_f] or self.joystick.get_button(1)) and self.special_meter <= 0:
                                self.attack(target, 3, character, surface)
                    else:
                        if key[pygame.K_s] or self.joystick.get_button(9):
                            self.blocking = True
                            dx = 0
                            dy = 0
                        else:
                            self.blocking = False
                            #jump
                            if (key[pygame.K_w]  or self.joystick.get_button(0))  and self.jump == False:
                                self.vel_y = -30
                                self.jump = True
                            #deteremine which attack type was used
                            if key[pygame.K_r] or self.joystick.get_button(3):
                                self.attack(target, 1, character, surface)
                            elif key[pygame.K_t] or self.joystick.get_button(2):
                                self.attack(target, 2, character, surface)
                            elif (key[pygame.K_f] or self.joystick.get_button(1)) and self.special_meter <= 0:
                                self.attack(target, 3, character, surface)
                        
            #check player2 cotnrols
            if self.player == 2:
                if controller[1] == "":
                   #movement
                    if key[pygame.K_LEFT]:
                        dx = -SPEED
                        self.running = True
                    if key[pygame.K_RIGHT]:
                        dx = SPEED
                        self.running = True    
                    if key[pygame.K_DOWN] and self.block_sphere_timer > 0:
                        self.blocking = True
                        dx = 0
                        dy = 0
                    else:
                        self.blocking = False
                        #jump
                        if key[pygame.K_UP]  and self.jump == False:
                            self.vel_y = -30
                            self.jump = True
                        #deteremine which attack type was used
                        if key[pygame.K_KP1]:
                            self.attack(target, 1, character, surface)
                        elif key[pygame.K_KP2]:
                            self.attack(target, 2, character, surface)
                        elif key[pygame.K_KP3] and self.special_meter <= 0:
                            self.attack(target, 3, character, surface)
                
                #movement
                elif controller[1] == "xbox" or controller[1] == "ps4":            
                    if key[pygame.K_LEFT] or self.joystick.get_axis(0) < -0.2:
                        dx = -SPEED
                        self.running = True
                    if key[pygame.K_RIGHT] or self.joystick.get_axis(0) > 0.2:
                        dx = SPEED
                        self.running = True
                    #blocking
                    if controller[1] == "xbox":    
                        if (key[pygame.K_DOWN] or self.joystick.get_button(4)) and self.block_sphere_timer > 0:
                            self.blocking = True
                            dx = 0
                            dy = 0
                        else:
                            self.blocking = False
                            #jump
                            if (key[pygame.K_UP]  or self.joystick.get_button(0))  and self.jump == False:
                                self.vel_y = -30
                                self.jump = True
                            #deteremine which attack type was used
                            if key[pygame.K_r] or self.joystick.get_button(3):
                                self.attack(target, 1, character, surface)
                            elif key[pygame.K_t] or self.joystick.get_button(2):
                                self.attack(target, 2, character, surface)
                            elif (key[pygame.K_f] or self.joystick.get_button(1)) and self.special_meter <= 0:
                                self.attack(target, 3, character, surface)
                    else:
                        if (key[pygame.K_DOWN] or self.joystick.get_button(9)) and self.block_sphere_timer > 0:
                            self.blocking = True
                            dx = 0
                            dy = 0
                        else:
                            self.blocking = False
                            #jump
                            if (key[pygame.K_w]  or self.joystick.get_button(0))  and self.jump == False:
                                self.vel_y = -30
                                self.jump = True
                            #deteremine which attack type was used
                            if key[pygame.K_KP1] or self.joystick.get_button(3):
                                self.attack(target, 1, character, surface)
                            elif key[pygame.K_KP2] or self.joystick.get_button(2):
                                self.attack(target, 2, character, surface)
                            elif (key[pygame.K_KP3] or self.joystick.get_button(1)) and self.special_meter <= 0:
                                self.attack(target, 3, character, surface)
                                

        #apply gravity
        self.vel_y += GRAVITY   
        dy += self.vel_y
        
        
        #ensure player stays in screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 40:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 40 - self.rect.bottom
        
        #ensure players face the correct direction based on player and input
        if self.player == 1:
            if controller[0] == "":
                if self.is_teleporting == True or self.being_hit_by_teleport == True:
                    self.teleportation_flip()
                elif key[pygame.K_a]:
                    self.flip = True
                elif key[pygame.K_d]:
                    self.flip = False              
                #This changes dircetion faced based on proximity to enemy    
                elif target.rect.centerx > self.rect.centerx:
                    self.flip = False            
                else:
                     self.flip = True
                     
            if controller[0] == "xbox" or controller[0] == "ps4":
                if self.is_teleporting == True or self.being_hit_by_teleport == True:
                    self.teleportation_flip()
                elif key[pygame.K_a]  or self.joystick.get_axis(0) < -0.2:
                    self.flip = True
                elif key[pygame.K_d]  or self.joystick.get_axis(0) > 0.2:
                    self.flip = False
                elif target.rect.centerx > self.rect.centerx:
                    self.flip = False            
                else:
                    self.flip = True

        if self.player == 2:
            if controller[1] == "":
                if self.is_teleporting == True or self.being_hit_by_teleport == True:
                    self.teleportation_flip()
                elif key[pygame.K_RIGHT]:
                   self.flip = False
                elif key[pygame.K_LEFT]:
                    self.flip = True
                elif target.rect.centerx > self.rect.centerx:
                   self.flip = False
                else:
                    self.flip = True
                
            if controller[1] == "xbox" or controller[0] == "ps4":
                if self.is_teleporting == True or self.being_hit_by_teleport == True:
                    self.teleportation_flip()
                elif key[pygame.K_a]  or self.joystick.get_axis(0) < -0.2:
                    self.flip = True
                elif key[pygame.K_d]  or self.joystick.get_axis(0) > 0.2:
                    self.flip = False
                elif target.rect.centerx > self.rect.centerx:
                    self.flip = False            
                else:
                    self.flip = True   
        
  
        #apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.shield_regen_timer < 100 and self.block_sphere_timer <= 0:
            self.shield_regen_timer += 1
        elif self.shield_regen_timer >= 100:
            self.block_sphere_timer = 150
            self.shield_regen_timer = 0
        
        
        #update player position
        self.rect.x += dx
        self.rect.y += dy
    

    #handle animations
    def update(self):
        #check what action player is performing
        if self.health <= 0:
            self.heath = 0
            self.alive = False
            self.update_action(6)#Death
        elif self.hit == True:
            self.update_action(5)#TakeHit
        elif self.blocking == True:
            self.update_action(7)#Block
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)#Attack1
            elif self.attack_type == 2:
                self.update_action(4)#Attack2
            elif self.attack_type == 3:
                self.update_action(8)
                
            
        elif self.jump == True:
            self.update_action(2)#Jump
        elif self.running == True:
           self.update_action(1)#Running
        else:
            self.update_action(0)#Idle
            
        animation_cooldown = 50
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #check if animation is done
        if self.frame_index >= len(self.animation_list[self.action]):
            #check if the player is dead the end animation
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0 
                #check if an attack was executed
                if self.action == 3:
                    self.attacking = False
                    self.attack_cooldown = 50
                elif self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 80
                elif self.action == 8:
                    self.attacking = False
                    self.attack_cooldown = 100
                #check if damage was taken
                if self.action == 5:
                    self.hit = False
                    #if player was in the middle of an attack then the attack is stopped
                    self.attacking = False
                    self.attack_cooldown = 50
            
    def attack(self, target, attack_type, character, surface):
        self.attack_type = attack_type
        self.can_use_special = False
        #self.character = character
        if self.special_meter <= 0:
            self.can_use_special = True
        if self.attack_cooldown == 0:
            #execute attack
            self.attacking = True
            self.attack_sound.play()
            attacking_rect = pygame.Rect(self.rect.centerx - (2.5 * self.rect.width * self.flip), self.rect.y, 2.5 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect) and target.blocking == False:
               if attack_type == 1:
                   target.health -= 5
                   target.hit = True
                   self.special_meter -= 10
                   target.special_meter -= 20
               elif attack_type == 2:
                   target.health -= 10
                   target.hit = True
                   self.special_meter -= 10
                   target.special_meter -= 20
            #This is not within the "collide and not blocking" because special's always hit. Unless it's Wally
            if attack_type == 3 and self.can_use_special == True: 
                #First determins which player
                if self.player == 1:
                    #Then which character and calls functions based off of that
                    if character[0] == 0:
                       self.special_meter = 100
                       if attacking_rect.colliderect(target.rect):
                           target.health -= 30
                           target.hit = True
                       else:
                            self.energy_blast((40,0)) 
                            self.blast.update()
                            self.blast.update_rect(target)                               
                    elif character[0] == 1:
                        self.special_meter = 100
                        self.teleport(target)
                        if target.blocking == False:
                            target.health -= 30
                            target.hit = True
                    elif character[0] == 2:
                        self.throw_spear((50,0))
                        self.special_meter = 100
                        self.spear.update()
                        self.spear.update_rect( target)
                    elif character[0] == 3:
                        self.special_meter = 100
                        self.lighting_strike(target, surface)
                        self.special_meter = 100
                if self.player == 2:
                    if character[1] == 0:
                        self.special_meter = 100
                        if attacking_rect.colliderect(target.rect):
                           target.health -= 30
                           target.hit = True
                        else:
                            self.energy_blast((40,0))
                            self.blast.update()
                            self.blast.update_rect(target)
                    elif character[1] == 1:
                        self.special_meter = 100
                        self.teleport(target)
                        if target.blocking == False:
                            target.health -= 30
                            target.hit = True
                    elif character[1] == 2:
                        self.throw_spear((50,0))
                        self.special_meter = 100
                        self.spear.update()
                        self.spear.update_rect(target)
                    elif character[1] == 3:
                        self.special_meter = 100
                        self.lighting_strike(target, surface)                     
    def update_action(self, new_action):
        #check if new action different to previous one
        if new_action != self.action:
            self.action = new_action
            #update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    
    #Helper function for drawing shield
    def draw_ellipse(self, xpos, ypos, xsize, ysize, surface):
        shield = pygame.draw.ellipse(surface, (0,0,255),((xpos,ypos - 25),(xsize,ysize)), 13)
    
    def blocking_sphere(self, surface):
        
        if self.block_sphere_timer > 0:
            self.block_sphere_timer -= 1
            if self.block_sphere_timer >= 125:
                sphereX = 150
                sphereY = 250
                offsetX = 0
                offsetY = 0
            elif self.block_sphere_timer < 125 and self.block_sphere_timer >= 75:
                sphereX = 125
                sphereY = 200
                offsetX = 15
                offsetY = 15
            elif self.block_sphere_timer < 75 and self.block_sphere_timer >= 25:
                sphereX = 75
                sphereY = 150 
                offsetX = 25
                offsetY = 30
            elif self.block_sphere_timer < 25 and self.block_sphere_timer > 0:
                sphereX = 50
                sphereY = 75 
                offsetX = 40
                offsetY = 60
            else:
                
                sphereX = 0
                sphereY = 0
                offsetX = 100
                offsetY = 100
                self.blocking = False
                self.shield_regen_timer = 0
       
        #uses whichever imagescale is used to decide the character and changes the size and pos of shield
        if self.blocking:
            if self.image_scale == 4:#WALLY
                if self.flip:
                    self.draw_ellipse((self.rect.x - 60 + offsetX), (self.rect.y + offsetY), sphereX, sphereY, surface)   
                else:
                    self.draw_ellipse((self.rect.x + offsetX), (self.rect.y + offsetY), sphereX, sphereY, surface)   
            elif self.image_scale == 3:#WILLY
                if self.flip:
                    self.draw_ellipse((self.rect.x - 60 + offsetX), (self.rect.y + offsetX), sphereX, sphereY, surface)
                else:
                    self.draw_ellipse((self.rect.x + offsetX), (self.rect.y + offsetY), sphereX, sphereY, surface)   
            elif self.image_scale == 3.5:#SAMMY
                if self.flip:
                    self.draw_ellipse((self.rect.x - 60 + offsetX), (self.rect.y + offsetY), sphereX, sphereY, surface)
                else:    
                    self.draw_ellipse((self.rect.x + offsetX), (self.rect.y + offsetY), sphereX, sphereY, surface)
            else:#HELEN
                if self.flip:
                    self.draw_ellipse((self.rect.x - 20 + offsetX), (self.rect.y + offsetY), sphereX, sphereY, surface)
                else:
                    self.draw_ellipse((self.rect.x - 50 + offsetX), (self.rect.y + offsetY), sphereX, sphereY, surface)  
    
    #This is the Samuari's Special move
    def teleport(self, target):
        self.is_teleporting = True
        target.being_hit_by_teleport = True
        
        if target.flip:
            if target.rect.centerx > 825:
                self.rect.x = target.rect.centerx 
            else:
                 self.rect.x = target.rect.centerx + 150
        if target.flip == False:
            if target.rect.centerx < 200: 
                self.rect.x = target.rect.centerx + 100
            else:
                self.rect.x = target.rect.centerx - 75

    def teleportation_flip(self):
        #Check to see which whether we are flipped or not
            if self.flip == False:
                    #The timer to keep them facing the "Wrong" dirction
                if self.teleport_attack_time >= 0:   
                    if (pygame.time.get_ticks() - self.teleport_time) >= 1000:
                        self.flip = False
                        self.teleport_attack_time -= 1
                        self.teleport_time = pygame.time.get_ticks()   
                else:
                        #Then flip them around 
                    self.being_hit_by_teleport= False
                    self.being_hit_by_teleport = False
                    self.flip = True
                    self.teleport_attack_time = 1
                #The exact same thing but opposite if flip is true    
            elif self.flip == True:
                if self.teleport_attack_time >= 0:       
                    if (pygame.time.get_ticks() - self.teleport_time) >= 1000:
                        self.flip = True
                        self.teleport_attack_time -= 1
                        self.teleport_time = pygame.time.get_ticks()
                else:
                     self.is_teleporting = False
                     self.being_hit_by_teleport = False            
                     self.flip = False
                     self.teleport_attack_time = 1
        
    #The fighter class function for throwing Helen's spear
    def throw_spear(self, velocity):
        self.spear = extra_classes.Spear(self.rect.x, self.rect.y, velocity, False, self.flip)
     
    #This is Wally's Special move
    def energy_blast(self, velocity):
        if self.flip: 
            self.blast = extra_classes.Energy_Wave(self.rect.x - 100, self.rect.y, velocity, False, True)
        else:
            self.blast = extra_classes.Energy_Wave(self.rect.x + 100, self.rect.y, velocity, False, False)
        
    #This Willy the Wizards Special move
    def lighting_strike(self, target, surface):
            self.lightning_bolt = extra_classes.Lightning(target, False)
        
    def draw(self, target, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y -(self.offset[1] * self.image_scale)))
        if self.spear is not None:
            self.spear.draw(surface, target)
        if self.blast is not None:
            self.blast.draw(surface, target)
        if self.lightning_bolt is not None and self.lightning_bolt.draw_lightning:
            self.lightning_bolt.update(target, surface)
        if self.blocking and self.block_sphere_timer > 0:
            self.blocking_sphere(surface)
        
        