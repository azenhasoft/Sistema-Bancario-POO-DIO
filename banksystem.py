# ============================================================================ #
# |                SISTEMA BANCÁRIO - VERSÃO ORIENTADA A OBJETOS             | #
# ============================================================================ #

# --- CLASSES DE TRANSAÇÃO ---
# Define a estrutura base para todas as transações (Saque, Depósito, etc.).
# Funciona como um "contrato" que obriga as classes filhas a implementarem
# certos métodos e propriedades para garantir um comportamento consistente.
class Transacao:
    """Classe base para todas as transações do sistema."""
    @property
    def valor(self):
        """Propriedade que deve retornar o valor da transação."""
        # Levanta um erro se a classe filha não implementar esta propriedade.
        raise NotImplementedError("A subclasse deve implementar a property 'valor'.")

    def registrar(self, conta):
        """Método que registra a transação em uma conta específica."""
        # Levanta um erro se a classe filha não implementar este método.
        raise NotImplementedError("A subclasse deve implementar o método 'registrar'.")

class Saque(Transacao):
    """Representa a transação de saque."""
    def __init__(self, valor):
        self._valor = valor  # Atributo que armazena o valor a ser sacado.

    @property
    def valor(self):
        """Retorna o valor do saque."""
        return self._valor

    def registrar(self, conta):
        """
        Executa a lógica de saque na conta fornecida e, se for bem-sucedido,
        adiciona esta transação ao histórico da conta.
        """
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    """Representa a transação de depósito."""
    def __init__(self, valor):
        self._valor = valor  # Atributo que armazena o valor a ser depositado.

    @property
    def valor(self):
        """Retorna o valor do depósito."""
        return self._valor

    def registrar(self, conta):
        """
        Executa a lógica de depósito na conta fornecida e, se for bem-sucedido,
        adiciona esta transação ao histórico da conta.
        """
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


# --- CLASSE DE HISTÓRICO ---
class Historico:
    """
    Responsável por manter uma lista de todas as transações
    realizadas em uma conta.
    """
    def __init__(self):
        # A lista `_transacoes` armazena um dicionário para cada transação.
        self._transacoes = []

    @property
    def transacoes(self):
        """Retorna a lista completa de transações."""
        return self._transacoes

    def adicionar_transacao(self, transacao):
        """
        Adiciona uma nova transação ao histórico.
        O método `__class__.__name__` obtém o nome da classe (ex: "Saque").
        """
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
            }
        )


# --- CLASSES DE CONTA ---
class Conta:
    """Classe base que define os atributos e métodos essenciais de uma conta bancária."""
    def __init__(self, numero, cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente      # Associa a conta a um objeto Cliente.
        self._historico = Historico() # Cada conta tem seu próprio objeto de histórico.

    @classmethod
    def nova_conta(cls, cliente, numero):
        """
        Método de fábrica (factory method) para criar uma nova instância de conta.
        Facilita a criação de contas de forma padronizada.
        """
        return cls(numero, cliente)

    # Propriedades (`@property`) fornecem acesso controlado aos atributos.
    # Elas permitem ler os valores, mas não modificá-los diretamente de fora da classe.
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

    def sacar(self, valor):
        """Valida e executa a operação de saque, se houver saldo suficiente."""
        if valor > self.saldo:
            print("\n@@@ Operação falhou! Saldo insuficiente. @@@")
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        
        return False

    def depositar(self, valor):
        """Valida e executa a operação de depósito."""
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

class ContaCorrente(Conta):
    """
    Classe especializada que herda de `Conta` e adiciona regras
    específicas para contas correntes, como limites de valor e quantidade de saques.
    """
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente) # Inicializa os atributos da classe mãe (Conta).
        self._limite = limite
        self._limite_saques = limite_saques
        self._numero_saques = 0

    def sacar(self, valor):
        """
        Sobrescreve o método `sacar` da classe `Conta` para incluir
        as validações de limite por saque e quantidade de saques diários.
        """
        if valor > self._limite:
            print(f"\n@@@ Operação falhou! O valor do saque excede o limite de R$ {self._limite:.2f}. @@@")
        elif self._numero_saques >= self._limite_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        else:
            # Se as validações específicas passarem, chama a lógica de saque da classe mãe.
            if super().sacar(valor):
                self._numero_saques += 1
                return True
        
        return False

    def __str__(self):
        """
        Define a representação em string do objeto. É chamado automaticamente
        pela função `print()` ou `str()`, facilitando a exibição dos dados da conta.
        """
        return f"""\
Agência:\t{self.agencia}
C/C:\t\t{self.numero}
Titular:\t{self.cliente.nome}
"""


