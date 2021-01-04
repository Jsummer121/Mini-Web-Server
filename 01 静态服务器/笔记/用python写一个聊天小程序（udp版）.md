@[]()

## 1.UDP简介

​		Internet协议集支持一个无连接的传输协议，该协议称为用户数据报协议（UDP）。UDP为应用程序提供了无需建立就可以发送封装的IP数据包的方法。

​		Internet的传输层有两个协议，互为补充。无连接是UDP，它除了给应用程序发送数据包功能并允许他们所需的层次上架构自己的协议之外，几乎没有做什么特别的事情。面向连接的是TCP，该协议几乎做了所有的事情。

中文名：用户数据协议

外文名：User Datagram Protocol

特点：无连接、不可靠、快速传输

基础：IP数据包服务上增加一点功能

类别：传输层协议

用途：发送数据包

## 2.socket

​		一般socket我们称为套接字，并且在Python中有socket这个库（可以使用pip命令自行下载`pip install socket`）。下面来说一下socket的简单流程

1. 获取套接字
2. 绑定端口
3. 选择发送或者接受
4. 关闭套接字

### 2-1 socket的发送

socket的发送很简单，下面是一般的最简代码：



```python
# -*- coding: utf-8 -*-
import socket


def sendMsg():
    # 获取套接字
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 为套接字绑定端口与ip
    # 这里的""是表示当前绑定的ip为本机的ip，后面的数字为该程序所绑定的端口号。
    # 如果不提前绑定端口号，则可能发送的时候，有电脑自动为该程序分发一个端口号。
    send_socket.bind(("", 7879))  # 当然这个端口也可以是7878，即发送的端口，后续会继续讲解 

    # 设置发送
    send_socket.sendto(b"123", ("127.0.0.1", 7878))

    # 关闭套接字
    send_socket.close()


if __name__ == '__main__':
    sendMsg()
```

### 2-2 socket的接收

注意，在recv中，一定需要提前绑定端口，因为这是接收消息的前提条件，那么选用什么端口呢？一般做实验或者写程序的时候，我们可以选择的端口范围在（1024-65535）之间。因为上面已经创建了socket的发送，并且选定了端口号为7878，那么我们此时的端口只需要绑定7878即可。

recv_socket.recvfrom(1024)表示单次接受的最大字节为1024，如果超出这个数值，那么只取前面的1024个。并且该函数返回的值是一个元组，与socket发送时一致`(b"123", ("127.0.0.1", 7878))`，因此在想要获取接受的内容是，需要利用下标索引。这里还需要注意一点，因为我们在传输的时候是靠字节去传输的，因此获取到的也是字节，我们需要为它进行编码，但是win系统与linux系统是不相同的，win系统默认的是gbk编码，但是linux默认的是utf-8编码，因此在获取字节之后，需要根据系统的类型选择相应的解码格式。

```python
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
    print("接收到来自{}，的{}信息".format(recv_data[1],recv_data[0].decode("gbk")))

    # 关闭套接字
    recv_socket.close()


if __name__ == '__main__':
    recvMsg()

```

## 3.实现收发功能

​		我们需要提前了解一些知识点：单工：只能收或者发、半双工：可以收也可以发，但是不能同时运行、全双工：同一时刻既可以收也可以发。并且socket是支持同时接收与发送数据的，因此socket是全双工的。

​		下面代码是实现socket的发送与接收功能

```python
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
    udp_socket.bind(("", 7891))

    # 发送对方信息
    udp_socket.sendto(b"hahahah", ("127.0.0.1", 7890))

    # 接收对方返回的信息,如果没有收到字符，则会阻塞，直到有信息返回
    recv_data = udp_socket.recvfrom(1024)

    # 转化打印出内容
    print("接收到来自{}，的{}信息".format(recv_data[1], recv_data[0].decode("utf-8")))

    # 关闭套接字
    udp_socket.close()


if __name__ == '__main__':
    SendAndRecv()

```

上面代码的确看起来有点“丑陋”我们来给他进行一些封装

```python
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

```

以上代码实现了程序的接受和发送。但是我们需要写两个程序来验证是否能执行吧，以下两个就是发送的检测代码和接收的检测代码。

```python
# -*- coding: utf-8 -*-
import socket


def recvMsg():
    # 创建套接字
    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 绑定端口
    recv_socket.bind(("", 7890))

    # 接收字节
    recv_data = recv_socket.recvfrom(1024)  # 这里的数字表示单次接受的最大字节数

    # 转化打印出内容
    print("接收到来自{}，的{}信息".format(recv_data[1],recv_data[0].decode("gbk")))

    # 关闭套接字
    recv_socket.close()


if __name__ == '__main__':
    recvMsg()

```

上面的代码是主程序接收是否能实现。

```python
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

```

​		上面的代码是主程序发送是否能实现。

​		当然为了严谨，同样可以在main函数里加上while True进行无限循环来验证，并且可以用户手动输入需要发送的ip地址、端口号、发送内容。这里就不一一写出来了，剩下的就留给大家了。

​		以上就是python利用socket写的聊天小程序。思路比较简单，代码也比较容易上手。tcp也是重点（后续会发），多多复习多多练习哟。