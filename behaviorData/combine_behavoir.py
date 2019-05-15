# -*- coding: utf-8 -*-
"""
Created on Sat May 11 15:21:04 2019

@author: Ye
合并每个被试的行为数据，即8个block合并为一组
"""
import pandas as pd
import os
import logging


logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -  \
                    %(levelname)s - %(message)s')
file_src = r'E:\expdata\exp1\formal\behavior'
output_src = ''
os.chdir(file_src)


def get_file_list(file_src):
    """
    获取待处理的文件名称.

    :param files_src: 输入路径
    """
    file_lists = []
    for foldername, subfolders, folders in os.walk(file_src):
        for i in folders:
            if i.endswith('csv'):
                file_lists.append(i)

    return file_lists


def generate_df(file):
    """
    生成汇总列表.

    :param file: 待处理文件
    """
    df2 = pd.DataFrame()
    df = pd.read_csv(file)[3:]

    df2['participant'] = df['participant']
    df2['block'] = pd.Series([int(file.split('_')[1][0])] * 69)
    df2['correct'] = df['main_resp.corr']
    df2['secResp'] = df['sec_resp.corr']
    df2['rt'] = df['main_resp.rt']
    df2['trigger'] = df['trigger']

    return df2


def main():
    df_out = pd.DataFrame(columns=['participant', 'block', 'correct',
                                   'secResp', 'rt', 'trigger'])

    file_lists = get_file_list(file_src)
    for i in file_lists:
        df = generate_df(i)
        df_out = pd.concat([df_out, df])
        logging.debug(i + ' is finished!')

    df_out.to_excel('total.xlsx', index=False,)


if __name__ == '__main__':
    main()
