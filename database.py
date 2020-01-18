import pymongo
import logging
import os


class Database:
    def __init__(self):
        self.connect_to_database()

    def connect_to_database(self):
        self.client = pymongo.MongoClient(f"{os.getenv('MONGODB_URL')}")
        self.db = self.client.mealbot
        logging.info('Connected to database successfully')
        return self.db

    def breakfast_insert_many(self, ops):
        self.db.breakfast.insert_many(ops)
        logging.info('Inserted to breakfast successfully')

    def dinner_insert_many(self, ops):
        self.db.dinner.insert_many(ops)
        logging.info('Inserted to dinner successfully')
