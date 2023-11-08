import pygame
from sys import exit
import settings
import random
import math
import time

class Monkeys(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.banana_surf = pygame.image.load("sprites/banana.png").convert_alpha()
        self.dangerous = True

        self.side = random.choice(["up", "down", "left", "right"])

        self.image = pygame.image.load("sprites/monkey.png").convert_alpha()
        self.rect = self.image.get_rect()

        if self.side == "up":
            self.rect.bottom = 0
            self.rect.left = random.randint(-51,settings.WIDTH)

        elif self.side == "down":
            self.rect.top = screen.get_height()
            self.rect.left = random.randint(-51,settings.WIDTH)

        elif self.side == "left":
            self.rect.bottom = random.randint(0,settings.HEIGHT + 50)
            self.rect.right = 0

        elif self.side == "right":
            self.rect.bottom = random.randint(0,settings.HEIGHT + 50)
            self.rect.left = screen.get_width()

        if (house_rect.centerx - self.rect.centerx) == 0: self.rect.centerx -=1

        self.angle = math.atan((self.rect.centery - house_rect.centery) / (house_rect.centerx - self.rect.centerx))
        if house_rect.centerx - self.rect.centerx < 0:
            self.angle += math.pi

        self.animation = 0

    def spinning_animation(self):
        if (self.animation * 10) % 10 == 0:
            self.image = pygame.transform.rotozoom(self.image,90,1)
            self.rect = self.image.get_rect(center = (self.rect.centerx,self.rect.centery))
        self.animation += 0.5

    def setting_angle(self):
        if (house_rect.centerx - self.rect.centerx) == 0: self.rect.centerx -=1

        self.angle = math.atan((self.rect.centery - house_rect.centery) / (house_rect.centerx - self.rect.centerx))
        if house_rect.centerx - self.rect.centerx < 0:
            self.angle += math.pi

    @staticmethod
    def reset():
        settings.house_health = settings.max_house_health
        pygame.time.set_timer(monkeys_timer,750)
        Monkeys.counter = 0
        Monkeys.created_counter = 0

    def update(self):
        self.setting_angle()

        if settings.mouse_rect and self.rect.colliderect(settings.mouse_rect) and self.dangerous:
            self.image = self.banana_surf
            self.dangerous = False

        if self.rect.colliderect(house_rect):
            Monkeys.counter += 1
            self.kill()
            self.remove(monkeys_group)
            if self.dangerous: settings.house_health -= 1
            else:
                coins_group.add(Coins_text())
                settings.balance += 1

        self.spinning_animation()

        self.rect.center = (self.rect.centerx + math.cos(self.angle) * settings.SPEED,self.rect.centery - math.sin(self.angle) * settings.SPEED)

class Coins_text(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.distance = 10
        self.image = font_25pxl.render(f"+ one banana",False,(111,196,169))
        self.rect = self.image.get_rect(center = (screen.get_width() / 2, screen.get_height() / 2 - house_surf.get_height() / 2 - 25))

    def update(self):
        self.rect = self.image.get_rect(center = (screen.get_width() / 2, screen.get_height() / 2 - house_surf.get_height() / 2 - 25 - self.distance))
        self.distance += 5
        if self.distance == 75:
            self.kill()
            self.remove(coins_group)

def score_message():
    score_text = font_50pxl.render(f"You have {settings.balance}",False,"#eb7310")
    mini_banana_surf = pygame.image.load("sprites/mini banana.png").convert_alpha()
    score_text_rect = score_text.get_rect(midtop = (screen.get_width() / 2, 20))
    mini_banana_rect = mini_banana_surf.get_rect(midleft = score_text_rect.midright)
    mini_banana_rect.left -= 5
    mini_banana_rect.bottom -= 5
    score_text_rect.left -= (mini_banana_rect.right - mini_banana_rect.left) / 2
    screen.blit(score_text, score_text_rect)
    screen.blit(mini_banana_surf, mini_banana_rect)

def health_bar_draw():
    pygame.draw.rect(screen, "red", (house_rect.centerx - house_surf.get_width() / 2,
                                     house_rect.centery - house_surf.get_height() / 2 - 15,
                                     settings.house_health * 100 / settings.max_house_health, 10))
    health_status = font_25pxl.render(str(settings.house_health),False,"black")
    health_status_rect = health_status.get_rect(center = (house_rect.centerx,
                                                house_rect.centery - house_surf.get_height() / 2 - 25))
    screen.blit(health_status, health_status_rect)

class Talking_print:
    complete_skip = True
    to_skip = False
    now_talking = None
    def __init__(self, texts, instructions):
        Talking_print.complete_skip = False
        Talking_print.to_skip = False
        Talking_print.now_talking = self
        self.texts = texts
        self.instructions = instructions
        self.speed = 3
        self.counter = 0
        self.active_displaying_text = 0
        self.skip_to_next = False

    def skip(self):
        if self.skip_to_next and self.active_displaying_text < len(self.texts) - 1:  # going to the next text
            self.active_displaying_text += 1
            self.skip_to_next = False
            self.counter = 0
        elif not self.skip_to_next:  # skipping the text
            self.skip_to_next = True
            self.counter = self.speed * len(self.texts[self.active_displaying_text])
        elif (not self.active_displaying_text < len(self.texts) - 1) and self.skip_to_next:
            Talking_print.complete_skip = True


    def update(self):
        if Talking_print.to_skip:
            Talking_print.to_skip = False
            self.skip()
        Talking_print.displaying_text_index = self.active_displaying_text
        if self.counter < self.speed * len(self.texts[self.active_displaying_text]):
            self.counter += 1
        elif self.counter >= self.speed * len(self.texts[self.active_displaying_text]):
            what_to_do_text = font_50pxl.render(self.instructions[self.active_displaying_text], True, "black")
            screen.blit(what_to_do_text, what_to_do_text.get_rect(bottomright=(1486, settings.HEIGHT - 25)))
            self.skip_to_next = True

        screen.blit(font_50pxl.render(self.texts[self.active_displaying_text][0:self.counter // self.speed], True, "yellow"), (10, settings.HEIGHT - 150))

def level_changing(change_to, level_changing_speed):
    if settings.level_changing_counter * level_changing_speed < settings.WIDTH:
        settings.level_changing_counter += 1
    elif settings.level_changing_counter * level_changing_speed >= settings.WIDTH:
        time.sleep(1)
        screen.fill("black")
        screen.blit(font_100pxl.render(change_to, True, "white"),
                    font_100pxl.render(change_to, True, "white").get_rect(
                        center=(settings.WIDTH / 2, settings.HEIGHT / 2)))
        pygame.display.update()
        time.sleep(2.5)
        settings.level_changing_counter = 0
        # checks if you need to change to a certain level or to something else
        if "Level" in change_to:
            settings.stage = "game"
            Monkeys.reset()
        else:
            pygame.time.set_timer(monkeys_timer,0)
            settings.stage = change_to
    pygame.draw.rect(screen, "black", (0, 0, settings.level_changing_counter * level_changing_speed, settings.HEIGHT))

pygame.init()

screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
settings.WIDTH = screen.get_width()
settings.HEIGHT = screen.get_height()
pygame.display.set_caption("House defender")
clock = pygame.time.Clock()

# fonts
font_25pxl = pygame.font.Font("fonts/Pixeltype.ttf",25)
font_50pxl = pygame.font.Font("fonts/Pixeltype.ttf",50)
font_100pxl = pygame.font.Font("fonts/Pixeltype.ttf",100)

# other displayable things
talking_menu = pygame.image.load("sprites/talking menu.png").convert_alpha()

magic_banana_wand = pygame.image.load("sprites/magic banana wand.png").convert_alpha()
banana_curser = pygame.image.load("sprites/banana curser.png").convert_alpha()

house_surf = pygame.image.load("sprites/house.png").convert_alpha()
house_surf = pygame.transform.rotozoom(house_surf,0,2)
house_rect = house_surf.get_rect(center = (settings.WIDTH / 2, settings.HEIGHT / 2))

# Groups
monkeys_group = pygame.sprite.Group()
coins_group = pygame.sprite.Group()

# Timers
monkeys_timer = pygame.USEREVENT + 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # talk events
        if not Talking_print.complete_skip:
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_KP_ENTER):
                Talking_print.to_skip = True

        if event.type == pygame.MOUSEBUTTONDOWN:  # checks for mouse click
            settings.mouse_rect = [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 26, 26]
        elif not settings.mouse_rect:
            settings.mouse_rect = None  # If you didn't click but the curser rect still has value, it will set it to None

        if settings.stage == "intro" and settings.intro_stage == 2:
            if Talking_print.now_talking.active_displaying_text >= 3:                                       # checks if it's the time for the wand to glow and being able to be clicked
                if magic_banana_wand.get_rect(center = (settings.WIDTH / 2, settings.HEIGHT / 2 - 100)).collidepoint(pygame.mouse.get_pos()):
                    magic_banana_wand = pygame.image.load("sprites/glowing magic banana wand.png").convert_alpha()
                else:
                    magic_banana_wand = pygame.image.load("sprites/magic banana wand.png").convert_alpha()
                if event.type == pygame.MOUSEBUTTONDOWN and magic_banana_wand.get_rect(center = (settings.WIDTH / 2, settings.HEIGHT / 2 - 100)).collidepoint(event.pos): # checks if the wand is clicked
                    pygame.mouse.set_visible(False)
                    settings.intro_stage += 1

        elif settings.stage == "game":
            if event.type == monkeys_timer:
                monkeys_group.add(Monkeys())

        elif settings.stage == "lose":
            pass

        elif settings.stage == "map":
            pass

        elif settings.stage == "shop":
            pass

    # setting when I don't need the background
    if not (settings.stage == "intro" and settings.intro_stage == 3):
        screen.blit(pygame.image.load("sprites/background.jpg").convert(), (0,0))

    if settings.stage == "intro":
        if settings.intro_stage == 0:
            for i in range (0, settings.WIDTH + 1, 3):
                screen.blit(talking_menu, talking_menu.get_rect(bottomright = (i, settings.HEIGHT)))
                time.sleep(0.001)
                pygame.display.update()
            settings.intro_stage += 1

        elif settings.intro_stage == 1:
            screen.blit(talking_menu, talking_menu.get_rect(bottomleft=(0, settings.HEIGHT)))
            Talking_print(["Hello mighty stranger!", "Our house is getting attacked by some lunatic space monkeys.", "Your mission is to turn these monkeys into bananas by this magic wand.", "Good luck! :)"],
                          ["Press Enter or Click Anywhere", "Press Enter or Click Anywhere", "Press Enter or Click Anywhere", "Click the wand"])
            settings.intro_stage += 1
            level_changing_reset = True

        elif settings.intro_stage == 2:
            screen.blit(talking_menu, talking_menu.get_rect(bottomleft=(0, settings.HEIGHT)))
            Talking_print.update(Talking_print.now_talking)

            if Talking_print.now_talking.active_displaying_text >= 2: # checks if it's the time to show the wand
                screen.blit(magic_banana_wand, magic_banana_wand.get_rect(center = (settings.WIDTH / 2, settings.HEIGHT / 2 - 100)))

        elif settings.intro_stage == 3:
                level_changing("Level 1", 25)

    elif settings.stage == "game":

        screen.blit(house_surf, house_rect)

        # Monkeys
        monkeys_group.draw(screen)
        monkeys_group.update()

        health_bar_draw()

        # Coins
        coins_group.draw(screen)
        coins_group.update()

        score_message()

    elif settings.stage == "lose":
        pass

    elif settings.stage == "map":
        pass

    elif settings.stage == "shop":
        pass

    # settings when I don't need the banana curser
    if not (settings.stage == "intro" or settings.level_changing_counter > 0):
        screen.blit(banana_curser,pygame.mouse.get_pos())

    pygame.display.update()
    clock.tick(60)
