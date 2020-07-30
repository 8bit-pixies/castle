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

    correct_stdout = sys.stdout

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
    sys.stdout = correct_stdout
    text = env.get_board_info()["text"].split("\n")
    print("\n".join(text))
    input("\nPress Enter to quit")


def play(env):
    """
    performs rollout
    """
    import curses
    import sys
    import os

    correct_stdout = sys.stdout

    def show_screen(scr, board, text, update):
        idx = 0
        if update and board is not None:
            # scr.clear()
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
    start_time = time.time()
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
                start_time = time.time()

        if time.time() - start_time > 1:
            action = 0
            update = True
            start_time = time.time()

    show_screen(scr, text_render, info, update)
    # scr.keypad(0)
    curses.echo()
    curses.endwin()
    sys.stdout = correct_stdout
    text = env.get_board_info()["text"].split("\n")
    print("\n".join(text))
    input("Press Enter to quit")


def play_random(env, delay=1):
    """
    performs rollout
    """
    import curses
    import sys
    import os

    correct_stdout = sys.stdout

    def show_screen(scr, board, text, update):
        idx = 0
        if update and board is not None:
            # scr.clear()
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

    update = True
    action = ""
    start_time = time.time()
    key = ""
    while key != ord("q"):
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

        if time.time() - start_time > delay:
            action = env.action_space.sample()
            update = True
            start_time = time.time()

    show_screen(scr, text_render, info, update)
    # scr.keypad(0)
    curses.echo()
    curses.endwin()
    sys.stdout = correct_stdout
    text = env.get_board_info()["text"].split("\n")
    print("\n".join(text))
