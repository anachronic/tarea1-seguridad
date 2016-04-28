#!/usr/bin/python

import sys
import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.backends import default_backend


def usage():
    print("usage:")
    print("encrypt -e <key>: encripta la entrada estandar usando key como clave")
    print("encrypt -d <key>: decripta la entrada estandar usando key como clave")


# Retorna texto cifrado via AES-CBC con clave key.
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

    texto = texto.encode()
    padder = padding.PKCS7(128).padder()
    texto = padder.update(texto)
    texto += padder.finalize()

    textocifrado = iv + encryptor.update(texto) + encryptor.finalize()

    return textocifrado


# Retorna el texto plano usando cifrador de bloque AES-CBC con clave key.
# Nota: cifrado viene sin el "b" al principio. (b de string binario)
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


# aqui me pasa la cuenta no saber suficiente Python :(
def parsear_input(entrada):
    hexa = False
    hexachars = ''
    bytez = []

    for c in entrada:
        if c == '\n':
            continue
        if hexa and c == 'x':
            continue

        if not hexa and c != '\\':
            bytez.append(ord(c))
        elif not hexa and c == '\\':
            hexa = True
            continue
        elif hexa:
            hexachars += c
            if len(hexachars) == 2:
                hexa = False
                bytez.append(int(hexachars, 16))
                hexachars = ''

    return bytes(bytez)


if __name__ == "__main__":
    if sys.argv[1] == '-e':
        print("Ingrese el texto a encriptar. (<Intro> para terminar)")
        texto = sys.stdin.readline()
        print(str(encriptar(texto, str(sys.argv[2]))))
    elif sys.argv[1] == '-d':
        print("Ingrese el texto a decriptar. (<Intro> para terminar)")
        texto = sys.stdin.readline()
        print(str(decriptar(parsear_input(texto), str(sys.argv[2]))))
    else:
        usage()
