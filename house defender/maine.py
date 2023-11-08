import pygame
from sys import exit
import random
import math
import time

class Monkeys(pygame.sprite.Sprite):
    house_health = 10
    counter = 0
    created_counter = 0
    def __init__(self):
        super().__init__()

        self.banana_surf = pygame.image.load("sprites/banana.png").convert_alpha()
        self.dangerous = True

        self.side = random.choice(["up", "down", "left", "right"])

        self.image = pygame.image.load("sprites/monkey.png").convert_alpha()
        self.rect = self.image.get_rect()

        if self.side == "up":
            self.rect.bottom = 0
            self.rect.left = random.randint(-51,screen.get_width())

        elif self.side == "down":
            self.rect.top = screen.get_height()
            self.rect.left = random.randint(-51,screen.get_width())

        elif self.side == "left":
            self.rect.bottom = random.randint(0,screen.get_height() + 50)
            self.rect.right = 0

        elif self.side == "right":
            self.rect.bottom = random.randint(0,screen.get_height() + 50)
            self.rect.left = screen.get_width()

        self.angle = math.atan((self.rect.centery - screen.get_height() / 2) / (screen.get_width() / 2 - self.rect.centerx))
        if screen.get_width() / 2 - self.rect.centerx < 0:
            self.angle += math.pi
        self.num = 0

        self.original_x = self.rect.centerx
        self.original_y = self.rect.centery

        self.animation = 0

    def spinning_animation(self):
        if (self.animation * 10) % 10 == 0:
            self.image = pygame.transform.rotozoom(self.image,90,1)
            self.rect = self.image.get_rect()
        self.animation += 0.25

    @staticmethod
    def reset():
        Monkeys.house_health = original_health
        Monkeys.counter = 0
        Monkeys.created_counter = 0

    def update(self):
        if killing_rect and self.rect.colliderect(killing_rect) and self.dangerous:
            self.image = self.banana_surf
            self.dangerous = False

        elif self.rect.colliderect(house_rect):
            Monkeys.counter += 1
            self.kill()
            self.remove(monkeys_group)
            if self.dangerous: Monkeys.house_health -= 1
            else:
                coins_group.add(Coins_text())
                Coins_text.coins += 1

        self.spinning_animation()

        self.num += SPEED
        self.rect.center = (int(self.original_x + math.cos(self.angle) * self.num),int(self.original_y - math.sin(self.angle) * self.num))

class Coins_text(pygame.sprite.Sprite):
    coins = 0
    def __init__(self):
        super().__init__()
        self.distance = 10
        self.image = text_font.render(f"+ one banana",False,(111,196,169))
        self.rect = self.image.get_rect(center = (screen.get_width() / 2, screen.get_height() / 2 - house_surf.get_height() / 2 - 25))


    def update(self):
        self.rect = self.image.get_rect(center = (screen.get_width() / 2, screen.get_height() / 2 - house_surf.get_height() / 2 - 25 - self.distance))
        self.distance += 5
        if self.distance == 75:
            self.kill()
            self.remove(monkeys_group)

class Level_buttons(pygame.sprite.Sprite):
    level = 0
    picking_point = None
    def __init__(self,btn_x,btn_y,image, level_number):
        super().__init__()

        print(btn_x,btn_y,image, level_number)
        self.number = level_number
        self.image = image
        self.rect = self.image.get_rect(topleft = (btn_x,btn_y))
        print(self.rect)

    def click(self):
        global stage
        Level_buttons.level = self.number
        stage = "level changing"
        pygame.display.update()

    def update(self):
        if Level_buttons.picking_point and self.rect.collidepoint(Level_buttons.picking_point):
            self.click()

