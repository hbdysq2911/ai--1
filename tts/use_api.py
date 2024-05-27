import requests
import pyaudio
import json

def tts(speakText):
    # 设置参数
    data = {
        "character": "sbx5",
        "emotion": "default",
        "text": speakText,
        "text_language": "auto",
        #"batch_size": ${batch_size},
        #"speed": ${speed},
        "top_k": 6,
        "top_p": 0.8,
        "temperature": 0.8,
        "stream": True,
        "save_temp": False
    }

    # 设置请求的URL
    url = 'http://127.0.0.1:5000/tts'

    # 发送POST请求
    try:
        response = requests.post(url, json=data, stream=True)
        # 检查响应状态码
        if response.status_code != 200:
            print("Failed to request TTS service. Status code:", response.status_code)
            return
    except requests.exceptions.RequestException as e:
        print("Error requesting TTS service:", e)
        return
    # 初始化pyaudio
    p = pyaudio.PyAudio()

    # 打开音频流
    stream = p.open(format=p.get_format_from_width(2),
                    channels=1,
                    rate=32000,
                    output=True)

    # 读取数据块并播放
    for data in response.iter_content(chunk_size=1024):
        stream.write(data)

    # 停止和关闭流
    stream.stop_stream()
    stream.close()

    # 终止pyaudio
    p.terminate()

# 使用示例
if __name__ == "__main__":
    tts("这是一段测试文本，旨在通过多种语言风格和复杂性的内容来全面检验文本到语音系统的性能。接下来，我们会探索各种主题和语言结构，包括文学引用、技术性描述、日常会话以及诗歌等。首先，让我们从一段简单的描述性文本开始：“在一个阳光明媚的下午，一位年轻的旅者站在山顶上，眺望着下方那宽广而繁忙的城市。他的心中充满了对未来的憧憬和对旅途的期待。”这段文本测试了系统对自然景观描写的处理能力和情感表达的细腻程度。")
