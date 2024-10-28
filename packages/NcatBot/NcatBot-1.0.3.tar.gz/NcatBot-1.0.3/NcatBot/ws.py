import websocket
import psutil
from box import Box
import json
from . import log
import os
from .start import download_and_extract
import yaml
import time

# 获取当前目录路径
current_directory = os.getcwd()
# 使用//分隔符
formatted_directory = current_directory.replace(os.sep, '//')

with open(formatted_directory + "//config.yaml", "r", encoding="utf-8") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    QQaccount = config["QQaccount"]
    log.info(f"当前QQ账号：{QQaccount}", "success")


process_name = "NapCatWinBootMain.exe"
found = False

# 遍历所有正在运行的进程
for process in psutil.process_iter(attrs=['pid', 'name']):
    if process.info['name'] == process_name:
        log.info(f"{process_name} 已运行，进程运行ID: {process.info['pid']}", "success")
        found = True
        break

if not found:
    log.warning("进程未运行, 开始尝试运行客户端...", "failure")
    if os.path.exists(formatted_directory + "//NapCatWinBootMain.exe"):
        log.info("客户端已存在，跳过下载！", "success")
    else:
        log.info("客户端不存在，开始下载客户端...", "info")
        download_and_extract()
    try:
        # 遍历config文件夹内所有文件，查看是否有napcat_{QQaccount}.json文件和onebot11_{QQaccount}.json文件
        if os.path.exists(formatted_directory + f"//config//napcat_{QQaccount}.json") and os.path.exists(formatted_directory + f"//config//onebot11_{QQaccount}.json"):
            log.info(f"找到配置文件：napcat_{QQaccount}.json和onebot11_{QQaccount}.json", "success")
            content=f"""@echo off
./launcher.bat {QQaccount}"""
            # 修改quickLoginExample.bat文件内容并覆盖原文件
            with open(formatted_directory + "//quickLoginExample.bat", "w", encoding="utf-8") as f:
                f.write(content)
            log.info("启动客户端...", "info")
            os.startfile(formatted_directory + "//quickLoginExample.bat")
        else:
            log.info(f"未找到配置文件：napcat_{QQaccount}.json和onebot11_{QQaccount}.json, 首次登入，先扫码登入后重新运行程序", "failure")
            os.startfile(formatted_directory + "//launcher.bat")
            log.info("二维码如果命令行无法扫码，请手动打开cache文件夹查看二维码，二维码在3秒后弹出", "info")
            time.sleep(3)
            os.startfile(formatted_directory + f"//cache//qrcode.png")

    except Exception as e:
        log.error(f"启动客户端失败，错误信息：{e}", "failure")
        exit()

class QQBot:
    def __init__(self, url):
        self.url = url
        self.ws = websocket.WebSocketApp(self.url, on_message=self.on_message, on_error=self.on_error, on_close=self.on_close)
        self.msg_handlers = {}

    def run(self):
        self.ws.run_forever()

    def on_message(self, ws, message):
        msg = json.loads(message)
        msg = Box(msg)
        msg_type = msg.post_type
        if msg_type in self.msg_handlers:
            for handler in self.msg_handlers[msg_type]:
                handler(msg)

    def on_error(self, ws, error):
        log.error(f"Websocket error: {error}", "failure")

    def on_close(self, ws, close_status_code, close_msg):
        log.warning(f"Websocket closed", "warning")

    def msg_register(self, msg_type):
        def decorator(func):
            if msg_type not in self.msg_handlers:
                self.msg_handlers[msg_type] = []
            self.msg_handlers[msg_type].append(func)
            return func
        return decorator

