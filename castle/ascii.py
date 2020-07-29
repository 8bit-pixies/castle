"""
A plain-old ascii rendering. We just use 
`os.system.clear()`
"""

from gym import Wrapper
import sys
import os

from castle.base import CastleMixin


class AsciiWrapper(Wrapper):
    def render(self):
        board = self.env.get_board()
        info = self.env.get_board_info()

        assert len(board.shape) == 2, "Ascii Wrapper does not support layers"
        text_board = [[info[c] for c in line] for line in board.tolist()]
        text_board = ["".join(l) for l in text_board]

        return text_board, info["text"].split("\n")

    def play(self, a):
        text = ""
        d = False
        try:
            _, _, d, _ = self.step(a)
        except:
            # possibly inject something into the text to display somehow
            text = "{} appears to be an invalid action".format(a)
        text_board, info = self.render()
        if text != "":
            info.append(text)
        return text_board, info, d
