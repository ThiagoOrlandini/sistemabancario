menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
 
=> """
 
saldo = 0 
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu)
    
    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))
        
        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
            
        else:
            print("Operação falhou! Valor inválido.")
    
    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))
        
        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        execedeu_saques = numero_saques >= LIMITE_SAQUES
        
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
        
        else:
            print("Operação falhou! Valor inválido.")
    
    elif opcao == "e":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"Saldo: R$ {saldo:.2f}")
        print("========================================")
    
    elif opcao == "q":
        break
    
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada!")
