from botik.input.keyboard.markup_factory import KeyboardMarkupFactory
from botik_vkbottle.input.keyboard.keyboard_markup import VkKeyboardMarkup


class VkKeyboardMarkupFactory(KeyboardMarkupFactory):
    def create(self, **native_args):
        return VkKeyboardMarkup(self.button_factory, native_args)
