from selenium.webdriver.common.by import By

from YAutoFramework.YUtils.Logger.Ylogger import GlobalLogger, LogLevel
from YAutoFramework.YUtils.POM.Base.BaseObject import BaseObjectClass


class MuYuQueryPage(BaseObjectClass) :
	"""
	用于描述 木鱼查询页面 的类
	"""

	def __init__(self, driver) :
		"""
		初始化一个 木鱼查询页面 对象
		:param driver:  selenium web _driver
		"""
		super().__init__(driver)
		self._driver = driver
		self._url = 'http://cps-test.bchrt.com/'
		self.__init_PageElements()

	def __init_PageElements(self) :
		"""
		初始化 木鱼查询页面 的页面元素
		:return:
		"""
		self.ClickToTestElement = BaseObjectClass(self._driver, (By.CSS_SELECTOR, 'button#start'), self)

	@GlobalLogger.log_decorator(level=LogLevel.DEBUG, message="打开页面")
	def open(self) :
		"""
		打开 木鱼查询页面
		:return: 木鱼查询页面
		"""
		self._driver.get(self._url)
		return self

	@GlobalLogger.log_decorator(level=LogLevel.DEBUG, message="关闭页面")
	def close(self) :
		"""
		关闭 木鱼查询页面
		:return: None
		"""
		self._driver.close()

	@GlobalLogger.log_decorator(level=LogLevel.DEBUG, message="进入上下文管理器")
	def __enter__(self) :
		"""
		进入上下文管理器时调用的方法，在此方法中调用 open 方法
		"""
		return self.open()

	@GlobalLogger.log_decorator(level=LogLevel.DEBUG, message="退出上下文管理器")
	def __exit__(self, exc_type, exc_val, exc_tb) -> bool :
		"""
		退出上下文管理器时调用的方法，在此方法中调用 close 方法
		"""
		if exc_type is not None :
			GlobalLogger.error(
					"意外发生了："
					f"异常类型：{exc_type}"
					f"异常值：{exc_val}"
					"追踪信息：",
					traceback.format_tb(exc_tb)
			)
		self.close()
		return True
