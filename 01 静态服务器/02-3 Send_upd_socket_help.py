# -*- coding: utf-8 -*-
import socket


def sendMsg():
    # 获取套接字
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 设置发送
    send_socket.sendto(b"123", ("127.0.0.1", 7891))

    # 关闭套接字
    send_socket.close()


if __name__ == '__main__':
    sendMsg()
