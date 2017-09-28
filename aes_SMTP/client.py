import socket

HOST = "172.18.24.27"
PORT = 14900
s = socket.socket()
s.connect((HOST, PORT))
print('Введите свое имя, на которое будет производиться отправка и получене почты')
UserName = bytes(input(), encoding='utf-8')
while True:
    s.send(UserName)
    print('Чтобы отправить сообщение введите команду send') 
    print('Чтобы посмотреть сообщения введите команду get')
    print('Чтобы выйти из программы введите команду end')
    Command = input()
    s.send(bytes(Command, encoding="utf-8"))
    if Command == 'send':
        print('Чтобы оправить сообщение введите имя получателя, а затем, через пробел, само сообщение')
        print('Если вы не хотите отправлять сообщение введите две звездочки (**) : ')        
        MessageTmp = input()
        if MessageTmp == '**':
            continue          
        Message = bytes(MessageTmp, encoding="utf-8")
        s.send(Message)
        print('Введите пароль до 16 символов:')
        Key = bytes(input(), encoding="utf-8")
        s.send(Key)
        Err = (s.recv(1024).decode('utf-8'))
        if Err == 'YES':
            print('Ваше сообщение успешно отправлено')
        else:
            print('Произошла ошибка, пожалуйста, проверьте сообщение и попробуйте еще раз')
        continue
    elif Command == 'get':
        print('Сколько последних сообщений вы хотите прочитать ? Введите число :')
        IntMails = input()
        NumberOfMails = bytes(IntMails, encoding="utf-8")
        s.send(NumberOfMails)
        RealNumber = (s.recv(1024).decode('utf-8'))
        IntMails = RealNumber
        print('Введите пароль:')
        s.send(bytes(input(), encoding="utf-8"))
        print('Получены сообщения для вас :')
        for _ in range(int(IntMails)):
            print(s.recv(1024).decode('utf-8'))
            print('_______________________________________________________________________________')
            print('Нажмите enter чтобы продолжить')
            input()
        print('Для того , чтобы закрыть сообщения введите две звездочки (**) :')
        if input() == '**':
            continue
    elif Command == 'end':
        print('Завершение программы....') 
        break
s.close()