# --- CLASSES DE CLIENTE ---
class Cliente:
    """Classe que gerencia os dados e as contas de um cliente."""
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = [] # Um cliente pode possuir múltiplas contas.

    def realizar_transacao(self, conta, transacao):
        """Centraliza a execução de transações para uma conta do cliente."""
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        """Vincula uma nova conta a este cliente."""
        self.contas.append(conta)

class PessoaFisica(Cliente):
    """
    Classe especializada que herda de `Cliente` e adiciona
    atributos específicos de uma pessoa física.
    """
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco) # Inicializa os atributos da classe mãe (Cliente).
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


# --- FUNÇÕES DE INTERAÇÃO COM O USUÁRIO ---
# Estas funções controlam o fluxo do programa, recebendo entradas do
# usuário e chamando os métodos apropriados nos objetos.

def menu():
    """Exibe o menu principal e retorna a opção escolhida pelo usuário."""
    menu_texto = """
================ MENU ================
[d]\tDepositar
[s]\tSacar
[e]\tExtrato
[nc]\tNova conta
[lc]\tListar contas
[nu]\tNovo usuário
[q]\tSair
=> """
    return input(menu_texto).lower() # Converte a entrada para minúscula.

def filtrar_cliente(cpf, clientes):
    """Busca um cliente na lista de clientes a partir do CPF."""
    clientes_filtrados = [c for c in clientes if c.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    """Retorna a primeira conta de um cliente. (Pode ser estendido para múltiplas contas)."""
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None
    return cliente.contas[0]

def depositar(clientes):
    """Orquestra a operação de depósito."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    try:
        valor = float(input("Informe o valor do depósito: "))
        transacao = Deposito(valor)
        conta = recuperar_conta_cliente(cliente)
        if conta:
            cliente.realizar_transacao(conta, transacao)
    except ValueError:
        print("\n@@@ Valor inválido! Por favor, informe um número. @@@")

def sacar(clientes):
    """Orquestra a operação de saque."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    try:
        valor = float(input("Informe o valor do saque: "))
        transacao = Saque(valor)
        conta = recuperar_conta_cliente(cliente)
        if conta:
            cliente.realizar_transacao(conta, transacao)
    except ValueError:
        print("\n@@@ Valor inválido! Por favor, informe um número. @@@")

def exibir_extrato(clientes):
    """Orquestra a exibição do extrato de uma conta."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes
    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in transacoes:
            print(f"{transacao['tipo']}:\t\tR$ {transacao['valor']:.2f}")

    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
    print("==========================================")

def criar_cliente(clientes):
    """Orquestra a criação de um novo cliente (PessoaFisica)."""
    cpf = input("Informe o CPF (somente números): ")
    if filtrar_cliente(cpf, clientes):
        print("\n@@@ Já existe um cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    novo_cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(novo_cliente)
    print("\n=== Cliente criado com sucesso! ===")

def criar_conta(numero_conta, clientes, contas):
    """Orquestra a criação de uma nova conta corrente para um cliente existente."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado, criação de conta encerrada! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    print("\n=== Conta criada com sucesso! ===")

def listar_contas(contas):
    """Exibe os dados de todas as contas cadastradas."""
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada. @@@")
        return
        
    for conta in contas:
        print("=" * 100)
        print(str(conta))

# --- FUNÇÃO PRINCIPAL ---
def main():
    """Função principal que inicializa o sistema e gerencia o loop de operações."""
    clientes = []
    contas = []

    # Loop infinito que mantém o programa em execução até o usuário decidir sair.
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
            print("\nObrigado por utilizar nosso sistema. Até logo!\n")
            break
        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


# --- PONTO DE ENTRADA DO PROGRAMA ---
# A linha abaixo garante que a função `main()` só será executada
# quando o script for rodado diretamente (e não quando for importado).
if __name__ == "__main__":
    main()
