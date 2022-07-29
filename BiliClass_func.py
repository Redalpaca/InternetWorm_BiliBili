import requests
from BiliClass import BiliVideo
BiliDownloadHeaders = {
'referer':'https://www.bilibili.com/video/BV1m44y1u7bs',
'user-agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/103.0.0.0Safari/537.36'
}

#导入列表进行批量下载
def ListDownload(BVList, Location = 'E:/WormDownloadLib/BiliVideo/', VideoQuality = 0):
    count = 0
    for BVnum in BVList:
        TempVideoExam = BiliVideo(BVnum)
        title = TempVideoExam.title + '.mp4'
        TempVideoExam.DownloadVideo(Location + title, quality=VideoQuality)
        count+=1
        print('VideoCount:%d'%count)
    pass
#导入原始URL直接下载
def Download(url, name= 'Video.mp4', location='C:/Users/DELL/Desktop/'):
    res = requests.get(url=url, headers= BiliDownloadHeaders)
    if(str(res.status_code)!='200'):
        print('Url opening failed.')
        return False
    with open(location+name, 'wb') as f:
        f.write(res.content)
    print('{VideoName} Down.'.format(VideoName = name))
    return True
    

#Download('https://upos-sz-mirrorhw.bilivideo.com/upgcxcode/71/05/715930571/715930571-1-30080.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1659026838&gen=playurlv2&os=hwbv&oi=243225050&trid=fe8aa14d3c9641a1a5663dbf76548a5bu&mid=0&platform=pc&upsig=478877f372193b08554145b3c264d1d9&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=0,3&agrr=1&bw=332395&logo=80000000')











