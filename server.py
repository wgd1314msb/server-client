import base64
import hashlib
import socket
import threading
import tkinter
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

win = tkinter.Tk()  # 创建主窗口
win.title('模拟服务器')
win.geometry("400x400+200+20")
users = {}#用户字典，也可以连接数据库

def run(ck, ca):
    userName = ck.recv(1024)#接受客户端发送的信息以1k作为单位这里接受到的信息为byte类型
    users[userName.decode("utf-8")] = ck#解码并储存用户的信息
    #print(users)
    printStr = "" + userName.decode("utf-8") + "连接\n"#在连接显示框中显示是否连接成功
    text.insert(tkinter.INSERT, printStr)
    keyStr=ekey.get()#获取密钥
    while True:
        rData = ck.recv(1024)  # 接受客户端发送的信息以1k作为单位这里接受到的信息为byte类型
        dataStr = rData.decode("utf-8")
        infolist = dataStr.split(":")  # 分割字符串从而得到所要发送的用户名和客户端所发送的信息
        if keyStr=="md5":
            str_len=infolist[1].encode("utf-8")
            h = hashlib.md5(str_len)
            h_en = h.hexdigest()#16进制
            pudata = userName.decode("utf-8") + "说" + infolist[1] + "\n"
            text.insert(tkinter.INSERT, pudata)
            text.insert(tkinter.INSERT, h_en)
            users[infolist[0]].send(
                (userName.decode("utf-8") + "说:" +str(h_en)+":"+keyStr+":"+ infolist[1]).encode("utf-8"))
        #要发送信息的客户端向目标客户端发送信息
        elif keyStr=="base64":
            str_len = infolist[1].encode("utf-8")
            b=base64.b64encode(str_len)
            text.insert(tkinter.INSERT, b)
            pudata = userName.decode("utf-8") + "说" + infolist[1] + "\n"
            text.insert(tkinter.INSERT, pudata)
            users[infolist[0]].send(
                (userName.decode("utf-8") + "说:" + str(b) + ":" + keyStr + ":" + infolist[1]).encode("utf-8"))
        elif keyStr=="aes":
            password = b'1234567812345678'  # 秘钥，b就是表示为bytes类型
            aes = AES.new(password, AES.MODE_ECB)
            aes_text = aes.encrypt(pad(infolist[1].encode("utf-8"), block_size=32))
            text.insert(tkinter.INSERT, aes_text)
            pudata = userName.decode("utf-8") + "说" + infolist[1] + "\n"
            text.insert(tkinter.INSERT, pudata)
            users[infolist[0]].send(
                (userName.decode("utf-8") + "说:"+keyStr +":"+ infolist[1]).encode("utf-8"))
        # users[infolist[0]].send(
        #     (userName.decode("utf-8") + "说:"+password.decode("utf-8")+":"+keyStr +":"+aes_text.decode("utf-8") +":"+ infolist[1]).encode("utf-8"))
        #比特流密码用utf-8没法加密
        else:
            error="输入密钥错误"
            text.insert(tkinter.INSERT, error)

def start():
    ipStr = eip.get()#从输入端中获取ip
    portStr = eport.get()#从输入端中获取端口，注意端口取得时候不能被占用（可以取8080，9876，等）
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#socked所准守ipv4或ipv6，和相关协议的
    server.bind((ipStr, int(portStr)))#绑定ip和端口号！！！1:注意输入的端口号是str型而这里的要传入int型
    #2:bind()的参数是一个元组的形式
    server.listen(10)#设置监听，和设置连接的最大的数量
    printStr = "服务器启动成功\n"#，是否连接成功
    text.insert(tkinter.INSERT, printStr)#显示在信息窗口中
    while True:#这里用死循环是因为模拟的服务器要一直运行
        ck, ca = server.accept()#接受所连接的客户端的信息
        # 其中ca是ip和端口号组成的元组，ck有关客户端的信息
        t = threading.Thread(target=run, args=(ck, ca))#每连接一个客户端就开启一个线程
        #其中Thread函数中的传入函数的参数也是以元组的形式
        t.start()#开启线程


def startSever():
    s = threading.Thread(target=start)#启用一个线程开启服务器
    s.start()#开启线程

#下面是关于界面的操作
labelIp = tkinter.Label(win, text='ip').grid(row=0, column=0)
labelPort = tkinter.Label(win, text='port').grid(row=1, column=0)
labelkey=tkinter.Label(win, text='key').grid(row=2, column=0)
eip = tkinter.Variable()
eport = tkinter.Variable()
ekey = tkinter.Variable()
entryIp = tkinter.Entry(win, textvariable=eip).grid(row=0, column=1)
entryPort = tkinter.Entry(win, textvariable=eport).grid(row=1, column=1)
entrykey = tkinter.Entry(win, textvariable=ekey).grid(row=2, column=1)
button = tkinter.Button(win, text="启动", command=startSever).grid(row=3, column=0)
text = tkinter.Text(win, height=7, width=30)
labeltext = tkinter.Label(win, text='连接消息').grid(row=4, column=0)
text.grid(row=4, column=1)
win.mainloop()