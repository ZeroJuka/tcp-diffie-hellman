# TRABALHO DE N1 DE SEGURANÇA DA INFORMAÇÃO

Participantes
-[João Vitor Antunes](https://github.com/ZeroJuka)
-[Davi Teramoto](https://github.com/daviteramoto)
-[Gustavo Henrique Portari](https://github.com/Gportari)
-[Leonardo de Carlos](https://github.com/LeooDevv)


# TCP + Cifra de Cesar + Diffie-Hellman + RSA

Projeto simples em Python que demonstra:
- Comunicação TCP cliente/servidor.
- Geração de chaves RSA de 4096 bits "do zero" (usando teste de primalidade de Miller-Rabin).
- Troca de chaves públicas RSA entre cliente e servidor.
- Troca de parâmetros Diffie–Hellman encriptada com o RSA para derivar um segredo compartilhado seguro.
- Uso do segredo DH como deslocamento de uma cifra de César para criptografar as mensagens do chat.

## Como Funciona (visão geral)
1. **Geração e Troca RSA**:
   - Cliente e Servidor começam gerando pares de chaves RSA (Pública e Privada) de 4096 bits.
   - Em seguida, trocam as suas chaves públicas RSA abertamente pela rede.

2. **Handshake Diffie-Hellman Seguro (RSA)**:
   - Servidor escolhe um primo público `p` e base `g`, gera seu segredo `b` e tenta enviar a string `p|g|B` (onde `B = g^b mod p`).
   - Antes do envio, o Servidor cifra esses dados usando a **chave pública RSA do Cliente**.
   - O Cliente recebe o pacote, decifra com sua **chave privada RSA** e lê os parâmetros DH.
   - O Cliente gera seu segredo `a` e calcula `A = g^a mod p`. Antes de mandar `A` para o servidor, cifra o valor usando a **chave pública RSA do Servidor**.
   - O Servidor recebe, decifra usando sua **chave privada RSA**.
   - Ao final, ambos calculam de forma unânime o segredo compartilhado `s = (A^b) mod p = (B^a) mod p`.
   - Derivamos `shift = s % 26` para usar como passo da Cifra de César.

3. **Comunicação (Cifra de César)**:
   - Cliente cifra seu input de texto com a chave `shift` e envia ao socket.
   - Servidor recebe o texto cifrado, decifra usando o mesmo `shift`, coloca o texto em letras maiúsculas (uppercase) e devolve a resposta encriptada.

## O que observar no terminal
- Hávírá um delay na inicialização devido ao esforço para originar os extensos primos longos de 2048 bits das chaves.
- Durante o Handshake de Criptografia Assimétrica, observarão os logs `==VALOR ENCRIPTADO: 0x...==` sinalizando o payload ilegível na sua ida ao seu respectivo ponto.
- Fechado o Handshake, cliente e servidor documentam na tela as chaves calculadas para avaliação (`p`, `g`, `A`, `B`, `secret` e o `shift`).
- Nas mensagens:
  - O Cliente exibe o cipher-text a ser despejado no cabo, seguido da mensagem validada em clear-text que retomou do backend.
  - O Servidor demonstra a cifra originada do request, sua limpeza, o processo efetuado (capitalized text), e o payload do novo cipher-text comutado para a devolução.

---

Projeto com propósito educativo (algoritmo RSA construído sem auxílio bibliotecas abstraídas de criptografia).
