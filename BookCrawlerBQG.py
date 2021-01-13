# -*- coding: utf-8 -*-

import os
import sys
from bs4 import BeautifulSoup

from BookCrawlerDefine import Book, Chapter, prefixOfContentLine, separatorBetweenLines
from BookCrawlerWeb import Param, parseCommandLine, request, write2FLBP

reload(sys)
sys.setdefaultencoding('utf8')

def getChapter(url, index):
    req = request(url = url)
    soup = BeautifulSoup(req.text.replace('<br>', '\n').replace('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t', ''), 'html.parser')
    title = soup.find_all('div', class_ = 'nr_title')[0].text.strip()
    content = soup.find(id = 'nr1').text.strip()
    lines = map(lambda x: x.strip(), content.split('\n'))
    lines = filter(lambda x: x != '', lines)
    content = prefixOfContentLine + (separatorBetweenLines + prefixOfContentLine).join(lines)
    
    chapter = Chapter()
    chapter.sourceUrl = url
    chapter.name = title
    chapter.content = content
    chapter.index = index
    chapter.size = len(content)
    print('\tchapter %04d: %s' %(chapter.index, title.strip()))
    return chapter

def getBook(param):
    req = request(url = param.bookUrl)
    soup = BeautifulSoup(req.text, 'html.parser')
    block_txt = soup.find_all('div', class_ = 'block_txt2')[0]
    title = block_txt.h2.string
    author = block_txt.find_all('p')[1].string.replace('作者：', '')
    update = block_txt.find_all('p')[4].string[3:13]
    cover = soup.find_all('div', class_ = 'block_img2')[0].img['src']
    introduction = soup.find_all('div', class_ = 'intro_info')[0].string
        
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
        chapters = soup.find_all('ul', class_ = 'chapter')[1]
        for chapter in chapters.find_all('li'):
            if chapterIndex >= param.start + param.maxChapters:
                break
            if chapterIndex < param.start:
                chapterIndex += 1
                continue
            chapter_url = param.baseUrl + chapter.a['href']
            chapter = getChapter(chapter_url, chapterIndex)
            book.chapters.append(chapter)
            chapterIndex += 1
        next_page = soup.find_all('span', class_ = 'right')[0]
        if next_page.a.has_attr('href'):
            page_url = param.baseUrl + next_page.a['href']
        else:
            page_url = ''
    return book
    
if __name__ == '__main__':
    param = Param()
    param.bookUrl = 'https://m.biqubu.com/book_20602/'
    param.outputpath = './'
    param.start = 0
    param.maxChapters = 2000000
    param.sourceName = '笔趣阁'
    param.baseUrl = 'https://m.biqubu.com'
    
    param = parseCommandLine(param)
    book = getBook(param)
    write2FLBP(book, param)
