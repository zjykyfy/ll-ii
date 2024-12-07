import re
import requests
import os
import time

# 定义要提取的网页列表和对应的保存文件名
urls = {
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJUaWFuamluIiAmJiBwcm90b2NvbD0iaHR0cCI%3D": "Tianjin_liantong.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJaaGVqaWFuZyIgJiYgb3JnPSJDaGluYW5ldCIgJiYgcHJvdG9jb2w9Imh0dHAi": "Zhejiang_dianxin.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJCZWlqaW5nIiAmJiBvcmc9IkNoaW5hIFVuaWNvbSBCZWlqaW5nIFByb3ZpbmNlIE5ldHdvcmsiICYmIHByb3RvY29sPSJodHRwIg%3D%3D": "Beijing_liantong.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJTaGFuZ2hhaSIgJiYgb3JnPSJDaGluYSBUZWxlY29tIEdyb3VwIiAmJiBwcm90b2NvbD0iaHR0cCI%3D": "Shanghai_dianxin.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJHdWFuZ2RvbmciICYmIG9yZz0iQ2hpbmFuZXQiICYmIHByb3RvY29sPSJodHRwIg%3D%3D": "Guangdong_dianxin.txt",
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
# 遍历网页列表
for url, filename in urls.items():
    try:
        print(f'正在爬取{filename}.....')
        # 发送GET请求获取源代码
        response = requests.get(url, headers=headers)
        page_content = response.text
        # 查找所有符合指定格式的网址
        pattern = r'<a href="http://(.*?)" target="_blank">'
        urls_all = re.findall(pattern, page_content)
        urls = set(urls_all)  # 去重得到唯一的URL列表
        existing_urls = []
        # 检查文件是否存在，如果不存在则创建文件
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='utf-8'):
                pass
        # 读取已存在的URL
        with open(filename, 'r', encoding='utf-8') as file:
            existing_urls = file.readlines()
        existing_urls = [url.strip() for url in existing_urls]  # 去除每行末尾的换行符
        with open(filename, 'r+', encoding='utf-8') as file:
            content = file.read()
            file.seek(0, 0)  # 将文件指针移到文件开头
            for url in urls:
                if url not in existing_urls:
                    file.write(url + "\n")
                    print(url)
                    existing_urls.append(url)  # 将新写入的URL添加到已存在的URL列表中
            file.write(content)  # 将原有内容写回文件
    except Exception as e:
        print(f"爬取 {filename} URL {url} 失败：{str(e)}")
        continue
    # 暂停5秒
    time.sleep(5)
    print(f'{filename}爬取完毕,下一个')
