def is_file(path :str) -> bool:
	"""
	判断路径是否指向一个文件。
	"""
	pass
def wxapkg_unpack(decryptedData :str,beautify :bool,thread :int) -> object:
	"""
	对wxapkg字符串解码得到文件。
	"""
	pass
def save_excel(filePath :str,sheets :object) -> None:
	"""
	将Excel对象保存至路径。
	"""
	pass
def tag_extract(data :str) -> object:
	"""
	从字符串中提取所有标签。
	"""
	pass
def read_file(filePath :str) -> str:
	"""
	读取文件内容。
	"""
	pass
def walk_dir(pathname :str,suffix :str,recursion :bool) -> object:
	"""
	遍历指定目录下的所有文件及文件夹。默认不递归。
	"""
	pass
def toml_dump(s :object) -> str:
	"""
	将对象序列化为Toml字符串。
	"""
	pass
def load_excel(filePath :str,numList :bool) -> object:
	"""
	加载一个Excel表格。
	"""
	pass
def save_file(path :str,content :str,cover :bool) -> None:
	"""
	保存内容到指定路径。不存在会创建，默认不覆盖。
	"""
	pass
def is_dir(path :str) -> bool:
	"""
	判断路径是否指向一个文件夹。
	"""
	pass
def toml_loads(data :str) -> object:
	"""
	加载并解析Toml字符串。
	"""
	pass
class Excel:
	def __init__(self) -> object:
		"""
		实例化Excel对象。
		"""
		pass
	def get_sheet_names(self) -> object:
		"""
		获取所有表格的名字。
		"""
		pass
	def set_sheet(self,name :str,sheet :object) -> object:
		"""
		放置一个表格到Excel。
		"""
		pass
	def get_sheet(self,name :str) -> object:
		"""
		获取指定表格。
		"""
		pass
	pass
class Sheet:
	def __init__(self) -> object:
		"""
		实例化Sheet对象。
		"""
		pass
	def get_key_list(self) -> object:
		"""
		获取表头。
		"""
		pass
	def set_key_list(self,list :object) -> object:
		"""
		设置表头。
		"""
		pass
	def set_data(self,line :int,rawData :object) -> None:
		"""
		按行号填充数据。行号从1开始。
		"""
		pass
	def get_all_data(self) -> object:
		"""
		获取表格中的所有数据。
		"""
		pass
	pass