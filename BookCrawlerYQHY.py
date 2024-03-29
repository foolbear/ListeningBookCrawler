# -*- coding: utf-8 -*-

import os
import sys
from bs4 import BeautifulSoup

from BookCrawlerDefine import formatContent, Book, Chapter
from BookCrawlerWeb import Param, parseCommandLine, request, write2FLBP

def getChapter(url, index, param):
    req = request(url = url)
    req.encoding = req.apparent_encoding
    soup = BeautifulSoup(req.text, 'html.parser')
    title = soup.find_all('div', class_ = 'nr_title')[0].text.strip()
    content = soup.find_all('div', class_ = 'nr_nr')[0].text.strip().replace('    ', '\n\n')
    content = content[:content.find('-->>')]
    content = formatContent(content)
    
    chapters = []
    chapter = Chapter()
    chapter.url = url
    chapter.name = title
    chapter.content = content
    chapter.index = index
    chapter.words = len(content)
    chapters.append(chapter)
    print('\tchapter %04d: %s' %(chapter.index, title.strip()))

    next_content = ''
    navigators = soup.find_all('div', class_ = 'nr_page')[1]
    next_page = navigators.find(text = '下一章')
    if next_page != None:
        page_url = param.baseUrl + next_page.find_parent()['href']
        if '_' in page_url:
            next_chapters = getChapter(page_url, index+1, param)
            chapters += next_chapters
    return chapters

def getBook(param):
    req = request(url = param.bookUrl)
    soup = BeautifulSoup(req.text, 'html.parser')
    block_txt = soup.find_all('div', class_ = 'block_txt')[0]
    title = block_txt.h2.string
    author = block_txt.p.a.string
    update = list(block_txt.children)[7].string[5:15]
    cover = soup.find_all('div', class_ = 'block_img')[0].img['src']
    introduction = soup.find_all('div', class_ = 'intro')[0].string
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
    page_url = param.baseUrl + soup.find_all('a', class_ = 'tc')[0]['href']
    while page_url != '' and param.start + chapterIndex < param.maxChapters:
        print('page: ' + page_url)
        req = request(url = page_url)
        soup = BeautifulSoup(req.text, 'html.parser')
        chapters = soup.find_all('ul', class_ = 'block list')[0]
        for chapter in chapters.find_all('li'):
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
        navigators = soup.find_all('div', class_ = 'page')[0]
        next_page = navigators.find(text = '下一页')
        if next_page != None:
            page_url = param.baseUrl + next_page.find_parent()['href']
        else:
            page_url = ''
    return book
    
if __name__ == '__main__':
    param = Param()
    param.bookUrl = 'https://m.yqhyy.com/read/1/1302/'
    param.outputpath = './'
    param.start = 0
    param.maxChapters = 2000000
    param.sourceName = '言情花园'
    param.baseUrl = 'https://m.yqhyy.com'
    
    param = parseCommandLine(param)
    book = getBook(param)
    write2FLBP(book, param)
