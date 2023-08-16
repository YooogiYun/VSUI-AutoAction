from YAutoFramework.YUtils.Ylogger import GlobalLogger


class YTestInfo :
	@staticmethod
	def Tester(name) :
		def wrapper(*args, **kwargs) :
			GlobalLogger.info()
