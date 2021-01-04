# -*- coding: utf-8 -*-
from socket import *


def main():
    # 创建tcp服务器的基本流程：
    # 1.socket创建套接字
    tcp_server_socket = socket(AF_INET, SOCK_STREAM)

    # 2.绑定ip和端口
    address = ("", 7788)
    tcp_server_socket.bind(address)

    # 3.listen使用套接字变成可以被动链接
    # 使用socket创建的套接字默认的属性是主动的，使用listen将其变成被动的，这样就可以接受别人的链接了
    tcp_server_socket.listen(128)

    # 4.accept等待客户端的连接
    client_socket, clientAdd = tcp_server_socket.accept()

    # 5.recv/send接收发送数据
    # 接受对方发送过来的数据
    recv_data = client_socket.recv(1024)  # 接收24个字节
    print("接收到的数据为：", recv_data.decode("gbk"))

    # 发送给对方数据
    client_socket.send("Thank You!".encode("gbk"))

    # 6.关闭客户端的套接字
    tcp_server_socket.close()
    client_socket.close()


if __name__ == '__main__':
    main()
