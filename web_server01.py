# -*- coding: utf-8 -*-
import re
import socket
import multiprocessing
import dynamic


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
			response_headers += "\r\n"
			resopnse_body = f.read()
			f.close()
			clint_socket.send(response_headers.encode('utf-8'))
			# 再发送body
			clint_socket.send(resopnse_body)
			# 关闭套接字
			clint_socket.close()


# 设置静态资源访问的路径
g_static_document_root = "./html"


def main():
	server = WSGIServer()
	server.run_forever()


if __name__ == '__main__':
	main()
