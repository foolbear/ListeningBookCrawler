# -*- coding: utf-8 -*-

postfixOfFLBP = '.flbp'

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
