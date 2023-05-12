from aiogram.dispatcher.filters.state import State, StatesGroup

class AdminPanel(StatesGroup):
    main_state = State()

# Seller Branch
class SellerRegistration(StatesGroup):
    get_sellers_name_state = State()
    get_sellers_phone_number_state = State()
    get_shop_address_state = State()
    get_sellers_TIN_state = State()
    get_sellers_shop_name_state = State()
    get_manager_id_state = State()

class SellersPersonalInfo(StatesGroup):
    get_all_sellers_info_state = State()
    change_data_state = State()
    change_sellers_name_state = State()
    change_sellers_number_state = State()
    change_sellers_addres_state = State()
    change_sellers_TIN_state = State()
    change_sellers_ShopsName_state = State()

# Director Branch
class DirectorRegistration(StatesGroup):
    get_directors_name_state = State()
    get_directors_phone_number_state = State()
    get_directors_TIN_state = State()
    get_directors_shop_name_state = State()
    get_manager_id_state = State()

class DirectorsPersonalInfo(StatesGroup):
    get_all_directors_info_state = State()
    change_data_state = State()
    change_directors_name_state = State()
    change_directors_number_state = State()
    change_directors_addres_state = State()
    change_directors_TIN_state = State()
    change_directors_ShopsName_state = State()

class DirectorAddShopLocations(StatesGroup):
    add_shop_state = State()

# Managers Branch
class CheckManager(StatesGroup):
    login_state = State()
    password_state = State()

class ShopOwnerM(StatesGroup):
    shop_owners_state = State()





class CheckAdmin(StatesGroup):
    login_state = State()
    password_state =State()