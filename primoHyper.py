#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Teste de primalidade - Autor: Fábio Cabrini (2025)
# Estrutura procedural simples, entrada/saída padronizadas e medição de tempo.
# Valor de teste padrão (Enter): 282739948845173

import time
import random

DEFAULT_N = 282739948845173

# --- HYPER: Miller–Rabin com pré-checagens e bases determinísticas (64 bits) ----

if __name__ == '__main__':
    try:
        raw = input(f"Digite um inteiro (Enter usa {DEFAULT_N}): ").strip()
        N = int(raw) if raw else DEFAULT_N
    except Exception:
        print("Entrada inválida. Encerrando.")
        raise SystemExit(1)
    
    t0 = time.perf_counter()

def is_probable_prime(n: int) -> bool:
    if n < 2:
        return False
    # atalhos para pequenos primos / divisores
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    if n in small:
        return True
    for p in small:
        if n % p == 0:
            return False

    # escreve n-1 como d*2^s com d ímpar
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    def witness(a: int) -> bool:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return True
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                return True
        return False  # testemunha de composição

    # bases determinísticas para n < 2**64
    if n < (1 << 64):
        bases = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)
    else:
        k = 12
        bases = [random.randrange(2, n - 2) for _ in range(k)]

    for a in bases:
        a %= n
        if a == 0:
            continue
        if not witness(a):
            return False
    return True

if __name__ == '__main__':
    primo = is_probable_prime(N)
    dt_ms = (time.perf_counter() - t0) * 1000.0

    print(f"[HYPER] {N} é primo? {primo}")
    print(f"[HYPER] Tempo: {dt_ms:.3f} ms")
