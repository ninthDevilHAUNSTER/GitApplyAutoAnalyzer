import pandas as pd
import numpy as np
from selenium import webdriver as wd
import random
import time

from config.config import *
import os


def get_patch_commit_id(string: str) -> str:
    # print(string)
    if "#" in string:
        string = string.split('#')[0]
    return string.split("/")[-1]


def get_cms_url(url: str) -> str:
    _ = url.split('/')
    return "{}/{}/{}".format(GITHUB_URL, _[3], _[4])


def find_patch_commit_parent(wd, patch_commit_id, cms_url):
    time.sleep(random.randint(SLEEP_TIME_MIN, SLEEP_TIME_MAX))
    wd.get("{}/commit/{}".format(cms_url, patch_commit_id))
    try:
        href = wd.find_element_by_class_name('sha').get_attribute('href')
        href = href.split('/')[-1]
    except:
        href = "Not Found !"
    print(href)
    return href


def input_version_header(cms_url, single_df):
    os.chdir(r"D:\php_box\safe_patch_git_apply_check_2")
    file_name = cms_url.split('/')[-1]
    result_df = single_df
    flag = True
    if os.path.exists(file_name) and os.path.isdir(file_name):
        os.chdir(r"D:\php_box\safe_patch_git_apply_check_2\{}".format(file_name))
        apply_version = single_df['version_range'].to_list()[0].__str__()
        print(apply_version)
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
        if apply_version in tag_list:
            tmp_df = single_df.copy()
            tmp_df['version_header'] = apply_version
            os.chdir(r"D:\python_box\PHPSinkPointAnalyzer\tools")
            return tmp_df
        else:
            print("input test_version :: put * to finish")
            s = input(">>")
        while s != '*':
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
            print("input test_version :: put * to finish")
            s = input(">>")
    else:
        print("File not found -==> {}".format(file_name))
    os.chdir(r"D:\python_box\PHPSinkPointAnalyzer\tools")
    return result_df


def version_mannual_input():
    # wd = webdriver.Firefox()
    df = pd.read_csv('../data/data6_updating.csv')
    result_df = None
    for i in range(0, df.__len__()):
        single_df = df.loc[i:i]
        cms_url = single_df['cms_url'].to_list()[0]
        if result_df is None:
            result_df = input_version_header(cms_url, single_df)
        else:
            result_df = pd.concat(
                [result_df, input_version_header(cms_url, single_df)], axis=0)
    os.chdir(r"D:\python_box\GitApplyAutoAnalyzer\base")
    result_df.to_csv('data6_updating.csv')


def get_fast_command(patch_commit_parent_id, patch_commit_id, sink_file, version_header):
    '''
    df = pd.read_csv('../data/___data6.csv')
    df['fast_command'] = df.apply(
        lambda x: get_fast_command(x['patch_commit_parent_id'], x['patch_commit_id'], x['sink_file'],
                                   x['version_header']), axis=1
    )
    df.to_csv('data6_updating.csv')
    :param patch_commit_parent_id:
    :param patch_commit_id:
    :param sink_file:
    :param version_header:
    :return:
    '''
    return GIT_DIFF_APPLY_CMD.format(
        p_c_id=patch_commit_parent_id, c_id=patch_commit_id, f="", v=version_header
    )

from subprocess import *

def get_git_apply_res(cve_id, patch_commit_id, cms_url, fast_command, version_header):
    if version_header.__str__() == "nan": return

    os.chdir(DATASET_GITFILE_DIR)
    file_name = cms_url.split('/')[-1]
    if os.path.exists(file_name) and os.path.isdir(file_name):
        res_dir_path = os.path.join(GIT_APPLY_RES,
                                    "{cve_id}-{patch_commit_id}".format(cve_id=cve_id, patch_commit_id=patch_commit_id))
        if not os.path.exists(res_dir_path): os.mkdir(res_dir_path)
        res_file_path = os.path.join(res_dir_path, "res_{}.txt".format(version_header))
        git_dir_path = os.path.join(DATASET_GITFILE_DIR, file_name)
        os.chdir(git_dir_path)
        p = Popen(fast_command, shell=True, stdout=PIPE, stderr=STDOUT, close_fds=True)
        text = p.stdout.read()
        f = open(res_file_path, 'wb')
        f.write(text)
        f.close()
    else:
        print("error::{}".format(cve_id))
    os.chdir(r"D:\python_box\PHPSinkPointAnalyzer\tools")


if __name__ == '__main__':
    df = pd.read_csv('../data/data6_updating.csv')
    df.apply(
        lambda x: get_git_apply_res(x['cve_id'], x['patch_commit_id'], x['cms_url'], x['fast_command'],
                                    x['version_header']), axis=1
    )

