from aiogram import Bot, Dispatcher, executor,types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

import config
import sqlite3
import logging

    #BASE FOR ALL USERS
start_connect = sqlite3.connect('users.db')
cur  = start_connect.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(
    username VARCHAR(255),
    id INTEGER,
    chat_id INTEGER
    );
    """)
start_connect.commit()

    #BASE FOR ADMINS
connect_admin = sqlite3.connect('admin.db')
curr  = connect_admin.cursor()
curr.execute("""CREATE TABLE IF NOT EXISTS admin(
    id INTEGER
    );
    """)
connect_admin.commit()

    #BASE FOR GAMERS
reg_connect = sqlite3.connect('register.db')
cur  = reg_connect.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS register_user(
    name VARCHAR(255),
    course VARCHAR(255),
    phone VARCHAR(255),
    id INTEGER
    );
    """)
reg_connect.commit()

bot = Bot(config.token)
dp = Dispatcher(bot, storage=MemoryStorage())
storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)

    #START
@dp.message_handler(commands=["start"])
async def start(message : types.Message):
    try:
        photo = open('/home/erk1nbaew/Desktop/ChessBot/photo/logo.jpg', "rb")
        cur  = start_connect.cursor()
        cur.execute(f"SELECT id FROM users WHERE  id  == {message.from_user.id};")
        result = cur.fetchall()
        if result ==[]:
            cur.execute(f"INSERT INTO users VALUES ('{message.from_user.username}', {message.from_user.id}, {message.chat.id});")
        start_connect.commit()
        await bot.send_photo(message.chat.id, photo)
        await message.answer(f"Здравстуйте ,{message.from_user.full_name}. Вас приветствует администрация Geektech.\nЕсли хотите узнать обо мне больше нажмите: /help ")
    except:
        await message.answer("Вышли не большие ошибки обратитесь тех.админу: @erk1nbaew")
        
    #HELP    
@dp.message_handler(commands="help")
async def help(message : types.Message):
    try:
        photo = open('/home/erk1nbaew/Desktop/ChessBot/photo/chess.png', "rb")
        await bot.send_photo(message.chat.id, photo)
        
        await message.answer(f"Привет👋🏼, бот был создан для турнира по шахматом.♟\nПрими участие ✅и выиграй приз 🤑💸.\n\nВот мои команды ➡️ \n1️⃣ /start - Запустить бота.\n2️⃣ /help - Информация о боте.\n3️⃣ /registration - Принять участие.\n 4️⃣ /gamers - Посмотреть список участников.")
    except:
        await message.answer("Вышли не большие ошибки обратитесь тех.админу: @erk1nbaew")

    #REGISTER
class ContactForm(StatesGroup):
    client = State()
    
@dp.message_handler(commands="registration")
async def registrate(message:types.Message):
    try:
        cur1  = reg_connect.cursor()
        cur1.execute("SELECT id FROM register_user;")
        result = cur1.fetchall()
        
        for user in result:
            print(user)
            reg_connect.commit()
        if message.from_user.id not in user:
            photo = open('/home/erk1nbaew/Desktop/ChessBot/photo/NurbolotBackend+99655800035 (1).png', "rb")
            await bot.send_photo(message.chat.id, photo)
            
            await message.answer(f"Пожалуйста заполните анкету в формате: \n Имя, Группа, Номер телефона:")
            await ContactForm.client.set()
            
        else:    
            await message.answer(f"Уважаемый {message.from_user.full_name},вы уже прошли регистрацию.")
    except:
        await message.answer("Вышли не большие ошибки обратитесь тех.админу: @erk1nbaew")
        
@dp.message_handler(state=ContactForm.client)
async def get_contact(message: types.Message, state: FSMContext):
    try:
        cur_contact = reg_connect.cursor()
        res = message.text.replace(',', '',).split()
        cur_contact = cur_contact.execute(f"INSERT INTO register_user (name, course, phone,id) VALUES ('{res[0]}', '{res[1]}', '{res[2]}',{message.from_user.id});")
        reg_connect.commit()
        await state.finish()
    except:
        await message.answer("Вышли не большие ошибки обратитесь тех.админу: @erk1nbaew")
        
    #GAMERS_LIST
