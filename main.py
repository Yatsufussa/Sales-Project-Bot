import States
import database
import buttons
from States import *
from database import *
from buttons import *
from aiogram import Dispatcher, Bot, executor
from aiogram.types import ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot("6111497813:AAFWkGgpPGDlK5LiUtA9NOgLcOBbq1d5EAE")
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=['start'],content_types=['text'])
async def start_command(message):
    start_text = f'Hello👋{message.from_user.first_name}\nIm Sales Bot SOJ'
    await message.answer(start_text)
    answer = message.text
    user_id = message.from_user.id
    seller = database.check_user(user_id)
    director = database.check_director(user_id)
    manager = database.check_manager(user_id)

    if seller:
        await message.answer("Welcome Seller.\nChoose the operation", reply_markup=buttons.sellors_main_menu_kb())

    elif director:
        await message.answer('Hello Director\nChoose the operation: ' ,reply_markup= buttons.directors_main_menu_kb())

    elif manager:
        await message.answer("Welcome Manager!\nWhat do you want?", reply_markup=buttons.managers_main_menu_kb())

    else:
        await message.answer("Registration\nWho Are You❔\nSeller🛒\nDirector🎩\nManager💻\nAdmin💎", reply_markup=buttons.admin_kb())
        await States.AdminPanel.main_state.set()


@dp.message_handler(state= AdminPanel.main_state,content_types=['text'])
async def main_menu(message):
    # If user already registered in database so we send menu
    admin = message.text
    if admin == "Im Seller":
            await message.answer("Write your full name in one message please: ", reply_markup=ReplyKeyboardRemove())
            await SellerRegistration.get_sellers_name_state.set()

    elif admin == "Im Director,Leader":
        await message.answer("Write your full name in one message please: ", reply_markup=ReplyKeyboardRemove())
        await DirectorRegistration.get_directors_name_state.set()

    elif admin =="Im Manager":
        await message.answer("Enter Login pls",reply_markup=ReplyKeyboardRemove())
        await CheckManager.login_state.set()
    elif admin == "Im Admin":
        await message.answer("Enter Login pls",reply_markup=ReplyKeyboardRemove())
        await CheckAdmin.login_state.set()
    else:
        await message.answer("Who are u press the button❓", reply_markup=buttons.admin_kb())

# MANAGERS SECURITY LOGIN
@dp.message_handler(state=CheckManager.login_state)
async def log(message,state = CheckManager.login_state):
     login = message.text
     if database.check_log(login):
         await message.answer("Correct login!✔️\nEnter password now: ",reply_markup=ReplyKeyboardRemove())
         await CheckManager.password_state.set()
     else:
        await message.answer("Incorrect choose the button!🚫 ",reply_markup=admin_kb())
        await AdminPanel.main_state.set()

@dp.message_handler(state=CheckManager.password_state)
async def log(message,state = CheckManager.password_state):
     password = message.text
     if database.check_pas(password):
         await message.answer("Verified Succesfully!✔️\nChoose operations: ",reply_markup=buttons.managers_main_menu_kb())
         user_id = message.from_user.id
         database.add_manager(user_id,password)
         await state.finish()
     else:
        await message.answer("Incorrect choose the button! 🚫",reply_markup=admin_kb())
        await AdminPanel.main_state.set()


# CHECK ADMINS PASSWORD AND LOGIN
@dp.message_handler(state=CheckAdmin.login_state)
async def log_a(message, state=CheckAdmin.login_state):
    login = message.text
    if database.check_a_log(login):
        await message.answer("Correct login!✔️\nEnter password now: ", reply_markup=ReplyKeyboardRemove())
        await CheckAdmin.password_state.set()
    else:
        await message.answer("Incorrect choose the button!🚫 ", reply_markup=admin_kb())
        await AdminPanel.main_state.set()

@dp.message_handler(state=CheckAdmin.password_state)
async def pas_a(message, state=CheckAdmin.password_state):
    password = message.text
    if database.check_a_pas(password):
        await message.answer("Verified Succesfully!✔️\nChoose operations: ", reply_markup=buttons.admin_main_menu_kb())
        user_id = message.from_user.id
        database.add_admin(user_id)
        await state.finish()
    else:
        await message.answer("Incorrect choose the button! 🚫", reply_markup=admin_kb())
        await AdminPanel.main_state.set()


# SELLER REGISTRATION BRANCH
@dp.message_handler(content_types=['text'],state = SellerRegistration.get_sellers_name_state)
async def sellers_name(message, state=SellerRegistration.get_sellers_name_state):
    sellers_name = message.text
    await state.update_data(user_name=sellers_name)
    await message.answer('Share now phone number📲', reply_markup=buttons.get_phone_number_kb())
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
    tasks = "No Task yet"
    await state.update_data(tasks = "No Task yet")
    user_id = message.from_user.id
    database.add_seller(user_id,seller_name, phone_num, latitude, longitude, INN, shop_name, manager_id,tasks)
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
        await message.answer("Send new phone number: 📲",reply_markup=buttons.get_phone_number_kb())
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
    await message.answer('Your name changed!✔️',reply_markup=buttons.sellors_main_menu_kb())
    await state.finish()

@dp.message_handler(state=SellersPersonalInfo.change_sellers_number_state,content_types=['contact'])
async def chanange_phone_num(message,state=SellersPersonalInfo.change_sellers_number_state):
    new_num = message.text
    await state.update_data(new_number= new_num)
    all_info = await state.get_data()
    new_num = all_info.get('new_number')
    user_id = message.from_user.id
    database.change_phone_number(new_num,user_id)
    await message.answer('Your number changed!📲',reply_markup=buttons.sellors_main_menu_kb())
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
    await message.answer('Location changed!✔️',reply_markup=buttons.sellors_main_menu_kb())
    await state.finish()

@dp.message_handler(state=SellersPersonalInfo.change_sellers_TIN_state)
async def chanange_phone_num(message,state=SellersPersonalInfo.change_sellers_TIN_state):
    new_inn = message.text
    await state.update_data(new_TIN= new_inn)
    all_info = await state.get_data()
    new_inn = all_info.get('new_TIN')
    user_id = message.from_user.id
    database.change_sellers_TIN(new_inn,user_id)
    await message.answer('Your changed TIN!✔️',reply_markup=buttons.sellors_main_menu_kb())
    await state.finish()

@dp.message_handler(state=SellersPersonalInfo.change_sellers_ShopsName_state)
async def chanange_phone_num(message,state=SellersPersonalInfo.change_sellers_ShopsName_state):
    new_sh_name = message.text
    await state.update_data(new_shop_name= new_sh_name)
    all_info = await state.get_data()
    new_sh_name = all_info.get('new_shop_name')
    user_id = message.from_user.id
    database.change_shop_name(new_sh_name,user_id)
    await message.answer('You changed Shops name!✔️',reply_markup=buttons.sellors_main_menu_kb())
    await state.finish()

# DIrector Branch

