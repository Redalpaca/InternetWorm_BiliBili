import requests
import re
from bs4 import BeautifulSoup
import json
import os
from tqdm import tqdm
#重要提醒: 注意在本项目中, 函数或方法的path参数通常都需要在末尾添加'/', 如:'C:/Users/DELL/Desktop/'
#重要提醒: 支持不同清晰度下载的方法需要ffmpeg第三方工具的支持, 若cmd显示找不到对应的程序, 可尝试将ffmpeg.exe放入system32文件夹中(详见python os.system函数的具体实现方式)

#注意cookie时不时更换一下，不然会失效。
#有时候cookie在原视频网址中会失效, 应尝试使用api网页重新获取cookie

#os.system 每调用一次命令就打开一个子进程, 不会影响父进程, 调用完则关闭, 因此连续的一系列命令需要一起调用 
#os.system 调用第三方工具是从System32文件夹调用, 若报错命令不存在则可尝试将第三方工具复制到该文件夹内
#ffmpeg参数: -y遇到同名文件强制覆盖(-n则相反), -loglevel quiet可设置让其不返回信息

BiliUniHeaders = {
'authority':'www.bilibili.com',
'method':'GET',
#s'path': '/video/BV1NY4y1E7Dd',
'scheme':'https',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'zh,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
'cookie':'buvid3=C6FA7D37-BDAB-8A98-F46C-F74DCCD9E1E590619infoc; _uuid=611AEF8F-FA10A-F25E-63B1-7C6851A3E69C92883infoc; buvid4=A0BF7CAD-00E0-291D-0057-8C4CC946B8DF91548-022012618-yPTK2yRnbGG1AbZfVzPX2Q%3D%3D; rpdid=|(kRJkkRmJ~0J\'uYRJumJumJ; buvid_fp_plain=undefined; blackside_state=0; CURRENT_BLACKGAP=0; i-wanna-go-back=-1; b_ut=5; LIVE_BUVID=AUTO9316494943737456; is-2022-channel=1; nostalgia_conf=-1; hit-dyn-v2=1; go_old_video=-1; theme_style=light; bsource=search_baidu; fingerprint3=b91abfafa0dabad6a036f1b9b0f4c5f3; fingerprint=e5690504a7252e22c88daa209cce9049; CURRENT_FNVAL=4048; b_lsid=B49FD875_182861848B2; b_timer=%7B%22ffp%22%3A%7B%22333.788.fp.risk_C6FA7D37%22%3A%221828618A9AA%22%2C%22333.1193.fp.risk_C6FA7D37%22%3A%221828189D702%22%2C%22333.999.fp.risk_C6FA7D37%22%3A%2218286187503%22%2C%22888.2421.fp.risk_C6FA7D37%22%3A%221828193B951%22%2C%22666.25.fp.risk_C6FA7D37%22%3A%22182859DCF3D%22%2C%22333.976.fp.risk_C6FA7D37%22%3A%2218272FE2BEE%22%2C%22444.41.fp.risk_C6FA7D37%22%3A%221827BA2EEE0%22%2C%22333.937.fp.risk_C6FA7D37%22%3A%22182731D8041%22%2C%22333.337.fp.risk_C6FA7D37%22%3A%221828596C0EF%22%2C%22777.5.0.0.fp.risk_C6FA7D37%22%3A%221828193925D%22%2C%22666.19.fp.risk_C6FA7D37%22%3A%2218276C82C19%22%2C%22333.967.fp.risk_C6FA7D37%22%3A%22182818AB45E%22%2C%22333.880.fp.risk_C6FA7D37%22%3A%221828193B897%22%2C%22333.42.fp.risk_C6FA7D37%22%3A%22182861C7407%22%7D%7D; SESSDATA=e20c69d7%2C1675659396%2C09715%2A81; bili_jct=54992fbb96d8876b46cc8abb37df1a57; DedeUserID=35671002; DedeUserID__ckMd5=d69f732e9248e565; buvid_fp=e5690504a7252e22c88daa209cce9049; CURRENT_QUALITY=116; bp_video_offset_35671002=692641245482188900; sid=7p2ab96c; PVID=11',
'referer':'www.bilibili.com',
'sec-ch-ua-mobile': '?0',
'sec-fetch-dest': 'document',
'sec-ch-ua-platform':'"Windows"',
'sec-fetch-dest':'document',
'sec-fetch-mode':'navigate',
'sec-fetch-site':'same-origin',
'sec-fetch-user':'?1',
'upgrade-insecure-requests':'1',
'user-agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/103.0.0.0Safari/537.36'
}
BiliDownloadHeaders = {
'referer':'https://www.bilibili.com/',
'user-agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/103.0.0.0Safari/537.36'
}
BiliApiHeaders = {
    'authority':'api.bilibili.com',
    'method':'GET',
    'scheme':'https',
    'path':'/pgc/season/episode/web/info?ep_id=374680',
    'cookie':'buvid3=C6FA7D37-BDAB-8A98-F46C-F74DCCD9E1E590619infoc; _uuid=611AEF8F-FA10A-F25E-63B1-7C6851A3E69C92883infoc; buvid4=A0BF7CAD-00E0-291D-0057-8C4CC946B8DF91548-022012618-yPTK2yRnbGG1AbZfVzPX2Q%3D%3D; rpdid=|(kRJkkRmJ~0J\'uYRJumJumJ; fingerprint=163f019b63a8ac7654d7e8634c3127cf; buvid_fp_plain=undefined; buvid_fp=4d18731a5a709bbdb5ce9d474ce68827; SESSDATA=201e1f7f%2C1665046259%2C56fc0%2A41; bili_jct=64787cb69067364c5e44cd1c3dd05938; DedeUserID=35671002; DedeUserID__ckMd5=d69f732e9248e565; sid=86748t3l; CURRENT_BLACKGAP=0; blackside_state=0; i-wanna-go-back=-1; b_ut=5; LIVE_BUVID=AUTO9316494943737456; is-2022-channel=1; nostalgia_conf=-1; hit-dyn-v2=1; go_old_video=-1; CURRENT_QUALITY=120; bsource=search_baidu; CURRENT_FNVAL=4048; bp_video_offset_35671002=691888544094879700; b_lsid=754D10442_1827BBDB3BF; PVID=2; b_timer=%7B%22ffp%22%3A%7B%22333.788.fp.risk_C6FA7D37%22%3A%221827BA2FD18%22%2C%22333.1193.fp.risk_C6FA7D37%22%3A%221827BDB67F0%22%2C%22333.999.fp.risk_C6FA7D37%22%3A%221827BCDAD31%22%2C%22888.2421.fp.risk_C6FA7D37%22%3A%221827BD6F803%22%2C%22666.25.fp.risk_C6FA7D37%22%3A%2218277746742%22%2C%22333.976.fp.risk_C6FA7D37%22%3A%2218272FE2BEE%22%2C%22444.41.fp.risk_C6FA7D37%22%3A%221827BA2EEE0%22%2C%22333.937.fp.risk_C6FA7D37%22%3A%22182731D8041%22%2C%22333.337.fp.risk_C6FA7D37%22%3A%2218276CD0604%22%2C%22777.5.0.0.fp.risk_C6FA7D37%22%3A%221827BCE5652%22%2C%22666.19.fp.risk_C6FA7D37%22%3A%2218276C82C19%22%7D%7D',
    #'referer':'www.bilibili.com/play/ep374676',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
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
#判断状态码是否有误
def Status(status_code:str)->bool:
    modeStr = re.compile('2..')
    res = re.search(modeStr, status_code)
    if(res != None):
        return True
    return False
#传入序列图片文件夹所在的目录与名称, 在指定目录输出gif图片
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
#传入链接与地址进行下载, 支持进度条显示
def Download_Pbar(url, path = 'C:/Users/DELL/Desktop/test1.mp4', headers = BiliDownloadHeaders):
    #先获取内容大小
    try:
        #stream元素设定当访问content元素时才获取输入流
        res = requests.get(url, headers= headers, stream= True)
        ResHeaders = res.headers
        file_size = int(ResHeaders['Content-Length'])
    except:
        print('ERROR: Unsuccessful to obtain the content.(Perhaps the url is overdue.)')
        file_size = 0
    #创建进度条类
    pbar = tqdm(
        total= file_size, initial= 0,
        unit= 'B', unit_scale= True, leave= True)
    with open(path, 'wb') as f:
        #使用迭代器模式获取content, 以1024Bytes为单位读取并写入本地
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(1024)#更新进度条
    pbar.close()
    return file_size
#cookie更新函数
def Cookie(apiURL):
    cookie = ''
    url = 'https://api.bilibili.com/x/player/v2?aid=643507695&cid=778294645'
    return cookie


class BiliVideo(object):
    model = 'https://www.bilibili.com/video/'
    UniHeaders = BiliUniHeaders
    StatusModeStr = re.compile('2..')
    
    def __init__(self, bvid: str, BiliHeaders: dict= BiliUniHeaders):
        #Web attrs
        self.url = BiliVideo.model + bvid
        self.Headers = BiliHeaders
        self.DownloadHeaders = BiliDownloadHeaders
        self.res = requests.get(self.url, headers= BiliUniHeaders)
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
        title = GetTitle(self.url, self.Headers)
        try:
            self.title = (re.search(re.compile('(.*?)_') ,title)).group(1)
        except:
            self.title = title
        pass
    #Get fundamental message
    def GetAID(self):
        print(self.aid)
        return self.aid
    def GetCID(self):
        print(self.cid)
        return self.cid
    #获取统计信息
    def TotalInfo(self):
        Html = self.res.text
        mode = '.{300}23295.{200}'
        mode = '"owner":{(.*?)}'
        AuthorInfo = re.search(mode, Html).group(1)
        mode = '"stat":{(.*?)}'
        VideoInfo = re.search(mode, Html).group(1)
        DictStr = '{' +VideoInfo + ',' + AuthorInfo +'}'
        InfoDict = json.loads(DictStr)
        return InfoDict
    #获取标签
    def GetTag(self, detailed = False):
        apiURL_mode = 'https://api.bilibili.com/x/web-interface/view/detail/tag?aid={aid}&cid={cid}'
        apiURL = apiURL_mode.format(aid = self.aid, cid = self.cid)
        res = requests.get(apiURL, headers= BiliApiHeaders)
        DetailDict = json.loads(res.text)
        if detailed :
            return DetailDict
        TagList = []
        for element in DetailDict['data']:
            temp = {'tag_id':element['tag_id'], 'tag_name':element['tag_name']}
            TagList.append(temp)
        return TagList
    #获取视频封面
    def GetFace(self, path = 'C:/Users/DELL/Desktop/'):
        '<meta data-vue-meta="true" itemprop="image" content="http://i0.hdslb.com/bfs/archive/9da93ef03a89a4384c03cca9189d61c964ebf20b.jpg">'
        soup = BeautifulSoup(self.html, 'lxml')
        node = soup.find('meta',attrs={'itemprop':"image"})
        url = node.attrs['content']
        Download_Pbar(url, path= path + self.title + '_封面.jpg')
        return True
        pass
    #获取评论
    def GetComments(self, index = 0):
        """
        Arg:
            mode (str, optional): Allows 'hot', 'new', 'regular', defaults to 'hot' 
            index (int, optional): Index refers to page of comment. A single page only shows 20 comments. 
        """
        mode = 'hot'
        modeDict = {'regular':1, 'new':2, 'hot':3}
        try:
            modeNum = modeDict[mode]
        except KeyError:
            print('Illigal mode.')
            modeNum = 3
            pass
        #next参数在热门评论模式(mode=3)下是显示第几页评论(1页20条)
        apiURL_mode = 'https://api.bilibili.com/x/v2/reply/main?mode={mode}&next={index}&oid={aid}&plat=1&type=1'
        apiURL = apiURL_mode.format(mode = modeNum, aid = self.aid, index = index)
        res = requests.get(apiURL, headers= BiliApiHeaders)
        dict_0 = json.loads(res.text)
        RepliesList = dict_0['data']['replies']
        if RepliesList == None:
            return None
        FinalList = []
        print(len(RepliesList))
        for element in RepliesList:
            #从单独api无法获取楼中楼所有评论, 进入新的api需要replyID
            rpid = element['rpid_str']
            temp = {'userID':element['mid'], 'content':element['content']['message'], 'InnerReplies':None}
            apiURL_root = 'https://api.bilibili.com/x/v2/reply/reply?oid={aid}&pn=1&ps=10&type=1&root={rpid}'
            apiURL_root = apiURL_root.format(aid = self.aid, rpid = rpid)
            if element['replies'] != None:
                res = requests.get(apiURL_root, headers= BiliApiHeaders)
                dict_1 = json.loads(res.text)
                InnerReplies = dict_1['data']['replies']

                SimpleReplyList = []
                try:
                    for reply in InnerReplies:
                        Innertemp = {'userID':reply['mid'], 'content':reply['content']['message']}
                        SimpleReplyList.append(Innertemp)
                    temp['InnerReplies'] = SimpleReplyList
                except TypeError:
                    pass
            FinalList.append(temp)
            pass

        #print(len(RepliesList[0]['replies']))
        #for key, value in RepliesList[0].items():
        #    print(key, value, end='\n\n')
        return FinalList
        pass
    #子类中的测试方法, 仅bangumi对象可以调用
    def OrderNum(self):
        if type(self) != Bangumi:
            print('This video might not be bangumi.')
            return False
        soup = BeautifulSoup(self.res.text, 'lxml')
        #'<span class="ep-list-progress">6/6</span>'
        temp = soup.find('span', class_= 'ep-list-progress').string
        mode = re.compile('(\d+)/(\d+)')
        index = re.search(mode, temp).group(1)
        total = re.search(mode, temp).group(2)
        return [index, total]
    #简易下载
    def DownloadLink(self, quality: int=0): #if quality == 1, you will get high_quality videolink
        #类名检测
        if type(self) == Bangumi:
            print('This video might be bangumi, try method: DetailedLink')
            return False
        TemplateURL = 'https://api.bilibili.com/x/player/playurl?avid={AID}&cid={CID}&qn=1&type=&otype=json&platform=html5&high_quality={Bool}'
        JumpURL = TemplateURL.format(AID = self.aid, CID = self.cid, Bool = quality)
        JumpHtml = requests.get(JumpURL, headers={}).text #不需要请求头
        try:
            DownloadURL_0 = re.search(re.compile('\"url\":\"(.*?)\"'), JumpHtml).group(1)
        except:
            return ''
        DownloadURL = DownloadURL_0.replace(r'\u0026','&')
        return DownloadURL
    def DownloadVideo(self, location: str='C:/Users/DELL/Desktop/video_4.mp4', quality: int=0):
        #类名检测
        if type(self) == Bangumi:
            print('This video might be bangumi, try method: MergeOutput(or MultipleDown)')
            return False
        DownloadURL = self.DownloadLink(quality)
        video = requests.get(DownloadURL, headers=self.Headers).content
        with open(location, 'wb') as f:
            f.write(video)
        print('{name}.mp4 Down.'.format(name= self.title), end=' ')
        return True
    #原始版本: 获取指定清晰度的视频音频原始URL
    """ 
    ! Attention !
    原DetailedLink方法获取的视频链接会定时失效, 需要对获取的链接更换域名
    """
    #设定的tail参数是为了下载多p视频而准备的, 普通视频默认无tail
    def DetailedLink_old(self, Quality: str='360p', tail = ''):
        html = requests.get(url=self.url + tail, headers= BiliUniHeaders).text
        #Ctrl+F搜索以获悉不同清晰度的播放链接位置。这些信息是以json格式存储的。分析结构得到结果
        modestr = re.compile('window.__playinfo__=(.*?)</script>')
        jsonFile = re.search(modestr, html).group(1)
        dict_0 = json.loads(jsonFile)

        VideoList = dict_0['data']['dash']['video']
        AudioList = dict_0['data']['dash']['audio']
        
        #1080p+有两种代码: 112, 116, 带来一定的困难
        QualityDict = {"4k":[120,6], "1080p+":[116,5], "1080p":[80,4], "720p":[64,3], "480p":[32,2], "360p":[16,1]}
        ReverseQualityDict = {'120':'4k','116':'1080p+','112':'1080p+','80':'1080p','64':'720p','32':'480p'}
        
        MaxQuality = VideoList[0]['id']
        print(MaxQuality)
        #注意ListLen不一定是清晰度的个数, 有些视频的list比较怪异, 是三个为一组的, 还是采用复杂度o(n)的线性查找吧, 反正表也不大.
        ListLen = len(VideoList)
        descript = Quality
        #输入清晰度的格式是否正确
        try:
            QualityDict[descript]
        except KeyError :
            print('\"%s\" has illigal format.'%descript)
            print('LegalFormat: [4k,1080p+,1080p,720p,480p,360p]')
            return {'video':VideoList[0]['baseUrl'], 'audio':AudioList[0]['baseUrl']}
        
        #清晰度是否过高
        if MaxQuality == 112: #处理特殊情况: 1080p+的id为112(番剧?)
            index = 0
            for i, element in enumerate(VideoList):
                if element['id'] == 112 :
                    index = i
                    break
            return {'video':VideoList[index]['baseUrl'], 'audio':AudioList[0]['baseUrl']}
        #正常情况下的处理: 在字典中寻找并比较id值
        if(QualityDict[descript][0] > MaxQuality):
            print('The VideoQuality is too high.(Or the Cookie is Overdue)')
            print('HighestQuality: %s'%ReverseQualityDict[str(MaxQuality)])
            return {'video':VideoList[0]['baseUrl'], 'audio':AudioList[0]['baseUrl']}

        index = 0
        #index = ListLen - QualityDict[descript][1]
        for i, element in enumerate(VideoList):
            if element['id'] == QualityDict[descript][0] :
                index = i
                break
        
        #print(QualityDict[descript][1])
        #print(index)
        #print(index)
        print('testID = ', end='')
        print(VideoList[index]['id'])
        #print(VideoList[index]['baseUrl'])
        Tempdict= {'video':VideoList[index]['baseUrl'], 'audio':AudioList[0]['baseUrl']}
        return Tempdict
        pass    
    #获取指定清晰度的视频音频原始URL的方法, 打了补丁
    #若失效, 尝试其他域名: upos-sz-mirrorali 
    def DetailedLink(self, Quality: str='360p', tail = ''):
        html = requests.get(url=self.url + tail, headers= BiliUniHeaders).text
        #Ctrl+F搜索以获悉不同清晰度的播放链接位置。这些信息是以json格式存储的。分析结构得到结果
        modestr = re.compile('window.__playinfo__=(.*?)</script>')
        jsonFile = re.search(modestr, html).group(1)
        dict_0 = json.loads(jsonFile)

        VideoList = dict_0['data']['dash']['video']
        AudioList = dict_0['data']['dash']['audio']
        
        #1080p+有两种代码: 112, 116, 带来一定的困难
        QualityDict = {"4k":[120,6], "1080p+":[116,5], "1080p":[80,4], "720p":[64,3], "480p":[32,2], "360p":[16,1]}
        ReverseQualityDict = {'120':'4k','116':'1080p+','112':'1080p+','80':'1080p','64':'720p','32':'480p'}
        
        MaxQuality = VideoList[0]['id']
        print(MaxQuality)
        #注意ListLen不一定是清晰度的个数, 有些视频的list比较怪异, 是三个为一组的, 还是采用复杂度o(n)的线性查找吧, 反正表也不大.
        ListLen = len(VideoList)
        descript = Quality
        #输入清晰度的格式是否正确
        try:
            QualityDict[descript]
        except KeyError :
            print('\"%s\" has illigal format.'%descript)
            print('LegalFormat: [4k,1080p+,1080p,720p,480p,360p]')
            return {'video':VideoList[0]['baseUrl'], 'audio':AudioList[0]['baseUrl']}
        
        #清晰度是否过高
        if MaxQuality == 112: #处理特殊情况: 1080p+的id为112(番剧?)
            index = 0
            for i, element in enumerate(VideoList):
                if element['id'] == 112 :
                    index = i
                    break
            return {'video':VideoList[index]['baseUrl'], 'audio':AudioList[0]['baseUrl']}
        #正常情况下的处理: 在字典中寻找并比较id值
        if(QualityDict[descript][0] > MaxQuality):
            print('The VideoQuality is too high.(Or the Cookie is Overdue)')
            print('HighestQuality: %s'%ReverseQualityDict[str(MaxQuality)])
            return {'video':VideoList[0]['baseUrl'], 'audio':AudioList[0]['baseUrl']}

        index = 0
        #index = ListLen - QualityDict[descript][1]
        for i, element in enumerate(VideoList):
            if element['id'] == QualityDict[descript][0] :
                index = i
                break
        VideoUrl:str = VideoList[index]['baseUrl']
        AudioUrl:str = AudioList[0]['baseUrl']
        
        #测试用代码, 观察清晰度选择是否出现问题
        print('testID = ', end='')
        print(VideoList[index]['id'])
        
        
        
        #补丁部分, 修改获取的临时url的域名
        modestr = re.compile('https://(.*?).bilivideo.com') 
        substr = re.search(modestr, VideoUrl).group(1)
        VideoUrl = VideoUrl.replace(substr, 'upos-sz-mirrorhwo1')
        
        #print(VideoList[index]['baseUrl'])
        Tempdict= {'video':VideoUrl, 'audio':AudioUrl}
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
    def DetailedAudioDownload(self, Quality:str ='360p', location= 'C:/Users/DELL/Desktop/'):
        DownloadURL = self.DetailedLink()['audio']
        Audio = requests.get(DownloadURL, headers=BiliDownloadHeaders).content
        with open(location + self.title + Quality + '.mp3', 'wb') as f:
            f.write(Audio)
        print('{name}.mp3 Down.'.format(name= self.title))
        pass
    #音视频下载并合并
    def MergeOutput(self, Quality = '360p', path = 'C:/Users/DELL/Desktop/', AddName = '', pbar = False):
        #类名检测, 若是番剧类型则将名称附上序号
        """
        if type(self) == Bangumi:
            order = self.OrderNum()[0]
            print('Order = {order}'.format(order = order))
            AddName = '_No.' + order
        """
        Link = self.DetailedLink(Quality)
        if Link == None: #检测获取链接的函数结果是否有误
            return
        VideoURL = Link['video']
        AudioURL = Link['audio']
        videoname = path + self.title + Quality +'_video.mp4'
        audioname = path + self.title + '_audio.mp3'
        
        #是否启用进度条?
        if pbar == True:
            print('Downloading video:')
            Download_Pbar(VideoURL, path = videoname)
            print('Downloading audio:')
            Download_Pbar(AudioURL, path = audioname)
            pass
        else:
            Video = requests.get(VideoURL, headers= BiliDownloadHeaders).content
            Audio = requests.get(AudioURL, headers= BiliDownloadHeaders).content
            with open(videoname, 'wb') as f:
                f.write(Video)
            with open(audioname, 'wb') as f:
                f.write(Audio)
        
        print(f'OutputPath: {path}')
        #可以设置让ffmpeg命令不返回信息: 使用命令-loglevel quiet, -y参数告知ffmpeg检测到同名文件则强制覆盖
        os.system('ffmpeg -n -loglevel quiet -i \"{video}\" -i \"{audio}\" -c copy \"{video_out}.mp4\"'.format(video = videoname, audio = audioname, video_out = path + self.title + Quality + AddName))
        #删除纯视频和音频文件
        os.remove('%s'%videoname)
        os.remove('%s'%audioname)
        print('Video:%s.mp4 Merge Over.'%(self.title + Quality + AddName))
        pass
    #下载多p视频的方法
    #由于附加了多p检测, 对所有视频都可以使用该方法.
    def MultipleDown(self, Quality='360p', path= 'C:/Users/DELL/Desktop/', intergrate = False, begin = 1, end = 1000, pbar = False):
        path_origin = path
        #防止对普通视频误调用该方法, 附加多p检测
        mode = re.compile('视频选集')
        if re.search(mode, self.html) == None:
            #print('This is a Single Video.')
            self.MergeOutput(Quality, path)
            return
        #正则获取该投稿内的视频总数
        mode = re.compile('>\(\d/(\d+)\)</span')
        Amount = re.search(mode, self.html).group(1)
        #确定下载范围, 防止越界
        end = end if int(Amount) > end else int(Amount)
        begin = begin if end >= begin else 1
        #创建新文件夹
        path = path + str(self.bvid) + '/'
        if(not os.path.exists(path)):
            os.makedirs(path)
        else: #若目录已存在则说明已经下载过了
            print('Dir already exist.')
        #循环下载多p视频
        for i in range(begin-1, end):
            Link = self.DetailedLink(Quality, tail='?p={index}'.format(index = i+1))#设置tail参数获取其它p的下载地址
            #获取url与名称
            VideoURL = Link['video']
            AudioURL = Link['audio']
            videoname = path + self.bvid + Quality +'_video.mp4'
            audioname = path + self.bvid + Quality +'_audio.mp3'
            #是否启用进度条?
            if pbar == True:
                print('Downloading video:')
                Download_Pbar(VideoURL, path = videoname)
                print('Downloading audio:')
                Download_Pbar(AudioURL, path = audioname)
                pass
            else:    
                Video = requests.get(VideoURL, headers= BiliDownloadHeaders).content
                Audio = requests.get(AudioURL, headers= BiliDownloadHeaders).content
                with open(videoname, 'wb') as f:
                    f.write(Video)
                with open(audioname, 'wb') as f:
                    f.write(Audio)
                
            
            #-n参数 默认不进行强制覆盖
            command = 'ffmpeg -n -loglevel quiet -i \"{video}\" -i \"{audio}\" -c copy \"{video_out}.mp4\"'.format(video = videoname, audio = audioname, video_out = path + self.bvid + Quality + '_p' + str(i+1))
            os.system(command)
            os.remove('%s'%videoname)
            os.remove('%s'%audioname)
            print('p{index} done.'.format(index = i+1))
        pass
        
        #视频拼接模块
        if intergrate :
            Intergrate(self.bvid, path_origin, path_origin)
            pass
    
    pass

#目前传参时允许使用seasonID
class Bangumi(BiliVideo):
    model = 'https://www.bilibili.com/bangumi/play/'
    #另一个示例: 获取链接的apiURL, qn参数是视频质量. 'https://api.bilibili.com/pgc/player/web/playurl?avid=59570290&cid=440840202&qn=120&ep_id=278577'
    #在Bangumi实例进行下载, 可采用父类的MergeOutput方法(也可单独下载音频或视频), 也可使用新定义的SerialDownload方法
    
    #类构造方法覆盖父类BiliVideo
    def __init__(self, bangumiID: str):
        """_summary_
        Args:
            bangumiID (str): please give the epid or seasonID of the bangumi(eg. ep21788, ss688)
        """
        #基本信息
        self.url = Bangumi.model + bangumiID
        self.id = bangumiID
        self.Headers = BiliUniHeaders
        self.DownHeaders = BiliDownloadHeaders
        
        #获取信息
        self.res = requests.get(self.url, headers= self.Headers)
        self.html = self.res.text
        title = GetTitle(self.url, headers=self.Headers)
        self.title = re.search(re.compile('(.*?)-'), title).group(1)
        self.ep_id = ''
        mode = 'ep_id":(\d+),'
        temp = re.search(mode, self.res.text)
        if temp != None:
            self.ep_id = temp.group(1)
        
        #防出错
        self.bvid = ''
        self.aid = ''
        self.cid = ''
        pass
    #获取该集在整部剧集中的序号
    def OrderNum(self):
        soup = BeautifulSoup(self.res.text, 'lxml')
        #'<span class="ep-list-progress">6/6</span>'
        temp = soup.find('span', class_= 'ep-list-progress').string
        mode = re.compile('(\d+)/(\d+)')
        index = re.search(mode, temp).group(1)
        total = re.search(mode, temp).group(2)
        return [index, total]
    #获取seasonID和mediaID(剧集的定位ID)
    def Origin(self):
        html = self.res.text
        mediaID = re.search('media/md(\d+)/' ,html).group(1)
        soup = BeautifulSoup(html, 'lxml')
        node = soup.find('meta',attrs={'property':'og:url'}) #获取对应节点
        InitialURL = node.attrs['content'] #获取节点属性content
        seasonID = re.search('/ss(\d+)/' ,InitialURL).group(1)
        return {'mediaID':mediaID, 'seasonID':seasonID}
    #覆盖父类方法, 获取统计信息
    def TotalInfo(self):
        apiURL_mode = 'https://api.bilibili.com/pgc/season/episode/web/info?ep_id={ep_id}'
        apiURL = apiURL_mode.format(ep_id = self.ep_id)
        res = requests.get(apiURL, headers=BiliUniHeaders)
        dict_0 = json.loads(res.text)
        dict_info = dict_0['data']['stat']
        return dict_info
    #获取整部剧集的统计信息
    def SeasonInfo(self):
        apiURL_mode = 'https://api.bilibili.com/pgc/web/season/stat?season_id={season_id}'
        seasonID = self.Origin()['seasonID']
        apiURL = apiURL_mode.format(season_id = seasonID)
        res = requests.get(apiURL, headers=BiliUniHeaders)
        dict_0 = json.loads(res.text)
        dict_info = dict_0['result']
        return dict_info
    #获取整部剧集所有分集的epID
    def SerialIDList(self):
        #这个api中含有每一话的id与标题等基本信息
        apiURL_mode = 'https://api.bilibili.com/pgc/view/web/season?ep_id={ep_id}'
        apiURL = apiURL_mode.format(ep_id = self.ep_id)
        res = requests.get(apiURL, headers=BiliUniHeaders)
        dict_0 = json.loads(res.text)
        InfoList = dict_0['result']['episodes']
        idList = [] #记录信息
        for element in InfoList :
            idList.append('ep' + str(element['id']))
        return idList
    #选择下载整个系列的哪一部分内容
    def SerialDownload(self, Quality='360p', path = 'C:/Users/DELL/Desktop/', begin=1, end=1000):
        """_summary_
        Args:
            path ATTENTION: Requires '/' at the end of the string
            begin (int, optional): The first episode user wants to get. Defaults to 1.
            end (int, optional): The last episode user wants to get. Defaults to 1000.
        """
        #创建新文件夹
        path = path + str(self.title) + '/'
        if(not os.path.exists(path)):
            os.makedirs(path)
        else: #若目录已存在则说明已经下载过了
            print('Dir already exist.')
        idList = self.SerialIDList()
        #对id进行切片以获取指定的下载范围
        end = end if end <= len(idList) else len(idList) 
        DownList = idList[begin-1:end]
        for index, id in enumerate(DownList, begin):
            temp = Bangumi(id)
            temp.MergeOutput(Quality=Quality, AddName='_%d'%index, path= path)
        pass
    pass


#bangumi = Bangumi('ss36198')
#print(bangumi.title)
#bangumi.MergeOutput()
def main():
    #上方这个url在经过一段时间后会自动失效, 这是从html代码中获取的 (即DetailedLink方法获取的)
    #将域名cn-hbwh-fx-bcache-11.bilivideo.com替换为upos-sz-mirrorhwo1.bilivideo.com, 可以解决这个问题
    url = 'https://cn-hbwh-fx-bcache-11.bilivideo.com/upgcxcode/31/69/493596931/493596931-1-30080.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1661357632&gen=playurlv2&os=bcache&oi=1939639009&trid=0000cd360b509dc64a8692d926fd25ce02c6p&mid=35671002&platform=pc&upsig=7b28cebb5311a53c4b7af38aa904987c&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&cdnid=3881&bvc=vod&nettype=0&orderid=0,3&agrr=0&bw=243430&logo=80000000'
    url = 'https://upos-sz-mirrorhwo1.bilivideo.com/upgcxcode/31/69/493596931/493596931-1-30080.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1661357632&gen=playurlv2&os=bcache&oi=1939639009&trid=0000cd360b509dc64a8692d926fd25ce02c6p&mid=35671002&platform=pc&upsig=7b28cebb5311a53c4b7af38aa904987c&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&cdnid=3881&bvc=vod&nettype=0&orderid=0,3&agrr=0&bw=243430&logo=80000000'
    
    url = 'https://upos-sz-mirrorhwo1.bilivideo.com/upgcxcode/31/69/493596931/493596931_hr1-1-30125.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1661358637&gen=playurlv2&os=bcache&oi=1939639009&trid=00008f3acc7a1a3d48f289c9c3f07c68fc78p&mid=35671002&platform=pc&upsig=6f60652ec77c6ae6117f5706d1dd05ba&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&cdnid=3875&bvc=vod&nettype=0&orderid=0,2&agrr=0&bw=691604&logo=80000000' 
    Download_Pbar(url=url, path='C:/Users/DELL/Desktop/test5.mp4')
    
    bangumi = Bangumi('ep451884')
    #bangumi.MergeOutput(pbar= True, Quality= '1080p')
    #print(bangumi.DetailedLink_1(Quality= '1080p+'))
    
    pass


if __name__ == '__main__':
    main()
    








