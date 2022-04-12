import base64
import hashlib
import tkinter
import socket
import threading
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad

win = tkinter.Tk()
win.title("客户端1")
win.geometry("400x400+200+20")

ck = None#用于储存客户端的信息


def getInfo():
    while True:
        data = ck.recv(1024)#用于接受服务其发送的信息
        rdata = data.decode("utf-8")
        rinfolist = rdata.split(":")
        if rinfolist[2] == "md5":
            rstr_len = rinfolist[3].encode("utf-8")
            rh = hashlib.md5(rstr_len)
            rh_en = rh.hexdigest()
            if str(rh_en) == rinfolist[1]:
                text.insert(tkinter.INSERT, data.decode("utf-8"))  # 显示在信息框上
                text.insert(tkinter.INSERT, "\n")
        elif rinfolist[2] == "base64":
            dbase64_text = base64.b64decode(rinfolist[3].encode("utf-8")).decode("utf-8")
            info = rinfolist[0] + ":" + rinfolist[1] + rinfolist[2] + rinfolist[3]
            text.insert(tkinter.INSERT, info) #显示在信息框上
            text.insert(tkinter.INSERT, "\n")
        elif rinfolist[1] == "aes":
            #raes = AES.new(rinfolist[1].encode("utf-8"), AES.MODE_ECB)
            passw = b'1234567812345678'
            raes = AES.new(passw, AES.MODE_ECB)
            daes_text = raes.encrypt(pad(rinfolist[2].encode("utf-8"), block_size=32))
            raes2 = AES.new(passw, AES.MODE_ECB)
            daes_text2 = raes2.decrypt(daes_text)
            info = rinfolist[0] + ":" + rinfolist[1] + unpad(daes_text2,block_size=32).decode("utf-8")
            text.insert(tkinter.INSERT, info)  # 显示在信息框上
            text.insert(tkinter.INSERT, "\n")
        else:
            text.insert(tkinter.INSERT, "未接受到信息\n")


def connectServer():
    global ck
    ipStr = eip.get()
    portStr = eport.get()
    userStr = euser.get()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#socked所准守ipv4或ipv6，和相关协议的
    client.connect((ipStr, int(portStr)))#连接ip和端口号！！！1:注意输入的端口号是str型而这里的要传入int型
    #2:bind()的参数是一个元组的形式
    client.send(userStr.encode("utf-8"))
    ck = client

    t = threading.Thread(target=getInfo)
    t.start()


def sendMail():
    friend = efriend.get()
    sendStr = esend.get()
    sendStr = friend + ":" + sendStr
    ck.send(sendStr.encode("utf-8"))


#下面是界面
labelUse = tkinter.Label(win, text="userName").grid(row=0, column=0)
euser = tkinter.Variable()
entryUser = tkinter.Entry(win, textvariable=euser).grid(row=0, column=1)

labelIp = tkinter.Label(win, text="ip").grid(row=1, column=0)
eip = tkinter.Variable()
entryIp = tkinter.Entry(win, textvariable=eip).grid(row=1, column=1)

labelPort = tkinter.Label(win, text="port").grid(row=2, column=0)
eport = tkinter.Variable()

entryPort = tkinter.Entry(win, textvariable=eport).grid(row=2, column=1)

button = tkinter.Button(win, text="启动", command=connectServer).grid(row=3, column=0)
text = tkinter.Text(win, height=5, width=30)
labeltext= tkinter.Label(win, text="显示消息").grid(row=4, column=0)
text.grid(row=4, column=1)

esend = tkinter.Variable()
labelesend = tkinter.Label(win, text="发送的消息").grid(row=5, column=0)
entrySend = tkinter.Entry(win, textvariable=esend).grid(row=5, column=1)

efriend = tkinter.Variable()
labelefriend= tkinter.Label(win, text="发给谁").grid(row=6, column=0)
entryFriend = tkinter.Entry(win, textvariable=efriend).grid(row=6, column=1)

button2 = tkinter.Button(win, text="发送", command=sendMail).grid(row=7, column=0)
win.mainloop()
