from aiogram.filters.callback_data import CallbackData

class StartFactory(CallbackData, prefix="start"):
    pass

class AnswerPostFirstQuestionFactory(CallbackData, prefix="answer_1"):
    status: bool

class BlockTheBotFactory(CallbackData, prefix="block_the_bot"):
    pass