import pygame
from sys import exit
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()

        self.image = pygame.Surface((10,10))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(center = (400,200))

        self.mouse_x = x
        self.mouse_y = y
        self.original_x = self.rect.centerx
        self.original_y = self.rect.centery
        self.angle = math.atan((self.original_y - self.mouse_y) / (self.mouse_x - self.original_x))
        if self.mouse_x - self.rect.centerx < 0:
            self.angle += math.pi
        self.num = 0

    def update(self):
        if self.rect.collidepoint((self.mouse_x,self.mouse_y)):
            self.kill()
            self.remove(bullet_group)
        self.num += speed
        self.rect.center = (int(self.original_x + math.cos(self.angle) * self.num),int(self.original_y - math.sin(self.angle) * self.num))

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Bullet_Psychic")
clock = pygame.time.Clock()
speed = 5

bullet_group = pygame.sprite.Group()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = event.pos
            shooting_sound = pygame.mixer.Sound("shooting sound.wav")
            shooting_sound.set_volume(0.05)
            shooting_sound.play()
            bullet_group.add(Bullet(x,y))

    screen.fill((30,30,30))

    bullet_group.draw(screen)
    bullet_group.update()

    pygame.display.update()
    clock.tick(60)

