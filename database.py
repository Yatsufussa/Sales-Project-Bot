import sqlite3
connection = sqlite3.connect("Sales Bot1.db")
sql = connection.cursor()

#sql.execute("CREATE TABLE sellers (user_id INTEGER, seller_name TEXT, phone_num TEXT, shop_lat REAL,shop_long REAL, INN TEXT,shop_name TEXT, manager_id INTEGER );")

def add_seller(user_id,seller_name, phone_num, latitude, longitude, INN, shop_name, manager_id):
    # Create/login to database
    connection = sqlite3.connect("Sales Bot1.db")
    # Creating translator
    sql = connection.cursor()
    # Adding user into database
    sql.execute("INSERT INTO sellers VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
                (user_id, seller_name, phone_num, latitude, longitude, INN, shop_name, manager_id))


    # fixiruem obnovleniye
    connection.commit()

def get_seller(user_id):
    # Create/login to database
    connection = sqlite3.connect("Sales Bot1.db")
    # Creating translator
    sql = connection.cursor()
    # Adding user into database
    seller = sql.execute("SELECT * FROM sellers WHERE user_id = ?;",(user_id,))
    return seller.fetchall()

def check_user(user_id):
    connection = sqlite3.connect("Sales Bot1.db")
    sql = connection.cursor()
    checker = sql.execute("SELECT user_id FROM sellers WHERE user_id = ?;", (user_id,))
    # Проверка есть ли данные из запроса
    if checker.fetchone():
        return True
    else:
        return False

def get_sellers():
    # Create/login to database
    connection = sqlite3.connect("Sales Bot1.db")
    # Creating translator
    sql = connection.cursor()
    sellers = sql.execute("SELECT seller_name,user_id FROM sellers;")
    return sellers.fetchall()

def change_name(new_name,user_id):
    # Create/login to database
    connection = sqlite3.connect("Sales Bot1.db")
    # Creating translator
    sql = connection.cursor()
    new_name = sql.execute("UPDATE sellers SET seller_name= ? WHERE user_id = ?;", (new_name,user_id,))
    connection.commit()

def change_phone_number(new_num,user_id):
    # Create/login to database
    connection = sqlite3.connect("Sales Bot1.db")
    # Creating translator
    sql = connection.cursor()
    new_name = sql.execute("UPDATE sellers SET phone_num= ? WHERE user_id = ?;", (new_num, user_id,))
    connection.commit()

def change_shop_address(shop_lat,shop_long,user_id):
    # Create/login to database
    connection = sqlite3.connect("Sales Bot1.db")
    # Creating translator
    sql = connection.cursor()
    new_name = sql.execute("UPDATE sellers SET shop_lat= ?,shop_long= ? WHERE user_id = ?;", (shop_lat,shop_long,user_id,))
    connection.commit()

def change_sellers_TIN(TIN,user_id):
    # Create/login to database
    connection = sqlite3.connect("Sales Bot1.db")
    # Creating translator
    sql = connection.cursor()
    new_name = sql.execute("UPDATE sellers SET INN=?  WHERE user_id = ?;", (TIN,user_id,))
    connection.commit()

def change_shop_name(new_shop_name,user_id):
    # Create/login to database
    connection = sqlite3.connect("Sales Bot1.db")
    # Creating translator
    sql = connection.cursor()
    new_name = sql.execute("UPDATE sellers SET shop_name= ? WHERE user_id = ?;", (new_shop_name,user_id,))
    connection.commit()



#sql.execute("CREATE TABLE Directors (user_id INTEGER, directors_name TEXT, phone_num TEXT,INN TEXT,shop_name TEXT, manager_id INTEGER );")

def add_director(user_id,director_name, phone_num,INN, shop_name, manager_id,Shop_address):
    # Create/login to database
    connection = sqlite3.connect("Sales Bot1.db")
    # Creating translator
    sql = connection.cursor()
    # Adding user into database
    sql.execute("INSERT INTO Directors VALUES (?, ?, ?, ?, ?, ?, ?);",
                (user_id, director_name, phone_num,INN, shop_name, manager_id,Shop_address))
    connection.commit()


def get_director(user_id):
    # Create/login to database
    connection = sqlite3.connect("Sales Bot1.db")
    # Creating translator
    sql = connection.cursor()
    # Adding user into database
    director = sql.execute("SELECT * FROM Directors WHERE user_id = ?;",(user_id,))
    return director.fetchall()

def check_director(user_id):
    connection = sqlite3.connect("Sales Bot1.db")
    sql = connection.cursor()
    checker = sql.execute("SELECT user_id FROM Directors WHERE user_id = ?;", (user_id,))
    # Проверка есть ли данные из запроса
    if checker.fetchone():
        return True
    else:
        return False

def change_d_name(new_name,user_id):
    # Create/login to database
    connection = sqlite3.connect("Sales Bot1.db")
    # Creating translator
    sql = connection.cursor()
    new_name = sql.execute("UPDATE Directors SET directors_name= ? WHERE user_id = ?;", (new_name,user_id,))
    connection.commit()

def change_d_phone_number(new_num,user_id):
    # Create/login to database
    connection = sqlite3.connect("Sales Bot1.db")
    # Creating translator
    sql = connection.cursor()
    new_name = sql.execute("UPDATE Directors SET phone_num= ? WHERE user_id = ?;", (new_num, user_id,))
    connection.commit()

