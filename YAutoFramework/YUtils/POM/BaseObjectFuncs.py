import abc

from selenium.webdriver.remote.webelement import WebElement


class BaseObjectFunctions :
	"""
	基础对象功能接口
	"""

	@abc.abstractmethod
	def exists(self) -> bool :
		"""
		判断元素是否存在
		:return: True if exists else False
		"""
		# 实现判断元素是否存在的逻辑
		pass

	@abc.abstractmethod
	def click(self, button_type: str = "left", click_times: int = 1, span_time: int = 125) -> bool :
		"""
		点击元素
		:param button_type: 鼠标按键类型，可选值：left、right、middle,forward,back, 默认为 left
		:param click_times: 点击次数，默认为 1
		:param span_time: 点击间隔时间，默认为 125ms
		:return: True if click success else False
		"""
		# 实现点击逻辑
		pass

	@abc.abstractmethod
	def long_click(
			self, button_type: str = "left", click_times: int = 1, duration_time: int = 250, interval: int = 125
	) -> bool :
		"""
		长按元素
		:param button_type:  鼠标按键类型，可选值：left、right、middle
		:param click_times:  点击次数
		:param duration_time: 长按时间
		:param interval:      间隔时间
		:return : True if click success else False:
		"""
		# 实现长按逻辑
		pass

	@abc.abstractmethod
	def wait_till_exists(self, timeout: float = None) -> bool :
		"""
		selenium 等待元素出现
		:param timeout: 超时时间
		:return: True if element exists else False
		"""
		# 实现等待逻辑
		pass

	@abc.abstractmethod
	def wait_till_disappear(self, timeout: float = None) -> bool :
		"""
		selenium 等待元素消失
		:param timeout: 超时时间
		:return: True if element not exists else False
		"""
		# 实现等待逻辑
		pass

	@abc.abstractmethod
	def wait_till_enabled(self, timeout: float = None) -> bool :
		"""
		selenium 等待元素可用
		:param timeout: 超时时间
		:return: True if element enabled else False
		"""
		# 实现等待逻辑
		pass

	@abc.abstractmethod
	def wait_till_disabled(self, timeout: float = None) -> bool :
		"""
		selenium 等待元素不可用
		:param timeout: 超时时间
		:return: True if element disabled else False
		"""
		# 实现等待逻辑
		pass

	@abc.abstractmethod
	def wait_for_ready(self, timeout: float = None) -> bool :
		"""
		等待元素就绪
		:param timeout: 超时时间
		:return: True if element ready else False
		"""
		# 实现等待逻辑
		pass

	@abc.abstractmethod
	def scroll_into_view(self) -> bool :
		"""
		滚动到元素可见
		:return: True if scroll success else False
		"""
		# 实现滚动逻辑
		pass


class BaseTextObjectFunctions :
	"""
	文本元素基类功能接口
	"""

	@abc.abstractmethod
	def get_text(self) -> str :
		"""
		获取元素文本
		:return: 元素文本
		"""
		# 实现获取元素文本逻辑
		pass

	@abc.abstractmethod
	def clear_text(self) -> bool :
		"""
		清空元素文本
		:return: True if clear success else False
		"""
		# 实现清空元素文本逻辑
		pass

	@abc.abstractmethod
	def set_text(self, text: str) -> bool :
		"""
		设置元素文本
		:param text: 要设置的文本
		:return: True if set success else False
		"""
		# 实现设置元素文本逻辑
		pass

	@abc.abstractmethod
	def append_text(self, text: str) -> bool :
		"""
		追加元素文本
		:param text: 要追加的文本
		:return: True if append success else False
		"""
		# 实现追加元素文本逻辑
		pass


class BaseSelectObjectFunctions :
	"""
	下拉框元素基类功能接口
	"""

	@abc.abstractmethod
	def get_options(self) -> list[WebElement | str | int] :
		"""
		获取所有选项
		:return: 所有选项
		"""
		# 实现获取所有选项逻辑
		pass

	@abc.abstractmethod
	def get_selected_option(self) -> WebElement | str | int :
		"""
		获取选中的选项
		:return: 选中的选项
		"""
		# 实现获取选中的选项逻辑
		pass

	@abc.abstractmethod
	def get_selected_options(self) -> list[WebElement | str | int] :
		"""
		获取选中的选项
		:return: 选中的选项
		"""
		# 实现获取选中的选项逻辑
		pass

	@abc.abstractmethod
	def select_by_index(self, index: int) -> bool :
		"""
		通过索引选择选项
		:param index: 索引
		:return: True if select success else False
		"""
		# 实现通过索引选择选项逻辑
		pass

	@abc.abstractmethod
	def select_by_value(self, value: str, partial_value: bool) -> bool :
		"""
		通过 value 选择选项
		:param value: value
		:param partial_value: 是否为模糊匹配
		:return: True if select success else False
		"""
		# 实现通过 value 选择选项逻辑
		pass

	@abc.abstractmethod
	def select_by_visible_text(self, text: str, partial_text: bool) -> bool :
		"""
		通过文本选择选项
		:param text: 文本
		:param partial_text: 是否为模糊匹配
		:return: True if select success else False
		"""
		# 实现通过文本选择选项逻辑
		pass


class BaseWebElementFunctions :
	"""
	获取元素基类功能接口
	"""

	@abc.abstractmethod
	def get_tag(self) :
		"""
		获取元素标签
		:return: 元素标签 if success_get else ""
		"""
		# 实现获取元素标签逻辑
		pass

	@abc.abstractmethod
	def get_attributes(self) :
		"""
		获取元素所有 attributes
		:return: 属性 if success_get else {}
		"""
		# 实现获取元素所有属性逻辑
		pass

	@abc.abstractmethod
	def get_attribute(self, name: str, partial_name: bool) :
		"""
		获取元素 attribute
		:param name: 属性名
		:param partial_name: 是否为模糊匹配
		:return: 属性值 if success_get else ""
		"""
		# 实现获取元素属性逻辑
		pass

	@abc.abstractmethod
	def get_properties(self) :
		"""
		获取所有元素 properties
		"""
		# 实现获取元素属性逻辑
		pass

	@abc.abstractmethod
	def get_property(self, name: str, partial_name: bool) :
		"""
		获取元素 property
		:param name: 属性名
		:return: 属性值 if success_get else ""
		"""
		# 实现获取元素属性逻辑
		pass

	@abc.abstractmethod
	def get_css_value(self, name: str, partial_name: bool) :
		"""
		获取元素 css 属性
		:param name: 属性名
		:param partial_name: 是否为模糊匹配
		:return: 属性值 if success_get else ""
		"""
		# 实现获取元素 css 属性逻辑
		pass

	@abc.abstractmethod
	def get_rect(self) :
		"""
		获取元素位置信息
		:return: 位置信息 if success_get else ""
		"""
		# 实现获取元素位置信息逻辑
		pass

	@abc.abstractmethod
	def get_size(self) :
		"""
		获取元素大小信息
		:return: 大小信息 if success_get else ""
		"""
		# 实现获取元素大小信息逻辑
		pass

	@abc.abstractmethod
	def get_location(self) :
		"""
		获取元素位置信息
		:return: 位置信息 if success_get else ""
		"""
		# 实现获取元素位置信息逻辑
		pass

	@abc.abstractmethod
	def get_text(self) :
		"""
		获取元素文本
		:return: 文本 if success_get else ""
		"""
		# 实现获取元素文本逻辑
		pass
