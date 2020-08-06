from tabula import read_pdf


def parse_menu(file_name, date_to_search):
    """returns a tuple of breakfast and dinner json objects"""
    df = parse_menu_to_df(file_name)
    date = date_to_search.strftime('%y%m%d')
    day_of_week = date_to_search.weekday()
    # sundays don't have breakfast
    if (day_of_week == 6): 
        breakfast = None
    else:
        breakfast = parse_df_for_breakfast(df[0], date)

    # saturdays don't have dinner.
    if day_of_week == 5:
        dinner = None
    # but sundays only have dinner, so index needs to be 0
    elif day_of_week == 6:
        dinner = parse_df_for_dinner(df[0], date)
    else:
        dinner = parse_df_for_dinner(df[1], date)

    return breakfast, dinner

def parse_menu_to_df(file_name):
    """returns a dataframe containing the breakfast and dinner menus"""
    df = read_pdf(file_name, pages='1', multiple_tables=True, lattice=True)
    return df


def parse_df_for_breakfast(df, date):
    """returns a json object containing the breakfast menu"""
    if len(df) < 36:  # no menu
        return None

    return extract_breakfast(df.values, date)


def parse_df_for_dinner(df, date):
    """returns a json object containing the dinner menu"""
    if len(df) < 38:  # no menu
        return None

    return extract_dinner(df.values, date)


def extract_breakfast(data, date):
    breakfast = {'date': date,
                 'self_service': extract_food_items(1, 5, data),
                 'western': extract_food_items(6, 11, data),
                 'dim_sum_congee_noodle': extract_food_items(12, 13, data),
                 'asian': extract_food_items(14, 17, data),
                 'asian_vegetarian': extract_food_items(18, 21, data),
                 'malay': extract_food_items(22, 25, data),
                 'halal_vegetarian': extract_food_items(26, 29, data)
                 }

    # Tabula can't parse the last item correctly
    # We clean it up ourselves
    for i in range(31, 36):
        data[i][1] = data[i][0]
    breakfast['grab_and_go'] = extract_food_items(30, 36, data)

    return breakfast


def extract_dinner(data, date):
    dinner = {'date': date,
              'self_service': extract_food_items(1, 5, data),
              'western': extract_food_items(6, 9, data),
              'noodle': extract_food_items(11, 12, data),
              'asian': extract_food_items(13, 18, data),
              'vegetarian': extract_food_items(20, 24, data),
              'malay': extract_food_items(25, 30, data),
              'soup': extract_soup(data)
              }

    # Tabula can't parse the last item correctly
    # We clean it up ourselves
    for i in range(33, 38):
        data[i][1] = data[i][0]
    dinner['indian'] = extract_food_items(32, 38, data)

    return dinner


def extract_soup(data):
    soup = set()  # sometimes have same soup
    indices = [9, 18, 30]
    for i in indices:
        soup_item = data[i][1]
        if isinstance(soup_item, str):
            soup.add(soup_item)
    return list(soup)


def extract_food_items(start_row, end_row, data):
    arr = []
    for i in range(start_row, end_row):
        # Food items are always in the second column
        food_item = data[i][1]
        # Ignore empty cells
        if isinstance(food_item, str):
            arr.append(food_item)
    return arr
