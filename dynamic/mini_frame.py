import re

g_url_route = dict()


def route(url):
	def set_func(func):
		g_url_route[url] = func
		
		def call_func(*args, **kwargs):
			return func(*args, **kwargs)
		
		return call_func
	
	return set_func


@route("/index.py")
def index():
	with open("./templates/index.html") as f:
		content = f.read()
	
	my_stock_info = "哈哈哈哈 这是你的本月名称....."
	
	content = re.sub(r"\{%content%\}", my_stock_info, content)
	
	return content


@route("/center.py")
def center():
	with open("./templates/center.html") as f:
		content = f.read()
	
	my_stock_info = "这里是从mysql查询出来的数据。。。"
	
	content = re.sub(r"\{%content%\}", my_stock_info, content)
	
	return content


def application(env, start_response):
	start_response('200 OK', [('Content-Type', 'text/html;charset=utf-8')])
	
	file_name = env['PATH_INFO']
	# file_name = "/index.py"
	
	try:
		return g_url_route[file_name]()
	except Exception as ret:
		return "%s" % ret
