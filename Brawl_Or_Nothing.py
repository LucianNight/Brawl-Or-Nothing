import random
import pygame
from bot import Bot
import extra_classes
from pygame import JOYDEVICEADDED, JOYDEVICEREMOVED, mixer
from fighters import Fighter 
 
mixer.init()
pygame.init()
pygame.joystick.init()

#Constants to create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

#using constants to create window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawl or Nothing")

#Sets the framerate
clock = pygame.time.Clock()
FPS = 60

#Constants to define colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREEN = (0, 100, 0)
BLACK = (0, 0, 0)
BLUE = (0,0,255)

#Define game variable
intro_count = 3
logo_count = 2
last_count_update = pygame.time.get_ticks()
score = [0, 0] #player scores [P1, P2]
round_over = False
WINNER_TIMER = 1500
ROUND_OVER_COOLDOWN = 3500
game_started = False
game_pause = False
menu_state = "main"
level = "menu"
menu_music = False
level0_music = False
level1_music = False
level2_music = False
level3_music = False
level4_music = False
player = 1
playerCount = 1
arcade_mode = False
tutorial_round_one = False
tutorial = False
enemies = []
current_enemy = 0
level_choice_list = []
choice = 0
level_choice= 0
choices = [] #character selector [P1,P2]
#Static variables for player 1
player1_pos_x = 200
player1_pos_y = 380
player1_flip = False
#Static variables for player 2
player2_pos_x = 700
player2_pos_y = 380
player2_flip = True
clicked = False
player1_name = ""
player2_name = ""
controller_name = ""
controller_names = ["",""]
joysticks = [0,1]
#controller = None
#controllers = []
gamepad1 = False
gamepad2 = False
a_button_pressed = False
w_button_pressed = False
s_button_pressed = False
d_button_pressed = False
r_button_pressed = False
t_button_pressed = False
f_button_pressed = False
space_bar_pressed = False
tutorial_finished = False

inverted = False


#Define fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [70, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [110, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]
HUNTRESS_SIZE = 150
HUNTRESS_SCALE = 4.5
HUNTRESS_OFFSET = [65, 56]
HUNTRESS_DATA = [HUNTRESS_SIZE, HUNTRESS_SCALE, HUNTRESS_OFFSET]
SAMURAI_SIZE = 200
SAMURAI_SCALE = 3.5
SAMURAI_OFFSET = [90, 75]
SAMURAI_DATA = [SAMURAI_SIZE, SAMURAI_SCALE, SAMURAI_OFFSET]
#save all of them into a list to pull for character select
fighter_DATA = [WARRIOR_DATA, SAMURAI_DATA, HUNTRESS_DATA, WIZARD_DATA]
character_names = ["WALLY", "SAMMY", "HELEN", "WILLY"]


#Load sounds
sword_fx = pygame.mixer.Sound("Assets/Audio/sword.wav")
sword_fx.set_volume(0.4)
magic_fx = pygame.mixer.Sound("Assets/Audio/magic.wav")
magic_fx.set_volume(0.4)


#Load in the Background Images
bg_image_ship = pygame.image.load("Assets/Images/Background/OhShip.jpg").convert_alpha()
bg_image_darkbeach = pygame.image.load("Assets/Images/Background/DarkBeachBackground.jpg").convert_alpha()
bg_image_smalltown = pygame.image.load("Assets/Images/Background/SmallTown.png").convert_alpha()
bg_image_burn_house = pygame.image.load("Assets/Images/Background/BurningHouse.jpg").convert_alpha()
bg_image_fuedal = pygame.image.load("Assets/Images/Background/FamilyFuedal.png").convert_alpha()
bg_image_noasias = pygame.image.load("Assets/Images/Background/Noasias.png").convert_alpha()

level_sprites = [bg_image_burn_house, bg_image_darkbeach, bg_image_fuedal, bg_image_noasias]


#Define animation list for background
TOWN_BG_ANI_STEPS = [1, 1, 1, 1, 1, 1, 1, 1]
SHIP_BG_ANI_STEPS = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
BURN_BG_ANI_STEPS = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
FUEDAL_BG_ANI_STEPS = [5, 5, 5, 5]
NOASIAS_BG_ANI_STEPS = [3, 3, 3, 3]

#Create instances of backgrounds
ship_gif = extra_classes.Background(bg_image_ship, SHIP_BG_ANI_STEPS, screen, 768, 259)
small_house_gif = extra_classes.Background(bg_image_smalltown, TOWN_BG_ANI_STEPS, screen, 750, 224)
burning_House_gif = extra_classes.Background(bg_image_burn_house, TOWN_BG_ANI_STEPS, screen, 800, 336)
dark_beach_gif = extra_classes.Background(bg_image_darkbeach, BURN_BG_ANI_STEPS, screen, 640, 480)
fuedal_gif = extra_classes.Background(bg_image_fuedal, FUEDAL_BG_ANI_STEPS, screen, 640, 480)
noasias_gif = extra_classes.Background(bg_image_noasias, NOASIAS_BG_ANI_STEPS, screen, 640, 368)

background_choice = [burning_House_gif, dark_beach_gif, fuedal_gif, noasias_gif]


#Load in the spritesheets
warrior_sheet = pygame.image.load("Assets/Fighters/Warrior/warriorNewest.png").convert_alpha()
wizard_sheet = pygame.image.load("Assets/Fighters/Wizard/wizardNewest.png").convert_alpha()
huntress_sheet = pygame.image.load("Assets/Fighters/Huntress/HuntressFullSheetNewest.png").convert_alpha()
samurai_sheet = pygame.image.load("Assets/Fighters/Samurai/SamuraiFullSheetNewest.png").convert_alpha()
fighter_sheets = [warrior_sheet, samurai_sheet, huntress_sheet, wizard_sheet]

#Load in inverted spritesheets
dark_warrior_sheet = pygame.image.load("Assets/Fighters/Warrior/warriorInverted.png").convert_alpha()
dark_wizard_sheet = pygame.image.load("Assets/Fighters/Wizard/wizardInverted.png").convert_alpha()
dark_huntress_sheet = pygame.image.load("Assets/Fighters/Huntress/HuntressInverted.png").convert_alpha()
dark_samurai_sheet = pygame.image.load("Assets/Fighters/Samurai/SamuraiInverted.png").convert_alpha()
dark_fighter_sheets = [dark_warrior_sheet, dark_samurai_sheet, dark_huntress_sheet, dark_wizard_sheet]

#Load in the victory image
victory_img = pygame.image.load("Assets/Images/Victory/victory.png").convert_alpha()

