# typing.Optional[float]
# import typing
import selenium
from selenium.common import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

import YAutoFramework
from YAutoFramework.YUtils.Logger.Ylogger import GlobalLogger, LogLevel
from YAutoFramework.YUtils.POM.BaseObjectFuncs import BaseObjectFunctions
from YAutoFramework.YUtils.POM.BaseObjectFuncs import BaseSelectObjectFunctions
from YAutoFramework.YUtils.POM.BaseObjectFuncs import BaseTextObjectFunctions
from YAutoFramework.YUtils.POM.BaseObjectFuncs import BaseWebElementFunctions

MouseButtonDict = {
	"left"    : MouseButton.LEFT,
	"middle"  : MouseButton.MIDDLE,
	"right"   : MouseButton.RIGHT,
	"forward" : MouseButton.FORWARD,
	"back"    : MouseButton.BACK,
}


def parse_attributes(element_attributes) :
	"""
	解析元素属性
	:param element_attributes: 元素的属性字符串
	:return: 属性字典
	"""
	attributes = { }
	# 解析属性字符串为字典
	# 根据属性字符串的格式来解析，可以使用正则表达式或其他方法进行解析
	# 这里仅作示例，你可以根据实际的属性字符串格式进行解析
	# 假设属性字符串的格式为 key="value"，每个属性之间用空格分隔
	attribute_list = element_attributes.split(" ")
	for attribute in attribute_list :
		if "=" in attribute :
			key, value = attribute.split("=")
			key = key.strip()
			value = value.strip().strip("\"'")
			attributes[key] = value
	return attributes


