# 正则逻辑：
# 查不到错误就是成功的

# 设定查找优先度
GIT_APPLY_FAIL_LIST = ["bad object", "No such file or directory",
                       "error: patch failed", "Rejected hunk"
                       ]
GIT_APPLY_RES = {
    "error: patch failed": "error:Code Conflict",
    "Rejected hunk": "error:Code Conflict",
    "No such file or directory": "error:File not found in low version",
    "bad object": "error:bad object"
}
