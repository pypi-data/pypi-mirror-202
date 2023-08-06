from botik.api import set_api
from botik.app import App
from botik.navigation import navigator
from botik.page.page_factory import PageFactory
from botik_vkbottle.api.api import VKApi
from botik_vkbottle.input.message_handlers.raw_message_handlers import RawMessageHandlers
from botik_vkbottle.page.page_factory import VkPageFactory


class VkApp(App):
    def start(self):
        self.initialize()
        self.bot.run_forever()

    def __init__(self, bot, raw_api, start_callback=None):
        super().__init__(bot)
        self.raw_api = raw_api
        self.message_handlers = RawMessageHandlers(bot, start_callback, self.user_input)

    def initialize(self):
        api = VKApi(self.bot, self.raw_api)
        set_api(api)

        self._page_fac: PageFactory = VkPageFactory()
        navigator.initialize(self._page_fac, self.pages_data)
