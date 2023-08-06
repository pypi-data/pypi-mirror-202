import os
import sys
import pandas
import psycopg2 as db_connect
import snowflake.connector as snowflake_connector
from dotenv import load_dotenv


# Load dotenv to get credential information.

load_dotenv()

class Engine(object):
    """Connection engine to get data from DB

    Args:
        query: SQL query to query data.

    Returns:
        object: Engine object which contains credential information related to the DB access.
    """

    def __init__(self, query):
        self.query = query
        function = sys._getframe().f_code.co_name
        
        # load dotenv
        self.variables = self.load_env_variables()
        
        # load credential information
        self.__credentials = {
            "host": self.variables["DB_HOST"],
            "user": self.variables["DB_USER"],
            "password": self.variables["DB_PASSWORD"],
            "database": self.variables["DB_NAME"]
        }
    
    '''
    Getter & Setter of self.__credentials
    '''
    @property
    def credentials(self):
        return self.__credentials
    
    @credentials.setter
    def credentials(self, dict):
        self.__credentials = dict

    def print_f(self, alert, message, function):
        print(alert + " | " + function + " | " + message)

    def load_env_variables(self):
        function = sys._getframe().f_code.co_name
        try:
            return os.environ
        except Exception as e:
            message = "Loading env_variables from .env Fail"
            self.print_f("Fail", message, function)
            print(e)

    def connect_database(self):
        function = sys._getframe().f_code.co_name
        try:
            connection = db_connect.connect(**self.credentials)
            self.cursor = connection.cursor()
        except Exception as e:
            message = "Connection Fail"
            self.print_f("Fail", message, function)
    
    def fetch_data(self):
        function = sys._getframe().f_code.co_name
        try:
            self.cursor.execute(self.query)
            data = self.cursor.fetchall()
            columns = []
            for elt in self.cursor.description:
                columns.append(elt[0])
            data = pandas.DataFrame(data, columns = columns)
            
            message = "Fetch data from query Success"
            self.print_f("Success", message, function)
        except Exception as e:
            message = "Fetch data Fail: " + str(e)
            self.print_f("Fail", message, function)
        return data

class SnowflakeEngine(Engine):
    def __init__(self, query):
        self.query = query
        
        # inherit from Engine
        super().__init__(query)
        
        # load credential information
        self.credentials = {
            "user": self.variables["SNOWFLAKE_USERNAME"],
            "password": self.variables["SNOWFLAKE_PASSWORD"],
            "account": self.variables["SNOWFLAKE_ACCOUNT"],
            "role": self.variables["SNOWFLAKE_ROLE"]
        }
    
    def connect_database(self):
        function = sys._getframe().f_code.co_name
        try:
            connection = snowflake_connector.connect(**self.credentials)
            self.cursor = connection.cursor()
        except Exception as e:
            message = "Connection Fail"
            self.print_f("Fail", message, function)
            print(e)