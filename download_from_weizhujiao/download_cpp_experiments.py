import requests

import json
import time

headers = {
    "User-Agent": "your_user_agent",
    "cookie": "your_cookie",
    "authorization": "your_authorization"
}

student_class_map = {
    # 因为同学们填写的班级可能格式不同
    "张三": "计算机2301班",
}
print(len(student_class_map))


def get_filename(student_id, student_name, task_num, submit_time, filetype):
    classname = student_class_map.get(student_name)
    return f"{classname}_{student_id}_{student_name}_{task_num}_{submit_time}.{filetype}"


from datetime import datetime

task_map = {
    1: "某次作业的id",
}

for task_id, task_url in task_map.items():
    url = f"https://www.teachermate.com.cn/api/v1/homework/{task_url}/result"
    response = requests.get(url, headers=headers)
    time.sleep(0.1)
    response.encoding = "utf-8"
    result = response.text
    result = json.loads(result)
    students = result["students"]
    for student in students:
        student_name = student["name"]
        student_id = student["studentNumber"]
        homework = student.get("homework")
        if homework is None:
            print(f"{student_name}没交实验{task_id}！")
            continue

        homework_id = homework["id"]
        detail_url = f"https://www.teachermate.com.cn/api/v1/homework/{task_url}/student-homework/{homework_id}?studentId={student['id']}"
        response = requests.get(detail_url, headers=headers)
        time.sleep(0.1)

        response.encoding = "utf-8"
        result = response.text
        result = json.loads(result)
        homeworks = result.get("studentHomeworkHistory")
        if homeworks is None or len(homeworks) == 0:
            print(f"{student_name}没交实验{task_id}！")
            continue
        if len(homeworks) > 1:
            print(f"{student_name}交了多次实验{task_id}？？")
        for homework in homeworks:
            if homework.get("content"):
                print(student_name, ": ", homework.get("content"))

            appendix = homework.get("appendix")
            if appendix is None or len(appendix) == 0:
                print(f"{student_name}没交实验{task_id}！")
                continue
            elif len(appendix) > 1:
                print(f"{student_name}交了多个附件在实验{task_id}？？")
            time_str = homework["submitTime"]
            time_obj = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
            formatted_date = time_obj.strftime("%m%d")  # 输出 '1026'

            for app in appendix:
                type = app["type"]
                filename = get_filename(student_id, student_name, task_id, formatted_date, type)
                download_url = app["ossUrl"]
                response = requests.get(download_url, headers=headers)
                time.sleep(0.1)
                with open(filename, 'wb') as f:
                    f.write(response.content)
