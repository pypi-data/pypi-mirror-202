from vkbottle.dispatch.rules.base import GeoRule, AttachmentTypeRule

from botik.input.message_handlers.events import events
from botik.input.message_handlers.raw_message_handlers import RawMessageHandlers

from botik_vkbottle.api.attachment_handlers.photo_attachment_handler import PhotoAttachmentHandler


class RawMessageHandlers(RawMessageHandlers):
    def _initialize_handlers(self, bot):
        bot.on.private_message(AttachmentTypeRule("photo"))(self.photo_reply)
        bot.on.private_message()(self.message_reply)
        bot.on.private_message(GeoRule())(self.location_reply)
        bot.on.private_message(text=["Начать"])(self.start_reply)

        check_inline = lambda m: m.get_payload_json().get("inline", None)
        bot.on.private_message(func=check_inline)(self.callbacks_handle)

    async def _get_user_from_message(self, message):
        user_id = message.from_id
        return await self._get_user_from_id(user_id)

    async def callbacks_handle(self, call):
        data = call.get_payload_json().get("inline")

        user_id = call.from_id
        user = await self._get_user_from_id(user_id)

        await self.user_input.forward_inline_button(user, data)

    async def photo_reply(self, message):
        user = await self._get_user_from_message(message)
        handler = PhotoAttachmentHandler()
        photo = await handler.from_server(message)
        await events.got_attachment(user, photo)

    async def location_reply(self, message):
        user = await self._get_user_from_message(message)
        location = message.geo

        await user.storage.set("location", location)
        await events.geo_share(user, location)
