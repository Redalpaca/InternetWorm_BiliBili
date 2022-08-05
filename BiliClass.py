from tkinter import N
import requests
import re
from bs4 import BeautifulSoup
import json
import os


#注意cookie时不时更换一下，不然会失效。
#os.system 每调用一次命令就打开一个子进程, 不会影响父进程, 调用完则关闭, 因此连续的一系列命令需要一起调用 
#os.system 调用第三方工具是从System32文件夹调用, 若报错命令不存在则可尝试将第三方工具复制到该文件夹内
#ffmpeg参数: -y遇到同名文件强制覆盖(-n则相反), -loglevel quiet可设置让其不返回信息

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
BiliDownloadHeaders = {
'referer':'https://www.bilibili.com/video/BV1m44y1u7bs',
'user-agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/103.0.0.0Safari/537.36'
}


def GetTitle(url, headers= BiliUniHeaders):
    html = requests.get(url, headers).text
    soup = BeautifulSoup(html, 'lxml')
    return soup.title.string
def GetSoup(url, headers= BiliUniHeaders):
    html = requests.get(url, headers).text
    soup = BeautifulSoup(html, 'lxml')
    return soup
def GetHtml(url, Headers):
    res = requests.get(url, headers=Headers)
    html = res.text
    return html
def GetContent(url, headers_0):
    return requests.get(url, headers=headers_0).content
def Status(status_code:str)->bool:
    modeStr = re.compile('2..')
    res = re.search(modeStr, status_code)
    if(res != None):
        return True
    return False


