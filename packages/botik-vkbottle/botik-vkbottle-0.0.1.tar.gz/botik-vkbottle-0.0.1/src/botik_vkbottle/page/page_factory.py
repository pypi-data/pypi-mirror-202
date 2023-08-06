from botik.page.page_data import PageData
from botik.page.page_factory import PageFactory
from botik_vkbottle.input.keyboard.button.button_factory import VkButtonFactory
from botik_vkbottle.input.keyboard.markup_factory import VkKeyboardMarkupFactory


class VkPageFactory(PageFactory):
    def _make_dependencies(self, page_data: PageData):
        button_factory = VkButtonFactory(page_data.inline)
        self.markup_factory = VkKeyboardMarkupFactory(button_factory)