#Load in button images
play_img = pygame.image.load("Assets/Images/Buttons/Play.png").convert_alpha()
exit_img = pygame.image.load("Assets/Images/Buttons/Exit.png").convert_alpha()
credits_img = pygame.image.load("Assets/Images/Buttons/Credits.png").convert_alpha()
soundtrack_img = pygame.image.load("Assets/Images/Buttons/Soundtrack.png").convert_alpha()
solo_img = pygame.image.load("Assets/Images/Buttons/SinglePlayer.png").convert_alpha()
two_player_img = pygame.image.load("Assets/Images/Buttons/TwoPlayer.png").convert_alpha()
tutorial_img = pygame.image.load("Assets/Images/Buttons/Tutorial.png").convert_alpha()
arcade_img = pygame.image.load("Assets/Images/Buttons/Arcade.png").convert_alpha()
single_fight_img = pygame.image.load("Assets/Images/Buttons/SingleFight.png").convert_alpha()
easy_img = pygame.image.load("Assets/Images/Buttons/Easy.png").convert_alpha()
medium_img = pygame.image.load("Assets/Images/Buttons/Medium.png").convert_alpha()
hard_img = pygame.image.load("Assets/Images/Buttons/Hard.png").convert_alpha()
resume_img = pygame.image.load("Assets/Images/Buttons/Resume.png").convert_alpha()
move_list_img = pygame.image.load("Assets/Images/Buttons/MoveList.png").convert_alpha()
main_menu_img = pygame.image.load("Assets/Images/Buttons/MainMenu.png").convert_alpha()
back_img = pygame.image.load("Assets/Images/Buttons/Back.png").convert_alpha()
fighter_choice1_img = pygame.image.load("Assets/Images/Buttons/WarriorButton.png").convert_alpha()
fighter_choice2_img = pygame.image.load("Assets/Images/Buttons/SamuaraiButton.png").convert_alpha()
fighter_choice3_img = pygame.image.load("Assets/Images/Buttons/HuntressButton.png").convert_alpha()
fighter_choice4_img = pygame.image.load("Assets/Images/Buttons/WizardButton.png").convert_alpha()
random_choice_image = pygame.image.load("Assets/Images/Buttons/Random.png").convert_alpha()
level1_img = pygame.image.load("Assets/Images/Buttons/BurningHouseLevel.png").convert_alpha()
level2_img = pygame.image.load("Assets/Images/Buttons/DarkBeachBackground.png").convert_alpha()
level3_img = pygame.image.load("Assets/Images/Buttons/FuedalButton.png").convert_alpha()
level4_img = pygame.image.load("Assets/Images/Buttons/NoasiasButton.png").convert_alpha()
rematch_img = pygame.image.load("Assets/Images/Buttons/Rematch.png").convert_alpha()
next_fight_img = pygame.image.load("Assets/Images/Buttons/NextFight.png").convert_alpha()
player_select_img = pygame.image.load("Assets/Images/Buttons/Character_Select.png").convert_alpha()

#creates instances of the buttons from the class
play_button = extra_classes.Button(250, 275, play_img, 0.4)
exit_button = extra_classes.Button(585, 275, exit_img, 0.4)
credits_button = extra_classes.Button(380, 400, credits_img, 0.4)
soundtrack_button = extra_classes.Button(675, 30, soundtrack_img, 0.2)
solo_button = extra_classes.Button(200,320, solo_img, 0.4)
two_player_button = extra_classes.Button(570, 320, two_player_img, 0.4)
tutorial_button = extra_classes.Button(380, 450, tutorial_img, 0.4)
arcade_button = extra_classes.Button(375, 200, arcade_img, 0.4)
single_fight_button = extra_classes.Button(375, 350, single_fight_img, 0.4)
easy_button = extra_classes.Button(420, 100,easy_img, 0.4)
medium_button = extra_classes.Button(420, 250,medium_img, 0.4)
hard_button = extra_classes.Button(420, 400,hard_img, 0.4)
resume_button = extra_classes.Button(440, 200, resume_img, 0.3)
back_button = extra_classes.Button(100, 125, back_img, 0.3)
credit_back_button = extra_classes.Button(170, 30, back_img, 0.3)
soundtrack_back_button = extra_classes.Button(235, 75, back_img, 0.3)
main_menu_button = extra_classes.Button(385, 400, main_menu_img, 0.3)
move_list_button = extra_classes.Button(385, 300, move_list_img, 0.3)
fighter1_button = extra_classes.Button(0, 230, fighter_choice1_img, 2.4)
fighter2_button = extra_classes.Button(250, 230, fighter_choice2_img, 2)
fighter3_button = extra_classes.Button(500, 230, fighter_choice3_img, 2.6)
fighter4_button = extra_classes.Button(800, 120, fighter_choice4_img, 1.75)
random_fighter_button = extra_classes.Button((SCREEN_WIDTH/2 - 100), 525, random_choice_image, 0.3)
random_level_button = extra_classes.Button((SCREEN_WIDTH/2 - 70), (SCREEN_HEIGHT/2 + 75), random_choice_image, 0.3)
level1 = extra_classes.Button(75, 200, level1_img, 0.4)
level2 = extra_classes.Button(75, 450, level2_img, 0.4)
level3 = extra_classes.Button(600, 200, level3_img, 0.4)
level4 = extra_classes.Button(600, 450, level4_img, 0.4)
rematch_button = extra_classes.Button(460, 260, rematch_img, 0.3)
next_fight_button = extra_classes.Button(400, 260, next_fight_img, 0.3)
player_select_button = extra_classes.Button(380, 350, player_select_img, 0.3)
main_menu_button2 = extra_classes.Button(400, 420, main_menu_img, 0.3)


#Define number of steps in each of the animations for characters
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7, 1, 8]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7, 1, 7]
HUNTRESS_ANIMATION_STEPS = [8, 8, 2, 5, 5, 3, 8, 1, 7]
SAMURAI_ANIMATION_STEPS = [4, 8, 2, 4, 4, 3, 7, 1, 5]
fighter_ANI_step = [WARRIOR_ANIMATION_STEPS, SAMURAI_ANIMATION_STEPS, HUNTRESS_ANIMATION_STEPS, WIZARD_ANIMATION_STEPS]

#Define the font
count_font = pygame.font.Font("Assets/Fonts/Turok.ttf", 80)
score_font = pygame.font.Font("Assets/Fonts/Turok.ttf", 30)
special_font = pygame.font.Font("Assets/Fonts/Turok.ttf", 20)

#Difficulties
easy = [300,350,500,False,False]
medium = [250,300,400,False,True]
hard = [200,200,250,True,True]
very_hard = [100, 100, 150, True, True]
difficulty = [easy,medium,hard,very_hard]
difficulty_choice = 0



#Function for drawing text in pygame window
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_player_select_text(player):
    
    if menu_state == "player1_selector":
        player_string = "Player 1 "
    if menu_state == "player2_selector" and playerCount == 2:
        player_string = "Player 2 "
    if menu_state == "player2_selector" and playerCount == 1:
        player_string = "   Bot "
    draw_text((player_string + "CHOOSE FIGHTER"), count_font, BLACK, 75, 50)
    draw_text(character_names[0], score_font, RED, 40, 200)
    draw_text(character_names[1], score_font, RED, 300, 200)
    draw_text(character_names[2], score_font, RED, 550, 200)
    draw_text(character_names[3], score_font, RED, 820, 200)
        
def draw_box(xsize, ysize, alpha, color, xpos, ypos):
    rect = pygame.Surface((xsize, ysize), pygame.SRCALPHA)
    rect.set_alpha(alpha)
    rect.fill(color)
    screen.blit(rect, (xpos, ypos))
    
