from Animal_class import *
import Rabbit_class

WOLF_SIZE = 50
WOLF_FOLLOW_CURSOR = True
EAT_RABBITS = False


class Wolf(Animal):
    """a wolf class, it might eat rabbits or follow cursor
    
    Arguments:
        Animal {Animal} -- base class
    """

    def __init__(self, wolf=0):
        """ctor for Wolf class
        
        Keyword Arguments:
            wolf {int or Wolf} -- if wolf is Wolf- shallow copy, else ctor for default Animal values (default: {0})
        """
        if isinstance(wolf, (Wolf)):
            # shallow copy
            self.copyCtor(wolf)
        else:
            # ctor for default values for wolf
            Animal.__init__(self, WOLF_SIZE, [0, 0], GRAY, uniform(0, 2 * PI), 1)
            self.eye_color = BROWN
            # random position
            self.pos = [randint(self.b_size, SCREEN_WIDTH - self.b_size),
                        randint(self.b_size, SCREEN_HEIGHT - self.b_size)]

    def calc_pointy_ears(self):
        """help function to draw, takes care of calculating the wolf's pointy ears to draw
        
        Returns:
            [list of points] -- the ears' points for 2 ears
        """
        x = self.pos[0]
        y = self.pos[1]
        # calc new x and new y to help calc the ears
        new_x = math.cos(self.angle) * self.b_size / 2.0
        new_y = math.sin(-self.angle) * self.b_size / 2.0

        results = []

        # for each ear
        for pos in [[x - new_x + new_y, y - new_y - new_x], [x - new_x - new_y, y - new_y + new_x]]:
            r1 = self.b_size
            r2 = self.b_size / 1.3
            # calculate base points for ears
            r = math.sqrt((new_y - new_x) ** 2 + (new_x + new_y) ** 2)
            base_points = [
                (1 / 2.0) * (self.pos[0] + pos[0]) + ((r1 ** 2 - r2 ** 2) / (2 * (r ** 2))) * (pos[0] - self.pos[0]),
                (1 / 2.0) * (self.pos[1] + pos[1]) + ((r1 ** 2 - r2 ** 2) / (2 * (r ** 2))) * (pos[1] - self.pos[1])]
            epsilon = ((1 / 2.0) * math.sqrt(
                (2 * (r1 ** 2 + r2 ** 2) / (r ** 2)) - ((r1 ** 2 - r2 ** 2) / (r ** 4)) - 1))
            # edit base point to fit the wanted ear size
            point_1 = [base_points[0] + epsilon * (pos[1] - self.pos[1]),
                       base_points[1] + epsilon * (-pos[0] + self.pos[0])]
            point_2 = [base_points[0] - epsilon * (pos[1] - self.pos[1]),
                       base_points[1] - epsilon * (-pos[0] + self.pos[0])]
            # point between point1 and 2
            avg_pt = [(point_1[0] + point_2[0]) / 2.0, (point_1[1] + point_2[1]) / 2.0]

            # normalize points, make them closer to each other
            point_1 = [(3 * point_1[0] + avg_pt[0]) / 4.0, (3 * point_1[1] + avg_pt[1]) / 4.0]
            point_2 = [(3 * point_2[0] + avg_pt[0]) / 4.0, (3 * point_2[1] + avg_pt[1]) / 4.0]
            point_3 = [2 * avg_pt[0] - x, 2 * avg_pt[1] - y]
            # add this ear to the results 
            results.append([point_1, point_2, point_3])
        return results

    # override
    def move(self, animals_list, event):
        """move a wolf's positon
        
        Arguments:
            animals_list {list of Animal} -- list that includes all animals
        """
        achieved_target = False
        # follow rabbits
        if EAT_RABBITS:
            x_dis = SCREEN_WIDTH + 1.0
            y_dis = SCREEN_HEIGHT + 1.0  # max values for x,y distances
            rabbits_list = [rabbit for rabbit in animals_list if isinstance(rabbit, (Rabbit_class.Rabbit))]
            chosen_rabbit = 0
            for rabbit in rabbits_list:
                new_x_dis = (rabbit.pos[0] - self.pos[0])
                new_y_dis = (rabbit.pos[1] - self.pos[1])

                if x_dis ** 2 + y_dis ** 2 > new_x_dis ** 2 + new_y_dis ** 2:
                    x_dis = new_x_dis
                    y_dis = new_y_dis
                    chosen_rabbit = rabbit
            # there is a rabbit
            if not (x_dis == SCREEN_WIDTH + 1.0 or y_dis == SCREEN_HEIGHT + 1.0):
                angle = math.atan2(-y_dis, x_dis)
                self.angle = angle
                if self.angle >= 2 * PI:
                    self.angle -= 2 * PI
            # eat rabbit
            if (MOVEMENT and chosen_rabbit and (x_dis ** 2 + y_dis ** 2) < (chosen_rabbit.b_size + self.b_size) ** 2):
                animals_list.remove(chosen_rabbit)
                achieved_target = True
            if (not len(rabbits_list)) and (
                    self.pos[0] > SCREEN_WIDTH - self.b_size or self.pos[1] > SCREEN_HEIGHT - self.b_size or self.pos[
                0] < self.b_size or self.pos[1] < self.b_size):
                achieved_target = True

        elif WOLF_FOLLOW_CURSOR:
            # get cursor position
            cursor_pos = pygame.mouse.get_pos()
            x_dis = (cursor_pos[0] - self.pos[0])
            y_dis = -(cursor_pos[1] - self.pos[1])
            # calculate the angle required to get to cursor
            angle = math.atan2(y_dis, x_dis)
            self.angle = angle
            # impossible angle
            if self.angle >= 2 * PI:
                self.angle -= 2 * PI
            # if cannot get any closer
            if MOVEMENT and (x_dis ** 2 + y_dis ** 2) < self.vel ** 2:
                achieved_target = True

        # move animal
        if MOVEMENT and (not achieved_target):
            delta_x = self.vel * math.cos(self.angle)
            delta_y = self.vel * math.sin(self.angle)
            if event == "MOUSE_BUTTON_DOWN":
                delta_x *= 2
                delta_y *= 2
            self.pos[0] += delta_x
            self.pos[1] -= delta_y

    # override
    def draw(self, screen):
        """draw a wolf on pygame screen
        
        Arguments:
            screen {pygame screen} -- the screen to write onto
        """
        x = self.pos[0]
        y = self.pos[1]
        # draw body
        pygame.draw.circle(screen, self.color, [int(x), int(y)], int(self.b_size))
        # calc deviation for eyes to look more realistic
        new_x = math.cos(self.angle) * self.b_size / 2.0
        new_y = math.sin(-self.angle) * self.b_size / 2.0
        # draw eyes
        pygame.draw.circle(screen, self.eye_color, [int(x + new_x + new_y / 1.5), int(y + new_y - new_x / 1.5)],
                           int(self.b_size / 4.0))
        pygame.draw.circle(screen, self.eye_color, [int(x + new_x - new_y / 1.5), int(y + new_y + new_x / 1.5)],
                           int(self.b_size / 4.0))
        # draw pupils
        pygame.draw.circle(screen, BLACK, [int(x + new_x * 1.2 + new_y / 1.5), int(y + new_y * 1.2 - new_x / 1.5)],
                           int(self.b_size / 8.0))
        pygame.draw.circle(screen, BLACK, [int(x + new_x * 1.2 - new_y / 1.5), int(y + new_y * 1.2 + new_x / 1.5)],
                           int(self.b_size / 8.0))

        # pointy ears calculate and draw
        ears = self.calc_pointy_ears()
        for ear in ears:
            pygame.draw.polygon(screen, self.color, ear, 0)

    # override
    def evolve(self, animals_list, event):
        """evolve wolf, currently wolf does not evolve
        
        Arguments:
            animals_list {list of Animal} -- contains all animals
        """
        pass

        # override

    def get_type(self):
        """get string type
        
        Returns:
            [str] -- type
        """
        return "Wolf"
