from email.policy import default
import requests
import os
import ffmpeg
from setuptools import Command
from urllib.request import urlopen
from urllib.request import Request
from tqdm import tqdm
url = 'https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/72/41/751214172/751214172-1-30016.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1660046248&gen=playurlv2&os=cosbv&oi=243224669&trid=2685a0f30c4f43fbb3d49c8ba5b57066u&mid=0&platform=pc&upsig=abd4e3995692423c6e9893e7e546170c&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=0,3&agrr=1&bw=47131&logo=80000000'
url = 'https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/76/85/347288576/347288576-1-100025.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1660046792&gen=playurlv2&os=cosbv&oi=243224669&trid=c20060efd68146bba01001710996fba1u&mid=0&platform=pc&upsig=b18ee6987681551913bba46cafc3c9d6&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=0,3&agrr=0&bw=104163&logo=80000000'
url = 'https://upos-sz-estgoss.bilivideo.com/upgcxcode/45/46/778294645/778294645-1-100023.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1660067476&gen=playurlv2&os=upos&oi=243224669&trid=babd96eb7ae247f58dbf715113fc73edu&mid=0&platform=pc&upsig=bb987cf7415f5f0a177adc140600264c&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&orderid=0,1&agrr=1&bw=20657&logo=80000000'


BiliDownloadHeaders = {
'Accept-Encoding': 'identity',
'referer':'https://www.bilibili.com/video/BV1m44y1u7bs',
'user-agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/103.0.0.0Safari/537.36'
}
def download_from_url(url, dst = 'C:/Users/DELL/Desktop/test1.mp4'):
    """
    @param: url to download file
    @param: dst place to put the file
    """
    url_get = Request(url, headers= BiliDownloadHeaders)
    file_size = int(urlopen(url_get).info().get('Content-Length', -1))

    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)
    else:
        first_byte = 0
    if first_byte >= file_size:
        return file_size
    #header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
    pbar = tqdm(
        total=file_size, initial=first_byte,
        unit='B', unit_scale=True, leave= True)
    req = requests.get(url, headers=BiliDownloadHeaders, stream=True)
    with(open(dst, 'wb')) as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(1024)
    pbar.close()
    #pbar.delay = 5
    return file_size


#if __name__ == '__main__':
#    url = "http://newoss.maiziedu.com/machinelearning/pythonrm/pythonrm5.mp4"
#    download_from_url(url, "./new.mp4")

#download_from_url(url)


#换个链接, 老链接403了
ResHeaders = requests.get(url, headers=BiliDownloadHeaders, stream=True).headers
print(ResHeaders['Content-Length'])
#res = requests.head(url, headers=BiliDownloadHeaders)
#print(res)
def Download_Pbar(url, dst = 'C:/Users/DELL/Desktop/test1.mp4', headers = BiliDownloadHeaders):
    """
    @param: url to download file
    @param: dst place to put the file
    """
    #url_get = Request(url, headers= BiliDownloadHeaders)
    #file_size = int(urlopen(url_get).info().get('Content-Length', -1))

    ResHeaders = requests.get(url, headers= headers, stream= True).headers
    #print(ResHeaders['Content-Length'])
    file_size = int(ResHeaders['Content-Length'])

    #若文件存在则获取文件大小, 使用附加模式接续文件
    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)
    else:
        first_byte = 0
    if first_byte >= file_size:
        return file_size
    pbar = tqdm(
        total = file_size, initial = first_byte,
        unit='B', unit_scale=True, leave= True)
    #stream元素设定当访问content元素时才获取输入流
    res = requests.get(url, headers= headers, stream= True)
    with(open(dst, 'ab')) as f:
        #使用迭代器模式获取content, 以1024Bytes为单位读取并写入本地
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(1024)
    pbar.close()
    #pbar.delay = 5
    return file_size


Download_Pbar(url)











#拼接多p视频
def Intergrate(path_in, name, path_out):
    List = os.listdir(path_in + name)
    with open(path_in + 'temp.txt', 'w') as f:
        for element in List:
            f.write('file '+ path_in + name + '/' +element + '\n')
    path_txt = path_in + 'temp.txt'
    command = 'ffmpeg.exe -loglevel quiet -n -f concat -safe 0 -i {path_txt} -c copy {path_output}'.format(path_txt = path_txt, path_output = path_out)
    os.system(command = command)
    print('Intergrate Over.')
    #删除临时txt文件
    os.remove(path_txt)
    
    pass

#Intergrate('C:/Users/DELL/Desktop/', 'BV1pa411q7AM', 'C:/Users/DELL/Desktop/test.mp4')

"""
url = 'https://upos-sz-staticcos-cmask.bilivideo.com/cmaskboss/786981347_30_0.webmask?trid=6e2458b79ffe449f9493f9f5214ed584B\u0026orderid=0,1\u0026logo=00000000'
url = url.replace(r'\u0026', '') 

video = requests.get(url, headers=BiliClass.BiliDownloadHeaders)
print(video)
with open('C:/Users/DELL/Desktop/video11111.mp4', 'wb') as f:
    f.write(video.content)
"""


