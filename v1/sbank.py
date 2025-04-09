menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """
# Menu de opções que será exibido continuamente para o usuário.

saldo = 0 
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
# Variáveis iniciais para controle do sistema bancário:
# - saldo: armazena o saldo atual da conta.
# - limite: valor máximo permitido por saque.
# - extrato: histórico das transações realizadas.
# - numero_saques: contador de saques realizados na sessão.
# - LIMITE_SAQUES: número máximo de saques permitido por sessão.

while True: 
    opcao = input(menu)
    # Loop principal do programa, que exibe o menu e aguarda a entrada do usuário.

    if opcao == "d": 
        valor = float(input("Informe o valor do depósito: "))
        # Solicita o valor do depósito ao usuário.

        if valor > 0: 
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
            # Atualiza o saldo e registra o depósito no extrato.

        else:
            print("Operação falhou! Valor inválido.")
            # Exibe mensagem de erro caso o valor informado seja inválido.

    elif opcao == "s": 
        valor = float(input("Informe o valor do saque: "))
        # Solicita o valor do saque ao usuário.

        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        execedeu_saques = numero_saques >= LIMITE_SAQUES
        # Realiza verificações para validar se o saque é permitido:
        # - excedeu_saldo: verifica se há saldo suficiente.
        # - excedeu_limite: verifica se o valor excede o limite de saque.
        # - execedeu_saques: verifica se o limite de saques foi atingido.

        if excedeu_saldo: 
            print("Operação falhou! Saldo insuficiente.")
        elif excedeu_limite:
            print("Operação falhou! Limite de saque excedido.")
        elif execedeu_saques: 
            print("Operação falhou! Número máximo de saques excedido.")
        elif valor > 0: 
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1
            # Realiza o saque, atualizando saldo, extrato e contador de saques.

        else:
            print("Operação falhou! Valor inválido.")
            # Exibe mensagem de erro caso o valor informado seja inválido.

    elif opcao == "e": 
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"Saldo: R$ {saldo:.2f}")
        print("========================================")
        # Exibe o extrato completo com as transações realizadas e o saldo atual.
        # Caso nenhuma movimentação tenha sido feita, exibe mensagem padrão.

    elif opcao == "q": 
        break
        # Finaliza o loop e encerra o programa.

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada!")
        # Mensagem exibida para entradas inválidas.
