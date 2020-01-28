import datetime
import logging
import os
from argparse import ArgumentParser

from dotenv import load_dotenv

import menu_downloader
from database import connect, breakfast_insert_many, dinner_insert_many
from parser import parse_menu


def get_menu(start_date, num_days):
    """download, parse and upload menu to mongodb"""
    breakfast_ops = []
    dinner_ops = []
    for i in range(num_days):
        date_to_search = start_date + datetime.timedelta(days=i)
        # add exception
        file_name = menu_downloader.download_menu_pdf(date_to_search)

        if not file_name:
            logging.error(f'No menu available on {str(date_to_search)}')
            continue

        breakfast, dinner = parse_menu(file_name)
        if breakfast:
            breakfast_ops.append(breakfast)
        else:
            logging.warning(f"No breakfast available on {str(date_to_search)}")

        if dinner:
            dinner_ops.append(dinner)
        else:
            logging.warning(f"No dinner available on {str(date_to_search)}")

        os.remove(file_name)

    breakfast_insert_many(breakfast_ops)
    dinner_insert_many(dinner_ops)


if __name__ == '__main__':
    # Parse command-line options
    date_format = '%Y-%m-%d'
    parser = ArgumentParser(description='Scrape RC meal menus')
    parser.add_argument('-L', '--loglevel', default='INFO',
                        choices=['CRITICAL', 'ERROR',
                                 'WARNING', 'INFO', 'DEBUG'],
                        help='The logging level')
    parser.add_argument('-s', '--start-date',
                        default=datetime.date.today().strftime(date_format),
                        help='Date to start scraping menus in YYYY-MM-DD format')
    parser.add_argument('-d', '--days', type=int, default=7,
                        help='Number of days to scrape menu')
    args = parser.parse_args()

    numeric_loglevel = getattr(logging, args.loglevel)
    start_date = datetime.datetime.strptime(args.start_date, date_format)
    days = args.days

    load_dotenv()
    logging.basicConfig(
        format='%(asctime)s-%(levelname)s: %(message)s', level=numeric_loglevel)
    logging.info(
        f'Scraping meal menus for {days} days starting from {start_date.strftime(date_format)}')
    connect()
    get_menu(start_date, days)
