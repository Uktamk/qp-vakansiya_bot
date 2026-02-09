import json
from aiohttp import ClientSession
import models
from .endpoints import EndPoints
from exceptions import exceptions as e
import msgspec


class Api:
    def __init__(self, session: ClientSession):
        self.session = session

    async def get_user(self, telegram_id) -> models.User | None:
        async with self.session.get(
            EndPoints.CREATE_USER.value,
            params={"telegram_id": telegram_id},
        ) as response:
            if response.status == 200:
                data_byte = await response.read()
                response_model = msgspec.json.decode(data_byte, type=models.User)
                return response_model
            else:
                data = await response.json()
                # print(data)
                raise e.UserDoesNotExistError(
                    error_code=response.status,
                    message=data["message"]
                    if data.get("message", False)
                    else data["detail"],
                )

    async def get_questionnaire(self, questionnaire_id) -> models.Questionnaire | None:
        async with self.session.get(
            EndPoints.GET_QUESTIONNAIRE.value.format(questionnaire_id=questionnaire_id),
            # params={"id": questionnaire_id},
            # headers={"Authorization": "Token 123123123"},
        ) as response:
            print(await response.json())
            # print(response.headers)
            if response.status == 200:
                data_byte = await response.read()
                response_model = msgspec.json.decode(
                    data_byte, type=models.Questionnaire
                )
                return response_model
            else:
                data = await response.json()
                raise e.QuestionnaireDoesNotExist(
                    error_code=response.status,
                    message=data["message"]
                    if data.get("message", False)
                    else data["detail"],
                )

    async def create_user(
        self, telegram_id, telegram_username, first_name
    ) -> models.User | None:
        async with self.session.post(
            EndPoints.CREATE_USER.value,
            json={
                "telegram_id": telegram_id,
                "telegram_username": telegram_username if telegram_username else "Юзернейм отсутствует",
                "first_name": first_name,
                # "phone_number": phone_number,
            },
        ) as response:
            if 200 <= response.status < 300:
                data = await response.json()
                # data = {"message": "...", "ok": True, "user": {...}}

                return msgspec.convert(data["user"], type=models.User)
            else:
                data = await response.json()
                raise e.BaseApiException(
                    error_code=response.status,
                    message=data["message"]
                    if data.get("message", False)
                    else data["detail"],
                )

    async def create_answer(
        self, telegram_id: int, questionnaire_id: int, answer_id: int
    ) -> str:
        async with self.session.post(
            EndPoints.CREATE_ANSWER.value,
            json={
                "telegram_id": telegram_id,
                "questionnaire_id": questionnaire_id,
                "answer_id": answer_id,
            },
        ) as response:
            if response.status == 200:
                data_byte = await response.read()
                response_model = msgspec.json.decode(
                    data_byte, type=models.AnswerResponse
                )
                return response_model
            else:
                data = await response.json()
                raise e.BaseApiException(
                    error_code=response.status,
                    message=data["message"]
                    if data.get("message", False)
                    else data["detail"],
                )

    async def answer_post_question_1(self, telegram_id, status: bool) -> bool:
        async with self.session.post(
            EndPoints.ANSWER_POST_QUESTION_1.value,
            data={
                "telegram_id": telegram_id,
                "status": status,
            },
        ) as response:
            if response.status == 200:
                return True
            else:
                data = await response.json()
                raise e.BaseApiException(
                    error_code=response.status,
                    message=data["message"]
                    if data.get("message", False)
                    else data["detail"],
                )

    async def answer_post_question_2(
        self, telegram_id, phone_number: str | None, status: bool
    ) -> bool:
        async with self.session.post(
            EndPoints.ANSWER_POST_QUESTION_2.value,
            data={
                "telegram_id": telegram_id,
                "phone_number": phone_number,
                "status": status,
            },
        ) as response:
            if response.status == 200:
                return True
            else:
                data = await response.json()
                raise e.BaseApiException(
                    error_code=response.status,
                    message=data["message"]
                    if data.get("message", False)
                    else data["detail"],
                )
