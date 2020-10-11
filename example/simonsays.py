"""
A really simple discrete environment to test for changing policies/environment
"""

import numpy as np
import random
from gym.spaces import Box, Discrete, Dict
import gym


class SimonSays(gym.Env):
    def __init__(self, switch_at_n_wins=2, target_goals=5, max_steps=10):
        # a win is recorded if n target goals are reached
        self.target_goals = target_goals
        # when we win n times, the target switches
        self.switch_at_n_wins = switch_at_n_wins
        self.max_steps = max_steps
        self.observation_space = Box(low=-1, high=1, shape=(4,), dtype=np.uint8)
        self.action_space = Discrete(4)

        self._ep_target_counter = 0
        self._wins_in_row = 0
        self.reward = None

        self.target0 = None
        self.target1 = None
        self.current_target = 0
        self.step_counter = 0
        self.reset()

    def reset_goals(self):
        rand = list(range(4))
        random.shuffle(rand)
        self.target0 = rand[0]
        self.target1 = rand[1]
        return self

    def refresh_target(self, act):
        if act == self.target0 or act == self.target1:
            self.reset_goals()

    def reset(self):
        if self._ep_target_counter > self.target_goals:
            self._wins_in_row += 1
        else:
            self._wins_in_row = 0

        if self._wins_in_row > self.switch_at_n_wins:
            self._wins_in_row = 0
            self.current_target = 1 - self.current_target

        self._ep_target_counter = 0
        self.step_counter = 0
        self.reset_goals()
        return self._obs()

    def _obs(self):
        obs = np.zeros(4)
        obs[self.target0] = 1
        obs[self.target1] = -1
        return obs

    def _reward(self, action):
        reward = 0
        if self.current_target == 0:
            if action == self.target0:
                reward = 1
            elif action == self.target1:
                reward = 0
            else:
                reward = -0.001
        else:
            if action == self.target0:
                reward = 0
            elif action == self.target1:
                reward = 1
            else:
                reward = -0.001

        self.reward = reward
        return self

    def step(self, action):
        done = False
        self._reward(action)
        self.refresh_target(action)
        obs = self._obs()
        self.step_counter += 1
        if self.step_counter > self.max_steps:
            done = True
        return obs, self.reward, done, {}

    def get_board(self):
        return self._obs().reshape(1, -1)

    def get_board_info(self):
        chr_mapping = {
            0: "ꞏ",
            1: "0",
            -1: "1",
            "text": "reward gained is: {}\ntarget0: {}\ntarget1: {}\ncurrent hidden is: {}".format(
                self.reward, self.target0, self.target1, self.current_target
            ),
        }
        return chr_mapping


if __name__ == "__main__":
    from castle.base import play_blocking, play_random
    from castle.ascii import AsciiWrapper

    env = AsciiWrapper(SimonSays())
    play_blocking(env)
