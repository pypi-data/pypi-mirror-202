import io

import requests
from PIL import Image


class PhotoAttachmentHandler:

    def to_server(self, photo: Image.Image):
        img_bytes = io.BytesIO()
        photo.save(img_bytes, 'JPEG', subsampling=0, quality=95)
        img_bytes.seek(0)
        return img_bytes

    async def from_server(self, message):
        url = message.attachments[0].photo.sizes[-5].url
        response = requests.get(url)
        img = Image.open(io.BytesIO(response.content))
        return img
