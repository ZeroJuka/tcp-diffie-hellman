#soma a chave ao valor ASCII do caractere
def encriptar(texto, chave) -> str:
    resultado = []
    for c in texto:
        # Verifica se o caractere é uma letra minúscula
        if "a" <= c <= "z":
            base = ord("a")
            deslocado = (ord(c) - base + chave) % 26 # pra iterar só o alfabeto
            resultado.append(chr(base + deslocado))
        # Verifica se o caractere é uma letra maiúscula
        elif "A" <= c <= "Z":
            base = ord("A")
            deslocado = (ord(c) - base + chave) % 26 # pra iterar só o alfabeto
            resultado.append(chr(base + deslocado))
        else:
            resultado.append(c)
    return "".join(resultado)

#só subtrair a chave na mesma lógica do encriptar
def decriptar(texto, chave) -> str:
    return encriptar(texto, -chave)
