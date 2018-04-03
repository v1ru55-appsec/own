import socket

HOST = "localhost"
PORT = 5000
s = socket.socket()
s.connect((HOST, PORT))
UserName = bytes('володя', encoding='utf-8')
while True:
    print('Чтобы отправить сообщение введите команду send') 
    print('Чтобы посмотреть сообщения введите команду get')
    print('Чтобы выйти из программы введите команду end')
    command = input()
    s.send(bytes(command, encoding="utf-8"))
    if command == 'send':
        print('Чтобы оправить сообщение введите имя получателя, а затем, через пробел, само сообщение')
        print('Если вы не хотите отправлять сообщение введите две звездочки (**) : ')        
        MessageTmp = input()
        Message = bytes(MessageTmp, encoding="utf-8")
        s.send(UserName)
        s.send(Message)
        if MessageTmp == '**':
            continue        
        Err = (s.recv(1024).decode('utf-8'))
        if Err == 'YES':
            print('Ваше сообщение успешно отправлено')
        else:
            print('Произошла ошибка, пожалуйста, проверьте сообщение и попробуйте еще раз')
        continue
    elif command == 'get':
        s.send(UserName)
        print('Сколько последних сообщений вы хотите прочитать? Введите число:')
        NumberOfMails = bytes(input(), encoding="utf-8")
        s.send(NumberOfMails)
        print('Получены сообщения для вас :')
        print(s.recv(1024).decode('utf-8'))
        print('Для того, чтобы закрыть сообщения введите две звездочки (**) :')
        if input() == '**':
            continue
    elif command == 'end':
        print('Завершение программы....') 
        break
s.close()
