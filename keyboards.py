from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


start = KeyboardButton('/start')
all_jobs = KeyboardButton('/all_jobs')
jobs_count = KeyboardButton('/jobs_count')


kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(start).row(all_jobs, jobs_count)
