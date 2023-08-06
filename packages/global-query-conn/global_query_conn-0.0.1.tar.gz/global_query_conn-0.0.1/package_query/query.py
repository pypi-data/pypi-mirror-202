import re
from package_logger.logger import LoggerAplication
import datetime
from configparser import ConfigParser
import hashlib

__config = ConfigParser()
__config.read('config.ini')
__databasetipe = __config.get("main_config","single_database_type")
__multidbstatus = __config.get("main_config","multiple_database_status")

__all__ = [
    "return_of_response",
    "additional_response",
    "build_message_detail",
    "generate_headers",
    "generate_footers"
    "datatables_view",
    "check_existing_data",
    "update_data",
    "insert_data",
    "delete_data",
    "validate"
]

def return_of_response(code:int = 500, status:str = "error", message:str = "No Response", message_detail:str = None, data:list = None,):
    """Membuat response dari request dengan otomatis dengan memasukan parameternya.
    code => untuk response ex: 200, 500, 400, 404, 403 dll
    status => status response seperti success, warning, error
    message => message dar response
    message_detail => detail message yang akan digunakan untuk masuk kedalam history
    data => jika ada response data maka diisi
    """
    return {"code": code, "status": status, "message": message, "messageDetail": message_detail, "data": data}

def additional_response(rows_count:int = None, headers:list = None, footers:dict = None, data_footers:list = None):
    """Tambahan dari return_of_response
    rows_count => jumlah datanya
    headers => headers untuk datatable
    footers => footers untuk datatable
    data_footers => data footers untuk datatble
    
    """
    return {"rowsCount": rows_count, "dataTable": {"headers": headers, "footers": footers}, "dataFooters": data_footers}

def build_message_detail(tipe:int = None, old_data:str = None, new_data:str = None, action:str = None, menu_name:str = None, params_value:list = None, data_name:str = None, params_char:list = None, target:str = None):
    """Digunakan untuk membuat message dan message detail
    tipe => tipe terdiri dari 1, 2, 3 dan 4, 1 utuk action view, 2 untuk insert, 3 untuk update, 4 untuk delete
    old_data => data lama
    new_data => data baru 
    action => aksi dalam bentuk string
    menu_name => nama menunya ketika melakukan event
    param_values => param yang digunakan untuk melakukan action
    data_name => data yang menjadi acuan action
    params_char => parameter yang digunakan
    target => target colom untuk update

    """
    message, message_detail = None, None
    if tipe == 1:
        message = f"{action} {menu_name}"
        message_detail = f"{menu_name} => {action} => Params {params_char} :{params_value if params_value else ''}"
    elif tipe == 2:
        message = f" {data_name} successfully {action} "
        message_detail = f"{menu_name} => {action} => {params_value if params_value else ''}"
    elif tipe == 3:
        message = f"{data_name} successfully {action}"
        message_detail = f"{menu_name} => {action} => Target {target} by Params {params_char} :{old_data} to {new_data}"
    elif tipe == 4:
        message = f"{data_name} successfully {action}"
        message_detail = f"{menu_name} => {action} => Params {params_char} :{params_value}"
    return message, message_detail

def generate_headers(title:list = None, data_index:list = None, isview:list = None):
    """untuk membuat header pada datatable
    title => name header kolomn
    data_index => taget data yang akan diambil
    isview => status akan di tampilkan atau tidak
    
    """
    if not title or not data_index or not isview or len(title) != len(data_index) != len(isview):
        return []
    headers = [{"dataIndex": data_idx, "title": title_idx, "isView": isview_idx} for data_idx, title_idx, isview_idx in zip(data_index, title, isview)] 
    return headers


def generate_footers(title:list = None, data_index:list = None, isview:list = None):
    """untuk membuat header pada datatable
    title => name header kolomn
    data_index => taget data yang akan diambil
    isview => status akan di tampilkan atau tidak
    
    """
    if not title or not data_index or not isview or len(title) != len(data_index) != len(isview):
        return []
    footers = [{"dataIndex": data_idx, "title": title_idx, "isView": isview_idx} for data_idx, title_idx, isview_idx in zip(data_index, title, isview)] 
    return footers

