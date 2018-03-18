#-*-coding:utf8--*--

import time,datetime,logging,os.path,random,pymysql
import sys,urllib,time,json,requests,socket,gzip,re
from lxml import etree


conn = pymysql.connect(host='',port=3306,user='',passwd='',db='')
conn.autocommit(1)
qs_cousor = conn.cursor()

class Token(object):
    # 获取token
    #def __init__(self,corpid,corpsecret):
    def __init__(self):
        corpid = ""  # 填写自己应用的
        corpsecret = "" # 填写自己应用的
        self.baseurl = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={0}&corpsecret={1}'.format(corpid, corpsecret)

    def get_token(self):
            response = requests.get(self.baseurl)
            ret = response.content.decode()
            ret = json.loads(ret)
            self.access_token = ret['access_token']
            #print (self.access_token)
            return self.access_token
    def send_msg(self,title,name,contert):
        # 发送消息
        ISOTIMEFORMAT='%Y-%m-%d %X' 
        now_time = time.strftime(ISOTIMEFORMAT,time.localtime(time.time()))
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={0}".format(self.access_token)
        payload = {
            "touser": "jree",
            "msgtype": "text",
            "agentid": "1",
            "text": {
                   "content": "{0}\n报告! {1}\n时间: {2}\n品种: {3}\n内容: {4}".format(title,'监控信息！',now_time,name,contert)
            },
            "safe": "0"
        }
        print(payload)
        data=json.dumps(payload, ensure_ascii=False)
        data= bytes(data,encoding='utf-8')
        ret = requests.post(url,data)
        if ret.json()['errmsg'] != "ok":
           qs=self.get_token()
           update_qs(qs)
           url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={0}".format(qs_token)
           payload = {
            "touser": "jree",
            "msgtype": "text",
            "agentid": "1",
            "text": {
                   "content": "{0}\n报告! {1}\n时间: {2}\n品种: {3}\n内容: {4}".format(title,'监控信息！',now_time,name,contert)
               },
            "safe": "0"
           }
           print(payload)
           data=json.dumps(payload, ensure_ascii=False)
           data= bytes(data,encoding='utf-8')
           ret = requests.post(url,data)
           
        
    def update_qs(self,qs):
        sql_update = "UPDATE qs SET qs_token = '"+qs+"' WHERE id = 1"
        #print(sql_update)
        qs_cousor.execute(sql_update)
        conn.commit()
    
    def insert_qs(self,qs):
        sql_insert = "insert into qs (qs_token) values ('"+qs+"')"
        qs_cousor.execute(sql_insert)
        conn.commit()

    def select_qs(self):
        sql_select = "select qs_token from qs where id=1"
        qs_cousor.execute(sql_select)
        qs_cousor.rowcount
        get_row = qs_cousor.fetchone()  
        return get_row
