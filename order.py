'''
 *@author: wr
 *@GitHub:https://github.com/wr0x00/Lsploit
 *@date: 2022.9.9
 *@description: 命令处理
'''

import requests as rq
from libs import strings
import libs.sniff
#设置语言
if  not __name__ == '__main__':
	try:
		import json
		# 读入示例json数据
		j=open("libs/configs.json",encoding='utf-8')
		demo_json = json.loads(j.read())

		if demo_json["language"]=='cn'or demo_json["language"]=='CN': #中文
			from libs.strings import String_CN as Str
		
		if demo_json["language"]=='en'or demo_json["language"]=='EN': #英文
			from libs.strings import String_EN as Str

	except Exception as e:
		from libs.strings import String_EN as Str
		print("langrage_ERROR:"+format(e))

def cve_info():   
    '''显示最新漏洞播报'''

    from bs4 import BeautifulSoup as b
    from prettytable import PrettyTable
    import json

    x = PrettyTable(["最新漏洞", "时间", "详情"])#绘制表格
    x.align["最新漏洞"] = "1" 
    x.padding_width = 1  # 填充宽度
    try:
        url="https://lyy289065406.github.io/threat-broadcast/"
        header = {'User-Agent': 'Mozilla/5.0 (Mac NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'}
        r=rq.get(url,headers=header,timeout=2)
    except requests.exceptions.ReadTimeout:
        print(Str.ERROR_CONNECT)
    soup=b(r.text,'html.parser')
    items=soup.find_all('tr')

    j=open("libs/configs.json",encoding='utf-8')
    demo_json = json.loads(j.read())
    max=int(demo_json["news"])+1

    for i in items[1:max]:
        tds=i.find_all('td')
        cve_info=tds[3].text
        time=tds[2].text
        for MORE_url in i.find_all('a'):
            x.add_row([cve_info,time,MORE_url.get('href')])

    print(x)
    print("\t\t\t\t----数据来源:https://lyy289065406.github.io/threat-broadcast")
    print("(使用setnows设置播报漏洞条数,例如“setnows 2”)\t\t\tCURL+c 退出")


def order_deal_Setting(order:str):
    import json
    s=order.split()

    with open("libs/configs.json", "r",encoding='utf-8') as jsonFile:
        demo_json = json.load(jsonFile)

    if s[0]=='setnews':     #设置播报显示多少数
        demo_json["news"]=s[1]
        print(Str.SUCCESS_SET)
    
    if s[0]=='setproxy':     #设置代理
        demo_json["proxy"]=s[1]
        print(Str.SUCCESS_SET)
        
    if s[0]=='setlang':       #设置语言
        demo_json["language"] =s[1]
        print(Str.SUCCESS_SET)

    with open("libs/configs.json", "w") as jsonFile:
        json.dump(demo_json, jsonFile,ensure_ascii=False)
    
    
    jsonFile.close()

