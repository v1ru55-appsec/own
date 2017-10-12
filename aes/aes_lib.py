from Crypto.Cipher import AES
from Crypto import Random
import base64
import re


class AesCode:# какая-то хрень которая работает на темной магии

    def __init__(self, key):
        self.key = key

    def encrypt(self, text):
        letters = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        rep_let = 0
        is_again = 0
        k = 0
        _ = 0
        is_rus = 0
        for i in range(len(text)):
            pos = letters.find(text[i + k])
            if pos > -1:
                rep_let = chr(pos + 65)
                if is_again == i + k - 1:
                    text = text[:i + k] + rep_let + text[i + k + 1:]
                    k += 0
                elif i == 0:
                    text = chr(127) + rep_let + text[i + k + 1:]
                    k += 1
                else:
                    if is_again != i + k - 1:
                        text = text[:i + k] + chr(127) + rep_let + text[i + k + 1:]
                        k += 1
                    elif is_again == 0 and i == 0:
                        text = text[:is_again] + chr(127) + text[is_again:i + k] + chr(127) + rep_let + text[i + k + 1:]
                        k += 2

                is_again = i + k
                _ = 1
            if pos == -1 and is_again != 0:
                if is_again == i + k - 1:
                    text = text[:is_again + 1] + chr(127) + text[is_again + 1:]
                    k += 1
        if _ == 1:
            text = text[:is_again + 1] + chr(127) + text[is_again + 1:]
        k = 0
        for i in range(len(text)):
            if text[i-k] == chr(127) and text[i -1-k] == chr(127) and (i != 0 or k != 0):
                text = text[:i - 1] + text[i:]
                k = 1
        BS = 16
        text = text + ((BS - len(text) % BS) * (chr(BS - len(text) % BS)))
        IV = Random.new().read(AES.block_size)
        aes = AES.new(self.key, AES.MODE_CBC, IV)
        encrypt_text = base64.b64encode(IV + aes.encrypt(text))
        return (encrypt_text.decode("utf-8"))

    def decrypt(self, cipher):
        cipher = base64.b64decode(cipher)
        IV = cipher[:16]
        aes = AES.new(self.key, AES.MODE_CBC, IV)
        dec_aes = aes.decrypt(cipher[16:])
        decrypt_text = dec_aes[:-ord(dec_aes[len(dec_aes) - 1:])]
        text = decrypt_text.decode("utf-8")
        letters = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        k = 0
        for i in range(len(text)):
            if text[i-k] == chr(127):
                text = text[:i-k] + text[i+1-k:]
                k += 1
                continue
            if k % 2 == 1:
                text = text[:i-k] + letters[(ord(text[i-k])-65)] + text[i+1-k:]
        return(text)

def replay(rep):
    alph = ")-3&$*kcjs+^$/%0"
    leng = len(rep)
    if leng < 16:
        rep += alph[0:16-leng]
    return(rep)
