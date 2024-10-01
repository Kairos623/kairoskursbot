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
    response = requests.get(url)
    data = response.json()
    return data['Valute']['USD']['Value']

@dp.message(Command('start'))
async def send_welcome(message: Message):
    await message.answer("Добрый день. Как вас зовут?")

@dp.message(F.text)
async def handle_name(message: Message):
    user_name = message.text
    usd_rate = get_usd_rate()
    await message.answer(f"Рад знакомству, {user_name}! Курс доллара сегодня {usd_rate:.2f}р.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())