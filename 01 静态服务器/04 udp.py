# -*- coding: utf-8 -*-
import socket


def send_msg(udp_socket):
    """发送消息"""
    udp_socket.sendto(b'124124', ("127.0.0.1", 7788))


def recv_msg(udp_socket):
    """接收数据"""
    recv_data = udp_socket.recvfrom(1024)
    print("%s:%s" % (str(recv_data[1]), recv_data[0].decode("gbk")))  # 如果是win系统通信，需要把deckde的解码格式改为gbk，但是在linux中可以为utf-8


def main():
    # 创建套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 绑定端口
    udp_socket.bind(("", 7788))

    # 循环来处理事情
    while True:
        print("------DreamsPy聊天器------")
        print("1:发送消息")
        print("2:接收消息")
        print("0:退出系统")
        op = input("请输入功能：")

        if op == "1":
            # 发送
            send_msg(udp_socket)
        elif op == "2":
            # 接收数据并显示
            recv_msg(udp_socket)
        elif op == "0":
            break
        else:
            print("您输入的命令有误，请重新输入")


if __name__ == '__main__':
    main()
