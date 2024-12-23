import os

from add_label_to_image import add_tags_to_image
from compose_to_video import generate_video_from_images

task_id_map = {
    66: 1,
    # 65: 9,
    # 67: 2,
    # 68: 3,
    # 69: 4,
    # 70: 5,
    # 71: 6,
    # 72: 7,
    # 73: 8,
    # 75: 10,
}
import os

download_dir = "downloads"

class Video:
    def __init__(self, id, task):
        self.id = id
        self.task = task
        self.base_dir = os.path.join("downloads", str(self.id))
        self.img_dir = os.path.join(self.base_dir, "images")
        self.label_path = os.path.join(self.base_dir, "default.txt")
        self.labeled_img_dir = os.path.join(self.base_dir, "labeled_images")
        if not os.path.exists(self.labeled_img_dir):
            os.mkdir(self.labeled_img_dir)


videos = [Video(id, task) for task, id in task_id_map.items()]

def generate_labeled_video(video):
    video = videos[0]

    base_dir = video.base_dir
    img_dir = video.img_dir
    label_path = video.label_path
    labeled_img_dir = video.labeled_img_dir

    with open(label_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            ss = line.strip().split(' ')
            img_name = ss[0]
            labels = ss[1:]
            src_img_path = os.path.join(img_dir, img_name)
            dst_img_path = os.path.join(labeled_img_dir, img_name)
            add_tags_to_image(src_img_path, dst_img_path, labels)
    generate_video_from_images(labeled_img_dir, os.path.join(base_dir, "output.mp4"), 6)
    print(f"Successfully generated labeled video for video {video.id} to {os.path.join(base_dir, 'output.mp4')}")

if __name__ == '__main__':
    generate_labeled_video(videos[0])