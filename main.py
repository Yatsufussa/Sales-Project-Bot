import States
import database
import buttons
from aiogram import Dispatcher, Bot, executor
from aiogram.types import ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from States import *
from database import *
from buttons import *



bot = Bot("6111497813:AAFWkGgpPGDlK5LiUtA9NOgLcOBbq1d5EAE")
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=['start'],content_types=['text'])
async def start_command(message):
    start_text = f'Hello {message.from_user.first_name} Im sales bot SOJ'
    await message.answer(start_text)
    answer = message.text
    user_id = message.from_user.id
    seller = database.check_user(user_id)
    director = database.check_director(user_id)
    manager = database.check_manager(user_id)

    if seller:
        await message.answer("Choose the operation", reply_markup=buttons.sellors_main_menu_kb())

    elif director:
        await message.answer('Hello Director,Choose operation: ' ,reply_markup= buttons.directors_main_menu_kb())

    elif manager:
        await message.answer("Welcome Manager!\nWhat do you want?", reply_markup=buttons.managers_main_menu_kb())

    else:
        await message.answer("Registration\nAre you:\nSeller\nDirector\nManager\nAdmin", reply_markup=buttons.admin_kb())
        await States.AdminPanel.main_state.set()

@dp.message_handler(state= AdminPanel.main_state,content_types=['text'])
async def main_menu(message):
    # If user already registered in database so we send menu
    await message.answer("Registration\nAre you Seller or Director:", reply_markup=buttons.admin_kb())
    admin = message.text
    if admin == "Im Seller":
            await message.answer("Write your full name in one message please: ", reply_markup=ReplyKeyboardRemove())
            await SellerRegistration.get_sellers_name_state.set()

    elif admin == "Im Director,Leader":
        await message.answer("Write your full name in one message please: ", reply_markup=ReplyKeyboardRemove())
        await DirectorRegistration.get_directors_name_state.set()

    elif admin =="Im Manager":
        await message.answer('Enter Login', reply_markup=ReplyKeyboardRemove())
        login = message.text
        await message.answer('Enter Password', reply_markup=ReplyKeyboardRemove())
        password = message.text
        database.check_log(login, password)
        if True:
            await message.answer("Welcome Manager!\nWhat do you want?", reply_markup=buttons.managers_main_menu_kb())
        else:
            await message.answer('Incorrect Login or Password!', reply_markup=buttons.admin_kb())
    else:
        await message.answer("Who are u press the button", reply_markup=buttons.admin_kb())


@dp.message_handler(content_types=['text'],state = SellerRegistration.get_sellers_name_state)
async def sellers_name(message, state=SellerRegistration.get_sellers_name_state):
    sellers_name = message.text
    await state.update_data(user_name=sellers_name)
    await message.answer('Share now phone number', reply_markup=buttons.get_phone_number_kb())
    await SellerRegistration.get_sellers_phone_number_state.set()



@dp.message_handler(state=SellerRegistration.get_sellers_phone_number_state, content_types=['contact'])
async def sellers_phone(message, state=SellerRegistration.get_sellers_phone_number_state):
    sellers_phone = message.contact.phone_number
    await state.update_data(phone_number=sellers_phone)
    await message.answer('Share location of your shop now', reply_markup=buttons.location_kb())
    await SellerRegistration.get_shop_address_state.set()


@dp.message_handler(state=SellerRegistration.get_shop_address_state, content_types=['location'])
async def sellers_shop_address(message, state=SellerRegistration.get_shop_address_state):
    user_answer = message.location.latitude
    user_answer_2 = message.location.longitude

    # Временно сохраняем
    await state.update_data(latitude=user_answer, longitude=user_answer_2)

    await message.answer("Write now your TIN(INN)", reply_markup=ReplyKeyboardRemove())
    await SellerRegistration.get_sellers_TIN_state.set()


@dp.message_handler(state=SellerRegistration.get_sellers_TIN_state, content_types=['text'])
async def sellers_TIN(message, state=SellerRegistration.get_sellers_TIN_state):
    sellers_TIN = message.text
    await state.update_data(TIN = sellers_TIN)
    await message.answer("Write your Shop's name", reply_markup=ReplyKeyboardRemove())
    await SellerRegistration.get_sellers_shop_name_state.set()


@dp.message_handler(state=SellerRegistration.get_sellers_shop_name_state, content_types=['text'])
async def sellors_shop_name(message, state=SellerRegistration.get_sellers_shop_name_state):
    sellers_shop_name = message.text
    await state.update_data(shop_name = sellers_shop_name)
    await message.answer("Write ID of your manager", reply_markup=ReplyKeyboardRemove())
    await SellerRegistration.get_manager_id_state.set()


