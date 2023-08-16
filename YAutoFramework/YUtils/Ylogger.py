import logging
import os
from abc import abstractmethod
from enum import Enum
from logging.handlers import RotatingFileHandler

from YAutoFramework import YUtils


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
	def __init__(self) :
		# 创建日志记录器
		self.logger = logging.getLogger()

		# 设置日志记录级别
		self.logger.setLevel(YUtils.level_log_default)

		# 创建日志处理器
		self.handler = RotatingFileHandler(
				filename=YUtils.file_log_default,
				maxBytes=YUtils.maxSize_bytes_log_default,
				backupCount=YUtils.backup_count_log_default,
				encoding=YUtils.encoding_log_default
		)

		# 每次启动创建一个新 log文件，而不是从原来的基础上继续添加
		self.handler.doRollover()

		# 创建日志格式化器
		self.formatter = logging.Formatter(YUtils.format_log_default)

		# 将日志格式化器添加到日志处理器
		self.handler.setFormatter(self.formatter)

		# 将日志处理器添加到日志记录器
		self.logger.addHandler(self.handler)

	@abstractmethod
	def log(self, level, message) :
		# 记录信息日志
		self.logger.log(level, message)

	@abstractmethod
	def debug(self, message) :
		# 记录调试信息日志
		self.log(LogLevel.DEBUG, message)

	@abstractmethod
	def step(self, message) :
		# 记录步骤信息日志
		self.log(LogLevel.INFO, message)

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
	def global_log(self, level: LogLevel = LogLevel.STEP, message: str = None) :
		"""
        装饰器函数，用于全局日志记录

        :param level: 日志级别，默认为 LogLevel.STEP
        :param message: 日志消息
        :return: 被装饰函数的执行结果
		"""

		# 定义装饰器函数
		def decorator(func) :
			# 定义包装函数
			def wrapper(*args, **kwargs) :
				try :
					result = func(*args, **kwargs)  # 执行被装饰的函数
					return result
				except Exception as e :
					self.error(str(e))  # 记录异常错误
				finally :
					log_level_value = level.value  # 获取日志级别的整数值
					self.log(log_level_value, message)  # 记录日志

			return wrapper

		return decorator


# Test Logger
class TestLogger(BaseYlogger) :
	def __init__(self, file_save_path) :
		super().__init__()
		# 创建日志处理器
		self.handler.baseFilename = os.fspath(file_save_path)

		# 设置日志处理器的文件保存路径
		self.logger.handlers[0] = self.handler

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

	def global_log(self, level: LogLevel = LogLevel.STEP, message: str = None) :
		"""
		装饰器函数，用于局部自定义日志记录

        :param level: 日志级别，默认为 LogLevel.STEP
        :param message: 日志消息
        :return: 被装饰函数的执行结果
		"""
		super().global_log(level=level, message=message)


# 实例化全局 Logger
GlobalLogger = BaseYlogger()
