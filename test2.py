import requests

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

DownloadHeaders = {
'referer':'www.bilibili.com',
'user-agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/103.0.0.0Safari/537.36'
}


testurl1 = 'https://upos-sz-mirrorhw.bilivideo.com/upgcxcode/36/79/315477936/315477936-1-16.mp4?e=ig8euxZM2rNcNbRVhwdVhwdlhWdVhwdVhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&uipk=5&nbs=1&deadline=1658989406&gen=playurlv2&os=hwbv&oi=243225050&trid=53a100a96579463581b7a9e0c21e3c45h&mid=0&platform=html5&upsig=7ea2bd14058fa80c1c3df32fdfa85740&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&bw=57707&logo=80000000'
testurl3 = 'https://cn-gdfs-dx-bcache-12.bilivideo.com/upgcxcode/36/79/315477936/315477936-1-30064.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1658986680&gen=playurlv2&os=bcache&oi=243225050&trid=00000f899b8fd4964fd4be578f78537fa9b5u&mid=0&platform=pc&upsig=cd14a471d8a151e712e1479bdcb7d264&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&cdnid=60912&bvc=vod&nettype=0&orderid=0,3&agrr=1&bw=101640&logo=80000000'
print(testurl3.replace(r'\u0026','&'))


#url_1 = 'https://cn-gdfs-dx-bcache-12.bilivideo.com/upgcxcode/36/79/315477936/315477936-1-30064.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=\u0026uipk=5\u0026nbs=1\u0026deadline=1658986680\u0026gen=playurlv2\u0026os=bcache\u0026oi=243225050\u0026trid=00000f899b8fd4964fd4be578f78537fa9b5u\u0026mid=0\u0026platform=pc\u0026upsig=cd14a471d8a151e712e1479bdcb7d264\u0026uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform\u0026cdnid=60912\u0026bvc=vod\u0026nettype=0\u0026orderid=0,3\u0026agrr=1\u0026bw=101640\u0026logo=80000000'
#url_1 = url_1.replace(r'\u0026','&')
#print(url_1)

res = requests.get(url=testurl3, headers=BiliUniHeaders)
print(res.status_code)
with open('C:/Users/DELL/Desktop/alpaca.mp4', 'wb') as f:
    f.write(res.content)
print('Down')



