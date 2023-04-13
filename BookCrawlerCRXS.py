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
    title = soup.find_all('div', class_ = 'chapter')[0].text.strip()
    paragraphs = soup.find_all('div', class_ = 'fiction')[0].find_all('p')
    content = ''
    for paragraph in paragraphs:
        content += paragraph.text + '\n'
    content = formatContent(content)
    
    chapter = Chapter()
    chapter.url = url
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
    title = soup.find_all('div', class_ = 'title')[0].string.strip()
    coverUrl = param.baseUrl + soup.find_all('img', class_ = 'cover')[0]['src']
    introduction= soup.find_all('div', class_ = 'brief')[0].string[3:]
    introduction = formatContent(introduction)
        
    book = Book()
    book.sourceName = param.sourceName
    book.sourceUrl = param.bookUrl
    book.author = '佚名'
    book.coverUrl = coverUrl
    book.introduction = introduction
    book.name = title
    book.sourceUpdateAt = ''
    print(title)
    
    chapterIndex = 0
    chapters = soup.find_all('div', class_ = 'chapters')[0]
    for chapter in chapters.find_all('div'):
        if chapterIndex >= param.start + param.maxChapters:
            break
        if chapterIndex < param.start:
            chapterIndex += 1
            continue
        chapter_url = param.baseUrl + chapter.a['href']
        chapter = getChapter(chapter_url, chapterIndex)
        book.chapters.append(chapter)
        chapterIndex += 1
    return book
    
if __name__ == '__main__':
    param = Param()
    param.bookUrl = 'https://crxs.me/fiction/id-604b512f8c79d.html'
    param.outputpath = './'
    param.start = 0
    param.maxChapters = 2000000
    param.sourceName = '成人小说'
    param.baseUrl = 'https://crxs.me'
    
    param = parseCommandLine(param)
    book = getBook(param)
    write2FLBP(book, param)
