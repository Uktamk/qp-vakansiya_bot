from aiogram.fsm.state import StatesGroup, State

class PollStates(StatesGroup):
    # waiting_for_question = State()
    waiting_for_answer = State()
    waiting_for_contact = State()