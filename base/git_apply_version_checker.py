import pandas as pd
import numpy as np

pd.set_option('mode.chained_assignment', None)
from selenium import webdriver


def gen_dict_data():
    for i in range(1, 56):
        print("{} : ".format(i) + "{" + """
        'cms_name':'',
        'cms_url':'',
        'version_header':'',
        'patch_commit_id':'',
        'patch_commit_parent_id':'',
        'sink_file':'',
        """ + "},")


GITHUB_URL = "https://github.com/"
SLEEP_TIME_MIN = 10
SLEEP_TIME_MAX = 15
import time
import random


def input_version_header(cms_url, single_df):
    os.chdir(r"D:\php_box\safe_patch_git_apply_check_2")
    file_name = cms_url.split('/')[-1]
    result_df = single_df
    flag = True
    if os.path.exists(file_name) and os.path.isdir(file_name):
        os.chdir(r"D:\php_box\safe_patch_git_apply_check_2\{}".format(file_name))
        r = os.popen("git tag")
        text = r.read()
        r.close()
        print(file_name)
        print(text)
        try:
            tag_list = text.split('\n')
        except:
            print("tag is None")
            return single_df

        print("input test_version :: put # to finish")
        s = input(">>")
        while s != '#':
            if s not in tag_list:
                print("not tag ")
            else:
                tmp_df = single_df.copy()
                tmp_df['version_header'] = s
                if flag:
                    result_df = tmp_df
                    flag = not flag
                else:
                    result_df = pd.concat([result_df, tmp_df], axis=0)
            print("input test_version :: put # to finish")
            s = input(">>")
    else:
        print("File not found -==> {}".format(file_name))
    os.chdir(r"D:\python_box\PHPSinkPointAnalyzer\tools")
    return result_df


import os, sys


def download_git(cms_url):
    os.chdir(r"D:\php_box\safe_patch_git_apply_check_2")
    file_name = cms_url.split('/')[-1]
    if os.path.exists(file_name) and os.path.isdir(file_name):
        pass
    else:
        os.system(
            "git clone {cms_url}.git".format(cms_url=cms_url)
        )
    os.chdir(r"D:\python_box\PHPSinkPointAnalyzer\tools")


if __name__ == '__main__':
    # wd = webdriver.Firefox()
    df = pd.read_csv('data3.csv')
    result_df = None
    for i in range(0, df.__len__()):
        single_df = df.loc[i:i]
        cms_url = single_df['cms_url'].to_list()[0]
        if result_df is None:
            result_df = input_version_header(cms_url, single_df)
        else:
            result_df = pd.concat(
                [result_df, input_version_header(cms_url, single_df)], axis=0)
    result_df.to_csv('data4.csv')
