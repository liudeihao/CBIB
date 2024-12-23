import os

import cv2

def add_tags_to_image(src_img_path, dst_img_path, labels):
    overlay_imgs = []

    # 读取标签图片
    for label in labels:
        overlay_image_path = os.path.join("tags", f"{label}.png")
        overlay_imgs.append(cv2.imread(overlay_image_path))
    # 读取基础图片
    base_img = cv2.imread(src_img_path)

    x, y = (10, 10)
    for overlay_img in overlay_imgs:
        # 获取图片尺寸
        h, w, _ = overlay_img.shape

        # 设置叠加区域为图片左上角的位置
        nx, ny = (x + w, y + h)

        # 叠加图片
        base_img[y:ny, x:nx] = overlay_img
        y = ny + 10

    # 保存图片
    cv2.imwrite(dst_img_path, base_img)
    print(f"Saved image with labels to {dst_img_path}")


if __name__ == '__main__':
    # 使用函数在图片上叠加图片
    labels = [1,2,3,4,5,6]
    add_tags_to_image('test.jpg', 'test1.jpg', labels)
