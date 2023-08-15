from YAutoFramework.YUtils.Ylogger import Ylogger


class YTestInfo :
	@staticmethod
	def Tester(name) :
		def wrapper(*args, **kwargs) :
			Ylogger.info()
