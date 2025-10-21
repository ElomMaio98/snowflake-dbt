import snowflake.connector
import os 
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class SnowflakeConnection:
    #cuida das conexões com o snowflake
    def __init__(self):
        self.account = os.getenv('SNOWFLAKE_ACCOUNT')
        self.user = os.getenv('SNOWFLAKE_USER')
        self.password = os.getenv('SNOWFLAKE_PASSWORD')
        self.database = os.getenv('SNOWFLAKE_DATABASE')
        self.schema = os.getenv('SNOWFLAKE_SCHEMA')
        self.warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
        self.connection: Optional[snowflake.connector.SnowflakeConnection] = None
    
    def execute_query(self,query: str):
        if not self.connection:
            self.connect()
    
        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results

    def connect(self):
        try:
            self.connection = snowflake.connector.connect(
                account = self.account,
                user=self.user,
                password=self.password,
                schema=self.schema,
                warehouse=self.warehouse
            )
            cursor = self.connection.cursor()
            cursor.execute(f"USE DATABASE {self.database}")
            cursor.execute(f"USE SCHEMA {self.schema}")
            cursor.close()
            return self.connection
        except Exception as e:
            raise Exception(f"Failed to connect: {e}")
        
    def close(self):
        if self.connection:
            self.connection.close()
            self.connection=None

    def __enter__(self):
        self.connect()
        return self
    
    def __exit__ (self, exc_type, exc_val, exc_tb):
        self.close()