@dp.message_handler(state=DirectorRegistration.get_directors_name_state, content_types=['text'])
async def directors_name(message, state=DirectorRegistration.get_directors_name_state):
    director_name = message.text
    await state.update_data(d_name=director_name)
    await message.answer('Share now phone number 📲', reply_markup=buttons.get_phone_number_kb())
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
    await state.update_data(d_manager_id = directors_manager_id)
    await message.answer("Thanks a lot you completed Registration", reply_markup=buttons.directors_main_menu_kb())
    all_info = await state.get_data()
    directors_name = all_info.get('d_name')
    phone_num = all_info.get('d_number')
    INN = all_info.get('d_TIN')
    shop_name = all_info.get("d_shop_name")
    manager_id = all_info.get("d_manager_id")
    latitude = 0
    longitude = 0
    tasks = "No Task yet"
    director_id = message.from_user.id
    await state.update_data(d_user_id=director_id)
    database.add_director(director_id,directors_name, phone_num,INN, shop_name, manager_id,latitude,longitude,tasks)
    await message.answer("Data accepted and collected")
    await state.finish()


# DIRECTORS CHANGE DATA BRANCH
@dp.message_handler(state=DirectorsPersonalInfo.change_data_state)
async def change_data(message,state=DirectorsPersonalInfo.change_data_state):
    admin = message.text
    if admin == "Change Name":
        await message.answer("Write new name: ",reply_markup=ReplyKeyboardRemove())
        await DirectorsPersonalInfo.change_directors_name_state.set()

    elif admin  == 'Change phone number':
        await message.answer("Send new phone number:📲 ",reply_markup=buttons.get_phone_number_kb())
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
    await message.answer('Your name changed!✔️',reply_markup=buttons.directors_main_menu_kb())
    await state.finish()

@dp.message_handler(state=DirectorsPersonalInfo.change_directors_number_state,content_types=['contact'])
async def chanange_phone_num(message,state=DirectorsPersonalInfo.change_directors_number_state):
    new_num = message.text
    await state.update_data(new_number= new_num)
    all_info = await state.get_data()
    new_num = all_info.get('new_number')
    user_id = message.from_user.id
    database.change_d_phone_number(new_num,user_id)
    await message.answer('Your number changed!📲v',reply_markup=buttons.directors_main_menu_kb())
    await state.finish()

@dp.message_handler(state=DirectorsPersonalInfo.change_directors_TIN_state)
async def chanange_phone_num(message,state=DirectorsPersonalInfo.change_directors_TIN_state):
    new_inn = message.text
    await state.update_data(new_TIN= new_inn)
    all_info = await state.get_data()
    new_inn = all_info.get('new_TIN')
    user_id = message.from_user.id
    database.change_directors_TIN(new_inn,user_id)
    await message.answer('Your changed TIN!✔️',reply_markup=buttons.directors_main_menu_kb())
    await state.finish()

@dp.message_handler(state=DirectorsPersonalInfo.change_directors_ShopsName_state)
async def chanange_phone_num(message,state=DirectorsPersonalInfo.change_directors_ShopsName_state):
    new_sh_name = message.text
    await state.update_data(new_shop_name= new_sh_name)
    all_info = await state.get_data()
    new_sh_name = all_info.get('new_shop_name')
    user_id = message.from_user.id
    database.change_d_shop_name(new_sh_name,user_id)
    await message.answer('You changed Shops name!✔️',reply_markup=buttons.directors_main_menu_kb())
    await state.finish()



# Directors ADD SHOP BRANCH



@dp.message_handler(state=DirectorAddShopLocations.add_shop_state, content_types=['location'])
async def add_shops(message, state=DirectorAddShopLocations.add_shop_state):
    all_info = await state.get_data()
    directors_name = all_info.get('d_name')
    phone_num = all_info.get('d_number')
    INN = all_info.get('d_TIN')
    shop_name = all_info.get("d_shop_name")
    manager_id = all_info.get("d_manager_id")
    user_answer1 = message.location.latitude
    user_answer2 = message.location.longitude
    await state.update_data(latitude=user_answer1, longitude=user_answer2)
    all_info = await state.get_data()
    latitude = all_info.get('latitude')
    longitude = all_info.get('longitude')
    tasks = "No Task yet"
    user_id = message.from_user.id
    database.add_shops(user_id, directors_name, phone_num, INN, shop_name, manager_id, latitude, longitude,tasks)
    await message.answer('Location Added!', reply_markup=buttons.directors_main_menu_kb())
    await state.finish()





# Managers Shop owners branch # FOR DIRECTOR DONE



@dp.message_handler(state=ShopOwnerM.shop_owners_state)
async def shop_own(message,state=ShopOwnerM.shop_owners_state):
    manager_id = message.text
    await state.update_data(d_manager_id=manager_id)
    director = database.get_shop_d_owners(manager_id)
    owner_info = "Owners Personal Info\nDirector:\n"
    for i in director:
        owner_info = f'Name: {i[1]}.\nPhone: {i[2]}.\nTIN: {i[3]}.\nShop name: {i[5]}.\nShop latitude: {i[7]}\nShop longitude: {i[8]}.'
        await message.answer(owner_info)
        await message.answer("Choose operation",reply_markup=buttons.shop_owner_kb())
        await ShopOwnerM.change_shop_info_state.set()

@dp.message_handler(state=ShopOwnerM.change_shop_info_state)
async def change_data_menu(message,state=ShopOwnerM.change_shop_info_state):
    action = message.text
    if action == 'Add new shop loc.':
        await message.answer("Share your location pls.\nPress the button.",reply_markup=buttons.location_kb())
        await ShopOwnerM.m_add_d_shop_state.set()

    elif action == 'Change Director info':
        await message.answer('What do u want to change',reply_markup=managers_change_owner_data_kb())
        await ShopOwnerM.change_data_state.set()

    elif action == 'Balance':
        pass

    elif action == 'Tasks':
         task = database.get_d_task()
         await message.answer(f"Your Task:\n{task}",reply_markup=buttons.managers_main_menu_kb())
         await state.finish()

    elif action == 'Back':
        await message.answer("Manager's main menu",reply_markup=buttons.managers_main_menu_kb())
        await state.finish()

# Managers Change Director Info Branch
@dp.message_handler(state=ShopOwnerM.change_data_state)
async def change_shop_info(message,state=ShopOwnerM.change_data_state):
    action = message.text

    if message.text == "Change Shop address":
        await message.answer("Send new location",reply_markup=buttons.location_kb())
        await ShopOwnerM.change_shop_loc_state.set()

    elif message.text == "Change Shop name":
        await message.answer("Write new shop name: ")
        await ShopOwnerM.change_shop_name_state.set()

    elif message.text == "Change Directors name":
        await message.answer("Write new name: ",reply_markup=ReplyKeyboardRemove())
        await ShopOwnerM.change_directors_name_state.set()

    elif message.text == "Change Directors phone 📲":
        await message.answer("Write new name: ",reply_markup=buttons.get_phone_number_kb())
        await ShopOwnerM.change_directors_phone_state.set()

    elif message.text == "Change Directors TIN":
        await message.answer("Write new TIN(INN): ", reply_markup=ReplyKeyboardRemove())
        await ShopOwnerM.change_directors_TIN_state.set()

    else:
        await message.answer('Choose what to change')

