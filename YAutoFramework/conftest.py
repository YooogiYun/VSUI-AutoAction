# content of conftest.py
import inspect

import allure
from _pytest.assertion.util import assertrepr_compare

from YAutoFramework.YUtils.Logger.Ylogger import GlobalLogger


def pytest_assertrepr_compare(config, op, left, right) :
	left_name, right_name = inspect.stack()[7].code_context[0].lstrip().lstrip('assert').rstrip('\n').split(op)
	pytest_output = assertrepr_compare(config, op, left, right)
	GlobalLogger.debug("{0} is\n {1}".format(left_name, left))
	GlobalLogger.debug("{0} is\n {1}".format(right_name, right))
	with allure.step("校验结果") :
		allure.attach(str(left), left_name)
		allure.attach(str(right), right_name)
	return pytest_output
