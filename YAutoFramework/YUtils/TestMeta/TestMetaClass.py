import os
import re
import time
from datetime import datetime

from selenium.webdriver.remote.webdriver import WebDriver as Base_WebDriver

import YAutoFramework
from YAutoFramework.YUtils.Logger.Ylogger import GlobalLogger, TestLogger
from YAutoFramework.YUtils.ScreenshotHelper.Screenshoter import Screenshoter
from YAutoFramework.YUtils.TestInfos.StatusINFO import ScriptStatus
from YAutoFramework.YUtils.TestInfos.YTestInfo import YTester


# @dataclass
# class TestMetaAttrs :
# 	ID = 'TC20018764'
# 	Title = 'Test Case Title'
# 	Description = 'Test Case '
# 	Tester = YTester.Admin
# 	Category = 'TestPlanPage'
# 	Script_Status = ScriptStatus.Reviewed and ScriptStatus.Accept
# 	Log = TestLogger(os.path.relpath(os.path.dirname(__file__)))


class TestMeta(type) :
	"""
	作为 Test Case class 的 Template
	自定义 Test Class 元类，用于在创建测试用例类时绑定其属性
	\nDriver =  selenium.webdriver.chrome.webdriver() -- 必填项
	\nID = 'TC20018764' --- 必填项
	\nTitle = 'Test Case Title'
	\nDescription = 'Test Case '
	\nTester = YTester.Admin
	\nCategory = 'TestPlanPage'
	\nScript_Status = ScriptStatus.Reviewed and ScriptStatus.Accept
	"""
	TestCases = { }  # 记录已经存在的 Test Cases, 还未实现该方法

	"""
	__new__方法在元类中的常见应用场景包括：
	
	1. 改变类创建过程：
	- 在类创建前修改类定义 (如修改类属性)
	- 在类创建后修改类对象 (如添加方法)
	- 控制类的实例化过程 (如实现单例模式)
	2.自定义类注册过程：
	- 将创建的类自动注册到注册表中
	- 检查子类是否满足注册条件
	3. 设计模式强制：
	- 检查子类是否遵循特定设计模式
	- 强制子类实现设计模式接口
	4.自动绑定属性/方法：
	- 为子类绑定非类定义中的属性或方法
	- 根据自定义逻辑添加属性/方法
	5.自动记录类信息：
	- 记录类的父类、属性、方法等信息
	- 实现自动文档或注释
	6.优化类创建：
	- 根据需要懒加载类属性或方法
	- 定制化类创建流程
"""

	def __new__(cls, name, bases, attrs) :
		"""
		__new__方法的主要作用是：

		获取原类定义信息
		创建原类对象
		修改原类对象
		返回修改后的原类对象
		:param name: 类名
		:param bases: 继承类组
		:param attrs: 特性组
		"""

		try :
			# 从类体定义中获取属性信息
			id_ = attrs.get('ID')
			if not id_ :
				raise ValueError('ID cannot be empty, ID must be entered.')
			# 正则匹配类名中的 ID 号
			if not id_ == (tc := re.search(r'TC\d+', name).group()) :
				raise ValueError(f'Test Case Class name is not equals ID >>> name:{tc} --- ID:{id_}.')

			driver_ = attrs.get('Driver')
			if not driver_ :
				raise ValueError('Driver cannot be empty, WebDriver must be entered.')
			if not isinstance(driver_, Base_WebDriver) :
				raise ValueError(f'Driver is not supported. >>> current _driver:{driver_}.')

			title = attrs.get('Title')
			desc = attrs.get('Description')
			tester = attrs.get('Tester', YTester.Unknown)
			category = attrs.get('Category', 'UI Test')
			creation_time = attrs.get('Creation_Time', datetime(2000, 1, 1))
			status = attrs.get('Script_Status', ScriptStatus.InReview)

		except ValueError as exp :
			GlobalLogger.error(f"Failed to create [{name}] Test Case Class.>>> Error Msg:{str(exp)}")
			raise exp
		except Exception as exp :
			GlobalLogger.critical(f"Failed to create [{name}] Test Case Class.>>> Critical Msg:{str(exp)}")
			raise exp
		# 直接通过 super 创建原类对象，不返回新对象
		cls_obj = type.__new__(cls, name, bases, attrs)

		# 在原类对象上绑定获取的属性
		cls_obj.id = id_
		cls_obj.title = title
		cls_obj.description = desc
		cls_obj.tester = tester
		cls_obj.category = category
		cls_obj.creation_time = creation_time
		cls_obj.status = status
		cls_obj.driver = driver_

		# 为当前类创建 dataout/Testcase ID 文件夹
		dataout_folder_full_path = os.path.join(YAutoFramework.dataout_folder, cls_obj.id)
		timestamp = time.strftime('%Y%m%d_%H%M', time.localtime())

		# 为当前类加上 Logger
		log_full_path = os.path.join(dataout_folder_full_path, "logs", f'{cls_obj.id}_{timestamp}.txt')
		cls_obj.Log = TestLogger(log_full_path)

		# 为当前类加上 Screenshoter
		cls_obj.Screenshot = Screenshoter(
				driver=cls_obj.Driver,
				logger=cls_obj.Log,
				file_folder_full_path=dataout_folder_full_path,
				folder_name="screenshots",
				screenshot_name=cls_obj.id
		)

		# 返回修改后的原类对象
		msg = f"Test Case:[{name}] created >>> ID:[{cls_obj.id}] >>> Title: [{cls_obj.title}]"
		GlobalLogger.debug(message=msg)
		return cls_obj