@dp.message_handler(state=ShopOwnerM.change_shop_loc_state,content_types=['location'])
async def m_change_d_shop_loc(message,state= ShopOwnerM.change_shop_loc_state):
    latitude = message.location.latitude
    longitude = message.location.longitude
    all_info = await state.get_data()
    manager_id = all_info.get('d_manager_id')
    database.m_change_d_shop_loc(latitude, longitude, manager_id)
    await message.answer('Location changed!✔️', reply_markup=buttons.shop_owner_kb())
    await ShopOwnerM.change_shop_info_state.set()

#Change directors shop name from manager
@dp.message_handler(state=ShopOwnerM.change_shop_name_state)
async def m_change_d_shop_loc(message, state=ShopOwnerM.change_shop_name_state):
    all_info = await state.get_data()
    manager_id = all_info.get('d_manager_id')
    new_shop_name = message.text
    database.m_change_d_shop_name(new_shop_name, manager_id)
    await message.answer("ShopName changed!✔️", reply_markup=buttons.shop_owner_kb())
    await ShopOwnerM.change_shop_info_state.set()


@dp.message_handler(state=ShopOwnerM.change_directors_name_state)
async def m_change_d_name(message,state=ShopOwnerM.change_directors_name_state):
    all_info = await state.get_data()
    manager_id = all_info.get('d_manager_id')
    directors_name = message.text
    database.m_change_d_name(directors_name,manager_id)
    await message.answer("Director's name changed!✔️", reply_markup=buttons.shop_owner_kb())
    await ShopOwnerM.change_shop_info_state.set()

@dp.message_handler(state=ShopOwnerM.change_directors_phone_state,content_types=['contact'])
async def m_change_d_phone(message,state=ShopOwnerM.change_directors_phone_state):
    all_info = await state.get_data()
    manager_id = all_info.get('d_manager_id')
    phone_num = message.contact.phone_number
    database.m_change_d_phone(phone_num,manager_id)
    await message.answer('Phone number changed! 📲', reply_markup=buttons.shop_owner_kb())
    await ShopOwnerM.change_shop_info_state.set()

@dp.message_handler(state=ShopOwnerM.change_directors_TIN_state)
async def m_change_d_phone(message,state=ShopOwnerM.change_directors_TIN_state):
    all_info = await state.get_data()
    manager_id = all_info.get('d_manager_id')
    INN = message.text               #TIN
    database.m_change_d_TIN(INN,manager_id)
    await message.answer('TIN changed!✔️', reply_markup=buttons.shop_owner_kb())
    await ShopOwnerM.change_shop_info_state.set()


# Add Shop to director state from manager

@dp.message_handler(state=ShopOwnerM.m_add_d_shop_state,content_types=['location'])
async def m_add_shop(message,state = ShopOwnerM.m_add_d_shop_state):
    all_info = await state.get_data()
    latitude = message.location.latitude
    longitude = message.location.longitude
    manager_id = all_info.get('d_manager_id')
    user_id = all_info.get('d_user_id')
    directors_name = all_info.get('d_name')
    phone_num = all_info.get('d_number')
    INN = all_info.get('d_TIN')
    shop_name = all_info.get("d_shop_name")
    manager_id = all_info.get("d_manager_id")
    tasks = "No Task yet"
    database.add_shops(user_id, directors_name, phone_num, INN, shop_name, manager_id, latitude, longitude,tasks)
    await message.answer('Location Updated!✔️', reply_markup=buttons.shop_owner_kb())
    await ShopOwnerM.change_shop_info_state.set()

# List of only directors shops location not working

# @dp.message_handler(state=ShopOwnerM.list_of_shops_state)
# async def Shop_List(message,state=ShopOwnerM.list_of_shops_state):
#     await message.answer('Hello fr')
#     all_info = await state.get_data()
#     manager_id = all_info.get('d_manager_id')
#     print(manager_id)
#     shops = database.get_shop_d_locations(manager_id)
#     # Проверка есть ли вообще что-то в базе
#     if shops:
#         # Формируем сообщение
#         result_answer = 'Location Coordinates: \n'
#
#         for i in shops:
#             result_answer = f'Shop Locations\nLatitude and Longitude:\n{i[0]},{i[1]}'
#
#         await message.answer(result_answer, 'Write what do u want to change?',
#                              reply_markup=buttons.managers_change_owner_data_kb())
#         str(print(i[0], i[1]))
#         await ShopOwnerM.change_shop_info_state.set()
#
#     else:
#         await message.answer('Director has no shops')

# MANAGERS BRANCH SELLERS
@dp.message_handler(state=MSeller.m_main_seller_state)
async def m_main_seller(message,state=MSeller.m_main_seller_state):
    manager_id = message.text
    await state.update_data(s_manager_id=manager_id)
    seller = database.get_shop_s_owners(manager_id)
    owner_info = "Owners Personal Info\nSellers:\n"
    if seller:
        for i in seller:
            owner_info = f'Name: {i[1]}.\nPhone: {i[2]}.\nShop_lat.: {i[3]}.\nShop_long: {i[4]}.\nTIN(INN): {i[5]}\nShop name: {i[6]}.'
            await message.answer(owner_info)
            await message.answer("Choose operation",reply_markup=buttons.managers_main_seller_menu_kb())
            await MSeller.sellers_state.set()
    else:
        await message.answer(f'No such seller with {manager_id}manager ID',reply_markup=managers_main_menu_kb())
        await state.finish()

# Managers Change Seller Data Branch
@dp.message_handler(state=MSeller.sellers_state)
async def seller_main(message,state = MSeller.sellers_state):
    action = message.text
    if action == "Change Sellers Info":
        await message.answer('What do you want to change: ',reply_markup=buttons.managers_change_seller_data_kb())
        await MSeller.change_seller_info_state.set()

    elif action == "Seller Balance":
        pass

    elif action == "Seller's Tasks":
        task = database.get_s_task()
        await message.answer(f"Your Task:\n{task}", reply_markup=buttons.managers_main_menu_kb())
        await state.finish()

    elif action == "Seller's Checks":
        pass

    elif action == "Back":
        await message.answer("Manager's main menu", reply_markup=buttons.managers_main_menu_kb())
        await state.finish()

    else:
        await message.answer("Press the button to change",reply_markup=buttons.managers_change_seller_data_kb())

