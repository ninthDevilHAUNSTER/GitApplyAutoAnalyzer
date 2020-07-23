data = {
    1: {},
    2: {},
    3: {},
    4: {},
    5: {},
    6: {},
    7: {},
    8: {},
    9: {},
    10: {},
    11: {},
    12: {},
    13: {},
    14: {},
    15: {},
    16: {},
    17: {},
    18: {},
    19: {},
    20: {},
    21: {},
    22: {},
    23: {},
    24: {},
    25: {},
    26: {},
    27: {},
    28: {},
    29: {},
    30: {},
    31: {},
    32: {},
    33: {},
    34: {},
    35: {},
    36: {},
    37: {},
    38: {},
    39: {},
    40: {},
    41: {},
    42: {},
    43: {},
    44: {},
    45: {},
    46: {},
    47: {},
    48: {},
    49: {},
    50: {},
    51: {},
    52: {},
    53: {},
    54: {},
    55: {},
}

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
import os

def find_cms_url(wd, cms_name):
    time.sleep(random.randint(SLEEP_TIME_MIN, SLEEP_TIME_MAX))
    wd.get("https://github.com/search?q={}&l=PHP&type=Repositories".format(cms_name))
    href = wd.find_element_by_xpath(
        '//*[@id="js-pjax-container"]/div/div[3]/div/ul/li[1]/div[2]/div[1]/a').get_attribute('href')
    return href


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


def find_patch_version_header(wd, version_number, cms_url):
    time.sleep(random.randint(SLEEP_TIME_MIN, SLEEP_TIME_MAX))
    wd.get("{}/releases/tag/{}".format(cms_url, version_number))
    try:
        version_header = wd.find_element_by_xpath(
            '/html/body/div[4]/div/main/div[2]/div/div[2]/div/div[1]/ul/li[2]/a/code'
        ).get_attribute('innerHTML')
    except:
        return "Not Found!"
    print(version_header)
    return version_header


import pandas as pd
import numpy as np

if __name__ == '__main__':
    wd = webdriver.Firefox()
    df = pd.read_csv('data4.csv')
    df['version_header_sha'] = df.apply(
        lambda x: find_patch_version_header(wd=wd, version_number=x['version_header'], cms_url=x['cms_url']),
        axis=1
    )
    wd.close()
    df.to_csv('data5.csv')

# df ['sum_value'] = df.apply(lambda x: sum_test(x['列名1']，x['列名2'])， axis=1)
