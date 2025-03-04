from config import config
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

bot: Bot = Bot(
    config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
