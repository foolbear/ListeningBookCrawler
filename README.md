# ListeningBookCrawler

## 目的
这个项目的目的是为了生成符合[ **“大笨熊听书”**  App](https://apps.apple.com/us/app/Foolistening/id1546690894) 需要格式化的 **“Foolbear Listening Book Package 2”** 而提供的 python 示例。您也可以使用其他语言和工具，只要生成“Foolbear Listening Book Package 2”即可。

## Foolbear Listening Book Package 2
这个格式是一个 Json 文件，其后缀是 **“.flbp2”** 。该文件可以通过类似 AirDrop 等方法导入到 **“大笨熊听书”**  App 中，即可听书。
其格式如下（[示例](https://github.com/foolbear/ListeningBookCrawler/blob/main/%E6%9D%A8%E5%B0%8F%E9%82%AA%E5%8F%91%E5%A8%81.flbp2)）：  
```json
{
    "sourceUrl": "https://m.biqubu.com/book_202/", 
    "name": "剑来", 
    "author": "烽火戏诸侯", 
    "introduction": "大千世界，无奇不有。我陈平安，唯有一剑，可搬山，倒海，降妖，镇魔，敕神，摘星，断江，摧城，开天！", 
    "coverUrl": "https://www.biqubu.com/files/article/image/0/202/202s.jpg", 
    "chapters": [
        {
            "content": "    新书的重心在于“构建一个光怪陆离却合理有趣的仙侠世界”，...", 
            "index": 0, 
            "sourceUrl": "https://m.biqubu.com/book_202/11074.html", 
            "name": "新书感言"
        }, 
        {
            "content": "    二月二，龙抬头。\n    暮色里，小镇名叫泥瓶巷的僻静地方...", 
            "index": 1, 
            "sourceUrl": "https://m.biqubu.com/book_202/11077.html", 
            "name": "第一章 惊蛰"
        }
    ], 
    "sourceName": "笔趣阁", 
    "sourceUpdateAt": "2020-12-28"
}
```

## 使用方法
### 数据源
这个项目接受两种数据源，一种是来自各大追书网站，一种是来自文本文件。

### 使用前
安装 python，安装相关模块：getopt、user_agent、json。

### 追书网站
对于各大追书网站，这里提供了两个示例：  
* BookCrawlerBQG.py:  笔趣阁（https://m.biqubu.com/）
* BookCrawlerYQHY.py: 言情花园（https://k.yqhy.org）

使用方法是：  
```shell
FoolMBP:~ foolbear$ python ~/Listening/Script/BookCrawlerBQG.py --help
FoolMBP:~ foolbear$ python ~/Listening/Script/BookCrawlerBQG.py -u https://m.biqubu.com/book_202/ -o ~/Downloads/ -m 3
```

* 对于这两个网站，基本上可以直接使用即可。您也可以根据具体书籍格式（空行数不同，段首空格不同）做些微调。  
* 对于其他追书网站，也可以在这两个示例的基础上修改，这可能需要您稍微了解下 python 的编程（很简单，我也是现学的，可能够用不够好）。

### 文本文件
对于文本文件，这里提供了一个示例：  
* BookCrawlerText.py

使用方法是：  
```shell
FoolMBP:~ foolbear$ python ~/Listening/Script/BookCrawlerText.py --help
FoolMBP:~ foolbear$ python ~/Listening/Script/BookCrawlerText.py -i ~/Downloads/杨小邪发威.txt -o ~/Downloads/ -m 3
```

它所支持的格式如下（[示例](https://github.com/foolbear/ListeningBookCrawler/blob/main/%E6%9D%A8%E5%B0%8F%E9%82%AA%E5%8F%91%E5%A8%81.txt)）：  
```text
杨小邪发威
李凉

第一章
    鬃红烈马，奔蹄如雷，旋风似地弛骋于车水马龙，繁华热闹的太原城广阔街道。...
    ...

第二章
    这一折腾回到通吃馆已是黄昏时分，万斤重之大棺材镖车，也许因风头出尽後，...
    ...

第叁章
    “五香紫烧鱼片”小顺子边念边找，除了一小部份，其他都已报销，鱼片只剩四五...
    ...
```

为了使用简单，请注意：  
* 第一行书名，第二行作者。一定填充内容，就算不知道，请注为“-”。
* 章节名前添加一行空行。
* 章节名前没有空格。
* 章节内容的每行前添加四个空格。

使用前还有几点注意：  
* 为了编码（utf-8）正确，简单的方法是：将文本文件用 Chrome 浏览器打开，并拷贝其中的内容回文本文件并保存。
* 为了符合上面的格式，推荐使用类似 Sublime Text 等工具进行格式化，善用 replace 就能完成很多的工作。

### 使用技巧
* 在使用这里的工具时，可以先加上 “-m 3” 的参数，观察三个章节的输出格式是否满意。满意之后，去掉该参数，输出所有章节。

## 联系我（foolbear@foolbear.com）
* 如果有朋友想一起完善这个项目，类似提供不同追书网站的支持，也可以联系我加入项目。  
* 如果有朋友玩不来 python，需要请求书籍或其他支持，也可以联系我，或者直接提交 Issue 让大家一起帮助您。
