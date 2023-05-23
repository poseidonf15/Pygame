import pygame
from sys import exit
import random
import pickle

class Player(pygame.sprite.Sprite):
    rect = None
    def __init__(self, player_xpos, player_ypos):
        super().__init__()
        # sprites
        packman1 = pygame.image.load("sprites/packman1.png").convert_alpha()
        packman2 = pygame.image.load("sprites/packman2.png").convert_alpha()
        packman3 = pygame.image.load("sprites/packman3.png").convert_alpha()
        packman4 = pygame.image.load("sprites/packman4.png").convert_alpha()
        packman5 = pygame.image.load("sprites/packman5.png").convert_alpha()
        packman6 = pygame.image.load("sprites/packman6.png").convert_alpha()
        packman7 = pygame.image.load("sprites/packman7.png").convert_alpha()
        self.packman = [packman1,packman2,packman3,packman4,packman5,packman6,packman7]

        death1 = pygame.image.load("sprites/packman death 1.png").convert_alpha()
        death2 = pygame.image.load("sprites/packman death 2.png").convert_alpha()
        death3 = pygame.image.load("sprites/packman death 3.png").convert_alpha()
        death4 = pygame.image.load("sprites/packman death 4.png").convert_alpha()

        self.death_animation_list = [death1, death2, death3, death4]
        self.death_animation_speed = 500

        self.speed = 2.5
        self.player_index = 2
        self.animation_loop = 0
        self.image = self.packman[int(self.player_index)]
        self.player_xpos = player_xpos
        self.player_ypos = player_ypos
        self.rect = self.image.get_rect(topleft = (self.player_xpos,self.player_ypos))
        self.future_rect = None
        self.moving = None

    def player_animation(self):
        if self.animation_loop % 2 == 0:
            self.player_index += 0.4
        else:
            self.player_index -= 0.4
        if self.player_index >= len(self.packman) - 1:self.animation_loop += 1
        elif self.player_index <= 1:self.animation_loop += 1
        self.image = self.packman[int(self.player_index)]
        self.rect = self.image.get_rect(topleft = (self.player_xpos,self.player_ypos))

    def player_input(self):
        keys = pygame.key.get_pressed()

        self.future_rect = self.image.get_rect(topleft=(self.player_xpos + self.speed, self.player_ypos))
        if (((keys[pygame.K_RIGHT] or keys[pygame.K_d]) and 0 < self.player_ypos < 575) or self.moving == "right") and not self.future_collide():
            self.moving = "right"
            self.player_xpos += self.speed

        self.future_rect = self.image.get_rect(topleft=(self.player_xpos - self.speed, self.player_ypos))
        if (((keys[pygame.K_LEFT] or keys[pygame.K_a]) and 0 < self.player_ypos < 575) or self.moving == "left") and not self.future_collide():
            self.moving = "left"
            self.player_xpos -= self.speed
            self.image = pygame.transform.flip(self.image,True,False)

        self.future_rect = self.image.get_rect(topleft = (self.player_xpos,self.player_ypos + self.speed))
        if (((keys[pygame.K_DOWN] or keys[pygame.K_s]) and 0 < self.player_xpos < 975) or self.moving == "down") and not self.future_collide():
            self.moving = "down"
            self.player_ypos += self.speed
            self.image = pygame.transform.rotozoom(self.image,-90,1)

        self.future_rect = self.image.get_rect(topleft=(self.player_xpos, self.player_ypos - self.speed))
        if (((keys[pygame.K_UP] or keys[pygame.K_w]) and 0 < self.player_xpos < 975) or self.moving == "up") and not self.future_collide():
            self.moving = "up"
            self.player_ypos -= self.speed
            self.image = pygame.transform.rotozoom(self.image,90,1)

        # Teleport when out of screen
        if self.rect.bottom <= 0 and self.moving == "up":
            self.player_ypos += 600

        if self.rect.top >= 575 and self.moving == "down":
            self.player_ypos -= 600

        if self.rect.right <= 0 and self.moving == "left":
            self.player_xpos += 1025

        if self.rect.left >= 975 and self.moving == "right":
            self.player_xpos -= 1025

    def future_collide(self):
        for collide in Wall.walls_rect:
            if self.future_rect.colliderect(collide): return True
        return False

    def death_animation(self):
        global death_animation
        global stage

        if self.death_animation_speed < current_time - death_animation_time < self.death_animation_speed * 2:
            self.image = self.death_animation_list[0]
            self.rect = self.image.get_rect(topleft = (self.player_xpos,self.player_ypos))
        elif self.death_animation_speed * 2 < current_time - death_animation_time < self.death_animation_speed * 3:
            self.image = self.death_animation_list[1]
            self.rect = self.image.get_rect(topleft = (self.player_xpos,self.player_ypos))
        elif self.death_animation_speed * 3 < current_time - death_animation_time < self.death_animation_speed * 4:
            self.image = self.death_animation_list[2]
            self.rect = self.image.get_rect(topleft = (self.player_xpos,self.player_ypos))
        elif self.death_animation_speed * 4 < current_time - death_animation_time < self.death_animation_speed * 5:
            self.image = self.death_animation_list[3]
            self.rect = self.image.get_rect(topleft = (self.player_xpos,self.player_ypos))

        elif self.death_animation_speed * 5 < current_time - death_animation_time < self.death_animation_speed * 6:
            death_animation = False
            stage = -1

    def update(self):
        if death_animation:
            self.death_animation()
        else:
            self.player_animation()
            self.player_input()
            Player.rect = self.rect