@dp.message_handler(state=MSeller.change_seller_info_state)
async def m_change_s_info(message,state = MSeller.change_seller_info_state):
    action = message.text
    if action == "Change Shop address":
        await message.answer("Send new address" ,reply_markup=buttons.location_kb())
        await MSeller.change_shop_loc_state.set()

    elif action == "Change Shop name":
        await message.answer("Write new name: ", reply_markup=ReplyKeyboardRemove())
        await MSeller.change_shop_name_state.set()

    elif action == "Change Seller's name":
        await message.answer("Write new name: ", reply_markup=ReplyKeyboardRemove())
        await MSeller.change_sellers_name_state.set()

    elif action == "Change Seller's phone":
        await message.answer("Send new contact 📲", reply_markup=buttons.get_phone_number_kb())
        await MSeller.change_sellers_phone_state.set()

    elif action == "Change Seller's TIN":
        await message.answer("Write new TIN(INN)", reply_markup=ReplyKeyboardRemove())
        await MSeller.change_sellers_TIN_state.set()

@dp.message_handler(state=MSeller.change_shop_loc_state,content_types=['location'])
async def m_change_d_shop_loc(message,state= MSeller.change_shop_loc_state):
    latitude = message.location.latitude
    longitude = message.location.longitude
    all_info = await state.get_data()
    manager_id = all_info.get('s_manager_id')
    database.m_change_s_shop_loc(latitude, longitude, manager_id)
    await message.answer('Location changed!', reply_markup=buttons.managers_main_seller_menu_kb())
    await MSeller.sellers_state.set()

#Change directors shop name from manager
@dp.message_handler(state= MSeller.change_shop_name_state,content_types=['text'])
async def m_change_d_shop_loc(message, state= MSeller.change_shop_name_state):
    all_info = await state.get_data()
    manager_id = all_info.get('s_manager_id')
    new_shop_name = message.text
    database.m_change_s_shop_name(new_shop_name, manager_id)
    await message.answer("ShopName changed!✔️", reply_markup=buttons.managers_main_seller_menu_kb())
    await MSeller.sellers_state.set()


@dp.message_handler(state= MSeller.change_sellers_name_state,content_types=['text'])
async def m_change_d_name(message,state= MSeller.change_sellers_name_state):
    all_info = await state.get_data()
    manager_id = all_info.get('s_manager_id')
    seller_name = message.text
    database.m_change_s_name(seller_name,manager_id)
    await message.answer("Seller's name changed!✔️", reply_markup=buttons.managers_main_seller_menu_kb())
    await MSeller.sellers_state.set()

@dp.message_handler(state=MSeller.change_sellers_phone_state,content_types=['contact'])
async def m_change_d_phone(message,state=MSeller.change_sellers_phone_state):
    all_info = await state.get_data()
    manager_id = all_info.get('s_manager_id')
    phone_num = message.contact.phone_number
    database.m_change_s_phone(phone_num,manager_id)
    await message.answer('Phone number changed! 📲', reply_markup=buttons.managers_main_seller_menu_kb())
    await MSeller.sellers_state.set()

@dp.message_handler(state= MSeller.change_sellers_TIN_state)
async def m_change_d_phone(message,state= MSeller.change_sellers_TIN_state):
    all_info = await state.get_data()
    manager_id = all_info.get('s_manager_id')
    INN = message.text                 #TIN
    database.m_change_s_TIN(INN,manager_id)
    await message.answer('TIN changed!✔️', reply_markup=buttons.managers_main_seller_menu_kb())
    await MSeller.sellers_state.set()


# managers Tasks Branch
@dp.message_handler(state=Tasks.main_tasks_state)
async def main_tasks(message,state = Tasks.main_tasks_state):

    if message.text =="Director's Tasks":
        await message.answer("Director's\nAdd Tasks or Change Tasks?",reply_markup=buttons.directors_tasks_kb())
        await Tasks.d_tasks.set()

    elif message.text =="Seller's Tasks":
        await message.answer("Seller's\nAdd Tasks or Change Tasks?",reply_markup=buttons.sellers_tasks_kb())
        await Tasks.s_tasks.set()

    elif message.text == 'Back':
        await message.answer("Manager's main menu",reply_markup=buttons.managers_main_menu_kb())
        await state.finish()

    else:
        await message.answer("Choose the button to change ",reply_markup=buttons.managers_tasks_kb())


# CHange tasks menu for Directors And Sellers

@dp.message_handler(state=Tasks.d_tasks)
async def D_task(message,state= Tasks.d_tasks):
    action = message.text
    if action == "Add Task":
        await message.answer("Write new Task",reply_markup=ReplyKeyboardRemove())
        await Tasks.add_d_tasks.set()

    elif action == "Change Task":
        await message.answer("Write Updated Task",reply_markup=ReplyKeyboardRemove())
        await Tasks.add_d_tasks.set()

    elif action == "Delete Task":
        await message.answer("Task deleted",reply_markup=buttons.managers_main_menu_kb())
        await Tasks.delete_d_task.set()

    elif action == "Back":
        await message.answer("Manager's main menu",reply_markup=buttons.managers_main_menu_kb())
        await state.finish()

    else:
        await message.answer("Choose the button")


@dp.message_handler(state=Tasks.s_tasks)
async def D_task(message, state=Tasks.s_tasks):
    if message.text == "Add Task":
        await message.answer("Write new Task 💬", reply_markup=ReplyKeyboardRemove())
        await Tasks.add_s_tasks.set()

    elif message.text == "Change Task":
        await message.answer("Write Updated Task 📜", reply_markup=ReplyKeyboardRemove())
        await Tasks.add_s_tasks.set()

    elif message.text == "Delete Task 🗑":
        await message.answer("Task deleted",reply_markup=buttons.managers_main_menu_kb())
        await Tasks.delete_s_task.set()

    elif message.text == "Back":
        await message.answer("Manager's main menu", reply_markup=buttons.managers_main_menu_kb())
        await state.finish()

    else:
        await message.answer("Choose the button")


@dp.message_handler(state=Tasks.add_d_tasks)
async def add_d_task(message,state=Tasks.add_d_tasks):
    TASKS = message.text
    await message.answer("Task added 💬", reply_markup = buttons.managers_tasks_kb())
    database.d_add_task(TASKS)
    await Tasks.main_tasks_state.set()

@dp.message_handler(state=Tasks.change_d_tasks)
async def add_d_task(message, state=Tasks.change_d_tasks):
    TASKS = message.text
    database.d_update_task(TASKS)
    await message.answer("Task Changed 📜", reply_markup=buttons.managers_tasks_kb())
    await Tasks.main_tasks_state.set()


@dp.message_handler(state=Tasks.delete_d_tasks)
async def add_d_task(message,state=Tasks.delete_d_tasks):
    database.d_delete_task()
    await message.answer("Task's Deleted 🗑", reply_markup=buttons.managers_tasks_kb())
    awaitTasks.main_tasks_state.set()


@dp.message_handler(state=Tasks.add_s_tasks)
async def add_d_task(message,state= Tasks.add_s_tasks):
    TASKS = message.text
    database.s_add_task(TASKS)
    await message.answer("Task added 💬", reply_markup=buttons.managers_tasks_kb())
    await Tasks.main_tasks_state.set()


@dp.message_handler(state=Tasks.change_s_tasks)
async def add_d_task(message, state=Tasks.change_s_tasks):
    TASKS = message.text
    database.s_update_task(TASKS)
    await message.answer("Task Changed 📜", reply_markup=buttons.managers_tasks_kb())
    await Tasks.main_tasks_state.set()


