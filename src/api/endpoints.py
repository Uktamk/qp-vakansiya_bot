from enum import Enum


class EndPoints(Enum):
    CREATE_USER = "api/v1/users/user/create/"
    GET_QUESTIONNAIRE = "api/v1/bot/questionnaires/get/{questionnaire_id}/"
    CREATE_ANSWER = "api/v1/bot/questionnaires/answer/create/"
    ANSWER_POST_QUESTION_1 = "api/v1/bot/questionnaires/answer/post_question_1/"
    ANSWER_POST_QUESTION_2 = "api/v1/bot/questionnaires/answer/post_question_2/"
