# -*- coding: utf-8 -*-
import socket


def main():
    # 1.创建套接字
    tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2.绑定服务器
    # tcp_client_socket.connect(("127.0.0.1", 7878))
    server_ip = input("请输入要链接的服务器：")
    server_port = int(input("请输入链接服务器的端口："))
    server_addr = (server_ip, server_port)
    tcp_client_socket.connect(server_addr)

    # 3.发送数据
    send_data = input("请输入要发送的数据：")
    tcp_client_socket.send(send_data.encode("gbk"))

    # 4.关闭套接字
    tcp_client_socket.close()


if __name__ == '__main__':
    main()
