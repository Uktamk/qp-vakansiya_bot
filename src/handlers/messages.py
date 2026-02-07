from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter, and_f
from aiogram.fsm.context import FSMContext
from api import Api
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram_i18n import I18nContext
from keyboards import inline_keyboard as inline
from states import states

messages_router = Router()


@messages_router.message(CommandStart())
async def handle_start_cmd(
    message: Message, api: Api, i18n: I18nContext, state: FSMContext
):
    await state.clear()
    await message.answer_photo(
        photo="AgACAgIAAxkBAANuaYTbZbvxjP3k6WNGAAFVZTLBTR9bAAIhDWsbN9YoSEpLBVvRDRvAAQADAgADcwADOAQ",
    )
    await message.answer(
        text=i18n.text.initial(_path="_default.ftl"),
        reply_markup=inline.start_kb(
            i18n=i18n,
        ),
    )
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
