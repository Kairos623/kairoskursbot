import requests
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F

API_TOKEN = '7625972697:AAHev481wOMvrYlWwmUMH1kGE7n2HlyuBpU'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


def get_usd_rate():
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка успешности запроса
        data = response.json()
        return data['Valute']['USD']['Value']
    except (requests.exceptions.RequestException, KeyError) as e:
        return None  # Возвращаем None, если произошла ошибка


@dp.message(Command('start'))
async def send_welcome(message: Message):
    await message.answer("Добрый день. Как вас зовут?")


@dp.message(F.text)
async def handle_name(message: Message):
    user_name = message.text
    usd_rate = get_usd_rate()

    if usd_rate is not None:
        await message.answer(f"Рад знакомству, {user_name}! Курс доллара сегодня {usd_rate:.2f}р.")
    else:
        await message.answer(f"Рад знакомству, {user_name}! К сожалению, не удалось получить данные о курсе доллара.")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())