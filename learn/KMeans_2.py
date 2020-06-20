import random
from math import sqrt
import jieba
import re
import math
import jieba.posseg as psg

import win_unicode_console
win_unicode_console.enable()


#TF-IDF计算关键词
def cal(term_sum,lst):
    word_freq = {}
    for sentence in lst:
        for word in sentence:
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1

    for key in word_freq:
        word_freq[key] = word_freq[key]/term_sum

    for key in word_freq:
        word_freq[key] = word_freq[key] * math.log((term_sum / (wordcount(key, lst) + 1)))

    # 返回列表
    dict1 = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

    return dict1


def wordcount(word,list):
    count=0
    for i in list:
        if word in set(i):
            count=count+1
        else:
            continue
    return count

def pearson(v1,v2):
    #简单求和
    sum1=sum(v1)
    sum2=sum(v2)

    #求平方和
    sum1Sq=sum([pow(v,2) for v in v1])
    sum2Sq=sum([pow(v,2) for v in v2])

    #求乘积之和
    pSum=sum([v1[i]*v2[i] for i in range(len(v1))])

    #计算r(Pearson score)
    num=pSum-(sum1*sum2/(len(v1)))
    den=sqrt((sum1Sq-pow(sum1,2)/len(v1))*(sum2Sq-pow(sum2,2)/len(v1)))

    if(den==0):
        return 0

    return 1.0-num/den



def kcluster(rows,distance=pearson,k=5):
    #计算每一个单词使用次数的最大值和最小值
    ranges=[(min([row[i] for row in rows]),max(row[i] for row in rows)) for i in range(len(rows[0]))]

    #随机创建k个中心点
    clusters=[[random.random()*(ranges[i][1]-ranges[i][0])+ranges[i][0] for i in range(len(rows[0]))] for j in range(k)]

    lastmatches=None
    for t in range(100):
        print("Iteration %d" %t)

        #存储与中心点最近的实例点的下标
        bestmatches=[[] for i in range(k)]
        for j in range(len(rows)):
            row=rows[j]
            bestmatch=0
            for i in range(k):
                d=distance(clusters[i],row)
                if(d<distance(clusters[bestmatch],row)):
                    bestmatch=i
            bestmatches[bestmatch].append(j)

        #判断这一轮循环得到的距离每个中心点最近的实例点与上一轮得到的距离每个中心点最近的实例点是否相同，如果相同停止循环，否则继续
        if(bestmatches==lastmatches):
            break
        lastmatches=bestmatches
        for i in range(k):
            avgs=[0.0]*len(rows[0])
            if(len(bestmatches[i])>0):
                for rowid in bestmatches[i]:
                    #先求和
                    for m in range(len(rows[rowid])):
                        avgs[m]+=rows[rowid][m]
                    #再除以实例点的个数
                    for j in range(len(avgs)):
                        avgs[i]/=len(bestmatches[i])
                    clusters[i]=avgs

    return bestmatches

def KMeans(text):

    # 加载停用词
    filename = "stopwords_1.txt"
    f1 = open(filename, "r", encoding='utf-8')
    stop_words = []
    for line in f1.readlines():
        line = line.strip()
        stop_words.append(line)
    f1.close()

    term_sum = 0
    delstopwords_alltext = []
    # 分词
    for i in range(0, len(text)):
        sentence = text[i].replace('\n', '').replace('\u3000', '').replace('\u00A0', '').replace('\u200b', '')
        new_sentence = re.sub('[a-zA-Z0-9.。:：,，)）(（！!?？”“·《》【】；🚩+•#、ฅ∀—/]', '', sentence)
        data = jieba.cut(new_sentence, cut_all=False)
        txt = []
        for word in data:
            if word not in stop_words:
                if word >= u'\u4e00' and word <= u'\u9fa5':
                    term_sum += 1
                    txt.append(word)
        delstopwords_alltext.append(txt)


    all_word = []
    for data in delstopwords_alltext:
        for word in data:
            if word not in all_word:
                all_word.append(word)


    vsm = [[0 for j in range(len(all_word))] for i in range(len(delstopwords_alltext))]

    for i in range(len(delstopwords_alltext)):
        for j in delstopwords_alltext[i]:
            if j in all_word:
                vsm[i][all_word.index(j)] += 1

    b=kcluster(vsm)

    all_weibo=[]
    for i in b:
        weibo=[]
        for number in i:
            weibo.append(text[number])
        all_weibo.append(weibo)

    print("----------------------!!!----------------------")
    all_example=[]
    for i in b:
        example=[]
        for number in i:
            example.append(delstopwords_alltext[number])
        all_example.append(example)

    print("------------------------------!!!---------------------------")
    print("已经过tfidf,未经词性标注的关键词：")
    for i in all_example:
        r=cal(term_sum,i)
        print(r[0][0],r[1][0],r[2][0],r[3][0],r[4][0])
    print("----------------------------!!!-----------------------------")

    all_keyword=[]
    for i in range(len(all_example)):
        keyword=[]
        r=cal(term_sum,all_example[i])
        for j in range(len(r)):
            keyword.append(r[j][0])
        all_keyword.append(keyword)

    #进行词性标注
    keyword_pos=[]
    for i in range(len(all_keyword)):
        s=''
        for j in range(len(all_keyword[i])):
            s+=all_keyword[i][j]
        keyword_pos.append(s)


    k = ['n', 'nr', 'ns', 'nt', 'nz', 'v', 'vn']

    finalresult=[]
    for i in keyword_pos:
        finalkeyword=[]
        for x in psg.cut(i):
            if(x.flag in k):
                finalkeyword.append(x.word)
        finalresult.append(finalkeyword)

    print("-------------------------!!!------------------")
    print("经过词性标注的关键词：")
    for i in range(len(finalresult)):
        print(finalresult[i][0],finalresult[i][1],finalresult[i][2],finalresult[i][3],finalresult[i][4])

    return finalresult,all_weibo

