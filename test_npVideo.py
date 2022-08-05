from BiliClass import BiliVideo
#import BiliClass_func
import re
import os
import requests



'BV1pa411q7AM'
'BV1Kt4y1a78y'
video = BiliVideo('BV1pa411q7AM')
html = video.html
mode = re.compile('视频选集')
if re.search(mode, html) != None:
    pass    

mode = re.compile('>\(\d/(\d)\)</span')
Amount = re.search(mode, html).group(1)





