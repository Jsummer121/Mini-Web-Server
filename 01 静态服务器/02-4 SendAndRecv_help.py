# -*- coding: utf-8 -*-
import socket


def SendAndRecv():
    """
    套接字是可以同时收发数据的
        单工：只能收或者发
        半双工：可以收也可以发，但是不能同时运行
        全双工：同一时刻既可以收也可以发
    注意：socket是全双工
    """
    # 获取套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 绑定端口（也可以不绑定，只需要查看发送时的端口号，在重新输入即可，但是这个程序最好提前绑定端口
    udp_socket.bind(("", 7890))

    # 发送对方信息
    udp_socket.sendto(b"hahahah", ("127.0.0.1", 7891))

    # 接收对方返回的信息,如果没有收到字符，则会阻塞，直到有信息返回
    recv_data = udp_socket.recvfrom(1024)

    # 转化打印出内容
    print("接收到来自{}，的{}信息".format(recv_data[1], recv_data[0].decode("gbk")))

    # 关闭套接字
    udp_socket.close()


if __name__ == '__main__':
    SendAndRecv()
