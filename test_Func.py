import requests
import re
import parsel
import os
from bs4 import BeautifulSoup
from BiliClass import BiliVideo
Headers_0 = BiliVideo.UniHeaders

def ListDownload(BVList, Location = 'E:/WormDownloadLib/BiliVideo/', VideoQuality = 0):
    count = 0
    for BVnum in BVList:
        TempVideoExam = BiliVideo(BVnum)
        title = TempVideoExam.title + '.mp4'
        TempVideoExam.DownloadVideo(Location + title, quality=VideoQuality)
        count+=1
        print('VideoCount:%d'%count)
    pass

#以下是爬取个人页获取所有视频的bv号的代码
PersonAPIurl_model = 'https://api.bilibili.com/x/space/arc/search?mid={MID}&ps=30&tid=0&pn=1&keyword=&order=pubdate&jsonp=jsonp'
PersonAPIurl = PersonAPIurl_model.format(MID = '35671002')
Html = requests.get(PersonAPIurl, headers={}).text
bvidList = re.findall(re.compile('\"bvid\":\"(.*?)\",'), Html)
print(bvidList)

ListDownload(BVList=bvidList)



#test = soup.find(name='div', class_='title-row')
#print(test)
#test1 = re.search(re.compile('title-row'), Html)
#print(test1)



#BVList = ['BV1m44y1u7bs','BV1pT4y16758']
#test(BVList, VideoQuality=1)




"""
Location = 'E:/WormDownloadLib/BiliVideo/'
for BVnum in BVList:
    TempVideoExam = BiliVideo(BVnum)
    title = TempVideoExam.title + '.mp4'
    TempVideoExam.DownloadVideo(Location + title, quality=0)
    pass
"""










"""
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

def GetSoup(url, headers= BiliUniHeaders):
    html = requests.get(url, headers).text
    soup = BeautifulSoup(html, 'lxml')
    return soup
#with open('C:/Users/DELL/Desktop/html.txt', 'r', encoding='utf-8') as f:
#    html = f.read()
url = 'https://www.bilibili.com/video/BV1m44y1u7bs'
html = requests.get(url, headers=BiliUniHeaders).text
soup = BeautifulSoup(html, 'lxml')

comment = soup.find(name='div', class_ ='reply-list')
print(comment)

#test = re.search(re.compile('<span class="total-reply".*?>(\d+)</span>'), html).group(1)
#print(test)



url = 'https://www.bilibili.com/video/BV17U4y1j7Sz?spm_id_from=333.851.b_7265636f6d6d656e64.6'
headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'referer': url
    }

def download(video_url,audio_url,title):
    video = requests.get(video_url, headers=headers).content
    audio = requests.get(audio_url, headers=headers).content
    #title_new = title + "纯"
    with open(r'C:/Users/DELL/Desktop/video.mp4', 'wb')as f:
        f.write(video)
    #with open('audio.mp3', 'wb')as f:
    #    f.write(audio)
    

def get_data(data):
    Xpath = parsel.Selector(data)
    title = Xpath.xpath('//*[@id="viewbox_report"]/h1/span/text()').extract_first()
    playinfo = Xpath.xpath('/html/head/script[5]/text()').extract_first()
    video_url = re.findall(re.compile(r'"baseUrl":"([\s\S]*)",'), playinfo)
    print(video_url)
    #audio_url = re.findall(r'"audio":.*?,"baseUrl":"(.*?)",', playinfo)[0]
    #download(video_url,audio_url,title)
    
def get_parse(url, headers):
    response = requests.get(url, headers=headers)
    data = response.text
    #print(data)
    get_data(data)
    
    
#get_parse(url, headers)

with open('C:/Users/DELL/Desktop/html.txt', 'r', encoding='utf-8') as f:
    html = f.read()

model = re.compile('\"video\":.*?,\"baseUrl\":\"(.*?)\"')
downurl = re.findall(model,html)
#print(downurl)


res = requests.get(downurl, headers=headers)
print(res)


"""