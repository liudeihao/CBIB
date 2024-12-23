import cv2
import os

def generate_video_from_images(image_folder_path, video_name, fps=None):
    # 帧率，可以根据需要调整
    if fps is None:
        fps = 6

    # 视频宽高，需要与图片尺寸匹配
    frame_width = 1920
    frame_height = 1080

    # 创建VideoWriter对象
    out = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    # 获取所有图片文件
    images = [img for img in os.listdir(image_folder_path) if img.endswith(".jpg") or img.endswith(".png")]

    # 按顺序对图片文件进行排序
    images.sort()  # 可以根据需要调整排序方式

    # 读取图片并写入视频
    for image in images:
        img_path = os.path.join(image_folder_path, image)
        img = cv2.imread(img_path)

        # 检查图片是否读取成功
        if img is None:
            print(f"Failed to read {img_path}")
            continue

        # 调整图片尺寸
        img = cv2.resize(img, (frame_width, frame_height))

        # 写入帧
        out.write(img)
        print(f"Adding {image} to video")

    # 释放资源
    out.release()
    cv2.destroyAllWindows()