import pygame
import extra_classes 
import fighters
import random

class Bot(fighters.Fighter):
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound, joysticks, difficulty, character, dark_side):
        super().__init__( player, x, y, flip, data, sprite_sheet, animation_steps, sound, joysticks)
        self.player_in_melee_range = False
        self.attack_timer = difficulty[0]
        self.attack_timer_left = 0
        self.ai_block_timer = difficulty[1]
        self.ai_block_timer_left = 0
        self.special_meter_wait_time = difficulty[2]
        self.special_meter_wait_time_left = 0
        self.random_attack_timer = 1000
        self.bot_timer = pygame.time.get_ticks()
        self.ai_can_use_special = difficulty[3]
        self.ai_can_block = difficulty[4]
        self.character = character
        self.dark_side = dark_side
       # self.move_timer = difficulty[5]
        self.retreating = False
        
    def move(self, screen_width, screen_height, surface, target, round_over, character, controller):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0
        
        if self.attacking == False and self.alive == True and round_over == False:
            if target.attacking and self.ai_block_timer_left <= 0 and self.block_sphere_timer >= 0 and self.ai_can_block:
                self.blocking = True
            if self.special_meter <= 0 and self.special_meter_wait_time_left <= 0 and self.blocking == False and self.ai_can_use_special:  
                self.attack(target, 3, surface) 
                self.special_meter_wait_time_left = self.special_meter_wait_time  
            else:   
        #Chase player and then stop when in range
                if self.retreating:
                    dx = self.retreat(target,dx,SPEED)
                if abs(self.rect.centerx - target.rect.centerx) > 180 and self.blocking == False and self.retreating == False:
                    self.running = True 
                    self.player_in_melee_range = False
                    if target.rect.centerx > self.rect.centerx:
                        dx = SPEED
                    if target.rect.centerx < self.rect.centerx:
                        dx = -SPEED
                if abs(self.rect.centerx - target.rect.centerx) <= 180:
                    if self.attack_timer_left <= 0 and self.blocking == False:
                        self.attack(target, random.randint(1,2), surface)
                        self.attack_timer_left = self.attack_timer
                 
            
            #Special Attack Cooldown
            self.special_meter_wait_time_left -= 1
            #Attack Cooldown
            self.attack_timer_left -= 1 
            #Block cooldown
            if self.ai_block_timer_left > -100:
                self.ai_block_timer_left -= 1
            else:
                self.ai_block_timer_left = self.ai_block_timer

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
            
        if self.is_teleporting == True or self.being_hit_by_teleport == True:
            self.teleportation_flip()
        elif target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        #apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        #Account for shield regen timer
        if self.shield_regen_timer < 100 and self.block_sphere_timer <= 0:
            self.shield_regen_timer += 1
        elif self.shield_regen_timer >= 100:
            self.block_sphere_timer = 150
            self.shield_regen_timer = 0   
            
        
        #update player position
        self.rect.x += dx
        self.rect.y += dy

    def retreat(self, target, dx, speed):
        self.retreating = True
        if abs(self.rect.centerx - target.rect.centerx) > 180 and abs(self.rect.centerx- target.rect.centerx) <= 300 and self.blocking == False:
            if self.rect.x < target.rect.x:
                dx = -speed
            if self.rect.x > target.rect.x:
                dx = speed
        else:
            self.retreating = False
        return dx


    def attack(self, target, attack_type, surface):
        self.assign_special_countdown()

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

                if self.character == 0:
                    self.special_meter = 100
                    if attacking_rect.colliderect(target.rect):
                        target.health -= 30
                        target.hit = True
                    else:
                        self.energy_blast((20,0))
                        self.blast.update(self.flip)
                        self.blast.update_rect(self.flip,target)
                elif self.character == 1:
                    self.special_meter = 100
                    self.teleport(target)
                    if target.blocking == False:
                        target.health -= 30
                        target.hit = True
                elif self.character == 2:
                    self.throw_spear((50,0), target)
                    self.special_meter = 100
                    self.spear.update(self.flip)
                    self.spear.update_rect(self.flip, target)
                elif self.character == 3:
                    self.special_meter = 100
                    self.lighting_strike(target, surface)     

                
    def assign_special_countdown(self):
        self.special_meter_wait_time_left = random.randint(50,200)
        
     #The fighter class function for throwing Helen's spear
    def throw_spear(self, velocity, target):
        self.spear = extra_classes.Spear(self.rect.x, self.rect.y, velocity, self.dark_side)
     
    #This is Wally's Special move
    def energy_blast(self,velocity):
        if self.flip: 
            self.blast = extra_classes.Energy_Wave(self.rect.x - 100, self.rect.y, velocity, self.dark_side)
        else:
            self.blast = extra_classes.Energy_Wave(self.rect.x + 100, self.rect.y, velocity, self.dark_side)
        
    #This Willy the Wizards Special move
    def lighting_strike(self, target, surface):
            self.lightning_bolt = extra_classes.Lightning(target,self.dark_side)
  
'''          
    def movement_timer(self, difficulty):
        if self.move_timer > 0:
            self.move_timer -= 1
        else:
            self.move_timer = difficulty[5]
'''