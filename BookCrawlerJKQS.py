# -*- coding: utf-8 -*-

import os
import sys
from bs4 import BeautifulSoup

from BookCrawlerDefine import formatContent, Book, Chapter
from BookCrawlerWeb import Param, parseCommandLine, request, write2FLBP

def getChapter(url, index):
    req = request(url = url)
    req.encoding = req.apparent_encoding
    soup = BeautifulSoup(req.text.replace('<br>', '\n'), 'html.parser')
    title = soup.find_all('h1', class_ = 'pt10')[0].text.strip()
    content = soup.find_all('div', class_ = 'readcontent')[0].text
    content = formatContent(content)
    
    chapter = Chapter()
    chapter.url = url
    chapter.name = title
    chapter.content = content
    chapter.index = index
    chapter.size = len(content)
    print('\tchapter %04d: %s' %(chapter.index, title.strip()))
    return chapter

def getBook(param):
    req = request(url = param.bookUrl)
    req.encoding = req.apparent_encoding
    soup = BeautifulSoup(req.text, 'html.parser')
    title = soup.find_all('h1', class_ = 'booktitle')[0].string
    booktag = soup.find_all('p', class_ = 'booktag')[0]
    author = booktag.find_all('a', class_ = 'red')[0].string
    update = soup.find_all('p', class_ = 'booktime')[0].string[5:15]
    cover = soup.find_all('img', class_ = 'thumbnail pull-left visible-xs')[0]['src']
    introduction = soup.find_all('p', class_ = 'bookintro')[0].text
    introduction = formatContent(introduction)

    book = Book()
    book.sourceName = param.sourceName
    book.sourceUrl = param.bookUrl
    book.author = author
    book.coverUrl = cover
    book.introduction = introduction
    book.name = title
    book.sourceUpdateAt = update
    print(title)
    
    chapterIndex = 0
    page_url = param.bookUrl
    while page_url != '' and chapterIndex < param.start + param.maxChapters:
        print('page: ' + page_url)
        req = request(url = page_url)
        soup = BeautifulSoup(req.text, 'html.parser')
        chapters = soup.find(id = 'list-chapterAll')
        for chapter in chapters.find_all('dd'):
            if chapterIndex >= param.start + param.maxChapters:
                break
            if chapterIndex < param.start:
                chapterIndex += 1
                continue
            chapter_url = chapter.a['href']
            
            try:
                chapter = getChapter(chapter_url, chapterIndex)
            except BaseException as error:
                print("getChapter exception at chapterIndex: " + str(chapterIndex) + ", for error: " + repr(error))
                return book

            book.chapters.append(chapter)
            chapterIndex += 1
        next_page = soup.find_all('a', class_ = 'next')
        if next_page:
            page_url = next_page[0]['href']
        else:
            page_url = ''
    return book
    
if __name__ == '__main__':
    param = Param()
    param.bookUrl = 'http://www.youkand.com/index/635/'
    param.outputpath = './'
    param.start = 0
    param.maxChapters = 2000000
    param.sourceName = '九库全书'
    param.baseUrl = 'http://www.youkand.com'
    
    param = parseCommandLine(param)
    book = getBook(param)
    write2FLBP(book, param)
