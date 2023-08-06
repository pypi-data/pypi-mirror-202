from random import randrange

from PIL import Image
from botik.api.send_message import SendMessage
from vkbottle import PhotoMessageUploader

from botik_vkbottle.api.attachment_handlers.photo_attachment_handler import PhotoAttachmentHandler


class VkSendMessage(SendMessage):

    def __init__(self, raw_api):
        self.raw_api = raw_api
        self.photo_uploader = PhotoMessageUploader(raw_api)

    async def send(self, user, text, attachment=None):
        uid = user.id
        if attachment and isinstance(attachment, Image.Image):
            handler = PhotoAttachmentHandler()
            photo = handler.to_server(attachment)

            photo = await self.photo_uploader.upload(
                file_source=photo.read(),
                peer_id=uid,
            )
            await self.raw_api.messages.send(user_id=uid, random_id=randrange(10e10),
                                             message=text, attachment=photo)
        else:
            await self.raw_api.messages.send(user_id=uid, random_id=randrange(10e10),
                                             message=text)

    async def send_with_keyboard(self, user, text, keyboard):
        uid = user.id
        markup = keyboard.get_native_markup()
        await self.raw_api.messages.send(user_id=uid, random_id=randrange(10e10),
                                         message=text, keyboard=markup)
