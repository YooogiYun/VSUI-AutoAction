import datetime
import logging
import os
from abc import abstractmethod
from enum import Enum
from functools import wraps
from logging.handlers import RotatingFileHandler
from os import PathLike
from typing import AnyStr

import YAutoFramework.YUtils.Logger as YLogger


def makesure_logfile_exists(log_save_path: PathLike[AnyStr]) :
	"""
	确保目录存在，如果不存在则递归创建完整路径
	:param log_save_path:
	:return: True if file_exists else False
	"""
	file_exists = False
	# 确保目录存在，递归创建完整路径
	os.makedirs(os.path.dirname(log_save_path), exist_ok=True)

	# 检查文件是否存在
	if not os.path.exists(log_save_path) :
		# 创建文件
		try :
			with open(log_save_path, 'w') as file :
				pass
			print(f'文件已创建：{log_save_path}')
			file_exists = True
		except OSError as e :
			print(f'创建文件时出现错误：{e}')
	else :
		print(f'文件已存在：{log_save_path}')
		file_exists = True
	return file_exists


# 映射 logging 的 log level
class LogLevel(Enum) :
	"""
	映射 logging 的日志级别\n
	Tips: STEP = INFO
	"""
	STEP = logging.INFO
	DEBUG = logging.DEBUG
	INFO = logging.INFO
	WARNING = logging.WARNING
	ERROR = logging.ERROR
	CRITICAL = logging.CRITICAL


# 软件全局 logger

class BaseYlogger :
	def __init__(self, file_path: PathLike[str]) :
		# 创建 log 文件
		makesure_logfile_exists(file_path)

		# 创建日志记录器
		self.logger = logging.getLogger()

		# 设置日志记录级别
		self.logger.setLevel(YLogger.level_log_default)

		# 创建日志处理器
		self.handler = RotatingFileHandler(
				filename=file_path,
				maxBytes=YLogger.maxSize_bytes_log_default,
				backupCount=YLogger.backup_count_log_default,
				encoding=YLogger.encoding_log_default
		)

		# 每次启动创建一个新 log 文件，而不是从原来的基础上继续添加
		# self.handler.doRollover()

		# 创建日志格式化器
		self.formatter = logging.Formatter(YLogger.format_log_default)

		# 将日志格式化器添加到日志处理器
		self.handler.setFormatter(self.formatter)

		# 将日志处理器添加到日志记录器
		self.logger.addHandler(self.handler)

	@abstractmethod
	def log(self, level, message) :
		# 记录信息日志
		print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]-({level.name}) >>> msg:{message}')
		self.logger.log(level.value, message)

	@abstractmethod
	def debug(self, message) :
		# 记录调试信息日志
		self.log(LogLevel.DEBUG, message)

	@abstractmethod
	def step(self, message) :
		# 记录步骤信息日志

		self.log(LogLevel.INFO, "[STEP] >>> " + message)

	@abstractmethod
	def info(self, message) :
		# 记录步骤信息日志
		self.log(LogLevel.INFO, message)

	@abstractmethod
	def warning(self, message) :
		# 记录警告信息日志
		self.log(LogLevel.WARNING, message)

	@abstractmethod
	def error(self, message) :
		# 记录错误信息日志
		self.log(LogLevel.ERROR, message)

	@abstractmethod
	def critical(self, message) :
		# 记录严重错误信息日志
		self.log(LogLevel.CRITICAL, message)

	@abstractmethod
	def log_decorator(self, level: LogLevel = LogLevel.INFO, message: str = None) :
		"""
		装饰器函数，用于全局日志记录
		使用格式化字符串，将函数的参数和返回值记录到日志中
		@log_decorator(level=LogLevel.DEBUG, message="点击 {self._locator} 元素是否可见，button_type={button_type}, click_times={click_times}")
		def click(self, button_type: str = "left", click_times: int = 1) -> bool:
		:param level: 日志级别，默认为 LogLevel.INFO
		:param message: 日志消息
		"""

		def decorator(func) :
			@wraps(func)
			def wrapper(self, *args, **kwargs) :
				# 将形参转换为字符串
				args_str = ", ".join(str(arg) for arg in args)
				kwargs_str = ", ".join(f"{key}={value}" for key, value in kwargs.items())
				params = ", ".join(filter(None, [args_str, kwargs_str]))

				# 构造最终的日志消息
				formatted_message = message.format(params)
				try :
					# 执行原始函数
					result = func(*args, **kwargs)
					self.log(
							level, f"[{func.__name__}] was called at [{datetime.datetime.now()}] >>> result: [{result}]"
					)
					return result
				except Exception as e :
					self.error(str(e))  # 记录异常错误
				finally :
					# 记录日志
					self.log(level, formatted_message)

			return wrapper

		return decorator


# Test Logger
class TestLogger(BaseYlogger) :
	def __init__(self, file_save_path) :
		super().__init__(file_save_path)
		# 确保日志文件存在
		makesure_logfile_exists(file_save_path)

		# 避免重复 log
		self.logger.removeHandler(self.handler)

		# 创建日志处理器
		self.handler.baseFilename = os.fspath(file_save_path)

		# 设置日志处理器的文件保存路径
		self.logger.addHandler(self.handler)

	def log(self, level, message) :
		super().log(level, message)

	def debug(self, message) :
		super().debug(message)

	def step(self, message) :
		super().step(message)

	def info(self, message) :
		super().info(message)

	def warning(self, message) :
		super().warning(message)

	def error(self, message) :
		super().error(message)

	def critical(self, message) :
		super().critical(message)

	def log_decorator(self, level: LogLevel = LogLevel.INFO, message: str = None) :
		"""
		装饰器函数，用于局部自定义日志记录

        :param level: 日志级别，默认为 LogLevel.STEP
        :param message: 日志消息
        :return: 被装饰函数的执行结果
		"""
		super().log_decorator(level=level, message=message)


# 实例化全局 Logger
GlobalLogger = BaseYlogger(YLogger.file_log_default)
