import selenium.webdriver
from selenium.webdriver.common.by import By

from YAutoFramework.YUtils.POM.BaseObject import BaseObject

# class TestTC20018764(metaclass=TestMeta) :
# 	ID = 'TC234234'

driver = selenium.webdriver.Chrome()
driver.get(r"http://cps-test.bchrt.com/")
target = BaseObject(driver=driver, locator=(By.CSS_SELECTOR, 'button#start'))
target.wait_till_exists(timeout=10)
target.click(click_times=10, interval=125)
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
input()
