import logging
import telebot

from botik.input.message_handlers.events import events
from botik.input.message_handlers.raw_message_handlers import RawMessageHandlers

from botik_telebot.api.attachment_handlers.photo_attachment_handler import PhotoAttachmentHandler


class RawMessageHandlers(RawMessageHandlers):
    def _initialize_handlers(self, bot):
        bot.message_handler(content_types=['text'])(self.message_reply)
        bot.message_handler(content_types=['photo'])(self.photo_reply)
        bot.message_handler(content_types=['contact'])(self.phone_reply)
        bot.message_handler(content_types=['location'])(self.location_reply)
        bot.message_handler(commands=['start'])(self.start_reply)

        bot.callback_query_handler(func=lambda call: True)(self.callbacks_handle)

    async def _get_user_from_message(self, message):
        user_id = message.from_user.id
        return await self._get_user_from_id(user_id)

    async def callbacks_handle(self, call):
        data = call.data

        user_id = call.from_user.id
        user = await self._get_user_from_id(user_id)

        await self.user_input.forward_inline_button(user, data)

    async def location_reply(self, message):
        user = await self._get_user_from_message(message)
        location = message.location

        await user.storage.set("location", location)
        await events.geo_share(user, location)

    async def photo_reply(self, message):
        user = await self._get_user_from_message(message)
        handler = PhotoAttachmentHandler(self.bot)
        photo = await handler.from_server(message)
        await events.got_attachment(user, photo)

    async def phone_reply(self, message):
        user = await self._get_user_from_message(message)
        number = message.contact.phone_number
        logging.debug(f"Got a number! {number}")

        await user.storage.set("phone", number)
        await events.contact_share(user, number)
