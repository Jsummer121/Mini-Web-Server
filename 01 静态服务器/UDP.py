# -*- coding: utf-8 -*-
import socket


def main():
    # 创建udp套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 绑定端口与ip
    local_addr = ("", 8080)
    udp_socket.bind(local_addr)

    # 可以使用套接字发送数据
    # udp_socket.sendto(b"hello summer", ("127.0.0.1", 3000))
    send_data = input("请输入要发送的数据：")
    udp_socket.sendto(send_data.encode("utf-8"), ("127.0.0.1", 3000))

    # 也可以使用套接字接收数据
    recv_data = udp_socket.recvfrom(1024)  # 1024表示本次接受的最大字节数
    # 它收到的是如下元组类型的数据(b"hello summer", ("127.0.0.1", 3000))
    # 显示接受到的数据
    print(recv_data[0].decode("gbk"))

    # 可以关闭套接字
    udp_socket.close()


if __name__ == '__main__':
    main()
