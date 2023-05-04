import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InputFile

from keyboards import kb
from all_jobs import xlsx


if os.path.isfile('.env'):
    with open('.env', 'r') as file:
        content = file.read()

bot = Bot(token=content)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def start_han(message: types.Message):
    '''
    Start commands
    '''
    await message.answer('Собираю данные об актуальных работах...', reply_markup=kb)
    await message.delete()


@dp.message_handler(commands=['all_jobs'])
async def all_jobs(message: types.Message):
    '''
    Commands for parc and send all actually jobs as excel file
    '''
    'Собираю данные...'
    xlsx()
    await message.reply_document(document=InputFile("data.xlsx"))


@dp.message_handler(commands=['jobs_count'])
async def jobs_count(message: types.Message):
    '''
    Return actually jobs count
    '''
    with open('parc.json', 'r') as file:
        import json
        jobs = json.load(file)
    await message.answer(f"Количество актуальных вакансий: {len(jobs)}")


@dp.message_handler()
async def echo_ans(message: types.Message):
    '''
    Echo answer, if user write anything
    '''
    await message.reply('Я не отвечаю, нажмите на одну из кнопок...')


if __name__ == '__main__':
    print('Bot activeted')
    executor.start_polling(dispatcher=dp, skip_updates=True)
    