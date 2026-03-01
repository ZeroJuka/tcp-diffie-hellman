from socket import *
from encryption.cifra_de_cesar import encriptar, decriptar
from encryption.diffie_hellman import (
    public_key,
    shared_secret,
    generate_private_key,
    derive_shift,
)

serverName = "192.168.18.4"
serverPort = 1300
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

#===============DIFFIE HELLMAN=====================
# Recebe parâmetros DH (p, g) e B do servidor
initial = clientSocket.recv(65000)
p_str, g_str, B_str = str(initial, "utf-8").split("|")
p = int(p_str)
g = int(g_str)
B = int(B_str)
# Gera segredo do cliente e valor público A
priv_a = generate_private_key(p)
A = public_key(g, priv_a, p)
# Envia A para o servidor
clientSocket.send(str(A).encode("utf-8"))
# Calcula segredo compartilhado e deslocamento para cifra de César
secret = shared_secret(B, priv_a, p)
shift = derive_shift(secret)
print('===========================')
print("CHAVEAMENTO DIFFIE-HELLMAN/nDH handshake concluído")
print(f"p={p}\ng={g}\nB={B}\nA={A}\nsecret={secret}\nshift={shift}")
#==================================================

sentence = ''
while sentence != 'exit':
    sentence = input("Input lowercase sentence: ")
    encrypted = encriptar(sentence, shift)
    print('===========================')
    print ("Encrypted: ", encrypted)
    clientSocket.send(bytes(encrypted, "utf-8"))

    modifiedSentence = clientSocket.recv(65000)
    text = decriptar(str(modifiedSentence,"utf-8"), shift)
    print ("Decrypted from Server: ", text)
    print('===========================')

clientSocket.send(bytes("exit", "utf-8"))
clientSocket.close()
