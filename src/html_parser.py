from datetime import datetime
from html.parser import HTMLParser
from lru import LRU

LRU_CACHE_SIZE = 500
IGNORED_WORDS = set(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"])

date_to_menu_map = LRU(LRU_CACHE_SIZE)

class CalendarParser(HTMLParser):
    def __init__(
        self,
        decode_html_entities=True,
    ):

        HTMLParser.__init__(self)

        self._in_td = False
        self._ignore_data = False

        self._current_month_year = None
        self._current_day = None
        self._current_href = None

    def handle_data(self, data):
        """ Leaf of parse tree"""
        if self._in_td:
            if data.isspace() or data in IGNORED_WORDS:
                self._ignore_data = True
            elif data.isdigit():
                self._current_day = data.strip()
            else:
                # Month, year string (eg. 'August 2020')
                self._ignore_data = True
                self._current_month_year = data.strip()

    def handle_starttag(self, tag, attrs):
        """ Internal node of parse tree, on the way down"""
        if tag == 'td':
            self._in_td = True
        elif tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    self._current_href = value

    def handle_endtag(self, tag):
        """ Internal node of parse tree, on the way up"""
        if tag == 'td':
            self._in_td = False
            if self._ignore_data:
                self._ignore_data = False
            elif self._current_href is not None:
                date_string = ' '.join([self._current_day, self._current_month_year])
                formatted_date_string = datetime.strptime(date_string, '%d %B %Y')
                date_to_menu_map[formatted_date_string] = self._current_href
                self._current_href = None
