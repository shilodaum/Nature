from Animal_class import *

BUSH_SIZE = 10


class Bush(Animal):
    """a plant that does not move but changes color and dies as time goes
    
    Arguments:
        Animal {extends Animal class} -- extends the Animall class
    """

    def __init__(self, bush=0):
        """constructor, changes beaviour according to the argument type
        
        Keyword Arguments:
            bush {int or Bush} -- if is not Bush create constructor, else create shallow copy (default: {0})
        """
        if isinstance(bush, (Bush)):
            # call copy constructor
            self.copyCtor(bush)
        else:
            # call animal constructor for bush default values
            Animal.__init__(self, BUSH_SIZE, [0, 0], GREEN, GREEN, 0, 0)
            # create random position
            self.pos = [randint(self.b_size, SCREEN_WIDTH - self.b_size),
                        randint(self.b_size, SCREEN_HEIGHT - self.b_size)]

    # override
    def draw(self, screen):
        """draw a bush
        
        Arguments:
            screen {pygame screen} -- the screen we print our bush onto
        """
        x = self.pos[0]
        y = self.pos[1]
        # a bush is a circle with a changing color over time
        pygame.draw.circle(screen, self.color, [int(x), int(y)], int(self.b_size))

    # override
    def move(self, animals_list, event):
        """move a bush, bushes usually don't move so this class is not implemented

        Arguments:
            animals_list {list of Animals} -- [list of all animals]
        """
        pass

    # override
    def evolve(self, animals_list, event):
        """evolve a bush, increase its age and change its color
        
        Arguments:
            animals_list {list of Animal} -- a list that includes all animals
        """
        # change age
        self.age += 1 / 50.0
        # delete if older than 10
        if self.age > 10:
            animals_list.remove(self)
        else:
            # if not too old, change color slightly and make older
            self.color = (self.color[0], max(self.color[1] - 20 / 50, 20), self.color[2])
            self.b_size += 1 / 50

        # override

    def get_type(self):
        """get string type
        
        Returns:
            [str] -- type
        """
        return "Bush"
