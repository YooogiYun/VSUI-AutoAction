# __init__.py
# 定义定义模块级常量
import os

version = ''
driver_chrome_default: str = 'chrome'
implicit_wait_time: float = 10  # 隐式等待时间，单位：s
poll_frequency: float = 0.5  # 重试间隔时间，单位：s
implicit_retry_times: int = 3  # 重试次数，单位：次

# \\YAutoFramework
root_folder = os.path.abspath(os.path.dirname(__file__))  # 项目根目录
# \\YAutoFramework\Datain\
datain_folder = root_folder + os.sep + 'Datain' + os.sep  # 数据输入文件夹：用于放置测试数据，如测试用例说明，测试数据，测试配置等
# \\YAutoFramework\Dataout\
dataout_folder = root_folder + os.sep + 'Dataout' + os.sep  # 数据输出文件夹：用于保存测试结果及其他数据，如截图，日志等
