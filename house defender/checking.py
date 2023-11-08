import pygame
from sys import exit
import random
import math
import time

pygame.init()

# main<>

# variables (main)
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
pygame.display.set_caption("House defender")
clock = pygame.time.Clock()

# Backgrounds (main)
game_background_surf = pygame.image.load("sprites/background.jpg").convert()

# Buttons (main)
shop_btn_surf = pygame.image.load("sprites/shop button.png").convert_alpha()
shop_btn_rect = shop_btn_surf.get_rect(center = (screen.get_width() / 2, screen.get_height() / 2 - 85 - 10))

map_btn_surf = pygame.image.load("sprites/map button.png").convert_alpha()
map_btn_rect = map_btn_surf.get_rect(center = (screen.get_width() / 2, screen.get_height() / 2 - 10))

pause_btn_surf = pygame.image.load("sprites/pause button.png").convert_alpha()
pause_btn_rect = pause_btn_surf.get_rect(topleft = (25, 10))

play_btn_surf = pygame.image.load("sprites/play button.png").convert_alpha()
play_btn_rect = play_btn_surf.get_rect(center = (screen.get_width() / 2, screen.get_height() / 2 + 100))

pause_menu_surf = pygame.image.load("sprites/pause menu.png").convert()
pause_menu_rect = pause_menu_surf.get_rect(center = (screen.get_width() / 2, screen.get_height() / 2))

# Timers (game stuff)
monkeys_timer = pygame.USEREVENT + 1
chasing_timer = pygame.USEREVENT + 2

# Groups (game stuff)
monkeys_group = pygame.sprite.Group()
coins_group = pygame.sprite.Group()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(game_background_surf, (0, 0))
    screen.blit(pause_btn_surf, pause_btn_rect)
    screen.blit(pause_menu_surf, pause_menu_rect)
    screen.blit(shop_btn_surf, shop_btn_rect)
    screen.blit(map_btn_surf, map_btn_rect)
    screen.blit(play_btn_surf, play_btn_rect)

    pygame.display.update()
    clock.tick(60)