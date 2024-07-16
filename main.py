import os
import tts.use_api
import llm.chatbaidu as baidutts
import llm.memory as memory

#api调用的key
WENXIN_AK = "xeN4w5pKFB0JeA0IU9iDsk7H"
WENXIN_SK = "AKk9DEa516Uv08LVZv1DmHfeOSaGgMif"


# 记录切换前的工作目录
#previous_dir = os.getcwd()
# 将当前工作目录切换到.bat文件所在的目录
#bat_dir = r'gpt-sovits\0 一键启动脚本'
#os.chdir(bat_dir)
# 启动语音合成api
#try:
    # 使用os.startfile打开.bat文件
#    os.startfile(r'5 启动后端程序.bat')
#except Exception as e:
#    print("Error running .bat file:", e)
# 切换回之前的工作目录
#os.chdir(previous_dir)

#建立聊天 
def callback(response):
        print("Response:", response)
chat_baidu = baidutts.ChatBaidu(baidutts.get_token(WENXIN_AK,WENXIN_SK))


#聊天，启动
while True:
    #初始化人设
    initialization="请你扮演名叫游戏恋爱绮谭不存在的夏天中的女主角苏半夏与我对话，请你尽量根据苏半夏的性格，使用口语化的形式和我对话。回答语言：中文。"
    history = [f"初始化信息：{initialization}"]
    #读取已有的对话记录
    if os.path.exists("llm\memory\conversation.txt"):
        with open("llm\memory\conversation.txt", "r") as file:
            #读取最近的10轮对话记录
            lines = file.readlines()
            start_index = max(0, len(lines) - 10)
            for line in lines[start_index:]:
                # 使用eval()将字符串转换为字典对象
                history.append(line.strip())
    #print(history)

    #输入信息
    tmp_msg=input("少女聆听中：")
    #保存输入信息
    with open("llm\memory\conversation.txt", "a") as file:
        file.write(f"user:{tmp_msg}" + "\n")
    with open("llm\memory\_new_document.txt", "a") as file:
        file.write(f"user:{tmp_msg}" + "\n")
    #查找历史记录
    historymsg=memory.vector_search(tmp_msg)
    history.append(f"以下是我和你的历史对话记录：{historymsg}")
    history.append("以下是我的问题:"+tmp_msg)

    #print("历史记录：",history)

    res=chat_baidu.request("".join(history), callback)
    if res.status_code == 200:
        response_data = res.json()
        result = response_data.get("result", "")
        history.append(f"ai苏半夏:{result}")
        #保存输出信息
        with open("llm\memory\conversation.txt", "a") as file:
                file.write(f"ai苏半夏:{result}" + "\n")
        with open("llm\memory\_new_document.txt", "a") as file:
                file.write(f"ai苏半夏:{result}" + "\n")
        #启动语言合成
        tts.use_api.tts(result)
        #记忆写入
        with open("llm\memory\_new_document.txt", "r") as file:
            lines = file.readlines()
            if len(lines) >= 10:
                memory.save_to_memory("llm\memory\_new_document.txt")
                open("llm\memory\_new_document.txt", "w").close()
             
    else:
        print("Error:", res.status_code)
