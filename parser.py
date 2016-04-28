# aqui me pasa la cuenta no saber suficiente Python :(
def parsear_input(entrada):
    hexa = False
    hexachars = ''
    bytez = []

    for c in entrada:
        if c == '\n':
            continue

        # esto es HORRIBLE, lo se, pero que le vamos a hacerle :(
        if hexa and c == 'x':
            continue
        if hexa and c == 'n':
            bytez.append(10)
            hexa = False
            continue
        if hexa and c == 'r':
            bytez.append(13)
            hexa = False
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
