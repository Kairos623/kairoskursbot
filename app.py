import asyncio
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F

API_TOKEN = '7625972697:AAHev481wOMvrYlWwmUMH1kGE7n2HlyuBpU'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


async def get_usd_rate():
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                return data['Valute']['USD']['Value']
    except (aiohttp.ClientError, KeyError):
        return None


@dp.message(Command('start'))
async def send_welcome(message: Message):
    await message.answer("Добрый день. Как вас зовут?")


@dp.message(F.text)
async def handle_name(message: Message):
    user_name = message.text
    usd_rate = await get_usd_rate()

    if usd_rate is not None:
        await message.answer(f"Рад знакомству, {user_name}! Курс доллара сегодня {usd_rate:.2f}р.")
    else:
        await message.answer(f"Рад знакомству, {user_name}! К сожалению, не удалось получить данные о курсе доллара.")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Начать заново", callback_data="restart")],
        [InlineKeyboardButton(text="Получить курс снова", callback_data="get_rate")]
    ])

    await message.answer("Что хотите сделать дальше?", reply_markup=keyboard)


@dp.callback_query(F.data == "restart")
async def handle_restart(callback_query):
    await callback_query.message.answer("Добрый день. Как вас зовут?")
    await callback_query.answer()


@dp.callback_query(F.data == "get_rate")
async def handle_get_rate(callback_query):
    usd_rate = await get_usd_rate()
    if usd_rate is not None:
        await callback_query.message.answer(f"Курс доллара сегодня {usd_rate:.2f}р.")
    else:
        await callback_query.message.answer("К сожалению, не удалось получить данные о курсе доллара.")
    await callback_query.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())