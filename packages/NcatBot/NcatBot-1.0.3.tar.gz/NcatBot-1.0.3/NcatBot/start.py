import requests
import zipfile
import os
from . import log


def download_and_extract(url="https://github.com/NapNeko/NapCatQQ/releases/download/v3.3.20/NapCat.Shell.zip", zip_file_name="NapCat.Shell.zip"):
    """
    下载并解压zip文件
    :param url: 下载地址
    :param zip_file_name: 下载后的zip文件名
    :param extract_folder: 解压后的文件夹名
    :return: None
    """
    # 获取当前目录路径
    current_directory = os.getcwd()

    # 使用//分隔符
    formatted_directory = current_directory.replace(os.sep, '//')
    # 下载文件
    response = requests.get(url)

    if response.status_code == 200:
        with open(formatted_directory + "//" + zip_file_name, "wb") as file:
            file.write(response.content)
        log.info("文件下载成功！", zip_file_name)
        
        
        # 解压文件
        with zipfile.ZipFile(formatted_directory + "//" + zip_file_name, 'r') as zip_ref:
            zip_ref.extractall(formatted_directory)  # 解压到当前目录
        log.info("文件解压成功！", zip_file_name)
        os.remove(formatted_directory + "//" + zip_file_name)  # 删除zip文件
    else:
        log.error(f"下载失败，状态码: {response.status_code}")


