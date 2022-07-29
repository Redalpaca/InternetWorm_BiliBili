import json
import requests
from bs4 import BeautifulSoup
import re
def Instead(string, i, ch):
    strlen = len(string)
    string = string[:i] + ch + string[i+1:strlen]
    return string
def SearchText(HtmlCode):
    pass
def Saves(HtmlCode):
    with open("C:/Users/DELL/Desktop/HeadersLib/Save/Temp.txt", "w", encoding= 'utf-8') as f:
        f.write(HtmlCode)
    pass
#Saves(res.text)




UniHeaders = {
'user-agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/103.0.0.0Safari/537.36'
}


BiliHeaders = {
'authority':'www.bilibili.com',
'method':'GET',
'path':'/video/BV1Ef4y1o7NU?spm_id_from=444.41.list.card_archive.click&vd_source=4a43fa8ae01ef716b6388654f580b256',
'scheme':'https',
'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'accept-encoding':'gzip,deflate,br',
'accept-language':'zh,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
'cache-control':'max-age=0',
'cookie':'buvid3=C6FA7D37-BDAB-8A98-F46C-F74DCCD9E1E590619infoc;_uuid=611AEF8F-FA10A-F25E-63B1-7C6851A3E69C92883infoc;buvid4=A0BF7CAD-00E0-291D-0057-8C4CC946B8DF91548-022012618-yPTK2yRnbGG1AbZfVzPX2Q%3D%3D;rpdid=|(kRJkkRmJ~0J\'uYRJumJumJ;fingerprint=163f019b63a8ac7654d7e8634c3127cf;buvid_fp_plain=undefined;buvid_fp=4d18731a5a709bbdb5ce9d474ce68827;SESSDATA=201e1f7f%2C1665046259%2C56fc0%2A41;bili_jct=64787cb69067364c5e44cd1c3dd05938;DedeUserID=35671002;DedeUserID__ckMd5=d69f732e9248e565;sid=86748t3l;CURRENT_BLACKGAP=0;blackside_state=0;i-wanna-go-back=-1;b_ut=5;LIVE_BUVID=AUTO9316494943737456;is-2022-channel=1;nostalgia_conf=-1;PVID=1;hit-dyn-v2=1;bsource=search_baidu;bp_video_offset_35671002=683780023791910900;theme_style=light;innersign=1;CURRENT_FNVAL=4048;b_lsid=FDB9A836_1821F9A3573;b_timer=%7B%22ffp%22%3A%7B%22333.1007.fp.risk_C6FA7D37%22%3A%221820B1D4B31%22%2C%22444.41.fp.risk_C6FA7D37%22%3A%221820B1D7971%22%2C%22333.788.fp.risk_C6FA7D37%22%3A%221821FC361D3%22%2C%22333.337.fp.risk_C6FA7D37%22%3A%221820B1F58D8%22%7D%7D',
'referer':'https//t.bilibili.com/?spm_id_from=333.1007.0.0',
'sec-ch-ua':'".Not/A)Brand";v="99","GoogleChrome";v="103","Chromium";v="103"',
'sec-ch-ua-mobile':'?0',
'sec-ch-ua-platform':'"Windows"',
'sec-fetch-dest':'document',
'sec-fetch-mode':'navigate',
'sec-fetch-site':'same-origin',
'sec-fetch-user':'?1',
'upgrade-insecure-requests':'1',
'user-agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/103.0.0.0Safari/537.36'
}

#biliurl = "https://www.bilibili.com/video/BV1Ef4y1o7NU"

biliurl = 'https://www.bilibili.com/video/BV1hS4y1p7Rh'

BiliUniHeaders = {
'authority':'www.bilibili.com',
'method':'GET',
'scheme':'https',
'cookie':'buvid3=C6FA7D37-BDAB-8A98-F46C-F74DCCD9E1E590619infoc;_uuid=611AEF8F-FA10A-F25E-63B1-7C6851A3E69C92883infoc;buvid4=A0BF7CAD-00E0-291D-0057-8C4CC946B8DF91548-022012618-yPTK2yRnbGG1AbZfVzPX2Q%3D%3D;rpdid=|(kRJkkRmJ~0J\'uYRJumJumJ;fingerprint=163f019b63a8ac7654d7e8634c3127cf;buvid_fp_plain=undefined;buvid_fp=4d18731a5a709bbdb5ce9d474ce68827;SESSDATA=201e1f7f%2C1665046259%2C56fc0%2A41;bili_jct=64787cb69067364c5e44cd1c3dd05938;DedeUserID=35671002;DedeUserID__ckMd5=d69f732e9248e565;sid=86748t3l;CURRENT_BLACKGAP=0;blackside_state=0;i-wanna-go-back=-1;b_ut=5;LIVE_BUVID=AUTO9316494943737456;is-2022-channel=1;nostalgia_conf=-1;PVID=1;hit-dyn-v2=1;bsource=search_baidu;bp_video_offset_35671002=683780023791910900;theme_style=light;innersign=1;CURRENT_FNVAL=4048;b_lsid=FDB9A836_1821F9A3573;b_timer=%7B%22ffp%22%3A%7B%22333.1007.fp.risk_C6FA7D37%22%3A%221820B1D4B31%22%2C%22444.41.fp.risk_C6FA7D37%22%3A%221820B1D7971%22%2C%22333.788.fp.risk_C6FA7D37%22%3A%221821FC361D3%22%2C%22333.337.fp.risk_C6FA7D37%22%3A%221820B1F58D8%22%7D%7D',
'referer':'{URL}'.format(URL = biliurl),
'sec-ch-ua-platform':'"Windows"',
'sec-fetch-dest':'document',
'sec-fetch-mode':'navigate',
'sec-fetch-site':'same-origin',
'sec-fetch-user':'?1',
'upgrade-insecure-requests':'1',
'user-agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/103.0.0.0Safari/537.36'
}


#Part Request
res = requests.get(biliurl, headers=BiliUniHeaders)
ReturnMessage = 'StatusCode = {number}'
print(ReturnMessage.format(number = res.status_code))
if res.status_code == 200:
    print('Accept.')
else:
    print('Warning.')

#Part Analysis
html_0 = res.text
#soup = BeautifulSoup(html_0, 'lxml')
#Result = soup.find_all(text = re.compile('cid=(.*?)'))
#for element in Result:
#    print(element)
CID = re.search(re.compile(r'\"cid\":(\b\d+\b)'), html_0)
print('Cid=%s'%CID.group(1)) #cid的值
#print(CID.group(1))
AID = re.search(re.compile(r'\"aid\":(\b\d+\b)'), html_0)
print('Aid=%s'%AID.group(1)) #aid的值
cidStr = CID.group(1)
aidStr = AID.group(1)

TemplateURL = 'https://api.bilibili.com/x/player/playurl?avid={AID}&cid={CID}&qn=1&type=&otype=json&platform=html5&high_quality=0'
#把链接尾部改成0可取消下载高清

JumpURL = TemplateURL.format(AID = aidStr, CID = cidStr)
#print(JumpURL)
JumpHtml = requests.get(JumpURL, headers={}).text
#print(JumpHtml)
DownloadURL_0 = re.search(re.compile('\"url\":\"(.*?)\"'), JumpHtml).group(1)
DownloadURL = DownloadURL_0.replace(r'\u0026','&')
#print(DownloadURL)

video = requests.get(DownloadURL, headers=UniHeaders).content
print(requests.get(DownloadURL, headers=UniHeaders))
with open('C:/Users/DELL/Desktop/video3.mp4','wb') as f:
   f.write(video)
   
















