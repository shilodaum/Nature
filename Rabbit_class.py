from Animal_class import *
import pygame
from pygame import locals
import math
from random import randint
from random import uniform

import Bush_class

RABBIT_FOLLOW_CURSOR = False
EAT_BUSHES = True
RABBIT_SIZE = 20


class Rabbit(Animal):
    """a Rabbit, it might eat bushes or follow cursor
    
    Arguments:
        Animal {Animal} -- subclass of Animal
    """

    def __init__(self, rabbit=0):
        """constructor, changes beaviour according to the argument type
        
        Keyword Arguments:
            rabbit {int or Rabbit} -- if is not Rabbit: create constructor, else create shallow copy (default: {0})
        """
        if isinstance(rabbit, (Rabbit)):
            # shallow copy
            self.copyCtor(rabbit)
        else:
            # ctor for rabbit with default values
            Animal.__init__(self, RABBIT_SIZE, [0, 0], WHITE, uniform(0, 2 * PI), 7, 0, 20)
            self.eye_color = RED
            # random position
            self.pos = [randint(self.b_size, SCREEN_WIDTH - self.b_size),
                        randint(self.b_size, SCREEN_HEIGHT - self.b_size)]

    # override
    def move(self, animals_list, event):
        """move the Rabbit according to the environment
        
        Arguments:
            animals_list {list of Animal} -- list of all animals
        """
        achieved_target = False
        # turn toward cursor
        if RABBIT_FOLLOW_CURSOR:
            # calculate the angle required to get to cursor
            cursor_pos = pygame.mouse.get_pos()
            x_dis = (cursor_pos[0] - self.pos[0])
            y_dis = -(cursor_pos[1] - self.pos[1])
            angle = math.atan2(y_dis, x_dis)
            self.angle = angle
            # impossible angle
            if self.angle >= 2 * PI:
                self.angle -= 2 * PI
            # if cannot get any closer
            if MOVEMENT and (x_dis ** 2 + y_dis ** 2) < self.vel ** 2:
                achieved_target = True

        # go the the closest bush
        elif EAT_BUSHES:
            x_dis = SCREEN_WIDTH + 1.0
            y_dis = SCREEN_HEIGHT + 1.0  # max vslues for x,y distances
            # use list comprehension to isolate all bushes into a second list
            bushes_list = [bush for bush in animals_list if isinstance(bush, (Bush_class.Bush))]
            chosen_bush = 0
            # iterate all bushes to finf the closest one
            for bush in bushes_list:
                new_x_dis = (bush.pos[0] - self.pos[0])
                new_y_dis = (bush.pos[1] - self.pos[1])
                # check if current distance is lower than the last one
                if x_dis ** 2 + y_dis ** 2 > new_x_dis ** 2 + new_y_dis ** 2:
                    x_dis = new_x_dis
                    y_dis = new_y_dis
                    # set new closest bush
                    chosen_bush = bush

            # there is a bush
            if not (x_dis == SCREEN_WIDTH + 1.0 or y_dis == SCREEN_HEIGHT + 1.0):
                # evaluate the required angle
                angle = math.atan2(-y_dis, x_dis)
                self.angle = angle
                # impossible angle handle
                if self.angle >= 2 * PI:
                    self.angle -= 2 * PI
            # is on bush
            if (MOVEMENT and chosen_bush and (x_dis ** 2 + y_dis ** 2) < (chosen_bush.b_size + self.b_size) ** 2):
                animals_list.remove(chosen_bush)
                # get success if ate
                self.success = min(self.success + 10, 100)
                achieved_target = True
            # did not eat
            else:
                self.success -= 1.0 / 5
            # is on wall
            if (not len(bushes_list)) and (
                    self.pos[0] > SCREEN_WIDTH - self.b_size or self.pos[1] > SCREEN_HEIGHT - self.b_size or self.pos[
                0] < self.b_size or self.pos[1] < self.b_size):
                achieved_target = True

        # move rabbit
        if MOVEMENT and (not achieved_target):
            self.pos[0] += self.vel * math.cos(self.angle)
            self.pos[1] -= self.vel * math.sin(self.angle)

    # override
    def draw(self, screen):
        """draw a Rabbit
        
        Arguments:
            screen {pygame screen} -- the screen we draw write onto
        """

        x = self.pos[0]
        y = self.pos[1]
        # draw the animal main body with the color
        pygame.draw.circle(screen, self.color, [int(x), int(y)], int(self.b_size))
        # add eyes- calculate eyes positions
        new_x = math.cos(self.angle) * self.b_size / 2
        new_y = math.sin(-self.angle) * self.b_size / 2
        # draw eyes with deviation so it looks more realistic
        pygame.draw.circle(screen, self.eye_color, [int(x + new_x + new_y / 1.5), int(y + new_y - new_x / 1.5)],
                           int(self.b_size / 4.0))
        pygame.draw.circle(screen, self.eye_color, [int(x + new_x - new_y / 1.5), int(y + new_y + new_x / 1.5)],
                           int(self.b_size / 4.0))
        # draw pupils with deviation
        pygame.draw.circle(screen, BROWN, [int(x + new_x * 1.2 + new_y / 1.5), int(y + new_y * 1.2 - new_x / 1.5)],
                           int(self.b_size / 8.0))
        pygame.draw.circle(screen, BROWN, [int(x + new_x * 1.2 - new_y / 1.5), int(y + new_y * 1.2 + new_x / 1.5)],
                           int(self.b_size / 8.0))
        # draw ears on the body edge, rabbits have round ears
        pygame.draw.circle(screen, self.color, [int(x - new_x + new_y), int(y - new_y - new_x)], int(self.b_size / 2.0))
        pygame.draw.circle(screen, self.color, [int(x - new_x - new_y), int(y - new_y + new_x)], int(self.b_size / 2.0))
        # write Rabbit's score on his body
        font = pygame.font.SysFont('Calibri', 25, True, False)
        text = font.render(str(int(self.success)), True, RED)
        screen.blit(text, self.pos)

    # override
    def evolve(self, animals_list, event):
        """evolve the rabbit
        
        Arguments:
            animals_list {list of Animal} -- includes all animals
        """
        # if a rabbit is successful, duplicate it
        if self.success > 80:
            new_born = Rabbit()
            new_born.pos = \
                [randint(int(self.pos[0] - SCREEN_WIDTH / 10), int(self.pos[0] + SCREEN_WIDTH / 10)),
                 randint(int(self.pos[1] - SCREEN_HEIGHT / 10), int(self.pos[1] + SCREEN_HEIGHT / 10))]
            new_born.success = 15
            self.b_size /= 3.0
            self.success = 20
            # add new rabbit to all animals
            animals_list.append(new_born)
        elif self.success > 50 and self.b_size < 120:
            # success to gain weight, add size and decrease success
            self.b_size += 1
            self.success -= 10
            # as a rbbits becomes fatter it also becomes slower
            self.vel = max(self.vel - 0.1, 1)
        elif self.success < 10 and self.b_size > 10:
            # when a  rabbit is starving, it gets thinner
            self.success += 1
            self.b_size -= max(1 / 5.0, self.b_size / 30.0)
            self.vel += 0.5
        elif self.success < 0:
            # die of starvation
            animals_list.remove(self)

    # override
    def get_type(self):
        """get string type
        
        Returns:
            [str] -- type
        """
        return "Rabbit"