def datatables_view(running_database:str = None, tablename:str = None, target_column:list = None, column_name:list = None, values:list = None, limit:int = None, page:int = None, order:str = None, 
                        order_tipe:str = None, tipe:int = None, group_values:list = None, disable_row_count:bool = None, menu_name:str = None, custom_logic:list = None, mode_as:bool = None,
                        having_condition:str = None):
    """
        Query yang biasa digunakan untuk datatable dengan parameter tertentu
        running_database => jenis database yang digunakan untuk melakukan query yaitu postgresql, mysql, mongodb
        tablename ==> nama table jika dimongodb nama collectionnya
        target_column ==> kolom yang akan dihasilkan tidak diperlukan di mongodb
        column_name ==> kolom yang digunakan untuk kondisi where dan and, jika di mongodb adalah keys saat find
        values ==> value yang digunakan untuk pencarian pada where atau and, jika di mongodb adalag value keys daat find
        limit ==> limit data
        page ==> offset
        order ==> kolom yang akan diorder
        order_tipe ==> tipe ordernya asc atau desc
        tipe ==> tipe query data, jika 1 maka fetchone(), jika dimongo db maka berubah menjadi find_one
        group_values ==> kondisi group by, digunakan jika diperlukan, tidak diperlukan di mongodb
        diasble_row_count ==> jika True maka tidak akan menghitung jumlah rownya untuk pagenation
        menu_name ==> nama menu saat menjalankan fungsi ini
        custom_logic ==> logic yang dapat dicustom seperi like dan lainnya, tidak diperlukan di mongodb
        mode_as ==> metode penghitungan setelah semua data ditampilkan, tidak diperlukan dimongodb
    """
    running_database = running_database if running_database else "NO DATABASE"
    logger = LoggerAplication(tanggal= datetime.datetime.now().date()).Configuration()
    data = None
    rows_count = 0
    if (__databasetipe.upper() in ["POSTGRESQL","MYSQL"] and __multidbstatus == "0") or (running_database.upper() in ["POSTGRESQL","MYSQL"] and __multidbstatus == "1"):
        valid_target = ", ".join(target_column) if target_column else "*"
        valid_columns = " AND ".join([f"{column} {'=' if not custom_logic else custom_logic[idx]} %s" for idx, column in enumerate(column_name)]) if column_name else ""
        valid_limit = f"LIMIT {limit}" if limit else ""
        valid_offset = f"OFFSET {limit * (page)}" if page and limit else ""
        valid_group = " ,".join([f"{group}" for group in group_values]) if group_values else ""
        valid_order = f"ORDER BY {order} {order_tipe}" if order and order_tipe else ""
        valid_having = having_condition if having_condition else ""


        query = f"SELECT {valid_target} FROM {tablename}"
        if not mode_as:
            query_total = f"SELECT count(*) as total FROM {tablename}"
        if column_name:
            query += f" WHERE {valid_columns}"
            if not mode_as:
                query_total += f" WHERE {valid_columns}"
        if mode_as:
            query_total = f"select count(*) as total from ({query} {' GROUP BY ' if group_values else ''} {valid_group} {'HAVING' if having_condition else''} {valid_having}) as a"
        query += f"{' GROUP BY ' if group_values else ''} {valid_group} {'HAVING' if having_condition else''} {valid_having} {valid_order} {valid_limit} {valid_offset}"

    if (running_database.upper() == "POSTGRESQL" and __multidbstatus == "1") or (__multidbstatus == '0' and __databasetipe.upper() == "POSTGRESQL"):
        from package_conn.conn import postgresql_connection
        with postgresql_connection() as cursor:
            try:
                cursor.execute(query, tuple(values) if values else None)
                data = cursor.fetchall() if not tipe else cursor.fetchone()
                logger.handlers.clear()
                if not disable_row_count:
                    cursor.execute(query_total, tuple(values) if values else None)
                    rows_count = cursor.fetchone()['total'] if not tipe else 1
                    add_response = additional_response(rows_count= rows_count)
                    response = return_of_response(code= 200, status= "success", data= data)
                    return {**response, **add_response}
                return return_of_response(code= 200, status= "success", data= data)
            except Exception as e:
                error_message = re.sub(' +',' ',str(e).replace('\n', ' '))
                logger.error(f"||{menu_name}|| {error_message}")
                logger.handlers.clear()
                return return_of_response(message= "Internal Server Error", message_detail= str(e))
            
    elif (running_database.upper() == "MYSQL" and __multidbstatus == "1") or (__multidbstatus == '0' and __databasetipe.upper() == "MYSQL"):
        from package_conn.conn import mysql_connection
        with mysql_connection() as cursor:
            try:
                cursor.execute(query, tuple(values) if values else None)
                data = cursor.fetchall() if not tipe else cursor.fetchone()
                logger.handlers.clear()
                if not disable_row_count:
                    cursor.execute(query_total, tuple(values) if values else None)
                    rows_count = cursor.fetchone()['total'] if not tipe else 1
                    add_response = additional_response(rows_count= rows_count)
                    response = return_of_response(code= 200, status= "success", data= data)
                    return {**response, **add_response}
                return return_of_response(code= 200, status= "success", data= data)
            except Exception as e:
                error_message = re.sub(' +',' ',str(e).replace('\n', ' '))
                logger.error(f"||{menu_name}|| {error_message}")
                logger.handlers.clear()
                return return_of_response(message= "Internal Server Error", message_detail= str(e))
            
    elif (running_database.upper() == "MONGODB" and __multidbstatus == "1") or (__multidbstatus == '0' and __databasetipe.upper() == "MONGODB"):
        from package_conn.conn import mongo_connection
        with mongo_connection() as cursor:
            try:
                __collection = cursor[tablename]
                __search_object_mongo = ({col:val} for col, val in zip(column_name, values) ) if column_name else {}
                __ordermongo = 1 if order_tipe.upper() == "ASC" else -1
                if tipe == 1:
                    __result = __collection.find_one(__search_object_mongo)
                else:
                    __result = __collection.find(__search_object_mongo).sort(order, __ordermongo) if not limit or not page else __collection.find(__search_object_mongo).sort(order, __ordermongo).skip(page).limit(limit)
                if not disable_row_count:
                    __rowscount = len(__result)
                    __addresponse = additional_response(rows_count= __rowscount)
                    __response = return_of_response(code= 200, status= "success", data= __result)
                    return {**__response, **__addresponse}
                return return_of_response(code= 200, status= "success", data= __result)
            except Exception as e:
                error_message = re.sub(' +',' ',str(e).replace('\n', ' '))
                logger.error(f"||{menu_name}|| {error_message}")
                logger.handlers.clear()
                return return_of_response(message= "Internal Server Error", message_detail= str(e))

    else:
        return return_of_response(message= "No selected database type")
        
   
