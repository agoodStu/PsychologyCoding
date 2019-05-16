# -*- coding: utf-8 -*-
"""
Created on Wed May  1 20:52:57 2019

@author: Yejishan
"""

"""
______        __   _______  ___ _____ _____ _   _  ___  _   _ 
| ___ \       \ \ / /  ___||_  |_   _/  ___| | | |/ _ \| \ | |
| |_/ /_   _   \ V /| |__    | | | | \ `--.| |_| / /_\ \  \| |
| ___ \ | | |   \ / |  __|   | | | |  `--. \  _  |  _  | . ` |
| |_/ / |_| |   | | | |__/\__/ /_| |_/\__/ / | | | | | | |\  |
\____/ \__, |   \_/ \____|____/ \___/\____/\_| |_|_| |_|_| \_/
        __/ |                                                 
       |___/                                                  
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
"""

file_src = r'E:\expdata\exp1\formal\test'
output_src = r'E:\expdata\exp1\formal\eyemoveConvert'
os.chdir(file_src)
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -  \
                    %(levelname)s - %(message)s')

def convert_to_pd(files):
    """
    用于将眼动文件转为pandas的DataFrame.

    :param file_list:待转换的眼动文件
    """
    with open(files) as f:
        data = f.read().split('\n')[6:]

    columns = data[0].split('\t')
    data_list = [i.split('\t') for i in data]

    df = pd.DataFrame(data_list[1:], columns=columns)
    df = df.drop(df[(df.GazePointXLeft.isnull()) | 
        (df.TimeStamp == 'TimeStamp')].index.tolist())
    df_convert = df.loc[:, columns[0:11]].astype(float)
    df['Event'] = df['Event'].replace('', np.nan)
    df_convert['Event'] = df['Event'].astype(float)

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


def data_process(df):
    """
    转为原点; 更改Event中trigger; 更改空值.

    :param df:转换后的dataframe
    """
    df['Event'] = df['Event'].fillna(method='ffill')
    df['Event'] = df['Event'].fillna('Event')

    df = df.drop(df[df.Event == 'Event'].index.tolist())
    df = df.drop(df[(df.Event == '1') | (df.Event == '0')].index.tolist())

    df.loc[:, ['GazePointXLeft', 'GazePointXRight', 'GazePointX']] = df.loc[:,
              ['GazePointXLeft', 'GazePointXRight', 'GazePointX']] + 960

    df.loc[:, ['GazePointYLeft', 'GazePointYRight', 'GazePointY']] = df.loc[:,
              ['GazePointYLeft', 'GazePointYRight', 'GazePointY']] + 540

    df = df.fillna(-1)

    return df


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


if __name__ == "__main__":
    main()
