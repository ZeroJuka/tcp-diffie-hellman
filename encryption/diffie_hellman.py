import secrets

def generate_private_key(p: int) -> int:
    return secrets.randbelow(p - 3) + 2

def public_key(g: int, private: int, p: int) -> int:
    return pow(g, private, p)

def shared_secret(peer_public: int, private: int, p: int) -> int:
    return pow(peer_public, private, p)

def derive_shift(secret: int) -> int:
    # Deriva um deslocamento para a cifra de César a partir do segredo DH
    return secret % 26

def checa_primo(N):
    i = 2
    while i < N:
        R = N % i
        if R == 0:
            return False
        i += 1
    else:
        return True