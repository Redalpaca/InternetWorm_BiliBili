from BiliClass import BiliVideo
import BiliClass_func
import re
import os
#BiliClass_func.Download('https://upos-sz-mirrorhw.bilivideo.com/upgcxcode/71/05/715930571/715930571-1-30080.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1659003820&gen=playurlv2&os=hwbv&oi=243225050&trid=d9a28188d3e743cd81f9180b78c17d89u&mid=0&platform=pc&upsig=89429c93830acbabd80bb2839f8856f4&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=0,3&agrr=1&bw=332395&logo=80000000')
#Video = BiliClass.BiliVideo('BV1m44y1u7bs')
#Video.DownloadVideo()
"""
modeStr = re.compile('2..')
res = re.search(modeStr, '304')
print(res)
"""
"""
location = 'C:/Users/DELL/Desktop/'
status_code = os.system('har2case C:/Users/DELL/Desktop/test11.har')
print(status_code)
"""
while(True):
    bvid = input('Enter the BVid:')
    Video_0 = BiliVideo(bvid)
    Quality = input('Enter appointed Video Quality:')
    location = input('Enter file directory:')
    Video_0.DetailedVideoDownload(Quality=Quality, location=location)
    print('Continue? (Y/N)')
    res = input()
    if(res=='Y'):
        continue
    else:
        exit()







