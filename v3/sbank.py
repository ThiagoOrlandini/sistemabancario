import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

# Classe Cliente que representa um cliente bancário
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []  # Lista de contas associadas ao cliente

    # Método para realizar uma transação em uma conta
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    # Método para adicionar uma nova conta ao cliente
    def adicionar_conta(self, conta):
        self.contas.append(conta)

# Subclasse PessoaFisica que herda de Cliente
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf  # CPF é utilizado como identificador único do cliente

# Classe Conta que representa uma conta bancária
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0  # Saldo inicial da conta
        self._numero = numero
        self._agencia = "0001"  # Código da agência padrão
        self._cliente = cliente
        self._historico = Historico()  # Histórico de transações da conta

    # Método para criar uma nova conta associada ao cliente
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    # Propriedades para acessar atributos privados da conta
    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    # Método para realizar um saque na conta
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo  # Verifica se o saque excede o saldo disponível

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif valor > 0:
            self._saldo -= valor  # Deduz o valor do saldo da conta
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    # Método para realizar um depósito na conta
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor  # Adiciona o valor ao saldo da conta
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True

# Classe ContaCorrente, que herda de Conta e adiciona limite de saque
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite  # Limite máximo permitido para saque
        self._limite_saques = limite_saques  # Número máximo de saques por período

    # Método para realizar saque considerando limite e quantidade de saques
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        else:
            return super().sacar(valor)

        return False

    # Método para exibir informações da conta corrente
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

# Classe Historico que registra todas as transações da conta
class Historico:
    def __init__(self):
        self._transacoes = []

    # Propriedade para acessar as transações registradas
    @property
    def transacoes(self):
        return self._transacoes

    # Método para adicionar uma nova transação ao histórico da conta
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),  # Data e hora da transação
            }
        )

# Classe abstrata Transacao para representar qualquer transação bancária
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

# Subclasse Saque que herda de Transacao e realiza saques
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

# Subclasse Deposito que herda de Transacao e realiza depósitos
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

# Função que exibe o menu e captura a opção escolhida pelo usuário
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
    return input(textwrap.dedent(menu))

# Função para encontrar um cliente pelo CPF
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

# Função para recuperar a conta de um cliente
def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]

# Função principal que executa o sistema bancário
def main():
    clientes = []  # Lista para armazenar os clientes
    contas = []  # Lista para armazenar as contas

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)
        elif opcao == "s":
            sacar(clientes)
        elif opcao == "e":
            exibir_extrato(clientes)
        elif opcao == "nu":
            criar_cliente(clientes)
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "q":
            break

# Executa o programa
main()
