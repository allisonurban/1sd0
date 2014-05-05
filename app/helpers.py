import re

class helpers(object):

    def __init__(self, txt):
        self.txt = txt

    def test(self):
        return "hi!"

    def wordCount(self):
        return len(re.findall(r'\w+', self.txt))



