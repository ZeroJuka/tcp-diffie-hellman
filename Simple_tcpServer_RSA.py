from socket import *
from encryption.cifra_de_cesar import encriptar, decriptar
from encryption.diffie_hellman import (
    public_key,
    shared_secret,
    generate_private_key,
    derive_shift,
    checa_primo,
)
from encryption.rsa import generate_keypair, encrypt_rsa, decrypt_rsa

serverPort = 1300
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(5) 
print ("TCP Server\n")
print("Gerando chaves RSA do Servidor...")
public_rsa_server, private_rsa_server = generate_keypair(4096)
print("Aguardando conexão do cliente...")
connectionSocket, addr = serverSocket.accept()


#===============TROCA DE CHAVES RSA================
print("Realizando troca de chaves RSA...")
# Envia a chave pública RSA para o cliente
e_s, n_s = public_rsa_server
connectionSocket.send(f"{e_s}|{n_s}".encode("utf-8"))

# Recebe a chave pública RSA do cliente
client_rsa_bytes = connectionSocket.recv(65000)
c_e_str, c_n_str = client_rsa_bytes.decode("utf-8").split("|")
public_rsa_client = (int(c_e_str), int(c_n_str))
print("Chave pública RSA do cliente recebida.")
#==================================================

#===============DIFFIE HELLMAN=====================
p = 2147483647  # primo (2^31 - 1)
g = 5
# Segredo do servidor e valor público B
priv_b = generate_private_key(p)
B = public_key(g, priv_b, p)
# Envia parâmetros e B para o cliente (Encriptados com RSA)
handshake_msg = f"{p}|{g}|{B}"
encrypted_handshake = encrypt_rsa(public_rsa_client, handshake_msg)
connectionSocket.send(encrypted_handshake.encode("utf-8"))
print("Mensagem DH (p|g|B) encriptada via RSA enviada ao cliente.")

# Recebe A do cliente e decripta com RSA
encrypted_A_bytes = connectionSocket.recv(65000)
decrypted_A_str = decrypt_rsa(private_rsa_server, encrypted_A_bytes.decode("utf-8"))
A = int(decrypted_A_str)
print("Valor DH 'A' recebido e decriptado com RSA.")

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
