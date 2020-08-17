import pandas as pd
import numpy as np
from selenium import webdriver as wd
import random
import time

from config.config import *
from config.git_apply_res import *
import os


def multiversion_concat(df):
    gdf = df.groupby('cve_id')

    result_df = None
    for name, group in gdf:
        group_inner_index = 0
        for row, data in group.iterrows():
            group_inner_index+=1
            tmp_df = pd.DataFrame(data).T

            if tmp_df['isfail'].values[0] == 1:
                if result_df is None:
                    result_df = tmp_df
                else:
                    result_df = pd.concat(
                        [result_df, tmp_df], axis=0)
                break
            else:
                if group_inner_index == group.__len__():
                    if result_df is None:
                        result_df = tmp_df
                    else:
                        result_df = pd.concat(
                            [result_df, tmp_df], axis=0)
    return result_df


def version_mannual_input():
    # wd = webdriver.Firefox()
    df = pd.read_csv('../data/data6_updating.csv')
    result_df = None
    for i in range(0, df.__len__()):
        single_df = df.loc[i:i]
        cms_url = single_df['cms_url'].to_list()[0]
        if result_df is None:
            result_df = multiversion_concat(single_df)
        else:
            result_df = pd.concat(
                [result_df, multiversion_concat(single_df)], axis=0)
    os.chdir(r"D:\python_box\GitApplyAutoAnalyzer\base")
    result_df.to_csv('data6_updating.csv')


#
# if __name__ == '__main__':
#     df = pd.read_csv('../data/data6_multiversion.csv')
#     gdf = df.groupby('cve_id')
#
#     result_df = None
#     for name, group in gdf:
#         group_inner_index = 0
#         print(group.__len__())
#         for row, data in group.iterrows():
#             group_inner_index+=1
#             tmp_df = pd.DataFrame(data).T
#
#             if tmp_df['isfail'].values[0] == 1:
#                 if result_df is None:
#                     result_df = tmp_df
#                 else:
#                     result_df = pd.concat(
#                         [result_df, tmp_df], axis=0)
#                 break
#             else:
#                 if group_inner_index == group.__len__():
#                     if result_df is None:
#                         result_df = tmp_df
#                     else:
#                         result_df = pd.concat(
#                             [result_df, tmp_df], axis=0)
#
#     result_df.to_csv('data7_final.csv')
#     #     single_df = _df[0]
#     # print(result_df)
