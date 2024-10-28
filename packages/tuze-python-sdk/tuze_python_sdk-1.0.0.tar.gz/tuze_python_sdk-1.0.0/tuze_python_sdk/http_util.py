#!/Users/tuze/.pyenv/shims/python

import json

import requests
from colorama import Fore, Style, init

# 初始化 colorama
init(autoreset=True)

def send_post_request(url, headers, data):
    """ 发送 POST 请求并返回响应 """
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response

def print_response(response):
    """ 打印请求的状态码、头部信息和响应体 """
    # 打印状态码
    if response.status_code == 200:
        print(Fore.GREEN+f"响应Code: {response.status_code}\n")
    else:
        print(Fore.RED+f"响应Code: {response.status_code}\n")

    # 打印Headers
    header_str="\n".join([f"{key}:{value}" for key,value in response.headers.items()])
    print(Fore.WHITE+f"响应Headers: \n{header_str}\n")
    
    # 打印响应体
    print(Fore.YELLOW+f"响应Body\n{response.text} \n")

        
def print_request(url, headers, data):
    """ 打印请求的状态码、头部信息和响应体 """
    # 打印url
    print(Fore.CYAN+f"请求URL:{url}\n")

    # 打印请求Headers
    print(Fore.WHITE+f"请求Headers\n{json.dumps(headers, indent=4)}\n")

    # 打印请求body
    print(Fore.MAGENTA+f"请求Body\n{json.dumps(data, indent=4)}\n")
