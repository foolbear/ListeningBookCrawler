# -*- coding: utf-8 -*-

import os
import sys
from bs4 import BeautifulSoup

from BookCrawlerDefine import formatContent, Book, Chapter
from BookCrawlerWeb import Param, parseCommandLine, request, write2FLBP

def getChapter(url, index):
    chapter = Chapter()
    chapter.sourceUrl = url
    chapter.index = index + param.reindex

    nextUrl = url
    while True:
        nextUrl = getPageContent(nextUrl, chapter)
        if nextUrl == None:
            break

    chapter.size = len(chapter.content)
    print('\tchapter %04d: %s' %(chapter.index, chapter.name))
    return chapter

def getPageContent(url, chapter):
    req = request(url = url)
#    req.encoding = req.apparent_encoding
    soup = BeautifulSoup(req.text.replace('<br>', '\n').replace('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t', ''), 'html.parser')

    if chapter.name == '':
        title = soup.find_all('div', class_ = 'nr_title')[0].text.strip()
        chapter.name = title

    content = soup.find(id = 'nr1').text.replace('/p>', '').replace('ßĨQÚbu.ČŐM', '').replace('毣趣阅', '')
    content = formatContent(content)
    if chapter.content != '':
        content = content.lstrip()
    chapter.content += content

    nextUrl = soup.find(id = 'pt_next')['href']
    if '_' in nextUrl[nextUrl.rfind('/'):]:
        return param.baseUrl + nextUrl
    return None

def getBook(param):
    req = request(url = param.bookUrl)
    soup = BeautifulSoup(req.text, 'html.parser')
    block_txt = soup.find_all('div', class_ = 'block_txt2')[0]
    title = block_txt.h2.string
    author = block_txt.find_all('p')[1].string.replace('作者：', '')
    update = block_txt.find_all('p')[4].string[3:13]
    cover = soup.find_all('div', class_ = 'block_img2')[0].img['src']
    introduction = soup.find_all('div', class_ = 'intro_info')[0].string
    introduction = formatContent(introduction)
        
    book = Book()
    book.sourceName = param.sourceName
    book.sourceUrl = param.bookUrl
    book.author = author
    book.coverUrl = param.baseUrl + cover
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

        chapters = soup.find_all('ul', class_ = 'chapter')[-1]
        for chapter in chapters.find_all('li'):
            if chapterIndex >= param.start + param.maxChapters:
                break
            if chapterIndex < param.start:
                chapterIndex += 1
                continue
            chapter_url = param.baseUrl + chapter.a['href']
            
            try:
                chapter = getChapter(chapter_url, chapterIndex)
            except BaseException as error:
                print("getChapter exception at chapterIndex: " + str(chapterIndex) + ", for error: " + repr(error))
                return book

            book.chapters.append(chapter)
            chapterIndex += 1
        next_page = soup.find_all('span', class_ = 'right')[0]
        if next_page.a.has_attr('href'):
            page_url = param.baseUrl + next_page.a['href']
            if page_url.find('.html') == -1:
                page_url = ''
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
