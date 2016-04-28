#!/usr/bin/python

import sys
import os
from parser import parsear_input

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.backends import default_backend


def usage():
    print("usage")
    print("mac -g <key>: Genera un MAC para la entrada estandar usando key como clave")
    print("mac -v <key>: Verifica la autenticidad de un texto (primera linea: texto, segunda linea: MAC)")


# en retrospectiva bastaba llamar a encriptar y sacar los ultimos 16 bytes...
def generar_mac(texto, key):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(key.encode())

    keydigest = digest.finalize()

    # 0^n es el vector de inicializacion segun las diapos...
    iv = bytes([0] * 16)
    cipher = Cipher(algorithms.AES(keydigest),
                    modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(128).padder()
    texto = padder.update(texto)
    texto += padder.finalize()

    textocifrado = encryptor.update(texto) + encryptor.finalize()

    if len(textocifrado) >= 16:
        return textocifrado[-16:]

    # Huh?
    return None


def verificar_mac(texto, mac, key):
    return mac == generar_mac(texto, key)


if __name__ == "__main__":
    if sys.argv[1] == "-g":
        texto = sys.stdin.readline()
        print("MAC generado: " +
              str(generar_mac(parsear_input(texto), str(sys.argv[2]))))
    elif sys.argv[1] == '-v':
        print("Ingrese el texto a verificar: ")
        texto = sys.stdin.readline()
        print("Ingrese el MAC a verificar:")
        mac = sys.stdin.readline()

        ok = verificar_mac(parsear_input(
            texto), parsear_input(mac), str(sys.argv[2]))

        if ok:
            print("ok")
        else:
            print("no")
    else:
        usage()