@dp.message_handler(state=Tasks.add_s_tasks)
async def add_d_task(message,state= Tasks.add_s_tasks):
    database.s_delete_task()
    await message.answer("Tasks Deleted 🗑", reply_markup=buttons.managers_tasks_kb())
    await Tasks.main_tasks_state.set()





# Admins Director Branch




@dp.message_handler(state=AdminShopOwnerM.shop_owners_state)
async def shop_own(message,state=AdminShopOwnerM.shop_owners_state):
    manager_id = message.text
    await state.update_data(d_manager_id=manager_id)
    director = database.get_shop_d_owners(manager_id)
    owner_info = "Owners Personal Info\nDirector:\n"
    for i in director:
        owner_info = f'Name: {i[1]}.\nPhone: {i[2]}.\nTIN: {i[3]}.\nShop name: {i[5]}.\nShop latitude: {i[-2]}\nShop longitude: {i[-1]}.'
        await message.answer(owner_info)
        await message.answer("Choose operation",reply_markup=buttons.shop_owner_kb())
        await AdminShopOwnerM.change_shop_info_state.set()

@dp.message_handler(state=AdminShopOwnerM.change_shop_info_state)
async def change_data_menu(message,state=AdminShopOwnerM.change_shop_info_state):
    action = message.text
    if action == 'Add new shop loc.':
        await message.answer("Share your location pls.\nPress the button.",reply_markup=buttons.location_kb())
        await AdminShopOwnerM.m_add_d_shop_state.set()

    elif action == 'Change Director info':
        await message.answer('What do u want to change⚙️',reply_markup=managers_change_owner_data_kb())
        await AdminShopOwnerM.change_data_state.set()

    elif action == 'Balance':
        pass

    elif action == 'Tasks':
      pass

    elif action == 'Back':
        await message.answer("Admin's main menu",reply_markup=buttons.managers_main_menu_kb())
        await state.finish()

# Admins Change Director Info Branch
@dp.message_handler(state=AdminShopOwnerM.change_data_state)
async def change_shop_info(message,state=AdminShopOwnerM.change_data_state):
    action = message.text

    if message.text == "Change Shop address":
        await message.answer("Send new location",reply_markup=buttons.location_kb())
        await AdminShopOwnerM.change_shop_loc_state.set()

    elif message.text == "Change Shop name":
        await message.answer("Write new shop name: ")
        await AdminShopOwnerM.change_shop_name_state.set()

    elif message.text == "Change Directors name":
        await message.answer("Write new name: ",reply_markup=ReplyKeyboardRemove())
        await AdminShopOwnerM.change_directors_name_state.set()

    elif message.text == "Change Directors phone":
        await message.answer("Share number:📲 ",reply_markup=buttons.get_phone_number_kb())
        await AdminShopOwnerM.change_directors_phone_state.set()

    elif message.text == "Change Directors TIN":
        await message.answer("Write new TIN(INN): ", reply_markup=ReplyKeyboardRemove())
        await AdminShopOwnerM.change_directors_TIN_state.set()

    else:
        await message.answer('Choose what to change')

@dp.message_handler(state=AdminShopOwnerM.change_shop_loc_state,content_types=['location'])
async def m_change_d_shop_loc(message,state= AdminShopOwnerM.change_shop_loc_state):
    latitude = message.location.latitude
    longitude = message.location.longitude
    all_info = await state.get_data()
    manager_id = all_info.get('d_manager_id')
    database.m_change_d_shop_loc(latitude, longitude, manager_id)
    await message.answer('Location changed!', reply_markup=buttons.shop_owner_kb())
    await AdminShopOwnerM.change_shop_info_state.set()

#Change directors shop name from Admin
@dp.message_handler(state=AdminShopOwnerM.change_shop_name_state)
async def m_change_d_shop_loc(message, state=AdminShopOwnerM.change_shop_name_state):
    all_info = await state.get_data()
    manager_id = all_info.get('d_manager_id')
    new_shop_name = message.text
    database.m_change_d_shop_name(new_shop_name, manager_id)
    await message.answer("ShopName changed!✔️", reply_markup=buttons.shop_owner_kb())
    await AdminShopOwnerM.change_shop_info_state.set()


@dp.message_handler(state=AdminShopOwnerM.change_directors_name_state)
async def m_change_d_name(message,state=AdminShopOwnerM.change_directors_name_state):
    all_info = await state.get_data()
    manager_id = all_info.get('d_manager_id')
    directors_name = message.text
    database.m_change_d_name(directors_name,manager_id)
    await message.answer("Director's name changed!✔️", reply_markup=buttons.shop_owner_kb())
    await AdminShopOwnerM.change_shop_info_state.set()

@dp.message_handler(state=AdminShopOwnerM.change_directors_phone_state,content_types=['contact'])
async def m_change_d_phone(message,state=AdminShopOwnerM.change_directors_phone_state):
    all_info = await state.get_data()
    manager_id = all_info.get('d_manager_id')
    phone_num = message.contact.phone_number
    database.m_change_d_phone(phone_num,manager_id)
    await message.answer('Phone number changed! 📲', reply_markup=buttons.shop_owner_kb())
    await AdminShopOwnerM.change_shop_info_state.set()

@dp.message_handler(state=AdminShopOwnerM.change_directors_TIN_state)
async def m_change_d_phone(message,state=AdminShopOwnerM.change_directors_TIN_state):
    all_info = await state.get_data()
    manager_id = all_info.get('d_manager_id')
    INN = message.text                 #TIN
    database.m_change_d_TIN(INN,manager_id)
    await message.answer('TIN changed!✔️', reply_markup=buttons.shop_owner_kb())
    await AdminShopOwnerM.change_shop_info_state.set()


# Add Shop to director state from Admin

@dp.message_handler(state=AdminShopOwnerM.m_add_d_shop_state,content_types=['location'])
async def m_add_shop(message,state = AdminShopOwnerM.m_add_d_shop_state):
    all_info = await state.get_data()
    latitude = message.location.latitude
    longitude = message.location.longitude
    manager_id = all_info.get('d_manager_id')
    user_id = all_info.get('d_user_id')
    directors_name = all_info.get('d_name')
    phone_num = all_info.get('d_number')
    INN = all_info.get('d_TIN')
    shop_name = all_info.get("d_shop_name")
    manager_id = all_info.get("d_manager_id")
    tasks = "No Task yet"
    database.add_shops(user_id, directors_name, phone_num, INN, shop_name, manager_id, latitude, longitude,tasks)
    await message.answer('Location Updated!🏢', reply_markup=buttons.shop_owner_kb())
    await AdminShopOwnerM.change_shop_info_state.set()



# Admins Seller Branch

