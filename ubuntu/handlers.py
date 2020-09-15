import random
from time import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, \
    CallbackQuery, Update

import states
from load_all import dp, bot
from states import Anketa


@dp.message_handler(commands=['start'])
async def start_bot(message : types.Message):
    first_name = message.from_user.first_name
    chat_id = message.from_user.id

    link = 'C:\\Users\\shake\\OneDrive\\Рабочий стол\\python\\TelegramBot2\\sticker\\'

    sleep(1)
    sti = open(link + 'sticker.webp', 'rb')
    await bot.send_sticker(chat_id=chat_id, sticker=sti)

    start_keyboardMarkup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton('Оставить заявку')
            ],
            [
                KeyboardButton('Дополнительная информация'),
                KeyboardButton('Начать заново')
            ]
        ], resize_keyboard=True
    )
    await message.answer('<b>🚀 Шалом, {username} 🚀</b>\n'
                         'Меня зовут <b>Мойша</b>. Я телеграм-бот от <a href="https://www.instagram.com/c0llege.hub/">'
                         'College hub</a>\n\n'
                         'Используйте <i>команды снизу</i> или же кнопки, которые у вас появились <i>вместо клавиатуры😚</i>'
                         '\n\n'
                         '/start - Начать заново\n'
                         '/info - Дополнительная информация\n'
                         '/search - Оставить заявку'.format(username = first_name), reply_markup=start_keyboardMarkup)

@dp.message_handler(commands=['info'])
async def info_bot(message : types.Message):
    random_number = random.randint(1, 15)
    link = 'C:\\Users\\shake\\OneDrive\\Рабочий стол\\python\\TelegramBot\\stickers\\sticker'
    sti = open(link + str(random_number) + '.webp', 'rb')

    sleep(1)
    await bot.send_sticker(message.chat.id, sti)
    await message.answer(text='<b>Ёууу, шалом ещё раз!🚀</b>\n\n'
                              'На связи <b>Шакиржан</b> - основатель College hub и создатель данного бота.\n\n'
                              'Если желаешь познакомиться или написать по поводу сотрудничества, '
                              'то не стесняйся и напиши мне👇🏻\n\n'
                              '<b>Мои контакты:(пишите лучше в инстаграм)\n\n</b>'
                              '📱Инстаграм: https://www.instagram.com/shakeszka/\n\n'
                              '📩Почта: shakeszka@gmail.com\n\n'
                              '🎆Телеграм: @shakeszka\n\n'
                              '💻ВКонтакте: https://vk.com/shakeszka\n\n\n'
                              '👇🏻👇🏻👇🏻\n'
                              '/start - Начать заново', parse_mode='html')

