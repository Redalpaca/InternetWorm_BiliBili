import json
import requests


def Instead(string, i, ch):
    strlen = len(string)
    string = string[:i] + ch + string[i+1:strlen]
    return string


tempdict = {
'cookie': 'buvid3=C6FA7D37-BDAB-8A98-F46C-F74DCCD9E1E590619infoc; _uuid=611AEF8F-FA10A-F25E-63B1-7C6851A3E69C92883infoc; buvid4=A0BF7CAD-00E0-291D-0057-8C4CC946B8DF91548-022012618-yPTK2yRnbGG1AbZfVzPX2Q%3D%3D; rpdid=|(kRJkkRmJ~0J\'uYRJumJumJ; fingerprint=163f019b63a8ac7654d7e8634c3127cf; buvid_fp_plain=undefined; buvid_fp=4d18731a5a709bbdb5ce9d474ce68827; SESSDATA=201e1f7f%2C1665046259%2C56fc0%2A41; bili_jct=64787cb69067364c5e44cd1c3dd05938; DedeUserID=35671002; DedeUserID__ckMd5=d69f732e9248e565; sid=86748t3l; CURRENT_BLACKGAP=0; blackside_state=0; i-wanna-go-back=-1; b_ut=5; LIVE_BUVID=AUTO9316494943737456; is-2022-channel=1; nostalgia_conf=-1; PVID=1; hit-dyn-v2=1; bsource=search_baidu; bp_video_offset_35671002=683780023791910900; theme_style=light; innersign=1; CURRENT_FNVAL=4048; b_lsid=FDB9A836_1821F9A3573; b_timer=%7B%22ffp%22%3A%7B%22333.1007.fp.risk_C6FA7D37%22%3A%221820B1D4B31%22%2C%22444.41.fp.risk_C6FA7D37%22%3A%221820B1D7971%22%2C%22333.788.fp.risk_C6FA7D37%22%3A%221821FC361D3%22%2C%22333.337.fp.risk_C6FA7D37%22%3A%221820B1F58D8%22%7D%7D' ,
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

url_0 = "https://www.bilibili.com/video/BV1Ef4y1o7NU?vd_source=4a43fa8ae01ef716b6388654f580b256"
res = requests.get(url_0, headers=tempdict)
#print(res)

def SearchText(HtmlCode):
    pass

def Saves(HtmlCode):
    with open("C:/Users/DELL/Desktop/HeadersLib/Save/Temp.txt", "r", encoding= 'utf-8') as f:
        f.write(HtmlCode)
    pass


















