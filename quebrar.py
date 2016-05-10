import sys
from mac import generar_mac
from mac import verificar_mac

from parser import parsear_input


def usage():
    print("Este programa está hecho para quebrar CBC-MAC cuando éste admite mensajes de distinto largo")
    print("Tenga en cuenta que los mensajes TIENEN que ser múltiplos de 16 carácteres")
    print("--------------------------------------------------------------------------")
    print("Primero, ingrese un mensaje de largo cualquiera múltiplo de 16 bytes")
    print("Segundo, ingrese el MAC generado para dicho mensaje")
    print("Tercero: ingrese un texto de 1 bloque más que el primero (o sea, si el primer mensaje tenía 64 bytes, el siguiente debe tener 80 bytes)")
    print("--------------------------------------------------------------------------")
    print("El programa hará xor de los últimos 16 bytes del segundo mensaje con el MAC del primer texto y se obtendrá un mensaje falsificado")
    print("El MAC de dicho mensaje es simplemente el mismo MAC del segundo mensaje")
    print("--------------------------------------------------------------------------")
    print("Explicación corta: Al permitir _un_ bloque más de encriptación, el MAC del texto más corto almacena todo el proceso de CBC dentro del MAC generado. O sea, se \"aprende\" lo que hace el proceso y se usa esto para, nuevamente bajo la lógica de CBC, falsificar un mensaje haciendo el xor de CBC manualmente DENTRO del mensaje y sólo dejando que AES haga su trabajo. En otras palabras, al falsificar no es CBC quien hace xor, sino que el xor va en el mensaje.")
    print("")
    print("")


# Retorna un par (a, b) en que:
#  a : Texto falsificado
#  b : MAC del texto falsificado
#  Para esto los MACs deben ser generados vía CBC-MAC
# Adicionalmente, texto1, texto2, mac1 y mac2 deben ser arrays BINARIOS
# (b'123\x02', por ejemplo) y múltiplos de 16 bytes
def falsificar(texto1, texto2, mac1, mac2):
    if len(texto2) - len(texto1) != 16:
        print("El segundo texto debe tener EXACTAMENTE 16 bytes más que el primero!!")
        return

    textofalsificado = [a ^ b for (a, b) in zip(mac1, texto2[-16:])]
    return (bytes(textofalsificado), mac2)


if __name__ == "__main__":
    usage()

    print("Ingrese el texto 1:")
    texto1 = parsear_input(sys.stdin.readline())

    print("Ingrese el MAC para ese texto")
    mac1 = parsear_input(sys.stdin.readline())

    print("Ingrese el texto 2 (16 bytes más que texto 1):")
    texto2 = parsear_input(sys.stdin.readline())

    print("Ingrese el MAC del texto 2")
    mac2 = parsear_input(sys.stdin.readline())

    (textofalso, macfalso) = falsificar(texto1, texto2, mac1, mac2)

    print("Texto Falso: " + str(textofalso))
    print("MAC Falso  : " + str(macfalso))
