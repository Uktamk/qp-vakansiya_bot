from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram_i18n import I18nContext


def contact_kb(i18n: I18nContext) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardBuilder()
    markup.button(
        text="Отправить контакт",
        request_contact=True,
    )
    markup.adjust(1)
    return markup.as_markup(resize_keyboard=True)
