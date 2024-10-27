class Manager:
	def __init__(self,distribute :object,execute :object) -> object:
		"""
		实例化多线程管理器。需要提供分发函数与执行函数。
		"""
		pass
	def handle_result(self,middleware :object) -> object:
		"""
		设置结果收集中间件。
		"""
		pass
	def handle_error(self,f :object) -> object:
		"""
		设置错误处理函数。
		"""
		pass
	def run(self,threads :int) -> object:
		"""
		启动。
		"""
		pass
	pass
class DistributeController:
	def stop(self) -> object:
		"""
		停止执行。
		"""
		pass
	def add_task(self,a :object) -> object:
		"""
		增加任务。
		"""
		pass
	pass
class ExecuteController:
	def stop(self) -> object:
		"""
		停止执行。
		"""
		pass
	def retry(self,a :object) -> object:
		"""
		重试任务。
		"""
		pass
	pass