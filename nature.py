import pygame
from pygame import locals
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import seaborn as sns
from Animal_factory_class import *
from Animal_class import *

FPS = 60
GEN_LEN = 180


def main():
    # start game
    pygame.init()

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("nature")

    # list of all animals
    animals_list = []
    # generation
    gen = 0
    gen_help = GEN_LEN - 1

    # Loop until the user clicks the close button.
    done = False
    s_event = ""
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Calibri', 25, True, False)

    while not done:
        # Event Processing
        for event in pygame.event.get():
            done, s_event = handle_event(animals_list, event)

        types_count = count_animal_types(animals_list)

        # count generations- each generation length
        blink_screen = False
        gen_help += 1
        if gen_help == GEN_LEN:
            gen += 1
            gen_help = 0
            blink_screen = True
        # Set the screen background
        if blink_screen:
            screen.fill((0, 0, 20))
        else:
            screen.fill(BLACK)

        # default behaviour- add 10 bushes every generation
        if blink_screen:
            for i in range(10):
                animals_list.append(Bush())

        # write number of instances of each animal
        draw_all_animals(animals_list, screen, s_event)
        text = font.render(str(types_count), True, WHITE)
        screen.blit(text, [250, 50])

        # print generation
        text = font.render('Generation: ' + str(gen), True, WHITE)
        screen.blit(text, [800, 50])

        # # draw middle
        # pygame.draw.line(screen, GREEN, [0, SCREEN_HEIGHT / 2], [SCREEN_WIDTH, SCREEN_HEIGHT / 2], 1)
        # pygame.draw.line(screen, GREEN, [SCREEN_WIDTH / 2, 0], [SCREEN_WIDTH / 2, SCREEN_HEIGHT], 1)

        # frames per seconds
        clock.tick(FPS)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Close everything down
    pygame.quit()


def count_animal_types(animals_list):
    # count types of animals
    types_count = dict()
    for animal in animals_list:
        # only class name
        key = animal.get_type()
        if key in types_count:
            types_count[key] += 1
        else:
            types_count[key] = 1
    return types_count


def handle_event(animals_list, event):
    done = False
    s_event = ""
    if event.type == pygame.QUIT:
        done = True
    # if a key was pressed
    if event.type == pygame.MOUSEBUTTONDOWN:
        s_event = "MOUSE_BUTTON_DOWN"
    if event.type == pygame.KEYDOWN:
        # space summons a rabbit
        if event.key == pygame.K_SPACE:
            animals_list.append(Animal_factory.get_new_Rabbit())
        elif event.key == pygame.K_UP:
            animals_list.append(Animal_factory.get_new_Wolf())
        # tab summons 10 bushes
        elif event.key == pygame.K_TAB:
            for i in range(10):
                animals_list.append(Animal_factory.get_new_Bush())
    return done, s_event


def update_graph(animals_types):
    # data
    df = pd.DataFrame({'x': range(1, 10), 'y': np.random.randn(9) * 80 + range(1, 10)})
    # plot
    draw_graph(df)


def draw_graph(df):
    plt.plot('x', 'y', data=df, linestyle='-', marker='o')
    plt.show()


def draw_all_animals(animals_list, screen, s_event=""):
    """iterate all animals, evolve them and then print them to screen

    Arguments:
        animals_list {list of animals} -- contains all animals
        screen {screen} -- the pygame screen
    """
    for animal in animals_list:
        animal.evolve(animals_list, s_event)
        animal.move(animals_list, s_event)
        animal.draw(screen)


if __name__ == "__main__":
    main()
