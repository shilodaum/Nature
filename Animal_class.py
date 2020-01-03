import pygame
import abc
from pygame import locals
import math
from random import randint
from random import uniform

# Define some constant colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (90, 20, 20)
GRAY = (80, 80, 80)
PI = 3.141592653
# define constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
MOVEMENT = True


class Animal(abc.ABC):
    """an abstract class to represent all animals
    """

    def __init__(self, _b_size=50, _pos=None, _color=WHITE, _angle=0, _vel=10, _age=0, _success=0):
        """the ctor for all animal based classses
        
        Arguments:
            abc {ABC} -- the abstract class
        
        Keyword Arguments:
            _b_size {int} -- [body size] (default: {50})
            _pos {list} -- [x and y positions on screen] (default: {[0,0]})
            _color {color} -- [color for body size] (default: {WHITE})
            _angle {int} -- [the angle of the body, determines where will the animal look] (default: {0})
            _vel {int} -- [velocity of the animal if moving] (default: {10})
            _age {int} -- [age of animal, changes its behaviour acoording to aniaml type] (default: {0})
            _success {int} -- [determines of successful an animal is, changes its behaviour for evolving acoording to aniaml type] (default: {0})
        """
        if _pos is None:
            _pos = [0, 0]
        self.b_size = _b_size
        self.pos = _pos
        self.color = _color
        self.angle = _angle
        self.vel = _vel
        self.age = _age
        self.success = _success

    def copyCtor(self, animal):
        """copy constructor for 2 animals, shallow copy
        
        Arguments:
            animal {animal} -- the other animal to copy from. does not copy age or success
        """
        self.b_size = animal.b_size
        self.pos = animal.pos
        self.color = animal.color
        self.angle = animal.angle
        self.vel = animal.vel

    def draw(self, screen):
        """draw an animal, is not implemented here, to bere overridden by the sons
        
        Arguments:
            screen {pygame screen} -- the pygame screen to write character onto
        """
        pass

    def move(self, animals_list, event):
        """move an animal, is not implemented here, to bere overridden by the sons
        
        Arguments:
            animals_list {list of animals} -- contains all animals
        """
        pass

    def evolve(self, animals_list, event):
        """evolve an animal, is not implemented here, to bere overridden by the sons
        
        Arguments:
            animals_list {list of animals} -- contains all animals
        """
        pass

    def get_type(self):
        """get string type of animal, to be overridden by sons 
        """
        pass