@dp.message_handler(state=SellerRegistration.get_manager_id_state, content_types=['text'])
async def seller_manager_id(message, state=SellerRegistration.get_manager_id_state):
    sellers_manager_id = message.text
    await state.update_data(manager_id = sellers_manager_id)
    await message.answer("Thanks a lot you completed Registration", reply_markup=buttons.sellors_main_menu_kb())
    all_info = await state.get_data()
    seller_name = all_info.get('user_name')
    phone_num = all_info.get('phone_number')
    latitude = all_info.get("latitude")
    longitude = all_info.get("longitude")
    INN = all_info.get('TIN')
    shop_name = all_info.get("shop_name")
    manager_id = all_info.get("manager_id")
    user_id = message.from_user.id
    database.add_seller(user_id,seller_name, phone_num, latitude, longitude, INN, shop_name, manager_id)
    await message.answer("Data accepted and collected")
    print(database.get_sellers())
    await state.finish()

@dp.message_handler(state=SellersPersonalInfo.change_data_state)
async def change_data(message,state=SellersPersonalInfo.change_data_state):
    admin = message.text
    if admin == "Change Name":
        await message.answer("Write new name: ",reply_markup=ReplyKeyboardRemove())
        await SellersPersonalInfo.change_sellers_name_state.set()

    elif admin  == 'Change phone number':
        await message.answer("Send new phone number: ",reply_markup=buttons.get_phone_number_kb())
        await SellersPersonalInfo.change_sellers_number_state.set()

    elif admin == 'Change shop address':
        await message.answer("Send new location: ",reply_markup=buttons.location_kb())
        await SellersPersonalInfo.change_sellers_addres_state.set()

    elif admin == 'Change TIN(INN)':
        await message.answer('Write new TIN(INN): ',reply_markup=ReplyKeyboardRemove())
        await SellersPersonalInfo.change_sellers_TIN_state.set()
    elif admin == 'Change shop name':
        await message.answer("Write new shops name: ",reply_markup=ReplyKeyboardRemove())
        await SellersPersonalInfo.change_sellers_ShopsName_state.set()

    else:
        await message.answer("Choose what to change")

# CHANGE DATA MESSAGE HANDLERS

@dp.message_handler(state=SellersPersonalInfo.change_sellers_name_state)
async def change_name(message,state=SellersPersonalInfo.change_sellers_name_state):
    new_name = message.text
    await state.update_data(changed_name= new_name)
    all_info = await state.get_data()
    new_name = all_info.get('changed_name')
    user_id = message.from_user.id
    database.change_name(new_name,user_id)
    await message.answer('Your name changed!',reply_markup=buttons.sellors_main_menu_kb())
    await state.finish()

@dp.message_handler(state=SellersPersonalInfo.change_sellers_number_state,content_types=['contact'])
async def chanange_phone_num(message,state=SellersPersonalInfo.change_sellers_number_state):
    new_num = message.text
    await state.update_data(new_number= new_num)
    all_info = await state.get_data()
    new_num = all_info.get('new_number')
    user_id = message.from_user.id
    database.change_phone_number(new_num,user_id)
    await message.answer('Your name changed!',reply_markup=buttons.sellors_main_menu_kb())
    await state.finish()

@dp.message_handler(state=SellersPersonalInfo.change_sellers_addres_state,content_types=['location'])
async def chanange_phone_num(message,state=SellersPersonalInfo.change_sellers_addres_state):
    user_answer = message.location.latitude
    user_answer_2 = message.location.longitude
    user_id = message.from_user.id
    await state.update_data(latitude=user_answer, longitude=user_answer_2)
    all_info = await state.get_data()
    latitude = all_info.get('latitude')
    longitude = all_info.get('longitude')
    database.change_shop_address(latitude,longitude,user_id)
    await message.answer('Location changed!',reply_markup=buttons.sellors_main_menu_kb())
    await state.finish()

@dp.message_handler(state=SellersPersonalInfo.change_sellers_TIN_state)
async def chanange_phone_num(message,state=SellersPersonalInfo.change_sellers_TIN_state):
    new_inn = message.text
    await state.update_data(new_TIN= new_inn)
    all_info = await state.get_data()
    new_inn = all_info.get('new_TIN')
    user_id = message.from_user.id
    database.change_sellers_TIN(new_inn,user_id)
    await message.answer('Your changed TIN!',reply_markup=buttons.sellors_main_menu_kb())
    await state.finish()

@dp.message_handler(state=SellersPersonalInfo.change_sellers_ShopsName_state)
async def chanange_phone_num(message,state=SellersPersonalInfo.change_sellers_ShopsName_state):
    new_sh_name = message.text
    await state.update_data(new_shop_name= new_sh_name)
    all_info = await state.get_data()
    new_sh_name = all_info.get('new_shop_name')
    user_id = message.from_user.id
    database.change_shop_name(new_sh_name,user_id)
    await message.answer('You changed Shops name!',reply_markup=buttons.sellors_main_menu_kb())
    await state.finish()

