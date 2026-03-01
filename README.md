# TRABALHO DE N1 DE SEGURANÇA DA INFORMAÇÃO

Participantes
-[João Vitor Antunes](https://github.com/ZeroJuka)
-[Davi Teramoto](https://github.com/daviteramoto)
-[Gustavo Henrique Portari](https://github.com/Gportari)
-[Leonardo de Carlos](https://github.com/LeooDevv)


# TCP + Cifra de Cesar + Diffie-Hellman (didático)

Projeto simples em Python que demonstra:
- Comunicação TCP cliente/servidor.
- Troca de chaves Diffie–Hellman para derivar um segredo compartilhado.
- Uso desse segredo como deslocamento de uma cifra de César para criptografar mensagens.

## Como Funciona (visão geral)
- Handshake DH:
  - Servidor escolhe um primo público `p` e base `g`, gera segredo `b` e envia `p|g|B` (com `B = g^b mod p`).
  - Cliente recebe, gera `a` e envia `A = g^a mod p`.
  - Ambos calculam o mesmo segredo `s = A^b = B^a (mod p)`.
  - Derivamos `shift = s % 26` para a cifra de César.
- Comunicação:
  - Cliente cifra a mensagem com `shift` e envia.
  - Servidor decifra, processa (uppercase) e reenvia cifrado com o mesmo `shift`.

## O que observar no terminal
- Durante o handshake, cliente e servidor imprimem `p`, `g`, `A`, `B`, o `secret` e o `shift`.
- Nas mensagens:
  - Cliente mostra o texto cifrado que está enviando e o texto decifrado que recebeu.
  - Servidor mostra o que recebeu cifrado, o texto decifrado, o uppercase e o que reenviou cifrado.

---

Projeto com propósito educativo.
