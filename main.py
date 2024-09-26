from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import emoji


api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

key_board = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
btn_1 = KeyboardButton(text=emoji.emojize('Рассчитать :fork_and_knife_with_plate:'))
btn_2 = KeyboardButton(text=emoji.emojize('Информация :eye:'))
btn_3 = KeyboardButton(text=emoji.emojize('Купить 💰'))
key_board.add(btn_1, btn_2, btn_3)

calculation_board = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=emoji.emojize('Рассчитать норму калорий 🧮'), callback_data='calories')],
        [InlineKeyboardButton(text='Формулы расчёта 🧙‍♀️', callback_data='formulas')]
    ]
)

buy_kb = []
for i in range(1, 5):
    buy_kb.append([InlineKeyboardButton(text=(f'Продукт{i}'), callback_data='product_buying')])
buy_board = InlineKeyboardMarkup(inline_keyboard=buy_kb)





@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=key_board)

@dp.message_handler(text=[emoji.emojize('Рассчитать :fork_and_knife_with_plate:')])
async def main_menu(message):
    await message.answer('Выбери опцию', reply_markup=calculation_board)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;\nдля женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()

@dp.message_handler(text=[emoji.emojize('Купить 💰')])
async def get_buying_list(message):
    for i in range(1, len(buy_kb)+1):
        with open(f'photos/photo{i}.jpg', "rb") as photo:
            await message.answer_photo(photo, f'Название: Product{i}| Описание: описание {i}| Цена: {i*100}')
    await message.answer('Выберите продукт для покупки:', reply_markup=buy_board)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

class UserState(StatesGroup):
    age = State()
    growth = State()
    weigth = State()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст 🎉')
    await UserState.age.set()
@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer(f'Введите свой рост 📏')
    await UserState.growth.set()
@dp.message_handler(state=UserState.growth)
async def set_weigth(message, state):
    await state.update_data(growth=message.text)
    await message.answer(f'Введите свой вес ⚖️')
    await UserState.weigth.set()
@dp.message_handler(state=UserState.weigth)
async def send_calories(message, state):
    await state.update_data(weigth=message.text)
    data = await state.get_data()
    calories_res = ((10 * int(data['weigth'])) + (6.25 * int(data['growth'])) - (5 * int(data['age'])) + 5)
    await message.answer(f'{calories_res} калорий 👍')
    await state.finish()

@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение')


if __name__=='__main__':
    executor.start_polling(dp, skip_updates=True)