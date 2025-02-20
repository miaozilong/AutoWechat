from pywinauto import Application
import os
import sys
import subprocess
import time

# os.popen('F:\Software\soft\WeChat\WeChat.exe')

wechat_path = 'F:\Software\soft\WeChat\WeChat.exe'
sleep = 2

if len(sys.argv) > 1:
    print(sys.argv[1])
    wechat_path = sys.argv[1]
    pass

if len(sys.argv) > 2:
    sleep = int(sys.argv[2])
    pass

# 启动微信
print("正在启动微信")
os.popen(wechat_path)

time.sleep(1)
# exit()


# 连接到微信窗口
# 假设微信窗口的标题包含“微信”
app = Application(backend="uia").connect(title_re=".*微信.*")

# 获取微信窗口
window = app.window(title_re=".*微信.*")



# 查找“进入微信”按钮
enter_button = window.child_window(title="进入微信", control_type="Button")


# 检查是否找到按钮
if enter_button.exists():
    print("找到“进入微信”按钮")
    # 模拟点击按钮
    enter_button.click_input()
    print("已点击“进入微信”按钮")
else:
    print("未找到“进入微信”按钮")
    pass

