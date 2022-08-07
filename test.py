import requests
import os
import ffmpeg
from setuptools import Command


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