# DIrector Branch

@dp.message_handler(state=DirectorRegistration.get_directors_name_state, content_types=['text'])
async def directors_name(message, state=DirectorRegistration.get_directors_name_state):
    director_name = message.text
    await state.update_data(d_name=director_name)
    await message.answer('Share now phone number', reply_markup=buttons.get_phone_number_kb())
    await DirectorRegistration.get_directors_phone_number_state.set()

@dp.message_handler(state=DirectorRegistration.get_directors_phone_number_state, content_types=['contact'])
async def directors_phone(message, state=DirectorRegistration.get_directors_phone_number_state):
    director_phone = message.contact.phone_number
    await state.update_data(d_number=director_phone)
    await message.answer('Write your TIN', reply_markup = ReplyKeyboardRemove())
    await DirectorRegistration.get_directors_TIN_state.set()

@dp.message_handler(state=DirectorRegistration.get_directors_TIN_state, content_types=['text'])
async def directors_TIN(message, state=DirectorRegistration.get_directors_TIN_state):
    director_TIN = message.text
    await state.update_data(d_TIN = director_TIN)
    await message.answer("Write your Shop's name", reply_markup=ReplyKeyboardRemove())
    await DirectorRegistration.get_directors_shop_name_state.set()

@dp.message_handler(state=DirectorRegistration.get_directors_shop_name_state, content_types=['text'])
async def director_shop_name(message, state=DirectorRegistration.get_directors_shop_name_state):
    directors_shop_name = message.text
    await state.update_data(d_shop_name = directors_shop_name)
    await message.answer("Write ID of your manager", reply_markup=ReplyKeyboardRemove())
    await DirectorRegistration.get_manager_id_state.set()

@dp.message_handler(state=DirectorRegistration.get_manager_id_state, content_types=['text'])
async def director_manager_id(message, state=DirectorRegistration.get_manager_id_state):
    directors_manager_id = message.text
    await state.update_data(manager_id = directors_manager_id)
    await message.answer("Thanks a lot you completed Registration", reply_markup=buttons.sellors_main_menu_kb())
    all_info = await state.get_data()
    seller_name = all_info.get('d_name')
    phone_num = all_info.get('d_number')
    INN = all_info.get('d_TIN')
    shop_name = all_info.get("d_shop_name")
    manager_id = all_info.get("manager_id")
    Shop_address = 0
    user_id = message.from_user.id
    database.add_director(user_id,seller_name, phone_num,INN, shop_name, manager_id,Shop_address)
    await message.answer("Data accepted and collected")
    print(database.get_director(user_id))
    await state.finish()


# DIRECTORS CHANGE DATA BRANCH
@dp.message_handler(state=DirectorsPersonalInfo.change_data_state)
async def change_data(message,state=SellersPersonalInfo.change_data_state):
    admin = message.text
    if admin == "Change Name":
        await message.answer("Write new name: ",reply_markup=ReplyKeyboardRemove())
        await DirectorsPersonalInfo.change_directors_name_state.set()

    elif admin  == 'Change phone number':
        await message.answer("Send new phone number: ",reply_markup=buttons.get_phone_number_kb())
        await DirectorsPersonalInfo.change_directors_number_state.set()

    elif admin == 'Change TIN(INN)':
        await message.answer('Write new TIN(INN): ',reply_markup=ReplyKeyboardRemove())
        await DirectorsPersonalInfo.change_directors_TIN_state.set()

    elif admin == 'Change shop name':
        await message.answer("Write new shops name: ",reply_markup=ReplyKeyboardRemove())
        await DirectorsPersonalInfo.change_directors_ShopsName_state.set()

    else:
        await message.answer("Choose what to change")

@dp.message_handler(state=DirectorsPersonalInfo.change_directors_name_state)
async def change_name(message,state=DirectorsPersonalInfo.change_directors_name_state):
    new_name = message.text
    await state.update_data(changed_name= new_name)
    all_info = await state.get_data()
    new_name = all_info.get('changed_name')
    user_id = message.from_user.id
    database.change_d_name(new_name,user_id)
    await message.answer('Your name changed!',reply_markup=buttons.directors_main_menu_kb())
    await state.finish()

@dp.message_handler(state=DirectorsPersonalInfo.change_directors_number_state,content_types=['contact'])
async def chanange_phone_num(message,state=DirectorsPersonalInfo.change_directors_number_state):
    new_num = message.text
    await state.update_data(new_number= new_num)
    all_info = await state.get_data()
    new_num = all_info.get('new_number')
    user_id = message.from_user.id
    database.change_d_phone_number(new_num,user_id)
    await message.answer('Your name changed!',reply_markup=buttons.directors_main_menu_kb())
    await state.finish()

