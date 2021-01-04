# Python—socket：TCP协议

在了解TCP协议之前，我们应该先知道TCP/IP是个啥东西。

## 一、TCP/IP协议族

&nbsp;&nbsp;&nbsp;&nbsp;计算机与网络设备要相互通信，双方就必须基于相同的方法。比如， 如何探测到通信目标、由哪一边先发起通信、使用哪种语言进行通 信、怎样结束通信等规则都需要事先确定。不同的硬件、操作系统之 间的通信，所有的这一切都需要一种规则。而我们就把这种规则称为协议（protocol），协议中存在各式各样的内容。

### 1.1 **TCP/IP** 的分层管理 

&nbsp;&nbsp;&nbsp;&nbsp;TCP/IP 协议族里重要的一点就是分层。TCP/IP 协议族按层次分别分 为以下 4 层：应用层、传输层、网络层和数据链路层。

### 1.2 TCP/IP 协议族各层的作用

- 应用层

&nbsp;&nbsp;&nbsp;**&nbsp;决定了向用户提供应用服务时通信的活动。** 

&nbsp;&nbsp;&nbsp;&nbsp;TCP/IP 协议族内预存了各类通用的应用服务。比如，FTP（File Transfer Protocol，文件传输协议）和 DNS（Domain Name System，域名系统）服务就是其中两类。 

- 传输层：两个联网的计算机之间的数据传输

&nbsp;&nbsp;&nbsp;**&nbsp;传输层对上层应用层，提供处于网络连接中的两台计算机之间的数据** 

传输。 在传输层有两个性质不同的协议：TCP（Transmission Control Protocol，传输控制协议）和 UDP（User Data Protocol，用户数据报 协议）。 

- 网络层(又称网络互联层)

&nbsp;&nbsp;**&nbsp;&nbsp;网络层用来处理在网络上流动的数据包。**数据包是网络传输的最小数 据单位。该层规定了通过怎样的路径（所谓的传输路线）到达对方计 算机，并把数据包传送给对方。 

&nbsp;&nbsp;&nbsp;&nbsp;与对方计算机之间通过多台计算机或网络设备进行传输时，网络层所 起的作用就是在众多的选项内选择一条传输路线。 

- 链路层（又名数据链路层，网络接口层） 

&nbsp;&nbsp;&nbsp;&nbsp;**&nbsp;用来处理连接网络的硬件部分。**包括控制操作系统、硬件的设备驱 动、NIC（Network Interface Card，网络适配器，即网卡），及光纤等 物理可见部分（还包括连接器等一切传输媒介）。硬件上的范畴均在链路层的作用范围之内。 

### 1.3 **TCP/IP** 通信传输流 

&nbsp;&nbsp;&nbsp;&nbsp;利用 TCP/IP 协议族进行网络通信时，会通过分层顺序与对方进行通信。发送端从应用层往下走，接收端则往应用层往上走。 

&nbsp;&nbsp;&nbsp;&nbsp;我们用 HTTP 举例来说明，首先作为发送端的客户端在应用层 （HTTP 协议）发出一个想看某个 Web 页面的 HTTP 请求。 

&nbsp;&nbsp;&nbsp;&nbsp;接着，为了传输方便，在传输层（TCP 协议）把从应用层处收到的数据（HTTP 请求报文）进行分割，并在各个报文上打上标记序号及端 口号后转发给网络层。 

&nbsp;&nbsp;&nbsp;&nbsp;在网络层（IP 协议），增加作为通信目的地的 MAC 地址后转发给链路层。这样一来，发往网络的通信请求就准备齐全了。 

&nbsp;&nbsp;&nbsp;&nbsp;接收端的服务器在链路层接收到数据，按序往上层发送，一直到应用层。当传输到应用层，才能算真正接收到由客户端发送过来的 HTTP 请求。 

&nbsp;&nbsp;&nbsp;&nbsp;发送端在层与层之间传输数据时，每经过一层时必定会被打上一个该层所属的首部信息。反之，接收端在层与层传输数据时，每经过一层 时会把对应的首部消去。 

&nbsp;&nbsp;&nbsp;&nbsp;这种把数据信息包装起来的做法称为封装（encapsulate）。 

## 二、IP协议

&nbsp;&nbsp;&nbsp;&nbsp;作用：把各种数据包传送给对方

&nbsp;&nbsp;&nbsp;&nbsp;IP地址指明了节点被分配到的地址，MAC地址是网卡所属的固定地址，IP地址可以和MAC地址进行配对，IP地址可变化，但MAC地址基本上不会发生改变。

## 三、TCP协议

&nbsp;&nbsp;&nbsp;&nbsp;按层次分，TCP 位于传输层，提供可靠的字节流服务。 

