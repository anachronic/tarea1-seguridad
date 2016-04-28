#!/usr/bin/python

import sys
import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


def usage():
    print("usage:")
    print("encrypt -e <key>: encripta la entrada estandar usando key como clave")
    print("encrypt -d <key>: decripta la entrada estandar usando key como clave")


# Retorna texto cifrado via AES-CBC con clave key.
def encriptar(texto, key):
    # primero hashear la clave para obtener 256 bits.
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(key.encode("utf-8"))
    # le tomamos digest y tenemos nuestros 16 bytes.
    keydigest = digest.finalize()

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(keydigest),
                    modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    texto = texto.encode("utf-8")
    while len(texto) % 16 != 0:
        texto = texto + b"0"

    textocifrado = encryptor.update(texto) + encryptor.finalize()

    return textocifrado


def decriptar(cifrado, key):
    # primero hashear la clave para obtener 256 bits.
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(key.encode("utf-8"))
    # le tomamos digest y tenemos nuestros 16 bytes.
    keydigest = digest.finalize()


if __name__ == "__main__":
    print("Ingrese el texto a encriptar. (<Intro> para terminar)")

    texto = sys.stdin.readline()
    print("texto cifrado: " + str(encriptar(texto, str(sys.argv[1]))))
