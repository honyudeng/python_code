#-*-coding:utf8--*--

import time,datetime,logging,os.path,random,send_wx
import sys,urllib,time,json,requests,socket,gzip,re
from lxml import etree


proxy=['http://118.178.124.33:3128',
'http://139.129.166.68:3128',
'http://61.163.39.70:9999',
'http://61.143.228.162']

class logs(object):
    def __init__(self):
      logger = logging.getLogger()
      logger.setLevel(logging.INFO)
      rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
      log_path = os.path.dirname(os.getcwd())+'/'
      #print(log_path)
      log_name = log_path + 'fund.log'
      logfile = log_name
      print (logfile)
      fh = logging.FileHandler(logfile,mode='w')
      fh.setLevel(logging.DEBUG)
      formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
      fh.setFormatter(formatter)
      logger.addHandler(fh)

class Token(object):
    # 获取token
    def __init__(self,corpid,corpsecret):
        #corpid = "wx1dccbd76c1773908"  # 填写自己应用的
        #corpsecret = "6BnPZKIbUVKr4zKLsOIBle412ikmD9Fs6ZT_wpHL_UOzr7CpEZ4V5OLeqx2O9F2l" # 填写自己应用的
        self.baseurl = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={0}&corpsecret={1}'.format(corpid, corpsecret)
        #print self.baseurl
    def get_token(self):
            response = requests.get(self.baseurl)
            ret = response.content.decode()
            ret = json.loads(ret)
            self.access_token = ret['access_token']
            #print self.access_token
            return self.access_token

