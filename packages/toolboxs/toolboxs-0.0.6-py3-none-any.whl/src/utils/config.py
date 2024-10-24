import os
import re
import json
import random
import logging
import datetime
from typing import Tuple,Optional, Union

'''
    @description: 日志服务
    @params: 
    @author: MR.阿辉
    @datetime: 2024-03-07 23:33:52
    @return: 
'''
class Logger():
    '''
        @description: 实例化 logger
        @params: log_file_path 日志文件保存目录
        @params: log_file_name 日志文件名称
        @params: logger_name logger 名称，默认为 logger
        @params: mode 写入模式 a 追加写，w
        @author: MR.阿辉
        @datetime: 2024-03-12 08:55:12
        @return: 
    '''
    def __init__(self,
                log_file_path:str,
                log_file_name:Optional[str]=None,
                logger_name:str='logger',mode:str='a') -> None:
        
        logger = logging.getLogger(logger_name)
        # 清空所有的 handler，避免重复日志写入
        logger.handlers.clear()
        
        # 设置日志级别
        logger.setLevel(logging.DEBUG)
        
        # 日志格式
        log_format = logging.Formatter(
            fmt='%(asctime)-20s%(filename)s:%(lineno)-4s| %(name)s[%(levelname)-8s]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 日志文件名称
        file_name:str =f'{logger_name if log_file_name is None else log_file_name}-{datetime.datetime.now().strftime("%Y%m%d")}.log'
        
        # 文件 handler
        fh = logging.FileHandler(filename=Utils.mkdirs(log_file_path,file_name), encoding='utf-8', mode=mode)
        
        # 定义handler的输出格式
        fh.setFormatter(log_format)
        logger.addHandler(fh)
        self.logger = logger

class Utils:
    
    '''
        @description: 判断字符串是否为url
        @params: url 字符串地址
        @author: MR.阿辉
        @datetime: 2024-03-12 14:40:38
        @return: 
    '''
    @staticmethod
    def is_url(url:str) -> bool:
        pattern = r'^https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$'
        return bool(re.match(pattern, url))
    
    '''
        @description: 判断字符串是否为数值
        @params: s 字符串
        @author: MR.阿辉
        @datetime: 2024-09-19 22:02:00
        @return: 
    '''
    @staticmethod
    def is_number(s:str):
        # 正则表达式匹配正整数或负整数
        pattern = r'^-?\d+(\.\d+)?$'
        return bool(re.match(pattern, s))
    
        
    '''
        @description: 判断字符串是否为文件地址
        @params: path 文件地址字符串
        @author: MR.阿辉
        @datetime: 2024-03-12 14:41:30
        @return: 
    '''
    @staticmethod
    def is_file_path(path:str) -> bool:
        try:
            if  not isinstance(path, str):
                return False
            # os.path.exists(0) 返回为 True ，绝了
            return os.path.exists(path) and os.path.isfile(path)
        except Exception as _:
            return False
    
    '''
        @description: 配置请求头
        @params: 
        @author: MR.阿辉
        @datetime: 2024-10-24 12:39:01
        @return: 
    '''
    @staticmethod
    def header_config():
        return {
            "PC": {
                "Mac": [
                    {
                        "Sec-Ch-Ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
                        "Sec-Ch-Ua-Mobile": "?0",
                        "Sec-Ch-Ua-Platform": "\"macOS\"",
                        "Sec-Fetch-Dest": "document",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-Site": "none",
                        "Sec-Fetch-User": "?1",
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
                    },
                    {
                        "Sec-Ch-Ua": "\"Not A(Brand\";v=\"99\", \"Google Chrome\";v=\"121\", \"Chromium\";v=\"121\"",
                        "Sec-Ch-Ua-Mobile": "?0",
                        "Sec-Ch-Ua-Platform": "\"macOS\"",
                        "Sec-Fetch-Dest": "document",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-Site": "none",
                        "Sec-Fetch-User": "?1",
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
                    }
                ],
                "Windows": [
                    {
                        "sec-ch-ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
                        "sec-ch-ua-mobile": "?0",
                        "sec-ch-ua-platform": "\"Windows\"",
                        "sec-fetch-dest": "empty",
                        "sec-fetch-mode": "cors",
                        "sec-fetch-site": "same-site",
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
                    }
                ]
            },
            "MP": {
                "Android": [
                    {
                        "Sec-Ch-Ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
                        "Sec-Ch-Ua-Mobile": "?1",
                        "Sec-Ch-Ua-Platform": "\"Android\"",
                        "Sec-Fetch-Dest": "document",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-Site": "cross-site",
                        "Sec-Fetch-User": "?1",
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"
                    }
                ],
                "iPhone": [
                    {
                        "Sec-Fetch-Dest": "image",
                        "Sec-Fetch-Mode": "no-cors",
                        "Sec-Fetch-Site": "cross-site",
                        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
                    },
                    {
                        "Sec-Fetch-Dest": "document",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-Site": "same-origin",
                        "Sec-Fetch-User": "?1",
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
                    },
                    {
                        "Sec-Fetch-Dest": "document",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-Site": "same-origin",
                        "Sec-Fetch-User": "?1",
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
                    },
                    {
                        "Sec-Fetch-Dest": "document",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-Site": "same-origin",
                        "Sec-Fetch-User": "?1",
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
                    },
                    {
                        "Sec-Fetch-Dest": "document",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-Site": "same-origin",
                        "Sec-Fetch-User": "?1",
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15"
                    },
                    {
                        "Sec-Fetch-Dest": "document",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-Site": "same-origin",
                        "Sec-Fetch-User": "?1",
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15"
                    }
                ]
            }
        }

    
    '''
        @description: mkdir 创建文件
        @params: file_dir 文件目录地址
        @params: file_name 文件名称
        @author: MR.阿辉
        @datetime: 2024-03-12 14:50:39
        @return: 
    '''
    @staticmethod
    def mkdirs(file_dir:str,file_name:str,) -> str:
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        return os.path.join(file_dir,file_name) 
    
    '''
        @description: 格式化秒
        @params: seconds 秒
        @author: MR.阿辉
        @datetime: 2024-03-12 17:10:39
        @return: 
    '''
    @staticmethod
    def format_seconds(seconds:Union[int,float]):
        if seconds < 60:
            return f"{round(seconds,2)}秒"
        minutes, seconds = divmod(seconds, 60)
        if minutes < 60:
            return f"{round(minutes,2)}分{round(seconds,2)}秒"
        hours, minutes = divmod(minutes, 60)
        return f"{round(hours,2)}时{round(minutes,2)}分{round(seconds,2)}秒"
    
    '''
        @description: 随机读取一个请求头配置
        @params: device 浏览器驱动 PC-Mac
        @author: MR.阿辉
        @datetime: 2024-03-12 17:20:37
        @return: 
    '''
    @staticmethod
    def get_headers(device:str) -> dict:
        # TODO：读取 请求头的 json 配置文件
        terminal,system = device.split('-')
        headers_data = Utils.header_config()
        headers_list = headers_data[terminal][system]
        # 随机取一个请求头
        return random.choice(headers_list)

if __name__ == "__main__" :
    print(Utils.format_seconds(1381))
    
    