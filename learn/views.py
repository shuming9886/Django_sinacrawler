from django.shortcuts import render
from .weibocrawler import crawler
from .KMeans_2 import KMeans
import win_unicode_console
win_unicode_console.enable()

def home(request):
    result=request.GET.get('a')
    result5=''
    if result:
        text = result
        result1 = crawler(text)
        print(result1)
        result2 = result1
        print(len(result2))
        # result4 = get_digest2(result2)
        # result5=getTag(result1)
        finalresult,weibodata = KMeans(result1)
        a1 = finalresult[0][0] + '  ' + finalresult[0][1] + '  ' + finalresult[0][2] + '  ' + finalresult[0][3] + '  ' + \
             finalresult[0][4]
        a2 = finalresult[1][0] + '  ' + finalresult[1][1] + '  ' + finalresult[1][2] + '  ' + finalresult[1][3] + '  ' + \
             finalresult[1][4]
        a3 = finalresult[2][0] + '  ' + finalresult[2][1] + '  ' + finalresult[2][2] + '  ' + finalresult[2][3] + '  ' + \
             finalresult[2][4]
        a4 = finalresult[3][0] + '  ' + finalresult[3][1] + '  ' + finalresult[3][2] + '  ' + finalresult[3][3] + '  ' + \
             finalresult[3][4]
        a5 = finalresult[4][0] + '  ' + finalresult[4][1] + '  ' + finalresult[4][2] + '  ' + finalresult[4][3] + '  ' + \
             finalresult[4][4]

        allweibodata=[]
        for i in weibodata:
            weibodata1='---------------------------------'+'\n'
            for j in i:
                weibodata1+=j
                weibodata1+='\n'
                weibodata1+='---------------------------------'+'\n'
            allweibodata.append(weibodata1)

        return render(request, "Home.html", {'result1':result1,'result3':a1,'result4':a2,'result5':a3,'result6':a4,'result7':a5,'weibodata1':allweibodata[0],'weibodata2':allweibodata[1],'weibodata3':allweibodata[2],'weibodata4':allweibodata[3],'weibodata5':allweibodata[4]})
    else:
        result='None'

    return render(request, "Home.html",{'result2':result5})