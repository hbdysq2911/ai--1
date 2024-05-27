from typing import List, Optional

from langchain.llms.base import LLM
from langchain.llms.utils import enforce_stop_tokens
import requests
import json

WENXIN_AK = "xeN4w5pKFB0JeA0IU9iDsk7H"
WENXIN_SK = "AKk9DEa516Uv08LVZv1DmHfeOSaGgMif"


def get_access_token():
    """
    使用 API Key,Secret Key 获取access_token
    """
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={WENXIN_AK}&client_secret={WENXIN_SK}"
    payload = json.dumps("")
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


class YiYan(LLM):
    temperature = 0.1  # 较高的数值会使输出更加随机，而较低的数值会使其更加集中和确定。默认0.95，范围 (0, 1.0]
    top_p = 0.8  # 影响输出文本的多样性，取值越大，生成文本的多样性越强。默认0.8，取值范围 [0, 1.0]
    penalty_score = 1  # 通过对已生成的token增加惩罚，减少重复生成的现象。值越大表示惩罚越大。默认1.0，取值范围：[1.0, 2.0]

    def __init__(self):
        super().__init__()
        
    @property
    def _llm_type(self) -> str:
        return "YiYan"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + get_access_token()
        data = {
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "top_p": self.top_p,
            "penalty_score": self.penalty_score,
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()['result']
        return "查询结果错误"