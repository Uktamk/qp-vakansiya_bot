from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import I18nContext
from aiogram.types import InlineKeyboardMarkup
from factories import factories as f


def start_kb(i18n: I18nContext) -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    markup.button(
        text=i18n.button.start(
            _path="_buttons.ftl",
        ),
        style="primary",
        icon_custom_emoji_id="5789901732196650829",
        callback_data=f.StartFactory().pack(),
    )
    markup.adjust(1)
    return markup.as_markup()


def yes_or_no_kb(i18n: I18nContext) -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    markup.button(
        text=i18n.button.yes(
            _path="_buttons.ftl",
        ),
        callback_data=f.AnswerPostFirstQuestionFactory(status=True).pack(),
    )
    # markup.button(
    #     text=i18n.button.no(
    #         _path="_buttons.ftl",
    #     ),
    #     callback_data=f.AnswerPostFirstQuestionFactory(status=False).pack(),
    # )
    markup.adjust(2)
    return markup.as_markup()
