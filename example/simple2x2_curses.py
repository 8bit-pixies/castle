import numpy as np
import random
from os import system

import gym
from gym.spaces import Box, Discrete, Tuple


class Simple2x2(gym.Env):
    """
    Builds a simple path-finding task on a 2x2 grid. 
    The agent starts in top left corner (state 1), with
    the goal of getting to state "G"

    0  1
    2  3
    """

    state = 0
    last_action = None
    prev_state = 0
    observation_space = Box(-1, 1, shape=(5,))
    action_space = Discrete(4)
    max_steps = 100
    step_counter = 0

    def gen_obs(self):
        obs = [0, 0, 0, 0, 0]
        obs[self.state] = 1
        return obs

    def reset(self):
        self.state = 0
        self.last_action = None
        self.prev_state = 0
        self.step_counter = 0
        return self.gen_obs()

    def step(self, action):
        # we hardcode the action order...
        # 0,1,2,3 --> up down left right
        self.prev_state = self.state
        self.last_action = action

        if self.state == 0 and action == 3:
            self.state = 1
        elif self.state == 0 and action == 1:
            self.state = 2
        elif self.state == 1 and action == 1:
            self.state = 3
        elif self.state == 1 and action == 2:
            self.state = 0
        elif self.state == 2 and action == 3:
            self.state = 3
        elif self.state == 2 and action == 0:
            self.state = 0

        done = self.state == 3
        reward = 100 if done else 0
        self.step_counter += 1
        if self.step_counter > self.max_steps:
            done = True
        return self.gen_obs(), reward, done, {}

    def render(self):
        action_mapping = dict(zip(range(4), ["UP", "DOWN", "LEFT", "RIGHT"]))
        state = np.zeros((2, 2), "<U1")
        state[1, 1] = "G"

        if self.state == 0:
            state[0, 0] = "A"
        elif self.state == 1:
            state[0, 1] = "A"
        elif self.state == 2:
            state[1, 0] = "A"
        elif self.state == 3:
            state[1, 1] = "A"

        print(state)
        print("Taking action: ", action_mapping.get(self.last_action))
        if self.state == 3:
            print("Solved game!")
        else:
            print("Action mapping is: ", action_mapping)
        print("\n")

    def get_board(self):
        state = np.zeros((2, 2))
        state[1, 1] = 2

        if self.state == 0:
            state[0, 0] = 1
        elif self.state == 1:
            state[0, 1] = 1
        elif self.state == 2:
            state[1, 0] = 1
        elif self.state == 3:
            state[1, 1] = 1
        return state

    def get_board_info(self):
        chr_mapping = {
            0: "ꞏ",
            1: "A",
            2: "G",
            "text": "\nTo play the game: \n0 to move UP\n1 to move DOWN\n2 to move LEFT\n3 to move RIGHT\n\nLast action taken: {}".format(
                self.last_action
            ),
        }
        return chr_mapping


if __name__ == "__main__":
    from castle.base import play_blocking
    from castle.ascii import AsciiWrapper
    from castle.curses_wrapper import AppWrapper

    AppWrapper(env=AsciiWrapper(Simple2x2())).run()
