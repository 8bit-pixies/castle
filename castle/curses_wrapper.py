"""
Curses wrapper in a similar structure to the kivy wrapper for consistency
"""

import time  # time.sleep(0.2) for 200 milliseconds sleeping
import curses
import sys
import os


class AppWrapper(object):
    def __init__(self, env, blocking=True):
        self.env = env
        self.blocking = blocking
        self.correct_stdout = sys.stdout
        self.scr = curses.initscr()
        curses.noecho()
        self.scr.nodelay(True)
        self.scr.clear()
        self.done = False
        self.action = None

    def show_screen(self, board, text, update):
        idx = 0
        if update and board is not None:
            self.scr.clear()
            for idx, el in enumerate(board):
                try:
                    self.scr.addstr(idx, 0, el)
                except:
                    pass
            idx += 1
            for tidx, el in enumerate(text):
                try:
                    self.scr.addstr(idx + tidx, 0, el)
                except:
                    pass
        return idx

    def update(self, dt=None):
        if self.action is not None and self.action != "":
            text_render, info, _ = self.env.play(self.action)
            self.show_screen(text_render, info, True)
            self.action = None

    def play(self, keys=[]):
        refresh = True
        done = False
        text_render, info = self.env.render()
        self.show_screen(text_render, info, refresh)
        while not done:
            if self.action != "":
                refresh = True
                self.update()

            key = self.scr.getch()
            info = {}

            for k in range(10):
                if key == ord(str(k)):
                    # TODO some kind of error checking
                    self.action = k

            # check for "W", "A", "S", "D" override
            if key in [ord(x) for x in keys]:
                self.action = chr(key)
                # print(action)

        self.update()

    def run(self):
        return self.play()
