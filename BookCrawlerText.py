# -*- coding: utf-8 -*-

import os
import sys
import getopt

from BookCrawlerDefine import Book, Chapter, write2FLBP

reload(sys)
sys.setdefaultencoding('utf8')

def getBook(param):
    book = Book()
    book.sourceName = param.sourceName
    book.sourceUrl = ''
    book.coverUrl = ''
    book.introduction = ''
    book.sourceUpdateAt = ''
    
    ifile = open(param.inputFile, 'r')
    
    book.name = ifile.readline().strip()
    book.author = ifile.readline().strip()
    print(book.name)
    
    chapterIndex = 0
    line = ifile.readline()
    prefixOfContentLine = '        '
    while line and chapterIndex < param.maxChapters:
        if line.strip() != '' and line.find(prefixOfContentLine) != 0:
            chapter = Chapter()
            chapter.sourceUrl = ''
            chapter.name = line.strip()
            chapter.index = chapterIndex
            chapterIndex += 1
            print('\tchapter %04d: %s' %(chapter.index, chapter.name))
            
            content = ''
            line = ifile.readline()
            while line and (line.strip() == '' or line.find(prefixOfContentLine) == 0):
                content += line
                line = ifile.readline()
            chapter.content = prefixOfContentLine + content.strip()
            book.chapters.append(chapter)
        else:
            line = ifile.readline()
    ifile.close()
    return book
    
class Param:
    def __init__(self):
        self.inputFile = ''
        self.outputPath = './'
        self.maxChapters = 2000000
        self.sourceName = '自由文本'
    
def parseCommandLine(defaultParam):
    param = defaultParam
    usage = 'Usage: %s -i <imputfile> -o <outputpath> -m <maxchapters>' %(sys.argv[0])
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hi:o:m:', ['help', 'ifile=', 'opath=', 'max='])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for key, value in opts:
        if key in ('-h', '--help'):
            print(usage)
            sys.exit()
        elif key in ('-i', '--ifile'):
            param.inputFile = value
        elif key in ('-o', '--opath'):
            param.outputPath = value
        elif key in ('-m', '--max'):
            param.maxChapters = int(value)
    print('read book from %s, outputPath=%s, maxChapters=%d' %(param.inputFile, param.outputPath, param.maxChapters))
    return param
    
if __name__ == '__main__':
    param = Param()
    param.inputFile = ''
    param.outputpath = './'
    param.maxChapters = 2000000
    
    param = parseCommandLine(param)
    book = getBook(param)
    write2FLBP(book, param)
