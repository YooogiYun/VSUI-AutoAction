import allure
from selenium.webdriver import Chrome

from YAutoFramework.YUtils.POM.UIDefinations.Example import MuYuQueryPage
from YAutoFramework.YUtils.TestInfos.StatusINFO import ScriptStatus
from YAutoFramework.YUtils.TestInfos.YTestInfo import YTester
from YAutoFramework.YUtils.TestMeta.TestMetaClass import TestMeta


class TestTC1008687(metaclass=TestMeta) :
	"""
	用例编号 TC1008687
	用例名称 用例名称
	用例描述 用例描述
	前置条件 前置条件
	测试步骤 测试步骤
	预期结果 预期结果
	"""
	Driver = Chrome()
	ID = 'TC1008687'
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
		with MuYuQueryPage(self.Driver).open() as MuYuPage :
			print(MuYuPage.title)
			allure.step("点击测试元素 20 次")
			MuYuPage.ClickToTestElement.click(click_count=20)

# MuYuPage = MuYuQueryPage(self.Driver).open()
# print(MuYuPage.title)
# MuYuPage.ClickToTestElement.click(click_count=20)
# MuYuPage.close()
