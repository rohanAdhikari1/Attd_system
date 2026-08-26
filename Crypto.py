import string
import random

chars = " " + string.punctuation + string.ascii_letters + string.digits
chars = list(chars)
key = chars.copy()

# random.shuffle(key)

def encrypt_id(id):
    cipher_text = ""
    for letter in id:
        index = chars.index(letter)
        cipher_text += key[index]
    return cipher_text


def decrypt_id(encrypted_id):
    plain_text = ""
    for letter in encrypted_id:
        index = key.index(letter)
        plain_text += chars[index]
    return plain_text