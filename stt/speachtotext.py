import speech_recognition as sr

def recognize_speech():
    # 创建一个语音识别器对象
    recognizer = sr.Recognizer()

    # 使用麦克风录音
    with sr.Microphone() as source:
        print("请说话...")
        # 设置环境噪音阈值
        recognizer.adjust_for_ambient_noise(source)
        # 监听麦克风输入，直到停止说话
        audio = recognizer.listen(source)

    try:
        print("识别中...")
        # 调用语音识别引擎进行识别
        text = recognizer.recognize_google(audio, language='zh-CN')
        return text
    except sr.UnknownValueError:
        print("无法识别，请重试...")
    except sr.RequestError as e:
        print(f"请求错误: {e}")

# 使用示例
if __name__ == "__main__":
    while True:
        user_input = input("按下Enter键开始录音，按下q键退出：")
        if user_input.lower() == "q":
            print("退出程序。")
            break
        else:
            text = recognize_speech()
            if text:
                print("识别结果:", text)
