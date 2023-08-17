import datetime

from YAutoFramework.YUtils.TestINFO import TestINFO


@TestINFO(
		ID='TC20018764',
		Title='Test the main page of Test Plan',
		Description='''
          This is a decorator 装饰器语法.
          Define some test case properties by decorator.
          ''',
		Tester='Yooogi',
		Category='TestPlanPage',
		Creation_Time=datetime.time(),
		Script_Status='Reviewed and Accept',
)
class TestTC20018764 :
