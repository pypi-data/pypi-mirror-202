import io

from PIL import Image


class PhotoAttachmentHandler:
    def __init__(self, bot):
        self.bot = bot

    def to_server(self, photo: Image.Image):
        img_bytes = io.BytesIO()
        photo.save(img_bytes, 'JPEG', subsampling=0, quality=95)
        img_bytes.seek(0)
        return img_bytes

    async def from_server(self, message):
        file_id = message.photo[-1].file_id
        file_info = await self.bot.get_file(file_id)
        downloaded_file = await self.bot.download_file(file_info.file_path)
        return Image.open(io.BytesIO(downloaded_file))
