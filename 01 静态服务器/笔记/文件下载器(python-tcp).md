文件下载器
=====
&nbsp;&nbsp;&nbsp;&nbsp;在写整个小项目之前，我们需要确定，需要用什么协议来写这个呢？是UDP还是TCP？
## 一、选UDP还是TCP？
&nbsp;&nbsp;&nbsp;&nbsp;我们知道，UDP是面向无连接的，即发送的信息是在不知道对方是否能接受到消息的情况下。而TCP是面向连接的，即发送信息是在已知对方一定能收到信息的情况下发送的。

&nbsp;&nbsp;&nbsp;&nbsp;并且文件是需要确保每个字节都需要发送到，因此如果选用UDP作为传输协议，那么很可能出现丢包的情况，导致传输过来的文件出现缺失。但是TCP就不会出现这样的情况，它的三次握手会确保客户端与服务器连接，并且确保每个字节都能传到。

**下面来整理一下TCP与UDP的区别**：
-   面向连接（确认有创建三方交握，连接已创建才作传输。）
-   有序数据传输
-   重发丢失的数据包
-   舍弃重复的数据包
-   无差错的数据传输
-   阻塞/流量控制

那么接下来我们就用TCP协议来写一个文件下载器

二、文件下载器-客户端
---------
### 2.1 客户端的基本流程

1. 创建套接字
2. 连接服务器
3. 发送/接收数据
4. 关闭客户端

### 2.2 本次客户端主要操作

1. 客户端与服务器相连
2. 发送需要下载的文件名
3. 服务器发送相应的内容：
   1. 如果服务器存在该文件，则返回该文件经过编码的二进制内容，并且客户端在本地创建相应的文件名，然后将内容输入。
   2. 如果服务器不存在该文件，则不进行任何操作

### 2.3 代码

```python
# -*- coding: utf-8 -*-
from socket import *


def main():
    # 创建socket
    tcp_client_socket = socket(AF_INET, SOCK_STREAM)

    # 目的信息,当然如果是自己测试完全不需要这样走
    server_ip = input("请输入服务器ip:")
    server_port = int(input("请输入服务器port:"))

    # 链接服务器
    tcp_client_socket.connect((server_ip, server_port))

    # 输入需要下载的文件名
    file_name = input("请输入要下载的文件名：")

    # 发送文件下载请求,因为自己电脑为win系统，如果是linux或者mac则将该编码格式转化为UTF-8即可
    tcp_client_socket.send(file_name.encode("gbk"))

    # 接收对方发送过来的数据，最大接收1024个字节（1K）
    recv_data = tcp_client_socket.recv(1024)
    # print('接收到的数据为:', recv_data.decode('utf-8'))
    
    # 如果接收到数据再创建文件，否则不创建
    # 这里注意，使recv解堵塞有两种方式，1.客户端发送过来数据，2.服务端主动调用close。
    # 因此如果使recv被赋值，要么有文件，服务器发送过来数据，要么没文件呢，服务器调用socket.close使得返回一个空字符。
    if recv_data:
        with open("[接收]" + file_name, "wb") as f:
            f.write(recv_data)

    # 关闭套接字
    tcp_client_socket.close()


if __name__ == "__main__":
    main()

```

## 三、文件下载器-服务器

### 3.1 客户端的基本流程

1. 创建套接字
2. 绑定ip与端口
3. 将套接字从主动变为被动（listen）
4. accept等待客户端连接
5. 发送/接收数据
6. 关闭服务器

### 3.2 本次服务器的主要操作

1. 等待客户端连接
2. 接收客户端发送过来的文件名
3. 在服务器内部查找是否存在该文件
   1. 如果存在，则返回文件内容给客户端
   2. 如果不存在，则直接关闭新的套接字

### 3.3 代码

```python
# -*- coding: utf-8 -*-
from socket import *
import sys


def get_file_content(file_name):
    """获取文件的内容"""
    try:
        with open(file_name, "rb") as f:
            content = f.read()
        return content
    except:
        print("没有下载的文件:%s" % file_name)


def main():
    if len(sys.argv) != 2:
        print("请按照如下方式运行：python3 xxx.py 7890")
        return
    else:
        # 运行方式为python3 xxx.py 7890
        port = int(sys.argv[1])

    # 创建socket
    tcp_server_socket = socket(AF_INET, SOCK_STREAM)
    # 本地信息，当然也可以自己直接输入port
    address = ('', port)
    # 绑定本地信息
    tcp_server_socket.bind(address)
    # 将主动套接字变为被动套接字，这里的listen内的数字时同一时刻服务器可与128个客户端进行相连
    tcp_server_socket.listen(128)

    while True:
        # 等待客户端的链接，即为这个客户端发送文件
        client_socket, clientAddr = tcp_server_socket.accept()
        # 接收对方发送过来的数据
        recv_data = client_socket.recv(1024)  # 接收1024个字节
        file_name = recv_data.decode("utf-8")
        print("对方请求下载的文件名为:%s" % file_name)
        file_content = get_file_content(file_name)
        
        # 因为获取打开文件时是以rb方式打开，所以file_content中的数据已经是二进制的格式，因此不需要encode编码
        if file_content:  # 如果文件存在，则发送文件的数据给客户端
            client_socket.send(file_content)
        # 不然关闭这个套接字
        client_socket.close()

    # 关闭监听套接字
    tcp_server_socket.close()


if __name__ == "__main__":
    main()

```