def change_directors_TIN(TIN,user_id):
    # Create/login to database
    connection = sqlite3.connect("Sales Bot1.db")
    # Creating translator
    sql = connection.cursor()
    new_name = sql.execute("UPDATE Directors SET INN=?  WHERE user_id = ?;", (TIN,user_id,))
    connection.commit()

def change_d_shop_name(new_shop_name,user_id):
    # Create/login to database
    connection = sqlite3.connect("Sales Bot1.db")
    # Creating translator
    sql = connection.cursor()
    new_name = sql.execute("UPDATE Directors SET shop_name= ? WHERE user_id = ?;", (new_shop_name,user_id,))
    connection.commit()

def add_coloumn():
    connection = sqlite3.connect("Sales Bot1.db")
    # Creating translator
    sql = connection.cursor()
    add_c = sql.execute("ALTER TABLE Directors ADD Shop_address REAL;")
def add_shops(new_location,user_id):
    # Create/login to database
    connection = sqlite3.connect("Sales Bot1.db")
    # Creating translator
    sql = connection.cursor()
    new_name = sql.execute("INSERT INTO Directors Shop_address= ? WHERE user_id = ?;", (new_location,user_id,))
    connection.commit()


#Managers Branch

#sql.execute("CREATE TABLE Managers (user_id INTEGER, login TEXT, password TEXT);")
def check_log(login):
    connection = sqlite3.connect("Sales Bot1.db")
    sql = connection.cursor()
    checker = sql.execute("SELECT login FROM Managers WHERE login = ?;", (login,))
    # Проверка есть ли данные из запроса
    if checker.fetchall():
        return True
    else:
        return False
def check_pas(password):
    connection = sqlite3.connect("Sales Bot1.db")
    sql = connection.cursor()
    checker = sql.execute("SELECT password FROM Managers WHERE password = ?;", (password,))
    # Проверка есть ли данные из запроса
    if checker.fetchall():
        return True
    else:
        return False
def check_manager(user_id):
    connection = sqlite3.connect("Sales Bot1.db")
    sql = connection.cursor()
    checker = sql.execute("SELECT user_id FROM Managers WHERE user_id = ?;", (user_id,))
    # Проверка есть ли данные из запроса
    if checker.fetchone():
        return True
    else:
        return False

def add_manager(user_id,password):
    connection = sqlite3.connect("Sales Bot1.db")
    # Creating translator
    sql = connection.cursor()
    # Adding  user into database
    manager = sql.execute('UPDATE Managers SET user_id=? WHERE password = ?;', (user_id,password,))
    connection.commit()

# def get_shop_s_locations(manager_id):
#     connection = sqlite3.connect("Sales Bot1.db")
#     sql = connection.cursor()
#     shop_owner_loc = sql.execute("SELECT latitude,longitude FROM Sellers WHERE manager_id = ?;", (manager_id,))
#     # Проверка есть ли данные из запроса
#     return shop_owner_loc.fetchall()
def get_shop_d_locations(manager_id):
    connection = sqlite3.connect("Sales Bot1.db")
    sql = connection.cursor()
    shop_owner_loc = sql.execute("SELECT Shop_address FROM Directors WHERE manager_id = ?;", (manager_id,))
    # Проверка есть ли данные из запроса
    return shop_owner_loc.fetchall()



# ADMIN BRANCH
# sql.execute("CREATE TABLE Admins (user_id INTEGER, login TEXT, password TEXT);")
def check_a_log(login):
    connection = sqlite3.connect("Sales Bot1.db")
    sql = connection.cursor()
    checker = sql.execute("SELECT login FROM Admins WHERE login = ?;", (login,))
    # Проверка есть ли данные из запроса
    if checker.fetchall():
        return True
    else:
        return False

def check_a_pas(password):
    connection = sqlite3.connect("Sales Bot1.db")
    sql = connection.cursor()
    checker = sql.execute("SELECT password FROM Admins WHERE password = ?;", (password,))
    # Проверка есть ли данные из запроса
    if checker.fetchall():
        return True
    else:
        return False

def get_shop_s_owners(manager_id):
    connection = sqlite3.connect("Sales Bot1.db")
    sql = connection.cursor()
    shop_owner_sel = sql.execute("SELECT * FROM sellers WHERE manager_id = ?;", (manager_id,))
   # shop_owner_dir = sql.execute("SELECT * FROM Directors WHERE manager_id = ?;", (manager_id,))
    # Проверка есть ли данные из запроса
    return shop_owner_sel.fetchall()#shop_owner_dir.fetchall()
def get_shop_d_owners(manager_id):
    connection = sqlite3.connect("Sales Bot1.db")
    sql = connection.cursor()
    shop_owner_dir = sql.execute("SELECT * FROM Directors WHERE manager_id = ?;", (manager_id,))
    # Проверка есть ли данные из запроса
    return shop_owner_dir.fetchall()

def add_admin(user_id):
    connection = sqlite3.connect("Sales Bot1.db")
    # Creating translator
    sql = connection.cursor()
    # Adding  user into database
    admin = sql.execute('UPDATE Admins SET user_id WHERE user_id = ?;', (user_id,))
    connection.commit()

print(get_shop_d_locations(111))