from aes_lib import *

while True:
    print("Введите 1 для ЗАШИФРОВКИ текста, Введите 2 для РАСШИФРОВКИ текста")
    if input() == '1':
        print("Введите текст который нужно зашифровать, потом нажмите ENTER, потом введите кодовое слово из 16 символов")
        text = input()
        key = input()
        key = replay(key)
        A = AesCode(key)
        hash_text = A.encrypt(text)
    
        print('Это зашифрованный текст :' + "\n" + hash_text)
    else :
        print("Введите текст который нужно расшифровать, потом нажмите ENTER, потом введите кодовое слово из 16 символов")
        cipher = input()
        key = input()
        key = replay(key)
        A = AesCode(key)
        hash_text = A.decrypt(cipher)
    
        print("Это расшифрованный текст" + "\n" + hash_text)
