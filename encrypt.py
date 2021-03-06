#!/usr/bin/python

import sys
import os
from parser import parsear_input

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.backends import default_backend


def usage():
    print("usage:")
    print("encrypt -e <key>: encripta la entrada estandar usando key como clave")
    print("encrypt -d <key>: decripta la entrada estandar usando key como clave")


# Retorna texto cifrado via AES-CBC con clave key.
# Nota: texto es texto BINARIO.
def encriptar(texto, key):
    # primero hashear la clave para obtener 256 bits.
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(key.encode())
    # le tomamos digest y tenemos nuestros 16 bytez.
    keydigest = digest.finalize()

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(keydigest),
                    modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(128).padder()
    texto = padder.update(texto)
    texto += padder.finalize()

    textocifrado = iv + encryptor.update(texto) + encryptor.finalize()

    return textocifrado


# Retorna el texto plano usando cifrador de bloque AES-CBC con clave key.
# Nota: cifrado es texto BINARIO.
def decriptar(cifrado, key):
    # primero hashear la clave para obtener 256 bits.
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(key.encode())
    # le tomamos digest y tenemos nuestros 16 bytez.
    keydigest = digest.finalize()

    cipher = Cipher(algorithms.AES(keydigest), modes.CBC(
        cifrado[:16]), backend=default_backend())

    decryptor = cipher.decryptor()

    texto_no_tan_plano = decryptor.update(cifrado[16:]) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(texto_no_tan_plano) + unpadder.finalize()


if __name__ == "__main__":
    if sys.argv[1] == '-e':
        print("Ingrese el texto a encriptar. (<Intro> para terminar)")
        texto = sys.stdin.readline()
        print(str(encriptar(parsear_input(texto), str(sys.argv[2]))))
    elif sys.argv[1] == '-d':
        print("Ingrese el texto a decriptar. (<Intro> para terminar)")
        texto = sys.stdin.readline()
        print(str(decriptar(parsear_input(texto), str(sys.argv[2]))))
    else:
        usage()