@dp.message_handler(state=AdminSeller.m_main_seller_state)
async def m_main_seller(message,state=AdminSeller.m_main_seller_state):
    manager_id = message.text
    await state.update_data(s_manager_id=manager_id)
    seller = database.get_shop_s_owners(manager_id)
    owner_info = "Owners Personal Info\nSellers:\n"
    if seller:
        for i in seller:
            owner_info = f'Name: {i[1]}.\nPhone: {i[2]}.\nShop_lat.: {i[3]}.\nShop_long: {i[4]}.\nTIN(INN): {i[5]}\nShop name: {i[6]}.'
            await message.answer(owner_info)
            await message.answer("Choose operation",reply_markup=buttons.managers_main_seller_menu_kb())
            await AdminSeller.sellers_state.set()
    else:
        await message.answer(f'No such seller with {manager_id}manager ID',reply_markup=managers_main_menu_kb())
        await state.finish()
@dp.message_handler(state=AdminSeller.sellers_state)
async def seller_main(message,state = AdminSeller.sellers_state):
    action = message.text
    if action == "Change Sellers Info":
        await message.answer('What do you want to change:⚙️ ',reply_markup=buttons.managers_change_seller_data_kb())
        await AdminSeller.change_seller_info_state.set()

    elif action == "Seller Balance":
        pass

    elif action == "Seller's Tasks":
        pass

    elif action == "Seller's Checks":
        pass

    elif action == "Back":
        await message.answer("Manager's main menu", reply_markup=buttons.managers_main_menu_kb())
        await state.finish()

    else:
        await message.answer("Press the button to change",reply_markup=buttons.managers_change_seller_data_kb())

@dp.message_handler(state=AdminSeller.change_seller_info_state)
async def m_change_s_info(message,state = AdminSeller.change_seller_info_state):
    action = message.text
    if action == "Change Shop address":
        await message.answer("Send new address" ,reply_markup=buttons.location_kb())
        await AdminSeller.change_shop_loc_state.set()

    elif action == "Change Shop name":
        await message.answer("Write new Shop's name: ", reply_markup=ReplyKeyboardRemove())
        await AdminSeller.change_shop_name_state.set()

    elif action == "Change Seller's name":
        await message.answer("Write new name: ", reply_markup=ReplyKeyboardRemove())
        await AdminSeller.change_sellers_name_state.set()

    elif action == "Change Seller's phone":
        await message.answer("Send new contact", reply_markup=buttons.get_phone_number_kb())
        await AdminSeller.change_sellers_phone_state.set()

    elif action == "Change Seller's TIN":
        await message.answer("Write new TIN(INN)", reply_markup=ReplyKeyboardRemove())
        await AdminSeller.change_sellers_TIN_state.set()

@dp.message_handler(state=AdminSeller.change_shop_loc_state,content_types=['location'])
async def m_change_d_shop_loc(message,state= AdminSeller.change_shop_loc_state):
    latitude = message.location.latitude
    longitude = message.location.longitude
    all_info = await state.get_data()
    manager_id = all_info.get('s_manager_id')
    database.m_change_s_shop_loc(latitude, longitude, manager_id)
    await message.answer('Location changed!', reply_markup=buttons.managers_main_seller_menu_kb())
    await AdminSeller.sellers_state.set()

#Change directors shop name from manager
@dp.message_handler(state= AdminSeller.change_shop_name_state,content_types=['text'])
async def m_change_d_shop_loc(message, state= AdminSeller.change_shop_name_state):
    all_info = await state.get_data()
    manager_id = all_info.get('s_manager_id')
    new_shop_name = message.text
    database.m_change_s_shop_name(new_shop_name, manager_id)
    await message.answer("ShopName changed!✔️", reply_markup=buttons.managers_main_seller_menu_kb())
    await AdminSeller.sellers_state.set()


@dp.message_handler(state= AdminSeller.change_sellers_name_state,content_types=['text'])
async def m_change_d_name(message,state= AdminSeller.change_sellers_name_state):
    all_info = await state.get_data()
    manager_id = all_info.get('s_manager_id')
    seller_name = message.text
    database.m_change_s_name(seller_name,manager_id)
    await message.answer("Seller's name changed!✔️", reply_markup=buttons.managers_main_seller_menu_kb())
    await AdminSeller.sellers_state.set()

@dp.message_handler(state=AdminSeller.change_sellers_phone_state,content_types=['contact'])
async def m_change_d_phone(message,state=AdminSeller.change_sellers_phone_state):
    all_info = await state.get_data()
    manager_id = all_info.get('s_manager_id')
    phone_num = message.contact.phone_number
    database.m_change_s_phone(phone_num,manager_id)
    await message.answer('Phone number changed!✔️', reply_markup=buttons.managers_main_seller_menu_kb())
    await AdminSeller.sellers_state.set()

@dp.message_handler(state= AdminSeller.change_sellers_TIN_state)
async def m_change_d_phone(message,state= AdminSeller.change_sellers_TIN_state):
    all_info = await state.get_data()
    manager_id = all_info.get('s_manager_id')
    INN = message.text                 #TIN
    database.m_change_s_TIN(INN,manager_id)
    await message.answer('TIN changed!✔️', reply_markup=buttons.managers_main_seller_menu_kb())
    await AdminSeller.sellers_state.set()


# Admin TAsks Branch


@dp.message_handler(state=AdminTasks.main_tasks_state)
async def main_tasks(message,state = AdminTasks.main_tasks_state):

    if message.text =="Director's Tasks":
        await message.answer("Director's\nAdd Tasks or Change Tasks?",reply_markup=buttons.directors_tasks_kb())
        await AdminTasks.d_tasks.set()

    elif message.text =="Seller's Tasks":
        await message.answer("Seller's\nAdd Tasks or Change Tasks?",reply_markup=buttons.sellers_tasks_kb())
        await AdminTasks.s_tasks.set()

    elif message.text == 'Back':
        await message.answer("Admin's main menu",reply_markup=buttons.managers_main_menu_kb())
        await state.finish()

    else:
        await message.answer("Choose the button to change ",reply_markup=buttons.managers_tasks_kb())


# CHange tasks menu for Directors And Sellers

@dp.message_handler(state=AdminTasks.d_tasks)
async def D_task(message,state= AdminTasks.d_tasks):
    action = message.text
    if action == "Add Task":
        await message.answer("Write new Task",reply_markup=ReplyKeyboardRemove())
        await AdminTasks.add_d_tasks.set()

    elif action == "Change Task":
        await message.answer("Write Updated Task",reply_markup=ReplyKeyboardRemove())
        await AdminTasks.add_d_tasks.set()

    elif action == "Delete Task":
        await message.answer("Task deleted",reply_markup=buttons.managers_main_menu_kb())
        await AdminTasks.delete_d_task.set()

    elif action == "Back":
        await message.answer("Admin's main menu",reply_markup=buttons.managers_main_menu_kb())
        await state.finish()

    else:
        await message.answer("Choose the button")


