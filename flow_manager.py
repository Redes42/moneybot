from telebot import types

from bot import bot
from menu import MENU, SelectStage, CustomSelectStage, InputStage
from party import Party
from stages import Stages


class FlowManager:

    def process(self, message: types.Message, stage: Stages, param: int=0, got_input: bool=False):
        stage_obj = MENU[stage]
        if got_input:
            if isinstance(stage_obj, InputStage):
                no_error = stage_obj.process(message)
                if no_error:
                    self.process(message, stage_obj.child, param)
            else:
                bot.send_message(message.chat.id, text='Неизвестное сообщение')
        else:
            if isinstance(stage_obj, InputStage):
                stage_obj.preprocess(message, param)
            if isinstance(stage_obj, SelectStage | CustomSelectStage):
                stage_obj.process(message)


manager = FlowManager()