class Cookie(pygame.sprite.Sprite):
    cookies_rect = []
    cookies = 0
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("sprites/cookie.png").convert_alpha()
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft = (x,y))
        Cookie.cookies_rect.append(self.rect)
        Cookie.cookies += 1

    def update(self):
        if self.rect.colliderect(Player.rect):
            Cookie.cookies -= 1
            self.kill()

class Wall(pygame.sprite.Sprite):
    walls_rect = []
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("sprites/wall1.png").convert()
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft = (x,y))
        Wall.walls_rect.append(self.rect)

class Unicorn(pygame.sprite.Sprite):
    def __init__(self,xpos,ypos):
        super().__init__()
        self.unicorn_left = pygame.image.load("sprites/unicorn_left.png").convert_alpha()
        self.unicorn_right = pygame.image.load("sprites/unicorn_right.png").convert_alpha()
        self.unicorn_index = 0
        self.unicorn = [self.unicorn_left, self.unicorn_right]
        self.image = self.unicorn[self.unicorn_index]
        self.xpos = xpos
        self.ypos = ypos
        self.rect = self.image.get_rect(topleft = (self.xpos,self.ypos))
        self.future_rect = None
        self.speed = 1
        self.sides = None
        self.last_sides = None
        self.side = None
        self.last_side = None
        self.out = False

    def animation(self):
        self.image = self.unicorn[int(self.unicorn_index)]
        if self.side == "right":
            self.unicorn_index = 1
        if self.side == "left":
            self.unicorn_index = 0
        self.rect = self.image.get_rect(topleft = (self.xpos,self.ypos))

    def movement(self):
        self.last_sides = self.sides
        self.last_side = self.side

        if self.xpos % 25 == 0 and self.ypos % 25 == 0:
            self.removing_sides()
            self.side = random.choice(self.sides)
            if self.last_sides == self.sides:
                self.side = self.last_side

        if self.side == "up":
            self.ypos -= self.speed
        elif self.side == "down":
            self.ypos += self.speed
        elif self.side == "right":
            self.xpos += self.speed
        elif self.side == "left":
            self.xpos -= self.speed

        if self.rect.bottom <= 0:
            self.ypos += 598

        if self.rect.top >= 575:
            self.ypos -= 598

        if self.rect.right <= 0:
            self.xpos += 1023

        if self.rect.left >= 975:
            self.xpos -= 1023

    def removing_sides(self):
        self.sides = []
        sides = ["down", "up", "right", "left"]
        for self.side in sides:
            if not self.future_collide():
                self.sides.append(self.side)
        if (not self.out) and ("up" in self.sides):
            self.out = True
            self.sides = ["up"]

        # checking so the unicorn didn't go back
        if self.last_side == "up" and len(self.sides) > 1: self.sides.remove("down")

        elif self.last_side == "down" and len(self.sides) > 1: self.sides.remove("up")

        elif self.last_side == "right" and len(self.sides) > 1: self.sides.remove("left")

        elif self.last_side == "left" and len(self.sides) > 1: self.sides.remove("right")

    def future_collide(self):
        if self.side == "up": self.future_rect = self.image.get_rect(topleft = (self.xpos, self.ypos - self.speed))

        elif self.side == "down": self.future_rect = self.image.get_rect(topleft = (self.xpos, self.ypos + self.speed))

        elif self.side == "right": self.future_rect = self.image.get_rect(topleft = (self.xpos + self.speed, self.ypos))

        elif self.side == "left": self.future_rect = self.image.get_rect(topleft = (self.xpos - self.speed, self.ypos))

        for collide in Wall.walls_rect:
            if self.future_rect.colliderect(collide) or \
                    (self.side == "up" and not (0 < self.xpos < 975)) or \
                    (self.side == "down" and not (0 < self.xpos < 975)) or \
                    (self.side == "right" and not (0 < self.ypos < 575)) or \
                    (self.side == "left" and not (0 < self.ypos < 575)): return True
        return False

    def update(self):
        self.animation()
        self.movement()

