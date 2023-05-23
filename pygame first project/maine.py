import pygame
from sys import exit
from random import randint, choice
from pygame import mixer

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Walking sprites
        Player_walk1 = pygame.image.load("sprites/Player_walk1.png").convert_alpha()
        Player_walk2 = pygame.image.load("sprites/Player_walk2.png").convert_alpha()
        player_crouch1 = pygame.image.load("sprites/Player_head1.png").convert_alpha()
        player_crouch2 = pygame.image.load("sprites/Player_head2.png").convert_alpha()
        self.player_walk = [Player_walk1,Player_walk2]

        # Crouching sprites
        self.player_crouch = [player_crouch1,player_crouch2]
        self.is_crouching = False

        # Jumping sprites
        self.player_jump = pygame.image.load("sprites/Player_jump.png").convert_alpha()

        self.player_index = 0

        self.player_xpos = 80
        self.player_ypos = 300
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (self.player_xpos, self.player_ypos))
        self.gravity = 0

        self.jump_Sound = mixer.Sound("sounds/cartoon-jump.wav")

    def player_input(self):
        keys = pygame.key.get_pressed()
        if audio: self.jump_Sound.set_volume(0.3)
        else: self.jump_Sound.set_volume(0)

        if keys[pygame.K_RIGHT] or keys[pygame.K_d] and self.rect.right < 800:
            self.player_xpos += 5

        if keys[pygame.K_LEFT] or keys[pygame.K_a] and self.rect.left > 5:
            self.player_xpos -= 5

        if keys[pygame.K_DOWN] or keys[pygame.K_s] and self.rect.bottom >= 300:
            self.is_crouching = True

        elif (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.bottom >= 300:
            self.gravity = -17
            self.jump_Sound.play()
        else:
            self.is_crouching = False

    def apply_gravity(self):
        self.gravity += 1
        self.player_ypos += self.gravity
        if self.player_ypos >= 300:
            self.player_ypos = 300

    def animation_state(self):
        if self.is_crouching:
            self.player_index += 0.1
            if self.player_index >= len(self.player_crouch):self.player_index = 0
            self.image = self.player_crouch[int(self.player_index)]
        else:
            if self.rect.bottom < 300:
                self.image = self.player_jump
            else:
                self.player_index += 0.1
                if self.player_index >= len(self.player_walk):self.player_index = 0
                self.image = self.player_walk[int(self.player_index)]
        self.rect = self.image.get_rect(midbottom=(self.player_xpos, self.player_ypos))

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        if pygame.time.get_ticks() - start_time <= 1:
            self.reset()

    def reset(self):
        self.player_xpos = 80
        self.player_ypos = 300


class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        self.repeat_animation = 0
        self.type = type

        if self.type == "enemy":
            enemy_1 = pygame.image.load("sprites/Enemy_walk1.png").convert_alpha()
            enemy_2 = pygame.image.load("sprites/Enemy_walk2.png").convert_alpha()
            self.frames = [enemy_1, enemy_2]
            y_pos = 300
        else:
            fly_enemy_1 = pygame.image.load("sprites/Fly_enemy_frame1.png").convert_alpha()
            fly_enemy_2 = pygame.image.load("sprites/Fly_Enemy_frame2.png").convert_alpha()
            fly_enemy_3 = pygame.image.load("sprites/Fly_enemy_frame3.png").convert_alpha()
            fly_enemy_4 = pygame.image.load("sprites/Fly_Enemy_frame4.png").convert_alpha()
            self.frames = [fly_enemy_1, fly_enemy_2, fly_enemy_3, fly_enemy_4]
            if self.type == "flying_enemy":
                y_pos = 300 - 63
            else:
                y_pos = 300 - 51

        self.animation_index = 0

        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def animation_state(self):
        if self.type == "flying_enemy":
            if self.repeat_animation % 2 == 0: self.animation_index += 1/3
            else: self.animation_index -= 1/3

            if self.animation_index >= len(self.frames):
                self.repeat_animation += 1
                self.animation_index -= 1/3
            elif self.animation_index <= 0: self.repeat_animation += 1
            self.image = self.frames[int(self.animation_index)]

        else:
            self.animation_index += 0.1
            if self.animation_index >= len(self.frames): self.animation_index = 0
            self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100: self.kill()

def display_score():
    global best_score
    current_time = round((pygame.time.get_ticks() - start_time) / 1000)
    score_surf = text_font.render(f"Your score is: {current_time}",False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    if current_time > best_score:
        file = open("score_data.txt","w")
        file.write(str(current_time))
        best_score = current_time
        file.close()
    best_score_message = text_font.render(f"Your best score is: {best_score}",False,(64,64,64))
    best_score_message_rect = best_score_message.get_rect(center = (400,100))
    screen.blit(score_surf,score_rect)
    screen.blit(best_score_message,best_score_message_rect)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        game_over_Sound = mixer.Sound("sounds/negative_beeps (game over).wav")
        if audio: game_over_Sound.set_volume(0.5)
        else: game_over_Sound.set_volume(0)
        game_over_Sound.play()
        return False
    else: return True

def background_animation():
    global background_rect, background_2_rect
    if background_rect.right <= 0: background_rect.left = 800
    if background_2_rect.right <= 0: background_2_rect.left = 800
    background_rect.left -= 1
    background_2_rect.left -= 1

pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0
file = open("score_data.txt","r")
best_score = int(file.read())
print (best_score)
file.close()
text_font = pygame.font.Font("fonts/Pixeltype.ttf",50)
mixer.music.load("sounds/music.wav")
mixer.music.set_volume(0.05)
mixer.music.play(-1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# Audio button
audio_on_btn_surf = pygame.image.load("sprites/Audio_on.png").convert_alpha()
audio_on_btn_rect = audio_on_btn_surf.get_rect(topleft = (720, 0))
audio_off_btn_surf = pygame.image.load("sprites/Audio_off.png").convert_alpha()
audio_off_btn_rect = audio_off_btn_surf.get_rect(topleft = (720, 0))
audio_status = [audio_on_btn_surf,audio_off_btn_surf,audio_on_btn_rect,audio_off_btn_rect]
audio = True

# Background
background_surf = pygame.image.load("sprites/Background.png").convert()
background_rect = background_surf.get_rect(topleft = (0,0))
background_2_surf = pygame.image.load("sprites/Background_2.png").convert()
background_2_rect = background_2_surf.get_rect(topleft = (800,0))
ground_surf = pygame.image.load("sprites/Ground.png").convert()

obstacle_rect_list = []

# Player sprites
player_walk1 = pygame.image.load("sprites/Player_walk1.png").convert_alpha()
player_walk2 = pygame.image.load("sprites/Player_walk2.png").convert_alpha()
player_walk = [player_walk1,player_walk2]
player_index = 0
player_jump = pygame.image.load("sprites/Player_jump.png").convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0

# Intro screen
player_stand = pygame.image.load("sprites/Player_regular.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = text_font.render("Pixel Runner", False, (111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = text_font.render("Press space to run", False, (111, 196, 169))
game_message_rect = game_message.get_rect(center = (400,320))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

background_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(background_animation_timer,2)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if not game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if audio_on_btn_rect.collidepoint(event.pos):
                    if audio:
                        audio = False
                        mixer.music.set_volume(0)
                    else:
                        audio = True
                        mixer.music.set_volume(0.05)

            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w):
                game_active = True
                start_time = pygame.time.get_ticks()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["flying_enemy","enemy","enemy","enemy","low_flying_enemy"])))

            if event.type == background_animation_timer:
                background_animation()

    if game_active:
        screen.blit(background_surf,background_rect)
        screen.blit(background_2_surf,background_2_rect)
        screen.blit(ground_surf,(0,300))
        score = display_score()

        # Player
        player.draw(screen)
        player.update()

        # Obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Collision
        game_active = collision_sprite()

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear()
        player_gravity = 0

        score_message = text_font.render(f"Your score: {score}",False,(111,196,169))
        score_message_rect = score_message.get_rect(center = (400,300))
        best_score_message = text_font.render(f"Your best score: {best_score}",False,(111, 196, 169))
        best_score_message_rect = best_score_message.get_rect(center=(400, 360))
        screen.blit(game_name,game_name_rect)
        screen.blit(best_score_message,best_score_message_rect)

        if audio: screen.blit(audio_status[0],audio_status[2])
        else: screen.blit(audio_status[1],audio_status[3])

        if score == 0:
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)

    pygame.display.update()
    clock.tick(60)