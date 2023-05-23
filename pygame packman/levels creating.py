import pygame
from sys import exit
import pickle

class Button(pygame.sprite.Sprite):
    selected = None
    selected_type = None
    def __init__(self, type, image, rect):
        super().__init__()
        self.type = type
        self.image = image
        self.rect = rect

    def update(self):
        if mouse_pos and self.rect.collidepoint(mouse_pos):
            Button.selected = self.rect
            Button.selected_type = self.type

class Cells(pygame.sprite.Sprite):
    def __init__(self,line,item,y_index,x_index,number):
        super().__init__()
        self.y = line
        self.x = item
        self.y_index = y_index
        self.x_index = x_index
        self.number = number

        image0 = pygame.image.load("sprites/air.png").convert_alpha()
        image1 = pygame.image.load("sprites/wall1.png").convert()
        image2 = pygame.image.load("sprites/packman2.png").convert_alpha()
        image3 = pygame.image.load("sprites/cookie.png").convert_alpha()
        image4 = pygame.image.load("sprites/unicorn_left.png").convert_alpha()
        self.images = [image0, image1, image2, image3, image4]
        self.image = self.images[self.number]
        self.rect = self.image.get_rect(center = (self.x + OBJECT_SIZE / 2, self.y + OBJECT_SIZE / 2))
        level[self.y_index].append(self.number)

    def click(self):
        self.image = self.images[self.number]
        self.rect = self.image.get_rect(center = (self.x + OBJECT_SIZE / 2, self.y + OBJECT_SIZE / 2))
        level[self.y_index][self.x_index] = self.number

    def update(self):
        if pygame.mouse.get_pressed(3)[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.number = Button.selected_type
            self.click()

            if fill and self.number == 0: self.number = 3



SCREEN_WIDTH = 975
SCREEN_HEIGHT = 675
OBJECT_SIZE = 25

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Levels Creating")
background = pygame.image.load("sprites/background.png").convert()
menu_background = pygame.image.load("sprites/menu background.png").convert()
clock = pygame.time.Clock()
text_font = pygame.font.Font("fonts/Pixeltype.ttf",50)
level_text = None
level_text_rect = None
pressed = []
level = []
mouse_pos = None
fill = False

with open("levels data.txt", "r") as f:
    level_number = int(f.readline())

# Buttons
save_btn = pygame.image.load("sprites/save_btn.png").convert()
save_btn_rect = save_btn.get_rect(topright = (975 / 2 - 50, 575 + 20))

open_btn = pygame.image.load("sprites/open_btn.png").convert()
open_btn_rect = open_btn.get_rect(topleft = (975 / 2 + 50, 575 + 20))

clear_btn = pygame.image.load("sprites/clear.png").convert()
clear_btn_rect = clear_btn.get_rect(center = (975 / 2, 575 + 51))

fill_btn = pygame.image.load("sprites/fill.png").convert()
fill_btn_rect = clear_btn.get_rect(center = (975 / 2 - 250, 575 + 51))

buttons_group = pygame.sprite.Group()

slots = pygame.image.load("sprites/slots .png").convert()

slots_buttons_xpos = 755
slots_buttons_difference = 25 + 5

trash_btn = pygame.image.load("sprites/trash can.png").convert_alpha()
trash_btn_rect = trash_btn.get_rect(topleft = (slots_buttons_xpos, 615))
buttons_group.add(Button(0, trash_btn, trash_btn_rect))

wall_btn = pygame.image.load("sprites/wall button.png").convert_alpha()
wall_btn_rect = wall_btn.get_rect(topleft = (slots_buttons_xpos + slots_buttons_difference, 615))
buttons_group.add(Button(1, wall_btn, wall_btn_rect))
Button.selected = wall_btn_rect
Button.selected_type = 1

packman_btn = pygame.image.load("sprites/packman button.png").convert_alpha()
packman_btn_rect = packman_btn.get_rect(topleft = (slots_buttons_xpos + slots_buttons_difference * 2, 615))
buttons_group.add(Button(2, packman_btn, packman_btn_rect))

cookie_btn = pygame.image.load("sprites/cookie button.png").convert_alpha()
cookie_btn_rect = cookie_btn.get_rect(topleft = (slots_buttons_xpos + slots_buttons_difference * 3, 615))
buttons_group.add(Button(3, cookie_btn, cookie_btn_rect))

unicorn_btn = pygame.image.load("sprites/unicorn_left button.png").convert_alpha()
unicorn_btn_rect = unicorn_btn.get_rect(topleft = (slots_buttons_xpos + slots_buttons_difference * 4, 615))
buttons_group.add(Button(4, unicorn_btn, unicorn_btn_rect))

# Level Text
def level_text_update():
    global level_text
    global level_text_rect
    level_text = text_font.render(f"Level: {level_number}", False, "black")
    level_text_rect = level_text.get_rect(topleft=(50, 610))

cells_group = pygame.sprite.Group()

def create_cells():
    global level

    cells_group.empty()
    level = []
    for line in range (int(575 / 25)):
        level.append([])
        for item in range (int(975 / 25)):
            cells_group.add(Cells(line * 25, item * 25, line, item, 0))

create_cells()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # buttons interaction
        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = event.pos
            buttons_group.update()

            # save button
            if save_btn_rect.collidepoint(event.pos):
                pickle_out = open(f"level{level_number} data", "wb")
                pickle.dump(level, pickle_out)
                pickle_out.close()

                with open("levels data.txt", "r+") as f:
                    maximum = int(f.readline())
                    f.seek(0)
                    if maximum < level_number: f.writelines(str(level_number))

                level_number += 1

            # open button
            elif open_btn_rect.collidepoint(event.pos):
                pickle_in = open(f"level{level_number} data", "rb")
                level = pickle.load(pickle_in)

                cells_group.empty()
                for y in range(int(575 / 25)):
                    for x in range(int(975 / 25)):
                        cells_group.add(Cells(y * 25, x * 25, y, x, int(level[y][x])))

            # clear button
            elif clear_btn_rect.collidepoint(event.pos): create_cells()

            elif fill_btn_rect.collidepoint(event.pos):
                for y in range(int(575 / 25)):
                    for x in range(int(975 / 25)):
                        if level[y][x] == 0: level[y][x] = 3
                cells_group.empty()
                for y in range(int(575 / 25)):
                    for x in range(int(975 / 25)):
                        cells_group.add(Cells(y * 25, x * 25, y, x, int(level[y][x])))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                level_number += 1

            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                level_number -= 1

    cells_group.update()
    screen.blit(background, (0,0))
    screen.blit(menu_background, (0,575))
    screen.blit(save_btn, save_btn_rect)
    screen.blit(open_btn, open_btn_rect)
    screen.blit(clear_btn, clear_btn_rect)
    screen.blit(fill_btn, fill_btn_rect)
    screen.blit(slots, (slots_buttons_xpos - 5, 610))
    level_text_update()
    screen.blit(level_text, level_text_rect)

    buttons_group.draw(screen)
    cells_group.draw(screen)

    if Button.selected:
        pygame.draw.rect(screen,"red",Button.selected,3)

    pygame.display.update()
    clock.tick(60)