def check_existing_data(running_database:str = None, tablename:str = None, column_name:list = None, values:list = None, tipe:int = None, lower_status:list = None, menu_name:str = None):
    """
        Untuk melakukan check data pada database
        running_database => jenis database yang digunakan untuk melakukan query yaitu postgresql, mysql, mongodb
        tablename => nama table dalam bentuk string
        column_name => column yang digunakan untuk where dalam bentuk list string seperti ["name","password"]
        values => values dari where pada column name dalam bentuk list string seperti ["name","password"]
        tipe => tipe hasil query, 1 => 1 baris
        lower_status => apakah valuenya akan mengalami lower character ex: [True,False]
        menu_name => nama menu saat melakukan query dan konek ke logger
    """
    running_database = running_database if running_database else "NO DATABASE"
    logger = LoggerAplication(tanggal= datetime.datetime.now().date()).Configuration()
    if (__databasetipe.upper() in ["POSTGRESQL","MYSQL"] and __multidbstatus == "0") or (running_database.upper() in ["POSTGRESQL","MYSQL"] and __multidbstatus == "1"):
        query = f"select * from {tablename} "
        if column_name and values and (len(column_name) == len(values)):
            query += F"WHERE {' AND '.join([f'LOWER({column}) = lower(%s)' if lower else f'{column} = %s' for column, lower in zip(column_name, lower_status)])}"

    if (running_database.upper() == "POSTGRESQL" and __multidbstatus == "1") or (__multidbstatus == '0' and __databasetipe.upper() == "POSTGRESQL"):
        from package_conn.conn import postgresql_connection
        with postgresql_connection() as cursor:
            try:
                cursor.execute(query, tuple(values))
                logger.handlers.clear()
                return return_of_response(code= 200, status= "success", message= None, data= cursor.fetchone() if tipe == 1 else cursor.fetchall())
            except Exception as e:
                error_message = re.sub(' +',' ',str(e).replace('\n', ' '))
                logger.error(f"||{menu_name}|| {error_message}")
                logger.handlers.clear()
                return return_of_response(message= "Internal Server Error", message_detail= str(e))
            
    elif (running_database.upper() == "MYSQL" and __multidbstatus == "1") or (__multidbstatus == '0' and __databasetipe.upper() == "MYSQL"):
        from package_conn.conn import mysql_connection
        with mysql_connection() as cursor:
            try:
                cursor.execute(query, tuple(values))
                logger.handlers.clear()
                return return_of_response(code= 200, status= "success", message= None, data= cursor.fetchone() if tipe == 1 else cursor.fetchall())
            except Exception as e:
                error_message = re.sub(' +',' ',str(e).replace('\n', ' '))
                logger.error(f"||{menu_name}|| {error_message}")
                logger.handlers.clear()
                return return_of_response(message= "Internal Server Error", message_detail= str(e))
            
    elif (running_database.upper() == "MONGODB" and __multidbstatus == "1") or (__multidbstatus == '0' and __databasetipe.upper() == "MONGODB"):
        from package_conn.conn import mongo_connection
        with mongo_connection() as cursor:
            try:
                __collection = cursor[tablename]
                __search_object_mongo = ({col:val} for col, val in zip(column_name, values) ) if column_name else {}
                if tipe == 1:
                    __result = __collection.find_one(__search_object_mongo)
                else:
                    __result = __collection.find(__search_object_mongo)
                return return_of_response(code= 200, status= "success", data= __result)
            except Exception as e:
                error_message = re.sub(' +',' ',str(e).replace('\n', ' '))
                logger.error(f"||{menu_name}|| {error_message}")
                logger.handlers.clear()
                return return_of_response(message= "Internal Server Error", message_detail= str(e))
            
    else:
        return return_of_response(message= "No selected database type")


