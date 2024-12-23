import os
from concurrent.futures import ThreadPoolExecutor
import paramiko

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
}

# SFTP的基础URL
hostname = "222.20.98.8"
port = 4396
username = "dhp"
password = "dhp123456"

# 创建 SSHClient 对象
ssh = paramiko.SSHClient()

try:
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname,port, username=username, password=password)
except Exception as e:
    print(f'Error connecting to {hostname}.')


# 下载目录
download_dir = './downloads/'

# 如果下载目录不存在，则创建它
if not os.path.exists(download_dir):
    os.makedirs(download_dir)


def download_image(task_id, video_id, download_all=True):
    try:
        # sftp获取文件
        sftp = ssh.open_sftp()
        remote_dir = f"/data/cyc/TS-Multi-Label-System/data/ts/images/{video_id:02d}/"
        local_dir = os.path.join(download_dir, str(video_id), 'images')
        label_file = os.path.join(download_dir, str(video_id), 'default.txt')
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)

        target_images = []
        if not download_all:
            # 获取所有已标注的文件。
            labeled_images = []
            with open(label_file) as f:
                for line in f:
                    img_name = line.strip().split(' ')[0]
                    labeled_images.append(img_name)
            target_images = labeled_images
        else:
            target_images = sftp.listdir(remote_dir)
        print(f"about to download {len(target_images)} images in video [{video_id}].")

        for img_name in target_images:
            remote_file = os.path.join(remote_dir, img_name)
            local_file = os.path.join(local_dir, img_name)
            try:
                sftp.get(remote_file, local_file)
            except Exception as e:
                print(f"error downloading image: [{img_name}] in video [{video_id}].",)

        print(f'Successfully downloaded images of task [{task_id}] to {local_dir} \t')

    except Exception as e:
        print(f'Error downloading task {task_id} image: {e}')


# 使用多线程下载每个任务的注释
with ThreadPoolExecutor(max_workers=15) as executor:
    futures = []
    for task_id, video_id in task_id_map.items():
        futures.append(executor.submit(download_image, task_id, video_id))

    # 等待所有任务完成
    for future in futures:
        future.result()


ssh.close()
exit(0)
