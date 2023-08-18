import os
import time
from datetime import datetime

import pytest

from YAutoFramework.YUtils.Logger.Ylogger import GlobalLogger, TestLogger
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

		# 为当前类加上 Logger
		log_full_path = TestMeta.create_log_file(cls_obj)
		cls_obj.Log = TestLogger(log_full_path)

		# 返回修改后的原类对象
		msg = f"Test Case:[{name}] created >>> ID:[{cls_obj.id}] >>> Title: [{cls_obj.title}]"
		GlobalLogger.global_log()
		return cls_obj

	@staticmethod
	def create_log_file(cls_obj) :
		# 获取当前位置和 TestCase ID 创建 [ID].txt
		log_folder_path = os.path.relpath(os.path.dirname(__file__))
		timestamp = time.strftime('%Y%m%d_%H', time.localtime())
		log_full_path = os.path.join(log_folder_path, 'logs', f'{cls_obj.id}_{timestamp}.txt')
		return log_full_path


class TestTC20018764Example(metaclass=TestMeta) :
	"""定义测试用例类，属性在元类中绑定
	\nID 为必填项
	\nTitle = 'Test Case Title'
	\nDescription = 'Test Case '
	\nTester = YTester.Admin
	\nCategory = 'TestPlanPage'
	\nScript_Status = ScriptStatus.Reviewed and ScriptStatus.Accept
	"""
	ID = __name__
	Title = 'Test the main page of Test Plan'
	Description = '...'
	Tester = YTester.Admin
	Category = 'TestPlanPage'
	Script_Status = ScriptStatus.Coding and ScriptStatus.InReview

	@pytest.fixture(scope="function")
	def fixture_setup_teardown(self) :
		# 测试下面测试方法运行前的 SetUp
		self.Log.step(
				"""1.  
				# 在每个测试用例之前执行一些操作
				# yield 之前的代码在每个测试用例之前执行
				# yield 关键字之前的部分相当于 setup 操作
				# 它可以进行一些准备工作，例如设置测试环境、初始化资源等
				"""
		)
		result = 'the result you want to pass to the test method'  # 控制权交给测试用例函数
		yield result
		self.Log.step(
				"""2.  
                # yield 之后的代码在每个测试用例之后执行
                # yield 关键字之后的部分相当于 teardown 操作
                # 它可以进行一些清理工作，例如释放资源、恢复环境等
                # 在每个测试用例之后执行一些操作
				"""
		)

	def test_method(self, fixture_setup_teardown) :
		# 测试逻辑
		print(self.ID)  # TC20018764
		print(self.Title)  # Test the main page of Test Plan
		self.Log.step(f"current {self.ID} and {self.Title}")
		assert type(fixture_setup_teardown) == str  # True

#
# if __name__ == '__main__' :
# 	a = TestTC20018764Example()
# 	pytest.main()