class BiliVideo(object):
    model = 'https://www.bilibili.com/video/'
    UniHeaders = BiliUniHeaders
    StatusModeStr = re.compile('2..')
    
    def __init__(self, bvid: str, BiliHeaders: dict= BiliUniHeaders):
        #Web attrs
        self.url = BiliVideo.model + bvid
        self.Headers = BiliHeaders
        self.DownloadHeaders = BiliDownloadHeaders
        self.html = GetHtml(self.url, self.Headers)
        if re.search(BiliVideo.StatusModeStr, str(requests.get(self.url, headers=BiliUniHeaders).status_code)) == None:
            print('Illigal bvid.')
            return None   
        
        #Video id (and mid of the author)
        self.bvid = bvid
        self.aid = re.search(re.compile(r'\"aid\":(\b\d+\b)'), self.html).group(1)
        self.cid = re.search(re.compile(r'\"cid\":(\b\d+\b)'), self.html).group(1)
        self.mid_author = re.search(re.compile(r'mid=(\b\d+\b)'), self.html).group(1)
        
        #Get title
        self.title = (re.search(re.compile('(.*?)_哔哩哔哩_') ,GetTitle(self.url, self.Headers))).group(1)
        pass
    #Get fundamental message
    def GetAID(self):
        print(self.aid)
        return self.aid
    def GetCID(self):
        print(self.cid)
        return self.cid
    def TotalMessage(self):
        Mdict = {'title':'','author':'','play':'','coin':'','favor':'','comment':'','star':'','share':'','danmu':''}
        Html = GetHtml(self.url, self.Headers)
        Mdict['title'] = self.title
        Mdict['author'] = re.search(re.compile('视频作者 (.*?)[,、]'), Html).group(1)
        Mdict['play'] = re.search(re.compile('视频播放量 (\d+)'), Html).group(1)
        Mdict['coin'] = re.search(re.compile('投硬币枚数 (\d+)'), Html).group(1)
        Mdict['favor'] = re.search(re.compile('点赞数 (\d+)'), Html).group(1)
        Mdict['star'] = re.search(re.compile('收藏人数 (\d+)'), Html).group(1)
        Mdict['share'] = re.search(re.compile('转发人数 (\d+)'), Html).group(1)
        Mdict['danmu'] = re.search(re.compile('弹幕量 (\d+)'), Html).group(1)
        #soup= GetSoup(self.url, self.Headers)
        #评论是动态加载的，不嵌在html代码中，常规静态爬取做不到，需要动态爬虫。
        #如果直接通过api接口拿json的话也可以
        #api: https://api.bilibili.com/x/v2/reply?&jsonp=jsonp&pn=%&type=1&oid={AID}&sort=%
        #Mdict['comment'] = soup.find(name='div', id ='comment')
        return Mdict

    #Download the video
    def DownloadLink(self, quality: int=0): #if quality == 1, you will get high_quality videolink
        TemplateURL = 'https://api.bilibili.com/x/player/playurl?avid={AID}&cid={CID}&qn=1&type=&otype=json&platform=html5&high_quality={Bool}'
        JumpURL = TemplateURL.format(AID = self.aid, CID = self.cid, Bool = quality)
        JumpHtml = requests.get(JumpURL, headers={}).text #不需要请求头
        DownloadURL_0 = re.search(re.compile('\"url\":\"(.*?)\"'), JumpHtml).group(1)
        DownloadURL = DownloadURL_0.replace(r'\u0026','&')
        return DownloadURL
    def DownloadVideo(self, location: str='C:/Users/DELL/Desktop/video_4.mp4', quality: int=0):
        DownloadURL = self.DownloadLink(quality)
        video = requests.get(DownloadURL, headers=self.Headers).content
        with open(location, 'wb') as f:
            f.write(video)
        print('{name}.mp4 Down.'.format(name= self.title), end=' ')
        return 0
    
    #获取指定清晰度的视频音频原始URL
    #设定的tail参数是为了下载多p视频而准备的, 普通视频默认无tail
    def DetailedLink(self, AutoQuality: str='360p', tail = ''):
        html = requests.get(url=self.url + tail, headers=self.Headers).text
        #Ctrl+F搜索以获悉不同清晰度的播放链接位置。这些信息是以json格式存储的。分析结构得到结果
        modestr = re.compile('window.__playinfo__=(.*?)</script>')
        jsonFile = re.search(modestr, html).group(1)
        dict_0 = json.loads(jsonFile)
        VideoList = dict_0['data']['dash']['video']
        AudioList = dict_0['data']['dash']['audio']
        
        QualityDict = {"4k":[120,6], "1080p+":[112,5], "1080p":[80,4], "720p":[64,3], "480p":[32,2], "360p":[16,1]}
        ReverseQualityDict = {'120':'4k','112':'1080p+','80':'1080p','64':'720p','32':'480p'}
        
        MaxQuality = VideoList[0]['id']
        ListLen = len(VideoList)
        descript = AutoQuality
        #输入清晰度的格式是否正确
        try:
            QualityDict[descript]
        except:
            print('\"%s\" has illigal format.'%descript)
            print('LegalFormat: [4k,1080p+,1080p,720p,480p,360p]')
            return None
        #该清晰度是否允许下载
        if(QualityDict[descript][0] > MaxQuality):
            print('The VideoQuality is too high.(Or the Cookie is Overdue)')
            print('HighestQuality: %s'%ReverseQualityDict[str(MaxQuality)])
            return None

        index = ListLen - QualityDict[descript][1]
        #print(index)
        #print(VideoList[index]['id'])
        #print(VideoList[index]['baseUrl'])
        Tempdict= {'video':VideoList[index]['baseUrl'], 'audio':AudioList[0]['baseUrl']}
        return Tempdict
        pass    
    #可分清晰度的下载 (仅下载纯视频或音频, 音频仅下载最高清晰度的)
    def DetailedVideoDownload(self, Quality:str ='360p', location= 'C:/Users/DELL/Desktop/'):
        DownloadURL = self.DetailedLink(Quality)['video']
        Video = requests.get(DownloadURL, headers=BiliDownloadHeaders).content
        print('Downloading')
        with open(location + self.title + Quality +'.mp4', 'wb') as f:
            f.write(Video)
        print('{name}.mp4 Down.'.format(name= self.title + Quality))
        pass
    def DetailedAudioDownload(self, location= 'C:/Users/DELL/Desktop/'):
        DownloadURL = self.DetailedLink()['audio']
        Audio = requests.get(DownloadURL, headers=BiliDownloadHeaders).content
        with open(location + self.title +'.mp3', 'wb') as f:
            f.write(Audio)
        print('{name}.mp3 Down.'.format(name= self.title))
        pass
    #音视频下载并合并
    def MergeOutput(self, Quality = '360p', path = 'C:/Users/DELL/Desktop/'):
        Link = self.DetailedLink(Quality)
        if Link == None: #检测获取链接的函数结果是否有误
            return
        VideoURL = Link['video']
        AudioURL = Link['audio']
        Video = requests.get(VideoURL, headers= BiliDownloadHeaders).content
        Audio = requests.get(AudioURL, headers= BiliDownloadHeaders).content
        print('Downloading video: BVid=%s'%self.bvid)
        videoname = path + self.title + Quality +'_video.mp4'
        audioname = path + self.title + '_audio.mp3'
        with open(videoname, 'wb') as f:
            f.write(Video)
        with open(audioname, 'wb') as f:
            f.write(Audio)
        print('OutputPath:', end=' ')
        print(path+self.title+Quality + '.mp4')
        #可以设置让ffmpeg命令不返回信息: 使用命令-loglevel quiet, -y参数告知ffmpeg检测到同名文件则强制覆盖
        os.system('ffmpeg -n -loglevel quiet -i \"{video}\" -i \"{audio}\" -c copy \"{video_out}.mp4\"'.format(video = videoname, audio = audioname, video_out = path+self.title + Quality))
        #删除纯视频和音频文件
        os.remove('%s'%videoname)
        os.remove('%s'%audioname)
        print('Video:%s.mp4 Merge Over.'%(self.title + Quality))
        pass
    
    #下载多p视频的方法
    #由于附加了多p检测, 对所有视频都可以使用该方法.
    def MultipleDown(self, Quality='360p', path= 'C:/Users/DELL/Desktop/'):
        #防止对普通视频误调用该方法, 只需附加多p检测
        mode = re.compile('视频选集')
        if re.search(mode, self.html) == None:
            #print('This is a Single Video.')
            self.MergeOutput(Quality, path)
            return
        
        #正则获取该投稿内的视频总数
        mode = re.compile('>\(\d/(\d)\)</span')
        Amount = re.search(mode, self.html).group(1)
        
        #创建新文件夹
        path = path + str(self.bvid) + '/'
        if(not os.path.exists(path)):
            os.makedirs(path)
        else: #若目录已存在则说明已经下载过了
            print('Dir already exist.')

        #循环下载多p视频
        for i in range(int(Amount)):
            Link = self.DetailedLink(Quality, tail='?p={index}'.format(index = i+1))#设置tail参数获取其它p的下载地址
            VideoURL = Link['video']
            AudioURL = Link['audio']
            Video = requests.get(VideoURL, headers= BiliDownloadHeaders).content
            Audio = requests.get(AudioURL, headers= BiliDownloadHeaders).content
            videoname = path + self.title + Quality +'_video.mp4'
            audioname = path + self.title + '_audio.mp3'
            with open(videoname, 'wb') as f:
                f.write(Video)
            with open(audioname, 'wb') as f:
                f.write(Audio)
            command = 'ffmpeg -n -loglevel quiet -i \"{video}\" -i \"{audio}\" -c copy \"{video_out}.mp4\"'.format(video = videoname, audio = audioname, video_out = path + self.title + Quality + '_p' + str(i+1))
            os.system(command)
            os.remove('%s'%videoname)
            os.remove('%s'%audioname)
            print('p{index} done.'.format(index = i+1))
        pass
    
    pass
    

class Person(object):
    SpaceURL_mode = 'https://space.bilibili.com/{userID}'
    def __init__(self, userID):
        self.userID = userID
        self.SpaceURL = Person.SpaceURL_mode.format(userID = userID)
        pass
    
    def name(self):
        pass
    def headpic(self):
        pass
    def VideoList(self):
        pass

#Video = BiliVideo('BV1Kt4y1a78y')
#Video.MultipleDown()




