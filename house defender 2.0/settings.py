HEIGHT = 0
WIDTH = 0
SPEED = 10

stage = "intro" # there are 5 stages [intro,game,lose,shop,map]
# stages for every stage for animation and stuff
intro_stage = 0
game_stage = 0
lose_stage = 0

balance = 0 # how much banana (game money) you have

levels = [ # the levels information
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

level = 1 # the number of the level (to get an index for the levels lise I do -1)

level_changing_counter = 0 # the level switching animation

mouse_rect = None

max_house_health = 10 # house's full health
house_health = 10     # house's current health
