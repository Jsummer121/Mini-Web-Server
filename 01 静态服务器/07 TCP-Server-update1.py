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

    while True:  # 循环为多个客户端服务
        # 4.accept等待客户端的连接
        print("等待新的客户端到来")
        client_socket, clientadd = tcp_server_socket.accept()
        print("一个新的客户端已经到来")

        while True:  # 循环多次为同一个客户端服务多次
            # 5.recv/send接收发送数据
            # 接受对方发送过来的数据
            # 如果recv解堵塞，有两种方式，1.客户端发送过来数据，2.客户端调用close。
            recv_data = client_socket.recv(1024)  # 接收1024个字节，如果客户端关闭，意味着对方调用了close，此时返回的recv_data为空
            print("接收到的数据为：%s" % (recv_data.decode("gbk")))
            if recv_data:
                # 发送给对方数据
                client_socket.send("Thank You!".encode("gbk"))
            else:
                break

        # 6.关闭客户端的套接字
        client_socket.close()

    tcp_server_socket.close()


if __name__ == '__main__':
    main()
