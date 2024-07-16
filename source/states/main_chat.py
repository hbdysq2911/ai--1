import pygame
import threading
from .. import setup
from .. import tools
from .. import constants as C
from .. components import info
import os
import llm.memory as memory
import tts.use_api
import llm.chatbaidu as baidutts

WENXIN_AK = "xeN4w5pKFB0JeA0IU9iDsk7H"
WENXIN_SK = "AKk9DEa516Uv08LVZv1DmHfeOSaGgMif"
chat_baidu = baidutts.ChatBaidu(baidutts.get_token(WENXIN_AK,WENXIN_SK))
def callback(response):
    print("Response:", response)

class Mainchat:

    def __init__(self):
        game_state = True #输入模式
        self.backspace_timer = 0  # 退格键计时器
        self.backspace_delay = 500  # 退格键连续删除的延迟（毫秒）
        self.start(game_state)

    def start(self,game_state):
        
        self.state = game_state
        self.setup_background()
        self.setup_assistant()
        self.setup_chat()
        self.setup_input()
        self.info = info.Info(self.state)
        
    def chat_baidu(self,input_mag):
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
        tmp_msg=input_mag
        with open("llm\memory\conversation.txt", "a") as file:
            file.write(f"user:{tmp_msg}" + "\n")
        with open("llm\memory\_new_document.txt", "a") as file:
            file.write(f"user:{tmp_msg}" + "\n")
        #查找历史记录
        historymsg=memory.vector_search(tmp_msg)
        history.append(f"以下是我和你的历史对话记录：{historymsg}")
        history.append("以下是我的问题:"+tmp_msg)
        print(history)
        res=chat_baidu.request("".join(history), callback)
        self.output_text = res.json().get("result", "")
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


    def setup_background(self):
        self.background = setup.GRAPHICS['Nekoday']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background,(int(self.background_rect.width*C.BG_MULTI)
                                                                   ,int(self.background_rect.height*C.BG_MULTI)))
        
    def setup_assistant(self):
        self.assistant = tools.get_image(setup.GRAPHICS['SBX1-01'],0,310,2757,2757,(0,0,0),C.AS_MULTI)
        
    def setup_chat(self):
        self.chat1 = tools.get_image(setup.GRAPHICS['DialogBox_text'],0,0,1920,294,(0,0,0),1)
        self.chat1.set_alpha(200)
        self.chat2 = tools.get_image(setup.GRAPHICS['DialogBox_name'],0,0,343,72,(0,0,0),1)

    def setup_input(self):
        self.input_box = pygame.Rect(150,540,1000,190)
        self.input_text = ''
        self.output_text = ''
        self.input_font = pygame.font.SysFont(C.FONT,30)
        self.input_color_active = pygame.Color('lightskyblue3')
        self.input_color_inactive = pygame.Color('gray15')
        self.input_color = self.input_color_inactive
        self.input_active = False  # 默认输入框未激活
    
    def handle_event(self, events, mouse_pos):
        if self.state:
            pygame.key.set_text_input_rect((0,0,0,0))
            for event in events:
                if event.type == pygame.QUIT:
                        pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_box.collidepoint(mouse_pos):  # 如果鼠标在输入框上
                        self.input_active = True  # 输入框激活
                    else:  #如果鼠标不在输入框上
                        self.input_active = False  # 输入框不激活
                elif event.type == pygame.KEYDOWN:  # 如果按下键盘按键
                    if self.input_active:  # 如果输入框激活
                        if event.key == pygame.K_RETURN:  # 如果按下的是回车键
                            print(self.input_text)  # 打印输入框中的文本
                            th_chat=threading.Thread(target=self.chat_baidu,args=(self.input_text,))
                            th_chat.start()
                            self.input_text = ''  # 清空输入框中的文本
                            self.state = False  # 助手显示文字
                            self.info = info.Info(self.state)
                        elif event.key == pygame.K_BACKSPACE:  # 如果按下的是退格键
                            self.input_text = self.input_text[:-1]  # 删除输入框中的最后一个字符
                            self.backspace_timer = pygame.time.get_ticks()  # 记录按下退格键的时间
                        else:
                            self.input_text += event.unicode  # 将按键对应的字符添加到输入框中
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_BACKSPACE:
                        self.backspace_timer = 0  # 释放退格键时重置计时器
                if event.type == pygame.TEXTINPUT:
                    self.input_text += event.text  # 处理IME输入法输入的字符
            # 检查退格键是否被持续按住
            if self.input_active and self.backspace_timer and pygame.time.get_ticks() - self.backspace_timer > self.backspace_delay:
                self.input_text = self.input_text[:-1]
        else:
            for event in events:
                if event.type == pygame.QUIT:
                        pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_box.collidepoint(mouse_pos):  # 如果鼠标在输入框上
                        self.state = True  # 输入激活
                        self.output_text = ''  # 清空输出框中的文本
                        self.info = info.Info(self.state)

    def input_show(self):
        self.input_to_shows=[]
        for i in range(0,len(self.input_text),33):
            chunk=self.input_text[i:i+33]
            if len(self.input_to_shows) >= 5:
                self.input_to_shows.pop(0)  # 移除列表中的第一个元素
            self.input_to_shows.append(chunk)  # 添加新元素

    def output_show(self):
        self.output_to_shows=[]
        for i in range(0,len(self.output_text),33):
            chunk=self.output_text[i:i+33]
            self.output_to_shows.append(chunk)  # 添加新元素
        

    def update(self, surface,events,mouse_pos):
        surface.blit(self.background, (0,0))
        surface.blit(self.assistant, (294,0))
        surface.blit(self.chat1, (0,480))
        surface.blit(self.chat2, (180,480))

        self.handle_event(events, mouse_pos)
        if self.input_active:  # 如果输入框激活，使用激活状态的颜色
            self.input_color = self.input_color_active
        else:  # 如果输入框未激活，使用非激活状态的颜色
            self.input_color = self.input_color_inactive

        pygame.draw.rect(surface, self.input_color, self.input_box, 2)# 绘制输入输出框
        if self.state:  # 如果处于输入状态，绘制输入框中的文本
            self.input_show()
            for i in range(len(self.input_to_shows)):
                text_surface = self.input_font.render(self.input_to_shows[i], True, (0, 0, 0))# 绘制输入框中的文本
                surface.blit(text_surface, (self.input_box.x + 5, self.input_box.y + 5+30*i))
        else:  # 如果处于输出状态，绘制输出框中的文本
            self.output_show()
            for i in range(len(self.output_to_shows)):
                text_surface = self.input_font.render(self.output_to_shows[i], True, (0, 0, 0))# 绘制输出框中的文本
                surface.blit(text_surface, (self.input_box.x + 5, self.input_box.y + 5+30*i))
        self.info.update()
        self.info.draw(surface)


        



