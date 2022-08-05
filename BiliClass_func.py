import requests
import re
from BiliClass import BiliVideo
import os
BiliDownloadHeaders = {
'referer':'https://www.bilibili.com/video/BV1m44y1u7bs',
'user-agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/103.0.0.0Safari/537.36'
}
def Status(status_code:str):
    modeStr = re.compile('2..')
    res = re.search(modeStr, status_code)
    if(res != None):
        return True
    return False
def URLTest(url):
    #url是否合法
    try:
        res = requests.get(url=url, headers= BiliDownloadHeaders)
    except:
        print('ERROR: Illigal URL')
        return False
    #状态码判断 
    if(not Status(str(res.status_code))):
        print('ERROR: Unsuccessful response:[%d]'%res.status_code)
        return False
    print('Accept.')
    return True

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
def Download(url, name= 'Video', path='C:/Users/DELL/Desktop/', format = '.mp4'):
    if(not URLTest(url)):
        return False
    res = requests.get(url=url, headers= BiliDownloadHeaders)
    with open(path + name + format, 'wb') as f:
        f.write(res.content)
    print('{File} Down.'.format(File = name + format))
    return True
#拼接多p视频
def Intergrate(bvid, path_in = 'C:/Users/DELL/Desktop/', path_out = 'C:/Users/DELL/Desktop/'):
    List = os.listdir(path_in + bvid)
    path_txt = path_in + 'temp.txt'
    with open(path_txt, 'w') as f:
        for element in List:
            f.write('file '+ path_in + bvid + '/' +element + '\n')
    command = 'ffmpeg -n -f concat -safe 0 -i {path_txt} -c copy \"{path_output}_intergrated.mp4\"'.format(path_txt = path_txt, path_output = path_out + bvid)
    os.system(command = command)
    print('Intergrate Over.')
    #删除临时txt文件
    os.remove(path_txt)    

#Intergrate('BV1gK411K75P')

#Download('https://upos-sz-mirrorhw.bilivideo.com/upgcxcode/71/05/715930571/715930571-1-30080.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1659026838&gen=playurlv2&os=hwbv&oi=243225050&trid=fe8aa14d3c9641a1a5663dbf76548a5bu&mid=0&platform=pc&upsig=478877f372193b08554145b3c264d1d9&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=0,3&agrr=1&bw=332395&logo=80000000')