@dp.message_handler(commands=['search'])
async def search(message : types.Message):
    sleep(1)
    sure_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton('Да, согласен!', callback_data='yes')
            ],
            [
                InlineKeyboardButton('Нет, я передумал😅', callback_data='no')
            ]
        ]
    )

    await message.answer('Мы работаем по одному алгоритму:\n\n'
                         '✅ Получаем Вашу заявку -> ✅ Проверяем её на адекватность и достоверность -> ✅ Выкладываем в сторис\n\n'
                         'Вы уверены, что хотите оставить заявку на поиск друг а😁?', reply_markup=sure_markup)

    @dp.callback_query_handler(text='no')
    async def stop_anketa(call: CallbackQuery):
        await start_bot(message)

    @dp.callback_query_handler(text='yes')
    async def start_anketa(call : CallbackQuery, state=None):
        await message.answer('Начинаем маленький тест....')

        last_messageid = call.message.message_id + 1 # получаем последний message id

        chat_id = call.from_user.id # получаем id юзера

        user_name = call.from_user.username

        sleep(2)

        await bot.delete_message(chat_id=chat_id, message_id=last_messageid)

        await message.answer('<b>🔻Вопрос №1</b>\n\n'
                             'Как Вас зовут?')

        await Anketa.Q0.set() #Устанавливаем состояние

        # получаем ответ
        @dp.message_handler(state=Anketa.Q0)
        async def answer_q0(message: types.Message, state: FSMContext):
            answer = message.text # сохраняем ответ в variable

            # сохраняем ответ в словарь
            await state.update_data(
                {"answer0": answer}
            )

            sleep(1)
            await message.answer('<b>🔻Вопрос №2</b>\n\n'
                                 'С какого Вы города?')

            await Anketa.next()

        @dp.message_handler(state=Anketa.Q1)
        async def answer_q1(message: types.Message, state: FSMContext):
            answer = message.text  # сохраняем ответ в variable

            # сохраняем ответ в словарь
            await state.update_data(
                {"answer1": answer}
            )
            sleep(1)
            await message.answer('<b>🔻Вопрос №3</b>\n\n'
                                 'Сколько Вам лет?')

            await Anketa.next()

        @dp.message_handler(state=Anketa.Q2)
        async def answer_q2(message: types.Message, state: FSMContext):
            answer2 = message.text

            # сохраняем ответ в словарь
            await state.update_data(
                {"answer2": answer2}
            )
            sleep(1)
            await message.answer("<b>🔻Вопрос №4</b>\n\n"
                                 "С какой Вы школы?(полное название)")

            await Anketa.next()

        @dp.message_handler(state=Anketa.Q3)
        async def answer_q3(message : types.Message, state: FSMContext):
            answer3 = message.text

            # сохраняем ответ в словарь
            await state.update_data(
                {"answer3": answer3}
            )
            sleep(1)
            await message.answer('<b>🔻Вопрос №5</b>\n\n'
                                 'В каком Вы классе?')

            await Anketa.next()

        @dp.message_handler(state=Anketa.Q4)
        async def answer_q4(message: types.Message, state: FSMContext):
            answer4 = message.text

            # сохраняем ответ в словарь
            await state.update_data(
                {"answer4": answer4}
            )
            sleep(1)
            await message.answer('<b>🔻Вопрос №6</b>\n\n'
                                 'Для каких целей вы ищите напарника?🧐\n'
                                 'Например: для совместной подгтовки к SAT, для написания эссе, для реализации проекта и так далее')

            await Anketa.next()

        @dp.message_handler(state=Anketa.Q5)
        async def answer_q5(message: types.Message, state: FSMContext):
            answer5 = message.text

            # сохраняем ответ в словарь
            await state.update_data(
                {"answer5": answer5}
            )
            sleep(1)
            await message.answer('<b>🔻Вопрос №7</b>\n\n'
                                 'Напишите то, что про Вас должен знать Ваш будущий товарищ😉\n'
                                 'Расскажите немного о себе: какой Вы в плане характера и общения. Какие темы Вас интересуют?')

            await Anketa.next()

        @dp.message_handler(state=Anketa.Q6)
        async def answer_q6(message: types.Message, state: FSMContext):
            answer6 = message.text

            # сохраняем ответ в словарь
            await state.update_data(
                {"answer6": answer6}
            )
            sleep(1)
            await message.answer('<b>🔻Вопрос №8</b>\n\n'
                                 'Каким должен быть ваш будущий напарник?(возраст, характер, интересы)')

            await Anketa.next()

        @dp.message_handler(state=Anketa.Q7)
        async def answer_q7(message: types.Message, state: FSMContext):
            answer7 = message.text

            # сохраняем ответ в словарь
            await state.update_data(
                {"answer7": answer7}
            )
            sleep(1)
            await message.answer('<b>🔻Вопрос №9</b>\n\n'
                                 'Оставьте свои контакты, по которым с Вами свяжется тот самый подходящий человек😁')

            await Anketa.next()

        @dp.message_handler(state=Anketa.Q8)
        async def answer_q8(message: types.Message, state: FSMContext):
            answer8 = message.text

            await state.update_data(
                {"answer8": answer8}
            )


            await state.reset_state(with_data=False)

            finish_markup = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text='Отправить✅', callback_data='readyready')
                    ],
                    [
                        InlineKeyboardButton(text='Начать заново🔙', callback_data='nonono')
                    ]
                ]
                )
            await message.answer('Готовы подтвердить заявку?', reply_markup=finish_markup)


        @dp.callback_query_handler(text_contains='readyready')
        async def yes_send(call : CallbackQuery):
            sleep(1)
            await call.message.answer("Спасибо за отправленную заявку💚\n\n"
                                "Команда <b>College hub</b> обязательно рассмотрит её и выложит в сторис в течение <b>семи дней🍀</b>\n\n"
                                      "<i>P.S. Если хотите удалить свою заявку, то напишите @shakeszka\n\n/start - Начать заново</i>")

            data = await state.get_data()
            answer0 = data.get('answer0')
            answer1 = data.get("answer1")
            answer2 = data.get("answer2")
            answer3 = data.get("answer3")
            answer4 = data.get("answer4")
            answer5 = data.get("answer5")
            answer6 = data.get("answer6")
            answer7 = data.get("answer7")
            answer8 = data.get('answer8')

            sleep(5)
            await bot.send_message(chat_id = -1001302742821, text='<b>Заявка на поиск друга(@{username}):</b>\n\n'
                                                            '<b>Имя: </b>{q0}\n\n'
                                                            '<b>Город: </b>{q1}\n\n'
                                                            '<b>Возвраст: </b>{q2}\n\n'
                                                            '<b>Школа: </b>{q3}\n\n'
                                                            '<b>Класс: </b>{q4}\n\n'
                                                            '<b>Для чего нужен напарник: </b>{q5}\n\n'
                                                            '<b>Что про Вас должен знать Ваш будущий напарник: </b>{q6}\n\n'
                                                            '<b>Каким должен быть Ваш будущий напарник: </b>{q7}\n\n'
                                                                    '<b>Контакты: </b>{q8}'.format(
                username=user_name, q0 = answer0, q1=answer1, q2=answer2, q3=answer3, q4=answer4, q5=answer5,
                q6=answer6,q7=answer7, q8=answer8))
            await state.finish()


        @dp.callback_query_handler(text_contains='nonono')
        async def no_send(call : CallbackQuery):
            sleep(1)
            await call.message.answer("Начинаем заново)")
            await search(message)

@dp.message_handler(text='Оставить заявку')
async def search_keyboard(message : types.Message):
    await search(message)


@dp.message_handler(text='Дополнительная информация')
async def info_keyboard(message : types.Message):
    await info_bot(message)

@dp.message_handler(text='Начать заново')
async def start_keyboard(message : types.Message):
    await start_bot(message)












