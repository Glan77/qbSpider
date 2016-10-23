import urllib.request
import re
import threading
import time
#---模块化---#
class Spider_Model:
    def __init__(self):
        self.page = 1  #初始页数
        self.pages = []  #存放段子的list
        self.enable = False

    #输入页数，返回段子list
    def getPage(self,page):
        print("%s线程正在获取第%s页" %(threading.current_thread().name,page))
        url = "http://www.qiushibaike.com/8hr/page/"+page
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2504.0 Safari/537.36'
        headers = {'User-agent':user_agent}
        request = urllib.request.Request(url,headers=headers)
        response = urllib.request.urlopen(request)
        myPage = response.read()
        unicodePage = myPage.decode('utf-8','ignore')  #igonre重要
        myItems = re.findall(r'<div class="content">\n+<span>(.*?)</span>\n+</div>',unicodePage,re.S)
        items = []
        for item in myItems:
            items.append(item)
        return items

    #段子加载器
    #加载效果是self.pages=[[第n页段子],[第n+1页段子]]
    #self.pages中元素少于2时调用GetPage获取n+2页段子list加入slef.pages
    def LoadPage(self):
        while self.enable:
            if len(self.pages)<2:
                try:
                    myPage = self.getPage(str(self.page))
                    self.page += 1  #获取完毕，页数+1
                    self.pages.append(myPage)  #将获取的段子list添加到self.pages list中
                except Exception as e:
                    print('except:',e)
                    print('无法连接糗事百科！\n')
            else:
                time.sleep(1)

    #段子显示器
    def ShowPage(self, nowPage, page):
        fout = open('output.html', 'w', encoding='utf-8')
        fout.write("<html>")
        fout.write("<head><meta http-equiv=\"content-type\" content=\"text/html;charset=utf-8\"></head>")
        fout.write("<body>")
        fout.write("<table>")
        i = 0
        for items in nowPage:	#将传来的list遍历print，用户input控制
            i += 1
            print(u'正在爬取第%d条内容' %i )
            fout.write(str(i))
            fout.write(".")
            fout.write(items)
            fout.write("<br/><br/><br/>")
            if  i == 20:   #退出标志，同时结束主副线程
                self.enable = False
                fout.write("</table>")
                fout.write("</body>")
                fout.write("</html>")
                fout.close()
                print("Over!")
                break


    def Start(self):
        self.enable = True
        page = self.page
        t = threading.Thread(target=self.LoadPage,name='LAN') #多线程  #只是想用threading而已 #不懂为什么要用
        t.start()

        while self.enable:
            if self.pages:
                nowPage = self.pages[0]  #取走一页list到nowPage
                del self.pages[0]
                self.ShowPage(nowPage,page)  #将这一页list和页码发给显示器
                page += 1   #翻页进入下一次主进程循环

if __name__ == "__main__":
    print(u"""
    ---------------------------------------
       原文地址(源代码):http://blog.csdn.net/pleasecallmewhy/article/details/8932310
       程序：糗百爬虫
       版本：0.3
       作者：why
       日期：2014-06-03
       语言：Python 2.7
       操作：输入quit退出阅读糗事百科
       功能：按下回车依次浏览今日的糗百热点
    ---------------------------------------
       源地址：https://github.com/YeXiaoRain/BoringCode/blob/master/qiubaipachong.py
       修改内容:网址和正则表达式部分
       修改者:Ryan
       修改日期:2015-09-19
       测试通过版本:Python 2.7.10
    ---------------------------------------
       修改内容: python3, 海量的无用注释
       修改者:Errorld
       修改日期:2015-09-25
       测试通过版本:Python 3.4.3
    ---------------------------------------
       修改内容: 优化输出，保存为html格式
       修改者:Glan
       修改日期:2016-10-23
       测试通过版本:Python 3.5.2

    """)
    myModel = Spider_Model()
    try:
        myModel.page = int(input('选择起始页数\n'))
    except Exception as e:
        print(e)
        print('输入有误，从第一页开始\n')
    myModel.Start()
