import json
import os
import yaml
from . import log
# 获取当前目录路径
current_directory = os.getcwd()

# 使用//分隔符
formatted_directory = current_directory.replace(os.sep, '//')

with open(formatted_directory + '//config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
    QQaccount = config['QQaccount']

json_file_path = f"{formatted_directory}//config//onebot11_{QQaccount}.json"

def update_ports(http_port, ws_port, reportSelfMessage=False, musicSignUrl=""):
    try:
        # 读取JSON文件
        with open(json_file_path, 'r', encoding='utf-8') as file:
            json_content = json.load(file)

        # 更新端口和其他设置
        json_content.update({
            'http': {'enable': True, 'port': http_port},
            'ws': {'enable': True, 'port': ws_port},
            'reportSelfMessage': reportSelfMessage,
            'musicSignUrl': musicSignUrl
        })

        # 写入更新后的内容到文件
        with open(json_file_path, 'w', encoding='utf-8') as file:
            json.dump(json_content, file, ensure_ascii=False, indent=4)

        log.info(f"HTTP端口已更新为{http_port}，WS端口已更新为{ws_port}", "NcatBot")
        
    except FileNotFoundError:
        log.error("配置文件未找到，请检查路径设置", "NcatBot")
    except json.JSONDecodeError:
        log.error("读取的JSON文件格式不正确", "NcatBot")
    except Exception as e:
        log.error(f"更新端口时发生错误: {e}", "NcatBot")

