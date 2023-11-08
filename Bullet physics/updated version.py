import pygame
from sys import exit
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((10,10))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(center = (400,200))

        if (pygame.mouse.get_pos()[0] - self.rect.centerx) == 0: self.rect.centerx -=1

        self.angle = math.atan((self.rect.centery - pygame.mouse.get_pos()[1]) / (pygame.mouse.get_pos()[0] - self.rect.centerx))
        if pygame.mouse.get_pos()[0] - self.rect.centerx < 0:
            self.angle += math.pi

    def update(self):
        if (pygame.mouse.get_pos()[0] - self.rect.centerx) == 0: self.rect.centerx -=1

        self.angle = math.atan((self.rect.centery - pygame.mouse.get_pos()[1]) / (pygame.mouse.get_pos()[0] - self.rect.centerx))
        if pygame.mouse.get_pos()[0] - self.rect.centerx < 0:
            self.angle += math.pi

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.kill()
            self.remove(bullet_group)

        self.rect.center = (self.rect.centerx + math.cos(self.angle) * speed,self.rect.centery - math.sin(self.angle) * speed)

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Bullet_Psychic")
clock = pygame.time.Clock()
speed = 3

bullet_group = pygame.sprite.Group()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            shooting_sound = pygame.mixer.Sound("shooting sound.wav")
            shooting_sound.set_volume(0.05)
            shooting_sound.play()
            bullet_group.add(Bullet())

    screen.fill((30,30,30))

    bullet_group.draw(screen)
    bullet_group.update()

    pygame.display.update()
    clock.tick(60)