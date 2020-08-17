import pandas as pd
import numpy as np
from selenium import webdriver as wd
import random
import time

from config.config import *
from config.git_apply_res import *
import os


def _concat_result(cve_id, patch_commit_id, cms_url, fast_command, version_header):
    if version_header.__str__() == "nan": return "error:git version not found"
    cve_id = cve_id.replace("/", "_")
    version_header = version_header.replace("/", "_")

    # print(cve_id)
    # print(patch_commit_id)
    res_dir_path = os.path.join(GIT_APPLY_RES_DIR,
                                "{cve_id}-{patch_commit_id}".format(cve_id=cve_id, patch_commit_id=patch_commit_id))
    res_file_path = os.path.join(res_dir_path, "res_{}.txt".format(version_header))
    with open(res_file_path, 'r', encoding='utf8') as f:
        content = f.read()
        for x in GIT_APPLY_FAIL_LIST:
            if x in content:
                return GIT_APPLY_RES[x]
        if "warn" in content:
            return "success:with warning"
    return "success:clearly"


def concat_result(df):
    df['reason'] = df.apply(
        lambda x: _concat_result(x['cve_id'], x['patch_commit_id'], x['cms_url'], x['fast_command'],
                                 x['version_header']), axis=1
    )
    df['isfail'] = df['reason'].apply(
        lambda x: 1 if x is None or "error" in x else 0
    )
    return df