def draw_moves_list(choice):
    if playerCount == 2:
        draw_box(650, 350, 175, WHITE, 150, 150)
        draw_text("    Player 1                    Player 2", score_font, BLACK, 250, 150)
        draw_text("Left:        A                      Left", score_font, RED, 200, 180)
        draw_text("Right:       D                      Right", score_font, RED, 200, 210)
        draw_text("Jump:        W                        Up", score_font, RED, 200, 240)
        draw_text("Block:       S                      Down", score_font, RED, 200, 270)
        draw_text("Atk 1:        R                          1", score_font, RED, 200, 300)
        draw_text("Atk 2:       T                          2", score_font, RED, 200, 330)
        draw_text("Special:     F                         3", score_font, RED, 200, 360)
        if choices[0] == 0:
            draw_text("(CLOSE) MEGACHOP", special_font, RED, 275, 385)
            draw_text("(RANGED) CATCH THE WAVE", special_font, RED, 250, 405)
        if choices[0] == 1:
            draw_text("(RANGED) ANKLE-BREAKER", special_font, RED, 275, 385)
        if choices[0] == 2:
            draw_text("(RANGED) HOLD THIS", special_font, RED, 275, 385)
        if choices[0] == 3:
            draw_text("(TRACKING) HERE COMES THE...", special_font, RED, 245, 385)
        if choices[1] == 0:
            draw_text("(CLOSE) MEGACHOP", special_font, RED, 500, 390)
            draw_text("(RANGED) CATCH THE WAVE", special_font, RED, 475, 410)
        if choices[1] == 1:
            draw_text("(RANGED) ANKLE-BREAKER", special_font, RED, 500, 390)
        if choices[1] == 2:
            draw_text("(RANGED) HOLD THIS", special_font, RED, 500, 390)
        if choices[1] == 3:
            draw_text("(TRACKING) HERE COMES THE...", special_font, RED, 500, 400)
    else:
        draw_box(650, 350, 175, WHITE, 150, 150)
        draw_text("Player   1", score_font, BLACK, 375, 150)
        draw_text("Left:    A", score_font, RED, 375, 180)
        draw_text("Right:   D", score_font, RED, 375, 210)
        draw_text("Jump:    W", score_font, RED, 375, 240)
        draw_text("Block:   S", score_font, RED, 375, 270)
        draw_text("Atk 1:    R", score_font, RED, 375, 300)
        draw_text("Atk 2:   T", score_font, RED, 375, 330)
        draw_text("Special: F", score_font, RED, 375, 360)
        if choices[0] == 0:
            draw_text("(CLOSE) MEGACHOP", special_font, RED, 375, 390)
            draw_text("(RANGED) CATCH THE WAVE", special_font, RED, 375, 415)
        if choices[0] == 1:
            draw_text("(RANGED) ANKLE-BREAKER", special_font, RED, 375, 390)
        if choices[0] == 2:
            draw_text("(RANGED) HOLD THIS", special_font, RED, 375, 390)
        if choices[0] == 3:
            draw_text("(TRACKING) HERE COMES THE...", special_font, RED, 375, 390)
        
def text_for_tutorial():
    
    draw_box(250, 160, 175, WHITE, 20, 105)
    
    draw_text("Left:     A", special_font, BLACK, 25, 100)
    draw_text("Right:    D", special_font, BLACK, 25, 120)
    draw_text("Jump:    W", special_font, BLACK, 25, 140)
    draw_text("Block:   S", special_font,BLACK, 25, 160)
    draw_text("Atk 1:     R", special_font, BLACK, 25, 180)
    draw_text("Atk 2:    T", special_font, BLACK, 25, 200)
    draw_text("Special: F (When bar filled)", special_font, BLACK, 25, 220)
    draw_text("SpaceBar: Pause", special_font, BLACK, 25, 240)
          
def draw_credits():
    draw_box(500, 515, 175, WHITE, 230, 50)
    draw_text("Final Design and Development:", special_font, BLACK, 350, 70)
    draw_text("Cornelius Holt", special_font, RED, 415, 100)
    draw_text("Artists:", special_font, BLACK, 450, 140)
    draw_text("Characters: LuizMelo", special_font, RED, 400, 170)
    draw_text("Backgrounds: RudeBootie", special_font,RED, 385, 200)
    draw_text("Cloud: a__ban__", special_font, RED, 425, 230)
    draw_text("Lightning bolt: Sanctumpixel", special_font, RED, 370, 260)
    draw_text("Energy Ball: yiannisd", special_font, RED, 405, 290)
    draw_text("Audio:", special_font, BLACK, 450, 330)
    draw_text("Sword Effect: Mateusz_Chenc", special_font, RED, 350, 360)
    draw_text("Magic Effect: qubodup", special_font,RED, 385, 390)
    draw_text("Music:", special_font, BLACK, 450, 430)
    draw_text("Sara Garrard", special_font, RED, 425, 460)
    draw_text("Honorable Mention for inital tutorial: ", special_font, BLACK, 320, 500)
    draw_text("CodingWithRuss", special_font, RED, 410, 530)
    
def draw_soundtrack():
    draw_box(350, 350, 175, WHITE, 300, 100)
    draw_text("MENU:", special_font, RED, 310, 150)
    draw_text("TUTORIAL:", special_font, RED, 310, 190)
    draw_text("LEVEL 1:", special_font, RED, 310, 230)
    draw_text("LEVEL 2:", special_font, RED, 310, 270)
    draw_text("LEVEL 3:", special_font, RED, 310, 310)
    draw_text("LEVEL 4:", special_font,RED, 310, 350)
    draw_text("Title: Origin Boss Battle", special_font, BLACK, 400, 150)
    draw_text("Title: Fated Battle", special_font, BLACK, 400, 190)
    draw_text("Title: Fight Stage 5", special_font, BLACK, 400, 230)
    draw_text("Title: Passion and Precision", special_font, BLACK, 400, 270)
    draw_text("Title: Dies Irae", special_font, BLACK, 400, 310)
    draw_text("Title: To Adventure", special_font,BLACK, 400, 350)
    
#Function for drawing health bars
def draw_health_bars(health, x, y):
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    ratio = health / 100
    pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30)) 
    
def draw_special_meter(special, x, y):
    pygame.draw.rect(screen, BLACK, (x - 2, y - 2, 204, 24))
    pygame.draw.rect(screen, YELLOW, (x, y, 200, 20))
    ratio = special / 100
    pygame.draw.rect(screen, WHITE, (x, y, 200 * ratio, 20)) 
    
def draw_block_bars(block,x,y):
    pygame.draw.rect(screen, BLACK, (x - 2, y - 2, 154, 19))
    pygame.draw.rect(screen, WHITE, (x, y, 150, 15))
    ratio = block / 100
    pygame.draw.rect(screen, BLUE, (x, y, 150 * ratio, 15))
    if block == 0:
        pygame.draw.rect(screen, BLUE, (x, y, 150, 15))
    
def display_all_stats():
    draw_health_bars(player1.health, 20, 20)
    draw_health_bars(player2.health, 580, 20)
    draw_special_meter(player1.special_meter, 20, 60)
    draw_special_meter(player2.special_meter, 780, 60)
    draw_block_bars(player1.shield_regen_timer,20,85)
    draw_block_bars(player2.shield_regen_timer,830,85)
    draw_box(175, 34, 150, WHITE, 250, 60)
    draw_text("P1: " + str(score[0]), score_font, RED, 374, 56)
    draw_text(player1_name, score_font, BLACK, 255, 56)
    draw_box(175, 34, 150, WHITE, 580, 60)
    draw_text("P2: " + str(score[1]), score_font, RED, 580, 56)
    draw_text(player2_name, score_font, BLACK, 665, 56)

