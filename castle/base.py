"""
Mixin which the environments should be structured - you don't have to use this. 

In fact I think this is actually a bad idea. But just for reference and 
documentation.
"""

import time  # time.sleep(0.2) for 200 milliseconds sleeping


class CastleMixin(object):
    def get_board(self):
        raise NotImplementedError

    def get_board_info(self):
        return {}

    def play(self):
        """
        Don't touch this(?)
        """
        pass

    def action_mapping(self):
        """
        we just assume NOOP is always "0"
        support discrete spaces only.
        """
        return 0


def play_blocking(env):
    """
    performs rollout on a blocking environment
    """
    import curses
    import sys
    import os

    def show_screen(scr, board, text, update):
        idx = 0
        if update and board is not None:
            scr.clear()
            for idx, el in enumerate(board):
                scr.addstr(idx, 0, el)
            idx += 1
            for tidx, el in enumerate(text):
                scr.addstr(idx + tidx, 0, el)

        return idx

    scr = curses.initscr()
    curses.noecho()
    scr.nodelay(True)
    scr.clear()
    done = False

    update = True
    action = ""
    while not done:
        if action != "":
            text_render, info, done = env.play(action)
        else:
            text_render, info = env.render()

        # reset stuff
        show_screen(scr, text_render, info, update)
        update = False
        action = ""

        key = scr.getch()
        info = {}

        for k in range(10):
            if key == ord(str(k)):
                # TODO some kind of error checking
                action = k
                update = True
    show_screen(scr, text_render, info, update)
    curses.endwin()


def play(env):
    """
    performs rollout
    """

    def show_screen(board, text):
        scr.clear()

        for idx, el in enumerate(board):
            scr.addstr(idx, 0, el)
        idx += 1
        for tidx, el in enumerate(text):
            scr.addstr(idx + tidx, 0, el)

    import curses
    import sys
    import os

    scr = curses.initscr()
    curses.noecho()
    scr.nodelay(True)
    scr.clear()
    done = False
    time_start = time.time()
    while not done:
        action = 0
        text_render, info = env.render()
        show_screen(text_render, info)

        key = scr.getch()
        info = {}

        for k in range(10):
            if key == ord(str(k)):
                # TODO some kind of error checking
                action = k

        if "sleep" in info.keys():
            if time.time() - time_start > info.get("sleep"):
                time_start = time.time()
                text_render, info = env.play(action)
    curses.endwin()
