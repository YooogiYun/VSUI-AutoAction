import selenium
from selenium.webdriver.remote.webdriver import WebDriver

# __init__.py
# 定义全局常量

version = ''
driver_chrome_default: WebDriver = selenium.webdriver.Chrome()
implicit_wait_time: float = 10  # 隐式等待时间, 单位: s
poll_frequency: float = 0.5  # 重试间隔时间, 单位: s
implicit_retry_times: int = 3  # 重试次数,    单位: 次
