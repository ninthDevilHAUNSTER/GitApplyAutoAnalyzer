import pandas as pd
import numpy as np
from selenium import webdriver as wd
import random
import time

from config.config import *
import os

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
    df = pd.read_csv('../data/data6_updating.csv', delimiter=",")
    df.apply(
        lambda x: download_git(x['cms_url']), axis=1
    )
