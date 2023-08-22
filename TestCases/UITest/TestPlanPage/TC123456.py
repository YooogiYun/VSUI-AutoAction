import time

import allure
from selenium.webdriver import Chrome

from YAutoFramework.YUtils.POM.UIDefinations.XiaoHongshu import XiaoHongShuPage
from YAutoFramework.YUtils.TestInfos.StatusINFO import ScriptStatus
from YAutoFramework.YUtils.TestInfos.YTestInfo import YTester
from YAutoFramework.YUtils.TestMeta.TestMetaClass import TestMeta


class TestTC123456(metaclass=TestMeta) :
	"""
	用例编号 TC1008687
	用例名称 用例名称
	用例描述 用例描述
	前置条件 前置条件
	测试步骤 测试步骤
	预期结果 预期结果
	"""
	Driver = Chrome()
	ID = locals()["__qualname__"].replace("Test", "")
	Title = 'Test Case Title'
	Description = 'Test Case '
	Tester = YTester.Admin
	Category = 'TestPlanPage'
	Script_Status = ScriptStatus.Reviewed and ScriptStatus.Accepted

	@allure.title("测试木鱼查询网站的点击功能")
	def test(self) :
		"""
		测试用例的主体
		"""
		allure.step("打开目标页面")
		xiaohongshuPage = XiaoHongShuPage(self.Driver).open()
		print(xiaohongshuPage.title)
		allure.step("点击测试元素 50 次")
		xiaohongshuPage.CloseButton.wait_for_ready()
		xiaohongshuPage.CloseButton.click()
		print(xiaohongshuPage.title)
		time.sleep(10)

# MuYuPage = MuYuQueryPage(self.Driver).open()
# print(MuYuPage.title)
# MuYuPage.ClickToTestElement.click(click_count=20)
# MuYuPage.close()
