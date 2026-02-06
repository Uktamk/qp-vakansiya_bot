import logging
from aiogram import Bot, Dispatcher
from aiogram_i18n import I18nMiddleware
import aiohttp
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
from handlers import router
from aiogram_i18n.cores import FluentRuntimeCore
from pathlib import Path
from api import Api, on_request_end, on_request_start
from config import TOKEN, BASE_URL


async def startup(dispatcher: Dispatcher, bot: Bot) -> None:
    i18n_middleware = I18nMiddleware(
        core=FluentRuntimeCore(path=Path(__file__).parent / "assets" / "locales" / "{locale}"),
        default_locale="uz",
    )
    i18n_middleware.setup(dispatcher=dispatcher)
    await i18n_middleware.core.startup()
    await bot.delete_webhook(drop_pending_updates=True)


async def main() -> None:
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(
        bot=bot,
        storage=MemoryStorage(),
    )
    trace_config = aiohttp.TraceConfig()
    trace_config.on_request_end.append(on_request_end)
    trace_config.on_request_start.append(on_request_start)
    api = Api(
        session=aiohttp.ClientSession(base_url=BASE_URL, trace_configs=[trace_config]),
    )
    dp["api"] = api
    dp.startup.register(startup)
    dp.include_router(router=router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())