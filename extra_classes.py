import pygame
from pygame import mixer
import random
from fighters import Fighter

mixer.init()

class Background(): 
    def __init__(self, sprite_sheet, animation_steps, surface, width, height):
        self.width = width
        self.height = height
        self.animation_list = self.load_bg_images(sprite_sheet, animation_steps, surface)
        self.frame = 0
        self.frame_index = 0
        self.image = self.animation_list[self.frame][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.screen = surface
        

    def load_bg_images(self, sprite_sheet, animation_steps, surface):
        #extract images from sprite sheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.width, y * self.height, self.width, self.height)
                temp_img_list.append(temp_img)
            animation_list.append(temp_img_list)
                
        return animation_list
    


    #Updates the background image based off of spritsheet loaded in
    def update (self):
        animation_cooldown = 200
        self.image = self.animation_list[self.frame][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.frame]): 
             if self.frame_index >= len(self.animation_list[self.frame]) - 1:
                 self.frame_index = 0
                 self.frame += 1
             if self.frame >= len(self.animation_list):
                 self.frame = 0
    
    def draw_BG(self, sprite_sheet, surface):
        #fills the screen with black before reblitting it
        surface.fill((0, 0, 0))
        #scales the background image
        
        scaled_bg = pygame.transform.scale(self.image, (1000, 600))
        surface.blit(scaled_bg, (0, 0))
        #calls the update to animate as it is being drawn
        self.update()
                 
#creates button class
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.topleft = (self.x,self.y)
        self.clicked = False
        self.active = False
        
        
    
    def draw(self, surface, clicked):
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x,self.y)
        action = False
        self.clicked = clicked

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos) and self.clicked == True:
            #if pygame.mouse.get_pressed()[0] == 1 and 
            #if self.clicked == True:
            action = True
                #self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
                
        
        #draws the button on the screen
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action
 

   
    def flip_switch(self, switch):
        if switch == 1:
            self.active = False
            self.rect = None
        if switch == 2:
            self.active = True
 
 ###These are Classes for Special Moves### 
             
#Class for the spear, only for Helen the Huntress(Needs collison)
class Spear:
    def __init__(self, x, y, velocity, dark_side, flipped):
        self.x = x
        self.y = y
        self.velocity = velocity
        if dark_side:
            self.image = pygame.image.load("Assets/Fighters/Huntress/SpearInverted.png")
        else:
            self.image = pygame.image.load("Assets/Fighters/Huntress/Spear.png")
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.timer = 500
        self.attack_clock = pygame.time.get_ticks()
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.hit = 0
        self.flipped = flipped
     
    #updates the location of the spear after being thrown
    def update (self):
        if self.flipped == False:
            self.x += self.velocity[0]
            self.y += self.velocity[1]
             
        else:
            self.x -= self.velocity[0]
            self.y -= self.velocity[1]
            
    def update_rect (self, target):
        if target.hit == False:
            if self.flipped == False:
                self.rect.x += self.velocity[0]
                self.rect.y += self.velocity[1]
             
            else:
                self.rect.x -= self.velocity[0]
                self.rect.y -= self.velocity[1]
        

    def attack_rect(self, target):
        self.update_rect(target)
        if self.rect.colliderect(target.rect):
            if target.blocking == False:
                self.hit += 1
                if self.hit == 1:
                    target.health -= 30
                    target.hit = True
                else:
                    target.hit = False

    
    #draws the spear on the screen then calls the update to move it across the screen
    def draw (self, surface, target):
        img = pygame.transform.flip(self.image, self.flipped, False)
       # surface.blit(img,(self.x, self.y))
        if pygame.time.get_ticks() - self.attack_clock >= self.timer:
            surface.blit(img,(self.x, self.y))
            if (self.x >= -300) and (self.x < 1000):
                self.update()
                self.attack_rect(target)
                            
     
