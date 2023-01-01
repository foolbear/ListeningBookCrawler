# -*- coding: utf-8 -*-

import os
import sys
from bs4 import BeautifulSoup

from BookCrawlerDefine import formatContent, Book, Chapter, prefixOfContentLine, separatorBetweenLines
from BookCrawlerWeb import Param, parseCommandLine, request, write2FLBP

def getChapter(url, index, param):
    req = request(url = url)
    req.encoding = req.apparent_encoding
    soup = BeautifulSoup(req.text, 'html.parser')
    title = soup.find_all('h1', class_ = 'cont-title')[0].text.strip()
    all = soup.find_all('div', class_ = 'cont-text')[0]
    lines = []
    for line in all.find_all('p'):
        lines.append(line.text.strip())
    lines = filter(lambda x: x != '', lines)
    content = prefixOfContentLine + (separatorBetweenLines + prefixOfContentLine).join(lines)
    
    chapters = []
    chapter = Chapter()
    chapter.sourceUrl = url
    chapter.name = title
    chapter.content = content
    chapter.index = index
    chapter.size = len(content)
    chapters.append(chapter)
    print('\tchapter %04d: %s' %(chapter.index, title.strip()))

    next_content = ''
    next_page = soup.find_all('button', class_ = 'btn btn-info')[2]
    if next_page.text.strip() == '下一页':
        page_url = param.baseUrl + next_page.find_parent()['href']
        if '_' in page_url:
            next_chapters = getChapter(page_url, index+1, param)
            chapters += next_chapters
    return chapters

def getBook(param):
    req = request(url = param.bookUrl)
    req.encoding = req.apparent_encoding
    soup = BeautifulSoup(req.text, 'html.parser')
    title = soup.find_all('h1', class_ = 'book-name')[0].a.string
    author = soup.find_all('div', class_ = 'col-md-4 col-sm-6 dark')[0].string[4:]
    update = soup.find_all('h3', class_ = 'panel-title')[0].string[10:20]
    cover = param.baseUrl + soup.find_all('img', class_ = 'book-img-middel')[0]['src']
    introduction = soup.find_all('div', class_ = 'book-detail')[0].string
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
    all_chapter = soup.find('div', {'id': 'all-chapter'})
    chapters = all_chapter.find_all('div', class_ = 'row')[0]
    for chapter in chapters.find_all('div'):
        if param.start + chapterIndex >= param.maxChapters:
            break
        if chapterIndex < param.start:
            chapterIndex += 1
            continue
        chapter_url = param.baseUrl + chapter.a['href']

        try:
            chapters = getChapter(chapter_url, chapterIndex, param)
        except BaseException as error:
            print("getChapter exception at chapterIndex: " + str(chapterIndex) + ", for error: " + repr(error))
            return book

        book.chapters += chapters
        chapterIndex += len(chapters)
    return book
    
if __name__ == '__main__':
    param = Param()
    param.bookUrl = 'https://www.20dcr.com/book/cikexintiao_wenyifuxing/'
    param.outputpath = './'
    param.start = 0
    param.maxChapters = 2000000
    param.sourceName = '稻草人书屋'
    param.baseUrl = 'https://www.20dcr.com'
    
    param = parseCommandLine(param)
    book = getBook(param)
    write2FLBP(book, param)
