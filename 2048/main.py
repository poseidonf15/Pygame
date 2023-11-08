import pygame
from sys import exit
import random
import math

WIDTH = 500
HEIGHT = 500
BOARD_WIDTH = 400
BOARD_HEIGHT = 400
SIZE = BOARD_WIDTH / 4

class Numbers(pygame.sprite.Sprite):
    board = []

    def __init__(self,index,number):
        super().__init__()
        self.index = index
        self.number = number
        Numbers.board.append(self)

        self.image = small_font.render(str(self.number), True, "#14996d")
        self.rect = self.image.get_rect(center = ((WIDTH / 2 - BOARD_WIDTH / 2 + SIZE / 2) + self.index % 4 * SIZE, (HEIGHT / 2 - BOARD_HEIGHT / 2 + SIZE / 2) + self.index // 4 * SIZE))


    @staticmethod
    def player_input(pressed):
        board_changed = False

        if pressed == pygame.K_UP or pressed == pygame.K_w:
            for column in [0,1,2,3]:
                for Number in range (column,12,4): # summing opportunity
                    Number = Numbers.board[Number]

                    print(f"\ncurrent number: {Number.number} index: {Number.index}")

                    next_index = 4
                    while Number.index + next_index < column + 13:
                        print(f"current next_number: {Numbers.board[Number.index + next_index].number} next_index: {Number.index + next_index}")
                        if Number.number == 0: break # checks that we are not spending time on a zero (empty place)
                        else:
                            if Number.number == Numbers.board[Number.index + next_index].number: # checks for summing opportunity
                                Number.number *= 2
                                Numbers.board[Number.index + next_index].number = 0
                                board_changed = True
                                break
                            elif Numbers.board[Number.index + next_index].number > 0: break  # checks if there is a number in between
                        next_index += 4

                empty_places = [] # each row has its own empty places
                for Number in range (column,16,4): # moving up opportunity
                    Number = Numbers.board[Number]

                    if Number.number == 0: # checks if the Object is an empty place
                        empty_places.append(Number)
                    elif empty_places: # checks if there is an empty place above you
                        print(f"\nmoving {Number.index} to {empty_places[0].index}\n")
                        empty_places[0].number = Number.number
                        Number.number = 0
                        del empty_places[0]
                        empty_places.append(Number)
                        board_changed = True

                    empty_places = list(set(empty_places)) # deleting copies (just in case)
                    empty_places.sort(key=list_sorter) # sorting from the smallest to the biggest number so the upper empty place will be the first

        elif pressed == pygame.K_DOWN or pressed == pygame.K_s:
            for column in [12,13,14,15]:
                for Number in range(column, 3, -4):  # summing opportunity
                    Number = Numbers.board[Number]

                    print(f"\ncurrent number: {Number.number} index: {Number.index}")

                    next_index = -4
                    while Number.index + next_index > column - 13:
                        print(f"current next_number: {Numbers.board[Number.index + next_index].number} next_index: {Number.index + next_index}")
                        if Number.number == 0:
                            break  # checks that we are not spending time on a zero (empty place)
                        else:
                            if Number.number == Numbers.board[
                                Number.index + next_index].number:  # checks for summing opportunity
                                Number.number *= 2
                                Numbers.board[Number.index + next_index].number = 0
                                board_changed = True
                                break
                            elif Numbers.board[Number.index + next_index].number > 0:
                                break  # checks if there is a number in between
                        next_index -= 4

                empty_places = []  # each row has its own empty places
                for Number in range(column, -1, -4):  # moving up opportunity
                    Number = Numbers.board[Number]

                    if Number.number == 0:  # checks if the Object is an empty place
                        empty_places.append(Number)
                    elif empty_places:  # checks if there is an empty place above you
                        print(f"\nmoving {Number.index} to {empty_places[0].index}\n")
                        empty_places[0].number = Number.number
                        Number.number = 0
                        del empty_places[0]
                        empty_places.append(Number)
                        board_changed = True

                    empty_places = list(set(empty_places))  # deleting copies (just in case)
                    empty_places.sort(key=list_sorter, reverse=True)  # sorting from the biggest to the smallest (reverse) number so the bottom empty place will be the first

        elif pressed == pygame.K_LEFT or pressed == pygame.K_a:
            for row in [0,4,8,12]:
                for Number in range (row,row+3): # summing opportunity
                    Number = Numbers.board[Number]

                    print(f"\ncurrent number: {Number.number} index: {Number.index}")

                    next_index = 1
                    while Number.index + next_index < row + 4:
                        print(f"current next_number: {Numbers.board[Number.index + next_index].number} next_index: {Number.index + next_index}")
                        if Number.number == 0: break # checks that we are not spending time on a zero (empty place)
                        else:
                            if Number.number == Numbers.board[Number.index + next_index].number: # checks for summing opportunity
                                Number.number *= 2
                                Numbers.board[Number.index + next_index].number = 0
                                board_changed = True
                                break
                            elif Numbers.board[Number.index + next_index].number > 0: break  # checks if there is a number in between
                        next_index += 1

                empty_places = [] # each row has its own empty places
                for Number in range (row,row+4): # moving up opportunity
                    Number = Numbers.board[Number]

                    if Number.number == 0: # checks if the Object is an empty place
                        empty_places.append(Number)
                    elif empty_places: # checks if there is an empty place above you
                        print(f"\nmoving {Number.index} to {empty_places[0].index}\n")
                        empty_places[0].number = Number.number
                        Number.number = 0
                        del empty_places[0]
                        empty_places.append(Number)
                        board_changed = True

                    empty_places = list(set(empty_places)) # deleting copies (just in case)
                    empty_places.sort(key=list_sorter) # sorting from the smallest to the biggest number so the upper empty place will be the first

        elif pressed == pygame.K_RIGHT or pressed == pygame.K_d:
            for row in [3,7,11,15]:
                for Number in range(row, row-3, -1):  # summing opportunity
                    Number = Numbers.board[Number]

                    print(f"\ncurrent number: {Number.number} index: {Number.index}")

                    next_index = -1
                    while Number.index + next_index > row - 4:
                        print(f"current next_number: {Numbers.board[Number.index + next_index].number} next_index: {Number.index + next_index}")
                        if Number.number == 0:
                            break  # checks that we are not spending time on a zero (empty place)
                        else:
                            if Number.number == Numbers.board[
                                Number.index + next_index].number:  # checks for summing opportunity
                                Number.number *= 2
                                Numbers.board[Number.index + next_index].number = 0
                                board_changed = True
                                break
                            elif Numbers.board[Number.index + next_index].number > 0:
                                break  # checks if there is a number in between
                        next_index -= 1

                empty_places = []  # each row has its own empty places
                for Number in range(row, row-4, -1):  # moving up opportunity
                    Number = Numbers.board[Number]

                    if Number.number == 0:  # checks if the Object is an empty place
                        empty_places.append(Number)
                    elif empty_places:  # checks if there is an empty place above you
                        print(f"\nmoving {Number.index} to {empty_places[0].index}\n")
                        empty_places[0].number = Number.number
                        Number.number = 0
                        del empty_places[0]
                        empty_places.append(Number)
                        board_changed = True

                    empty_places = list(set(empty_places))  # deleting copies (just in case)
                    empty_places.sort(key=list_sorter, reverse=True)  # sorting from the biggest to the smallest (reverse) number so the bottom empty place will be the first

        if board_changed: # generates a new number only if the board has changed
            while True:
                rnd = random.randint(0, 15)
                if Numbers.board[rnd].number == 0:
                    Numbers.board[rnd].number = 2
                    print(f"\ngenerating number at {rnd}\n")
                    break
        else: print(f"\nNO CHANGES!\n")

    def update(self):
        if self.number > 0:
            pygame.draw.rect(screen,(20,100,math.log(self.number,2) * 20), ((WIDTH / 2 - BOARD_WIDTH / 2) + self.index % 4 * SIZE, (HEIGHT / 2 - BOARD_HEIGHT / 2) + self.index // 4 * SIZE, SIZE - 1, SIZE - 1))
            self.image = small_font.render(str(self.number), True, "black")
        else:
            self.image = small_font.render("", True, "#14996d")
        self.rect = self.image.get_rect(center=((WIDTH / 2 - BOARD_WIDTH / 2 + SIZE / 2) + self.index % 4 * SIZE,
                                                (HEIGHT / 2 - BOARD_HEIGHT / 2 + SIZE / 2) + self.index // 4 * SIZE))

def list_sorter(place):
    return place.index

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")
clock = pygame.time.Clock()

small_font = pygame.font.Font("fonts/Pixeltype.ttf",50)

stage = "intro"

numbers_group = pygame.sprite.Group()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            Numbers.player_input(event.key)

    screen.fill("#76758f")

    if stage == "intro":
        for num in range (16):
            numbers_group.add(Numbers(num,0))
        Numbers.board[random.randint(0,15)].number = 2
        Numbers.board[5].number = 4
        Numbers.board[9].number = 4
        Numbers.board[13].number = 8
        stage = "game"

    elif stage == "game":
        pygame.draw.rect(screen,"#3d3c57", (WIDTH/2 - BOARD_WIDTH/2, HEIGHT/2 - BOARD_HEIGHT/2, BOARD_WIDTH, BOARD_HEIGHT))
        for num in range (1, int(BOARD_WIDTH / SIZE)):
            pygame.draw.line(screen,"black",(WIDTH/2 - BOARD_WIDTH/2 + SIZE * num, HEIGHT/2 - BOARD_HEIGHT/2),(WIDTH/2 - BOARD_WIDTH/2 + SIZE * num, HEIGHT - (HEIGHT/2 - BOARD_HEIGHT/2)))
            pygame.draw.line(screen,"black",(WIDTH/2 - BOARD_WIDTH/2, HEIGHT/2 - BOARD_HEIGHT/2 + SIZE * num),(WIDTH - (WIDTH/2 - BOARD_WIDTH/2), HEIGHT/2 - BOARD_HEIGHT/2 + SIZE * num))

        numbers_group.update()
        numbers_group.draw(screen)

    elif stage == "lose":
        pass

    pygame.display.update()
    clock.tick(60)