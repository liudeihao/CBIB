import os

from PIL import Image, ImageDraw, ImageFont

class Label:
    def __init__(self, id, name, color):
        self.id = id
        self.name = name
        self.color = color

labels = [
    Label(id=0, name="体外", color=(250, 50, 83)),
    Label(id=1, name="无器械", color=( 51,221,255)),
    Label(id=2, name="模糊", color=(139,148, 86)),
    Label(id=3, name="烟雾", color=( 38,156, 38)),
    Label(id=4, name="光照不均", color=( 20,100, 15)),
    Label(id=5, name="遮挡", color=( 50,183,250)),
    Label(id=6, name="其他遮挡", color=(105, 54, 93)),
    Label(id=7, name="钳类", color=(146,108, 96)),
    Label(id=8, name="超声刀", color=( 73, 95, 97)),
    Label(id=9, name="Ligasure", color=(227, 22,226)),
    Label(id=10, name="吸引器", color=( 62, 80, 62)),
    Label(id=11, name="施夹钳", color=(255,106, 77)),
    Label(id=12, name="剪刀", color=(178, 80, 80)),
    Label(id=13, name="钩类", color=(245,147, 49)),
    Label(id=14, name="持针器", color=(115, 51,128)),
    Label(id=15, name="推线杆", color=(146,171,144)),
    Label(id=16, name="未知器械", color=(130,152,128)),
    Label(id=17, name="白钉仓", color=(114,133,112)),
    Label(id=18, name="天蓝钉仓", color=( 50,183,250)),
    Label(id=19, name="蓝钉仓", color=( 81, 95, 80)),
    Label(id=20, name="紫钉仓", color=( 65, 76, 64)),
    Label(id=21, name="金钉仓", color=( 48, 57, 48)),
    Label(id=22, name="绿钉仓", color=( 32, 38, 32)),
    Label(id=23, name="黑钉仓", color=( 16, 19, 16)),
    Label(id=24, name="其他钉仓", color=(  8,  9,  8)),
    Label(id=25, name="针线", color=( 24, 85, 24)),
    Label(id=26, name="样本袋", color=( 40,142, 40)),
    Label(id=27, name="Hem-O-Lok", color=(  9, 12,104)),
    Label(id=28, name="钛夹", color=( 72,105, 72)),
    Label(id=29, name="纱布", color=( 88,121,120)),
    Label(id=30, name="未知耗材", color=(104, 44,136)),
    Label(id=31, name="电刀", color=( 29, 29,185)),
    Label(id=32, name="止血棉", color=(255, 53, 94)),
]


def check_char_type(char):
    if '\u0020' <= char <= '\u007F':
        return 'English'
    elif '\u4e00' <= char <= '\u9fff':
        return 'Chinese'
    else:
        return 'Other'

def generate_label(label):
    # 要转换为图片的文字
    width = 30
    for char in label.name:
        if check_char_type(char) == 'Chinese':
            width += 30
        else:
            width += 15
    # 创建一个新的图像，设置宽度和高度
    height = 55

    image = Image.new('RGBA', (width, height), color=(0,0,0,255))  # 黑色背景

    # 创建一个可以在图像上绘图的Draw对象
    draw = ImageDraw.Draw(image)

    # 设置圆角矩形的半径
    corner_radius = 4

    # 设置圆角矩形的位置和大小
    rect = (corner_radius, corner_radius, width - corner_radius, height - corner_radius)

    # 绘制圆角矩形
    draw.rounded_rectangle(rect, fill=label.color, radius=corner_radius)

    font_path = 'LXGWWenKaiMono-Bold.ttf'  # 字体文件路径
    font_size = 30  # 字体大小
    font = ImageFont.truetype(font_path, font_size)

    # 计算文本的位置以使其居中
    text_position = (15, 10)

    # 将文字绘制到图像上，设置文本颜色为白色
    draw.text(text_position, label.name, font=font, fill=(255, 255, 255))

    # 保存图像到文件
    filename = os.path.join("tags", f"{label.id}.png")
    image.save(filename)

if not os.path.exists("tags"):
    os.mkdir("tags")

for label in labels:
    generate_label(label)
