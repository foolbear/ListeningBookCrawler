# -*- coding: utf-8 -*-

import json

flbp_postfix = '.flbp'
text_postfix = '.txt'

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
        
def write2Text(book, param):
    path = param.outputPath + book.name + text_postfix
    file = open(path, 'w')
    file.write(book.name + '\n' + book.author + '\nfrom ' + book.sourceUrl + '\n\n')
    for chapter in book.chapters:
        content = chapter.name + '\n\n' + chapter.content + '\n\n'
        file.write(content)
    file.close()
    print('write2Text Success, output file: %s' %(path))

def write2FLBP(book, param):
    path = param.outputPath + book.name + flbp_postfix
    file = open(path, 'w')
    json.dump(obj = book, fp = file, encoding = 'UTF-8', ensure_ascii = False, default = lambda x : x.__dict__, sort_keys = False, indent = 4)
    print('write2FLBP success, output file: %s' %(path))
