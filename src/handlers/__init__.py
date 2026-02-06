from aiogram import Router
from .callbacks import callbacks_router
from .messages import messages_router
from .exceptions import exceptions_router

router = Router()
router.include_routers(callbacks_router, messages_router, exceptions_router)
