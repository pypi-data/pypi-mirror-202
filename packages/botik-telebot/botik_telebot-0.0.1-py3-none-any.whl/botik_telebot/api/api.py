from botik.api.api import Api
from botik_telebot.api.api_type import TgApiType
from botik_telebot.api.send_message import TgSendMessage


class TgApi(Api):
    def __init__(self, bot):
        self.bot = bot
        self.msg = TgSendMessage(bot)
        self.api_type = TgApiType()