#Class for Willy the Wizard's lightning strike            
class Lightning:
    def __init__(self, target, dark_side):
        self.x = target.rect.x
        self.y = target.rect.y
        if dark_side:
            self.thunder_cloud = pygame.image.load("Assets/Fighters/Wizard/ThunderCloudInverted.png").convert_alpha() 
            self.thunder_strike = pygame.image.load("Assets/Fighters/Wizard/ThunderStrikeInverted.png").convert_alpha()
        else:
            self.thunder_cloud = pygame.image.load("Assets/Fighters/Wizard/ThunderCloud.png").convert_alpha() 
            self.thunder_strike = pygame.image.load("Assets/Fighters/Wizard/ThunderStrike.png").convert_alpha()
        self.update_timer = 500
        self.attack_clock = pygame.time.get_ticks()
        self.strike_timer = 1000
        self.lightning_clock = pygame.time.get_ticks()
        self.entire_timer = 1500
        self.entire_clock = pygame.time.get_ticks()
        self.draw_lightning = True
        self.width = self.thunder_strike.get_width()
        self.height = self.thunder_strike.get_height()
        self.rect = pygame.Rect(target.rect.x - 100, target.rect.y - 150,self.width,self.height)
        self.hit = 0
        
        

    def strike(self, target, surface):
        img = self.thunder_strike
        surface.blit(img,(target.rect.x - 100, target.rect.y - 150))
        
    
    def draw_cloud(self, target, surface):
        img = self.thunder_cloud
        surface.blit(img,(target.rect.x - 100, target.rect.y - 150))
        
    def update(self, target, surface):    
 
        if pygame.time.get_ticks() - self.attack_clock >= self.update_timer:
            self.draw_cloud(target, surface)
            if pygame.time.get_ticks() - self.lightning_clock >= self.strike_timer:
                self.strike(target, surface)
                self.check_collision(target)
                if pygame.time.get_ticks() - self.entire_clock >= self.entire_timer:
                    self.draw_lightning = False
    
    def check_collision(self, target):
        if self.rect.colliderect(target.rect) and target.blocking == False:
            self.hit += 1
            if self.hit == 1:
               target.health -= 30
               target.hit = True 
            else:
                target.hit = False
                    
#Wally the Warrior's special move (Needs collison)       
class Energy_Wave:
    def __init__(self, x, y, velocity, dark_side, flipped):
        self.x = x
        self.y = y
        self.velocity = velocity
        if dark_side:
            self.image = pygame.image.load("Assets/Fighters/Warrior/EnergyWaveInverted.png")
        else:   
            self.image = pygame.image.load("Assets/Fighters/Warrior/EnergyWave.png")
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.timer = 250
        self.attack_clock = pygame.time.get_ticks()
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.hit = 0
        self.flipped = flipped
        
     
    #updates the location of the eneragry wave after being blasted
    def update (self):
        if self.flipped == False:
            self.x += self.velocity[0]
            self.y += self.velocity[1]
        else:
            self.x -= self.velocity[0]
            self.y -= self.velocity[1]
            
    def update_rect (self, target):
        if target.hit == False:
            if self.flipped == False:
                self.rect.x += self.velocity[0]
                self.rect.y += self.velocity[1]
             
            else:
                self.rect.x -= self.velocity[0]
                self.rect.y -= self.velocity[1]
                
    def attack_rect(self, target):
        self.update_rect( target)
        if self.rect.colliderect(target.rect):
            if target.blocking == False:
                self.hit += 1
                if self.hit == 1:
                    target.health -= 30
                    target.hit = True
                else:
                    target.hit = False

    
    #draws the energy wave on the screen then calls the update to move it across the screen
    def draw (self, surface, target):
        img = pygame.transform.flip(self.image, self.flipped,False)
        if pygame.time.get_ticks() - self.attack_clock >= self.timer:
            surface.blit(img,(self.x, self.y))
            if (self.x >= -300) and (self.x < 1000):
                self.update()
                self.attack_rect(target)
                

    

