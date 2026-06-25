from telebot import types, TeleBot

from bot.log import debug, warning
from bot.safe_sender import send_safe_message
from entities.user import User
from flow.callback_codec import CallbackCodec
from db.app import Users, Persons
from entities.party import Party
from flow.menu import Menu
from flow.session import UserSession
from flow.stage_data import StageData
from flow.stages import InputStage, Stage
from logic.stage_logic import PreprocessResult


class FlowManager:
    def __init__(self, bot: TeleBot, menu: Menu):
        self.bot = bot
        self.menu = menu
        self.sessions = dict()

    @staticmethod
    def is_allowed_user(chat_id: int) -> bool:
        user_db = Users.get_user(chat_id)
        if user_db is None:
            return False
        return True

    def get_session(self, chat_id: int) -> UserSession:
        if chat_id not in self.sessions:
            self.sessions[chat_id] = UserSession(
                user=Users.get_user(chat_id),
                current_stage=self.menu.start_stage,
                party=Party(),
                people=list(Persons.get_persons(chat_id))
            )
        return self.sessions[chat_id]

    def _make_stage_data(self, session: UserSession) -> StageData:
        return StageData(
            user=session.user,
            people=session.people,
            party=session.party,
            payload=session.payload,
        )

    def open_stage(self, session: UserSession, stage: Stage) -> None:
        previous_stage = session.current_stage
        session.current_stage = stage
        stage_data = self._make_stage_data(session)
        debug(previous_stage, stage_data, f'Opening stage {stage.name}...')
        result: PreprocessResult = stage.preprocess(stage_data)
        if not result.skip_current_stage:
            data = self._make_stage_data(session)
            stage.render_message(data)
        else:
            debug(stage, stage_data, 'Skipped stage')
            self.open_stage(session, session.current_stage.default_child)

    def handle_callback(self, chat_id: int, callback_data: str) -> None:
        back = False
        session = self.get_session(chat_id)
        current_stage = session.current_stage
        data = self._make_stage_data(session)
        new_stage = self.menu.get_stage_by_name(callback_data)
        if new_stage is None:
            payload = CallbackCodec.decode_payload(callback_data)
            if payload.get('back'):
                if current_stage.parent:
                    back = True
                del payload['back']
            debug(current_stage, data, f'Got payload update from callback data = {payload}')
            data.payload.update(payload)
            debug(current_stage, data, f'Updated session payload from callback data. Payload = {data.payload}')
        if back:
            data.payload.clear()
            self.open_stage(session, current_stage.parent)
            return
        success = current_stage.process(data)
        if not success:
            return
        if current_stage.clear_payload_on_success:
            data.payload.clear()
            debug(new_stage, data, f'Payload cleared after {current_stage.name}')
        if new_stage is None:
            self.open_stage(session, current_stage.default_child)
        else:
            self.open_stage(session, new_stage)

    def handle_message(self, message: types.Message) -> None:
        chat_id = message.chat.id
        text = message.text
        session = self.get_session(chat_id)
        stage = session.current_stage
        if not isinstance(stage, InputStage):
            stage_text = (
                f'Вы сейчас находитесь на этапе "{stage.title}".\n'
                f'Воспользуйтесь инструкциями, полученными выше'
            )
            send_safe_message(
                chat_id,
                f'Неизвестное сообщение.\n{stage_text}'
            )
            warning(
                stage,
                StageData(User(chat_id)),
                f'Got unexpected input message = "{text}"')
            return
        else:
            debug(stage, StageData(User(chat_id)), f'Got input message = "{text}"')
        session.payload['value'] = text
        data = self._make_stage_data(session)
        success = stage.process(data)
        if not success:
            return
        else:
            debug(stage, data, f'Updated session payload from input. Payload = {data.payload}')
        if stage.clear_payload_on_success:
            data.payload.clear()
            debug(stage, data, f'Payload cleared after {stage.name}')
        if stage.children:
            self.open_stage(session, stage.default_child)
