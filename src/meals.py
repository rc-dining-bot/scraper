class Breakfast:
    def __init__(self, df, date):
        """hardcode mapping of value to key"""
        self.date = date
        self.populate_data(df.values)

    def populate_data(self, data):
        self.add_day(data)
        self.add_self_service(data)
        self.add_western(data)
        self.add_dim_sum_congee_noodle(data)
        self.add_asian(data)
        self.add_asian_vegetarian(data)
        self.add_malay(data)
        self.add_halal_vegetarian(data)
        self.add_grab_and_go(data)

    def add_day(self, data):
        self.day = data[0][1]

    def add_self_service(self, data):
        self.self_service = collect_data_range(1, 5, data)

    def add_western(self, data):
        self.western = collect_data_range(6, 11, data)

    def add_dim_sum_congee_noodle(self, data):
        self.dim_sum_congee_noodle = collect_data_range(12, 13, data)

    def add_asian(self, data):
        self.asian = collect_data_range(14, 17, data)

    def add_asian_vegetarian(self, data):
        self.asian_vegetarian = collect_data_range(18, 21, data)

    def add_malay(self, data):
        self.malay = collect_data_range(22, 25, data)

    def add_halal_vegetarian(self, data):
        self.halal_vegetarian = collect_data_range(26, 29, data)

    def add_grab_and_go(self, data):
        for i in range(31, 36):
            data[i][1] = data[i][0]  # clean data
        self.grab_and_go = collect_data_range(30, 36, data)


class Dinner:
    def __init__(self, df, date):
        """hardcode mapping of value to key"""
        self.populate_data(df.values)
        self.date = date

    def populate_data(self, data):
        self.add_day(data)
        self.add_self_service(data)
        self.add_western(data)
        self.add_noodle(data)
        self.add_asian(data)
        self.add_vegetarian(data)
        self.add_malay(data)
        self.add_indian(data)
        self.add_soup(data)

    def add_day(self, data):
        self.day = data[0][1]

    def add_self_service(self, data):
        self.self_service = collect_data_range(1, 5, data)

    def add_western(self, data):
        self.western = collect_data_range(6, 9, data)

    def add_noodle(self, data):
        self.noodle = collect_data_range(11, 12, data)

    def add_asian(self, data):
        self.asian = collect_data_range(13, 18, data)

    def add_vegetarian(self, data):
        self.vegetarian = collect_data_range(20, 24, data)

    def add_malay(self, data):
        self.malay = collect_data_range(25, 30, data)

    def add_indian(self, data):
        for i in range(33, 38):
            data[i][1] = data[i][0]  # clean data
        self.indian = collect_data_range(32, 38, data)

    def add_soup(self, data):
        soup = set()  # sometimes have same soup
        indices = [9, 18, 30]
        for i in indices:
            soup_item = data[i][1]
            if isinstance(soup_item, str):
                soup.add(soup_item)
        self.soup = list(soup)


def collect_data_range(start_index, end_index, data):
    arr = []
    for i in range(start_index, end_index):
        food_item = data[i][1]
        if isinstance(food_item, str):
            arr.append(data[i][1])
    return arr
