from telebot import types

from bot.callback_codec import CallbackCodec
from flow.menu import Menu
from stage_data import StageData


def create_keyboard(self,
                    message: types.Message) -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    for child in self.children:
        button = types.InlineKeyboardButton(text=MENU[child].title,
                                            callback_data=str(
                                                MENU[child].command))
        keyboard.add(button)
    if self.parent is not None:
        button = types.InlineKeyboardButton('< Назад',
                                            callback_data=self.parent)
        keyboard.add(button)
    return keyboard

class BaseKeyboardBuilder:
    def build(self, stage: "SelectStage", data: StageData) -> types.InlineKeyboardMarkup | None:
        raise NotImplementedError


class ChildrenKeyboardBuilder(BaseKeyboardBuilder):
    def build(self, stage: "SelectStage", data: StageData) -> types.InlineKeyboardMarkup | None:
        keyboard = types.InlineKeyboardMarkup()
        relation = menu.get_relation(stage)

        for child in relation.children:
            stage_name = menu.get_stage_name(child)
            keyboard.add(
                types.InlineKeyboardButton(
                    text=child.title,
                    callback_data=CallbackCodec.encode_stage(stage_name),
                )
            )

        if relation.parent:
            keyboard.add(
                types.InlineKeyboardButton(
                    text="Назад",
                    callback_data=CallbackCodec.encode_back(),
                )
            )

        return keyboard


class CustomKeyboardBuilder(BaseKeyboardBuilder):
    def __init__(self, factory: "KeyboardFactory") -> None:
        self.factory = factory

    def build(self, stage: "SelectStage", data: StageData, menu: Menu) -> types.InlineKeyboardMarkup | None:
        return self.factory(stage, data, menu)
