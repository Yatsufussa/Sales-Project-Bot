from aiogram.types import ReplyKeyboardRemove,ReplyKeyboardMarkup,KeyboardButton

#First admin menu buttons
def admin_kb():
    kb =ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
    button1 =KeyboardButton("Im Seller")
    button2 =KeyboardButton("Im Director,Leader")
    kb.add(button1,button2)
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
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
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
    button3 = KeyboardButton('Check download')
    button4 = KeyboardButton('Balance')
    button5 = KeyboardButton('Gifts available')
    button6 = KeyboardButton('Get the Cash')
    button7 = KeyboardButton('Knowledge Base')
    button8 = KeyboardButton('Ask a question')
    kb.add(button1,button2,button3,button4,button5,button6,button7,button8)
    return kb