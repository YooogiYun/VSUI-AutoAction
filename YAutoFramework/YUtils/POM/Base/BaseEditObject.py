from selenium.webdriver.remote.webdriver import WebDriver

from YAutoFramework.YUtils.POM.Base.BaseObject import BaseObjectClass
from YAutoFramework.YUtils.POM.Base.BaseObjectFuncs import BaseTextObjectFunctions


class BaseEditObjectClass(BaseObjectClass, BaseTextObjectFunctions) :
	"""
	文本输入框基类
	"""

	def __init__(self, driver: WebDriver, locator: tuple[any, str], parent: BaseObjectClass = None) :
		super().__init__(driver, locator, parent)

	# 以下为 BaseObjectFunctions 接口实现
	def exists(self) -> bool :
		return super().exists()

	def click(self, button_type: str = "left", click_count: int = 1, interval: int = 125) -> bool :
		return super().click(button_type, click_count, interval)

	def double_click(
			self, button_type: str = "left", click_count: int = 1, doubleclick_span: int = 100, interval: int = 125
	) -> bool :
		return super().double_click(button_type, click_count, doubleclick_span, interval)

	def right_click(self, button_type: str = "right", click_count: int = 1, interval: int = 125) -> bool :
		return super().right_click(button_type, click_count, interval)

	def long_click(
			self, button_type: str = "left",
			click_count: int = 1,
			duration: int = 250,
			interval: int = 125
	) -> bool :
		return super().long_click(button_type, click_count, duration, interval)

	def scroll_into_view(self) -> bool :
		return super().scroll_into_view()

	def wait_for_ready(self, timeout: float = None) -> bool :
		return super().wait_for_ready(timeout)

	def wait_till_exists(self, timeout: float = None) -> bool :
		return super().wait_till_exists(timeout)

	def wait_till_disappear(self, timeout: float = None) -> bool :
		return super().wait_till_disappear(timeout)

	def wait_till_disabled(self, timeout: float = None) -> bool :
		return super().wait_till_disabled(timeout)

	def wait_till_enabled(self, timeout: float = None) -> bool :
		return super().wait_till_enabled(timeout)

	# 以下为 BaseTextObjectFunctions 接口实现
	def clear_text(self) -> bool :
		return super().clear_text()

	def set_text(self, text: str) -> bool :
		return super().set_text(text)

	def append_text(self, text: str) -> bool :
		return super().append_text(text)

	# 以下为 BaseWebElementFunctions 接口实现
	def get_text(self) -> str :
		return super().get_text()

	def get_attribute(self, attribute_name: str, partial_name: bool) -> str :
		return super().get_attribute(attribute_name, partial_name)

	def get_attributes(self) -> dict :
		return super().get_attributes()

	def get_property(self, property_name: str, partial_name: bool) -> str :
		return super().get_property(property_name, partial_name)

	def get_properties(self) -> dict :
		return super().get_properties()

	def get_css_value(self, css_name: str, partial_name: bool) -> str :
		return super().get_css_value(css_name, partial_name)

	def get_tag(self) -> str :
		return super().get_tag()
