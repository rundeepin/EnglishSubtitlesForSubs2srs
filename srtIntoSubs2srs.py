#!python3
# -*- coding:utf8 -*-
# Author: Rundeepin
# Contact: alicecui.ac@gmail.com

from typing import List
from tkinter import filedialog
import os
import ntpath


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


def merge_line(subtitle):
    index = 0
    while index < len(subtitle) - 1:
        if any(c.isalpha() for c in subtitle[index]):
            if any(c.isalpha() for c in subtitle[index + 1]):
                subtitle[index] += ' ' + subtitle[index + 1]
                subtitle.pop(index + 1)
        index += 1


def is_1time_1line(subtitle):
    index = 0
    while index < len(subtitle):
        if len(subtitle[index]) == 2:
            index += 2
        else:
            return False
    return True


def merge_subtitle(raw_data):
    subtitle = select_subtitle(raw_data)
    while True:
        if is_1time_1line(subtitle):
            break
        else:
            merge_line(subtitle)
    return subtitle

print("请选择utf-8格式的srt >>>")
TextPath = filedialog.askopenfilename(filetypes=[('srt file','*.srt')])
filename = os.path.basename(TextPath)

with open(TextPath, 'r', encoding='utf-8') as file:
    raw_data = file.readlines()

data = merge_subtitle(raw_data)

# print(data)


index = 1
while index < len(data):
    if data[index][0] == '(' and data[index][-1] == ')':
        del data[index]
        del data[index-1]
    else:
        # if ' ' in data[index]:
        #     data[index].replace('  ',' ')
        index += 2


def start_merge(data):
    index = 3
    while index < len(data):
        if data[index][0].islower():
            data[index - 2] += ' ' + data[index]
            del data[index - 3][1]
            data[index - 3].append(data[index - 1][1])
            del data[index]
            del data[index - 1]
        else:
            index += 2
    return data


def end_merge(data):
    index = 1
    while index < len(data):
        if data[index][-1:-3] == '...' or data[index][-1].islower() or data[index][-1] == ',':
            data[index] += ' ' + data[index + 2]
            del data[index - 1][1]
            data[index - 1].append(data[index + 1][1])
            del data[index + 2]
            del data[index + 1]
        else:
            index += 2
    return data


subtitle = end_merge(start_merge(end_merge(start_merge(data))))

# print(subtitle)


subtitleOut = open(filename+'_Final.srt', 'w', encoding="utf-8")

list_num = 1
i = 0
while i < len(subtitle) - 1:
    subtitleOut.write(str(list_num) + '\n')
    subtitleOut.write(subtitle[i][0] + ' --> ' + subtitle[i][1] + '\n')
    subtitleOut.write(subtitle[i + 1] + '\n\n')
    i += 2
    list_num += 1

subtitleOut.close()

print('finished')
