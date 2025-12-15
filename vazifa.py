import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

from openai import OpenAI

import os
from dotenv import load_dotenv

load_dotenv()
API = os.getenv("API")
API_chat =os.getenv("API_chat")

client = OpenAI(
        base_url="https://api.langdock.com/openai/eu/v1",
        api_key=API_chat,
    )


dp=Dispatcher()
@dp.message(Command('start'))
async def command_start_hendler(message: Message) -> None:
    await message.answer(f"Salom, {html.bold(message.from_user.full_name)}!")

async def Chat_API(h:str="NO"):
    completion = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "user", "content": h}
        ]
    )

    return completion.choices[0].message.content

@dp.message()
async def command_start_handler(message: Message) -> None:
    try:
        h=await message.answer("🧐")
        await message.answer(f"{await Chat_API(message.text+"\nuzbekcha yubor")}")
        await h.delete()
    except:
        await message.answer ("Bunday malumot topilmadi.")
        await h.delete()

async def main() -> None:
    bot = Bot(token=API, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