@dp.message_handler(state=DirectorsPersonalInfo.change_directors_TIN_state)
async def chanange_phone_num(message,state=DirectorsPersonalInfo.change_directors_TIN_state):
    new_inn = message.text
    await state.update_data(new_TIN= new_inn)
    all_info = await state.get_data()
    new_inn = all_info.get('new_TIN')
    user_id = message.from_user.id
    database.change_directors_TIN(new_inn,user_id)
    await message.answer('Your changed TIN!',reply_markup=buttons.directors_main_menu_kb())
    await state.finish()

@dp.message_handler(state=DirectorsPersonalInfo.change_directors_ShopsName_state)
async def chanange_phone_num(message,state=DirectorsPersonalInfo.change_directors_ShopsName_state):
    new_sh_name = message.text
    await state.update_data(new_shop_name= new_sh_name)
    all_info = await state.get_data()
    new_sh_name = all_info.get('new_shop_name')
    user_id = message.from_user.id
    database.change_d_shop_name(new_sh_name,user_id)
    await message.answer('You changed Shops name!',reply_markup=buttons.directors_main_menu_kb())
    await state.finish()

# Directors ADD SHOP BRANCH

@dp.message_handler(state=DirectorAddShopLocations.add_shop_state, content_types=['location'])
async def add_shops(message, state=DirectorAddShopLocations.add_shop_state):
    user_answer = message.location.latitude
    user_answer_2 = message.location.longitude
    user_id = message.from_user.id
    await state.update_data(latitude=user_answer, longitude=user_answer_2)
    all_info = await state.get_data()
    new_location = all_info.get('latitude','longitude')
    database.add_shops(new_location, user_id)
    await message.answer('Location Added!', reply_markup=buttons.directors_main_menu_kb())
    await state.finish()













@dp.message_handler(content_types=['text'])
async def sellors_all_info(message):
    user_id = message.from_user.id
    seller = database.check_user(user_id)
    director = database.check_director(user_id)
    manager = database.check_manager(user_id)
    answer = message.text


    if seller:
        if  answer == 'Personal info':
            result_answer = "Personal Info:\n"
            for i in seller:
                result_answer = f'Name: {i[1]}.\nPhone: {i[2]}.\nLocation Latitude: {i[3]}.Location Longitude: {i[4]}\nTIN: {i[5]}.\nShop name: {i[6]}'
                await message.answer(result_answer,reply_markup=buttons.sellors_main_menu_kb())
        elif answer == "Change data":
            await message.answer('What do u want to change', reply_markup=buttons.change_sellors_personal_data_kb())
            await SellersPersonalInfo.change_data_state.set()

        elif  answer == 'Tasks':
            pass
        elif  answer == 'Check download':
            pass
        elif  answer == 'Balance':
            pass
        elif  answer == 'Gifts available':
            pass
        elif  answer == 'Get the Cash':
            pass
        elif  answer == 'Knowledge Base':
            pass
        elif  answer == 'Ask a question':
            pass
        else:
            pass


    elif director:
        if  answer == 'Personal info':
            director_all_info = database.get_director(user_id)
            result_answer = "Personal Info:\n"
            for i in director_all_info:
                result_answer = f'Name: {i[1]}.\nPhone: {i[2]}.\nTIN: {i[3]}.\nShop name: {i[4]}'
                await message.answer(result_answer, reply_markup=buttons.change_personal_data_kb())

        elif answer == "Change data":
            await message.answer('What do u want to change', reply_markup=buttons.change_directors_personal_data_kb())
            await DirectorsPersonalInfo.change_data_state.set()

        elif answer == 'Tasks':
            pass

        elif answer == 'Add shop location':
            # await message.answer('Add locations of your shops: ',reply_markup=buttons.location_kb())
            # await States.DirectorAddShopLocations.add_shop_state.set()
            pass

        elif  answer == 'Balance':
            pass
        elif  answer == 'Gifts available':
            pass
        elif  answer == 'Get the Cash':
            pass
        elif  answer == 'Knowledge Base':
            pass
        elif  answer == 'Ask a question':
            pass
        else:
            await message.answer("Choose the buttonn")

    elif manager:
        if answer == 'Shop Owners':
            pass
        elif answer == 'Sellers':
            pass
        elif answer == 'Tasks':
            pass
        elif answer == 'Balance':
            pass
        elif answer == 'Gifts to change':
            pass
        elif answer == 'Chat':
            pass
        else:
            await message.answer("Choose the operation manager")


    else:
        await message.answer("Choose the button from kb")



executor.start_polling(dp)