import requests
import json
import os
import sys
import time
import config
import login

cookies = {}
configs = config.load_config('config')
courses = config.load_config('courses')

def get_cookies():
    all_cookies = login.login()
    for i in all_cookies:
        cookies.update({i['name']: i['value']})

def send_package(course_id):
    url = configs['up_course_url'] + configs['username']
    heads = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.42',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate'
            }
    pay_load = {'jxb_ids':courses[course_id]['jxb_ids'],
                'kch_id':course_id,
                'rwlx': 1,
                'rlzlkz':0,
                'sxbj':0,
                'qz':'0',
                'xxkbj':0,
                'xbj':0,
                'xkkz_id':courses[course_id]['xkkz_id'],
                'zyh_id': 3318,
                'njdm_id':2021,
                'xklc': 1,
                'xkxnm':'2022',
                'xkxqm':'12',
                }
    pay_load = courses[course_id]
    pay_load = '''jxb_ids=2b196b9dd58c5b34e2e931c35678268bef79579a07dad2edf91b3147c72cb00222b4c27e711ee2a2fdc5fa16b57a6d4110f4ebdabe8cbf52f1c825049151427ce363689b8c0c4246dbbaba768cf748ae1d7ef872b2d70438263cd808267119cf4a9f33a4ac1cc02505c0bf708746ebbe7390a394206a69d249a832216397a35a&kch_id=03608&kcmc=(03608)%E7%BE%BD%E6%AF%9B%E7%90%83(%E5%88%9D%E7%BA%A7)+-+1.0+%E5%AD%A6%E5%88%86&rwlx=2&rlkz=0&rlzlkz=0&sxbj=0&xxkbj=0&qz=0&cxbj=0&xkkz_id=EEFF96706E5379DDE0530100007F2C3D&njdm_id=2021&zyh_id=3318&kklxdm=05&xklc=1&xkxnm=2022&xkxqm=12'''
    print(pay_load)
    input()
    p = requests
    answ = p.post(url=url,data=pay_load,headers=heads,cookies=cookies)
    print(answ.text)
    if json.loads(answ.text)['flag'] == '1':
        print('抢课成功')
    return 0
    

if __name__ == '__main__':
    cookies = {'JSESSIONID':'CA7305261A1A9900A41940D9A4F73731',
	            'route':'b6c4112deca225961740e038b0b4c078'}
    send_package('03608')