# -*- coding: utf-8 -*-

import json

flbp_postfix = '.flbp'

prefixOfContentLine = '        '
separatorBetweenLines = '\n\n'

class Book:
    def __init__(self):
        self.author = ''
        self.coverUrl = ''
        self.introduction = ''
        self.name = ''
        self.sourceName = ''
        self.sourceUrl = ''
        self.sourceUpdateAt = ''
        self.chapters = []
        
class Chapter:
    def __init__(self):
        self.index = 0
        self.content = ''
        self.name = ''
        self.sourceUrl = ''
        self.size = 0

def write2FLBP(book, param):
    path = param.outputPath + book.name + flbp_postfix
    file = open(path, 'w')
    json.dump(obj = book, fp = file, encoding = 'UTF-8', ensure_ascii = False, default = lambda x : x.__dict__, sort_keys = False, indent = 4)
    print('write2FLBP success, output file: %s' %(path))
