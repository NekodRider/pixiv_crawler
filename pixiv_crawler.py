# -*- coding:utf-8 -*-
import requests,urllib
from bs4 import BeautifulSoup
import os,time
URLHEAD="http://www.pixiv.net/"
headers = {
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    'Content-Length':'175',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'DNT':'1',
    'Host':'accounts.pixiv.net',
    'Origin':'https://accounts.pixiv.net',
    'Pragma':'no-cache',
    'Referer':'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest'
}
class mzitu():

    def all_url(self, url):
        html = self.login('account','password',url)
        all_rank_item=BeautifulSoup(html.text, 'html.parser').find_all('div', class_='ranking-item')
        progress=0
        for rank_item in all_rank_item:
            a = rank_item.find('div', class_='work_wrapper').find_all('a')
            title = rank_item.select('.data h2 a')[0].text
            print(u'Downloading：', title)
            path = str(title)
            self.mkdir(path)
            os.chdir(path)
            href = URLHEAD+a[0]['href']
            self.html(str(href))
            os.chdir("..")
            time.sleep(15)
            progress+=1
            print('The progress is '+str(progress)+'/100')
            print('='*70)
        print('Done!')

    def html(self, href1):
        print(href1)
        html = self.request(href1)
        if(len(BeautifulSoup(html.text, 'html.parser').select("._work.multiple"))!=0):
            if(len(BeautifulSoup(html.text, 'html.parser').select(".works_display a"))!=0):
                print(u'This is a album , maybe need more time.')
                html1=self.request(URLHEAD+BeautifulSoup(html.text, 'html.parser').select(".works_display a")[0]['href'])
                pp=0
                for htm in BeautifulSoup(html1.text, 'html.parser').select(".item-container a"):
                    html2=self.request(URLHEAD+htm['href'])
                    self.img(BeautifulSoup(html2.text, 'html.parser').img['src'],href1)
                    pp+=1
                    print(str(pp)+' done')
                    time.sleep(10)
            else:
                print(u"Can't find this pic!Maybe deleted ")
        else:
            if (len(BeautifulSoup(html.text, 'html.parser').select(".works_display img")) != 0):
                self.img(BeautifulSoup(html.text, 'html.parser').select(".original-image")[0]['data-src'],href1)
            else:
                print(u"Can't find this pic!Maybe deleted ")


    def img(self, page_url,href1):
        img_html = self.request(page_url)
        #img_url = BeautifulSoup(img_html.text, 'html.parser').find('div', class_='main-image').find('img')['src']
        self.save(page_url,href1)

    def save(self, img_url,href1):
        sp_hd={
            'Accept': 'image/webp,image/*,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Host':img_url.split("/")[2],
            'Pragma': 'no-cache',
            'Referer':href1,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
        }
        name = img_url.replace(".","/")
        name=name.split("/")[-2]
        img = s.get(img_url, headers=sp_hd)
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()

    def mkdir(self, path):
        path = path.strip()
        isExists = os.path.exists(os.path.join("path", path))
        if not isExists:
            print(u'Make a directory called: "', path,u'"')
            os.makedirs(os.path.join("path", path))
            return True
        else:
            print(u'The directory called "', path, u'" is already existed!')
            return False

    def request(self, url):
        postdata1 = {
            'pixiv_id': 'pixiv_id',
            'password': 'password',
            'captcha': '',
            'g_recaptcha_response': '',
            'post_key': str(postkey),
            'source': 'pc',
            'return_to': 'http://www.pixiv.net/ranking_area.php?type=detail&no=6'
        }
        hd = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        }
        content = s.get(url, data=postdata1,headers=hd)
        return content
    def login(self,username,password,url):
        login_url="https://accounts.pixiv.net/api/login?lang=zh"

        login_html=s.get('https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index').text
        soup=BeautifulSoup(login_html,"html.parser")
        global postkey
        postkey=str(soup.find_all(attrs={'name':'post_key'})[0]).split("\"")[5]
        postdata = {
            'pixiv_id': 'pixiv_id',
            'password': 'password',
            'captcha': '',
            'g_recaptcha_response': '',
            'post_key': str(postkey),
            'source': 'pc',
            'return_to': 'http://www.pixiv.net/ranking_area.php?type=detail&no=6'
        }
        res=s.post(login_url,data=postdata,headers=headers)
        if(res.status_code==200):
            print('Successfully login!')
            print('=' * 70)
            return s.get(url)
        else:
            print(res.status_code)
            print('Failed to login!')

Mzitu = mzitu()
global s
s=requests.Session()
Mzitu.all_url('http://www.pixiv.net/ranking_area.php?type=detail&no=6')

url='http://www.pixiv.net/ranking_area.php?type=detail&no=6'
