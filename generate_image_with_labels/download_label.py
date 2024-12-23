import requests
from urllib.parse import urljoin
import os
import zipfile
import time
from concurrent.futures import ThreadPoolExecutor

# 假设这是你要下载的任务ID和视频ID映射
task_id_map = {
    65: 9,
    66: 1,
    67: 2,
    68: 3,
    69: 4,
    70: 5,
    71: 6,
    72: 7,
    73: 8,
    75: 10,
    # 117: 11,
    # 118: 25,
    # 119: 28,
    # 120: 12,
    # 121: 13,
    # 122: 14,
    # 123: 15,
    # 124: 17,
    # 125: 18,
    # 126: 19,
    # 127: 20,
    # 128: 21,
    # 129: 22,
    # 131: 24,
    # 132: 26,
}

# API的基础URL
base_url = 'http://222.20.96.3:8333/api/tasks/'

# 下载目录
download_dir = './downloads/'

# 如果下载目录不存在，则创建它
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# 设置Cookie
cookies = {
    # 'csrftoken': '4m80HUlJ6ReLoyOSgLRRqC6skyQzsSVL',
    # 'sessionid': 's0o3ru87dw0kxogh0e5ajoyj3cdtal8s'
    'csrftoken': 'mmqJn8JZsuYER70N8dPLp5aOLfUMjwB4',
    'sessionid': 'tghwrjjr2q7kbejsyu0n80kkp9sdc9vr'
}

def download_annotation(task_id, video_id):
    # 构建完整的API URL
    api_url = urljoin(base_url, f'{task_id}/annotations?org=TSMultiLabel&use_default_location=true&format=ImageNet+1.0&action=download')
    
    try:
        # 发送初始GET请求
        response = requests.get(api_url, cookies=cookies)
        
        # 检查请求是否被接受
        while response.status_code == 202:
            print(f'Task {task_id} annotation is being processed, waiting...')
            time.sleep(3)  # 等待3秒
            response = requests.get(api_url, cookies=cookies)
        
        # 检查请求是否成功
        if response.status_code == 200:
            # 定义文件名
            file_name = f'task_{task_id}_annotation.zip'
            file_path = os.path.join(download_dir, file_name)
            
            # 写入文件
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f'Successfully downloaded {file_name}')
            
            # 解压文件到相应的video_id文件夹
            video_dir = os.path.join(download_dir, str(video_id))
            if not os.path.exists(video_dir):
                os.makedirs(video_dir)
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(video_dir)
            print(f'Successfully extracted to {video_dir}')
            
            # 删除临时zip文件
            os.remove(file_path)
        else:
            print(f'Failed to download task {task_id} annotation, status code: {response.status_code}')
    
    except Exception as e:
        print(f'Error downloading task {task_id} annotation: {e}')

# 使用多线程下载每个任务的注释
with ThreadPoolExecutor(max_workers=15) as executor:
    futures = []
    for task_id, video_id in task_id_map.items():
        futures.append(executor.submit(download_annotation, task_id, video_id))
    
    # 等待所有任务完成
    for future in futures:
        future.result()