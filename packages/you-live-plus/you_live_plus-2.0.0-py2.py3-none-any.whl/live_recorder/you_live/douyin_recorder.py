# coding=utf-8
import requests, re, json
from ._base_recorder import BaseRecorder, recorder

@recorder(liver = 'douyin')
class DouYinRecorder(BaseRecorder):
    
    def __init__(self, short_id, **args):
        BaseRecorder.__init__(self, short_id, **args)
    
    def getLiveInfo(self):
        url = "https://live.douyin.com/webcast/room/web/enter/?aid=6383&live_id=1&device_platform=web&language=zh-CN&enter_from=web_live&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=94.0.4606.81&room_id_str=&enter_source=&web_rid=" + self.short_id

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
        }
        self.headers = headers
        if not self.cookies is None:
            headers['Cookie'] = self.cookies
            
        r = requests.get(url, timeout=10, headers=headers)
        # print(r.text)
        rjson = json.loads(r.text)
        status_code = rjson['status_code']
        if status_code == 0:
            return json.loads(r.text)
        else:
            return None

    def getRoomInfo(self):
        roomInfo = {}
        roomInfo['short_id'] = self.short_id
        roomInfo['room_id'] = self.short_id
        
        r_json = self.getLiveInfo()
        if r_json is None:
            return None
        data = r_json['data']
        user = data['user']
        room = data['data'][0]
        stream_url = room['stream_url']
        roomInfo['stream_url'] = None
        roomInfo['room_owner_id'] = int(user['id_str'])
        roomInfo['room_owner_name'] = user['nickname']
        roomInfo['room_description'] = roomInfo['room_owner_name'] + '的直播间'
        roomInfo['room_title'] = room['title']
        if stream_url == None:
            roomInfo['live_status'] = '0'
        else:
            roomInfo['live_status'] = '1'
            roomInfo['stream_url'] = stream_url['flv_pull_url']
            roomInfo['live_rates'] = {}
            flv_sources = stream_url['live_core_sdk_data']['pull_data']['options']['qualities']
            for index in range(0,len(flv_sources)):
                level = int(flv_sources[index]['level'])
                roomInfo['live_rates'][index] = flv_sources[index]['name']

        self.roomInfo = roomInfo    
        # print(self.roomInfo)
        return roomInfo
        
    def getLiveUrl(self, qn):
        qn = int(qn)
        if not hasattr(self, 'roomInfo'):
            self.getRoomInfo()
        if self.roomInfo['live_status'] != '1':
            print('当前没有在直播')
            return None
        
        live_data_json = self.roomInfo
        self.live_url = live_data_json["stream_url"]['FULL_HD1']
        self.live_qn = qn
        print("申请清晰度 %s的链接，得到清晰度 %d的链接"%(qn, self.live_qn))
        return self.live_url