Sistema Bancário em Python (POO)

📝 Descrição do Projeto

Este projeto é uma simulação de um sistema bancário básico, desenvolvido em Python puro, com o objetivo de aplicar e demonstrar os conceitos fundamentais da Programação Orientada a Objetos (POO). O sistema permite criar usuários, associar contas correntes a eles e realizar operações financeiras essenciais como saques, depósitos e consulta de extrato.

Todo o código é autocontido em um único arquivo (banksystem.py) e não requer a instalação de nenhuma biblioteca externa.

✨ Funcionalidades

O sistema oferece as seguintes operações através de um menu interativo no terminal:

    [d] Depositar: Adicionar um valor monetário à conta de um cliente.

    [s] Sacar: Retirar um valor da conta, respeitando o saldo e os limites da conta corrente (máximo de 3 saques e limite de R$ 500,00 por saque).

    [e] Extrato: Exibir o histórico de transações (saques e depósitos) e o saldo atual da conta.

    [nu] Novo Usuário: Cadastrar um novo cliente (pessoa física) no sistema.

    [nc] Nova Conta: Criar uma nova conta corrente vinculada a um usuário existente.

    [lc] Listar Contas: Exibir todas as contas cadastradas no sistema.

    [q] Sair: Encerrar a execução do programa.

🏛️ Arquitetura e Conceitos de POO Aplicados

O projeto foi estruturado utilizando classes que representam as entidades do mundo real de um banco, promovendo um código mais organizado, reutilizável e escalável.

    Herança:

        PessoaFisica herda de Cliente, especializando a classe base com atributos como nome e CPF.

        ContaCorrente herda de Conta, adicionando regras de negócio específicas, como limites de saque.

    Encapsulamento:

        Atributos sensíveis, como _saldo e _limite, são definidos como "protegidos" (usando um _ underscore) e acessados através de propriedades (@property), garantindo que a manipulação dos dados seja feita de forma controlada pelos métodos da classe.

    Abstração:

        A classe Transacao serve como um contrato abstrato, definindo que toda transação deve ter um valor e um método registrar. As classes Saque e Deposito fornecem as implementações concretas dessa abstração.

    Composição:

        Uma Conta é "composta por" um Historico. Em vez de a conta gerenciar diretamente uma lista de transações, ela delega essa responsabilidade a um objeto Historico, mantendo as responsabilidades bem separadas.

Estrutura das Classes

    Cliente / PessoaFisica: Representam o usuário do banco.

    Conta / ContaCorrente: Representam a conta bancária e suas regras.

    Historico: Armazena o registro de transações de uma conta.

    Transacao / Saque / Deposito: Modelam as operações financeiras como objetos.

🚀 Tecnologias Utilizadas

    Python 3: Toda a lógica do programa foi desenvolvida em Python, sem dependências externas.

⚙️ Como Executar

Para executar este projeto, você precisará ter o Python 3 instalado em sua máquina.

    Clone o repositório:
    Bash

git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git

Navegue até o diretório do projeto:
Bash

cd SEU-REPOSITORIO

Execute o script:
Bash
    python banksystem.py

Após a execução, o menu interativo será exibido no seu terminal.
