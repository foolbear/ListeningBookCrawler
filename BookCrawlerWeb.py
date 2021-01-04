# -*- coding: utf-8 -*-

import sys
import getopt
import requests
from user_agent import generate_user_agent
        
request_timeout = 60

class Param:
    def __init__(self):
        self.bookUrl = ''
        self.outputPath = './'
        self.maxChapters = 2000000
        self.sourceName = ''
        self.baseUrl = ''

def parseCommandLine(defaultParam):
    param = defaultParam
    usage = 'Usage: %s -u <url> -o <outputpath> -m <maxchapters>' %(sys.argv[0])
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hu:o:m:', ['help', 'url=', 'opath=', 'max='])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for key, value in opts:
        if key in ('-h', '--help'):
            print(usage)
            sys.exit()
        elif key in ('-u', '--url'):
            param.bookUrl = value
        elif key in ('-o', '--opath'):
            param.outputPath = value
        elif key in ('-m', '--max'):
            param.maxChapters = int(value)
    print('request book from %s(%s), outputPath=%s, maxChapters=%d' %(param.sourceName, param.bookUrl, param.outputPath, param.maxChapters))
    return param

def request(url):
    userAgent = generate_user_agent()
    referrer = 'http://shurufa.baidu.com/dict.html'
    headers = {'User-Agent': userAgent, 'Referer': referrer}
    try:
        response = requests.get(url, timeout = request_timeout, headers = headers)
        if response.status_code == 200:
            return response
        else:
            raise Exception('response for ' + url + ', status_code = ' + str(response.status_code))
    except requests.exceptions.RequestException as e:
        raise Exception('exception when request ' + url + ', ' + str(e))
