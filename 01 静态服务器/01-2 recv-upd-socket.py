# -*- coding: utf-8 -*-
import socket


def recvMsg():
    # 创建套接字
    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 绑定端口
    recv_socket.bind(("", 7878))

    # 接收字节
    recv_data = recv_socket.recvfrom(1024)  # 这里的数字表示单次接受的最大字节数

    # 转化打印出内容
    print("接收到来自{}，的{}信息".format(recv_data[1],recv_data[0].decode("utf-8")))

    # 关闭套接字
    recv_socket.close()


if __name__ == '__main__':
    recvMsg()
