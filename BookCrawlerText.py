# -*- coding: utf-8 -*-

import os
import sys
import json
import getopt

from BookCrawlerDefine import Book, Chapter, postfixOfFLBP, prefixOfContentLine, separatorBetweenLines

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
    chapterName = ''
    chpaterContent = ''
    line = ifile.readline()
    while line and chapterIndex < param.maxChapters:
        if line.strip() != '' and line.startswith('  ') == False:
            name = line.strip()
            content = ''
            line = ifile.readline()
            while line and (line.strip() == '' or line.startswith('  ') == True or line.startswith('\t') == True):
                if line.strip() != '':
                    content += prefixOfContentLine + line.strip() + separatorBetweenLines
                line = ifile.readline()
                
            if name == chapterName:
                chapterContent += content
            else:
                if chapterName != '' and  chapterContent != '':
                    chapter = Chapter()
                    chapter.index = chapterIndex
                    chapter.name = chapterName
                    chapter.content = chapterContent
                    chapter.words = len(chapter.content)
                    chapter.url = ''
                    book.chapters.append(chapter)
                    print('\tchapter %04d: %s' %(chapter.index, chapter.name))
                    chapterIndex += 1
                chapterName = name
                chapterContent = content
        else:
            line = ifile.readline()
        
    if chapterName != '' and  chapterContent != '':
        chapter = Chapter()
        chapter.index = chapterIndex
        chapter.name = chapterName
        chapter.content = chapterContent
        chapter.words = len(chapter.content)
        chapter.url = ''
        book.chapters.append(chapter)
        print('\tchapter %04d: %s' %(chapter.index, chapter.name))
        chapterIndex += 1
    
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
    if False == param.outputPath.endswith('/'):
        param.outputPath += '/'
    print('read book from %s, outputPath=%s, maxChapters=%d' %(param.inputFile, param.outputPath, param.maxChapters))
    return param

def write2FLBP(book, param):
    path = param.outputPath + book.name + '_m' + str(param.maxChapters) + postfixOfFLBP
    with open(path, 'w') as file:
        json.dump(obj = book, fp = file, ensure_ascii = False, default = lambda x : x.__dict__, sort_keys = False, indent = 4)
    print('write2FLBP success, output file: %s' %(path))
    
if __name__ == '__main__':
    param = Param()
    param.inputFile = ''
    param.outputpath = './'
    param.maxChapters = 2000000
    
    param = parseCommandLine(param)
    book = getBook(param)
    write2FLBP(book, param)
