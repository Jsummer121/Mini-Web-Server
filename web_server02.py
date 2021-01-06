# -*- coding: utf-8 -*-
import re
import socket
import multiprocessing
import time

from dynamic import my_web


class WSGIServer:
	def __init__(self):
		# 创建套接字
		self.http_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# 设置当服务器先close 即服务器端4次挥手之后资源能够立即释放，这样就保证了，下次运行程序时 可以立即绑定7890端口
		self.http_socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		# 绑定端口
		self.http_socket_server.bind(("", 7890))
		# 改主动为被动
		self.http_socket_server.listen(128)
	
	def run_forever(self):
		# 接受客户端响应
		while True:
			clint_socket, clint_addr = self.http_socket_server.accept()
			p = multiprocessing.Process(target=self.recv, args=(clint_socket,))
			p.start()
			clint_socket.close()
	
	def recv(self, clint_socket):
		# 获取客户端发送的信息
		recv_data = clint_socket.recv(1024).decode('utf-8')
		print(recv_data)  # 获取该信息的第一行GET / HTTP/1.1
		request_header_line_0 = recv_data.splitlines()[0]
		
		# 从客户端发送的信息中获取客户端想要的资源
		get_file_name = re.match(r"[^/]+(/[^ ]*)", request_header_line_0).group(1)
		# print("clint want file_name is %s" % get_file_name)
		
		if get_file_name == "/":
			file_name = g_static_document_root + "/index.html"
		else:
			file_name = g_static_document_root + get_file_name
		
		# 如果文件不是以py结尾，说明请求的是静态文件
		if not file_name.endswith(".py"):
			try:
				# 如果存在资源，将资源发送给对方
				f = open(file_name, "rb")
			except IOError:
				# 如果不存在资源，则发送404响应
				response_headers = "HTTP/1.1 404 NOT FOUND\r\n"
				page_404 = g_static_document_root + "/404.html"
				f = open(page_404, "rb")
			else:
				response_headers = "HTTP/1.1 200 OK\r\n"
			
			finally:
				resopnse_body = f.read()
				f.close()
				response_headers += "Content-Length: %d\r\n" % len(resopnse_body)
				response_headers += "\r\n"
				clint_socket.send(response_headers.encode('utf-8'))
				# 再发送body
				clint_socket.send(resopnse_body)
				# 关闭套接字
				clint_socket.close()
		# 客户端请求py（动态文件）
		else:
			# 利用WSGI协议写动态文件
			env = dict()
			# 合并header和body
			response_body = my_web.application(env, self.set_response_headers)
			response_header = "HTTP/1.1 {status}\r\n".format(status=self.headers[0])
			response_header += "Content-Type: text/html; charset=utf-8\r\n"
			response_header += "Content-Length: %d\r\n" % len(response_body)
			for temp_head in self.headers[1]:
				response_header += "{0}:{1}\r\n".format(*temp_head)
			
			response = response_header + "\r\n"
			response += response_body
			
			clint_socket.send(response.encode('utf-8'))
			
	def set_response_headers(self, status, headers):
		"""这个方法，会在 web框架中被默认调用"""
		response_header_default = [("Data", time.ctime()), ("Server", "ItCast-python mini dynamic server")]
		
		# 将状态码/相应头信息存储起来
		# [字符串, [xxxxx, xxx2]]
		self.headers = [status, response_header_default + headers]


# 设置静态资源访问的路径
g_static_document_root = "./html"


def main():
	server = WSGIServer()
	server.run_forever()


if __name__ == '__main__':
	main()
