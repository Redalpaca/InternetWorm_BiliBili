import requests
import re
from bs4 import BeautifulSoup
import json
import os
from BiliClass import BiliVideo
from BiliClass_func import DetailedListDownload


BiliUniHeaders = {
'authority':'www.bilibili.com',
'method':'GET',
'scheme':'https',
'cookie':'buvid3=C6FA7D37-BDAB-8A98-F46C-F74DCCD9E1E590619infoc;_uuid=611AEF8F-FA10A-F25E-63B1-7C6851A3E69C92883infoc;buvid4=A0BF7CAD-00E0-291D-0057-8C4CC946B8DF91548-022012618-yPTK2yRnbGG1AbZfVzPX2Q%3D%3D;rpdid=|(kRJkkRmJ~0J\'uYRJumJumJ;fingerprint=163f019b63a8ac7654d7e8634c3127cf;buvid_fp_plain=undefined;buvid_fp=4d18731a5a709bbdb5ce9d474ce68827;SESSDATA=201e1f7f%2C1665046259%2C56fc0%2A41;bili_jct=64787cb69067364c5e44cd1c3dd05938;DedeUserID=35671002;DedeUserID__ckMd5=d69f732e9248e565;sid=86748t3l;CURRENT_BLACKGAP=0;blackside_state=0;i-wanna-go-back=-1;b_ut=5;LIVE_BUVID=AUTO9316494943737456;is-2022-channel=1;nostalgia_conf=-1;PVID=1;hit-dyn-v2=1;bsource=search_baidu;bp_video_offset_35671002=683780023791910900;theme_style=light;innersign=1;CURRENT_FNVAL=4048;b_lsid=FDB9A836_1821F9A3573;b_timer=%7B%22ffp%22%3A%7B%22333.1007.fp.risk_C6FA7D37%22%3A%221820B1D4B31%22%2C%22444.41.fp.risk_C6FA7D37%22%3A%221820B1D7971%22%2C%22333.788.fp.risk_C6FA7D37%22%3A%221821FC361D3%22%2C%22333.337.fp.risk_C6FA7D37%22%3A%221820B1F58D8%22%7D%7D',
'referer':'www.bilibili.com',
'sec-ch-ua-platform':'"Windows"',
'sec-fetch-dest':'document',
'sec-fetch-mode':'navigate',
'sec-fetch-site':'same-origin',
'sec-fetch-user':'?1',
'upgrade-insecure-requests':'1',
'user-agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/103.0.0.0Safari/537.36'
}
BiliDownloadHeaders = {
'referer':'https://www.bilibili.com/video/BV1m44y1u7bs',
'user-agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/103.0.0.0Safari/537.36'
}
BiliApiHeaders = {
    'authority':'api.bilibili.com',
    'method':'GET',
    'scheme':'https',
    'path':'/pgc/season/episode/web/info?ep_id=374680',
    'cookie':'buvid3=C6FA7D37-BDAB-8A98-F46C-F74DCCD9E1E590619infoc; _uuid=611AEF8F-FA10A-F25E-63B1-7C6851A3E69C92883infoc; buvid4=A0BF7CAD-00E0-291D-0057-8C4CC946B8DF91548-022012618-yPTK2yRnbGG1AbZfVzPX2Q%3D%3D; rpdid=|(kRJkkRmJ~0J\'uYRJumJumJ; fingerprint=163f019b63a8ac7654d7e8634c3127cf; buvid_fp_plain=undefined; buvid_fp=4d18731a5a709bbdb5ce9d474ce68827; SESSDATA=201e1f7f%2C1665046259%2C56fc0%2A41; bili_jct=64787cb69067364c5e44cd1c3dd05938; DedeUserID=35671002; DedeUserID__ckMd5=d69f732e9248e565; sid=86748t3l; CURRENT_BLACKGAP=0; blackside_state=0; i-wanna-go-back=-1; b_ut=5; LIVE_BUVID=AUTO9316494943737456; is-2022-channel=1; nostalgia_conf=-1; hit-dyn-v2=1; go_old_video=-1; CURRENT_FNVAL=4048; CURRENT_QUALITY=120; bsource=search_baidu; bp_video_offset_35671002=691280144785997800; b_lsid=CBD22374_1827669CDBD; PVID=2; b_timer=%7B%22ffp%22%3A%7B%22333.788.fp.risk_C6FA7D37%22%3A%2218272FEB16C%22%2C%22333.1193.fp.risk_C6FA7D37%22%3A%221827676EE21%22%2C%22333.999.fp.risk_C6FA7D37%22%3A%221827676EBCC%22%2C%22888.2421.fp.risk_C6FA7D37%22%3A%221826EA1E547%22%2C%22666.25.fp.risk_C6FA7D37%22%3A%221827674CE10%22%2C%22333.976.fp.risk_C6FA7D37%22%3A%2218272FE2BEE%22%2C%22444.41.fp.risk_C6FA7D37%22%3A%2218272FE6D5D%22%2C%22333.937.fp.risk_C6FA7D37%22%3A%22182731D8041%22%2C%22333.337.fp.risk_C6FA7D37%22%3A%221827676F357%22%7D%7D',
    #'referer':'www.bilibili.com/play/ep374676',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/103.0.0.0Safari/537.36'
}

class Person(object):
    SpaceURL_mode = 'https://space.bilibili.com/{userID}'
    def __init__(self, userID):
        self.userID = userID
        self.SpaceURL = Person.SpaceURL_mode.format(userID = userID)
        
        self.res = requests.get(self.SpaceURL, headers= BiliUniHeaders)
        self.name = re.search('title>(.*?)的个人空间_', self.res.text).group(1)
        pass
    #获取用户头像(搜索'face'定位链接)
    def Profilepic(self, path = 'C:/Users/DELL/Desktop/'):
        soup = BeautifulSoup(self.res.text, 'lxml')
        picURL = soup.find('link', attrs={'rel':'apple-touch-icon'}).attrs['href']
        picURL = 'https:' +picURL
        print(picURL)
        res = requests.get(picURL, headers=BiliDownloadHeaders)
        with open(path + self.name + '_Face.jpg', 'wb') as f:
            f.write(res.content)
    #获取所有视频的bv号序列
    def VideoBVList(self, begin=1, end=1000):
        apiUrl = 'https://api.bilibili.com/x/space/arc/search?mid={userID}&ps=30&tid=0&pn={index}&keyword=&order=pubdate&jsonp=jsonp'
        bvlist = []
        for index in range(begin, end+1):
            res = requests.get(apiUrl.format(userID = self.userID, index = index), headers=BiliApiHeaders)
            dict = json.loads(res.text)
            tempList = dict['data']['list']['vlist']
            if tempList == []:
                break
            for element in tempList:
                bvlist.append(element['bvid'])
            pass
        #print(len(bvlist))
        return bvlist
    #获取所有视频的基本信息序列
    def VideoList(self, begin=1, end=1000):
        apiUrl = 'https://api.bilibili.com/x/space/arc/search?mid={userID}&ps=30&tid=0&pn={index}&keyword=&order=pubdate&jsonp=jsonp'
        vlist = []
        for index in range(begin, end+1):
            res = requests.get(apiUrl.format(userID = self.userID, index = index), headers=BiliApiHeaders)
            dict = json.loads(res.text)
            tempList = dict['data']['list']['vlist']
            if tempList == []:
                break
            for element in tempList:
                vlist.append(element)
            pass
        return vlist
    
    
    
    

alpaca = Person('26607148')
bvlist = alpaca.VideoBVList()
print('bvList Created')
#DetailedListDownload(bvlist)




