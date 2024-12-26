# 假设这是你要下载的任务ID和视频ID映射
from Video import Video

task_id_map = {
    233: 85,
    232: 84,
    231: 83,
    230: 82,
    229: 81,
    228: 80,
    227: 79,
    226: 78,
    225: 77,
    224: 76,
    223: 75,
    222: 74,
    221: 73,
    220: 72,
    219: 71,
    218: 70,
    217: 69,
    216: 68,
    215: 67,
    214: 66,
    213: 65,
    212: 64,
    211: 63,
    210: 62,
    209: 61,
    208: 60,
    206: 59,
    205: 58,
    204: 57,
    203: 56,
    202: 55,
    201: 54,
    200: 53,
    199: 52,
    198: 51,
    197: 50,
    196: 49,
    195: 48,
    194: 47,
    193: 46,
    192: 45,
    191: 44,
    190: 43,
    189: 42,
    188: 41,
    187: 40,
    186: 39,
    185: 38,
    184: 37,
    183: 36,
    182: 35,
    181: 34,
    180: 86,
    179: 33,
    178: 32,
    177: 87,
    176: 31,
    175: 88,
    174: 89,
    173: 30,
    172: 90,
    171: 91,
    170: 92,
    # 169: 29,
    168: 93,
    # 167: 27,
    166: 94,
    165: 95,
    164: 96,
    163:23,
    # 162:16,
    161: 97,
    160: 98,
    159: 99,
    158: 100,
    157: 101,
    156: 102,
    155: 103,
    154: 104,
    153: 105,
    152: 106,
    151: 107,
    150: 108,
    149: 109,
    # 119: 28,
    207: 11,
    # 65: 9,
    # 66: 1,
    # 67: 2,
    # 68: 3,
    # 69: 4,
    # 70: 5,
    # 71: 6,
    # 72: 7,
    # 73: 8,
    # 75: 10,
    # 118: 25,
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


id_task_map = {id: task for task, id in task_id_map.items()}
# 每20个打个包
target = [_ for _ in range(31,51)]
# target = [_ for _ in range(51,71)]
# target = [_ for _ in range(71,91)]
# target = [_ for _ in range(91,109)]

target_map = {k: id_task_map[k] for k in target}

id_task_map = target_map
print(id_task_map.keys())
work_videos = [Video(id, task) for id, task in id_task_map.items()]



if __name__ == '__main__':
    print(id_task_map)