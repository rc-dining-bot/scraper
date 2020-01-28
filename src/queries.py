breakfast_insert_query = "INSERT INTO breakfast (date, self_service, western, "\
    "dim_sum_congee_noodle, asian, asian_vegetarian, malay, "\
    "halal_vegetarian, grab_and_go)"\
    "VALUES %s"

breakfast_insert_template = "(%(date)s, %(self_service)s, %(western)s, "\
    "%(dim_sum_congee_noodle)s, %(asian)s, %(asian_vegetarian)s, "\
    "%(malay)s, %(halal_vegetarian)s, %(grab_and_go)s)"

dinner_insert_query = "INSERT INTO dinner (date, self_service, western, "\
    "noodle, asian, vegetarian, malay, "\
    "soup, indian)"\
    "VALUES %s"

dinner_insert_template = "(%(date)s, %(self_service)s, %(western)s, "\
    "%(noodle)s, %(asian)s, %(vegetarian)s, "\
    "%(malay)s, %(soup)s, %(indian)s)"
