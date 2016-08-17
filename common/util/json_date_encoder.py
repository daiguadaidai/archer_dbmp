#-*- coding: utf-8 -*-

from time import mktime

import simplejson as json
import datetime

class JsonDateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))

        return json.JSONEncoder.default(self, obj)

def main():
    pass

if __name__ == '__main__':
    main()