def randHeader():  
    ''' 
    随机生成User-Agent 
    :return: 
    '''  
    head_connection = ['Keep-Alive', 'close']  
    head_accept = ['text/html, application/xhtml+xml, */*']  
    head_accept_language = ['zh-CN,fr-FR;q=0.5', 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3']  
    head_user_agent = ['Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',  
                       'Opera/9.27 (Windows NT 5.2; U; zh-cn)',  
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',  
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',  
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',  
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',  
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',  
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',  
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',  
                       'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',  
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',  
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',  
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',  
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',  
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',  
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',  
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',  
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11',  
                       'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',  
                       'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0'  
                       ]  
    result = {  
        'Connection': head_connection[0],  
        'Accept': head_accept[0],  
        'Accept-Language': head_accept_language[1],  
        'User-Agent': head_user_agent[random.randrange(0, len(head_user_agent))]  
    }  
    return result 

def getURL(url,tries_num=5, sleep_time=0, time_out=10,max_retry = 5):  
        ''''' 
           这里重写get函数，主要是为了实现网络中断后自动重连，同时为了兼容各种网站不同的反爬策略及，通过sleep时间和timeout动态调整来测试合适的网络连接参数； 
           通过isproxy 来控制是否使用代理，以支持一些在内网办公的同学 
        :param url: 
        :param tries_num:  重试次数 
        :param sleep_time: 休眠时间 
        :param time_out: 连接超时参数 
        :param max_retry: 最大重试次数，仅仅是为了递归使用 
        :return: response 
        '''  
        sleep_time_p = sleep_time  
        time_out_p = time_out  
        tries_num_p = tries_num  
        try:  
            res = requests.Session()
            header = randHeader()  
            if isproxy == 1:  
                res = requests.get(url, headers=header, timeout=time_out, proxies=proxy)  
            else:  
                res = requests.get(url, headers=header, timeout=time_out)  
            res.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常  
        except requests.RequestException as e:  
            sleep_time_p = sleep_time_p + 10  
            time_out_p = time_out_p + 10  
            tries_num_p = tries_num_p - 1  
            # 设置重试次数，最大timeout 时间和 最长休眠时间  
            if tries_num_p > 0:  
                time.sleep(sleep_time_p)  
                print (getCurrentTime(), url, 'URL Connection Error: 第',max_retry - tries_num_p, u'次 Retry Connection', e)  
                return getURL(url, tries_num_p, sleep_time_p, time_out_p,max_retry)  
        return res  

def get_html():
    try:
      city = parse.quote('深圳')
      url = 'http://wthrcdn.etouch.cn/WeatherApi?city=%s'%city
      req=request.Request(url)
      req.add_header("user-agent","Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36")
      response=request.urlopen(req).read()
      html = gzip.decompress(response)
      html = html.decode('utf-8')
      	
      res_tr_x = r'<alarm_details><!\[CDATA\[(.*?)\]\]></alarm_details>'
      res_str = r'<suggest><!\[CDATA\[(.*?)\]\]></suggest>'
      x=re.findall(res_tr_x,html)
      if x != []:
         y=re.findall(res_str,html)
         strs = y[0].split('；')
         zz = ''
         for z in strs:
            zz = zz + z +'\n'
         return x[0],'\n'+zz
      else:
         return None
    except:
         return None


def GetNowTime():
    return time.strftime("%H",time.localtime(time.time()))

fundcodes=["070019",
     "004986",
     "005207"]


hours=3600
i=0
funds={}
old_values={}
name=''
#global
isproxy = 0  # 如需要使用代理，改为1，并设置代理IP参数 proxy
logs()
logging.info('开始作业 ')
y = 0
chan_day=False
#发微信
old_day = time.strftime('%d',time.localtime(time.time()))
msg = send_wx.Token()
qs = msg.get_token()#获取最新token
msg.update_qs(qs)#将最新的token上传到数据库
#content = "标题"+'\n'+"开市值: "+str(1.23)+'\n'+"最新值: "+str(4.43)
#msg.send_msg(u'鸡场信息','4532',content)

def get_fund_value():
     global old_day,chan_day
     if old_day != time.strftime("%d",time.localtime(time.time())):
            chan_day = True
            old_day = time.strftime("%d",time.localtime(time.time()))
     
     for fund_code in fundcodes:
        try:
            fund_url="http://fundgz.1234567.com.cn/js/"+fund_code+".js?rt=1463558676006"
            res = getURL(fund_url)
            res = res.text[8:-2]
            res = json.loads(res)
            #print (res['name'],res['fundcode'],res['jzrq'],"单位净值:",res['dwjz'],"净值估算",res['gsz'],"估算张幅：",res['gszzl'],res['gztime'],)
            if float(res['gszzl']) < 0:
                name = res['name']
                code = res['fundcode']
                value = res['gsz']
                update_time = res['gztime']
                #logging.info('刷新'+name+' '+code+' '+value)
                #print ('降下来了！',name)
                if name in funds:
                   if funds[name]!=value:
                      if name not in old_values or chan_day == True:
                         old_values[name] = funds[name]
                      new_value = value
                      funds[name]=value
                      #print (name,old_value,new_value,'有数据,有变化')
                      content = name+'\n'+"开市值: "+str(old_values[name])+'\n'+"最新值: "+str(new_value)
                      msg.send_msg(u'鸡场最新信息',code,content)
                   else:
                      if chan_day == True:
                         old_values[name] = funds[name]
                         #send_msg('养基专业户',name,code,old_value,new_value)
                         content = name+'\n'+"开市值: "+str(old_values[name])+'\n'+"最新值: "+str(new_value)
                         msg.send_msg(u'鸡场最新信息',code,content)
                else:
                   funds[name] = value
                   new_value = value
                   #print (name,funds[name],'添加数据')
                   if name in old_values:
                      content = name+'\n'+"开市值: "+str(old_values[name])+'\n'+"最新值: "+str(new_value)
                   else:
                      content = name+'\n'+"最新值: "+str(new_value)
                   msg.send_msg(u'鸡场初始化信息',code,content)
            else:
                name = res['name']
                code = res['fundcode']
                value = res['gsz']
                update_time = res['gztime']
                if name in funds:
                   if funds[name]!=value:
                      old_values[name] = funds[name]
                      new_value = value
                      funds[name]=value
                else:
                   funds[name]=value
                   new_value = value
                   content = name+'\n'+"开市值: "+str(old_values[name])+'\n'+"最新值: "+str(new_value)
                   msg.send_msg(u'鸡场最新信息',code,content)
      
            if chan_day == True and name in old_values:
               logging.info(name+' 更新净值  '+str(old_values[name]))
               old_values[name] = funds[name]
               content = name+'\n'+"开市值: "+str(old_values[name])+'\n'+"最新值: "+str(new_value)
               msg.send_msg(u'鸡场最新信息',code,content)
               chan_day = False
        except Exception as e:
              #print (fund_code,'网络错误')
              logging.info('出现错误'+str(e))
     if chan_day == True:
        chan_day=False
  
while True:
  i+=1
  if i==hours*1:#间隔小时数
    i=0
    y += 1
    if y == 4:
    	y = 0
    now_day = time.strftime('%a',time.localtime())
    now_hour = int(GetNowTime())
    if now_hour >=8 and now_hour<=23:
      #print(now_day,now_hour,y)
      if now_day != 'Sat' and now_day != 'Sun':
         get_fund_value()
    else:
        logging.info('不在时间内')
  else:
      time.sleep(1)
      #print "循环时间外",i    

