# -*- coding: utf-8 -*-

import os
import sys
from bs4 import BeautifulSoup

from BookCrawlerDefine import formatContent, Book, Chapter
from BookCrawlerWeb import Param, parseCommandLine, request, write2FLBP

def getChapter(url, index):
    req = request(url = url)
#    req.encoding = req.apparent_encoding
    soup = BeautifulSoup(req.text, 'html.parser')
    title = soup.find_all('h1', class_ = 'post-title')[0].text.strip()
    content = soup.find(id = 'nr1').text.replace('💐 鲲l 弩x 小x 说s =  Ww w * k u n n u * co m', '').replace('鲲|弩|小|说|ww w |k u n n u | co M|', '').replace('🌲 鲲#弩#小#说#  ku n Nu # co m', '').replace('🍐 鲲`弩-小`说ww w ，K u n N u ，c o m', '').replace('鲲·弩+小·说 - k u n n u - c om', '').replace('鲲^弩^小^说 🌼 w w w*k u n n u*c o M *', '').replace('💑 鲲=弩=小=说~w w w =k u n n u = C om', '').replace('鲲 # 弩 # 小 # 说 #   w ww # ku n Nu # co m', '').replace('🌽 鲲~弩~小~说~w w w -k u n n u - co m', '')
    content = formatContent(content)
    
    chapter = Chapter()
    chapter.url = url
    chapter.name = title
    chapter.content = content
    chapter.index = index
    chapter.words = len(content)
    print('\tchapter %04d: %s' %(chapter.index, title))
    return chapter

def getBook(param):
    req = request(url = param.bookUrl)
    soup = BeautifulSoup(req.text, 'html.parser')
    describe = soup.find_all('div', class_ = 'book-describe')[0]
    title = describe.h1.string
    author = describe.find_all('p')[0].string[3:]
    update = describe.find_all('p')[3].string[5:]
    introduction = describe.find_all('div', class_ = 'describe-html')[0].find_all('p')[1].string
    introduction = formatContent(introduction)
        
    book = Book()
    book.sourceName = param.sourceName
    book.sourceUrl = param.bookUrl
    book.author = author
    book.coverUrl = ''
    book.introduction = introduction
    book.name = title
    book.sourceUpdateAt = update
    print(title)
    
    chapterIndex = 0
    chapters = soup.find_all('div', class_ = 'book-list clearfix')[0].find_all('ul')[0]
    for chapter in chapters.find_all('li'):
        if chapterIndex >= param.start + param.maxChapters:
            break
        if chapterIndex < param.start:
            chapterIndex += 1
            continue
        chapter_url = ''
        a = chapter.a
        if a != None:
            chapter_url = a['href']
        else:
            chapter_url = chapter.b['onclick'][13:][:-2]
            
        try:
            chapter = getChapter(chapter_url, chapterIndex)
        except BaseException as error:
            print("getChapter exception at chapterIndex: " + str(chapterIndex) + ", for error: " + repr(error))
            return book

        book.chapters.append(chapter)
        chapterIndex += 1
    return book
    
if __name__ == '__main__':
    param = Param()
    param.bookUrl = 'https://www.kunnu.com/siteng/'
    param.outputpath = './'
    param.start = 0
    param.maxChapters = 2000000
    param.sourceName = '鲲弩小说'
    param.baseUrl = 'https://www.kunnu.com'
    
    param = parseCommandLine(param)
    book = getBook(param)
    write2FLBP(book, param)