def insert_data(running_database:str = None, tablename:str = None, column_name:list = None, values:list = None, commit_status:bool = False, menu_name:str = None):
    """
        Untuk insert data
        running_database => jenis database yang digunakan untuk melakukan query yaitu postgresql, mysql, mongodb
        tablename => nama table dalam bentuk string, pada mongodb dapat sebagai mana collection
        column_name => column yang digunakan untuk insert dalam bentuk list string seperti ["name","password"], di mongodb sebagai keys
        values => values dari insert pada column name dalam bentuk list string seperti ["name","password"], di mongodb sebagai value keys
        commit_status => jika True maka akan commit, tidak dipakai pada mongodb
        menu_name => nama menu saat melakukan query dan konek ke logger
    """
    running_database = running_database if running_database else "NO DATABASE"
    logger = LoggerAplication(tanggal= datetime.datetime.now().date()).Configuration()
    if (__databasetipe.upper() in ["POSTGRESQL","MYSQL"] and __multidbstatus == "0") or (running_database.upper() in ["POSTGRESQL","MYSQL"] and __multidbstatus == "1"):
        string_val = ", ".join(["%s"] * len(values))
        column_dec = ", ".join(f"{clm}" for clm in column_name)
        query = f"insert into  {tablename} ({column_dec}) values ({string_val})"

    if (running_database.upper() == "POSTGRESQL" and __multidbstatus == "1") or (__multidbstatus == '0' and __databasetipe.upper() == "POSTGRESQL"):
        from package_conn.conn import postgresql_connection
        with postgresql_connection(commit= True) as cursor:
            try:
                cursor.execute(query, tuple(values))
                logger.handlers.clear()
                return return_of_response(code= 200, status= "success", message= None)
            except Exception as e:
                error_message = re.sub(' +',' ',str(e).replace('\n', ' '))
                logger.error(f"||{menu_name}|| {error_message}")
                logger.handlers.clear()
                return return_of_response(message= "Internal Server Error", message_detail= str(e))
    
    elif (running_database.upper() == "MYSQL" and __multidbstatus == "1") or (__multidbstatus == '0' and __databasetipe.upper() == "MYSQL"):
        from package_conn.conn import mysql_connection
        with mysql_connection(commit= True) as cursor:
            try:
                cursor.execute(query, tuple(values))
                logger.handlers.clear()
                return return_of_response(code= 200, status= "success", message= None)
            except Exception as e:
                error_message = re.sub(' +',' ',str(e).replace('\n', ' '))
                logger.error(f"||{menu_name}|| {error_message}")
                logger.handlers.clear()
                return return_of_response(message= "Internal Server Error", message_detail= str(e))
            
    elif (running_database.upper() == "MONGODB" and __multidbstatus == "1") or (__multidbstatus == '0' and __databasetipe.upper() == "MONGODB"):
        from package_conn.conn import mongo_connection
        with mongo_connection() as cursor:
            try:
                __collection = cursor[tablename]
                __search_object_mongo = ({col:val} for col, val in zip(column_name, values) ) if column_name else {}
                logger.handlers.clear()
                __collection.insert_one(__search_object_mongo)
                return return_of_response(code= 200, status= "success", message= None)
            except Exception as e:
                error_message = re.sub(' +',' ',str(e).replace('\n', ' '))
                logger.error(f"||{menu_name}|| {error_message}")
                logger.handlers.clear()
                return return_of_response(message= "Internal Server Error", message_detail= str(e))
    else:
        return return_of_response(message= "No selected database type")

