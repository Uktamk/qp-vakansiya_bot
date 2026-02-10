from aiogram import Router, Bot
from factories import factories as f
from aiogram.types import CallbackQuery, PollAnswer
from aiogram.filters import StateFilter
from api import Api
from aiogram_i18n import I18nContext
from states import states
from exceptions import exceptions as e
from aiogram.fsm.context import FSMContext
import models
from keyboards import inline_keyboard as inline
from keyboards import default_keyboard as default

callbacks_router = Router()


@callbacks_router.callback_query(f.StartFactory.filter())
async def handle_start_factory(
    call: CallbackQuery, api: Api, i18n: I18nContext, state: FSMContext
):
    await call.answer()
    user = await api.get_user(
        telegram_id=call.from_user.id,
    )
    if user.session is None:
        raise e.UserDoesNotExistError(error_code=404, message="User does not exist")
    if user.is_blocked:
        await call.message.answer(
            text=user.session.reply_text,
            # parse_mode="HTML",
        )
        return

    if not user.session.is_finished and user.session.status == "in_progress":
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
        return
    session = user.session
    if user.is_interviewed and session.is_finished:
        # waiting_for_answer_1
        if session.status == "waiting_for_answer_1":
            await state.clear()

            text = (
                session.reply_text
                if session.reply_text
                else i18n.text.finished.first(_path="_default.ftl")
            )

            await call.message.answer(
                text=text,
                reply_markup=inline.yes_or_no_kb(i18n=i18n),
            )
            return

        # waiting_for_answer_2
        if session.status == "waiting_for_answer_2":
            await state.set_state(states.PollStates.waiting_for_contact)

            text = (
                session.reply_text
                if session.reply_text
                else i18n.text.finished.second(_path="_default.ftl")
            )

            await call.message.answer(
                text=text,
                reply_markup=default.contact_kb(i18n=i18n),
            )
            return

        # finished
        if session.status == "finished":
            text = (
                session.reply_text
                if session.reply_text
                else i18n.text.already_interviewed(_path="_default.ftl")
            )

            await call.message.answer(text=text)
            return


@callbacks_router.poll_answer(states.PollStates.waiting_for_answer)
async def handle_poll_answer(
    poll_answer: PollAnswer,
    bot: Bot,
    api: Api,
    i18n: I18nContext,
    state: FSMContext,
):
    # await call.answer()
    data = await state.get_data()
    await bot.stop_poll(
        chat_id=poll_answer.user.id,
        message_id=data["poll_message_id"],
        reply_markup=None,
    )
    result: models.AnswerResponse = await api.create_answer(
        telegram_id=poll_answer.user.id,
        questionnaire_id=data["poll_api_id"],
        answer_id=poll_answer.option_ids[0],
    )
    if result.status_code == "moving_to_next_question":
        new_questionnaire = await api.get_questionnaire(
            questionnaire_id=result.next_questionnaire
        )
        new_poll = await bot.send_poll(
            chat_id=poll_answer.user.id,
            question=new_questionnaire.question,
            options=[
                answer.text
                for answer in sorted(
                    new_questionnaire.answers,
                    key=lambda a: a.ordering,
                )
            ],
            is_anonymous=False,
            type="regular",
        )
        await state.set_state(states.PollStates.waiting_for_answer)
        await state.update_data(
            poll_message_id=new_poll.message_id,
            poll_api_id=new_questionnaire.id,
        )
        return
    if result.status_code == "finished":
        await state.clear()
        await bot.send_message(
            chat_id=poll_answer.user.id,
            text=i18n.text.finished.first(_path="_default.ftl"),
            reply_markup=inline.yes_or_no_kb(i18n=i18n),
        )
        return
    if result.status_code == "finished_incorrect":
        await state.clear()
        await bot.send_message(
            chat_id=poll_answer.user.id,
            text=result.reply_text if result.reply_text else "Вы заблокированы",
        )
        return


@callbacks_router.callback_query(f.AnswerPostFirstQuestionFactory.filter())
async def handle_first_post_question(
    call: CallbackQuery,
    callback_data: f.AnswerPostFirstQuestionFactory,
    state: FSMContext,
    api: Api,
    i18n: I18nContext,
):
    await call.answer()
    result = await api.answer_post_question_1(
        telegram_id=call.from_user.id, status=callback_data.status
    )
    if result:
        if callback_data.status:
            await state.set_state(states.PollStates.waiting_for_contact)
            await call.message.answer(
                text=i18n.text.finished.second(_path="_default.ftl"),
                reply_markup=default.contact_kb(i18n=i18n),
            )
        else:
            await state.clear()
            await call.message.answer(
                text=i18n.text.finished.cancel(_path="_default.ftl"),
                # reply_markup=inline.yes_or_no_kb(i18n=i18n),
            )


@callbacks_router.callback_query(f.BlockTheBotFactory.filter())
async def block_th_bot(
    call: CallbackQuery, callback_data: f.BlockTheBotFactory, api: Api
):
    await call.answer()
    await api.answer_post_question_2(telegram_id=call.from_user.id, status=False)
    await call.message.answer(
        text="❤️ “Qalb house”ga qiziqish bildirganingiz va e'tiboringiz uchun rahmat!"
    )
