from botik.input.keyboard.markup_factory import KeyboardMarkupFactory
from botik_telebot.input.keyboard.keyboard_markup import TgKeyboardMarkup


class TgKeyboardMarkupFactory(KeyboardMarkupFactory):
    def create(self, **native_args):
        return TgKeyboardMarkup(self.button_factory, native_args)
