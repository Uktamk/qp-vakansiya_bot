from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, StateFilter, and_f
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile
from api import Api
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram_i18n import I18nContext
from keyboards import inline_keyboard as inline
from keyboards import default_keyboard as default
from states import states
import asyncio
from config import config
import models as m

messages_router = Router()


@messages_router.message(CommandStart())
async def handle_start_cmd(
    message: Message, api: Api, i18n: I18nContext, state: FSMContext
):
    await state.clear()
    await message.answer_photo(
        photo=FSInputFile(path="assets/images/initial.png"),
        caption=i18n.text.initial.first(_path="_default.ftl"),
        reply_markup=inline.start_kb(
            i18n=i18n,
        ),
    )
    # await asyncio.sleep(3)
    # await message.answer(
    #     text=i18n.text.initial.second(_path="_default.ftl"),
    #     # reply_markup=inline.start_kb(
    #     #     i18n=i18n,
    #     # ),
    # )
    # await asyncio.sleep(3)
    # await message.answer(
    #     text=i18n.text.initial.third(_path="_default.ftl"),
    #     reply_markup=inline.start_kb(
    #         i18n=i18n,
    #     ),
    # )
    ########################### TEST
    # questionnaire = await api.get_questionnaire(questionnaire_id=1,)
    # poll = await message.answer_poll(
    #         question=questionnaire.question,
    #         options=[answer.text for answer in questionnaire.answers],
    #         is_anonymous=False,
    #         type="regular"
    #     )
    # await state.set_state(states.PollStates.waiting_for_answer)
    # await state.update_data(poll_message_id=poll.message_id,)

    # await message.answer(
    #     text="Приветственный текст и объяснение",
    #     reply_markup=inline.start_kb(
    #         i18n=i18n,
    #     ),
    # )


# @messages_router.message(F.photo)
# async def handle_photo(message: Message):
#     await message.answer(
#         text=message.photo[0].file_id,
#     )


@messages_router.message(
    F.text, and_f(StateFilter(states.PollStates.waiting_for_answer))
)
async def handle_open_ended_answer(
    message: Message, state: FSMContext, api: Api, i18n: I18nContext, bot: Bot
):
    data = await state.get_data()
    result: m.AnswerResponse = await api.create_answer(
        telegram_id=message.from_user.id,
        questionnaire_id=data["poll_api_id"],
        open_ended_answer=message.text,
        answer_id=None,
    )
    if result.status_code == "moving_to_next_question":
        new_questionnaire = await api.get_questionnaire(
            questionnaire_id=result.next_questionnaire
        )
        if new_questionnaire.is_open_ended_question:
            await bot.send_message(
                chat_id=message.from_user.id,
                text=new_questionnaire.question,
            )
            await state.set_state(states.PollStates.waiting_for_answer)
            await state.update_data(
                # poll_message_id=poll.message_id,
                poll_api_id=new_questionnaire.ordering,
            )
            return
        new_poll = await bot.send_poll(
            chat_id=message.from_user.id,
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
            poll_api_id=new_questionnaire.ordering,
        )
        return
    if result.status_code == "finished":
        await state.set_state(states.PollStates.waiting_for_portfolio)
        await message.answer(
            text=i18n.text.finished.first(_path="_default.ftl"),
        )
        return
    if result.status_code == "finished_incorrect":
        await state.clear()
        await bot.send_message(
            chat_id=message.from_user.id,
            text=result.reply_text if result.reply_text else "Вы заблокированы",
        )
        return


@messages_router.message(
    F.contact, and_f(StateFilter(states.PollStates.waiting_for_contact))
)
async def handle_contact(
    message: Message, state: FSMContext, api: Api, i18n: I18nContext
):
    await state.clear()
    result = await api.answer_post_question_2(
        telegram_id=message.contact.user_id,
        phone_number=message.contact.phone_number,
        status=True,
    )
    if result:
        await message.answer(
            text=i18n.text.finished.final(_path="_default.ftl"),
            reply_markup=ReplyKeyboardRemove(),
        )


@messages_router.message(
    F.document, and_f(StateFilter(states.PollStates.waiting_for_portfolio))
)
async def handle_document(
    message: Message, state: FSMContext, api: Api, i18n: I18nContext, bot: Bot
):
    await state.clear()
    result = await api.answer_post_question_1(
        telegram_id=message.from_user.id,
        status=True,
    )
    # result = await message.answer(
    #     text=i18n.text.finished.final(_path="_default.ftl"),
    #     reply_markup=ReplyKeyboardRemove(),
    # )
    if result:
        await state.set_state(states.PollStates.waiting_for_contact)
        await message.answer(
            text=i18n.text.finished.second(_path="_default.ftl"),
            reply_markup=default.contact_kb(i18n=i18n),
        )
        topic = await bot.create_forum_topic(
            chat_id=config.GROUP_ID,
            name=message.from_user.first_name,
        )
        await bot.send_document(
            chat_id=config.GROUP_ID,
            message_thread_id=topic.message_thread_id,
            document=message.document.file_id,
            caption=f"""
Новое портфолио 
Ссылка на пользователя: {config.BASE_URL + f"/admin/users/user/?q={message.from_user.id}"}
""",
        )
