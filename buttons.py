from aiogram.types import ReplyKeyboardRemove,ReplyKeyboardMarkup,KeyboardButton

#First admin menu buttons
def admin_kb():
    kb =ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
    button1 =KeyboardButton("Im Seller")
    button2 =KeyboardButton("Im Director,Leader")
    button3 =KeyboardButton("Im Manager")
    button4 =KeyboardButton("Im Admin")
    kb.add(button1,button2,button3,button4)
    return kb

def get_phone_number_kb():
    kb =ReplyKeyboardMarkup(resize_keyboard=True)
    button1 =KeyboardButton("Press the button to Share phone number",request_contact=True)
    kb.add(button1)
    return kb

def location_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton("Share Location", request_location=True)
    kb.add(button1)
    return kb

#Sellors Branch
def sellors_main_menu_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True,row_width=3)
    button1 = KeyboardButton('Personal info')
    button2 = KeyboardButton('Tasks')
    button3 = KeyboardButton('Check download')
    button4 = KeyboardButton('Balance')
    button5 = KeyboardButton('Gifts available')
    button6 = KeyboardButton('Get the Cash')
    button7 = KeyboardButton('Knowledge Base')
    button8 = KeyboardButton('Ask a question')
    kb.add(button1,button2,button3,button4,button5,button6,button7,button8)
    return kb

def change_personal_data_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton('Change data')
    kb.add(button1)
    return kb

def change_sellors_personal_data_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton('Change Name')
    button2 = KeyboardButton('Change phone number')
    button3 = KeyboardButton('Change shop address')
    button4 = KeyboardButton('Change TIN(INN)')
    button5 = KeyboardButton('Change shop name')
    kb.add(button1,button2,button3,button4,button5)
    return kb

def change_directors_personal_data_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
    button1 = KeyboardButton('Change Name')
    button2 = KeyboardButton('Change phone number')
    button3 = KeyboardButton('Change TIN(INN)')
    button4 = KeyboardButton('Change shop name')
    kb.add(button1,button2,button3,button4)
    return kb

def directors_main_menu_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True,row_width=3)
    button1 = KeyboardButton('Personal info')
    button2 = KeyboardButton('Tasks')
    button3 = KeyboardButton('Add shop location')
    button4 = KeyboardButton('Balance')
    button5 = KeyboardButton('Gifts available')
    button6 = KeyboardButton('Get the Cash')
    button7 = KeyboardButton('Knowledge Base')
    button8 = KeyboardButton('Ask a question')
    kb.add(button1,button2,button3,button4,button5,button6,button7,button8)
    return kb

def managers_main_menu_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    button1 = KeyboardButton('Directors')
    button2 = KeyboardButton('Sellers')
    button3 = KeyboardButton('Tasks')
    button4 = KeyboardButton('Balance')
    button5 = KeyboardButton('Gifts to change')
    button6 = KeyboardButton('Chat')
    kb.add(button1, button2, button3, button4, button5, button6)
    return kb

def admin_main_menu_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    button1 = KeyboardButton('Directors')
    button2 = KeyboardButton('Sellers')
    button3 = KeyboardButton('Managers')
    button4 = KeyboardButton('Tasks')
    button5 = KeyboardButton('Gifts to change')
    button6 = KeyboardButton('Withdrawal of money')
    button7 = KeyboardButton('Chat')
    button8 = KeyboardButton('Knowledge Database')
    kb.add(button1, button2, button3, button4, button5, button6, button7, button8,)
    return kb

def shop_owner_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button2 = KeyboardButton('Add new shop loc.')
    button3 = KeyboardButton('Change Director info')
    button4 = KeyboardButton('Balance')
    button5 = KeyboardButton('Tasks')
    button6 = KeyboardButton('Back')
    kb.add(button2, button3, button4, button5,button6)
    return kb
def managers_change_owner_data_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button1 = KeyboardButton("Change Shop address")
    button2 = KeyboardButton("Change Shop name")
    button3 = KeyboardButton("Change Directors name")
    button4 = KeyboardButton("Change Directors phone")
    button5 = KeyboardButton("Change Directors TIN")
    kb.add(button1,button2,button3,button4,button5)
    return kb