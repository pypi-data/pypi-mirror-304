def new_ssh(addr :str,username :str,passwdOrId_rsa :str) -> object:
	"""
	连接ssh。
	"""
	pass
def request(method :str,targetUrl :str,params :object,data :object,headers :object,verify :bool,proxyStr :str,timeout :int) -> object:
	"""
	发起请求。
	"""
	pass
def ssh(addr :str,username :str,passwdOrId_rsa :str) -> None:
	"""
	连接ssh。
	"""
	pass
def ssh_run(addr :str,username :str,passwdOrId_rsa :str,command :str) -> None:
	"""
	通过ssh执行命令。
	"""
	pass
def ssh_exec(addr :str,username :str,passwdOrId_rsa :str,command :str) -> str:
	"""
	通过ssh执行命令并获取执行结果。
	"""
	pass
GET= None #GET Method
POST= None #POST Method
class SSH:
	def exec_command(self,command :str) -> str:
		"""
		执行命令。
		"""
		pass
	def close(self) -> object:
		"""
		关闭连接。
		"""
		pass
	pass
class HTTPRequest:
	def __init__(self,data :object) -> object:
		"""
		实例化一个HTTP请求对象。
		"""
		pass
	def header(self,header :object) -> object:
		"""
		获取或设置请求头。
		"""
		pass
	def body(self,body :object) -> object:
		"""
		获取或设置请求体。
		"""
		pass
	def raw_query(self,query :object) -> str:
		"""
		获取原始query。
		"""
		pass
	def method(self,method :object) -> str:
		"""
		获取或设置请求方式。
		"""
		pass
	def proto(self,p :object) -> str:
		"""
		获取或设置协议。
		"""
		pass
	def to_request(self) -> object:
		"""
		——
		"""
		pass
	def path(self,path :object) -> str:
		"""
		获取路径。
		"""
		pass
	def query(self,k :object,v :object,diableCover :bool) -> object:
		"""
		获取或获取请求中的GET参数。
		"""
		pass
	def url(self) -> str:
		"""
		获取URL。
		"""
		pass
	pass
class HTTPResponse:
	def __init__(self,data :object,req :object) -> object:
		"""
		实例化一个HTTP响应对象。
		"""
		pass
	def to_response(self) -> object:
		"""
		——
		"""
		pass
	def status(self,text :object) -> str:
		"""
		获取或设置状态。
		"""
		pass
	def status_code(self,code :object) -> int:
		"""
		获取或设置状态码。
		"""
		pass
	def header(self,header :object) -> object:
		"""
		获取或设置响应头。
		"""
		pass
	def body(self,body :object) -> object:
		"""
		获取或设置响应体。
		"""
		pass
	def request(self) -> object:
		"""
		获取生成该响应的请求。
		"""
		pass
	pass
class HTTPProxyServer:
	def __init__(self,handleReq :object,handleResp :object,caRootPath :str) -> object:
		"""
		实例化一个HTTP代理对象。
		"""
		pass
	def start(self,addr :str,proxy :str,verbose :bool) -> None:
		"""
		启动代理。
		"""
		pass
	pass
class WebSocketServer:
	def __init__(self,handler :object,welcome :str) -> object:
		"""
		实例化一个WebSocket服务对象。
		"""
		pass
	def start(self,addr :str,path :str) -> None:
		"""
		启动WebSocket。
		"""
		pass
	pass