def talking_print_skip(texts, speed):
    global counter
    global active_displaying_text
    global talking_done
    global complete_talking_done

    if talking_done and active_displaying_text < len(texts) - 1: # going to the next text
        active_displaying_text += 1
        talking_done = False
        counter = 0
    elif (not talking_done) and (active_displaying_text != 0): # skipping the text
        talking_done = True
        counter = speed * len(texts[active_displaying_text])
    elif active_displaying_text >= len(texts) - 2 and texts[active_displaying_text][0:counter // speed] == texts[active_displaying_text]:
        complete_talking_done = True

def talking_print(texts, instructions, speed):
    global counter
    global active_displaying_text
    global talking_done

    if counter < speed * len(texts[active_displaying_text]):
        counter += 1
    elif counter >= speed * len(texts[active_displaying_text]):
        what_to_do_text = score_font.render(instructions[active_displaying_text], True, "black")
        screen.blit(what_to_do_text, what_to_do_text.get_rect(bottomright=(1486, screen.get_height() - 25)))
        talking_done = True

    snip = score_font.render(texts[active_displaying_text][0:counter // speed], True, "yellow")
    screen.blit(snip, (10, screen.get_height() - 150))

def pause():
    global stage
    paused = True

    while paused:

        for pause_event in pygame.event.get():
            if pause_event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if pause_event.type == pygame.MOUSEMOTION: curser_rect.center = pause_event.pos

            if (pause_event.type == pygame.MOUSEBUTTONDOWN and play_btn_rect.colliderect(curser_rect)) or (pause_event.type == pygame.KEYDOWN and pause_event.key == pygame.K_ESCAPE):
                paused = False

            if pause_event.type == pygame.MOUSEBUTTONDOWN and map_btn_rect.colliderect(curser_rect):
                pygame.time.set_timer(monkeys_timer,0)
                paused = False
                stage = "map"
                for l in range(1, 4):
                    level_buttons_group.add(Level_buttons(l * 100, 100, pygame.image.load(f'sprites/level{l} button.png').convert_alpha(),l))

            else:
                screen.blit(game_background_surf, (0, 0))
                monkeys_group.draw(screen)
                score_message()
                screen.blit(pause_menu_surf, pause_menu_rect)
                screen.blit(shop_btn_surf, shop_btn_rect)
                screen.blit(map_btn_surf, map_btn_rect)
                screen.blit(play_btn_surf, play_btn_rect)
                screen.blit(curser_img, curser_rect)

        pygame.display.update()
        clock.tick(60)

pygame.init()

# main<>

# variables (main)
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
pygame.display.set_caption("House defender")
clock = pygame.time.Clock()
game_status = "intro"
text_font = pygame.font.Font("fonts/Pixeltype.ttf",25)
score_font = pygame.font.Font("fonts/Pixeltype.ttf",50)
level_changing_font = pygame.font.Font("fonts/Pixeltype.ttf",100)
stages = ["intro", "game", "lose", "level changing"]
Level_buttons.level = 0
stage = stages[0]
changed_mouse = False
curser_img = pygame.image.load("sprites/banana curser.png").convert_alpha()
curser_rect = curser_img.get_rect(center = (0,0))
active_displaying_text = 0

levels = [
    {"monkeys" : 10},
    {"monkeys" : 15},
    {"monkeys" : 15},
    {"monkeys" : 20},
    {"monkeys" : 25},
    {"monkeys" : 30},
    {"monkeys" : 40},
    {"monkeys" : 50},
    {"monkeys" : 60},
    {"monkeys" : 80},
    {"monkeys" : 100}
]

# Backgrounds (main)
game_background_surf = pygame.image.load("sprites/background.jpg").convert()
map_background1 = pygame.image.load("sprites/levels background 1.jpg").convert()

# Buttons (main)
shop_btn_surf = pygame.image.load("sprites/shop button.png").convert_alpha()
shop_btn_rect = shop_btn_surf.get_rect(center = (screen.get_width() / 2, screen.get_height() / 2 - 100))

map_btn_surf = pygame.image.load("sprites/map button.png").convert_alpha()
map_btn_rect = map_btn_surf.get_rect(center = (screen.get_width() / 2, screen.get_height() / 2 - 25))

pause_btn_surf = pygame.image.load("sprites/pause button.png").convert_alpha()
pause_btn_rect = pause_btn_surf.get_rect(topleft = (25, 10))

play_btn_surf = pygame.image.load("sprites/play button.png").convert_alpha()
play_btn_rect = play_btn_surf.get_rect(center = (screen.get_width() / 2, screen.get_height() / 2 + 100))

pause_menu_surf = pygame.image.load("sprites/pause menu.png").convert()
pause_menu_rect = pause_menu_surf.get_rect(center = (screen.get_width() / 2, screen.get_height() / 2))

# intro stuff <>

intro_screen_stages = ["talking menu", "talking", "finish"]
current_intro_screen_stage = 0

talking_menu_surf = pygame.image.load("sprites/talking menu.png").convert_alpha()
magic_banana_wand_surf = pygame.image.load("sprites/magic banana wand.png").convert_alpha()

# game stuff <>
# variables (game stuff)
SPEED = 5
killing_rect = None
original_health = 10
interval = None

# House sprites (game stuff)
house_surf = pygame.image.load("sprites/house.png").convert_alpha()
house_surf = pygame.transform.rotozoom(house_surf,0,2)
house_rect = house_surf.get_rect(center = (screen.get_width() / 2, screen.get_height() / 2))

#functions (game stuff)
def health_bar_draw():
    global health_status
    global health_status_rect

    pygame.draw.rect(screen, "red", (screen.get_width() / 2 - house_surf.get_width() / 2,
                                     screen.get_height() / 2 - house_surf.get_height() / 2 - 15,
                                     Monkeys.house_health * 100 / original_health, 10))
    health_status = text_font.render(str(Monkeys.house_health),False,"black")
    health_status_rect = health_status.get_rect(center = (screen.get_width() / 2,
                                                screen.get_height() / 2 - house_surf.get_height() / 2 - 25))

def score_message():
    score_text = score_font.render(f"You have {Coins_text.coins}",False,"#eb7310")
    mini_banana_surf = pygame.image.load("sprites/mini banana.png").convert_alpha()
    score_text_rect = score_text.get_rect(midtop = (screen.get_width() / 2, 20))
    mini_banana_rect = mini_banana_surf.get_rect(midleft = score_text_rect.midright)
    mini_banana_rect.left -= 5
    mini_banana_rect.bottom -= 5
    score_text_rect.left -= (mini_banana_rect.right - mini_banana_rect.left) / 2
    screen.blit(score_text, score_text_rect)
    screen.blit(mini_banana_surf, mini_banana_rect)

# lose stuff <>

losing_screen_stages = ["switching", "talking_menu", "talking1", "chasing1", "talking2", "chasing2", "animation"]
current_losing_screen_stage = 0

# switching (lose stuff)
switching_cubes = 8
switching_cubes_counter = 0
original_switching_cube_size = screen.get_width() / 16

# chasing (lose stuff)
chasing1 = [
    {"done" : False, "rect" : (screen.get_width() / 4 * 3, screen.get_height() / 2), "img" : "sprites/chasing monkey.png"}
]
chasing_stage = 0

chasing2 = [
    {"done" : False, "rect" : (screen.get_width() / 2 + screen.get_width() / 8,screen.get_height() / 2 - 200), "img" : "sprites/chasing monkey 2.png"},
    {"done" : False, "rect" : (screen.get_width() / 2,screen.get_height() / 2), "img" : "sprites/chasing monkey 2.png"}
]

chasing_monkey_surf = pygame.image.load(chasing1[chasing_stage]["img"]).convert_alpha()
chasing_monkey_rect = chasing_monkey_surf.get_rect(center = (screen.get_width() / 2, screen.get_height() / 2))

# animation (lose stuff)
static_animations = [
    {"done" : False, "place" : (screen.get_width() / 2, screen.get_height() / 2), "img family" : "sprites/dust animation", "starting number" : 1, "ending number" : 8, "step number" : 1},
    {"done" : False, "place" : (screen.get_width() / 2, screen.get_height() / 2), "img family" : "sprites/dust animation", "starting number" : 7, "ending number" : 0, "step number" : -1}
]
current_static_animation = 0
current_dust_animation = 1

# map stuff <>

# Timers (game stuff)
monkeys_timer = pygame.USEREVENT + 1
chasing_timer = pygame.USEREVENT + 2

# Groups (game stuff)
monkeys_group = pygame.sprite.Group()
coins_group = pygame.sprite.Group()
level_buttons_group = pygame.sprite.Group()

print(f"width: {screen.get_width()}, height: {screen.get_height()}")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if not stage == "lose" and changed_mouse and event.type == pygame.MOUSEMOTION:
            curser_rect.center = event.pos

        if stage == "map" and event.type == pygame.MOUSEBUTTONDOWN:
            Level_buttons.picking_point = event.pos
        else:
            Level_buttons.picking_point = None

        if not stage == "map" and not stage == "intro" and not stage == "level changing" and not stage == "lose" and ((event.type == pygame.MOUSEBUTTONDOWN and pause_btn_rect.collidepoint(event.pos)) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
            pause()

        if stage == "intro": # intro events
            if intro_screen_stages[current_intro_screen_stage] == "finish": # checking if we finished talking to the player
                # checks if the big banana wand button is clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if magic_banana_wand_surf.get_rect(center = (screen.get_width() / 2, screen.get_height() / 2 - 75)).collidepoint(event.pos):
                        pygame.mouse.set_visible(False)
                        level_changing_counter = 0
                        level_changing_speed = 25
                        changed_mouse = True
                        stage = stages[-1]
                        Level_buttons.level = 1
            if intro_screen_stages[current_intro_screen_stage] == "finish" or active_displaying_text >= 3:
                # checks if you hover over the banana wand to make it glow
                if event.type == pygame.MOUSEMOTION:
                    if magic_banana_wand_surf.get_rect(center = (screen.get_width() / 2, screen.get_height() / 2 - 75)).collidepoint(event.pos): magic_banana_wand_surf = pygame.image.load("sprites/glowing magic banana wand.png"). convert_alpha()
                    else: magic_banana_wand_surf = pygame.image.load("sprites/magic banana wand.png").convert_alpha()

            if intro_screen_stages[current_intro_screen_stage] == "talking":

                if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN:
                    talking_print_skip(
                        ["Hello mighty stranger!", "Our house is getting attacked by some lunatic space monkeys.",
                         "Your mission is to turn these monkeys into bananas by this magic wand.", "Good luck! :)"], 3)

        if stage == "game": # game events
            if event.type == monkeys_timer:
                Monkeys.created_counter += 1
                monkeys_group.add(Monkeys())

            if event.type == pygame.MOUSEBUTTONDOWN:
                killing_rect = (event.pos[0], event.pos[1], -25, -25)
            else: killing_rect = None

        if stage == "lose":
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN:
                if "talking1" in losing_screen_stages[current_losing_screen_stage]:
                    talking_print_skip(["Oh no!"],3)
                if "talking2" in losing_screen_stages[current_losing_screen_stage]:
                    talking_print_skip(["NOOOOOOO", "The monkey took your wanddd!!!"],3)

    # not related to any specific stage things
    if not (stage == "lose" and (losing_screen_stages[current_losing_screen_stage] == "switching" or losing_screen_stages[current_losing_screen_stage] == "talking2")): screen.blit(game_background_surf, (0, 0))
    if (stage != "lose" and (losing_screen_stages[current_losing_screen_stage] != "switching" or losing_screen_stages[current_losing_screen_stage] != "talking2")) and (stage != "intro") and (stage != "level changing"):

        screen.blit(pause_btn_surf, pause_btn_rect)

    if stage == "intro": # everything that's displaying in the intro

        if intro_screen_stages[current_intro_screen_stage] == "talking menu":
            for x in range (0,1537,3):
                screen.blit(talking_menu_surf, talking_menu_surf.get_rect(bottomleft = (x - 1536, screen.get_height())))
                time.sleep(0.001)
                pygame.display.update()
            current_intro_screen_stage += 1
            counter = 0
            active_displaying_text = 0
            complete_talking_done = False
            talking_done = False


        # text animation
        elif intro_screen_stages[current_intro_screen_stage] == "talking":
            screen.blit(talking_menu_surf, talking_menu_surf.get_rect(bottomleft=(0, screen.get_height())))
            talking_print(["Hello mighty stranger!", "Our house is getting attacked by some lunatic space monkeys.", "Your mission is to turn these monkeys into bananas by this magic wand.", "Good luck! :)"],
                          ["Press Enter or Click Anywhere", "Press Enter or Click Anywhere", "Press Enter or Click Anywhere", "Click the wand"], 3)
            if complete_talking_done:
                current_intro_screen_stage += 1
            if 2 <= active_displaying_text: screen.blit(magic_banana_wand_surf, magic_banana_wand_surf.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 75)))

        elif intro_screen_stages[current_intro_screen_stage] == "finish":
            screen.blit(talking_menu_surf, talking_menu_surf.get_rect(bottomleft=(0, screen.get_height())))
            screen.blit(magic_banana_wand_surf,magic_banana_wand_surf.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 75)))
            screen.blit(score_font.render("Click the wand", True, "black"), score_font.render("Click the wand", True, "black").get_rect(bottomright = (1486, screen.get_height() - 25)))
            screen.blit(score_font.render("Good luck! :)",True,"yellow"),(10,screen.get_height() - 150))

    elif stage == "game": # everything that's displaying in the game

        screen.blit(house_surf, house_rect)

        # Monkeys
        monkeys_group.draw(screen)
        monkeys_group.update()

        health_bar_draw()
        screen.blit(health_status, health_status_rect)

        coins_group.draw(screen)
        coins_group.update()

        if Monkeys.house_health <= 0:
            pygame.time.set_timer(monkeys_timer,0)
            current_losing_screen_stage = 0
            stage = "lose"

        if Monkeys.created_counter >= levels[Level_buttons.level-1]["monkeys"]: pygame.time.set_timer(monkeys_timer,0)

        if not interval and Monkeys.counter >= levels[Level_buttons.level-1]["monkeys"]: interval = pygame.time.get_ticks()
        if interval and (pygame.time.get_ticks() - interval >= 1000):
            level_changing_counter = 0
            level_changing_speed = 25
            stage = "level changing"
            Level_buttons.level += 1
            Monkeys.reset()

        score_message()

    elif stage == "lose":

        if losing_screen_stages[current_losing_screen_stage] != "switching":
            if not static_animations[0]["done"]: screen.blit(house_surf, house_rect)
            else: screen.blit(pygame.image.load("sprites/broken house.png").convert_alpha(), pygame.image.load("sprites/broken house.png").get_rect(center = (screen.get_width() / 2, screen.get_height() / 2)))

        if losing_screen_stages[current_losing_screen_stage] == "switching":
            if switching_cubes_counter < 24:
                for switching_cube in range (switching_cubes): # 0 - 7
                    x = switching_cubes_counter - switching_cube # 0 - 0
                    if -1 < x < 17:
                        switching_cube_size = int(original_switching_cube_size * ((switching_cube + 1) / switching_cubes))
                        for y in range (9):
                            pygame.draw.rect(screen, "black", (int(x * original_switching_cube_size + (original_switching_cube_size - switching_cube_size) / 2),
                                             int(original_switching_cube_size * y + (original_switching_cube_size - switching_cube_size) / 2),
                                             switching_cube_size, switching_cube_size))

                        time.sleep(0.025)
                        pygame.display.update()
                switching_cubes_counter += 1
            else:
                for letter in range (1, len("You lose :(") + 1):
                    if letter >= 4: letter += 1
                    if letter >= 9: letter += 1
                    screen.blit(score_font.render("You lose :("[:letter], True, "white"), score_font.render("You lose :(", True, "white").get_rect(center = (screen.get_width() / 2, screen.get_height() / 2)))
                    time.sleep(0.7)
                    pygame.display.update()
                time.sleep(1.5)
                current_losing_screen_stage += 1

        elif losing_screen_stages[current_losing_screen_stage] == "talking_menu":
            for x in range (0,1537,3):
                screen.blit(talking_menu_surf, talking_menu_surf.get_rect(bottomleft = (x - 1536, screen.get_height())))
                time.sleep(0.001)
                pygame.display.update()
            current_losing_screen_stage += 1
            counter = 0
            active_displaying_text = 0
            complete_talking_done = False
            talking_done = False

        # text animation
        elif losing_screen_stages[current_losing_screen_stage] == "talking1":
            screen.blit(talking_menu_surf, talking_menu_surf.get_rect(bottomleft=(0, screen.get_height())))
            talking_print(["Oh no!"], ["Press Enter or Click Anywhere"], 3)
            if complete_talking_done: current_losing_screen_stage += 1

        elif losing_screen_stages[current_losing_screen_stage] == "chasing1":
            if not chasing1[chasing_stage]["done"]:
                chasing_angle = math.atan((chasing_monkey_rect.centery - chasing1[chasing_stage]["rect"][1]) / (chasing1[chasing_stage]["rect"][0] - chasing_monkey_rect.centerx))
                if chasing1[chasing_stage]["rect"][0] - chasing_monkey_rect.centerx < 0:
                    chasing_angle += math.pi
                chasing_num = 0
                chasing_monkey_animation = 0

                chasing_original_x = chasing_monkey_rect.centerx
                chasing_original_y = chasing_monkey_rect.centery
                chasing1[chasing_stage]["done"] = True

            if chasing_monkey_rect.center[0] // 5 != chasing1[chasing_stage]["rect"][0] // 5 or chasing_monkey_rect.center[1] // 5 != chasing1[chasing_stage]["rect"][1] // 5:
                if chasing_stage < 1:
                    screen.blit(curser_img, chasing1[chasing_stage]["rect"])
                if (chasing_monkey_animation * 10) % 10 == 0:
                    chasing_monkey_surf = pygame.transform.rotozoom(chasing_monkey_surf, 90, 1)
                    chasing_monkey_rect = chasing_monkey_surf.get_rect()
                chasing_monkey_animation += 0.25

                chasing_num += 5
                chasing_monkey_rect.center = (int(chasing_original_x + math.cos(chasing_angle) * chasing_num),int(chasing_original_y - math.sin(chasing_angle) * chasing_num))
            else:
                chasing_monkey_surf = pygame.image.load(chasing1[chasing_stage]["img"]).convert_alpha()
                if chasing_stage < len(chasing1) - 1:
                    chasing_stage += 1
                    chasing_monkey_surf = pygame.image.load(chasing1[chasing_stage]["img"]).convert_alpha()
                else:
                    chasing_stage = 0
                    chasing_monkey_surf = pygame.image.load(chasing2[chasing_stage]["img"]).convert_alpha()
                    chasing_monkey_rect = chasing_monkey_surf.get_rect(center = (int(chasing_original_x + math.cos(chasing_angle) * chasing_num),int(chasing_original_y - math.sin(chasing_angle) * chasing_num)))
                    current_losing_screen_stage += 1
                    counter = 0
                    active_displaying_text = 0
                    complete_talking_done = False
                    talking_done = False

            screen.blit(chasing_monkey_surf,chasing_monkey_rect)

        # text animation
        elif losing_screen_stages[current_losing_screen_stage] == "talking2":
            screen.blit(talking_menu_surf, talking_menu_surf.get_rect(bottomleft=(0, screen.get_height())))
            talking_print(["NOOOOOOO", "The monkey took your wanddd!!!"], ["Press Enter or Click Anywhere", "Press Enter or Click Anywhere"], 3)
            if complete_talking_done: current_losing_screen_stage += 1

        elif losing_screen_stages[current_losing_screen_stage] == "chasing2":
            # setting the required variables
            if not chasing2[chasing_stage]["done"]:
                chasing_angle = math.atan((chasing_monkey_rect.centery - chasing2[chasing_stage]["rect"][1]) / (chasing2[chasing_stage]["rect"][0] - chasing_monkey_rect.centerx))
                if chasing2[chasing_stage]["rect"][0] - chasing_monkey_rect.centerx < 0:
                    chasing_angle += math.pi
                chasing_num = 0
                chasing_monkey_animation = 0

                chasing_original_x = chasing_monkey_rect.centerx
                chasing_original_y = chasing_monkey_rect.centery
                chasing2[chasing_stage]["done"] = True

            # checking if the monkey reached his final destination or not
            if chasing_monkey_rect.center[0] // 5 != chasing2[chasing_stage]["rect"][0] // 5 or chasing_monkey_rect.center[1] // 5 != chasing2[chasing_stage]["rect"][1] // 5:
                if (chasing_monkey_animation * 10) % 10 == 0:
                    chasing_monkey_surf = pygame.transform.rotozoom(chasing_monkey_surf, 90, 1)
                    chasing_monkey_rect = chasing_monkey_surf.get_rect()
                chasing_monkey_animation += 0.25

                chasing_num += 5
                chasing_monkey_rect.center = (int(chasing_original_x + math.cos(chasing_angle) * chasing_num),int(chasing_original_y - math.sin(chasing_angle) * chasing_num))
            else:
                chasing_monkey_surf = pygame.image.load(chasing2[chasing_stage]["img"]).convert_alpha()
                if chasing_stage < len(chasing2) - 1:
                    chasing_stage += 1
                    chasing_monkey_surf = pygame.image.load(chasing2[chasing_stage]["img"]).convert_alpha()
                else: current_losing_screen_stage += 1

            screen.blit(chasing_monkey_surf,chasing_monkey_rect)

        elif losing_screen_stages[current_losing_screen_stage] == "animation":
            if not static_animations[current_static_animation]["done"]:
                screen.blit(pygame.image.load(f"{static_animations[current_static_animation]['img family']} {current_dust_animation}.png").convert_alpha(), pygame.image.load(f"{static_animations[current_static_animation]['img family']} {current_dust_animation}.png").get_rect(center = (static_animations[current_static_animation]["place"])))
                time.sleep(0.3)
                pygame.display.update()
                current_dust_animation += static_animations[current_static_animation]["step number"]
                if current_dust_animation == static_animations[current_static_animation]["ending number"]:
                    static_animations[current_static_animation]["done"] = True
                    if current_static_animation + 1 < len(static_animations):
                        current_static_animation += 1
                        current_dust_animation = static_animations[current_static_animation]["starting number"]
                    # else: current_losing_screen_stage += 1

    elif stage == "level changing":

        if level_changing_counter * level_changing_speed < screen.get_width():
            level_changing_counter += 1
        elif level_changing_counter * level_changing_speed >= screen.get_width():
            time.sleep(1)
            screen.fill("black")
            screen.blit(level_changing_font.render(f"level {Level_buttons.level}", True, "white"), level_changing_font.render(f"level {Level_buttons.level}", True, "white").get_rect(center = (screen.get_width() / 2, screen.get_height() / 2)))
            pygame.display.update()
            time.sleep(2.5)
            interval = None
            stage = stages[1]
            pygame.time.set_timer(monkeys_timer,750)
        pygame.draw.rect(screen,"black", (0,0,level_changing_counter * level_changing_speed,screen.get_height()))

    elif stage == "map":
        screen.blit(map_background1, (0,0))

        level_buttons_group.draw(screen)
        level_buttons_group.update()


    if changed_mouse and not stage == "lose" and not stage == "level changing": screen.blit(curser_img, curser_rect) # curser displaying

    pygame.display.update()
    clock.tick(60)