def update_data(running_database:str = None, tablename:str = None, update_column:list = None, where_column:list = None, commit_status:bool = False, values:list = None, values_filter_mongodb:list = None, menu_name:str = None):
    """
        Untuk update data
        tablename => nama table dalam bentuk string
        update_column => column yang digunakan untuk target update dalam bentuk list string seperti ["name","password"]
        where_column => colum yang digunakan menjadi where nya dimana  dalam bentuk list string seperti ["name","password"]
        values => values dari update pada column name dalam bentuk list string seperti ["name","password"]
        commit_status => jika True maka akan commit
        menu_name => nama menu saat melakukan query dan konek ke logger
    """
    running_database = running_database if running_database else "NO DATABASE"
    logger = LoggerAplication(tanggal= datetime.datetime.now().date()).Configuration()
    if (__databasetipe.upper() in ["POSTGRESQL","MYSQL"] and __multidbstatus == "0") or (running_database.upper() in ["POSTGRESQL","MYSQL"] and __multidbstatus == "1"):
        update_col = ", ".join(f"{clm} = %s " for clm in update_column)
        valid_columns = " AND ".join([f"{column}=%s" for column in where_column]) if where_column else ""

        query = f"update {tablename} set {update_col} "
        if where_column:
            query += f" WHERE {valid_columns}"

    if (running_database.upper() == "POSTGRESQL" and __multidbstatus == "1") or (__multidbstatus == '0' and __databasetipe.upper() == "POSTGRESQL"):
        from package_conn.conn import postgresql_connection
        with postgresql_connection(commit= True) as cursor:
            try:
                cursor.execute(query, tuple(values))
                logger.handlers.clear()
                return return_of_response(code= 200, status= "success", message= None)
            except Exception as e:
                error_message = re.sub(' +',' ',str(e).replace('\n', ' '))
                logger.error(f"||{menu_name}|| {error_message}")
                logger.handlers.clear()
                return return_of_response(message= "Internal Server Error", message_detail= str(e))
            
    elif (running_database.upper() == "MYSQL" and __multidbstatus == "1") or (__multidbstatus == '0' and __databasetipe.upper() == "MYSQL"):
        from package_conn.conn import mysql_connection
        with mysql_connection(commit= True) as cursor:
            try:
                cursor.execute(query, tuple(values))
                logger.handlers.clear()
                return return_of_response(code= 200, status= "success", message= None)
            except Exception as e:
                error_message = re.sub(' +',' ',str(e).replace('\n', ' '))
                logger.error(f"||{menu_name}|| {error_message}")
                logger.handlers.clear()
                return return_of_response(message= "Internal Server Error", message_detail= str(e))
            
    elif (running_database.upper() == "MONGODB" and __multidbstatus == "1") or (__multidbstatus == '0' and __databasetipe.upper() == "MONGODB"):
        from package_conn.conn import mongo_connection
        with mongo_connection() as cursor:
            try:
                __collection = cursor[tablename]
                logger.handlers.clear()
                __update_object_mongo = ({col:val} for col, val in zip(update_column, values) ) if update_column else {}
                __filtermongo = ({col:val} for col, val in zip(where_column, values_filter_mongodb) ) if where_column else {}
                __collection.update_one(__filtermongo, __update_object_mongo)
                return return_of_response(code= 200, status= "success", message= None)
            except Exception as e:
                error_message = re.sub(' +',' ',str(e).replace('\n', ' '))
                logger.error(f"||{menu_name}|| {error_message}")
                logger.handlers.clear()
                return return_of_response(message= "Internal Server Error", message_detail= str(e))
    else:
        return return_of_response(message= "No selected database type")