@dp.message_handler(state=AdminTasks.s_tasks)
async def D_task(message, state=AdminTasks.s_tasks):
    if message.text == "Add Task":
        await message.answer("Write new Task", reply_markup=ReplyKeyboardRemove())
        await AdminTasks.add_s_tasks.set()

    elif message.text == "Change Task":
        await message.answer("Write Updated Task", reply_markup=ReplyKeyboardRemove())
        await AdminTasks.add_s_tasks.set()

    elif message.text == "Delete Task":
        await message.answer("Task deleted",reply_markup=buttons.managers_main_menu_kb())
        await AdminTasks.delete_s_task.set()

    elif message.text == "Back":
        await message.answer("Admins's main menu", reply_markup=buttons.managers_main_menu_kb())
        await state.finish()

    else:
        await message.answer("Choose the button")


@dp.message_handler(state=AdminTasks.add_d_tasks)
async def add_d_task(message,state=AdminTasks.add_d_tasks):
    TASKS = message.text
    await message.answer("Task added", reply_markup = buttons.managers_tasks_kb())
    database.d_add_task(TASKS)
    await AdminTasks.main_tasks_state.set()

@dp.message_handler(state=AdminTasks.change_d_tasks)
async def add_d_task(message, state=AdminTasks.change_d_tasks):
    TASKS = message.text
    database.d_update_task(TASKS)
    await message.answer("Task Changed", reply_markup=buttons.managers_tasks_kb())
    await AdminTasks.main_tasks_state.set()


@dp.message_handler(state=AdminTasks.delete_d_tasks)
async def add_d_task(message,state=AdminTasks.delete_d_tasks):
    database.d_delete_task()
    await message.answer("Task's Deleted", reply_markup=buttons.managers_tasks_kb())
    await AdminTasks.main_tasks_state.set()


@dp.message_handler(state=AdminTasks.add_s_tasks)
async def add_d_task(message,state= AdminTasks.add_s_tasks):
    TASKS = message.text
    database.s_add_task(TASKS)
    await message.answer("Task added", reply_markup=buttons.managers_tasks_kb())
    await Tasks.main_tasks_state.set()


@dp.message_handler(state=AdminTasks.change_s_tasks)
async def add_d_task(message, state=AdminTasks.change_s_tasks):
    TASKS = message.text
    database.s_update_task(TASKS)
    await message.answer("Task Changed", reply_markup=buttons.managers_tasks_kb())
    await AdminTasks.main_tasks_state.set()


@dp.message_handler(state=AdminTasks.add_s_tasks)
async def add_d_task(message,state= AdminTasks.add_s_tasks):
    database.s_delete_task()
    await message.answer("Tasks Deleted", reply_markup=buttons.managers_tasks_kb())
    await AdminTasks.main_tasks_state.set()

# ADmins Manager Branch
@dp.message_handler(state=AdminManager.m_main_manager_state)
async def adm_m_main(message,state=AdminManager.m_main_manager_state):
    action = message.text
    if action == "Add Manager":
        await message.answer("Write new manager's name: ",reply_markup=ReplyKeyboardRemove())
        await AdminManager.get_managers_name_state.set()
    elif action == "Find Manager":
        await message.answer("Write the id of manager",reply_markup=ReplyKeyboardRemove())
        await AdminManager.get_managers_list.set()
    elif action == "Back":
        pass
    else:
        await message.answer("Choose the button",reply_markup=buttons.admin_m_main_menu_kb())

@dp.message_handler(state=AdminManager.get_managers_name_state)
async def manager_name(message,state=AdminManager.get_managers_name_state):
    managers_name = message.text
    await state.update_data(m_name = managers_name)
    await message.answer("Send manager's number",reply_markup=get_phone_number_kb())
    await AdminManager.get_managers_phone_number_state.set()

@dp.message_handler(state=AdminManager.get_managers_phone_number_state,content_types=['contact'])
async def manager_name(message,state=AdminManager.get_managers_phone_number_state):
    managers_num = message.contact.phone_number
    await state.update_data(phone_num = managers_num)
    await message.answer("Write manager's id",reply_markup=ReplyKeyboardRemove())
    await AdminManager.get_managers_id_state.set()

@dp.message_handler(state=AdminManager.get_managers_id_state)
async def manager_name(message,state=AdminManager.get_managers_id_state):
    manager_id = message.text
    await state.update_data(m_id = manager_id)
    await message.answer("Write managers Login",reply_markup=ReplyKeyboardRemove())
    await AdminManager.get_managers_log_state.set()

@dp.message_handler(state=AdminManager.get_managers_log_state)
async def manager_name(message,state=AdminManager.get_managers_log_state):
    manager_login = message.text
    await state.update_data(manager_log = manager_login)
    await message.answer("Write managers Password",reply_markup=ReplyKeyboardRemove())
    await AdminManager.get_managers_password_state.set()

@dp.message_handler(state=AdminManager.get_managers_password_state)
async def manager_name(message,state=AdminManager.get_managers_password_state):
    password = message.text
    await message.answer("Manager Added",reply_markup=buttons.admin_main_menu_kb())
    all_info = await state.get_data()
    user_id = 0
    manager_id = all_info.get('m_id')
    m_name = all_info.get('m_name')
    phone_num = all_info.get('phone_num')
    login = all_info.get('manager_log')
    database.a_add_manager(user_id,m_name,phone_num,login,password,manager_id)
    print(database.a_add_manager(user_id,m_name,phone_num,login,password,manager_id))
    await message.answer("Manager Added", reply_markup=buttons.admin_main_menu_kb())
    await AdminManager.m_main_manager_state.set()

@dp.message_handler(state=AdminManager.get_managers_list)
async def a_get_manager(message,state =AdminManager.get_managers_list):
    manager_id = message.text
    await state.update_data(m_manager_id = manager_id)
    manager = database.get_manager(manager_id)
    manager_info = "Manager Infor"
    if manager:
        for i in manager:
            manager_info = f'Name: {i[1]}.\nPhone: {i[2]}.\nLogin.: {i[3]}.\nPassword: {i[4]}.\nManager ID: {i[5]}.'
            await message.answer(manager_info)
            await message.answer("Choose operation",reply_markup=buttons.admin_m_change_data_kb())
            await AdminManager.change_info_state.set()
    else:
        await message.answer("No such manager in database",reply_markup=buttons.admin_main_menu_kb())
        await state.finish()

@dp.message_handler(state=AdminManager.change_info_state)
async def adm_m_main(message, state=AdminManager.change_info_state):
    action = message.text
    if action == "Change name":
        await message.answer("Write new manager's name: ", reply_markup=ReplyKeyboardRemove())
        await AdminManager.change_managers_name.set()

    elif action == "Change phone":
        await message.answer("Share new number", reply_markup=buttons.get_phone_number_kb())
        await AdminManager.change_managers_phone.set()

    elif action == "Change login":
        await message.answer("Write the login to change", reply_markup=ReplyKeyboardRemove())
        await AdminManager.change_managers_log.set()

    elif action == "Change password":
        await message.answer("Write new password", reply_markup=ReplyKeyboardRemove())
        await AdminManager.change_managers_pass.set()

    elif action == "Change manager id":
        await message.answer("Write new  id of manager", reply_markup=ReplyKeyboardRemove())
        await AdminManager.change_managers_id.set()

    else:
        await message.answer("Choose the button", reply_markup=buttons.admin_m_main_menu_kb())

