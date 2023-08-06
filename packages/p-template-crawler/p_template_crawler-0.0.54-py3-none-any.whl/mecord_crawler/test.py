import json
import urllib.parse

from lxml import etree

if __name__ == '__main__':
    value1 = "1"
    value2 = "2"
    s3 = "xxxx {1} xxx{0}".format(value1, value2)
    print(s3)

    # cursor: int = 234
    # o2 = f'''{
    #     "json": {
    #         "period": "Day",
    #         "sort": "Newest",
    #         "modelId": 7240,
    #         "limit": 50,
    #         "cursor": {cursor}
    #     }
    # }'''

    pp = '''{
            "period": "Day",
            "sort": "Newest",
            "modelId": %d,
            "limit": 50,
            "cursor": %d
        }''' % (1,1)
    print(pp)
    s2 = "xxxx {age} xxxx {name}".format(age=18, name="hangman")
    print(s2)
    # pp.format(c=1)

    # p = {
    #     "json": {
    #         "period": "Day",
    #         "sort": "Newest",
    #         "modelId": 7240,
    #         "limit": 50,
    #         "cursor": 'null'
    #     },
    #     # "meta": {
    #     #     "values": {
    #     #         "cursor": [
    #     #             "undefined"
    #     #         ]
    #     #     }
    #     # }
    # }
    #
    # pp = {
    #     "input": p
    # }
    #
    # o = {"json":{"period":"Day","sort":"Newest","modelId":7240,"limit":50,"cursor":"null"},"meta":{"values":{"cursor":["undefined"]}}}
    # o = {"input":o}
    #
    #
    # # k = '{"json":{"period":"Day","sort":"Newest","modelId":7240,"limit":50,"cursor":null},"meta":{"values":{"cursor":["undefined"]}}}'
    # #
    # # kk = urllib.parse.urlencode(k)
    # # print(kk)
    #
    # # i = '{"json":{"period":"Day","sort":"Newest","modelId":7240,"limit":50,"cursor":null},"meta":{"values":{"cursor":["undefined"]}}}'
    # #
    # # ii = json.load(i)
    # # print(ii)
    #
    # # jsonData = '{"a":1,"b":2,"c":3,"d":4,"e":5}'
    #
    # # text = json.loads(jsonData)
    # # print(text)
    #
    # # v = json.dumps(p)
    # v = urllib.parse.urlencode(pp)
    #
    # # j = 'input=%7B%22json%22%3A%7B%22period%22%3A%22Day%22%2C%22sort%22%3A%22Newest%22%2C%22modelId%22%3A7240%2C%22limit%22%3A50%2C%22cursor%22%3Anull%7D%2C%22meta%22%3A%7B%22values%22%3A%7B%22cursor%22%3A%5B%22undefined%22%5D%7D%7D%7D',
    # j = '''input=%7B%22json%22%3A%7B%22period%22%3A%22Day%22%2C%22sort%22%3A%22Newest%22%2C%22modelId%22%3A7240%2C%22limit%22%3A50%2C%22cursor%22%3Anull%7D%2C%22meta%22%3A%7B%22values%22%3A%7B%22cursor%22%3A%5B%22undefined%22%5D%7D%7D%7D'''
    # jj = urllib.parse.unquote(v)
    # # jj = urllib.parse.unquote(j)
    # print(jj)
    # h= 'input={\'json\':+{\'period\':+\'Day\',+\'sort\':+\'Newest\',+\'modelId\':+7240,+\'limit\':+50,+\'cursor\':+\'null\'}}'
    # hh = urllib.parse.urlencode(jj)
    # print(hh)
    #
    # print(v)

