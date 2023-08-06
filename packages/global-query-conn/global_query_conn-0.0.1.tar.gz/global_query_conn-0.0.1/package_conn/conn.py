
from configparser import ConfigParser
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import register_inet
from psycopg2.pool import ThreadedConnectionPool
from urllib.parse import urlparse
import psycopg2
from contextlib import contextmanager
import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
from pymongo import MongoClient

__all__ = [
    "create_connection"
]

__config = ConfigParser()
__config.read('config.ini')

@contextmanager
def postgresql_connection(commit=False):
    try:
        __connectionhost = __config.get("postgresql","host")
        __connectionport = __config.get("postgresql","port")
        __connectionuser = __config.get("postgresql","user")
        __connectionpassword = __config.get("postgresql","password")
        __connectiondatabase = __config.get("postgresql","database")
        pool = ThreadedConnectionPool(1, 500,
            database = __connectiondatabase,
            user = __connectionuser,
            password = __connectionpassword,
            host = __connectionhost,
            port = __connectionport,
            connect_timeout=5)
        
        @contextmanager
        def postgres_connection_pool():
            try:
                connection = pool.getconn()
                yield connection
            finally:
                pool.putconn()

        with postgres_connection_pool() as connection:
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            try:
                yield cursor
                if commit:
                    connection.commit()
            finally:
                cursor.close()
    except Exception as e:
        response = {'status':'error','message':"Offline "+str(e)}
        return response

@contextmanager
def mysql_connection(commit = False):
    try:
        __connectionhost = __config.get("mysql","host")
        __connectionport = __config.get("mysql","port")
        __connectionuser = __config.get("mysql","user")
        __connectionpassword = __config.get("mysql","password")
        __connectiondatabase = __config.get("mysql","database")
        pool = MySQLConnectionPool(pool_name="mypool",
                            pool_size=10,
                            database= __connectiondatabase,
                            user= __connectionuser,
                            password= __connectionpassword,
                            host= __connectionhost)
        @contextmanager
        def mysql_connection_pool():
            try:
                connection = pool.get_connection()
                yield connection
            finally:
                pool.add_connection()
        
        with mysql_connection_pool() as connection:
            cursor = connection.cursor(dictionary=True)
            try: 
                yield cursor
                if commit:
                    connection.commit()
            finally:
                cursor.close()
    except Exception as e:
        response = {'status':'error','message':"Offline "+str(e)}
        return response

@contextmanager
def mongo_connection():
    __mongourl = __config.get("mongodb","mongourl")
    __connectionuser = __config.get("mongodb","user")
    __connectionpassword = __config.get("mongodb","password")
    __connectiondatabase = __config.get("mongodb","database")
    try:
        client = MongoClient(__mongourl, maxPoolSize=10)
        db = client[__connectiondatabase]
        db.authenticate(__connectionuser, __connectionpassword)
        yield db
    except Exception as e:
        response = {'status':'error','message':"Offline "+str(e)}
        return response

connection_postgresql = postgresql_connection
connection_mysql = mysql_connection
conncetion_mongodb = mongo_connection