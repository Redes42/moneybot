from telebot import types

from bot.callback_codec import CallbackCodec
from flow.menu import Menu
from flow.session import UserSession
from flow.stage_data import StageData
from flow.stages import InputStage, SelectStage, Stage


class FlowManager:
    def __init__(self, bot, menu: Menu):
        self.bot = bot
        self.menu = menu
        self.sessions = {}

    def get_session(self, chat_id: int):
        if chat_id not in self.sessions:
            self.sessions[chat_id] = UserSession(chat_id=chat_id, current_stage=self.menu.start_stage)
        return self.sessions[chat_id]

    def _make_stage_data(self, session: UserSession) -> StageData:
        return StageData(
            chat_id=session.chat_id,
            people=session.people,
            party=session.party,
            payload=dict(session.payload),
        )


    def open_stage(self, session: UserSession, stage: Stage) -> None:
        session.current_stage = stage

        preprocess_data = self._make_stage_data(session)
        stage.preprocess(preprocess_data)

        prompt_data = self._make_stage_data(session)
        stage.render_message(prompt_data)


    def handle_callback(self, chat_id: int, raw: str) -> None:
        session = self.get_session(chat_id)
        current_stage = session.current_stage

        stage_name, payload = CallbackCodec.decode(raw)

        data = self._make_stage_data(session)
        data.payload = payload
        current_stage.process(data)

        stage = self.menu.get_stage_by_name(stage_name)
        if stage  is not None:
            self.open_stage(session, stage)
        else:
            raise ValueError('Не указано имя стадии')

        if not isinstance(current_stage, SelectStage):
            return






    def handle_message(self, message: types.Message) -> None:
        chat_id = message.chat.id
        text = message.text

        session = self.get_session(chat_id)
        current_stage = session.current_stage

        if not isinstance(current_stage, InputStage):
            return

        data = self._make_stage_data(session)
        success = current_stage.process(data, text)
        self._apply_stage_data(session, data)

        if not success:
            return

        relation = self.menu.get_relation(current_stage)
        if relation.children:
            self.open_stage(session, relation.children[0])