@dp.message_handler(state=AdminManager.change_managers_name)
async def ch_name(message,state = AdminManager.change_managers_name):
    new_name = message.text
    all_info = await state.get_data()
    manager_id = all_info.get('m_manager_id')
    database.change_m_name(new_name,manager_id)
    await message.answer("Name changed",reply_markup=buttons.admin_m_main_menu_kb())
    await AdminManager.m_main_manager_state.set()

@dp.message_handler(state=AdminManager.change_managers_phone,content_types=['contact'])
async def ch_name(message,state = AdminManager.change_managers_phone):
    new_num = message.contact.phone_number
    all_info = await state.get_data()
    manager_id = all_info.get('m_manager_id')
    database.change_m_num(new_num,manager_id)
    await message.answer("Number changed",reply_markup=buttons.admin_m_main_menu_kb())
    await AdminManager.m_main_manager_state.set()

@dp.message_handler(state=AdminManager.change_managers_log)
async def ch_name(message,state = AdminManager.change_managers_log):
    new_log = message.text
    all_info = await state.get_data()
    manager_id = all_info.get('m_manager_id')
    database.change_m_log(new_log,manager_id)
    await message.answer("Login Changed",reply_markup=buttons.admin_m_main_menu_kb())
    await AdminManager.m_main_manager_state.set()

@dp.message_handler(state=AdminManager.change_managers_pass)
async def ch_name(message,state = AdminManager.change_managers_pass):
    new_pass = message.text
    all_info = await state.get_data()
    manager_id = all_info.get('m_manager_id')
    database.change_m_pass(new_pass,manager_id)
    await message.answer("Password changed",reply_markup=buttons.admin_m_main_menu_kb())
    await AdminManager.m_main_manager_state.set()

@dp.message_handler(state=AdminManager.change_managers_id)
async def ch_name(message,state = AdminManager.change_managers_id):
    new_id = message.text
    all_info = await state.get_data()
    manager_id = all_info.get('m_manager_id')
    database.change_m_id(new_id,manager_id)
    await message.answer("ID changed",reply_markup=buttons.admin_m_main_menu_kb())
    await AdminManager.m_main_manager_state.set()


# Chat State
@dp.message_handler(state=ChatState.chat_state)
async def chat(message,state=ChatState.chat_state):
    mail = message.text
    await bot.send_message(877993978, mail)
    await message.answer("Your mail sended!", reply_markup=buttons.managers_main_menu_kb())

    await state.finish()



# MAIN MESSAGE HANDLER
@dp.message_handler(content_types=['text'])
async def sellors_all_info(message):
    user_id = message.from_user.id
    seller = database.check_user(user_id)
    director = database.check_director(user_id)
    manager = database.check_manager(user_id)
    admin = database.check_admin(user_id)
    answer = message.text

    if seller:
        if  answer == 'Personal info':
            seller_all_info = database.get_seller(user_id)
            result_answer = "Personal Info:\n"
            for i in seller_all_info:
                result_answer = f'Name: {i[0]}.\nPhone: {i[1]}.\nLocation Latitude: {i[2]}.Location Longitude: {i[3]}\nTIN: {i[4]}.\nShop name: {i[5]}'
                await message.answer(result_answer,reply_markup=buttons.change_personal_data_kb())
        elif answer == "Change data":
            await message.answer('What do u want to change', reply_markup=buttons.change_sellors_personal_data_kb())
            await SellersPersonalInfo.change_data_state.set()

        elif  answer == 'Tasks':
            task = database.get_s_task()
            await message.answer(f"Your Task:\n{task}", reply_markup=buttons.sellors_main_menu_kb())

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
            await message.answer('Write your mail: ', reply_markup=ReplyKeyboardRemove())
            await ChatState.chat_state.set()
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
            await message.answer('What do u want to change⚙️', reply_markup=buttons.change_directors_personal_data_kb())
            await DirectorsPersonalInfo.change_data_state.set()

        elif answer == 'Tasks':
            task = database.get_d_task()
            await message.answer(f"Your Task:\n{task}", reply_markup=buttons.directors_main_menu_kb())
            await state.finish()

        elif answer == 'Add shop location':
             await message.answer('Add locations of your shops: ',reply_markup=buttons.location_kb())
             await DirectorAddShopLocations.add_shop_state.set()

        elif  answer == 'Balance':
            pass

        elif  answer == 'Gifts available':
            pass

        elif  answer == 'Get the Cash':
            await message.answer("Request sended",reply_markup=buttons.directors_main_menu_kb())
            await state.finish()

        elif  answer == 'Knowledge Base':
            pass

        elif  answer == 'Ask a question':
            await message.answer('Write your mail: ', reply_markup=ReplyKeyboardRemove())
            await ChatState.chat_state.set()

        else:
            await message.answer("Choose the buttonn")

    elif manager:

        if answer == 'Directors':
            await message.answer("Write the ID of the Director's manager:🪪",reply_markup=ReplyKeyboardRemove())
            await ShopOwnerM.shop_owners_state.set()

        elif answer == 'Sellers':
            await message.answer("Write the ID of the Seller's manager:🪪",reply_markup=ReplyKeyboardRemove())
            await MSeller.m_main_seller_state.set()

        elif answer == 'Tasks':
            await message.answer("Tasks to Director or Seller?", reply_markup=buttons.managers_tasks_kb())
            await Tasks.main_tasks_state.set()

        elif answer == 'Balance':
            pass

        elif answer == 'Gifts to change':
            pass

        elif answer == 'Chat':
            await message.answer('Write your mail: ', reply_markup=ReplyKeyboardRemove())
            await ChatState.chat_state.set()


        else:
            await message.answer("Choose the operation manager")


    elif admin:

        if answer == 'Directors':
            await message.answer("Write the ID of the Director's manager:🪪 ", reply_markup=ReplyKeyboardRemove())
            await AdminShopOwnerM.shop_owners_state.set()

        elif answer == 'Sellers':
            await message.answer("Write the ID of the Seller's manager:🪪 ", reply_markup=ReplyKeyboardRemove())
            await AdminSeller.m_main_seller_state.set()

        elif answer == 'Tasks':
            await message.answer("Tasks to Director or Seller?", reply_markup=buttons.managers_tasks_kb())
            await AdminTasks.main_tasks_state.set()

        elif answer == "Managers":
            await message.answer("Choose the operation",reply_markup=admin_m_main_menu_kb())
            await AdminManager.m_main_manager_state.set()

        elif answer == 'Balance':
            pass

        elif answer == 'Gifts to change':
            pass

        elif answer == 'Chat':
             await message.answer('Write your mail: ',reply_markup=ReplyKeyboardRemove())
             await ChatState.chat_state.set()

        else:
            await message.answer("Choose the operation manager")

    else:
        await message.answer("Choose the button from kb")



executor.start_polling(dp)