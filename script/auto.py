import pyautogui
import time
import pyperclip

def exportSrt(name):
    time.sleep(1)
    currentMouseX, currentMouseY = pyautogui.position() # 鼠标当前位置
    print(currentMouseX, currentMouseY)
    # pyautogui.click(x=1687, y=60, duration=0.5) # 先移动到(100, 200)再单击
    # time.sleep(2)
    # currentMouseX, currentMouseY = pyautogui.position() # 鼠标当前位置
    # print(currentMouseX, currentMouseY)
    # pyautogui.click(x=1065, y=346, duration=0.5) # 先移动到(100, 200)再单击
    # pyautogui.hotkey('command', 'a')
    # pyautogui.typewrite('Hello world')
    # 点击导出
    # pyautogui.click(x=1136, y=847, duration=0.5) # 先移动到(100, 200)再单击
    # 关闭导出框
    # pyautogui.click(x=1129, y=565, duration=0.5) # 先移动到(100, 200)再单击

    # time.sleep(100)
    # 点击+
    # pyauto gui.moveTo(228, 262, duration=0.5) # 移动到 (100,100)
    pyautogui.click(x=224, y=262, duration=0.5) # 先移动到(100, 200)再单击

    # pyautogui.moveTo(109, 702, duration=0.5) # 移动到 (100,100)

    #选中音乐，识别歌词
    # pyautogui.click(x=moveToX, y=moveToY, clicks=num_of_clicks, interval=secs_between_clicks, button='left')
    # 其中，button属性可以设置成left，middle和right。
    pyautogui.click(500, 957, 1, 0.5, button='right')

    pyautogui.click(x=544, y=1061, duration=0.5) # 先移动到(100, 200)再单击

    time.sleep(18)

    # time.sleep(2)
    currentMouseX, currentMouseY = pyautogui.position() # 鼠标当前位置
    print(currentMouseX, currentMouseY)
    #保存结果

    pyautogui.click(x=1687, y=60, duration=0.5) # 先移动到(100, 200)再单击
    # time.sleep(1)
    currentMouseX, currentMouseY = pyautogui.position() # 鼠标当前位置
    print(currentMouseX, currentMouseY)
    pyautogui.click(x=1065, y=346, duration=0.5) # 先移动到(100, 200)再单击
    pyperclip.copy(name)
    pyautogui.hotkey('command', 'a')
    # pyautogui.typewrite(name)
    pyautogui.hotkey('command', 'v')
    # 点击导出
    pyautogui.click(x=1136, y=847, duration=0.5) # 先移动到(100, 200)再单击
    # 关闭导出框
    pyautogui.click(x=1129, y=565, duration=0.5) # 先移动到(100, 200)再单击
    pyautogui.click(x=1133, y=507, duration=0.5) # 先移动到(100, 200)再单击

    p = "/Users/lism/Movies/"+name + ".srt"
    ok = check_ok(p)
    if ok:
        print(p, '完成!!!')
    else:
        print(p, '失败')
        #取消识别
        pyautogui.click(865, 635, 1, 1, button='left')

        #删除第一首素材
        pyautogui.click(177, 239, 1, 0.5, button='right')
        pyautogui.click(x=206, y=255, duration=0.5) # 先移动到(100, 200)再单击
        #确定
        pyautogui.click(x=900, y=664, duration=0.5) # 先移动到(100, 200)再单击

        shutil.move(path + file_name, banzou_path)
        return
    #移动到音乐编辑区按下ctrl+a，点击删除
    pyautogui.moveTo(109, 702, duration=0.5) # 移动到 (100,100)
    pyautogui.hotkey('command', 'a')
    time.sleep(0.5)
    pyautogui.click(x=203, y=669, duration=0.5) # 先移动到(100, 200)再单击


    #删除第一首素材
    pyautogui.click(177, 239, 1, 0.5, button='right')
    pyautogui.click(x=206, y=255, duration=0.5) # 先移动到(100, 200)再单击
    #确定
    pyautogui.click(x=900, y=664, duration=0.5) # 先移动到(100, 200)再单击
import os
import shutil


def check_ok(path):
    if '伴奏' in path or '钢琴' in path:
        return True
    return os.path.exists(path)
if __name__ == '__main__':
    path = '/Users/lism/Program/WebStormProjects/slidev-praise/public/assets/media/'
    banzou_path = '/Users/lism/Program/WebStormProjects/slidev-praise/public/assets/ban/'
    g = os.walk(path)
    r = []  # 解决文件顺序混乱时用的列表

    for path,dir_list,file_list in g:
        for file_name in file_list:
            if file_name.endswith(".mp3") or file_name.endswith(".mkv"):
                # print(file_name)
                # f1 = re.findall(r"\d+\.?\d*", file_name)  # 这一段 是为了解决文件乱序问题
                # f1 = (f1[0], f1[1][:-1])
                # f1 = list(map(int, f1))
                r.append(file_name)
    alllist = sorted(r)
    print(alllist)
    time.sleep(2)
    # currentMouseX, currentMouseY = pyautogui.position() # 鼠标当前位置
    # print(currentMouseX, currentMouseY)
    # time.sleep(2)
    # currentMouseX, currentMouseY = pyautogui.position() # 鼠标当前位置
    # print(currentMouseX, currentMouseY)
    #删除第一首素材
    # pyautogui.click(177, 239, 1, 0.5, button='right')
    # # time.sleep(2)
    # currentMouseX, currentMouseY = pyautogui.position() # 鼠标当前位置
    # print(currentMouseX, currentMouseY)
    # pyautogui.click(x=206, y=255, duration=0.5) # 先移动到(100, 200)再单击
    # #确定
    # pyautogui.click(x=900, y=664, duration=0.5) # 先移动到(100, 200)再单击
    #
    # print(check_ok('016丰盛的人生_伴奏_消音.mp3'))
    for name in alllist:
        file_name = name
        name = name.replace('.mp3', '')
        name = name.replace('.mkv', '')
        p = "/Users/lism/Movies/"+name + ".srt"
        if check_ok(p):
            continue
        print(name+'导出开始')
        exportSrt(name)
        # ok = check_ok(p)
        # if ok:
        #     print(p, '完成')
        # else:
        #     print(p, '失败')
        #
        #     # time.sleep(30)
        #     #取消识别
        #     pyautogui.click(865, 635, 1, 1, button='left')
        #
        #     #删除第一首素材
        #     pyautogui.click(177, 239, 1, 0.5, button='right')
        #     pyautogui.click(x=206, y=255, duration=0.5) # 先移动到(100, 200)再单击
        #     #确定
        #     pyautogui.click(x=900, y=664, duration=0.5) # 先移动到(100, 200)再单击
        #
        #     shutil.move(path + file_name, banzou_path)

# shutil.move('/Users/lism/Program/WebStormProjects/slidev-praise/public/assets/media/062-使.mp3','/Users/lism/Program/WebStormProjects/slidev-praise/public/assets/ban/')