def randomize_list():
    # Specify the range and number of elements
    start = 0
    end = 3
    count = 4
    rand_list = []

    # Generate the list
    rand_list = random.sample(range(start, end + 1), count)
    
    return rand_list

def set_last_enemy(enemy_list, player_choice):
    if player_choice in enemy_list:
        last_enemy = enemy_list.pop(enemy_list.index(player_choice))
        enemy_list.append(last_enemy)
    else:
        enemy_list.append(player_choice)
    return enemy_list

def play_background_music(menu_music,level0_music, level1_music, level2_music, level3_music, level4_music):
    if level == "menu":
        if level0_music or level1_music or level2_music or level3_music or level4_music:
            pygame.mixer.music.unload()
            level0_music = False 
            level1_music = False
            level2_music = False
            level3_music = False
            level4_music = False      
        if not pygame.mixer.music.get_busy():           
            pygame.mixer.music.load("Assets/Audio/Music/Origin Boss Battle.wav")
            pygame.mixer.music.play(-1,0.0,5)
            pygame.mixer.music.set_volume(0.3)
            menu_music = True
    if level == "tutorial":
        if menu_music:
            pygame.mixer.music.unload()
            menu_music = False
        if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load("Assets/Audio/Music/Fated Battle loop.wav")
                pygame.mixer.music.play(-1,0.0,5)
                pygame.mixer.music.set_volume(0.3)
                level0_music = True 
    if level == "one":
        if menu_music or level2_music or level3_music or level4_music:
            pygame.mixer.music.unload()
            menu_music = False
            level2_music = False
            level3_music = False
            level4_music = False 
        if not pygame.mixer.music.get_busy():     
                pygame.mixer.music.load("Assets/Audio/Music/Fight Stage 5.wav")
                pygame.mixer.music.play(-1,0.0,5)
                pygame.mixer.music.set_volume(0.3)
                level1_music = True   
    
    if level == "two":
        if menu_music or level1_music or level3_music or level4_music:
            pygame.mixer.music.unload()
            menu_music = False
            level1_music = False
            level3_music = False
            level4_music = False 
        if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load("Assets/Audio/Music/Passion and Precision.wav")
                pygame.mixer.music.play(-1,0.0,5)
                pygame.mixer.music.set_volume(0.3)
                level2_music = True            
    if level == "three":
        if menu_music or level1_music or level2_music or level4_music:
            pygame.mixer.music.unload()
            menu_music = False
            level1_music = False
            level2_music = False
            level4_music = False 
        if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load("Assets/Audio/Music/Dies Irae.wav")
                pygame.mixer.music.play(-1,0.0,5)
                pygame.mixer.music.set_volume(0.3)
                level3_music = True              
    if level == "four":
        if menu_music or level1_music or level2_music or level3_music:
            pygame.mixer.music.unload()
            menu_music = False
            level1_music = False
            level2_music = False
            level3_music = False 
        if not pygame.mixer.music.get_busy():    
                pygame.mixer.music.load("Assets/Audio/Music/To Adventure.wav")
                pygame.mixer.music.play(-1,0.0,5)
                pygame.mixer.music.set_volume(0.3)
                level4_music = True        

    return menu_music,level0_music, level1_music, level2_music, level3_music, level4_music       

