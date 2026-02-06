from aiogram import Router, F
from aiogram.filters import ExceptionTypeFilter
from exceptions import exceptions as e
from api import Api
from aiogram_i18n import I18nContext
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ErrorEvent
import models
from states import states

exceptions_router = Router()


@exceptions_router.error(
    ExceptionTypeFilter(e.UserDoesNotExistError), F.update.callback_query.as_("call")
)
async def handle_user_does_not_exist_error(
    event: ErrorEvent,
    call: CallbackQuery,
    api: Api,
    state: FSMContext,
    i18n: I18nContext,
):
    user: models.User = await api.create_user(
        call.from_user.id,
        call.from_user.username,
        call.from_user.first_name,
        # call.from_user.phone_number,
    )
    if user.is_blocked:
        await call.message.answer(
            text=user.session.reply_text,
            # parse_mode="HTML",
        )
        return
    if user.is_interviewed:
        await call.message.answer(
            text=i18n.text.already_interviewed(_path="_default.ftl"),
            # parse_mode="HTML",
        )
        return
    if not user.session.is_finished:
        questionnaire = await api.get_questionnaire(
            questionnaire_id=user.session.questionnaire,
        )
        poll = await call.message.answer_poll(
            question=questionnaire.question,
            options=[
                answer.text
                for answer in sorted(questionnaire.answers, key=lambda a: a.ordering)
            ],
            is_anonymous=False,
            type="regular",
        )
        await state.set_state(states.PollStates.waiting_for_answer)
        await state.update_data(
            poll_message_id=poll.message_id,
            poll_api_id=questionnaire.id,
        )
