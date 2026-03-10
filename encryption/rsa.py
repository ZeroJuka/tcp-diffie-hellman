import sys
import os
import random

# Para garantir a importação do primoHyper a partir da raiz do projeto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from primoHyper import is_probable_prime

def generate_large_prime(bits=2048):
    print(f"Gerando primo de {bits} bits")
    while True:
        # Gera um número ímpar aleatório com o número de bits especificado
        num = random.getrandbits(bits)
        # Garante que o número tem exatamente 'bits' de comprimento e é ímpar
        num |= (1 << (bits - 1)) | 1
        
        if is_probable_prime(num):
            return num

def generate_keypair(bits=4096):
    print(f"===== INICIANDO GERAÇÃO DE CHAVES RSA ({bits} bits) =====")
    prime_bits = bits // 2
    
    p = generate_large_prime(prime_bits)
    q = generate_large_prime(prime_bits)
    
    # Para garantir que p e q são diferentes
    while p == q:
        q = generate_large_prime(prime_bits)
        
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = 65537
    d = pow(e, -1, phi)
    
    print("===== CHAVES RSA GERADAS COM SUCESSO =====")
    return ((e, n), (d, n))

def encrypt_rsa(public_key, message: str) -> str:
    e, n = public_key
    message_bytes = message.encode('utf-8')
    message_int = int.from_bytes(message_bytes, byteorder='big')
    
    if message_int >= n:
        raise ValueError("Mensagem longa demais para ser cifrada com essa chave RSA.")
        
    # c = m^e mod n
    cipher_int = pow(message_int, e, n)
    return hex(cipher_int)

def decrypt_rsa(private_key, ciphertext_hex: str) -> str:
    d, n = private_key
    cipher_int = int(ciphertext_hex, 16)
    
    # m = c^d mod n
    message_int = pow(cipher_int, d, n)
    
    # Converte o número inteiro de volta para string
    num_bytes = (message_int.bit_length() + 7) // 8
    message_bytes = message_int.to_bytes(num_bytes, byteorder='big')
    
    return message_bytes.decode('utf-8')
