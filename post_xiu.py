#_*_coding:utf-8_*_ 
import requests,json,time,logging,os.path,send_wx


class logs(object):
    def __init__(self):
      logger = logging.getLogger()
      logger.setLevel(logging.INFO)
      rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
      log_path = os.path.dirname(os.getcwd())+'/youyu/'
      log_name = log_path + 'post_xiu.log'
      logfile = log_name
      #print logfile,log_path
      fh = logging.FileHandler(logfile,mode='w')
      fh.setLevel(logging.DEBUG)
      formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
      fh.setFormatter(formatter)
      logger.addHandler(fh)

def GetNowTime():
    return time.strftime("%H",time.localtime(time.time()))
    
def renovate(url_code):
	 try:
		  e = s.get('http://job.6xiu.com/member/index.php?c=job&act=opera&up=%s'%str(url_code))
		  logging.info( e.json()['msg']+str(url_code))
	 except Exception as e:
		  logging.info(str(url_code)+' 本次刷新失败 '+str(e))
		  msg.send_msg(u'刷新职位',url_code,u'刷新失败')
url = 'http://job.6xiu.com/m_login-c_loginsave.html'
s = requests.session()
head = {'Accept':'*/*',  
       'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',  
       'X-Requested-With':'XMLHttpRequest',  
       'Referer':'http://job.6xiu.com',  
       'Accept-Language':'zh-CN',  
       'Accept-Encoding':'gzip, deflate',  
       'User-Agent':'Mozilla/5.0(Windows NT 6.1;WOW64;Trident/7.0;rv:11.0)like Gecko',  
       'Host':'job.6xiu.com'}  
       
data = {'loginname':0,
		  'password':'',
		  'username':'',
		}
r = s.post(url,data=data,headers=head)
logs()
list_code=[
'33090',
'33406'
]
global msg,qs
msg = send_wx.Token()
qs = msg.get_token()
msg.update_qs(qs)
if qs != "":
   logging.info("微信模块启动")   
logging.info('开始作业 ')
if r.json()['msg'] == u'登录成功':
	e = s.get('http://job.6xiu.com/member/index.php?c=job&act=opera&up=33090')
	logging.info(e.json()['msg']+'33090')
	time.sleep(10)#10秒
	e = s.get('http://job.6xiu.com/member/index.php?c=job&act=opera&up=33406')
	logging.info(e.json()['msg']+'33406')
	i=0
	y = 0
	while True:
		i += 1
		if y == 4:
			   y = 0
		if i == 1800:
			y += 1	
			#print 早8点到晚8点刷新
			if int(time.strftime('%H',time.localtime(time.time()))) <= 23 and int(time.strftime('%H',time.localtime(time.time()))) > 7:
				for url_code in list_code:
					renovate(url_code)
					time.sleep(10)
			i = 0
		time.sleep(1)
else:
	logging.info("登录失败")
# and time.strftime('%H',time.localtime(time.time())) > 7 