&nbsp;&nbsp;&nbsp;&nbsp;所谓的字节流服务（Byte Stream Service）是指，为了方便传输，将大 块数据分割成以报文段（segment）为单位的数据包进行管理。而可 靠的传输服务是指，能够把数据准确可靠地传给对方。一言以蔽之， TCP 协议为了更容易传送大数据才把数据分割，而且 TCP 协议能够确认数据最终是否送达到对方。 

&nbsp;&nbsp;&nbsp;&nbsp;为了准确无误地将数据送达目标处，TCP 协议采用了**三次握手** （three-way handshaking）策略。用 TCP 协议把数据包送出去后，TCP不会对传送后的情况置之不理，它一定会向对方确认是否成功送达。

### 3.1 三次握手

&nbsp;&nbsp;&nbsp;&nbsp;握手过程中使用了 TCP 的标志（flag） —— SYN（synchronize） 和 ACK（acknowledgement）。 

&nbsp;&nbsp;&nbsp;&nbsp;发送端首先发送一个带 SYN 标志的数据包给对方。接收端收到后， 回传一个带有 SYN/ACK 标志的数据包以示传达确认信息。最后，发 送端再回传一个带 ACK 标志的数据包，代表“握手”结束。 

&nbsp;&nbsp;&nbsp;&nbsp;若在握手过程中某个阶段莫名中断，TCP 协议会再次以相同的顺序发送相同的数据包。 

## 四、python实现tcp网络通信

### 4.1 tcp客户端（client）

&nbsp;&nbsp;&nbsp;&nbsp;**实现客户端的基本流程**：

- 创建套接字（socket.AF_INET, socket.SOCK_STREAM）
- 绑定端口
- 接收/发送数据
- 关闭套接字

```python
# -*- coding: utf-8 -*-
import socket


def main():
    # 1.创建套接字
    tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2.绑定服务器
    # tcp_client_socket.connect(("127.0.0.1", 7878))
    server_ip = input("请输入要链接的服务器：")
    server_port = int(input("请输入链接服务器的端口："))
    server_addr = (server_ip, server_port)
    tcp_client_socket.connect(server_addr)

    # 3.发送数据
    send_data = input("请输入要发送的数据：")
    tcp_client_socket.send(send_data.encode("gbk"))

    # 4.关闭套接字
    tcp_client_socket.close()


if __name__ == '__main__':
    main()

```

### 4.2 tcp服务端(server)

&nbsp;&nbsp;&nbsp;**实现服务端的基本流程**：

- 创建套接字（AF_INET,SOCK_STREAM)
- 绑定端口
- 将套接字从主动变为被动（listen使用套接字变成可以被动链接）
- accept等待客户端连接
- 接收/发送数据
- 关闭套接字

```python
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
    # 128意味着同一时刻可以和128个客户端进行通信，这里注意一点，一般的服务器搭建都是linux，此时可以写多但是一般是128。
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

```

&nbsp;&nbsp;&nbsp;&nbsp;当然如果要实现多次为多个客户端服务，只需要添加两层while即可，代码如下：

```python
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
            # 如果recv接堵塞，有两种方式，1.客户端发送过来数据，2.客户端调用close。
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

```

## 五、tcp注意点

1. tcp服务器一般情况下都需要绑定，否则客户端找不到这个服务器
2. tcp客户端一般不绑定，因为是主动链接服务器，所以只要确定好服务器的ip、port等信息就好，本地客户端可以随机
3. tcp服务器中通过listen可以将socket创建出来的主动套接字变为被动的，这是做tcp服务器时必须要做的
4. 当客户端需要链接服务器时，就需要使用connect进行链接，udp是不需要链接的而是直接发送，但是tcp必须先链接，只有链接成功才能通信
5. 当一个tcp客户端连接服务器时，服务器端会有1个新的套接字，这个套接字用来标记这个客户端，单独为这个客户端服务
6. listen后的套接字是被动套接字，用来接收新的客户端的链接请求的，而accept返回的新套接字是标记这个新客户端的
7. 关闭listen后的套接字意味着被动套接字关闭了，会导致新的客户端不能够链接服务器，但是之前已经链接成功的客户端正常通信。
8. 关闭accept返回的套接字意味着这个客户端已经服务完毕
9. 当客户端的套接字调用close后，服务器端会recv解堵塞，并且返回的长度为0，因此服务器可以通过返回数据的长度来区别客户端是否已经下线

## 六、tcp与udp

**udp的创建流程**：

- socket（AF_INST,SOCK_DGRAM）
- bind（可选）
- sendto/recvfrom
- close

**tcp客户端创建流程：**

- skcket(AF_INST,SOCK_STREAM)
- connect
- send/recv
- close

**tcp服务器创建流程：**

- socket(AF_INST,SOCK_STREAM)
- bind
- listen
- accept
- recv/send
- close