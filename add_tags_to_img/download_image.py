import os
from concurrent.futures import ThreadPoolExecutor
import paramiko

# SFTP的基础URL
hostname = "222.20.98.8"
port = 4396
username = "dhp"
password = "dhp123456"

# 创建 SSHClient 对象
ssh = paramiko.SSHClient()

try:
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port, username=username, password=password)
except Exception as e:
    print(f'Error connecting to {hostname}.')


def download_image(video):
    try:
        # sftp获取文件
        sftp = ssh.open_sftp()
        remote_dir = f"/data/cyc/TS-Multi-Label-System/data/ts/images/{video.id:02d}/"

        local_images_set = set(os.listdir(video.img_dir))
        print(f"total {len(video.image_filenames)} images in video [{video.id}].")

        for img_name in video.image_filenames:
            # 已存在
            if img_name in local_images_set:
                print(f"{video.id} already exists {img_name}, skip it.")
                continue

            remote_file = os.path.join(remote_dir, img_name)
            local_file = os.path.join(video.img_dir, img_name)
            try:
                sftp.get(remote_file, local_file)
            except Exception as e:
                print(f"error downloading image: [{img_name}] in video [{video.id}].", )

        print(f'Successfully downloaded images of video [{video.id}] to {video.img_dir} \t')

    except Exception as e:
        print(f'Error downloading task {video.id} image: {e}')



def download_all_videos(videos):
    # 使用多线程下载每个任务的注释
    with ThreadPoolExecutor(max_workers=15) as executor:
        futures = []
        for video in videos:
            futures.append(executor.submit(download_image, video))

        # 等待所有任务完成
        for future in futures:
            future.result()


# ssh.close()

