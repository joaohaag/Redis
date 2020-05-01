import redis
import time

redis = redis.Redis('localhost')

input('Aperte [ENTER] para Gerar os cartões!')
#while para poder reiniciar o jogo
while True:
    redis.delete('bingo')
    redis.delete('pontos')
    #Números bingo
    for i in range(99):
        redis.sadd('bingo', i+1)

    #Listar número do bingo -> SMEMBERS bingo

    print(30*'-'+'Cartões da Rodada'+30*'-')

    # Usuários e Cartões
    for i in range(50):
        jogador = f'Jogador:{i+1}'
        cartao = f'Cartao:{i+1}'
        # Reseta o cartão toda vez que iniciar
        redis.delete(cartao)
        redis.delete(jogador)
        redis.hset(jogador, 'Nome', f'Jogador {i+1}')
        redis.hset(jogador, 'Cartao', cartao)
        #Listar Jogador -> HGETALL Jogador:1
        #Retorna 15 números do bingo aleatóriamente e atribui a uma variável. A função estava retornando set. Transformei para lista.
        numerosCartao = list(redis.srandmember('bingo', 15))

        #Como os itens da lista estavam vindo com o tipo byte alterei para int.
        numerosCartaoint = []
        numerosCartaoint = [int(i) for i in numerosCartao]

        #Atribui números ao cartão do jogador
        for n in range(len(numerosCartaoint)):
               redis.sadd(cartao, numerosCartaoint[n])
        #Verifica números do Cartão -> SMEMBERS Cartao:1
        print('{} - Cartão: {}'.format(jogador, numerosCartaoint))

    print(77*'-')
    input('Aperte [ENTER] para Iniciar o sorteio dos números!')
    print('Sorteando os números .....')
    listsorteados = []
    v = 0
    # Rodada do Bingo
    # Chama com pop o bingo e verifica quem tem o número. Se tiver incrementa na pontuação. Se tiver 15 pontos ganhou.
    while True:
        pedra = int(redis.spop('bingo'))
        listsorteados.append(pedra)
        print(f'Número...: {pedra}')
        time.sleep(0.5)
        for i in range(50):
            cartaosorteado = list(redis.smembers(f'Cartao:{i+1}'))
            # Como os itens da lista estavam vindo com o tipo byte alterei para int.
            cartaosorteadoint = []
            cartaosorteadoint = [int(i) for i in cartaosorteado]
            for n in range(len(cartaosorteadoint)):
                if cartaosorteadoint[n] == pedra:
                      pontos = redis.zincrby('pontos', 1, f'Jogador:{i+1}')
                      if pontos == 15:
                          print(15 * '-')
                          print(f'Bingo!! Vencedor: Jogador:{i+1}')
                          print(f'Números do cartão: {cartaosorteadoint}')
                          print(f'Números Sorteados: {listsorteados}')
                          print(15 * '-')
                          v = 1
                          break
        #Caso tiver ganhador volta para o while do jogo. Pode reiniciar o jogo.
        if v == 1:
            break

    n = str(input('Reiniciar o Jogo? [S/N]:'))
    if n.upper() == 'N':
        input('Aperte [ENTER] para finalizar!')
        break