def order_deal_Common(order:str,agent=None):
    import libs
    s=order.split()

    if s[0]=='help':
        print(Str.HELP)

    elif s[0]=='sw':          #扫描网址目录（线程默认60)
        import httpx
        try:
            if s[2] and not s[3]:
                libs.sniff.httpx_dirscan(format(s[1]), "libs/dict.txt", int(s[2]))
            if s[3] and s[2]:
                libs.sniff.httpx_dirscan(format(s[1]), s[3], int(s[2]))
        except IndexError:
            try:
                libs.sniff.httpx_dirscan(format(s[1]), "libs/dict.txt",60)
            except httpx.ConnectTimeout:
                print(Str.ERROR_CONNECT)
        except httpx.ConnectTimeout:
            print(Str.ERROR_CONNECT)
        finally:
            print(Str.ERROR_ORDER)

    elif s[0]=='sp': 
        try:
            import os,libs.sniff         #扫描端口

            if "/" in s[1]:         #批量扫描
                target=s[1].split(".")
                max=target[3].split('/')
                online=[]
                print(Str.LOADING)

                for i in range(int(max[0]),int(max[1])+1):
                    cmd=os.popen('ping  %s' % (target[0]+'.'+target[1]+'.'+target[2]+'.'+str(i))).read()

                    if "ttl" in cmd or "TTL" in cmd:
                        #print(os.popen('ping  %s' % (target[0]+'.'+target[1]+'.'+target[2]+'.'+str(i))).read())
                        online.append(i)
                        continue

                    else:              
                        continue

                for i in online:
                    print("[online][+]"+target[0]+'.'+target[1]+'.'+target[2]+'.'+str(i))

                for i in online:
                    print("\033[94m[+]"+target[0]+'.'+target[1]+'.'+target[2]+'.'+str(i)+"\033[1;37;40m")
                    libs.sniff.ScanPort(target[0]+'.'+target[1]+'.'+target[2]+'.'+str(i),int(s[2]))

            else:    
                libs.sniff.ScanPort(format(s[1]),int(s[2]))  

        except IndexError:       
            import os,libs.sniff         #扫描端口

            if "/" in s[1]:         #批量扫描
                target=s[1].split(".")
                max=target[3].split('/')
                online=[]
                print(Str.LOADING)
                for i in range(int(max[0]),int(max[1])+1):

                    if "ms" in os.popen('ping  %s' % (target[0]+'.'+target[1]+'.'+target[2]+'.'+str(i))).read():
                        #print(os.popen('ping  %s' % (target[0]+'.'+target[1]+'.'+target[2]+'.'+str(i))).read())
                        online.append(i)
                        continue

                    else:              
                        continue

                for i in online:
                    print("[online][+]"+target[0]+'.'+target[1]+'.'+target[2]+'.'+str(i))

                for i in online:
                    print("\033[94m[+]"+target[0]+'.'+target[1]+'.'+target[2]+'.'+str(i)+"\033[1;37;40m")
                    libs.sniff.ScanPort(target[0]+'.'+target[1]+'.'+target[2]+'.'+str(i))

            else:    
                libs.sniff.asyncio_ScanPort(format(s[1]))   

    elif s[0]=='sd':
        import libs.subdomain
        try:
            if s[2]:
                libs.subdomain.subdomain(format(s[1]),s[2])  
        except IndexError:
            libs.subdomain.subdomain(format(s[1]),"libs/subdomain.txt")          #扫描子域名(字典默认modules\subdomain.txt)
    
    elif s[0]=='whois':       #whois查询 
        libs.sniff.whois_sniff(format(s[1]))

    elif s[0]=='shod':         #shodan
        libs.sniff.shodan_search(format(s[1]))

    elif s[0]=='c':
        import libs.cms as cms
        cms.set_agent(agent)
        cms.cms(format(s[1]))

    elif s[0]=='poc':  
        try:
            import os
            os.system("python libs/ws.py -po " + format(s[2]) + " -t " +s[1])
        except IndexError:
            import os
            os.system("python libs/ws.py" + " -t " + s[1])
    
    elif s[0]=='ssh': 
        import libs.ssh as r
        if s[4]:
            r.force_ssh(s[1], s[4], s[2], int(s[3]))
        else:
            r.force_ssh(s[1], 'libs/pwddic/password/_top19576.txt', s[2], int(s[3]))
    
    elif s[0]=='webshell': 
        import libs.webshell as w
        w.set_agent(agent)
        w.exp(s[1], s[2])  

    elif s[0]=='dos': 
        import libs.dosattack as y
        try:
            y.exp(s[1], s[2], int(s[3]))
        except IndexError:
            y.exp(s[1], s[2],40)

    elif s[0]=='exp': 
        try:
            exp = s[1].replace("-", "_")
            exp = exp.replace("cve", "C")
            exec("import libs.exp." + exp + "_EXP as t\n")
            exec(f"t.set_agent(agent)\n")

            if s[2]:
                exec(f"t.exp('{s[2]}',{s[3]})")
        except IndexError:
            print(Str.ERROR_ORDER)
    else:
        print(Str.ERROR_ORDER)
