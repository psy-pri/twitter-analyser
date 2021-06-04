import psycopg2
from psycopg2 import pool
from configparser import ConfigParser

# Read config.ini file
config_object = ConfigParser()
config_object.read("config.ini")

# Get the creds
creds = config_object['creds']

class Database:
    __connection_pool = None
    
    @classmethod
    def initialise(cls,**kwargs):
        cls.__connection_pool = pool.SimpleConnectionPool(1,5,**kwargs)
    
    @classmethod
    def get_connection(cls):
        return cls.__connection_pool.getconn()
    
    @classmethod
    def put_connection(cls,connection):
        cls.__connection_pool.putconn(connection)
    
    @classmethod
    def close_all_connections(cls):
        Database.__connection_pool.closeall()

class CursorFromConnectionFromPool:
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        self.connection = Database.get_connection()
        self.cursor = self.connection.cursor()
        return self.cursor
    
    def __exit__(self,exc_type, exc_value, tb):
        if exc_type is not None:
            #tb.print_exception(exc_type, exc_value, tb)
            self.connection.rollback()
        else:
            self.connection.commit()
            self.cursor.close()
        Database.put_connection(self.connection)