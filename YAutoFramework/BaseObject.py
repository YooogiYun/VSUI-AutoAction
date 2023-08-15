# typing.Optional[float]
# import typing

from selenium.common import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import YAutoFramework
from YAutoFramework.YUtils.YTestInfo import YTestInfo
from YAutoFramework.YUtils.Ylogger import Ylogger


class BaseObject(object) :
	def __init__(self, driver: WebDriver = None) :
		self.driver = YAutoFramework.driver_chrome_default if driver is None else driver
		self.locator = None
		self.timeout = YAutoFramework.implicit_wait_time
		self.poll_frequency = YAutoFramework.poll_frequency
		self.parent = None
		self.children = []
		self.is_displayed = False
		self.is_enabled = False
		self.text = None
		self.tag = None
		self.attributes = { }
		self.css = { }
		self.url = None
		self.title = None
		self.size = None
		self.location = None
		self.screenshot = None

	@YTestInfo.Tester('hello')
	@Ylogger.debug('hello')
	def wait_till_exist(self, timeout: float = None) -> bool :
		# 实现等待逻辑
		if timeout is None :
			# 如果未传入 timeout 参数，执行默认的等待逻辑
			timeout = self.timeout
			print(f"等待逻辑（默认超时时间：{timeout}）")
		else :
			# 如果传入了 timeout 参数，执行自定义的等待逻辑
			print(f"等待逻辑（超时时间：{timeout}）")
		try :
			# 实现等待逻辑，假设使用 self.driver.find_element 来查找元素
			(WebDriverWait(self.driver, timeout, self.poll_frequency)
			 .until(EC.presence_of_element_located(self.locator)))
			return True
		except TimeoutException as exp :

			return False
