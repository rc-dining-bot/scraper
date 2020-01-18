from tabula import read_pdf
import json
from datetime import datetime

from meals import Breakfast, Dinner


def parse_menu(file_name):
    '''returns a tuple of breakfast and dinner json objects'''
    df = parse_menu_to_df(file_name)
    date = parse_file_name_for_date(file_name)
    breakfast = parse_df_for_breakfast(df, date)
    dinner = parse_df_for_dinner(df, date)

    return (breakfast, dinner)


def parse_file_name_for_date(file_name):
    name = file_name.split('/')[-1]
    date_str = name[:6]
    return date_str


def parse_menu_to_df(file_name):
    '''returns a dataframe containing the breakfast and dinner menus'''
    df = read_pdf(file_name, pages='1', multiple_tables=True)
    return df


def parse_df_for_breakfast(df, date):
    '''returns a json object containing the breakfast menu'''
    breakfast_df = df[0]
    if len(breakfast_df) < 36:  # no menu
        return None

    breakfast = Breakfast(breakfast_df, date)
    return breakfast.__dict__


def parse_df_for_dinner(df, date):
    '''returns a json object containing the dinner menu'''
    dinner_df = df[1]
    if len(dinner_df) < 38:  # no menu
        return None

    dinner = Dinner(dinner_df, date)
    return dinner.__dict__
