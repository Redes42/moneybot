import ast

from telebot import types

from bot.callback_codec import CallbackCodec
from db.db import get_people
from entities.party import Party
from entities.person import Person
from flow.menu import Menu
from flow.session import UserSession
from flow.stage_data import StageData
from flow.stages import InputStage, SelectStage, Stage
from logic.stage_logic import PreprocessResult


class FlowManager:
    def __init__(self, bot, menu: Menu):
        self.bot = bot
        self.menu = menu
        self.sessions = dict()

    def get_session(self, chat_id: int):
        if chat_id not in self.sessions:
            self.sessions[chat_id] = UserSession(
                chat_id=chat_id,
                current_stage=self.menu.start_stage,
                party=Party(),
                people=get_people(chat_id)
            )
        return self.sessions[chat_id]

    def _make_stage_data(self, session: UserSession) -> StageData:
        return StageData(
            chat_id=session.chat_id,
            people=session.people,
            party=session.party,
            payload=session.payload,
        )

    def open_stage(self, session: UserSession, stage: Stage) -> None:
        session.current_stage = stage
        stage_data = self._make_stage_data(session)
        result: PreprocessResult = stage.preprocess(stage_data)
        if not result.skip_current_stage:
            prompt_data = self._make_stage_data(session)
            stage.render_message(prompt_data)
        else:
            self.open_stage(session, session.current_stage.default_child)


    def handle_callback(self, chat_id: int, callback_data: str) -> None:
        session = self.get_session(chat_id)
        current_stage = session.current_stage
        if not isinstance(current_stage, SelectStage):
            return
        data = self._make_stage_data(session)
        stage = self.menu.get_stage_by_name(callback_data)
        if stage is None:
            payload = ast.literal_eval(callback_data)
            data.payload.update(payload)
        success = current_stage.process(data)
        if not success:
            return
        if current_stage.clear_payload_on_success:
            data.payload.clear()
        if stage is not None:
            self.open_stage(session, stage)
        else:
            self.open_stage(session, current_stage.default_child)

    def handle_message(self, message: types.Message) -> None:
        chat_id = message.chat.id
        text = message.text
        session = self.get_session(chat_id)
        current_stage = session.current_stage
        if not isinstance(current_stage, InputStage):
            return
        session.payload['value'] = text
        data = self._make_stage_data(session)
        success = current_stage.process(data)
        if not success:
            return
        if current_stage.clear_payload_on_success:
            data.payload.clear()
        if current_stage.children:
            self.open_stage(session, current_stage.default_child)
