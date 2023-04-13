# -*- coding: utf-8 -*-

import os
import sys
from bs4 import BeautifulSoup

from BookCrawlerDefine import formatContent, Book, Chapter
from BookCrawlerWeb import Param, parseCommandLine, request, write2FLBP

def getChapter(url, index):
    req = request(url = url)
    soup = BeautifulSoup(req.text.replace('<br />', '\n'), 'html.parser')
    title = soup.find_all('div', class_ = 'bookname')[0].h1.string.strip()
    content = soup.find(id = 'content').text.replace(u'\xa0\xa0\xa0\xa0', '')
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
    soup = BeautifulSoup(req.text, 'html.parser')
    box_con = soup.find_all('div', class_ = 'box_con')[0]
    info = box_con.find(id = 'info')
    title = info.h1.string
    ps = info.find_all('p')
    author = ps[0].string.strip()[5:]
    update = ps[2].string.strip()[5:]
    cover = box_con.find(id = 'fmimg').img['src']
    introduction = box_con.find(id = 'intro').find_all('p')[0].text
    introduction = formatContent(introduction)
        
    book = Book()
    book.sourceName = param.sourceName
    book.sourceUrl = param.bookUrl
    book.author = author
    book.coverUrl = cover
    book.introduction = ""
    book.name = title
    book.sourceUpdateAt = update
    print(title)
    
    chapterIndex = 0
    page_url = param.bookUrl
    chapters = soup.find(id = 'list').dl
    for chapter in chapters.find_all('dd'):
        if chapterIndex >= param.start + param.maxChapters:
            break
        if chapterIndex < param.start:
            chapterIndex += 1
            continue
        chapter_url = param.bookUrl + chapter.a['href']
        chapter = getChapter(chapter_url, chapterIndex)
        book.chapters.append(chapter)
        chapterIndex += 1
    return book
    
if __name__ == '__main__':
    param = Param()
    param.bookUrl = 'http://www.quanben.me/ls-21969/'
    param.outputpath = './'
    param.start = 0
    param.maxChapters = 2000000
    param.sourceName = '全本小说网'
    param.baseUrl = 'http://www.quanben.me/'
    
    param = parseCommandLine(param)
    book = getBook(param)
    write2FLBP(book, param)
