import os
import shutil

from add_label_to_image import add_tags_to_image
from generate_video import generate_video_from_images


class Video:
    def __init__(self, id, task):
        self.id = id
        self.task = task
        self.base_dir = os.path.join("downloads", str(self.id))
        self.img_dir = os.path.join(self.base_dir, "images")
        self.label_path = os.path.join(self.base_dir, "default.txt")
        self.labeled_img_dir = os.path.join(self.base_dir, "labeled_images")
        self.image_filenames = None
        if not os.path.exists(self.label_path):
            print("default.txt not found!")
        else:
            self.image_filenames = []
            with open(self.label_path, "r") as f:
                lines = f.readlines()
                for line in lines:
                    filename = line.strip().split(" ")[0]
                    self.image_filenames.append(filename)

        if not os.path.exists(self.img_dir):
            os.makedirs(self.img_dir)

        if not os.path.exists(self.labeled_img_dir):
            os.mkdir(self.labeled_img_dir)

    def __del__(self):
        if os.path.exists(self.img_dir) and not os.listdir(self.img_dir):
            os.rmdir(self.img_dir)
        if os.path.exists(self.labeled_img_dir) and not os.listdir(self.labeled_img_dir):
            os.rmdir(self.labeled_img_dir)

    def clean(self):
        unwanted_files = [
            os.path.join(self.base_dir, str(self.id))
        ]
        for file in unwanted_files:
            if os.path.isdir(file):
                shutil.rmtree(file)
                print("removed", file)
            elif os.path.exists(file):
                os.remove(file)
                print("removed", file)

    def move_labeled_images_to(self, dst_dir, force=False):
        src_dir_name = os.path.join(self.base_dir, str(self.id))
        if str(self.id) not in os.listdir(self.base_dir):
            os.rename(self.labeled_img_dir, src_dir_name)
        src = src_dir_name
        dst_path = os.path.join(dst_dir)
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)
        if str(self.id) not in os.listdir(dst_path):
            shutil.move(src, dst_path)
            print(f"Renamed {self.labeled_img_dir} to {src}, moved images to {dst_path}")
        elif force:
            shutil.rmtree(dst_path)
            shutil.move(src, dst_path)
            print(f"{dst_path}/{str(self.id)} already exists! Overwriting {src} images to {dst_path}...")
        else:
            print(f"{dst_path}/{str(self.id)} already exists! Use force=True to overwrite.")

    def generate_labeled_images(self):
        with open(self.label_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                ss = line.strip().split(' ')
                img_name = ss[0]
                labels = ss[1:]
                src_img_path = os.path.join(self.img_dir, img_name)
                dst_img_path = os.path.join(self.labeled_img_dir, f"{self.id:02}_{img_name}")
                add_tags_to_image(src_img_path, dst_img_path, labels)

    def generate_labeled_video(self):
        generate_video_from_images(self.labeled_img_dir, os.path.join(self.base_dir, "output.mp4"), 6)
        print(f"Successfully generated labeled video for video {self.id} to {os.path.join(self.base_dir, 'output.mp4')}")

    def check_synsets(self, global_synsets_path):
        local_synsets_path = os.path.join(self.base_dir, "synsets.txt")
        assert os.path.exists(local_synsets_path), "synsets.txt doesn't exist, are you sure default.txt exist?"

        lf = open(local_synsets_path, 'r')
        gf = open(global_synsets_path, 'r')
        while True:
            ll = lf.readline()
            gl = gf.readline()
            assert ll == gl, "Synsets file does not match global synsets file!"
            if not ll:
                break