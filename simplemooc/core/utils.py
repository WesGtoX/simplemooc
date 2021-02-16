import hashlib
import string
import random


def random_key(size=5):
    """
    Qera uma random key, caracteres randômicos
    """
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for x in range(size))


def generate_hash_key(salt, random_str_size=5):
    """
    Pega os textos randômicos e adiciona um 'salt',
    que é alguma informação do usuário, email ou username...
    Que é uma forma de dificultar uma chave que deve ser única,
    duas vezes, duplicada (ainda existe uma pequena chance, mas vamos ignorar).
    """
    random_str = random_key(random_str_size)
    text = random_str + salt
    return hashlib.sha224(text.encode('utf-8')).hexdigest()
