import asyncio

from botik.api import set_api
from botik.app import App
from botik.navigation import navigator
from botik.page.page_factory import PageFactory
from botik_telebot.api.api import TgApi
from botik_telebot.input.message_handlers.raw_message_handlers import RawMessageHandlers
from botik_telebot.page.page_factory import TgPageFactory


class TgApp(App):
    def start(self):
        self.initialize()
        loop = asyncio.get_event_loop()
        loop.create_task(self.bot.polling())
        loop.run_forever()

    def __init__(self, bot, start_callback=None):
        super().__init__(bot)
        RawMessageHandlers(bot, start_callback,
                           self.users, self.user_input)

    def initialize(self):
        api = TgApi(self.bot)
        set_api(api)

        self._page_fac: PageFactory = TgPageFactory()
        navigator.initialize(self._page_fac, self.pages_data)
