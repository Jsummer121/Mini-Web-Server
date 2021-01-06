# -*- coding: utf-8 -*-
import time
import socket
import sys
import re
import multiprocessing


class WSGIServer(object):
	"""定义一个WSGI服务器的类"""
	
	def __init__(self, port, documents_root, app):
		
		# 1. 创建套接字
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# 2. 绑定本地信息
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server_socket.bind(("", port))
		# 3. 变为监听套接字
		self.server_socket.listen(128)
		
		# 设定静态资源文件的路径
		self.documents_root = documents_root
		
		# 设定web框架可以调用的函数(对象)【即动态文件】
		self.app = app
	
	def run_forever(self):
		"""运行服务器"""
		
		# 等待对方链接
		while True:
			new_socket, new_addr = self.server_socket.accept()
			# 创建一个新的进程来完成这个客户端的请求任务
			# new_socket.settimeout(3)  # 3s
			new_process = multiprocessing.Process(target=self.deal_with_request, args=(new_socket,))
			new_process.start()
			new_socket.close()
	
	def deal_with_request(self, client_socket):
		"""以长链接的方式，为这个浏览器服务器"""
		while True:
			try:
				request = client_socket.recv(1024).decode("utf-8")
			except Exception as ret:
				print("========>", ret)
				client_socket.close()
				return
			
			# 判断浏览器是否关闭
			if not request:
				client_socket.close()
				return
			
			# 查看请求的内容
			request_lines = request.splitlines()
			for i, line in enumerate(request_lines):
				print(i, line)
			
			# 提取请求的文件(index.static)
			# GET /a/b/c/d/e/index.static HTTP/1.1
			ret = re.match(r"([^/]*)([^ ]+)", request_lines[0])
			if ret:
				print("正则提取数据:", ret.group(1))
				print("正则提取数据:", ret.group(2))
				file_name = ret.group(2)
				if file_name == "/":
					file_name = "/index.html"
			
			# 如果不是以py结尾的文件，认为是普通的文件
			if not file_name.endswith(".py"):
				
				try:
					# 如果存在资源，将资源发送给对方
					f = open(self.documents_root + file_name, "rb")
				except IOError:
					# 如果不存在资源，则发送404响应
					response_headers = "HTTP/1.1 404 NOT FOUND\r\n"
					f = open(self.documents_root + "/404.html", "rb")
				else:
					response_headers = "HTTP/1.1 200 OK\r\n"
				finally:
					resopnse_body = f.read()
					f.close()
					response_headers += "Content-Length: %d\r\n" % len(resopnse_body)
					response_headers += "\r\n"
					client_socket.send(response_headers.encode('utf-8'))
					# 再发送body
					client_socket.send(resopnse_body)
			
			# 以.py结尾的文件，就认为是浏览需要动态的页面
			else:
				# 准备一个字典，里面存放需要传递给web框架的数据
				env = {}
				# 存web返回的数据
				response_body = self.app(env, self.set_response_headers)
				
				# 合并header和body
				response_header = "HTTP/1.1 {status}\r\n".format(status=self.headers[0])
				response_header += "Content-Type: text/html; charset=utf-8\r\n"
				response_header += "Content-Length: %d\r\n" % len(response_body)
				for temp_head in self.headers[1]:
					response_header += "{0}:{1}\r\n".format(*temp_head)
				
				response = response_header + "\r\n"
				response += response_body
				
				client_socket.send(response.encode('utf-8'))
	
	def set_response_headers(self, status, headers):
		"""这个方法，会在 web框架中被默认调用"""
		response_header_default = [("Data", time.ctime()), ("Server", "ItCast-python mini dynamic server")]
		
		# 将状态码/相应头信息存储起来
		# [字符串, [xxxxx, xxx2]]
		self.headers = [status, response_header_default + headers]


# 设置静态资源访问的路径
g_static_document_root = "./html"
# 设置动态资源访问的路径
g_dynamic_document_root = "./dynamic"


def main():
	# 把该路径放入路径下
	sys.path.append(g_dynamic_document_root)
	# 设置端口号，动态库名称和函数名
	port = 7890
	web_frame_module_name = "my_web"
	app_name = "application"
	
	# 导入web框架的主模块
	web_frame_module = __import__(web_frame_module_name)
	# 获取那个可以直接调用的函数(对象)
	app = getattr(web_frame_module, app_name)
	
	# 启动http服务器
	http_server = WSGIServer(port, g_static_document_root, app)
	# 运行http服务器
	http_server.run_forever()


if __name__ == "__main__":
	main()
