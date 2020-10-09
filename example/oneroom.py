"""
A simple one small room variation
implemented in pure python
"""

import numpy as np
import random
from gym.spaces import Box, Discrete, Dict
import gym


class OneRoomGym(gym.Env):
    def __init__(
        self, width=5, height=5, switch_at_n_wins=1000, target_goals=3, max_steps=100
    ):
        # a win is recorded if n target goals are reached
        self.target_goals = target_goals
        # when we win n times, the target switches
        self.switch_at_n_wins = switch_at_n_wins
        self.max_steps = max_steps
        self.width = width
        self.height = height
        self.agent = (height // 2, width // 2)
        self.grid = np.zeros((height, width))
        self.observation_space = Box(low=-10.0, high=10.0, shape=(10,))
        self.action_space = Discrete(4)

        self._ep_target_counter = 0
        self._wins_in_row = 0
        self.reward = None

        self.target0 = None
        self.target1 = None
        self.current_target = 0
        self.step_counter = 0
        self.grid_mapping = {"agent": 1, "wall": 2, "target0": 3, "target1": 4}
        self.action_mapping = {
            0: (-1, 0),  # up
            1: (1, 0),  # down
            2: (0, -1),  # left
            3: (0, 1),  # right
            "w": (-1, 0),
            "a": (0, -1),
            "s": (1, 0),
            "d": (0, 1),
        }
        self.reset()

    def reset_goals(self):
        num_rand = self.width * self.height - 3
        self.grid = np.zeros((self.height, self.width))

        self.grid[self.agent] = self.grid_mapping["agent"]
        target_pos = np.argwhere(self.grid == 0).tolist()
        indx = random.sample(range(num_rand), 2)
        self.target0 = tuple(target_pos[indx[0]])
        self.target1 = tuple(target_pos[indx[1]])

        # self.grid[self.target0] = self.grid_mapping['target0']
        # self.grid[self.target1] = self.grid_mapping['target1']
        return self

    def move_agent(self, delta):
        agent = [self.agent[0] + delta[0], self.agent[1] + delta[1]]
        agent[0] = min(max(agent[0], 0), self.height - 1)
        agent[1] = min(max(agent[1], 0), self.width - 1)
        return tuple(agent)

    def refresh_target(self):
        if (self.agent[0] == self.target0[0] and self.agent[1] == self.target0[1]) or (
            self.agent[0] == self.target1[0] and self.agent[1] == self.target1[1]
        ):
            self.reset_goals()

    def render(self):
        self.grid = self.grid * 0
        self.grid[self.agent] = self.grid_mapping["agent"]
        self.grid[self.target0] = self.grid_mapping["target0"]
        self.grid[self.target1] = self.grid_mapping["target1"]
        return self.grid

    def step(self, action):
        done = False
        delta = self.action_mapping[action]
        self.agent = self.move_agent(delta)
        # print(self.agent)
        reward = self._reward()
        self.refresh_target()
        obs = self._obs()
        self.step_counter += 1
        if self.step_counter > self.max_steps:
            done = True
        return obs, reward, done, {}

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
        return np.array(self._obs())

    def _obs(self):
        obs = []
        obs.extend(self.agent)
        obs.extend(self.target0)
        obs.extend(self.target1)
        obs.append(self.agent[0] - self.target0[0])
        obs.append(self.agent[1] - self.target0[1])
        obs.append(self.agent[0] - self.target1[0])
        obs.append(self.agent[1] - self.target1[1])

        # obs space is size 10
        return np.array(obs)

    def _reward(self):
        if (
            self.agent[0] == self.target0[0] and self.agent[1] == self.target0[1]
        ) and self.current_target == 0:
            reward = 1
        elif (
            self.agent[0] == self.target1[0] and self.agent[1] == self.target1[1]
        ) and self.current_target == 1:
            reward = 1
        else:
            reward = -0.001
        self.reward = reward
        return reward

    def get_board(self):
        return self.render()

    def get_board_info(self):
        chr_mapping = {
            0: "ꞏ",
            1: "@",
            3: "0",
            4: "1",
            "text": "reward gained is: {}\nagent is at {}\ntarget0 is at {}\ntarget1 is at {}\ncurrent hidden target is {}\nobs:{}".format(
                self.reward,
                self.agent,
                self.target0,
                self.target1,
                self.current_target,
                self._obs(),
            ),
        }
        return chr_mapping


if __name__ == "__main__":
    try:
        from castle.base import play_blocking, play_random
        from castle.ascii import AsciiWrapper

        env = AsciiWrapper(OneRoomGym())
        play_blocking(env, keys=["w", "a", "s", "d"])
    except:
        pass
