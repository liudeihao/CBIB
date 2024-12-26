from download_image import download_all_videos
from id_task_map import work_videos


if __name__ == '__main__':

    # download_all_videos(work_videos)
    for video in work_videos:
        video.generate_labeled_images()
        video.move_labeled_images_to("E:\数据标注结果\\31_50")
        # video.clean()