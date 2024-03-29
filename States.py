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

class CheckAdmin(StatesGroup):
    login_state = State()
    password_state =State()

# Manager Director Branch
class ShopOwnerM(StatesGroup):
    shop_owners_state = State()
    change_data_state = State()
    list_of_shops_state = State()
    change_shop_info_state = State()
    change_shop_name_state = State()
    change_shop_loc_state = State()
    change_directors_name_state = State()
    change_directors_phone_state = State()
    change_directors_TIN_state = State()
    m_add_d_shop_state = State()

class MSeller(StatesGroup):
    m_main_seller_state = State()
    sellers_state = State()
    change_seller_info_state = State()
    change_shop_name_state = State()
    change_shop_loc_state = State()
    change_sellers_name_state = State()
    change_sellers_phone_state = State()
    change_sellers_TIN_state = State()

#D - Director,S-Seller
class Tasks(StatesGroup):
    main_tasks_state = State()
    d_tasks = State()
    add_d_tasks = State()
    delete_d_tasks= State()
    change_d_tasks = State()
    s_tasks = State()
    add_s_tasks = State()
    delete_s_tasks= State()
    change_s_tasks = State()

class AdminShopOwnerM(StatesGroup):
    shop_owners_state = State()
    change_data_state = State()
    list_of_shops_state = State()
    change_shop_info_state = State()
    change_shop_name_state = State()
    change_shop_loc_state = State()
    change_directors_name_state = State()
    change_directors_phone_state = State()
    change_directors_TIN_state = State()
    m_add_d_shop_state = State()

class AdminSeller(StatesGroup):
    m_main_seller_state = State()
    sellers_state = State()
    change_seller_info_state = State()
    change_shop_name_state = State()
    change_shop_loc_state = State()
    change_sellers_name_state = State()
    change_sellers_phone_state = State()
    change_sellers_TIN_state = State()

class AdminManager(StatesGroup):
    m_main_manager_state = State()
    add_manager_state = State()
    get_managers_name_state = State()
    get_managers_phone_number_state = State()
    get_managers_log_state = State()
    get_managers_password_state = State()
    get_managers_id_state = State()
    get_managers_list = State()
    change_info_state = State()
    change_managers_name = State()
    change_managers_phone = State()
    change_managers_log = State()
    change_managers_pass = State()
    change_managers_id = State()
    delete_manager_state = State()




class AdminTasks(StatesGroup):
    main_tasks_state = State()
    d_tasks = State()
    add_d_tasks = State()
    delete_d_tasks= State()
    change_d_tasks = State()
    s_tasks = State()
    add_s_tasks = State()
    delete_s_tasks= State()
    change_s_tasks = State()

class ChatState(StatesGroup):
    chat_state = State()