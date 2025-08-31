from pywinauto import Application
import os
import sys
import subprocess
import time
import logging
import tempfile
from datetime import datetime
try:
    import win32gui
    import win32con
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

# 配置日志
log_file = os.path.join(tempfile.gettempdir(), 'AutoWechat.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)  # 同时输出到控制台
    ]
)

def log_info(message):
    """记录信息日志"""
    logging.info(message)

def log_error(message):
    """记录错误日志"""
    logging.error(message)

# os.popen('F:\Software\soft\WeChat\WeChat.exe')

wechat_path = r'"C:\Program Files\Tencent\WeChat\WeChat.exe"'
sleep = 10

# 输出日志文件位置
log_info(f"日志文件位置: {log_file}")

if len(sys.argv) > 1:
    log_info(f"命令行参数 - 微信路径: {sys.argv[1]}")
    wechat_path = sys.argv[1]
    pass

if len(sys.argv) > 2:
    sleep = int(sys.argv[2])
    log_info(f"命令行参数 - 等待时间: {sleep}秒")
    pass

# 启动微信
log_info("正在启动微信")
os.popen(wechat_path)

log_info(f"等待 {sleep} 秒让微信启动...")
time.sleep(sleep)

try:
    # 连接到微信窗口
    log_info("正在连接到微信窗口...")
    
    # 首先尝试连接到主微信窗口（通常标题就是"微信"）
    try:
        app = Application(backend="uia").connect(title="微信")
        window = app.window(title="微信")
        log_info("成功连接到主微信窗口")
    except Exception as e:
        log_error(f"连接主微信窗口失败: {e}")
        log_info("尝试连接到包含'微信'的窗口...")
        
        # 如果失败，尝试查找所有包含"微信"的窗口
        from pywinauto import findwindows
        windows = findwindows.find_elements(title_re=".*微信.*", backend="uia")
        
        if not windows:
            log_error("未找到任何微信窗口")
            sys.exit(1)
        
        log_info(f"找到 {len(windows)} 个包含'微信'的窗口:")
        for i, win in enumerate(windows):
            log_info(f"  {i+1}. 标题: {win.rich_text}, PID: {win.process_id}")
        
        # 选择第一个窗口（通常是主窗口）
        target_window = windows[0]
        app = Application(backend="uia").connect(process=target_window.process_id)
        window = app.window(handle=target_window.handle)
        log_info(f"已连接到窗口: {target_window.rich_text}")

except Exception as e:
    log_error(f"连接微信窗口时发生错误: {e}")
    log_error("请确保微信已正确启动")
    sys.exit(1)



try:
    # 查找"进入微信"按钮
    log_info("正在查找'进入微信'按钮...")
    enter_button = window.child_window(title="进入微信", control_type="Button")
    
    # 检查是否找到按钮
    if enter_button.exists():
        log_info("找到'进入微信'按钮")
        
        # 尝试多种点击方法，确保即使被遮挡也能成功点击
        click_success = False
        
        # 方法1: 使用鼠标模拟点击
        try:
            enter_button.click_input()
            log_info("使用鼠标模拟点击成功")
            click_success = True
        except Exception as e1:
            log_error(f"鼠标模拟点击失败: {e1}")
        if click_success:
            log_info("微信自动登录完成！")
        else:
            log_error("失败了，请检查微信窗口状态")
    else:
        log_info("未找到'进入微信'按钮")
        log_info("可能微信已经登录，或者界面与预期不同")
        
        # 打印窗口的所有控件信息，帮助调试
        log_info("当前窗口的控件信息:")
        try:
            # 将控件信息重定向到日志
            import io
            from contextlib import redirect_stdout
            
            output_buffer = io.StringIO()
            with redirect_stdout(output_buffer):
                window.print_control_identifiers()
            control_info = output_buffer.getvalue()
            log_info(f"控件信息:\n{control_info}")
        except Exception as debug_e:
            log_error(f"无法打印控件信息: {debug_e}")

except Exception as e:
    log_error(f"查找或点击按钮时发生错误: {e}")
    log_info("微信可能已经登录，或者界面结构发生了变化")