class BaseObject(BaseObjectFunctions, BaseTextObjectFunctions, BaseSelectObjectFunctions, BaseWebElementFunctions) :
	"""
	POM 基础对象
	"""

	drivers_dict = {
		"chrome"  : selenium.webdriver.Chrome,
		"firefox" : selenium.webdriver.firefox,
		"edge"    : selenium.webdriver.edge,
		"ie"      : selenium.webdriver.ie,
		"safari"  : selenium.webdriver.safari,
	}

	def __init__(self, driver: WebDriver = None, locator: tuple[any, str] = None, parent = None) :
		self._driver = self.drivers_dict[YAutoFramework.driver_chrome_default]() if driver is None else driver
		self._locator = locator
		self._timeout = YAutoFramework.implicit_wait_time
		self._poll_frequency = YAutoFramework.poll_frequency
		self._parent = parent
		self._childrens = []
		self.is_displayed = self.exists
		self.is_enabled = self.__is_enabled
		self.text = self.get_text
		self.tag = self.get_tag
		self.attributes = self.get_attributes
		self.css = { }
		self.url = self._driver.current_url
		self.title = self._driver.title
		self.size = self.get_size
		self.location = self.get_location

	def __is_enabled(self) :
		"""
		判断元素是否可用
		:return: True if enabled else False
		"""
		return self.wait_till_enabled(timeout=1)

	# @GlobalLogger.log_decorator(level=LogLevel.DEBUG, message=f"判断 {self._locator} 元素是否存在")
	def exists(self) -> bool :
		"""
		判断元素是否存在
		:return: True if exists else False
		"""
		GlobalLogger.log(level=LogLevel.DEBUG, message=f"判断 {self._locator} 元素是否存在")
		try :
			self._driver.find_element(*self._locator)
			GlobalLogger.debug(f"元素 {self._locator} 存在")
			return True
		except Exception as e :
			GlobalLogger.error(f"元素 {self._locator} 不存在，error msg: {str(e)}")
			return False

	# @GlobalLogger.log_decorator(
	# 		level=LogLevel.DEBUG,
	# 		message=f"点击 {self._locator} 元素是否可见 >>> button_type: {button_type} >>> click_times: {click_times} 次"
	# )
	def click(self, button_type: str = "left", click_times: int = 1, interval: int = 125) -> bool :
		"""
		点击元素
		:param button_type: 鼠标按键类型，可选值：left、right、middle,forward,back, 默认为 left
		:param click_times: 点击次数，默认为 1
		:param interval: 点击间隔时间，默认为 125ms
		:return: True if click success else False
		"""
		GlobalLogger.log(
				level=LogLevel.DEBUG,
				message=f"点击 {self._locator} 元素是否可见 >>> button_type: {button_type} >>> click_times: {click_times} 次"
		)
		try :
			actions = ActionChains(self._driver)  # 鼠标操作对象
			element = self._driver.find_element(*self._locator)  # 元素
			button_ = MouseButtonDict[button_type]  # 鼠标按键类型
			interval = (interval if interval > 0 else 125) / 1000.0  # 间隔时间，单位：s
			if button_ is None :
				raise ValueError(f"Invalid button_type: {button_type}")

			actions.move_to_element(to_element=element)
			for _ in range(click_times) :
				(actions.w3c_actions.pointer_action
				 .pointer_down(button_)
				 .pointer_up(button_)
				 .pause(interval))
			actions.perform()
		except Exception as e :
			GlobalLogger.error(f"点击 {self._locator} 元素失败 >>> error: {str(e)}")
			return False
		else :
			GlobalLogger.info(f"点击 {self._locator} 元素成功")
			return True

	# @GlobalLogger.log_decorator(
	# 		level=LogLevel.DEBUG,
	# 		message="长按元素 {self._locator} >>> duration_time: {duration_time} ms >>> button_type: {button_type} >>> "
	# 		        "click_times: {click_times} 次"
	# )
	def long_click(
			self, button_type: str = "left", click_times: int = 1, duration_time: int = 250, interval: int = 125
	) -> bool :
		"""
		长按元素
		:param button_type:  鼠标按键类型，可选值：left、right、middle,forward,back, 默认为 left
		:param click_times:  点击次数，默认为 1
		:param duration_time: 长按时间，默认 250ms，单位：ms
		:param interval:     点击间隔时间，默认为 125ms
		:return : True if click success else False:
		"""
		GlobalLogger.log(
				level=LogLevel.DEBUG,
				message=f"长按元素 {self._locator} >>> duration_time: {duration_time} ms >>> button_type: {button_type} >>> "
				        "click_times: {click_times} 次"
		)
		try :
			actions = ActionChains(self._driver)
			element = self._driver.find_element(*self._locator)
			duration_time = (duration_time if duration_time > 0 else 250) / 1000.0  # 持续时间，单位：s
			interval = (interval if interval > 0 else 125) / 1000.0  # 间隔时间，单位：s
			button_ = MouseButtonDict[button_type]  # 鼠标按键类型
			if button_ is None :
				raise ValueError(f"Invalid button_type: {button_type}")

			actions.move_to_element(to_element=element)
			for _ in range(click_times) :
				(actions.w3c_actions.pointer_action
				 .pointer_down(button_)
				 .pause(duration_time)
				 .pointer_up(button_)
				 .pause(interval))
			actions.perform()
		# time.sleep(0.5)  # 添加适当的延迟，模拟多次点击的效果
		except Exception as e :
			GlobalLogger.error(f"长按 {self._locator} 元素失败 >>> error: {str(e)}")
			return False
		else :
			GlobalLogger.info(f"长按 {self._locator} 元素 {duration_time} s 成功")
			return True

	# @GlobalLogger.log_decorator(level=LogLevel.DEBUG, message=f"等待 {self._locator} 元素出现 >>> _timeout: {timeout}s")
	def wait_till_exists(self, timeout: float = None) -> bool :
		"""
		selenium 等待元素出现
		:param timeout: 超时时间，单位：s
		:return: True if element exists else False
		"""
		GlobalLogger.log(level=LogLevel.DEBUG, message=f"等待 {self._locator} 元素出现 >>> _timeout: {timeout}s")
		# 实现等待逻辑
		if timeout is None :
			# 如果未传入 _timeout 参数，执行默认的等待逻辑
			timeout = self._timeout
			GlobalLogger.info(f"等待逻辑（默认超时时间：{timeout}）")
		else :
			# 如果传入了 _timeout 参数，执行自定义的等待逻辑
			GlobalLogger.info(f"等待逻辑（超时时间：{timeout}）")
		try :
			# 实现等待逻辑，假设使用 self._driver.find_element 来查找元素
			(WebDriverWait(self._driver, timeout, self._poll_frequency)
			 .until(EC.presence_of_element_located(self._locator)))
			GlobalLogger.info(f"元素已出现：{self._locator}")
			return True
		except TimeoutException as exp :
			GlobalLogger.error(f"元素：{self._locator} 在 {timeout} s 内未找到，错误信息：{exp}")
			return False

	# @GlobalLogger.log_decorator(level=LogLevel.DEBUG, message=f"等待 {self._locator} 元素消失 >>> _timeout: {timeout}s")
	def wait_till_disappear(self, timeout: float = None) -> bool :
		"""
		等待元素消失
		:param timeout: 超时时间，单位：s
		:return: True if element disappear else False
		"""
		GlobalLogger.log(level=LogLevel.DEBUG, message=f"等待 {self._locator} 元素消失 >>> _timeout: {timeout}s")
		# 实现等待逻辑
		if timeout is None :
			# 如果未传入 _timeout 参数，执行默认的等待逻辑
			timeout = self._timeout
			GlobalLogger.info(f"等待逻辑（默认超时时间：{timeout}）")
		else :
			# 如果传入了 _timeout 参数，执行自定义的等待逻辑
			GlobalLogger.info(f"等待逻辑（超时时间：{timeout}）")
		try :
			# 实现等待逻辑，假设使用 self._driver.find_element 来查找元素
			(WebDriverWait(self._driver, timeout, self._poll_frequency)
			 .until_not(EC.presence_of_element_located(self._locator)))
			GlobalLogger.info(f"元素已消失：{self._locator}")
			return True
		except TimeoutException as exp :
			GlobalLogger.error(f"元素：{self._locator} 在 {timeout} s 内未消失，错误信息：{exp}")
			return False

	# @GlobalLogger.log_decorator(level=LogLevel.DEBUG, message=f"等待 {self._locator} 元素可见 >>> _timeout: {timeout}s")
	def wait_till_enabled(self, timeout: float = None) -> bool :
		"""
		等待元素可用
		:param timeout: 超时时间，单位：s
		:return: True if element enabled else False
		"""
		GlobalLogger.log(level=LogLevel.DEBUG, message=f"等待 {self._locator} 元素可见 >>> _timeout: {timeout}s")
		# 实现等待逻辑
		if timeout is None :
			# 如果未传入 _timeout 参数，执行默认的等待逻辑
			timeout = self._timeout
			GlobalLogger.info(f"等待逻辑（默认超时时间：{timeout}）")
		else :
			# 如果传入了 _timeout 参数，执行自定义的等待逻辑
			GlobalLogger.info(f"等待逻辑（超时时间：{timeout}）")
		try :
			# 实现等待逻辑，假设使用 self._driver.find_element 来查找元素
			(WebDriverWait(self._driver, timeout, self._poll_frequency)
			 .until(EC.element_to_be_clickable(self._locator)))
			GlobalLogger.info(f"元素已可用：{self._locator}")
			return True
		except TimeoutException as exp :
			GlobalLogger.error(f"元素：{self._locator} 在 {timeout} s 内未可用，错误信息：{exp}")
			return False

	# @GlobalLogger.log_decorator(
	# 		level=LogLevel.DEBUG, message=f"等待 {self._locator} 元素不可见 >>> _timeout: {timeout}s"
	# )
	def wait_till_disabled(self, timeout: float = None) -> bool :
		"""
		等待元素不可用
		:param timeout: 超时时间，单位：s
		:return: True if element disabled else False
		"""
		GlobalLogger.log(level=LogLevel.DEBUG, message=f"等待 {self._locator} 元素不可见 >>> _timeout: {timeout}s")
		# 实现等待逻辑
		if timeout is None :
			# 如果未传入 _timeout 参数，执行默认的等待逻辑
			timeout = self._timeout
			GlobalLogger.info(f"等待逻辑（默认超时时间：{timeout}）")
		else :
			# 如果传入了 _timeout 参数，执行自定义的等待逻辑
			GlobalLogger.info(f"等待逻辑（超时时间：{timeout}）")
		try :
			# 实现等待逻辑，假设使用 self._driver.find_element 来查找元素
			(WebDriverWait(self._driver, timeout, self._poll_frequency)
			 .until_not(EC.element_to_be_clickable(self._locator)))
			GlobalLogger.info(f"元素已不可用：{self._locator}")
			return True
		except TimeoutException as exp :
			GlobalLogger.error(f"元素：{self._locator} 在 {timeout} s 内未不可用，错误信息：{exp}")
			return False

	# @GlobalLogger.log_decorator(
	# 		level=LogLevel.DEBUG, message=f"等待 {self._locator} 元素可见、可用 >>> _timeout: {timeout}s"
	# )
	def wait_for_ready(self, timeout: float = None) -> bool :
		"""
		等待元素可见、可用
		:param timeout: 超时时间，单位：s
		:return:  True if element ready else False
		"""
		GlobalLogger.log(
				loglevel=LogLevel.DEBUG, message=f"等待 {self._locator} 元素可见、可用 >>> _timeout: {timeout}s"
		)
		# 实现等待逻辑
		if timeout is None :
			# 如果未传入 _timeout 参数，执行默认的等待逻辑
			timeout = self._timeout
			GlobalLogger.info(f"等待逻辑（默认超时时间：{timeout}）")
		else :
			# 如果传入了 _timeout 参数，执行自定义的等待逻辑
			GlobalLogger.info(f"等待逻辑（超时时间：{timeout}）")
		try :
			# 实现等待逻辑，假设使用 self._driver.find_element 来查找元素
			(WebDriverWait(self._driver, timeout, self._poll_frequency)
			 .until(EC.visibility_of_element_located(self._locator)))
			(WebDriverWait(self._driver, timeout, self._poll_frequency)
			 .until(EC.element_to_be_clickable(self._locator)))
			GlobalLogger.info(f"元素已可见、可用：{self._locator}")
			return True
		except TimeoutException as exp :
			GlobalLogger.error(f"元素：{self._locator} 在 {timeout} s 内未可见、可用，错误信息：{exp}")
			return False

	# @GlobalLogger.log_decorator(level=LogLevel.DEBUG, message=f"使 {self._locator} 元素滚动到可见区域")
	def scroll_into_view(self) -> bool :
		"""
		滚动到元素可见
		:return:  True if element scrolled else False
		"""
		GlobalLogger.log(level=LogLevel.DEBUG, message=f"使 {self._locator} 元素滚动到可见区域")
		try :
			# 实现滚动逻辑，假设使用 self._driver.execute_script 来滚动元素
			element = self._driver.find_element(*self._locator)
			self._driver.execute_script("arguments[0].scrollIntoView();", element)
			GlobalLogger.info(f"滚动到元素可见：{self._locator}")
			return True
		except Exception as exp :
			GlobalLogger.error(f"滚动到元素：{self._locator} 时出错，错误信息：{str(exp)}")
			return False

	# @GlobalLogger.log_decorator(level=LogLevel.DEBUG, message=f"获取元素：{self._locator} 文本：{text}")
	def get_text(self) -> str :
		"""
		获取元素文本
		:return: 元素文本 if success_get else ""
		"""
		GlobalLogger.log(level=LogLevel.DEBUG, message=f"获取元素：{self._locator} 文本：{text}")
		try :
			# 实现获取文本逻辑，假设使用 self._driver.find_element 来查找元素
			text = self._driver.find_element(*self._locator).text
			GlobalLogger.info(f"获取元素文本：{self._locator}，文本值：{text}")
			return text
		except Exception as exp :
			GlobalLogger.error(f"获取元素：{self._locator} 的文本时出错，错误信息：{str(exp)}")
			return ""

	# @GlobalLogger.log_decorator(level=LogLevel.DEBUG, message=f"清空元素：{self._locator} 文本")
	def clear_text(self) -> bool :
		"""
		清空元素文本
		:return:  True if element cleared else False
		"""
		GlobalLogger.log(level=LogLevel.DEBUG, message=f"清空元素：{self._locator} 文本")
		try :
			# 实现清空文本逻辑，假设使用 self._driver.find_element 来查找元素
			self._driver.find_element(*self._locator).clear()
			GlobalLogger.info(f"清空元素文本：{self._locator}")
			return True
		except Exception as exp :
			GlobalLogger.error(f"清空元素：{self._locator} 的文本时出错，错误信息：{str(exp)}")
			return False

	# @GlobalLogger.log_decorator(level=LogLevel.DEBUG, message=f"设置元素：{self._locator} 文本：{text}")
	def set_text(self, text: str) -> bool :
		"""
		设置元素文本
		:param text: 文本值
		:return: True if element set else False
		"""
		GlobalLogger.log(level=LogLevel.DEBUG, message=f"设置元素：{self._locator} 文本：{text}")
		try :
			# 实现设置文本逻辑，假设使用 self._driver.find_element 来查找元素
			element = self._driver.find_element(*self._locator)
			element.clear()
			element.send_keys(text)
			GlobalLogger.info(f"设置元素文本：{self._locator}，文本值：{text}")
			return True
		except Exception as exp :
			GlobalLogger.error(f"设置元素：{self._locator} 的文本时出错，错误信息：{str(exp)}")
			return False

	# @GlobalLogger.log_decorator(level=LogLevel.DEBUG, message=f"追加元素：{self._locator} 文本：{text}")
	def append_text(self, text: str) -> bool :
		"""
		追加元素文本
		:param text: 文本值
		:return: True if element appended else False
		"""
		GlobalLogger.log(level=LogLevel.DEBUG, message=f"追加元素：{self._locator} 文本：{text}")
		try :
			# 实现追加文本逻辑，假设使用 self._driver.find_element 来查找元素
			self._driver.find_element(*self._locator).send_keys(text)
			GlobalLogger.info(f"追加元素文本：{self._locator}，文本值：{text}")
			return True
		except Exception as exp :
			GlobalLogger.error(f"追加元素：{self._locator} 的文本 {text} 时出错，错误信息：{str(exp)}")
			return False

	# @GlobalLogger.log_decorator(level=LogLevel.DEBUG, message=f"获取元素：{self._locator} 所有选项")
	def get_options(self) -> list[WebElement | str | int] :
		"""
		获取所有选项
		:return: 所有选项 if success_get else []
		"""
		GlobalLogger.log(level=LogLevel.DEBUG, message=f"获取元素：{self._locator} 所有选项")
		try :
			# 实现获取选项逻辑，假设使用 self._driver.find_element 来查找元素
			select_element = Select(self._driver.find_element(*self._locator))
			options_by_select_element = select_element.options
			return options_by_select_element
		except Exception as exp :
			GlobalLogger.error(f"利用 Select 实例获取元素：{self._locator} 的所有选项时出错，错误信息：{str(exp)}")
			try :
				options = self._driver.find_element(*self._locator).get_attribute("value")
				GlobalLogger.info(f"获取所有选项：{self._locator}，选项值：{options}")
				return [options]
			except Exception as exp :
				GlobalLogger.error(f"获取元素：{self._locator} 的所有选项时出错，错误信息：{str(exp)}")
				return []

	# @GlobalLogger.log_decorator(level=LogLevel.DEBUG, message=f"获取元素：{self._locator} 选中选项")
	def get_selected_option(self) -> WebElement | str | int :
		"""
		获取选中的选项
		:return: 选中的选项 if success_get else None
		"""
		GlobalLogger.log(level=LogLevel.DEBUG, message=f"获取元素：{self._locator} 选中选项")
		try :
			# 实现获取选中选项逻辑，假设使用 self._driver.find_element 来查找元素
			select_element = Select(self._driver.find_element(*self._locator))
			option_by_select_element = select_element.first_selected_option
			return option_by_select_element
		except Exception as exp :
			GlobalLogger.error(f"利用 Select 实例获取元素：{self._locator} 的选中选项时出错，错误信息：{str(exp)}")
			try :
				option = self._driver.find_element(*self._locator).get_attribute("value")
				GlobalLogger.info(f"获取选中的选项：{self._locator}，选项值：{option}")
				return option
			except Exception as exp :
				GlobalLogger.error(
						f"利用 attribute(\"value\") 获取元素：{self._locator} 的选中选项时出错，错误信息：{str(exp)}"
				)
				return None

	# @GlobalLogger.log_decorator(level=LogLevel.DEBUG, message=f"获取元素：{self._locator} 所有选中选项")
	def get_selected_options(self) -> list[WebElement | str | int] :
		"""
		获取所有选中的选项
		:return: 选中的选项列表 if success_get else []
		"""
		GlobalLogger.log(level=LogLevel.DEBUG, message=f"获取元素：{self._locator} 所有选中选项")
		try :
			select_element = Select(self._driver.find_element(*self._locator))
			options_by_select_element = select_element.all_selected_options
			return options_by_select_element
		except NoSuchElementException as exp :
			GlobalLogger.error(
					f"Error occurred while getting selected options for element: {self._locator}. Error: {str(exp)}"
			)
			try :
				selected_value = self._driver.find_element(*self._locator).get_attribute("value")
				GlobalLogger.info(f"获取选中的选项：{self._locator}，选项值：{selected_value}")
				return [selected_value]
			except NoSuchElementException as exp :
				GlobalLogger.error(
						f"Error occurred while getting selected option using attribute('value') for element: {self._locator}. Error: {str(exp)}"
				)
				return []

	# @GlobalLogger.log_decorator(level=LogLevel.DEBUG, message=f"根据索引:{index} 选择元素：{self._locator} 的选项")
	def select_by_index(self, index: int) -> bool :
		"""
		根据索引选择选项
		:param index: 索引值
		:return: True if success_select else False
		"""
		GlobalLogger.log(level=LogLevel.DEBUG, message=f"根据索引:{index} 选择元素：{self._locator} 的选项")
		try :
			# 实现根据索引选择选项逻辑，假设使用 self._driver.find_element 来查找元素
			select_element = Select(self._driver.find_element(*self._locator))
			select_element.select_by_index(index)
			GlobalLogger.info(f"根据索引选择选项：{self._locator}，索引值：{index}")
			return True
		except Exception as exp :
			GlobalLogger.error(f"根据索引选择元素：{self._locator} 的选项时出错，错误信息：{str(exp)}")
			return False

	# @GlobalLogger.log_decorator(level=LogLevel.DEBUG, message=f"根据 value:{value} 选择元素：{self._locator} 的选项")
	def select_by_value(self, value: str, partial_value: bool) -> bool :
		"""
		根据 value 选择选项
		:param value: value 值
		:param partial_value: 是否为模糊匹配
		:return: True if success_select else False
		"""
		GlobalLogger.log(level=LogLevel.DEBUG, message=f"根据 value:{value} 选择元素：{self._locator} 的选项")
		try :
			# 实现根据 value 选择选项逻辑，假设使用 self._driver.find_element 来查找元素
			select_element = Select(self._driver.find_element(*self._locator))
			if partial_value :
				for option in select_element.options :
					if value in option.get_attribute("value") :
						option.click()
						break
			else :
				select_element.select_by_value(value)
			GlobalLogger.info(f"根据 value 选择选项：{self._locator}，value 值：{value}")
			return True
		except Exception as exp :
			GlobalLogger.error(f"根据 value 选择元素：{self._locator} 的选项时出错，错误信息：{str(exp)}")
			return False

	# @GlobalLogger.log_decorator(level=LogLevel.DEBUG, message=f"根据文本:{text} 选择元素：{self._locator} 的选项")
	def select_by_visible_text(self, text: str, partial_text: bool) -> bool :
		"""
		根据文本选择选项
		:param text: 文本值
		:param partial_text: 是否为模糊匹配
		:return: True if success_select else False
		"""
		GlobalLogger.log(level=LogLevel.DEBUG, message=f"根据文本:{text} 选择元素：{self._locator} 的选项")
		try :
			# 实现根据文本选择选项逻辑，假设使用 self._driver.find_element 来查找元素
			select_element = Select(self._driver.find_element(*self._locator))
			if partial_text :
				for option in select_element.options :
					if text in option.text :
						option.click()
						break
			else :
				select_element.select_by_visible_text(text)
			GlobalLogger.info(f"根据文本选择选项：{self._locator}，文本值：{text}")
			return True
		except Exception as exp :
			GlobalLogger.error(f"根据文本选择元素：{self._locator} 的选项时出错，错误信息：{str(exp)}")
			return False

	# @GlobalLogger.log_decorator(level=LogLevel.DEBUG, message=f"获取元素：{self._locator} 标签")
	def get_tag(self) :
		"""
		获取元素标签
		:return: 元素标签 if success_get else ""
		"""
		try :
			# 实现获取标签逻辑，假设使用 self._driver.find_element 来查找元素
			tag = self._driver.find_element(*self._locator).tag_name
			GlobalLogger.info(f"获取元素标签：{self._locator}，标签值：{tag}")
			return tag
		except Exception as exp :
			GlobalLogger.error(f"获取元素：{self._locator} 的标签时出错，错误信息：{str(exp)}")
			return ""

	# @GlobalLogger.log_decorator(level=LogLevel.DEBUG, message=f"获取元素：{self._locator} 所有 attribute 属性")
	def get_attributes(self) :
		"""
		获取元素所有 attributes
		:return: 属性 if success_get else {}
		"""
		attributes = { }
		try :
			# 获取元素
			element = self.driver.find_element_by_xpath("your_xpath_here")

			# 获取元素的所有属性
			element_attributes = element.get_attribute("outerHTML")

			# 解析元素的所有属性
			if element_attributes :
				attributes = parse_attributes(element_attributes)

		except Exception as e :
			# 处理异常
			GlobalLogger.error("Error occurred while getting attributes:", str(e))

		return attributes

	# @GlobalLogger.log_decorator(
	# 		level=LogLevel.DEBUG, message=f"获取元素：{self._locator} attribute 属性 >>> name: {name}, "
	# 		                              f"partial_name: {partial_name}"
	# )
	def get_attribute(self, name: str, partial_name: bool) :
		"""
		获取元素 attribute
		:param name: 属性名
		:param partial_name: 是否模糊匹配
		:return: 属性值 if success_get else "" | []
		"""
		try :
			if partial_name :
				attributes = self.get_attributes()
				attribute = []
				for key in attributes.keys() :
					if name in key :
						attribute.append((key, attributes[key]))
						GlobalLogger.info(
								f"模糊匹配 >>> 获取元素属性：{self._locator}，属性名：{name}, 匹配到的属性名：{key}，属性值：{attribute}"
						)
			else :
				# 实现获取属性逻辑，假设使用 self._driver.find_element 来查找元素
				attribute = self._driver.find_element(*self._locator).get_attribute(name)
				GlobalLogger.info(f"精准查询 >>> 获取元素属性：{self._locator}，属性名：{name}，属性值：{attribute}")
			return attribute
		except Exception as exp :
			GlobalLogger.error(f"获取元素：{self._locator} 的属性时出错，错误信息：{str(exp)}")
			return ""

	def get_properties(self) :
		"""
		获取所有元素 properties
		暂时不支持
		"""
		# 实现获取元素属性逻辑
		pass

	def get_property(self, name: str, partial_name: bool) :
		"""
		获取元素属性
		:param name: 属性名
		:param partial_name: 是否模糊匹配，暂时不支持
		:return: 属性值 if success_get else "" | []
		"""
		try :
			partial_name = False
			if partial_name :
				attributes = self.get_attributes()
				a = self._driver.find_element(*self._locator).get_property()
				attribute = []
				for key in attributes.keys() :
					if name in key :
						attribute.append((key, attributes[key]))
						GlobalLogger.info(
								f"模糊匹配 >>> 获取元素属性：{self._locator}，属性名：{name}, 匹配到的属性名：{key}，属性值：{attribute}"
						)
			else :
				# 实现获取属性逻辑，假设使用 self._driver.find_element 来查找元素
				attribute = self._driver.find_element(*self._locator).get_property(name)
				GlobalLogger.info(f"精准查询 >>> 获取元素属性：{self._locator}，属性名：{name}，属性值：{attribute}")
			return attribute
		except Exception as exp :
			GlobalLogger.error(f"获取元素：{self._locator} 的属性时出错，错误信息：{str(exp)}")
			return ""

	# @GlobalLogger.log_decorator(
	# 		level=LogLevel.DEBUG, message=f"获取元素：{self._locator} CSS value >>> name: {name}, "
	# 		                              f"partial_name: {partial_name}"
	# )
	def get_css_value(self, name: str, partial_name: bool) :
		"""
		获取元素 CSS value
		:param name: 属性名
		:param partial_name: 是否模糊匹配
		:return: 属性值 if success_get else "" | []
		"""
		try :
			# 获取元素
			element = self._driver.find_element(*self._locator)

			if partial_name :
				# 模糊匹配属性名
				css_properties = element.value_of_css_property("*")
				matching_values = []
				for property_name, property_value in css_properties.items() :
					if name in property_name :
						matching_values.append((property_name, property_value))
						GlobalLogger.info(
								f"获取元素 CSS value：{self._locator}，属性名：{name}，"
								f"匹配到的属性名:{property_name},属性值：{property_value}"
						)
				return matching_values
			else :
				# 精确匹配属性名
				css_value = element.value_of_css_property(name)
				GlobalLogger.info(f"获取元素 CSS value：{self._locator}，属性名：{name}，属性值：{css_value}")
				return css_value

		except Exception as exp :
			GlobalLogger.error(f"获取元素：{self._locator} 的 CSS value 时出错，错误信息：{str(exp)}")
		return ""

	def get_rect(self) :
		"""
		获取元素 rect
		:return: rect if success_get else {}
		"""
		try :
			# 获取元素
			element = self._driver.find_element(*self._locator)

			# 获取元素 rect
			rect = element.rect
			GlobalLogger.info(f"获取元素 rect：{self._locator}，rect：{rect}")
			return rect

		except Exception as exp :
			GlobalLogger.error(f"获取元素：{self._locator} 的 rect 时出错，错误信息：{str(exp)}")
		return { }

	def get_size(self) :
		"""
		获取元素尺寸
		:return: 尺寸 if success_get else {}
		"""
		try :
			# 获取元素
			element = self._driver.find_element(*self._locator)

			# 获取元素尺寸
			size = element.size
			GlobalLogger.info(f"获取元素尺寸：{self._locator}，尺寸：{size}")
			return size

		except Exception as exp :
			GlobalLogger.error(f"获取元素：{self._locator} 的尺寸时出错，错误信息：{str(exp)}")
		return { }

	def get_location(self) :
		"""
		获取元素位置
		:return: 位置 if success_get else {}
		"""
		try :
			# 获取元素
			element = self._driver.find_element(*self._locator)

			# 获取元素位置
			location = element.location
			GlobalLogger.info(f"获取元素位置：{self._locator}，位置：{location}")
			return location

		except Exception as exp :
			GlobalLogger.error(f"获取元素：{self._locator} 的位置时出错，错误信息：{str(exp)}")
		return { }