@dp.message_handler(commands="gamers")
async def gamers(message:types.Message):
    try:
        await message.answer(f"Вот список игроков")
        cur_contact = reg_connect.cursor()
        cur_contact.execute(f"SELECT name FROM register_user;")
        result = cur_contact.fetchall()
        for user in result:
            res = "".join(list(str(user))).replace(",", "").replace("'", "").replace("(", "").replace(")", "").replace("[", "").replace("]", " s")
            await message.answer(f"{res}")
    except:
        await message.answer("Вышли не большие ошибки обратитесь тех.админу: @erk1nbaew")

    #ADD ADMIN
class AdminState(StatesGroup):
    admin = State()

@dp.message_handler(commands=["add_admin"])
async def start(message : types.Message):
    try:
        cur1  = connect_admin.cursor()
        cur1.execute("SELECT * FROM admin;")
        result = cur1.fetchall()
        for user in result:
            print(user)
            
        if message.from_user.id in user:
            
            await message.answer('Введите id админа: ')
            await AdminState.admin.set()
        else:
            await message.answer("У вас нет прав")
    except:
        await message.answer("Вышли не большие ошибки обратитесь тех.админу: @erk1nbaew")
        
@dp.message_handler(state=AdminState.admin)
async def admin_add(message : types.Message,state : FSMContext):
    try:
        cur1  = connect_admin.cursor()
        cur1.execute("SELECT * FROM admin;")
        result = cur1.fetchall()
        for user in result:
            print(user)
        await state.finish()
        
        if message.from_user.id in user:
            res = message.text.split()
            
            cur_admin = cur_admin.execute(f"INSERT INTO admin (id) VALUES ('{res[0]}');")
            connect_admin.commit()
            await state.finish()
        else:
            await message.answer("У вас нет прав")
    except:
        await message.answer("Произошла ошибка, повторите попытку позже")


    #MAILING
class MailingState(StatesGroup):
    mailing = State()

@dp.message_handler(commands=["mailing"])
async def mailing(message : types.Message):
    try:
        cur1  = connect_admin.cursor()
        cur1.execute("SELECT * FROM admin;")
        result = cur1.fetchall()
        for user in result:
            print(user)
        
        if message.from_user.id in user:
            
            await message.answer('Введите сообщение рассылки: ')
            await MailingState.mailing.set()
        else:
            await message.answer("У вас нет прав")
    except:
        await message.answer("Вышли не большие ошибки обратитесь тех.админу: @erk1nbaew")

@dp.message_handler(state=MailingState.mailing)
async def mailing(message : types.Message, state : FSMContext):
    try:
        
        cur = start_connect.cursor()
        cur.execute("SELECT chat_id FROM users;")
        result = cur.fetchall()
        for i in result:

            await bot.send_message(chat_id=int(i[0]), text = message.text)
        await state.finish()
    except:
        await message.answer("Произошла ошибка, повторите попытку позже")
        await state.finish()


    #RANDOM
import random


@dp.message_handler(commands="random")
async def mailing(message : types.Message, state : FSMContext):
    # try:
        cur1  = connect_admin.cursor()
        cur1.execute("SELECT * FROM admin;")
        result = cur1.fetchall()
        for user in result:
            print(user)
        
        if message.from_user.id in user:
            
            cur_contact = reg_connect.cursor()
            cur_contact.execute(f"SELECT name FROM register_user;")
            result = cur_contact.fetchall()
            
            ramdom = random.choice(result)   
                
            cur = start_connect.cursor()
            cur.execute("SELECT chat_id FROM users;")
            result = cur.fetchall()
            for i in result:

                await bot.send_message(chat_id=int(i[0]), text = ramdom)
            await state.finish()

        else:
            await message.answer("У вас нет прав")

    # except:
    #     await message.answer("Произошла ошибка, повторите попытку позже")
    #     await state.finish()
executor.start_polling(dp)