def collisions():
    global stage
    if pygame.sprite.spritecollide(player.sprite,unicorn_group,False):
        return True

def check_win():
    if Cookie.cookies == 0:
        return True

SCREEN_WIDTH = 975
SCREEN_HEIGHT = 575
OBJECT_SIZE = 25

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Packman")
background = pygame.image.load("sprites/background.png").convert()
text_font = pygame.font.Font("fonts/Pixeltype.ttf",50)
clock = pygame.time.Clock()
stage = 0
levels = [[],[]]

# counting how many levels there is
with open("levels data.txt", "r") as f:
    num2 = int(f.readline())

# Map parts
wall_group = None
player = None
unicorn_group = None
cookie_group = None

# storing all the levels data into the levels variable
for num in range(1, num2 + 1):
    pickle_in = open(f"level{num} data", "rb")
    level = pickle.load(pickle_in)
    pickle_in.close()
    levels.insert(num,level)

death_animation = False

# Outro screen
outro_img = pygame.image.load("sprites/outro img.png").convert_alpha()
outro_img = pygame.transform.rotozoom(outro_img,0,2)
outro_img_rect = outro_img.get_rect(center = (SCREEN_WIDTH // 2 - 30, SCREEN_HEIGHT // 2 - 50))

retry_btn1 = pygame.image.load("sprites/retry_btn.png").convert()
retry_btn2 = pygame.image.load("sprites/retry_btn 2.png").convert()
retry_btn = retry_btn1
retry_btn_rect = retry_btn.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 200))

# Intro screen
intro_img = pygame.image.load("sprites/start menu logo.png").convert_alpha()
intro_img = pygame.transform.rotozoom(intro_img,0,3)
intro_img_rect = intro_img.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))

start_btn1 = pygame.image.load("sprites/start_btn.png").convert()
start_btn2 = pygame.image.load("sprites/start_btn 2.png").convert()
start_btn = start_btn1
start_btn_rect = start_btn1.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 200))

# Groups
def groups_creating():
    global wall_group
    global player
    global unicorn_group
    global cookie_group

    cookie_group = pygame.sprite.Group()
    unicorn_group = pygame.sprite.Group()
    player = pygame.sprite.GroupSingle()
    wall_group = pygame.sprite.Group()

    for y in range (int(575 / 25)):
        for x in range (int(975 / 25)):

            if int(levels[stage][y][x]) == 1:
                wall_group.add(Wall(x * OBJECT_SIZE,y * OBJECT_SIZE))               # walls

            elif int(levels[stage][y][x]) == 2:
                player.add(Player(x * 25, y * 25))                                  # player

            elif int(levels[stage][y][x]) == 3:
                cookie_group.add(Cookie(x * OBJECT_SIZE + 5,y * OBJECT_SIZE + 5))   # cookies

            elif int(levels[stage][y][x]) == 4:
                unicorn_group.add(Unicorn(x * OBJECT_SIZE, y * OBJECT_SIZE))        # unicorns

# Timer
current_time = 0
death_animation_time = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # main menu events
        if stage == 0:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn_rect.collidepoint(event.pos):
                    stage = 1
                    groups_creating()

            if event.type == pygame.MOUSEMOTION:
                if start_btn_rect.collidepoint(event.pos):
                    start_btn = start_btn2
                else:
                    start_btn = start_btn1

        # death menu events
        elif stage == -1:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_btn_rect.collidepoint(event.pos):
                    stage = 1
                    groups_creating()
            if event.type == pygame.MOUSEMOTION:
                if retry_btn_rect.collidepoint(event.pos):
                    retry_btn = retry_btn2
                else:
                    retry_btn = retry_btn1

    current_time = pygame.time.get_ticks()
    screen.blit(background,(0,0))

    if death_animation:
        player.update()
        wall_group.draw(screen)
        player.draw(screen)
        cookie_group.draw(screen)
        unicorn_group.draw(screen)

    else:
        if stage > 0:
                # Walls
                wall_group.draw(screen)

                # Player
                player.draw(screen)
                player.update()

                # Cookies
                cookie_group.draw(screen)
                cookie_group.update()

                # Unicorns
                unicorn_group.draw(screen)
                unicorn_group.update()

                if collisions():
                    death_animation = True
                    death_animation_time = pygame.time.get_ticks()

                if check_win():
                    stage += 1
                    if stage >= len(levels) - 1: stage = 0
                    else: groups_creating()

        elif stage == 0:    # Start screen
            screen.blit(start_btn,start_btn_rect)
            screen.blit(intro_img,intro_img_rect)

        elif stage == -1:   # End screen
            screen.blit(retry_btn,retry_btn_rect)
            screen.blit(outro_img,outro_img_rect)

    pygame.display.update()
    clock.tick(60)
