#!python3
# -*- coding:utf8 -*-
# Author: Rundeepin
# Contact: alicecui.ac@gmail.com

from typing import List
from tkinter import filedialog
import os
import ntpath

# 选择时间轴和字幕正文
def select_subtitle(raw_data):
    data = []
    for line in raw_data:
        data.append(line.rstrip())
    subtitle = []
    index = 0
    while index < len(data):
        if '-->' in data[index]:
            timeline = data[index].split(' --> ')
            subtitle.append(timeline)
        if any(c.isalpha() for c in data[index]):
            subtitle.append(data[index])
        index += 1
    return subtitle

# 同一条时间轴内字幕拼成一行
def merge_line(subtitle):
    index = 0
    while index < len(subtitle) - 1:
        if any(c.isalpha() for c in subtitle[index]):
            if any(c.isalpha() for c in subtitle[index + 1]):
                subtitle[index] += ' ' + subtitle[index + 1]
                subtitle.pop(index + 1)
        index += 1

# 判断是不是一条字幕一行
def is_1time_1line(subtitle):
    index = 0
    while index < len(subtitle):
        if len(subtitle[index]) == 2:
            index += 2
        else:
            return False
    return True

# 以上三个函数合并使用得到初始字幕
def merge_subtitle(raw_data):
    subtitle = select_subtitle(raw_data)
    while True:
        if is_1time_1line(subtitle):
            break
        else:
            merge_line(subtitle)
    return subtitle

# 处理句首字母小写的句子
def start_merge(data):
    index = 3
    while index < len(data) - 1:
        if data[index][0].islower():
            data[index - 2] += ' ' + data[index]
            del data[index - 3][1]
            data[index - 3].append(data[index - 1][1])
            del data[index]
            del data[index - 1]
        else:
            index += 2
    return data

# 处理句末是逗号或者小写字母无标点的句子
def end_merge(data):
    index = 1
    while index < len(data) - 1:
        if data[index][-1].islower() or data[index][-1] == ',':
            data[index] += ' ' + data[index + 2]
            del data[index - 1][1]
            data[index - 1].append(data[index + 1][1])
            del data[index + 2]
            del data[index + 1]
        else:
            index += 2
    return data



print("请选择utf-8格式的srt >>>")
TextPath = filedialog.askopenfilename(filetypes=[('srt file','*.srt')])
filename = os.path.basename(TextPath)

with open(TextPath, 'r', encoding='utf-8') as file:
    raw_data = file.readlines()

data = merge_subtitle(raw_data)

# 删除只有括号说明文本的字幕，经测试不能全部删掉，留有少量。
# 待修订
index = 1
while index < len(data):
    if data[index][0] == '(' and data[index][-1] == ')':
        del data[index]
        del data[index-1]
    else:
        index += 2

# 不同时间轴字幕拼合
subtitle = end_merge(start_merge(end_merge(start_merge(data))))

# 写出到结果
subtitleOutput = open(filename+'_Final.srt', 'w', encoding="utf-8")
list_num = 1
i = 0
while i < len(subtitle) - 1:
    subtitleOutput.write(str(list_num) + '\n')
    subtitleOutput.write(subtitle[i][0] + ' --> ' + subtitle[i][1] + '\n')
    subtitleOutput.write(subtitle[i + 1] + '\n\n')
    i += 2
    list_num += 1
subtitleOutput.close()

print('finished')
