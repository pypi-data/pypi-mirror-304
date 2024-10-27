def replace(text :str,old :str,new :str,num :int) -> str:
	"""
	字符串替换。
	:param text: 文本
	:param old: 原始字符串
	:param new: 替换字符串
	:param num: 替换次数，可省略，默认-1为全部替换
	:return:
	"""
	pass
def bracket(text :str,pairsRaw :object) -> bool:
	"""
	检查字符串中的括号是否闭合。
	"""
	pass
def cut(text :str,sep :str,reverse :bool) -> tuple[str,str]:
	"""
	将字符串按指定字符串切分为两部分。
	"""
	pass
def split(s :str,substr :str) -> object:
	"""
	将字符串按指定字符串切分为多个部分。
	"""
	pass
def format(s :str,args :object) -> str:
	"""
	格式化字符串，格式与go相同。
	"""
	pass
def join(parts :object,sep :str) -> str:
	"""
	以指定字符串为间隔拼接多个字符串。
	"""
	pass
def trim_left(s :str,cutset :str) -> str:
	"""
	移除字符串左侧所有包含在移除字符集中的字符。
	"""
	pass
def trim(s :str,cutset :str) -> str:
	"""
	移除字符串中所有包含在移除字符集中的字符。
	"""
	pass
def format_split(text :str,formatStr :str,leftSep :str,rightSep :str) -> object:
	"""
	按照指定模式在字符串中匹配符合模式的所有结果。
	"""
	pass
def match(text :str,left :str,right :str,whole :bool) -> object:
	"""
	匹配文本中满足条件的全部文本。
	:param left: 左侧文本 
	:param right: 右侧文本
	:param text: 需要匹配的文本
	:return: 返回包含结果的字符串列表
	"""
	pass
def is_upper(s :str) -> bool:
	"""
	检查一个字符串首字母是否大写。
	"""
	pass
def trim_right(s :str,cutset :str) -> str:
	"""
	移除字符串右侧所有包含在移除字符集中的字符。
	"""
	pass
def pascal_to_snake(s :str) -> str:
	"""
	将驼峰字符串转为蛇形。
	Eg. AaBbCc -> aa_bb_cc
	"""
	pass