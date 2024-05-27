import requests
import json


def get_token(WENXIN_AK,WENXIN_SK):
        url = f"https://aip.baidubce.com/oauth/2.0/token?client_id={WENXIN_AK}&client_secret={WENXIN_SK}&grant_type=client_credentials"
    
        payload = json.dumps("")
        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
            }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json().get("access_token")

class ChatBaidu:
    def __init__(self, token):
        self.url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions"
        self.token = token

        
    def request(self, post_word, callback):
        post_url = self.url + "?access_token=" + self.token
        post_data = {
            "messages": [{"role": "user","content": post_word}],
            "stream": True,
            "user_id": ""
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(post_url, data=json.dumps(post_data), headers=headers,stream=True)
        
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith('data:'):
                        json_data = json.loads(decoded_line.split('data: ')[1])
                        result = json_data.get('result')
                        callback(result)
        else:
            print(f"Error: {response.status_code}")
        return response

# 使用示例
if __name__ == '__main__':
    WENXIN_AK = "xeN4w5pKFB0JeA0IU9iDsk7H"
    WENXIN_SK = "AKk9DEa516Uv08LVZv1DmHfeOSaGgMif"
    def callback(response):
        if response:
            print(response) 
    chat_baidu = ChatBaidu(get_token(WENXIN_AK,WENXIN_SK))
    while True:
        _msg=input("请输入：")
        chat_baidu.request(_msg, callback)
        



