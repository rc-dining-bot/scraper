from dotenv import load_dotenv
import os
import datetime
import logging

import menu_downloader
import parser
from database import Database


def get_menu(start_date, num_days, db):
    '''download, parse and upload menu to mongodb'''
    breakfast_ops = []
    dinner_ops = []
    for i in range(num_days):
        date_to_search = start_date + datetime.timedelta(days=i)
        # add exception
        file_name = menu_downloader.download_menu_pdf(
            date_to_search)

        if not file_name:
            logging.error(f'No menu available on {str(date_to_search)}')
            continue

        breakfast, dinner = parser.parse_menu(file_name)
        if breakfast:
            breakfast_ops.append(breakfast)
        else:
            logging.warning(f"No breakfast available on {str(date_to_search)}")

        if dinner:
            dinner_ops.append(dinner)
        else:
            logging.warning(f"No dinner available on {str(date_to_search)}")

        os.remove(file_name)

    db.breakfast_insert_many(breakfast_ops)
    db.dinner_insert_many(dinner_ops)


if __name__ == '__main__':
    load_dotenv()
    # logging.basicConfig(level=logging.WARNING)
    db = Database()
    get_menu(datetime.date.today(), 7, db)  # run on sundays
