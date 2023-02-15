import requests
import json
import re
import argparse

class Headers:
    """Class for headers."""
    def __init__(self):
        """Construct of makidiary class."""
        self.data = {
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate, br", 
                "Accept-Language": "en,en-US;q=0.7,zh-CN;q=0.3",
                "Connection": "keep-alive",
                "Content-Type": "application/json",
                "Host": "api.maki-math.com",
                "Origin": "http://www.maki-math.com",
                "Referer": "http://www.maki-math.com/",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "cross-site",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0", 
                # "Content-Length": "58", # no use
                }
        
    def __setitem__(self, key, value):
        """Add data to headers"""
        self.data[key] = value


class Makidiary:
    """Class to easily diary in maki-lab website."""
    api = 'https://api.maki-math.com'
    def __init__(self, username, passwd):
        """Construct of makidiary class."""
        self.login_api = self.api + '/auth/login/'
        self.diary_api = self.api + '/diary/'
        self.user_profile_api = self.api + "/user_profile/current/"
        self.username = username
        self.passwd = passwd
        self.token = None
        self.id = None

    def get_token(self):
        """Get token by username and password"""
        headers = Headers()
        data = {
                "password": self.passwd, 
                "remember": True,
                "username": self.username
                }
        response = requests.post(self.login_api, data=json.dumps(data), headers=headers.data)
        self.token = self._extract_key(response, 'key')

    def get_user_id(self):
        """Get user id."""
        headers = Headers()
        headers['Authorization'] = 'Token '+self.token
        response = requests.get(self.user_profile_api, headers=headers.data)
        self.id = self._extract_key(response, "id")

    def _extract_key(self, response, key):
        """Decode json, extract corresponding key."""
        return json.loads(response.text)[key]
    
    def diary(self):
        """Update today's diary."""
        headers = Headers()
        headers['Authorization'] = 'Token '+self.token
        if self.id is not None:
            data = {
                    "author":{
                        "id": self.id
                        },
                    "items":[
                        {"action":"白","objectName":"日","objectType":"依","quant":"山","unit":"尽"},
                        {"action":"黄","objectName":"河","objectType":"入","quant":"海","unit":"流"},
                        {"action":"欲","objectName":"穷","objectType":"千","quant":"里","unit":"目"},
                        {"action":"更","objectName":"上","objectType":"一","quant":"层","unit":"楼"},
                        ]
                    }
        else:
            raise TypeError("Please get id first!")
        response = requests.post(self.diary_api, data=json.dumps(data), headers=headers.data)
        print(response.text)

class Diarydata:
    """The class to record diary data."""
    def __init__(self):
        """Construct for Diarydata class."""
        pass


if __name__ == '__main__':
    hapo = Makidiary('hapo', 'xxxxxxxx')
    hapo.get_token()
    print(hapo.token)
    hapo.get_user_id()
    print(hapo.id)
    # print(hapo.diary_api)
    hapo.diary()
        
