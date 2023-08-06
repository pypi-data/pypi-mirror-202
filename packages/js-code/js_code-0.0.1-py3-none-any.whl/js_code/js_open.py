from functools import partial  # 锁定参数
import subprocess

# 防止乱码
subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
import execjs


def js_lead_into(file, mode="r", encoding="utf-8"):
    """
    :param file: 需要手动添加文件路径，或者javascript的代码格式(function fn(){return xxx;};
    有条件判断增加相应的条件判断，或者循环)
    :param mode: 默认 r读取 只需要读取 不需要写入
    :param encoding: 默认utf-8
    """
    try:
        # 读取javascript 代码
        with open(file, mode=mode, encoding=encoding) as f:
            js_code = f.read()
            # 加载 javascript 代码
        js = execjs.compile(js_code)
    except:
        # 做一个适配同时兼容 javascript 代码 不用读出javascript代码文件
        js = execjs.compile(file)
    return js
