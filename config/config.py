DATASET_HEADER = "cve_id,cms_name,version_range,commit_url,patch_commit_parent_id,patch_commit_id,sink_file,version_header_sha,reason,pic,fast_command,isfail,cms_url,version_header".split(
    ",")
GITHUB_URL = "https://github.com"

SLEEP_TIME_MIN = 10
SLEEP_TIME_MAX = 15

GIT_DIFF_APPLY_CMD = "git diff {p_c_id} {c_id} {f} > 1.patch && git reset --hard {v} &&  git apply --reject 1.patch"
GIT_APPLY_RES_DIR = r"D:\python_box\GitApplyAutoAnalyzer\data\res"

DATASET_GITFILE_DIR = r"D:\php_box\safe_patch_git_apply_check_2"
