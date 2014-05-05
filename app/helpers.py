import re
from datetime import datetime, date

class helpers(object):

    def __init__(self, txt):
        self.txt = txt

    def userShouldWrite(self):
        if self.txt is None:
            return True
        return self.txt.published_date.date() < date.today()

    def wordCount(self):
        return len(re.findall(r'\w+', self.txt))



