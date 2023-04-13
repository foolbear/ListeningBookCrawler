# -*- coding: utf-8 -*-

import os
import sys
from bs4 import BeautifulSoup

from BookCrawlerDefine import formatContent, Book, Chapter
from BookCrawlerWeb import Param, parseCommandLine, request, write2FLBP

def getChapter(url, index):
    req = request(url = url)
    req.encoding = req.apparent_encoding
    soup = BeautifulSoup(req.text, 'html.parser')
    title = soup.find_all('div', class_ = 'h1title')[0].h1.text.strip()
    content = soup.find(id = 'htmlContent').text
    content = content[: content.find('上一页')].replace('</div>', '')
    content = formatContent(content)
    
    chapter = Chapter()
    chapter.sourceUrl = url
    chapter.name = title
    chapter.content = content
    chapter.index = index
    chapter.size = len(content)
    print('\tchapter %04d: %s' %(chapter.index, title))
    return chapter

def getBook(param):
    req = request(url = param.bookUrl)
    req.encoding = req.apparent_encoding
    soup = BeautifulSoup(req.text, 'html.parser')
    book_info = soup.find_all('div', class_ = 'book_info')[0]
    title = book_info.h1.string
    author = book_info.find_all('div', class_ = 'infos')[0].h3.string[3:]
    coverUrl = book_info.find_all('div', class_ = 'pic')[0].img['src']
    introduction = book_info.p.string
    introduction = formatContent(introduction)
        
    book = Book()
    book.sourceName = param.sourceName
    book.sourceUrl = param.bookUrl
    book.author = author
    book.coverUrl = coverUrl
    book.introduction = introduction
    book.name = title
    book.sourceUpdateAt = ''
    print(title)
    
    chapterIndex = 0
    chapters = soup.find_all('div', class_ = 'book_list boxm')[0].find_all('ul')[0]
    for chapter in chapters.find_all('li'):
        if chapterIndex >= param.start + param.maxChapters:
            break
        if chapterIndex < param.start:
            chapterIndex += 1
            continue
        chapter_url = chapter.a['href']
        chapter = getChapter(chapter_url, chapterIndex)
        book.chapters.append(chapter)
        chapterIndex += 1
    return book
    
if __name__ == '__main__':
    param = Param()
    param.bookUrl = 'http://www.dzwx520.com/book_11826/'
    param.outputpath = './'
    param.start = 0
    param.maxChapters = 2000000
    param.sourceName = '大众文学网'
    param.baseUrl = 'http://www.dzwx520.com'
    
    param = parseCommandLine(param)
    book = getBook(param)
    write2FLBP(book, param)
