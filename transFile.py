# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 15:49:27 2022

@author: Ye JiShan

为了不手动转移文件，没有执行顺序，可以参考os用法
"""

import os
import shutil


# 转移脑电文件
# eeg_path = r'F:\Ye\data\adhd\eeg'
# eeg_out_path = r'F:\Ye\eeg_script\data\Lissajous'

# sub_list = []
# for root, dirs, files in os.walk(eeg_path):
#     for file in files:
#         prefix = int(file[:3])
#         sub_list.append(prefix)
        
#         if file.split('.cdt')[0][-1] != '2':
#             fix_orgin_path = os.path.join(eeg_path, file)
#             fix_out_path = os.path.join(eeg_out_path, 'sub' + str(prefix),
#                                         'eeg', file)
#             shutil.copyfile(fix_orgin_path, fix_out_path)


# 创建文件夹
# e.g. F:\sub1
#           \eeg
#           \eye            
# data_path = r'F:\Ye\eeg_script\data\fixation'         
# create_files = set(sub_list)
# # create_files = [1]  # test
# for i in create_files:
#     out_path = os.path.join(data_path, 'sub' + str(i))
#     if not os.path.exists(out_path):
#         os.mkdir(out_path)
#     if os.path.exists(out_path):
#         eeg_path = os.path.join(out_path, 'eeg')
#         eye_path = os.path.join(out_path, 'eye')
#         if not os.path.exists(eeg_path):
#             os.mkdir(eeg_path)
#         if not os.path.exists(eye_path):
#             os.mkdir(eye_path)
            

# 转移眼动文件

eye_path = r'F:\Ye\data\adhd\eyeData\Lissajous'
eye_out_path = r'F:\Ye\eeg_script\data\Lissajous'


for root, dirs, files in os.walk(eye_path):
    for file in files:
        if file.split('.')[-1] == 'asc':
            sub = int(file[:2])
            prefix = file.split('.')[0]
            file_path = os.path.join(eye_path, prefix, file)
            file_out_path = os.path.join(eye_out_path, 'sub' + str(sub),
                                         'eye' ,file)
            
            shutil.copy(file_path, file_out_path)
