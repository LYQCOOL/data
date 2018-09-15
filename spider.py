from bs4 import BeautifulSoup
import requests
import xlrd
from xlutils.copy import copy
import time
import random
def crawer(id):
    datas=[]
    headers={
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie':'visid_incap_99025=babKYtmwTLaf+ImTYwcD1WM8R1sAAAAAQUIPAAAAAABeLjBe1NguLhA+zPaQ7hWw; incap_ses_1044_99025=IbbLddndSW4IEE3IdQl9DmM8R1sAAAAAFrUpwD5NP3PvFtzXaIlRZw==; nlbi_99025=pgStDZphyAILIXx88F1n9AAAAAAcvACDG4TEwMKFMQbx94BR; __utma=209907974.1954295422.1531395177.1531395177.1531395177.1; __utmc=209907974; __utmz=209907974.1531395177.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.2.1954295422.1531395177; _gid=GA1.2.195663399.1531395178; cookie_consent=1531395186830; csrftoken=GeKi1AClNifdWOUbbiJToZIIgrSqoKaY; stmpkola=s60xttw8nqc68d2hmnulu8s2jb7dy6bh; incap_ses_460_99025=ipZIJ28JaX7bGS8cukBiBiFJR1sAAAAAhxatE28utZTTwt7o6p7rHw==; incap_ses_572_99025=q/qaYPpUqkcWxluw1yfwB/9LR1sAAAAAKo5K25NHPHoaWEvRkN+TGw==',
    'Host': 'www.bitstamp.net',
    'Referer': 'https://www.bitstamp.net/news/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
    }
    data=requests.get('https://www.bitstamp.net/ajax/news/?start={0}&limit=10'.format(id),headers=headers)
    soup=BeautifulSoup(data.text,'lxml')
    time=soup.select('body > article > a > hgroup > h3 > time')
    title=soup.select('body > article > a > section > h1 ')
    content=soup.select('body > article > a > section > div')
    # print(time)
    # print(time)
    for a in time:
        data={
            'time':a.text,
            'title':title[time.index(a)].text.replace('\r','').replace('\n',''),
            'content':content[time.index(a)].text.replace('\r','').replace('\n','').replace('*\t',''),
        }
        datas.append(data)
    return datas
def write2(datas):
    col = 0
    rb = xlrd.open_workbook('datas.xls')
    # 通过sheet_by_index()获取的sheet没有write()方法
    rs = rb.sheet_by_index(0)
    row=rs.nrows
    wb = copy(rb)
    # 通过get_sheet()获取的sheet有write()方法
    ws = wb.get_sheet(0)
    for data in datas:
        ws.write(row,col,data['time'])
        ws.write(row, col+1, data['title'])
        ws.write(row, col+2, data['content'])
        row+=1
    wb.save('datas.xls')
if __name__=='__main__':
 for i in range(0,43):
  print('开始爬取第'+str(i+1)+'页')
  datas=crawer(i*10)
  write2(datas)
  print('爬取第' + str(i + 1) + '成功')
  if i%50==0:
      time.sleep(random.randint(1,3))
