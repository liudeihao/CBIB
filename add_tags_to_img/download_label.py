print("should not use package [download_label]!!!")
exit(1)

import requests
from urllib.parse import urljoin
import os
import zipfile
import time
from concurrent.futures import ThreadPoolExecutor

# API的基础URL
base_url = 'http://222.20.96.3:8333/api/tasks/'

# 设置Cookie
cookies = {
    'csrftoken': '27396mztvyj2olqt0qdrsyxvbl5dzaor',
    'sessionid': 'KbGmmeFOpegGuBNPJ5lDhuegoks0d3tl'
}

def download_annotation(video):
    # 构建完整的API URL
    api_url = urljoin(base_url, f'{video.task}/annotations?org=TSMultiLabel&use_default_location=true&format=ImageNet+1.0&action=download')
    print(api_url)
    try:
        # 发送初始GET请求
        response = requests.get(api_url, cookies=cookies)
        
        # 检查请求是否被接受
        while response.status_code == 202:
            print(f'Task {video.task} annotation is being processed, waiting...')
            time.sleep(3)  # 等待3秒
            response = requests.get(api_url, cookies=cookies)
        
        # 检查请求是否成功
        if response.status_code == 200:
            # 定义文件名
            file_name = f'task_{video.task}_annotation.zip'
            file_path = os.path.join(video.base_dir, file_name)
            
            # 写入文件
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f'Successfully downloaded {file_name}')
            
            # 解压文件到相应的video.id文件夹
            video_dir = os.path.join(video.base_dir, str(video.id))

            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(video_dir)
            print(f'Successfully extracted to {video_dir}')
            
            # 删除临时zip文件
            os.remove(file_path)
        else:
            print(f'Failed to download task {video.task} annotation, status code: {response.status_code}')
    
    except Exception as e:
        print(f'Error downloading task {video.task} annotation: {e}')



# 使用多线程下载每个任务的注释
def download_label(videos):
    with ThreadPoolExecutor(max_workers=15) as executor:
        futures = []
        for video in videos:
            futures.append(executor.submit(download_annotation, video))

        # 等待所有任务完成
        for future in futures:
            future.result()
