from email import header
import requests
import re
from bs4 import BeautifulSoup
import json
import os
from BiliClass import BiliVideo
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

BiliUniHeaders = {
'authority':'www.bilibili.com',
'method':'GET',
'scheme':'https',
'cookie':'buvid3=C6FA7D37-BDAB-8A98-F46C-F74DCCD9E1E590619infoc; _uuid=611AEF8F-FA10A-F25E-63B1-7C6851A3E69C92883infoc; buvid4=A0BF7CAD-00E0-291D-0057-8C4CC946B8DF91548-022012618-yPTK2yRnbGG1AbZfVzPX2Q%3D%3D; rpdid=|(kRJkkRmJ~0J\'uYRJumJumJ; buvid_fp_plain=undefined; blackside_state=0; CURRENT_BLACKGAP=0; i-wanna-go-back=-1; b_ut=5; LIVE_BUVID=AUTO9316494943737456; is-2022-channel=1; nostalgia_conf=-1; hit-dyn-v2=1; go_old_video=-1; theme_style=light; bsource=search_baidu; fingerprint3=b91abfafa0dabad6a036f1b9b0f4c5f3; fingerprint=e5690504a7252e22c88daa209cce9049; CURRENT_FNVAL=4048; b_lsid=B49FD875_182861848B2; b_timer=%7B%22ffp%22%3A%7B%22333.788.fp.risk_C6FA7D37%22%3A%221828618A9AA%22%2C%22333.1193.fp.risk_C6FA7D37%22%3A%221828189D702%22%2C%22333.999.fp.risk_C6FA7D37%22%3A%2218286187503%22%2C%22888.2421.fp.risk_C6FA7D37%22%3A%221828193B951%22%2C%22666.25.fp.risk_C6FA7D37%22%3A%22182859DCF3D%22%2C%22333.976.fp.risk_C6FA7D37%22%3A%2218272FE2BEE%22%2C%22444.41.fp.risk_C6FA7D37%22%3A%221827BA2EEE0%22%2C%22333.937.fp.risk_C6FA7D37%22%3A%22182731D8041%22%2C%22333.337.fp.risk_C6FA7D37%22%3A%221828596C0EF%22%2C%22777.5.0.0.fp.risk_C6FA7D37%22%3A%221828193925D%22%2C%22666.19.fp.risk_C6FA7D37%22%3A%2218276C82C19%22%2C%22333.967.fp.risk_C6FA7D37%22%3A%22182818AB45E%22%2C%22333.880.fp.risk_C6FA7D37%22%3A%221828193B897%22%2C%22333.42.fp.risk_C6FA7D37%22%3A%22182861C7407%22%7D%7D; SESSDATA=e20c69d7%2C1675659396%2C09715%2A81; bili_jct=54992fbb96d8876b46cc8abb37df1a57; DedeUserID=35671002; DedeUserID__ckMd5=d69f732e9248e565; buvid_fp=e5690504a7252e22c88daa209cce9049; CURRENT_QUALITY=116; bp_video_offset_35671002=692641245482188900; sid=7p2ab96c; PVID=11',
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
BiliApiHeaders = {
    'authority':'api.bilibili.com',
    'method':'GET',
    'scheme':'https',
    'path':'/pgc/season/episode/web/info?ep_id=374680',
    'cookie':'buvid3=C6FA7D37-BDAB-8A98-F46C-F74DCCD9E1E590619infoc; _uuid=611AEF8F-FA10A-F25E-63B1-7C6851A3E69C92883infoc; buvid4=A0BF7CAD-00E0-291D-0057-8C4CC946B8DF91548-022012618-yPTK2yRnbGG1AbZfVzPX2Q%3D%3D; rpdid=|(kRJkkRmJ~0J\'uYRJumJumJ; fingerprint=163f019b63a8ac7654d7e8634c3127cf; buvid_fp_plain=undefined; buvid_fp=4d18731a5a709bbdb5ce9d474ce68827; SESSDATA=201e1f7f%2C1665046259%2C56fc0%2A41; bili_jct=64787cb69067364c5e44cd1c3dd05938; DedeUserID=35671002; DedeUserID__ckMd5=d69f732e9248e565; sid=86748t3l; CURRENT_BLACKGAP=0; blackside_state=0; i-wanna-go-back=-1; b_ut=5; LIVE_BUVID=AUTO9316494943737456; is-2022-channel=1; nostalgia_conf=-1; hit-dyn-v2=1; go_old_video=-1; CURRENT_FNVAL=4048; CURRENT_QUALITY=120; bsource=search_baidu; bp_video_offset_35671002=691280144785997800; b_lsid=CBD22374_1827669CDBD; PVID=2; b_timer=%7B%22ffp%22%3A%7B%22333.788.fp.risk_C6FA7D37%22%3A%2218272FEB16C%22%2C%22333.1193.fp.risk_C6FA7D37%22%3A%221827676EE21%22%2C%22333.999.fp.risk_C6FA7D37%22%3A%221827676EBCC%22%2C%22888.2421.fp.risk_C6FA7D37%22%3A%221826EA1E547%22%2C%22666.25.fp.risk_C6FA7D37%22%3A%221827674CE10%22%2C%22333.976.fp.risk_C6FA7D37%22%3A%2218272FE2BEE%22%2C%22444.41.fp.risk_C6FA7D37%22%3A%2218272FE6D5D%22%2C%22333.937.fp.risk_C6FA7D37%22%3A%22182731D8041%22%2C%22333.337.fp.risk_C6FA7D37%22%3A%221827676F357%22%7D%7D',
    #'referer':'www.bilibili.com/play/ep374676',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/103.0.0.0Safari/537.36'
}
Bilicookies = {
        "name":"name",
        "value":"bilibili",
        "buvid3":"C6FA7D37-BDAB-8A98-F46C-F74DCCD9E1E590619infoc",
        "_uuid":"611AEF8F-FA10A-F25E-63B1-7C6851A3E69C92883infoc",
        "buvid4":"A0BF7CAD-00E0-291D-0057-8C4CC946B8DF91548-022012618-yPTK2yRnbGG1AbZfVzPX2Q%3D%3D",
        "rpdid":"|(kRJkkRmJ~0J\'uYRJumJumJ",
        "fingerprint":"163f019b63a8ac7654d7e8634c3127cf",
        "buvid_fp_plain":"undefined",
        "buvid_fp":"4d18731a5a709bbdb5ce9d474ce68827",
        "SESSDATA":"201e1f7f%2C1665046259%2C56fc0%2A41",
        "bili_jct":"64787cb69067364c5e44cd1c3dd05938",
        "DedeUserID":"35671002",
        "DedeUserID__ckMd5":"d69f732e9248e565",
        "sid":"86748t3l",
        "CURRENT_BLACKGAP":"0",
        "blackside_state":"0",
        "i-wanna-go-back":"-1",
        "b_ut":"5",
        "LIVE_BUVID":"AUTO9316494943737456",
        "is-2022-channel":"1",
        "nostalgia_conf":"-1",
        "hit-dyn-v2":"1", 
        "go_old_video":"-1",
        "CURRENT_FNVAL":"4048",
        "CURRENT_QUALITY":"120",
        "bsource":"search_baidu",
        "bp_video_offset_35671002":"691280144785997800",
        "b_lsid":"CBD22374_1827669CDBD",
        "PVID":"2", 
        "b_timer":"%7B%22ffp%22%3A%7B%22333.788.fp.risk_C6FA7D37%22%3A%2218272FEB16C%22%2C%22333.1193.fp.risk_C6FA7D37%22%3A%221827676EE21%22%2C%22333.999.fp.risk_C6FA7D37%22%3A%221827676EBCC%22%2C%22888.2421.fp.risk_C6FA7D37%22%3A%221826EA1E547%22%2C%22666.25.fp.risk_C6FA7D37%22%3A%221827674CE10%22%2C%22333.976.fp.risk_C6FA7D37%22%3A%2218272FE2BEE%22%2C%22444.41.fp.risk_C6FA7D37%22%3A%2218272FE6D5D%22%2C%22333.937.fp.risk_C6FA7D37%22%3A%22182731D8041%22%2C%22333.337.fp.risk_C6FA7D37%22%3A%221827676F357%22%7D%7D"}
class BiliUser(object):
    SpaceURL_mode = 'https://space.bilibili.com/{userID}'
    def __init__(self, userID):
        self.userID = userID
        self.SpaceURL = BiliUser.SpaceURL_mode.format(userID = userID)
        
        self.res = requests.get(self.SpaceURL, headers= BiliUniHeaders)
        self.name = re.search('title>(.*?)的个人空间_', self.res.text).group(1)
        pass
    #获取用户头像(搜索'face'定位链接)
    def Profilepic(self, path = 'C:/Users/DELL/Desktop/'):
        soup = BeautifulSoup(self.res.text, 'lxml')
        picURL = soup.find('link', attrs={'rel':'apple-touch-icon'}).attrs['href']
        picURL = 'https:' +picURL
        print(picURL)
        res = requests.get(picURL, headers=BiliDownloadHeaders)
        with open(path + self.name + '_Face.jpg', 'wb') as f:
            f.write(res.content)
    #获取所有视频的bv号序列
    def VideoBVList(self, begin=1, end=1000):
        apiUrl = 'https://api.bilibili.com/x/space/arc/search?mid={userID}&ps=30&tid=0&pn={index}&keyword=&order=pubdate&jsonp=jsonp'
        bvlist = []
        for index in range(begin, end+1):
            res = requests.get(apiUrl.format(userID = self.userID, index = index), headers=BiliApiHeaders)
            dict = json.loads(res.text)
            tempList = dict['data']['list']['vlist']
            if tempList == []:
                break
            for element in tempList:
                bvlist.append(element['bvid'])
            pass
        #print(len(bvlist))
        return bvlist
    #获取所有视频的基本信息序列
    def VideoList(self, begin=1, end=1000):
        apiUrl = 'https://api.bilibili.com/x/space/arc/search?mid={userID}&ps=30&tid=0&pn={index}&keyword=&order=pubdate&jsonp=jsonp'
        vlist = []
        for index in range(begin, end+1):
            res = requests.get(apiUrl.format(userID = self.userID, index = index), headers=BiliApiHeaders)
            dict = json.loads(res.text)
            tempList = dict['data']['list']['vlist']
            if tempList == []:
                break
            for element in tempList:
                vlist.append(element)
            pass
        return vlist
    #获取基本信息
    def TotalInfo(self):
    
        pass
    
#总体BiliBili类, 用于广泛查询
class BiliBili(object):
    origin_url = 'https://www.bilibili.com/'
    #频道字典
    channel = {'番剧': 'https://www.bilibili.com/anime/', '电影': 'https://www.bilibili.com/movie/', '国创': 'https://www.bilibili.com/guochuang/', '电视剧': 'https://www.bilibili.com/tv/', '综艺': 'https://www.bilibili.com/variety/ ', '纪录片': 'https://www.bilibili.com/documentary/', '动画': 'https://www.bilibili.com/v/douga/', '游戏': 'https://www.bilibili.com/v/game/', '鬼畜': 'https://www.bilibili.com/v/kichiku/', '音乐': 'https://www.bilibili.com/v/music', '舞蹈': 'https://www.bilibili.com/v/dance/', '影视': 'https://www.bilibili.com/v/cinephile', '娱乐': 'https://www.bilibili.com/v/ent/', '知识': 'https://www.bilibili.com/v/knowledge/', '科技': 'https://www.bilibili.com/v/tech/', '资讯': 'https://www.bilibili.com/v/information/', '美食': 'https://www.bilibili.com/v/food', '生活': 'https://www.bilibili.com/v/life', '汽车': 'https://www.bilibili.com/v/car', '时尚': 'https://www.bilibili.com/v/fashion', '运动': 'https://www.bilibili.com/v/sports', '动物圈': 'https://www.bilibili.com/v/animal', 'VLOG': 'https://www.bilibili.com/v/life/daily/#/530003', '搞笑': 'https://www.bilibili.com/v/life/funny', '单机游戏': 'https://www.bilibili.com/v/game/stand_alone', '虚拟UP主': 'https://www.bilibili.com/v/virtual', '公益': 'https://love.bilibili.com', '公开课': 'https://www.bilibili.com/mooc'} 
    #类构造方法
    def __init__(self):
        self.res = requests.get(BiliBili.origin_url, headers= BiliUniHeaders)
        self.html = self.res.text
        pass    
    #如果频道有变化则进行更新
    def channel_update(self):
        soup = BeautifulSoup(self.html, 'lxml')
        NodeList = soup.find_all('a', class_ = 'channel-link')
        dict_0 = {}
        for node in NodeList:
            dict_0[node.string] = node.attrs['href']
        print(dict_0)
        BiliBili.channel = dict_0
        pass
    #使用api简易搜索单独的页面
    def search_single(self, keyword = '1', mode = 'comprehensive', page = 1):
        dict_order = {'comprehensive':' ', 'new':'pubdate', 'view':'click', 'danmu':'dm', 'bookmark':'stow'}
        try:
            order = dict_order[mode]
        except:
            order = dict_order['bookmark']
        keyword = keyword.replace(' ', '%20')
        #api页面的显示方式是: 一页20个视频, 若能返回搜索结果, 则最多有1000个. 
        apiURL_mode = 'https://api.bilibili.com/x/web-interface/search/all/v2?__refresh__=true&_extra=&context=&page={page}&order={order}&duration=&platform=pc&highlight=1&single_column=0&keyword={keyword}&preload=true&com2co=true'
        apiURL = apiURL_mode.format(order= order, keyword= keyword, page = page)
        res = requests.get(apiURL, headers= BiliApiHeaders)
        dict_0 = json.loads(res.text)
        numPages = dict_0['data']['numPages']
        for element in dict_0['data']['result']:
            if element['result_type'] == 'video':
                VideoDict = element
                break
            else: VideoDict = {}
        bvList = []
        for video in VideoDict['data']:
            bvList.append(video['bvid'])
        #print(bvList.__len__())
        return bvList    
    #使用api直接获取从第一页到指定页的搜索结果
    #警告: 多次使用该方法容易报412错误, 建议使用selenium等测试软件进行爬虫
    def search_all(self, keyword = '1', mode = 'comprehensive', page_end = 1):
        #获取总页数
        apiURL = 'https://api.bilibili.com/x/web-interface/search/all/v2?__refresh__=true&_extra=&context=&page=1&order=&duration=&platform=pc&highlight=1&single_column=0&keyword={keyword}&preload=true&com2co=true'.format(keyword= keyword)
        res = requests.get(apiURL, headers= BiliApiHeaders)
        numPages = json.loads(res.text)['data']['numPages']
        page_end = page_end if numPages > page_end else numPages
        #搜索并添加
        bvList_all = []
        for page in range(1,page_end+1):
            print('Getting page: %d.'%page)
            temp = self.search_single(keyword= keyword, page= page, mode= mode)
            bvList_all.extend(temp)
        print(len(bvList_all))
        return bvList_all
        pass
    #缓慢搜索
    def search_safe(self, keyword = '1'):
        url_search = 'https://search.bilibili.com/all?'
        '<input class="search-input-el" type="text" placeholder="输入关键字搜索" data-v-07fdfa75="">'
        '<button class="vui_button vui_button--blue vui_button--lg search-button" data-v-07fdfa75="">搜索</button>'
        browser = webdriver.Chrome()
        #browser.add_cookie(Bilicookies)
        browser.get(url_search)
        InputNode = browser.find_element(By.CLASS_NAME, 'search-input-el')
        InputNode.send_keys(keyword)
        #InputNode.submit()
        button = browser.find_element(By.XPATH , '//*[@id="i_cecream"]/div[1]/div[1]/div/div/div/div/button')
        button.click()
        time.sleep(5)
        '//*[@id="i_cecream"]/div[1]/div[1]/div[2]/div/div/div[1]/div'
        #AllVideoNode = browser.find_element(By.XPATH, '//*[@id="i_cecream"]/div[1]/div[1]/div[2]/div/div/div[1]/div')
        '/html/body/div[3]/div[1]/div[1]/div[2]/div/div'
        AllVideoNode = browser.find_element(By.CSS_SELECTOR, 'body')
        text = AllVideoNode
        print(text)
        time.sleep(50)
        browser.close()
        pass
    
    pass


site = BiliBili()




