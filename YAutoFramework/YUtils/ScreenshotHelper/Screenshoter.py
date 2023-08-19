import os
from os import PathLike
from typing import AnyStr

from selenium.webdriver.remote.webdriver import WebDriver

from YAutoFramework.YUtils import ScreenshotHelper
from YAutoFramework.YUtils.Logger.Ylogger import BaseYlogger


class Screenshoter :
	def __init__(
			self, driver: WebDriver, logger: BaseYlogger, folder_name: str = "screenshots",
			screenshot_name: str = None,
			file_folder_full_path: PathLike[AnyStr] | str = None
	) :
		"""
		初始化一个 屏幕截图工具，该工具会将截图保存到指定的文件夹中，文件夹位置由参数 file_folder_full_path+folder_name+screenshot_name.png 指定。

		:param driver:  selenium web driver
		:param logger:  logger
		:param folder_name:  截图文件夹名
		:param screenshot_name:  屏幕截图文件名
		:param file_folder_full_path:  截图文件夹位置的完整路径
		"""
		self.driver = driver
		self.logger = logger
		screenshot_name = screenshot_name if screenshot_name else ScreenshotHelper.screenshot_name_default
		file_folder_full_path = file_folder_full_path if file_folder_full_path else ScreenshotHelper.root_folder_screenshot
		self.file_full_path = os.path.join(
				file_folder_full_path,
				folder_name,
				f'{screenshot_name}_{ScreenshotHelper._time_stamp}{ScreenshotHelper.screenshot_extension_default}'
		)
		# 创建截图文件夹
		if not os.path.exists(os.path.dirname(self.file_full_path)) :
			os.makedirs(os.path.dirname(self.file_full_path))

	def take_screenshot(self) :
		"""
		在给定的 WebDriver 实例上执行截图操作，并将截图保存为指定的文件名。
		"""
		try :
			self.driver.save_screenshot(self.file_full_path)
			self.logger.info(message=f"截图已保存为 {self.file_full_path}")
		except Exception as e :
			self.logger.error(message=f"截图失败：{str(e)}")
