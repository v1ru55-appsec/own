import socket
import os

HOST = ''
PORT = 5000
s = socket.socket()
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
while True:
    Key = (conn.recv(1024).decode('utf-8'))
    print(Key)
    if Key == 'send':
        From = (conn.recv(1024).decode('utf-8'))
        Message = (conn.recv(1024).decode('utf-8'))
        if Message == '**':
            continue
        if Message.count(' ') > 1:
            ToNumber = Message.find(' ' , 0)
            To = Message[0 : ToNumber]   
            Text = Message[ToNumber + 1 :]
            if not Text.isspace():
                File = open(str('E:\py-cod\SMTP\conn' + str(To) + '.txt' ), 'a+')
                File.write ('От кого : ' + From + '\n') 
                File.write ('Сообщение : ' + Text + ('\n' * 2))
                File.close()
                conn.send(bytes('YES', encoding='utf-8'))
            else:
                conn.send(bytes('NO', encoding='utf-8'))
    elif Key == 'get':
        To = (conn.recv(1024).decode('utf-8'))
        CountMails = int((conn.recv(1024).decode('utf-8')))
        print(CountMails, To)
        File = open(str('E:\py-cod\SMTP\conn' + str(To) + '.txt' ), 'r+')
        TmpMails = [line.strip() for line in File]
        if CountMails > len(TmpMails):
            GetMail = '\n'.join(TmpMails[0:])
        else:
            GetMail = '\n'.join(TmpMails[(len(TmpMails)-CountMails*3):])
        conn.send(bytes(GetMail, encoding='utf-8'))
    elif Key == 'end':
        continue
conn.close()        
