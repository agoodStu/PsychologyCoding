# -*- coding: utf-8 -*-
"""
Created on Wed May  1 20:52:57 2019

@author: Ye
"""


import os
import pandas as pd
import numpy as np
import logging


"""
目的分析：
1. 由于眼动程序生成的文件格式是tsv (tobii支持)，为了excel处理方便
   在源代码中改成了xls，但excel不能正常打开，所以不能直接使用pandas。
   解决思路：通过with open打开，通过数据格式处理，转为pandas支持的数据框。
2. 输出的眼动文件中，以屏幕中心为0点。但为了方便计算，需要改成以左上角为0点。
   解决思路：显示器分辨率为1920*1080，因此，x + 960, y + 540
3. 在Event列，输出的眼动文件中，只在每一事件开始时的一行写triiger。为了后续
   分析方面，需要连续写入相同triiger，直到该事件结束。
   解决思路：
       1) 使用fillna(method='ffill')，以前一个trigger为准，填充空值
       2) 使用fillna('Event')填充其他空值
4. 原眼动文件中空值的标记方式是"np.nan",为了方便后续在matlab中计算眼动，需改成"-1"
   解决思路：在Event列处理完成后通过fillna(-1)实现
5. 删除特定行，如Event==1, Event=='Event'等
   解决思路：获取特定行的index，使用tolist()转为列表，通过drop()删除
6. 将TimeStamp列时间递增。即第二个试次的开始时间为第一个试次的结束时间。
"""

file_src = r'E:\expdata\exp1\formal\test'
output_src = r'E:\expdata\exp1\formal\eyemoveConvert'
os.chdir(file_src)
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -  \
                    %(levelname)s - %(message)s')


def convert_to_pd(files):
    """
    input
    -----
    用于将眼动文件转为pandas的DataFrame.

    :param file_list:待转换的眼动文件
    
    return
    ------
    转换后的文件
    """
    with open(files) as f:
        data = f.read().split('\n')[6:]

    columns = data[0].split('\t')
    data_list = [i.split('\t') for i in data]

    # 对df赋值
    df = pd.DataFrame(data_list[1:], columns=columns)
    
    # trial的计算：因为每个试次时分开写入，所以其中都会包含"TimeStamp"行
    # 以及"Session End"行
    # 因此，将"TimeStamp"和"Session End"中间的数据记为一个试次
    # 在新添trial列
    df['Trial'] = np.nan
    # 试次开始行index    
    time_loc = df['TimeStamp'].loc[df['TimeStamp'] == 'TimeStamp'].index
    # 试次结束行index
    sessi_end = df['TimeStamp'].loc[df['TimeStamp'] == 'Session End'].index
    # 因为第一行数据是数据，所以插入0
    time_loc = time_loc.insert(0, 0)
    block_loc = list(zip(time_loc, sessi_end))
    
    n = 1
    for i in block_loc:
        df['Trial'].iloc[i[0]: i[1]] = n
        n = n + 1

    df = df.drop(df[(df.GazePointXLeft.isnull()) |
        (df.TimeStamp == 'TimeStamp') |
        (df.GazePointXLeft == '')].index.tolist())
    df_convert = df.loc[:, columns[0:11]].astype(float)
    df['Event'] = df['Event'].replace('', np.nan)
    df_convert['Event'] = df['Event'].astype(float)
    df_convert['Trial'] = df['Trial'].astype(float)

    return df_convert


def get_file_list(file_src):
    """
    获取待处理的文件名称.

    :param files_src: 输入路径
    """
    file_lists = []
    for foldername, subfolders, folders in os.walk(file_src):
        for i in folders:
            if i.endswith('xls'):
                file_lists.append(i)

    return file_lists


def data_process(df_convert):
    """
    转为原点; 更改Event中trigger; 更改空值; 
    转换为连续时间

    :param df_convert:转换后的dataframe
    """
    
    # 获取trial
    trail_lists = df_convert['Trial'].unique()
    
    # 刚跟不同trial块填充试次    
    for i in trail_lists:
        df_convert['Event'].loc[df_convert['Trial'] == i] \
        = df_convert['Event'].loc[df_convert['Trial'] == i].fillna(method='ffill')
    
    # 删除不需要的行    
    df_convert['Event'] = df_convert['Event'].fillna('Event')
    df_convert = df_convert.drop(df_convert[df_convert.Event == 'Event'].index.tolist())
    df_convert = df_convert.drop(df_convert[(df_convert.Event == 1) | 
            (df_convert.Event == 0) | (df_convert.TimeStamp < 0)].index.tolist())
    df_convert = df_convert.drop(df_convert[(df_convert.Event == 33330) | (df_convert.Event == 33331)
            | (df_convert.Event == 33332) | (df_convert.Event == 33333)].index.tolist())
    
    # 转为以左上角为0点    
    df_convert.loc[:, ['GazePointXLeft', 'GazePointXRight', 'GazePointX']] = df_convert.loc[:,
                  ['GazePointXLeft', 'GazePointXRight', 'GazePointX']] + 960
    df_convert.loc[:, ['GazePointYLeft', 'GazePointYRight', 'GazePointY']] = df_convert.loc[:,
                  ['GazePointYLeft', 'GazePointYRight', 'GazePointY']] + 540

    # 填充空值
    df_convert.fillna(-1, inplace=True)    
    
    # 重置index
    df_convert.reset_index(inplace=True, drop=True)
    
    # 获取新的trial(删除了填充试次)
    new_trial_lists = df_convert['Trial'].unique()
    # 根据试次累加时间
    for i in new_trial_lists[1:]:
        last_trial_index = df_convert['TimeStamp'].loc[df_convert['Trial'] == i].index[0]-1
        last_trial_endtime = df_convert['TimeStamp'].iloc[last_trial_index]
        df_convert['TimeStamp'].loc[df_convert['Trial'] == i] \
        = df_convert['TimeStamp'].loc[df_convert['Trial'] == i] + last_trial_endtime
    
    return df_convert

    
def main():
    file_lists = get_file_list(file_src)
    try:
        for i in file_lists:
            file_name = i.split('.')[0] + '_convert.xlsx'
            df_convert = convert_to_pd(i)
            df_out = data_process(df_convert)
            df_out.to_excel(output_src + os.sep + file_name, index=False)
            logging.debug(i.split('.')[0] + ' is converted!')
    except:
        logging.debug(i.split('.')[0] + ' has some problems!')


if __name__ == '__main__':
    main()