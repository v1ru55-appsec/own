import socket
from aes_lib import *

HOST = ''
PORT = 14900
s = socket.socket()
s.bind((HOST, PORT))
while True:
    s.listen(2)
    conn, addr = s.accept()
    Nik = (conn.recv(1024).decode('utf-8'))
    Command = (conn.recv(1024).decode('utf-8'))
    if Command == 'send':
        From = Nik
        Message = (conn.recv(1024).decode('utf-8'))
        Key = (conn.recv(1024).decode('utf-8'))
        Key = replay(Key)
        if Message == '**':
            continue
        if Message.count(' ') >= 1:
            ToNumber = Message.find(' ' , 0)
            To = Message[0 : ToNumber]   
            Text = Message[ToNumber + 1 :]
            A = AesCode(Key)
            Text = A.encrypt(Text)
            if not Text.isspace():
                File = open(str('conn' + str(To) + '.txt' ), 'a+')
                File.write ('\n' + 'От кого : ' + From + '\n')
                File.write ('Сообщение : ' + Text + '\n')
                File.close()
                conn.send(bytes('YES', encoding='utf-8'))
            else:
                conn.send(bytes('NO', encoding='utf-8'))
    elif Command == 'get':
        To = Nik
        CountMails = int((conn.recv(1024).decode('utf-8')))
        File = open(str('conn' + str(To) + '.txt'), 'r+')
        TmpMails = [line.strip() for line in File]
        Strings = len(TmpMails)
        if CountMails > (Strings // 3):
            CountMails = (Strings // 3)
        conn.send(bytes(str(CountMails), encoding='utf-8'))
        Key = replay(conn.recv(1024).decode('utf-8'))
        i = 0
        for _ in range(CountMails):
            if i < Strings:
                GetMail = '\n'.join(TmpMails[Strings - i - 3: Strings - i])
                Index = GetMail.find("Сообщение : ")
                Text = GetMail[Index+12 :]
                GetMail = GetMail.replace(Text, 'ala')
                A = AesCode(Key)
                Text = A.decrypt(Text)
                GetMail = GetMail.replace('ala', Text)
                conn.send(bytes(GetMail, encoding='utf-8'))
                i += 3
    elif Command == 'end':
        continue
conn.close()
