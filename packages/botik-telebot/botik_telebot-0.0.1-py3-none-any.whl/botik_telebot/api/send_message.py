from botik.api.send_message import SendMessage
from botik_telebot.api.attachment_handlers.photo_attachment_handler import PhotoAttachmentHandler
from PIL import Image


class TgSendMessage(SendMessage):

    async def send(self, user, text, attachment=None):
        if attachment and isinstance(attachment, Image.Image):
            handler = PhotoAttachmentHandler(self.bot)
            photo = handler.to_server(attachment)
            await self.bot.send_photo(user.id, photo=photo, caption=text)
        else:
            await self.bot.send_message(user.id, text)

    async def send_with_keyboard(self, user, text, keyboard):
        markup = keyboard.get_native_markup()
        await self.bot.send_message(user.id, text, reply_markup=markup)
