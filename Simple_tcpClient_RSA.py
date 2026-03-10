from socket import *
from encryption.cifra_de_cesar import encriptar, decriptar
from encryption.diffie_hellman import (
    public_key,
    shared_secret,
    generate_private_key,
    derive_shift,
)
from encryption.rsa import generate_keypair, encrypt_rsa, decrypt_rsa

serverName = "192.168.18.4"
serverPort = 1300
clientSocket = socket(AF_INET, SOCK_STREAM)

print("Gerando chaves RSA do Cliente...")
public_rsa_client, private_rsa_client = generate_keypair(4096)

print(f"Conectando-se ao servidor {serverName}:{serverPort}...")
clientSocket.connect((serverName,serverPort))

#===============TROCA DE CHAVES RSA================
print("Realizando troca de chaves RSA...")
# Recebe a chave pública RSA do servidor
server_rsa_bytes = clientSocket.recv(65000)
s_e_str, s_n_str = server_rsa_bytes.decode("utf-8").split("|")
public_rsa_server = (int(s_e_str), int(s_n_str))
print("Chave pública RSA do servidor recebida.")

# Envia a chave pública RSA para o servidor
e_c, n_c = public_rsa_client
clientSocket.send(f"{e_c}|{n_c}".encode("utf-8"))
#==================================================

#===============DIFFIE HELLMAN=====================
# Recebe parâmetros DH (p, g) e B do servidor encriptados
encrypted_initial = clientSocket.recv(65000)
decrypted_initial = decrypt_rsa(private_rsa_client, encrypted_initial.decode("utf-8"))
p_str, g_str, B_str = decrypted_initial.split("|")
p = int(p_str)
g = int(g_str)
B = int(B_str)
print("Mensagem DH (p|g|B) recebida e decriptada com RSA.")

# Gera segredo do cliente e valor público A
priv_a = generate_private_key(p)
A = public_key(g, priv_a, p)
# Envia A para o servidor, encriptado com a chave RSA do servidor
encrypted_A = encrypt_rsa(public_rsa_server, str(A))
clientSocket.send(encrypted_A.encode("utf-8"))
print("Valor DH 'A' encriptado via RSA enviado ao servidor.")

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
