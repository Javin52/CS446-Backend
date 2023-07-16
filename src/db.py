import mysql.connector
import os
import logging
from env import DB_USER, DB_NAME, DB_PASSWORD, DB_HOST, DB_PORT

class database:
    def __init__(self):
        try:
            USER = DB_USER
            PASSWORD = DB_PASSWORD
            HOST = DB_HOST
            PORT = DB_PORT
        except:
            print("Could not access env vars")
            return "Internal Server Error"
    
        db = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            port=PORT,
            database=DB_NAME
        )
        db.autocommit = True
        self.db = db
    
    def execute(self, query, params, expectoutput=True):
        cursor = self.db.cursor()
        logging.info("STARTING QUERY")
        cursor.execute(query, params)
        if expectoutput:
            results = cursor.fetchall() #VERY INNEFICIENT LOADS EVERYTHING INTO MEMORY
            logging.info("QUERY RESULT")
            logging.info(results)
            return results
