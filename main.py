from aiogram import Bot , executor, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import  State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
bot = Bot(token='5878371934:AAEMrVRyaodCgNE8qKspLPcCS-9LEoliaBk')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
available_food_names = ['пельмени','пицца','хачапури']
available_food_sizes = ['большую','больше','ещё больше']

class OrderFood(StatesGroup):
    waitin_for_food_name = State()
    waitin_for_food_size = State()
@dp.message_handler(commands=['food'])
async def food_start(message: types.Message, state : FSMContext):
    keyboard= types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in available_food_names:
        keyboard.add(name)
    await message.answer('Выберите блюдо',reply_markup=keyboard)
    await state.set_state(OrderFood.waitin_for_food_name.state)
@dp.message_handler(state=OrderFood.waitin_for_food_name.state)
async  def food_change(message: types.Message,state : FSMContext):
    if message.text.lower() not in available_food_names:
        await message.answer('Пожалуйста выберите блюдо используя кнопки ниже')
        return
    await  state.update_data(chosen_food=message.text.lower())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for size in available_food_sizes:
        keyboard.add(size)
    await  state.set_state(OrderFood.waitin_for_food_size.state)

    await  message.answer('Теперь выберите размер блюда с низу',reply_markup=keyboard)
@dp.message_handler(state=OrderFood.waitin_for_food_size)
async  def food_size_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_food_sizes:
        await  message.answer('Пожалуйста выбери размер блюда используя кнопки ниже ')
        return
    user_data = await state.get_data()
    await message.answer(f"Вы заказали{message.text.lower()} порцию {user_data['chosen_food']}\n"
                         f"Попоробуйте заказать напитки /drinks ", reply_markup=types.ReplyKeyboardRemove())
    await  state.finish()
def register_handlers_food(dp:Dispatcher):
    dp.register_message_handler(food_start, commands="food",state='*')
    dp.register_message_handler(food_change, state=OrderFood.waitin_for_food_name)
    dp.register_message_handler(food_size_chosen, state=OrderFood.waitin_for_food_size)


@dp.message_handler()
async def cmd_text(message: types.Message):

    if message.text == "Привет":
        await  bot.send_message(message.from_user.id, "Привет, ты какое существо?")

    elif message.text == "Человек":
        await  bot.send_message(message.from_user.id, "Ясно")

    elif message.text == "Патрик":
        await  bot.send_message(message.from_user.id, "О, Привет Патрик! Как дела?")

    elif message.text == "Что ясно?":
        await  bot.send_message(message.from_user.id, "Не люблю людей")

    elif message.text == "В смысле?":
        await bot.send_photo(message.chat.id, photo='https://i.ytimg.com/vi/mf2joR532u4/maxresdefault.jpg')

    elif message.text == "Что?":
        await  bot.send_message(message.from_user.id, "Ясно")

    elif message.text == "Патрик":
        await  bot.send_message(message.from_user.id, "О, Привет Патрик! Как дела?")

    elif message.text == "Что ясно?":
        await  bot.send_message(message.from_user.id, "Не люблю людей")

    elif message.text == "В смысле?":
        await bot.send_photo(message.chat.id, photo='https://i.ytimg.com/vi/mf2joR532u4/maxresdefault.jpg')

if __name__ == '__main__':
    executor.start_polling(dp)

