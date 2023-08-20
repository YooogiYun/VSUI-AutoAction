from YAutoFramework.YUtils.Logger.Ylogger import GlobalLogger, LogLevel


# class TestTC20018764(metaclass=TestMeta) :
# 	ID = 'TC234234'

class ADecorator :
	def __init__(self, func) :
		self.func = func

	def __call__(self, *args, **kwargs) :
		print("装饰器开始")
		a = self.func
		print(a)
		self.func(*args, **kwargs)
		print("装饰器结束")


class BtestOne :
	def __init__(self) :
		self.nametitle = "BtestOne"

	@ADecorator
	@GlobalLogger.log_decorator(LogLevel.STEP, "步骤 1,nametitle: name: {name}, age: {age}, time: {time}")
	def methodtes_toperator(self, name: str, age: int, time: float = 1.0) :
		print(name)
		print(age)
		print(time)


#
# driver = selenium.webdriver.Chrome()
# # driver.get(r"http://cps-test.bchrt.com/")
# driver.get(r"https://www.baidu.com/")
# target = BaseObjectClass(driver=driver, locator=(By.CSS_SELECTOR, 'button#start'))
# target.wait_till_exists(timeout=10)
# target.click(click_count=10, interval=125)
# print(target.is_enabled())
# print(target.is_displayed())

BtestOne().methodtes_toperator(age=18, name="张三", time=1.0)
input()

# MouseButtonDict = {
# 	"left"    : MouseButton.LEFT,
# 	"middle"  : MouseButton.MIDDLE,
# 	"right"   : MouseButton.RIGHT,
# 	"forward" : MouseButton.FORWARD,
# 	"back"    : MouseButton.BACK,
# }
#
# button_ = MouseButtonDict["okk"]
# if button_ is None:
# 	print("None")
# else:
# 	print(button_)

# _driver = selenium.webdriver.Chrome
# _driver = _driver()
# # _driver.get("https://www.baidu.com/")
# _driver.get(r"http://cps-test.bchrt.com/")
# title = _driver.title
# url = _driver.current_url
# print(title, url)
# actions = ActionChains(_driver)
# element = _driver.find_element(By.CSS_SELECTOR, "button#start")
# actions = actions.move_to_element(element)
# button_ = MouseButtonDict["left"]
# for _ in range(10) :
# 	(actions.w3c_actions.pointer_action
# 	 .pointer_down(button_)
# 	 .pause(0.125)
# 	 .pointer_up(button_)
# 	 .pause(0.1))
# actions.perform()
# # actions.w3c_actions.pointer_action.click(element, MouseButton.RIGHT)
# # actions.w3c_actions.perform()
# actions.pause(10)