def delete_data(running_database:str = None, logger:str = None,tablename:str = None, delete_column:list = None, values:list = None, commit_status:bool = False, menu_name:str = None):
    """
        Untuk menghapus data
        tablename => nama table dalam bentuk string
        delete_column => colum yang digunakan menjadi where nya dimana  dalam bentuk list string seperti ["name","password"]
        values => values dari delete pada column name dalam bentuk list string seperti ["name","password"]
        commit_status => jika True maka akan commit
        menu_name => nama menu saat melakukan query dan konek ke logger
    """
    running_database = running_database if running_database else "NO DATABASE"
    logger = LoggerAplication(tanggal= datetime.datetime.now().date()).Configuration()
    if (__databasetipe.upper() in ["POSTGRESQL","MYSQL"] and __multidbstatus == "0") or (running_database.upper() in ["POSTGRESQL","MYSQL"] and __multidbstatus == "1"):
        query = f"delete from {tablename} "
        valid_columns = " AND ".join([f"{column}=%s" for column in delete_column]) if delete_column else ""
        if delete_column:
            query += f" WHERE {valid_columns}"

    if (running_database.upper() == "POSTGRESQL" and __multidbstatus == "1") or (__multidbstatus == '0' and __databasetipe.upper() == "POSTGRESQL"):
        from package_conn.conn import postgresql_connection
        with postgresql_connection(commit= True) as cursor:
            try:
                cursor.execute(query, tuple(values))
                logger.handlers.clear()
                return return_of_response(code= 200, status= "success", message= None)
            except Exception as e:
                error_message = re.sub(' +',' ',str(e).replace('\n', ' '))
                logger.error(f"||{menu_name}|| {error_message}")
                logger.handlers.clear()
                return return_of_response(message= "Internal Server Error", message_detail= str(e))
            
    elif (running_database.upper() == "MYSQL" and __multidbstatus == "1") or (__multidbstatus == '0' and __databasetipe.upper() == "MYSQL"):
        from package_conn.conn import mysql_connection
        with mysql_connection(commit= True) as cursor:
            try:
                cursor.execute(query, tuple(values))
                logger.handlers.clear()
                return return_of_response(code= 200, status= "success", message= None)
            except Exception as e:
                error_message = re.sub(' +',' ',str(e).replace('\n', ' '))
                logger.error(f"||{menu_name}|| {error_message}")
                logger.handlers.clear()
                return return_of_response(message= "Internal Server Error", message_detail= str(e))
            
    elif (running_database.upper() == "MONGODB" and __multidbstatus == "1") or (__multidbstatus == '0' and __databasetipe.upper() == "MONGODB"):
        from package_conn.conn import mongo_connection
        with mongo_connection() as cursor:
            try:
                __collection = cursor[tablename]
                logger.handlers.clear()
                __delete_object_mongo = ({col:val} for col, val in zip(delete_column, values) ) if delete_column else {}
                __collection.delete_one(__delete_object_mongo)
                return return_of_response(code= 200, status= "success", message= None)
            except Exception as e:
                error_message = re.sub(' +',' ',str(e).replace('\n', ' '))
                logger.error(f"||{menu_name}|| {error_message}")
                logger.handlers.clear()
                return return_of_response(message= "Internal Server Error", message_detail= str(e))
    else:
        return return_of_response(message= "No selected database type")
        

def validate(username:str = None, password:str = None):
    """untuk memvalidasi username dan password
    username => usrnamenya
    password => passwordnya
    
    """
    pattern = r"[^A-Za-z0-9_]"
    match = re.search(pattern, username)
    if len(str(username)) < 8:
        return return_of_response(code= 400, message= "The length of the username is less than eight character")
    elif len(str(username)) > 20:
        return return_of_response(code= 400, message= "The length of the username is more than twenty character")
    elif match:
        return return_of_response(code= 400, message= "Username have special character")
    elif any(char.isupper() for char in username):
        return return_of_response(code= 400, message= "Username must be lowercase")

    if password:
        if len(str(password)) < 8:
            return return_of_response(code= 400, message= "The length of the password is less than eight character ")
        else:
            if not any(char.isdigit() for char in password):
                password = False
                return return_of_response(code= 400, message= "Password must have one digit of number")
            if not any(char.isupper() for char in password):
                password = False
                return return_of_response(code= 400, message= "Password must have one capital letter")
            if not any(char.islower() for char in password):
                password = False
                return return_of_response(code= 400, message= "Password must have one lowercase letter")
    return return_of_response(code= 200, status= "success", message= None)

def convert_sha256(character:str = None, password_status:bool = None):
    hash_object = hashlib.sha256(character.encode())
    hex_dig = hash_object.hexdigest()   
    return "\\x"+hex_dig
    
create_main_response = return_of_response
create_additional_response = additional_response
generate_message = build_message_detail
create_headers = generate_headers
create_footers = generate_footers
multi_query = datatables_view
checking_query = check_existing_data
update_query = update_data
insert_query = insert_data
delete_query = delete_data
validate_uname_pass = validate
create_sha256  = convert_sha256