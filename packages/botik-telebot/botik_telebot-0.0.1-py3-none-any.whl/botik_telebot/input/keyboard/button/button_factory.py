from botik.input.keyboard.button.button_factory import ButtonFactory
from botik_telebot.input.keyboard.button.button import TgButton


class TgButtonFactory(ButtonFactory):
    button_type = TgButton
