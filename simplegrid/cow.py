import colorsys
import math
import random
from enum import IntEnum

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


MAX_ENERGY = 1000


class Action(IntEnum):
    NONE = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
    SPLIT = 5

    @classmethod
    def from_letter(cls, letter):
        number = 'URDL'.find(letter) + 1
        return cls(number)

    def __repr__(self):
        return self.name

    def to_direction(self):
        return {
            Action.UP: (0, -1),
            Action.RIGHT: (1, 0),
            Action.DOWN: (0, 1),
            Action.LEFT: (-1, 0),
        }[self]

    def to_observation(self, offset):
        dir = self.to_direction()
        return dir[0] + offset, dir[1] + offset


def random_color():
    hue = random.uniform(0.5, 1.1)
    lightness = random.uniform(0.5, 0.8)
    saturation = random.uniform(0.7, 0.9)
    return tuple(map(lambda f: int(f * 255), colorsys.hls_to_rgb(hue, lightness, saturation)))


class SimpleCow(object):
    id_count = 1

    def __init__(self, x, y, settings, energy=None):
        self.x = x
        self.y = y
        self.settings = settings
        self.color = random_color()
        self.actioncolor = BLACK
        self.energy = energy or settings.init_energy
        self.id = SimpleCow.id_count
        SimpleCow.id_count += 1

    def step(self, observation):
        if self.energy > MAX_ENERGY:
            return Action.SPLIT

        return random.choice(list(Action)[1:-1])

    def learn(self, reward, done):
        pass

    def draw(self, display):
        display.circle(
            self.x, self.y, math.sqrt(min(0.64, 2 * self.energy / MAX_ENERGY)), self.color
        )
        # Action color is interesting for later. For now it has no use
        # display.circle(
        #     self.x,
        #     self.y,
        #     0.3 * min(0.8, math.sqrt(2 * self.energy / MAX_ENERGY)),
        #     self.actioncolor,
        # )

    def split(self):
        new_creature = self.__class__(self.x, self.y, self.settings, self.energy / 2)
        self.energy /= 2
        return new_creature

    def __repr__(self):
        return '\%s:%02d/' % (self.__class__.__name__, self.id)


class GreedyCow(SimpleCow):
    def __init__(self, x, y, settings, energy=None):
        super().__init__(x, y, settings, energy)
        self.color = RED

    def step(self, observation):

        if self.energy > MAX_ENERGY:
            return Action.SPLIT

        offset = observation.shape[0] // 2
        possible_actions = list(Action)[1:-1]
        interesting_actions = [
            a for a in possible_actions if observation[a.to_observation(offset)] == -1
        ]

        if interesting_actions:
            return random.choice(interesting_actions)
        else:
            return Action.RIGHT  # Was: random.choice(possible_actions)
