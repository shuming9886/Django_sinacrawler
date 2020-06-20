# Django_sinacrawler项目介绍

## 项目简介
大二（18年）时期作品，有点粗糙/捂脸。
该系统基于自然语言处理，通过爬取指定关键词的微博进行文本处理，将文本进行聚类分析（分成5类），以期得到5类事件的关键词，得出突发事件的重要信息, 并通过系统展示。 项目使用Python3.5语言，Django 框架，前端使用了 Bootstrap 框架。


## 使用介绍
1. 命令行运行：
    ```bash
    python3 manage.py runserver
    ```
2. 打开浏览器输入[http://localhost:8000/home/](http://localhost:8000/home/)。
![1.jpg](https://cdn.nlark.com/yuque/0/2020/jpeg/731832/1592640450277-48b8f9d6-8e50-4dc3-9e15-5646ad8894a4.jpeg#align=left&display=inline&height=989&margin=%5Bobject%20Object%5D&name=1.jpg&originHeight=989&originWidth=1920&size=165202&status=done&style=none&width=1920)

3. 输入关键词:苏州，点击提交，会有缓冲loading动画。中间的大框会显示已爬取的相关微博并滚动播放。底下的五个框显示通过K-Means算法分好类的微博的五个关键词，提取关键词用到了TF-IDF算法。分别点击五个框，会显示分类的微博。
