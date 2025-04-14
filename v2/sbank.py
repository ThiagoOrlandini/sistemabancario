import textwrap

# Função para exibir o menu de opções ao usuário
def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    # Retorna a entrada do usuário após exibir o menu
    return input(textwrap.dedent(menu))

# Função responsável por realizar depósitos
def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor  # Atualiza o saldo com o valor do depósito
        extrato += f"Depósito:\tR$ {valor:.2f}\n"  # Registra o depósito no extrato
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    # Retorna o saldo atualizado e o extrato
    return saldo, extrato

# Função responsável por realizar saques com várias verificações
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo  # Verifica se o saldo é insuficiente
    excedeu_limite = valor > limite  # Verifica se o saque excede o limite permitido
    excedeu_saques = numero_saques >= limite_saques  # Verifica se o número máximo de saques foi atingido

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
    elif valor > 0:
        saldo -= valor  # Deduz o valor do saldo
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"  # Registra o saque no extrato
        numero_saques += 1  # Incrementa o número de saques realizados
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    # Retorna o saldo atualizado e o extrato
    return saldo, extrato

# Função para exibir o extrato ao usuário
def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    # Exibe mensagem caso não tenha movimentações
    print("Não foram realizadas movimentações." if not extrato else extrato)
    # Exibe o saldo atual
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")

# Função para criar um novo usuário
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)  # Busca por CPF na lista de usuários
    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return
    # Captura as informações do novo usuário
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    # Adiciona o usuário na lista de usuários
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("=== Usuário criado com sucesso! ===")

# Função para filtrar usuários pelo CPF
def filtrar_usuario(cpf, usuarios):
    # Procura na lista de usuários utilizando list comprehension
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    # Retorna o usuário encontrado ou None
    return usuarios_filtrados[0] if usuarios_filtrados else None

# Função para criar uma nova conta vinculada a um usuário
def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)  # Busca pelo usuário com o CPF informado
    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        # Retorna os dados da conta criada
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")

# Função para listar todas as contas registradas
def listar_contas(contas):
    for conta in contas:
        # Prepara os dados de cada conta para exibição
        linha = f"""\ 
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))  # Remove indentação para exibição

# Função principal do programa, gerencia as operações
def main():
    LIMITE_SAQUES = 3  # Define o limite máximo de saques por usuário
    AGENCIA = "0001"  # Define o número da agência padrão

    # Variáveis iniciais
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()  # Exibe o menu e captura a escolha do usuário

        if opcao == "d":  # Depósito
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":  # Saque
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":  # Extrato
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":  # Novo usuário
            criar_usuario(usuarios)

        elif opcao == "nc":  # Nova conta
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "lc":  # Listar contas
            listar_contas(contas)

        elif opcao == "q":  # Sair
            break

        else:  # Opção inválida
            print("Operação inválida, por favor selecione novamente a operação desejada.")

# Chama a função principal para iniciar o programa
main()