#Flag for main Game Loop
runGame = True
#play_background_music()
#Game Loop
while runGame:
    
    menu_music,level0_music, level1_music, level2_music, level3_music, level4_music = play_background_music(menu_music,level0_music, level1_music, level2_music, level3_music, level4_music)
    clock.tick(FPS)
    
    #draw the background
    
    if game_started == False:
        ship_gif.draw_BG(bg_image_ship, screen)
        level = "menu"
        #Make sure timer doesn't start until round does
        last_count_update = pygame.time.get_ticks()  
        draw_text("BRAWL OR NOTHING", count_font, RED, (210), 100)
        #draw "main menu"
        if menu_state == "main":
            if play_button.draw(screen, clicked):
                clicked = False
                menu_state = "player_count"
            if exit_button.draw(screen, clicked): 
                runGame = False
            if credits_button.draw(screen, clicked):
                clicked = False
                menu_state = "credits"
        if menu_state == "credits":
            small_house_gif.draw_BG(bg_image_smalltown, screen)
            draw_credits()
            if credit_back_button.draw(screen, clicked):
                clicked = False
                menu_state = "main"
            if soundtrack_button.draw(screen,clicked):
                clicked = False
                menu_state = "soundtrack_list"
        if menu_state == "soundtrack_list":
            small_house_gif.draw_BG(bg_image_smalltown, screen)
            draw_soundtrack()
            if soundtrack_back_button.draw(screen,clicked):
                clicked = False
                menu_state = "credits"
        if menu_state == "player_count":
            ship_gif.draw_BG(bg_image_ship, screen)
            draw_text("PLAYER COUNT", count_font, RED, (260), 100)
            if solo_button.draw(screen, clicked):
                clicked = False
                playerCount = 1
                menu_state = "game_mode"
            if two_player_button.draw(screen, clicked):
                clicked = False
                playerCount = 2
                menu_state = "player1_selector"
            if tutorial_button.draw(screen, clicked):
                clicked = False
                tutorial = True
                tutorial_round_one = True
                game_started = True
                choice = 0
                choices.append(choice)
                p1fx = sword_fx
                p2fx = sword_fx

                player1 = Fighter(1, player1_pos_x, player1_pos_y, player1_flip, 
                            fighter_DATA[choice], fighter_sheets[choice], fighter_ANI_step[choice], p1fx, joysticks[0])
                choice = 0
                choices.append(choice)
                player2 = Bot(3, player2_pos_x, player2_pos_y, player2_flip,  
                            fighter_DATA[current_enemy], fighter_sheets[current_enemy], fighter_ANI_step[current_enemy],
                            p2fx, joysticks[1], 
                            difficulty[difficulty_choice], current_enemy, inverted)
        if menu_state == "game_mode":
            ship_gif.draw_BG(bg_image_ship, screen)
            draw_text("BRAWL OR NOTHING", count_font, RED, (210), 100)
            if single_fight_button.draw(screen, clicked):
                clicked = False
                menu_state = "difficulty_selector"
            if arcade_button.draw(screen, clicked):
                clicked = False
                arcade_mode = True
                enemies = randomize_list()
                level_choice_list = randomize_list()
                menu_state = "player1_selector"   
        if menu_state == "difficulty_selector":
            ship_gif.draw_BG(bg_image_ship, screen)
            if easy_button.draw(screen, clicked):
                clicked = False
                difficulty_choice = 0
                menu_state = "player1_selector"
            if medium_button.draw(screen, clicked):
                clicked = False
                difficulty_choice = 1
                menu_state = "player1_selector"   
            if hard_button.draw(screen, clicked):
                clicked = False
                difficulty_choice = 2
                menu_state = "player1_selector"
        if menu_state == "player1_selector":
            #draws the background and names of characters for character selector
            small_house_gif.draw_BG(bg_image_smalltown, screen)
            draw_player_select_text(player)
            if random_fighter_button.draw(screen, clicked):
                clicked = False
                choice = random.randint(0,3)
                choices.append(choice)
                player1_name = character_names[choice]
                character_names
                if choice != 3:
                    p1fx = sword_fx
                else:
                    p1fx = magic_fx
                player1 = Fighter(1, player1_pos_x, player1_pos_y, player1_flip, 
                          fighter_DATA[choice], fighter_sheets[choice], fighter_ANI_step[choice], p1fx, joysticks[0])
                if arcade_mode: 
                    enemies = set_last_enemy(enemies,choice)
                    current_enemy = enemies.pop(0)
                    level_choice = level_choice_list.pop(0)
                    if current_enemy != 3:
                        p2fx = sword_fx
                    else:
                        p2fx = magic_fx    
                    player2 = Bot(3, player2_pos_x, player2_pos_y, player2_flip,  
                          fighter_DATA[current_enemy], fighter_sheets[current_enemy], fighter_ANI_step[current_enemy],
                         p2fx, joysticks[1], 
                          difficulty[difficulty_choice], current_enemy, inverted)
                    background_choice[level_choice].draw_BG(level_sprites[level_choice], screen)
                    if level_choice == 0:
                        level = "one"
                    elif level_choice == 1:
                        level = "two"
                    elif level_choice == 2:
                        level = "three"
                    elif level_choice == 3:
                        level = "four"  
                    game_started = True
                else:    
                    menu_state = "player2_selector"   
            if fighter1_button.draw(screen, clicked):
                clicked = False
                choice = 0
                player1_name = character_names[0]
                choices.append(choice)
                p1fx = sword_fx
                player1 = Fighter(1, player1_pos_x, player1_pos_y, player1_flip,  
                          fighter_DATA[choice], fighter_sheets[choice], fighter_ANI_step[choice],p1fx, joysticks[0])
                if arcade_mode: 
                    enemies = set_last_enemy(enemies,choice)
                    current_enemy = enemies.pop(0)
                    level_choice = level_choice_list.pop(0)
                    if current_enemy != 3:
                        p2fx = sword_fx
                    else:
                        p2fx = magic_fx    
                    player2 = Bot(3, player2_pos_x, player2_pos_y, player2_flip, 
                          fighter_DATA[current_enemy], fighter_sheets[current_enemy], fighter_ANI_step[current_enemy],
                         p2fx, joysticks[1], 
                          difficulty[difficulty_choice], current_enemy, inverted)
                    background_choice[level_choice].draw_BG(level_sprites[level_choice], screen)
                    if level_choice == 0:
                        level = "one"
                    elif level_choice == 1:
                        level = "two"
                    elif level_choice == 2:
                        level = "three"
                    elif level_choice == 3:
                        level = "four"  
                    game_started = True
                else:    
                    menu_state = "player2_selector"   
            if fighter2_button.draw(screen, clicked):
                clicked = False
                choice = 1
                player1_name = character_names[1]
                choices.append(choice)
                p1fx = sword_fx
                player1 = Fighter(1, player1_pos_x, player1_pos_y, player1_flip, 
                          fighter_DATA[choice], fighter_sheets[choice], fighter_ANI_step[choice], p1fx, joysticks[0])
                if arcade_mode: 
                    enemies = set_last_enemy(enemies,choice)
                    current_enemy = enemies.pop(0)
                    level_choice = level_choice_list.pop(0)
                    if current_enemy != 3:
                        p2fx = sword_fx
                    else:
                        p2fx = magic_fx    
                    player2 = Bot(3, player2_pos_x, player2_pos_y, player2_flip,  
                          fighter_DATA[current_enemy], fighter_sheets[current_enemy], fighter_ANI_step[current_enemy],
                         p2fx, joysticks[1], 
                          difficulty[difficulty_choice], current_enemy, inverted)
                    background_choice[level_choice].draw_BG(level_sprites[level_choice], screen)
                    if level_choice == 0:
                        level = "one"
                    elif level_choice == 1:
                        level = "two"
                    elif level_choice == 2:
                        level = "three"
                    elif level_choice == 3:
                        level = "four"  
                    game_started = True
                else:    
                    menu_state = "player2_selector"
                
            if fighter3_button.draw(screen, clicked):
                clicked = False
                choice = 2
                player1_name = character_names[2]
                choices.append(choice)
                p1fx = sword_fx
                player1 = Fighter(1, player1_pos_x, player1_pos_y, player1_flip, 
                          fighter_DATA[choice], fighter_sheets[choice], fighter_ANI_step[choice], p1fx, joysticks[0])
                if arcade_mode: 
                    enemies = set_last_enemy(enemies,choice)
                    current_enemy = enemies.pop(0)
                    if current_enemy != 3:
                        p2fx = sword_fx
                    else:
                        p2fx = magic_fx    
                    player2 = Bot(3, player2_pos_x, player2_pos_y, player2_flip, 
                          fighter_DATA[current_enemy], fighter_sheets[current_enemy], fighter_ANI_step[current_enemy],
                         p2fx, joysticks[1], 
                          difficulty[difficulty_choice], current_enemy, inverted)
                    background_choice[level_choice_list[0]].draw_BG(level_sprites[level_choice_list[0]], screen)
                    if level_choice == 0:
                        level = "one"
                    elif level_choice == 1:
                        level = "two"
                    elif level_choice == 2:
                        level = "three"
                    elif level_choice == 3:
                        level = "four"  
                    game_started = True
                else:    
                    menu_state = "player2_selector"
            if fighter4_button.draw(screen, clicked):
                clicked = False
                choice = 3
                player1_name = character_names[3]
                choices.append(choice)
                p1fx = magic_fx
                player1 = Fighter(1, player1_pos_x, player1_pos_y, player1_flip, 
                          fighter_DATA[choice], fighter_sheets[choice], fighter_ANI_step[choice], p1fx, joysticks[0])
                if arcade_mode: 
                    enemies = set_last_enemy(enemies,choice)
                    current_enemy = enemies.pop(0)
                    level_choice = level_choice_list.pop(0)
                    if current_enemy != 3:
                        p2fx = sword_fx
                    else:
                        p2fx = magic_fx
                        
                    player2 = Bot(3, player2_pos_x, player2_pos_y, player2_flip,  
                          fighter_DATA[current_enemy], fighter_sheets[current_enemy], fighter_ANI_step[current_enemy],
                         p2fx, joysticks[1], 
                          difficulty[difficulty_choice], current_enemy, inverted)
                    background_choice[level_choice].draw_BG(level_sprites[level_choice], screen)
                    if level_choice == 0:
                        level = "one"
                    elif level_choice == 1:
                        level = "two"
                    elif level_choice == 2:
                        level = "three"
                    elif level_choice == 3:
                        level = "four"  
                    game_started = True
                else:    
                    menu_state = "player2_selector"   
        if menu_state == "player2_selector":
            #redraws the background and names of characters for character selector
            small_house_gif.draw_BG(bg_image_smalltown, screen)
            draw_player_select_text(player)
            #draws the fighters buttons and creates player 2's instance based off of choice
            if random_fighter_button.draw(screen, clicked):
                clicked = False
                choice = random.randint(0,3)
                choices.append(choice)
                player2_name = character_names[choice]
                character_names
                if choice != 3:
                    p2fx = sword_fx
                else:
                    p2fx = magic_fx
                if playerCount == 1:
                    player2 = Bot(3, player2_pos_x, player2_pos_y, player2_flip, 
                          fighter_DATA[choice], fighter_sheets[choice], fighter_ANI_step[choice], p2fx, joysticks[1], 
                          difficulty[difficulty_choice], choice, inverted)
                else:    
                    player2 = Fighter(2, player2_pos_x, player2_pos_y, player2_flip, 
                          fighter_DATA[choice], fighter_sheets[choice], fighter_ANI_step[choice], p2fx, joysticks[1])
                menu_state = "level_choice"   
            if fighter1_button.draw(screen, clicked):
                clicked = False
                choice = 0
                player2_name = character_names[0]
                choices.append(choice)
                p2fx = sword_fx
                if playerCount == 1:
                    player2 = Bot(3, player2_pos_x, player2_pos_y, player2_flip, 
                          fighter_DATA[choice], fighter_sheets[choice], fighter_ANI_step[choice], p2fx, joysticks[1],
                          difficulty[difficulty_choice], choice, inverted)
                else:    
                    player2 = Fighter(2, player2_pos_x, player2_pos_y, player2_flip, 
                          fighter_DATA[choice], fighter_sheets[choice], fighter_ANI_step[choice], p2fx, joysticks[1])
                menu_state = "level_choice"
            if fighter2_button.draw(screen, clicked):
                 clicked = False 
                 choice = 1
                 player2_name = character_names[1]
                 choices.append(choice)
                 p2fx = sword_fx
                 if playerCount == 1:
                    player2 = Bot(3, player2_pos_x, player2_pos_y, player2_flip, 
                          fighter_DATA[choice], fighter_sheets[choice], fighter_ANI_step[choice], p2fx, joysticks[1], 
                          difficulty[difficulty_choice], choice, inverted)
                 else:    
                    player2 = Fighter(2, player2_pos_x, player2_pos_y, player2_flip, 
                          fighter_DATA[choice], fighter_sheets[choice], fighter_ANI_step[choice], p2fx, joysticks[1])
                 menu_state = "level_choice"
            if fighter3_button.draw(screen, clicked):
                clicked = False
                choice = 2
                player2_name = character_names[2]
                choices.append(choice)
                p2fx = sword_fx
                if playerCount == 1:
                    player2 = Bot(3, player2_pos_x, player2_pos_y, player2_flip, 
                          fighter_DATA[choice], fighter_sheets[choice], fighter_ANI_step[choice], p2fx, joysticks[1], 
                          difficulty[difficulty_choice], choice, inverted)
                else:    
                    player2 = Fighter(2, player2_pos_x, player2_pos_y, player2_flip, 
                          fighter_DATA[choice], fighter_sheets[choice], fighter_ANI_step[choice], p2fx, joysticks[1])
                menu_state = "level_choice"
            if fighter4_button.draw(screen, clicked):
                clicked = False
                choice = 3
                player2_name = character_names[3]
                choices.append(choice)
                p2fx = magic_fx
                if playerCount == 1:
                    player2 = Bot(3, player2_pos_x, player2_pos_y, player2_flip, 
                          fighter_DATA[choice], fighter_sheets[choice], fighter_ANI_step[choice], p2fx, joysticks[1], 
                          difficulty[difficulty_choice], choice, inverted)
                else:    
                    player2 = Fighter(2, player2_pos_x, player2_pos_y, player2_flip, 
                          fighter_DATA[choice], fighter_sheets[choice], fighter_ANI_step[choice], p2fx, joysticks[1])
                menu_state = "level_choice"
        if menu_state == "level_choice": 
            #Draw level choice background and menu and use choice to set the background instance
            small_house_gif.draw_BG(bg_image_smalltown, screen)
            draw_text("CHOOSE LEVEL", count_font, BLACK, 275, 50)
            if random_level_button.draw(screen, clicked):
                clicked = False
                game_started = True
                level_choice = random.randint(0,3)
                if level_choice == 0:
                    level = "one"
                elif level_choice == 1:
                    level = "two"
                elif level_choice == 2:
                    level = "three"
                elif level_choice == 3:
                    level = "four"   
            if level1.draw(screen, clicked):
                clicked = False
                game_started = True
                level_choice = 0
                level = "one"
            if level2.draw(screen, clicked):
                clicked = False
                game_started = True
                level_choice = 1
                level = "two"
            if level3.draw(screen, clicked):
                clicked = False
                game_started = True
                level_choice = 2
                level = "three"
            if level4.draw(screen, clicked):
                clicked = False
                game_started = True
                level_choice = 3
                level = "four"        
    else:
        if tutorial:
            ship_gif.draw_BG(bg_image_ship, screen)
            level = "tutorial"
        else:

            background_choice[level_choice].draw_BG(level_sprites[level_choice], screen)
        #Check if game is paused
        if game_pause == True:
           
            #check menu state
            if menu_state == "pause":
                draw_box(270, 400, 175, BLACK, 370, 150)
                #draw pause screen
                if resume_button.draw(screen, clicked):
                    clicked = False
                    game_pause = False
                    if tutorial:
                       space_bar_pressed = True 
                if move_list_button.draw(screen, clicked):
                    clicked = False
                    menu_state = "moves_list"
                if main_menu_button.draw(screen, clicked):
                    clicked = False
                    game_started = False
                    game_pause = False
                    tutorial = False
                    tutorial_round_one = False
                    arcade_mode = False
                    #resets the timer variables so you have a proper count down each time
                    intro_count = 3
                    logo_count = 2
                    menu_state = "main"
                    choices.clear()
                    enemies.clear()
                    level_choice_list.clear()
                    score = [0,0]
            #check if moves list is open
            if menu_state == "moves_list":
               draw_moves_list(choices)
               if back_button.draw(screen, clicked):
                   clicked = False
                   menu_state = "pause"       
        else:        
             #show player stats and character names
             display_all_stats()
             
             #update countdown
             if intro_count <= 0:
                 #display logo
                 if logo_count > 0:
                     draw_text("BRAWL", count_font, YELLOW, (SCREEN_WIDTH / 2.5), (SCREEN_HEIGHT / 3))
                     if (pygame.time.get_ticks() - last_count_update) >= 1000:
                         logo_count -= 1
                         last_count_update = pygame.time.get_ticks()
                
                 #move fighters        
                 player1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player2, round_over, choices, controller_names)
                 if tutorial:
                    text_for_tutorial()
                    key = pygame.key.get_pressed()
                    if key[pygame.K_a]:
                        a_button_pressed = True
                    if key[pygame.K_s]:
                        s_button_pressed = True
                    if key[pygame.K_d]:
                        d_button_pressed = True
                    if key[pygame.K_w]:
                        w_button_pressed = True
                    if key[pygame.K_r]:
                        r_button_pressed = True
                    if key[pygame.K_t]:
                        t_button_pressed = True
                    if key[pygame.K_f]:
                        f_button_pressed = True
                    if key[pygame.K_SPACE]:
                        space_bar_pressed = True
                    if a_button_pressed:
                        pygame.draw.line(screen,RED,(25,112),(110,112), 4)
                    if d_button_pressed:
                        pygame.draw.line(screen,RED,(25,132),(110,132), 4)
                    if w_button_pressed:
                        pygame.draw.line(screen,RED,(25,152),(110,152), 4) 
                    if s_button_pressed:
                        pygame.draw.line(screen,RED,(25,172),(110,172), 4)             
                    if r_button_pressed:
                        pygame.draw.line(screen,RED,(25,192),(110,192), 4)      
                    if t_button_pressed:
                        pygame.draw.line(screen,RED,(25,212),(110,212), 4)       
                    if f_button_pressed:
                        pygame.draw.line(screen,RED,(25,232),(260,232), 4)       
                    if space_bar_pressed:
                        pygame.draw.line(screen,RED,(25,252),(160,252), 4)
                    if tutorial_round_one == False and player1.alive and player2.alive:
                        draw_text("WIN FIGHT", count_font, WHITE, 330, 145)
                    if tutorial_finished:
                        pygame.draw.line(screen,RED,(330,145),(630,145), 8)
                 if tutorial_round_one == False:
                     
                     #if playerCount == 1:
                      #  player2.movement_timer(difficulty[difficulty_choice])
                       # if player2.move_timer >= 0 and player2.move_timer < 50:

                         #   player2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player1, round_over, choices, controller_names)
                   #  elif playerCount == 2:
                    player2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player1, round_over, choices, controller_names)
                 
             else:
                 #display count timer
                 if score[0] + score[1] == 2:
                    draw_text("FINAL ROUND", count_font, YELLOW, (SCREEN_WIDTH / 3), (SCREEN_HEIGHT / 3))
                 else:
                    draw_text(("ROUND " + str((score[0]) + (score[1]) + 1)), count_font, YELLOW, (SCREEN_WIDTH / 2.6), (SCREEN_HEIGHT / 3))             
                 #update countdown timer
                 if (pygame.time.get_ticks() - last_count_update) >= 1000:
                     intro_count -= 1
                     last_count_update = pygame.time.get_ticks()
             
             #update Players       
             player1.update()
             player2.update()
             #draw fighters
             player1.draw(player2, screen)
             player2.draw(player1, screen)
             
             #Check for player defeat
             if round_over == False:
                 if player1.alive == False:
                     score[1] += 1
                     round_over = True
                     round_over_time = pygame.time.get_ticks()
                     win_logo_time = pygame.time.get_ticks()
                 elif player2.alive == False:
                     score[0] += 1
                     round_over = True
                     round_over_time = pygame.time.get_ticks()
                     win_logo_time = pygame.time.get_ticks()
             else:
                 #display victory image
                 screen.blit(victory_img, (350, 100))
        
                 if player1.alive == False and pygame.time.get_ticks() - win_logo_time > WINNER_TIMER:
                     draw_text("PLAYER 2 WINS!", count_font, WHITE, 280, 145)
                 elif player2.alive == False and pygame.time.get_ticks() - win_logo_time > WINNER_TIMER:
                     draw_text("PLAYER 1 WINS!", count_font, WHITE, 280, 145)
                 if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                    if tutorial:
                        if score[0] == 1:
                            tutorial_round_one = False
                            
                        if score[0] + score[1] == 3 or score[0] == 2 or score[1] == 2:
                            if score[0] == 2:
                                tutorial_finished = True
                            draw_box(300, 250, 175, BLACK, 370, 240)
                            if rematch_button.draw(screen, clicked):
                                clicked = False
                                #reset variables
                                round_over = False
                                tutorial_finished = False
                                intro_count = 3
                                logo_count = 2
                                score = [0,0]
                                #recreate the instances of players, resetting their static values
                                player1 = Fighter(1, player1_pos_x, player1_pos_y, player1_flip, 
                                fighter_DATA[choices[0]], fighter_sheets[choices[0]], fighter_ANI_step[choices[0]], p1fx, joysticks[1])
                                if playerCount == 1:   
                                    player2 = Bot(3, player2_pos_x, player2_pos_y, player2_flip, 
                                        fighter_DATA[choices[1]], fighter_sheets[choices[1]], fighter_ANI_step[choices[1]], p2fx, joysticks[1], 
                                        difficulty[difficulty_choice],choices[1], inverted)
                                else:
                                    player2 = Fighter(2, player2_pos_x, player2_pos_y, player2_flip, 
                                        fighter_DATA[choices[1]], fighter_sheets[choices[1]], fighter_ANI_step[choices[1]], p2fx, joysticks[1], inverted)
                            if main_menu_button2.draw(screen, clicked):
                                clicked = False
                                game_started = False
                                game_pause = False
                                tutorial = False
                                tutorial_finished = False
                                tutorial_round_one = False
                                #resets the timer variables so you have a proper count down each time
                                intro_count = 3
                                logo_count = 2
                                menu_state = "main"
                                choices.clear()
                                score = [0,0]
                        else:
                         #reset variables
                            round_over = False
                            intro_count = 3
                            logo_count = 2
                            #recreate the instances of players, resetting their static values
                            player1 = Fighter(1, player1_pos_x, player1_pos_y, player1_flip, 
                                fighter_DATA[choices[0]], fighter_sheets[choices[0]], fighter_ANI_step[choices[0]], p1fx, joysticks[0])
                            player2 = Bot(3, player2_pos_x, player2_pos_y, player2_flip, 
                                fighter_DATA[choices[1]], fighter_sheets[choices[1]], fighter_ANI_step[choices[1]], p2fx, joysticks[1], 
                                difficulty[difficulty_choice], choices[1], inverted)
                    if arcade_mode:
                        if score[1] == 2:
                            draw_box(300, 250, 175, BLACK, 370, 240)
                           
                            if rematch_button.draw(screen, clicked):
                                clicked = False
                                #reset variables
                                round_over = False
                                intro_count = 3
                                logo_count = 2
                                score = [0,0]
                                #recreate the instances of players, resetting their static values
                                player1 = Fighter(1, player1_pos_x, player1_pos_y, player1_flip, 
                                fighter_DATA[choices[0]], fighter_sheets[choices[0]], fighter_ANI_step[choices[0]], p1fx, joysticks[1])
                                player2 = Bot(3, player2_pos_x, player2_pos_y, player2_flip, 
                                    fighter_DATA[current_enemy], fighter_sheets[current_enemy], fighter_ANI_step[current_enemy], p2fx, joysticks[1], 
                                    difficulty[difficulty_choice], current_enemy, inverted)                               
                            if player_select_button.draw(screen, clicked):
                                clicked = False
                                game_started = False
                                menu_state = "player1_selector"
                                score = [0, 0]
                                choices.clear()
                            if main_menu_button2.draw(screen, clicked):
                                clicked = False
                                game_started = False
                                game_pause = False
                                arcade_mode = False
                                #resets the timer variables so you have a proper count down each time
                                intro_count = 3
                                logo_count = 2
                                menu_state = "main"
                                choices.clear()
                                enemies.clear()
                                level_choice_list.clear()
                                score = [0,0]       
                        elif score[0] == 2:
                            if len(enemies) > 0:
                                draw_box(300, 250, 175, BLACK, 370, 240)
                                if next_fight_button.draw(screen, clicked):
                                    clicked = False
                                    #reset variables
                                    round_over = False
                                    intro_count = 3
                                    logo_count = 2
                                    score = [0,0]
                                    current_enemy = enemies.pop(0)
                                    level_choice = level_choice_list.pop(0)
                                    if level_choice == 0:
                                        level = "one"
                                    elif level_choice == 1:
                                        level = "two"
                                    elif level_choice == 2:
                                        level = "three"
                                    elif level_choice == 3:
                                        level = "four" 
                                    difficulty_choice += 1
                                    #recreate the instances of players, resetting their static values
                                    player1 = Fighter(1, player1_pos_x, player1_pos_y, player1_flip,
                                    fighter_DATA[choices[0]], fighter_sheets[choices[0]], fighter_ANI_step[choices[0]], p1fx, joysticks[0])
                                    if current_enemy != 3:
                                        p2fx = sword_fx
                                    else:
                                        p2fx = magic_fx
                                    if len(enemies) > 0:
                                        player2 = Bot(3, player2_pos_x, player2_pos_y, player2_flip, 
                                            fighter_DATA[current_enemy], fighter_sheets[current_enemy], fighter_ANI_step[current_enemy], p2fx, joysticks[1], 
                                            difficulty[difficulty_choice], current_enemy, inverted)
                                    else:
                                        inverted = True
                                        player2 = Bot(3, player2_pos_x, player2_pos_y, player2_flip, 
                                            fighter_DATA[current_enemy], dark_fighter_sheets[current_enemy], fighter_ANI_step[current_enemy], p2fx, joysticks[1], 
                                            difficulty[difficulty_choice], current_enemy, inverted)
                                if main_menu_button2.draw(screen, clicked):
                                    clicked = False
                                    game_started = False
                                    game_pause = False
                                    arcade_mode = False
                                    #resets the timer variables so you have a proper count down each time
                                    intro_count = 3
                                    logo_count = 2
                                    menu_state = "main"
                                    choices.clear()
                                    enemies.clear()
                                    level_choice_list.clear()
                                    score = [0,0] 
                            else:
                                clicked = False
                                game_started = False
                                game_pause = False
                                #resets the timer variables so you have a proper count down each time
                                intro_count = 3
                                logo_count = 2
                                menu_state = "main"
                                choices.clear()
                                enemies.clear()
                                level_choice_list.clear()
                                
                        else:
                            round_over = False
                            intro_count = 3
                            #recreate the instances of players, resetting their static values
                            player1 = Fighter(1, player1_pos_x, player1_pos_y, player1_flip, 
                            fighter_DATA[choices[0]], fighter_sheets[choices[0]], fighter_ANI_step[choices[0]], p1fx, joysticks[1])
                            if len(enemies) > 0:
                                player2 = Bot(3, player2_pos_x, player2_pos_y, player2_flip, 
                                    fighter_DATA[current_enemy], fighter_sheets[current_enemy], fighter_ANI_step[current_enemy], p2fx, joysticks[1], 
                                    difficulty[difficulty_choice], current_enemy, inverted)
                            else:
                                
                                player2 = Bot(3, player2_pos_x, player2_pos_y, player2_flip, 
                                    fighter_DATA[current_enemy], dark_fighter_sheets[current_enemy], fighter_ANI_step[current_enemy], p2fx, joysticks[1], 
                                    difficulty[difficulty_choice], current_enemy, inverted)
                            #player2 = Bot(3, player2_pos_x, player2_pos_y, player2_flip, 
                             #   fighter_DATA[current_enemy], fighter_sheets[current_enemy], fighter_ANI_step[current_enemy], p2fx, joysticks[1], 
                             #   difficulty[difficulty_choice], current_enemy,inverted)
                    
                    else:
                        if score[0] + score[1] == 3 or score[0] == 2 or score[1] == 2:
                            draw_box(300, 250, 175, BLACK, 370, 240)
                            if rematch_button.draw(screen, clicked):
                                clicked = False
                                #reset variables
                                round_over = False
                                intro_count = 3
                                logo_count = 2
                                score = [0,0]
                                #recreate the instances of players, resetting their static values
                                player1 = Fighter(1, player1_pos_x, player1_pos_y, player1_flip, 
                                fighter_DATA[choices[0]], fighter_sheets[choices[0]], fighter_ANI_step[choices[0]], p1fx, joysticks[0])
                                if playerCount == 1: 
                                    player2 = Bot(3, player2_pos_x, player2_pos_y, player2_flip, 
                                        fighter_DATA[choices[1]], fighter_sheets[choices[1]], fighter_ANI_step[choices[1]], p2fx, joysticks[1], 
                                        difficulty[difficulty_choice],choices[1],inverted)
                                if playerCount == 2:  
                                    player2 = Fighter(2, player2_pos_x, player2_pos_y, player2_flip, 
                                        fighter_DATA[choices[1]], fighter_sheets[choices[1]], fighter_ANI_step[choices[1]], p2fx, joysticks[1])
                            if player_select_button.draw(screen, clicked):
                                clicked = False
                                game_started = False
                                menu_state = "player1_selector"
                                score = [0, 0]
                                choices.clear()
                            if main_menu_button2.draw(screen, clicked):
                                clicked = False
                                game_started = False
                                game_pause = False
                                #resets the timer variables so you have a proper count down each time
                                intro_count = 3
                                logo_count = 2
                                menu_state = "main"
                                choices.clear()
                                score = [0,0]
                        else:
                         #reset variables
                            round_over = False
                            intro_count = 3
                            logo_count = 2
                            #recreate the instances of players, resetting their static values
                            player1 = Fighter(1, player1_pos_x, player1_pos_y, player1_flip, 
                                fighter_DATA[choices[0]], fighter_sheets[choices[0]], fighter_ANI_step[choices[0]], p1fx, joysticks[0])
                            if playerCount == 1:
  
                                player2 = Bot(3, player2_pos_x, player2_pos_y, player2_flip,
                                    fighter_DATA[choices[1]], fighter_sheets[choices[1]], fighter_ANI_step[choices[1]], p2fx, joysticks[1], 
                                    difficulty[difficulty_choice], choices[1],inverted)
                            else:
                                
                                player2 = Fighter(2, player2_pos_x, player2_pos_y, player2_flip,
                                    fighter_DATA[choices[1]], fighter_sheets[choices[1]], fighter_ANI_step[choices[1]], p2fx, joysticks[1])
               
        
                
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.JOYDEVICEADDED:
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks.insert(event.device_index,joy)
            if event.device_index == 0:
                gamepad1 = True
            if event.device_index == 1:
                gamepad2 = True
            controller_names[event.device_index] = str(joy.get_name())
            if controller_names[event.device_index].find("PS4") != -1:
                controller_names[event.device_index] = "ps4"
            else:
                controller_names[event.device_index] = "xbox"  
        if event.type == JOYDEVICEREMOVED:
            if len(joysticks) < 1:
                joy = None
                joysticks.clear()
                gamepad2 = False
                gamepad1 = False
                controller_names = ["",""]
            else:

                for gamepad in joysticks:
                    if gamepad.get_instance_id() == 0:
                        gamepad2 = False
                        gamepad1 = True
                    if gamepad.get_instance_id() == 0:
                        gamepad2 = True
                        gamepad1 = False
                        
                        
            
        if event.type == pygame.KEYDOWN:   
            if event.key == pygame.K_SPACE and game_started:
                game_pause = True
                menu_state = "pause"
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False
           
        if event.type == pygame.QUIT:
            runGame = False
               
    #update the display   
    pygame.display.update()        
            
#Exit Pygame
pygame.quit()
