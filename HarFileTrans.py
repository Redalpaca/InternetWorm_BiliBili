import requests
import re
from bs4 import BeautifulSoup, Script
import json
import os
#只有这个请求头对从开发者工具里摘录的链接有效
BiliDownloadHeaders = {
'referer':'https://www.bilibili.com/video/BV1m44y1u7bs',
'user-agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/103.0.0.0Safari/537.36'
}
testurl = 'https://upos-sz-mirrorhw.bilivideo.com/upgcxcode/71/05/715930571/715930571-1-30080.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1659002743&gen=playurlv2&os=hwbv&oi=243225050&trid=f3a0db6d473f4c7793fa72f6a436da76u&mid=0&platform=pc&upsig=1423683fa29ec042e63a304b6730c263&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=0,3&agrr=1&bw=332395&logo=80000000'
testurl = testurl.replace(r'\u0026','&')
#这是从浏览器里摘下来的链接
testurl1 = "https://upos-sz-estgoss.bilivideo.com/upgcxcode/71/05/715930571/715930571-1-30112.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1659000137&gen=playurlv2&os=upos&oi=243225050&trid=ac64e03595c74374809c9316426e6091u&mid=35671002&platform=pc&upsig=7977a6645bbdde61b684d6a0d5beecf5&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=0,1&agrr=1&bw=648879&logo=80000000"

location = 'C:/Users/DELL/Desktop/'
status_code = os.system('har2case C:/Users/DELL/Desktop/test11.har')
print(status_code)

res = requests.get(url='https://www.bilibili.com/video/BV1m44y1u7bs/?spm_id_from=autoNext&vd_source=4a43fa8ae01ef716b6388654f580b256', headers=BiliDownloadHeaders)
print(res)
html = res.text
#Ctrl+F搜索以获悉不同清晰度的播放链接位置。这些信息是以json格式存储的。还是按惯例，通过for迭代抽丝剥茧得到json文件的结构
modestr = re.compile('window.__playinfo__=(.*?)</script>')
jsontest = re.search(modestr, html).group(1)

dict_0 = json.loads(jsontest)
VideoList = dict_0['data']['dash']['video']
AudioList = dict_0['data']['dash']['audio']


#for key in VideoList:
#    print(key)
"""
QualityDict = {"4k":[120,6], "1080p+":[116,5], "1080p":[80,4], "720p":[64,3], "480p":[32,2], "360p":[16,1]}
MaxQuality = VideoList[0]['id']
ListLen = len(VideoList)

print(MaxQuality)
#print(VideoList[0]['baseUrl'])
descript = '360p'
#输入清晰度的格式是否正确
try:
    QualityDict[descript]
except:
    print('Format Error')
    exit()
#该清晰度是否允许下载
if(QualityDict[descript][0] > MaxQuality):
    print('The VideoQuality is too high.(Or the Cookie is Overdue)')
    exit()

index = ListLen - QualityDict[descript][1]
print(index)
print(VideoList[index])
"""








