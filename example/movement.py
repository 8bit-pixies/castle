"""
What is the grid world is less grid like - sort of like zelda?
"""

from enum import Enum
import numpy as np
import random
import gym
from gym.spaces import Box, Discrete, Tuple


class Direction(Enum):
    NOOP = 0
    N = 1
    S = 2
    W = 3
    E = 4
    NE = 5
    NW = 6
    SE = 7
    SW = 8


direction_delta = dict(
    N=(-1, 0),
    S=(1, 0),
    W=(0, -1),
    E=(0, 1),
    NE=(-1, 1),
    NW=(-1, -1),
    SE=(1, 1),
    SW=(1, -1),
)


class Block(object):
    """
    a block of some shape, we always start from the top left corner
    and we can move it around (+ checking collisions)
    """

    def __init__(self, x, y, height=1, width=1):
        self.x = x
        self.y = y
        self.height = height
        self.width = width

    def try_move(self, direction, mask=None):
        if Direction(direction) == Direction["NOOP"]:
            return self

        dx, dy = direction_delta[Direction(direction).name]
        x, y = self.x + dx, self.y + dy

        if mask is None:
            self.x = x
            self.y = y
            return self
        if not (
            x >= 0
            and y >= 0
            and x + self.height < mask.shape[0]
            and y + self.width < mask.shape[1]
        ):
            # out of bounds
            return self
        elif np.sum(mask[x : x + self.height, y : y + self.width]) == 0:
            # otherwise we have to check that the new proposal is all in blank spaces
            self.x = x
            self.y = y
            return self
        else:
            # we'll collide with something in proposed move
            return self

    def create_mask(self, height, width):
        base_mask = np.zeros((height, width))
        base_mask[self.x : self.x + self.height, self.y : self.y + self.width] = 1
        return base_mask


maze = """000000000000000000000
000000000000000000000
000000000000000000000
000000000000000000000
000000001111111000000
000000000000001000000
000000000000001000000
000000000000001000000
000000000000001000000
000000000000001000000
000000000000001000000
000000000000001000000
000000000000001000000
000000000000000000000
000000000000000000000""".split(
    "\n"
)
maze = np.array([list(x) for x in maze]).astype(int)


class GridWorld(gym.Env):
    def __init__(self, maze=maze, block=None):
        self.maze = maze
        self.height, self.width = maze.shape
        if block is None:
            self.block = Block(1, 1, 2, 2)
        else:
            self.block = block
        self.last_action = None
        self.action_space = Discrete(9)
        self.observation_space = Box(0, 10, (self.height, self.width))

    def step(self, action):
        self.last_action = Direction(action).name.ljust(5, " ")
        self.block.try_move(action, self.maze)
        return None, None, None, None

    def get_board(self):
        maze_render = self.maze.copy()
        block_mask = self.block.create_mask(self.height, self.width).astype(int)
        maze_render[block_mask > 0] = 2
        assert np.sum(block_mask) > 0
        return maze_render

    def get_board_info(self):
        chr_mapping = {
            0: "ꞏ",
            1: "#",
            2: "@",
            "text": "last action taken is: {}".format(self.last_action),
        }
        return chr_mapping


if __name__ == "__main__":
    from castle.base import play_blocking, play_random
    from castle.ascii import AsciiWrapper

    env = AsciiWrapper(GridWorld(block=Block(1, 1, 4, 4)))
    play_random(env, 0.01)
