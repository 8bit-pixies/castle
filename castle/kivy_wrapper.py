"""
A simple kivy wrapper
"""

import kivy

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock


"""
A really simple discrete environment to test for changing policies/environment
"""

import numpy as np
import random
from gym.spaces import Box, Discrete, Dict
import gym
from gym import Wrapper


class KivyWrapper(BoxLayout):
    def __init__(self, env=None, **kwargs):
        super(KivyWrapper, self).__init__(**kwargs)
        self.env = env
        self.action = None
        self.info = Label(text="Starting Game", font_name="RobotoMono-Regular")
        # self._trigger = Clock.schedule_interval(self.update, 1.0/60.0)
        self.add_widget(self.info)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, "text")
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def show_screen(self, board, info, update):
        text = ""
        if update and board is not None:
            text += "\n".join(board)
            text += "\n"
            text += "\n".join(info)
        self.info.text = text

    def update(self, dt):
        for idx in range(10):
            if self.action == str(idx):
                self.action = idx

        if self.action is not None:
            text_render, info, done = self.env.play(self.action)
        else:
            text_render, info = self.env.render()
        self.show_screen(text_render, info, True)
        self.action = None

    def _keyboard_closed(self):
        # print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        key_register = modifiers + [text]
        # print("Key input received is:\n{}".format(key_register))
        self.action = text

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == "escape":
            keyboard.release()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True


def app_wrapper(env):
    class MyApp(App):
        def build(self):
            game = KivyWrapper(env=env)
            game.env.reset()
            Clock.schedule_interval(game.update, 1.0 / 60.0)
            return game

    return MyApp
