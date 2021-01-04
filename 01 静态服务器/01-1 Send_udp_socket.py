# -*- coding: utf-8 -*-
import socket


def sendMsg():
    # 获取套接字
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 为套接字绑定端口与ip
    """
        这里的""是表示当前绑定的ip为本机的ip，后面的数字为该程序所绑定的端口号。
        如果不提前绑定端口号，则可能发送的时候，有电脑自动为该程序分发一个端口号。
    """
    send_socket.bind(("", 7879))

    # 设置发送
    send_socket.sendto(b"123", ("127.0.0.1", 7878))

    # 关闭套接字
    send_socket.close()


if __name__ == '__main__':
    sendMsg()
