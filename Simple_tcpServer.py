from socket import *
from encryption.cifra_de_cesar import encriptar, decriptar
from encryption.diffie_hellman import (
    public_key,
    shared_secret,
    generate_private_key,
    derive_shift,
    checa_primo,
)

serverPort = 1300
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(5) 
print ("TCP Server\n")
connectionSocket, addr = serverSocket.accept()


#===============DIFFIE HELLMAN=====================
p = 2147483647  # primo (2^31 - 1)
g = 5
# Segredo do servidor e valor público B
priv_b = generate_private_key(p)
B = public_key(g, priv_b, p)
# Envia parâmetros e B para o cliente
handshake_msg = f"{p}|{g}|{B}"
connectionSocket.send(handshake_msg.encode("utf-8"))
# Recebe A do cliente
A_bytes = connectionSocket.recv(65000)
A = int(str(A_bytes, "utf-8"))
# Calcula segredo compartilhado e deriva deslocamento
secret = shared_secret(A, priv_b, p)
shift = derive_shift(secret)
print('===========================')
print("CHAVEAMENTO DIFFIE-HELLMAN/nDH handshake concluído")
print(f"p={p}\ng={g}\nA={A}\nB={B}\nsecret={secret}\nshift={shift}")
#==================================================


# Loop de eco com cifra de César usando o deslocamento derivado
sentence = ""
while sentence != "exit":
    sentence = connectionSocket.recv(65000)
    if sentence == b"exit":
        break
    decrypted = decriptar(str(sentence, "utf-8"), shift)
    print('===========================')
    print("Encrypted From Client: ", sentence)
    print("Decrypted From Client: ", decrypted)
    capitalizedSentence = decrypted.upper()

    encrypted = encriptar(capitalizedSentence, shift)
    print("Capitalized Sentence: ", capitalizedSentence)
    print("Encrypted To Client: ", encrypted)
    print('===========================')
    connectionSocket.send(encrypted.encode("utf-8"))

connectionSocket.close()
