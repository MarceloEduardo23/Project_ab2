# 🚗 AV Rental Car System

Este é um sistema estruturado de **locação de veículos**, desenvolvido em Python.

O sistema oferece funcionalidades completas como cadastro de clientes e veículos, realização, modificação e cancelamento de reservas, controle de manutenções, pagamentos (com gestão de caução e reembolso), devolução, avaliação da experiência, registro de incidentes, geração de contrato e simulação de rastreamento GPS.

---

## ✅ Funcionalidades Implementadas

* **Gestão de Inventário de Veículos**: Cadastro de veículos e verificação de disponibilidade.
* **Sistema de Reservas Completo**:
    * **Criar Reserva**: Clientes podem alugar veículos disponíveis.
    * **Modificar Reserva**: Alterar detalhes de uma reserva (antes do pagamento).
    * **Cancelar Reserva**: Cancelar uma reserva (antes do pagamento).
* **Preços e Ofertas Especiais**:
    * Preços dinâmicos por veículo.
    * Desconto automático para aluguéis de longa duração (7+ dias).
    * Sistema de cupons de desconto (códigos promocionais) gerenciado pelo administrador.
* **Processamento de Pagamentos**: Inclui descontos e opções de parcelamento.
* **Gestão de Caução e Reembolso**: Sistema de depósito de segurança que é reembolsado na devolução.
* **Gestão de Contratos de Aluguel**: Geração e exibição digital do contrato.
* **Simulação de Rastreamento GPS**: Função para administradores "localizarem" veículos da frota.
* **Registros de Manutenção e Serviço**: Histórico completo de manutenções por veículo.
* **Relatório de Danos e Incidentes**: Registro de incidentes associados a uma reserva.
* **Feedback e Avaliações de Clientes**: Coleta de nota e comentário após a devolução.
* **Perfis Diferenciados (Cliente/Admin)** com menus e permissões específicas.
* **Relatórios Gerenciais (Admin)** para controle da frota e pagamentos.

---

## 🏛️ Arquitetura e Padrões de Projeto
Para garantir um código flexível, manutenível e escalável, o sistema foi construído utilizando diversos Padrões de Projeto (Design Patterns), organizados em suas três categorias principais:

## Padrões Criacionais
* **Singleton**: Garante uma instância única para as classes de gerenciamento (GerenciarCliente, GerenciarVeiculo, Gerenciar_Reserva), centralizando o estado da aplicação.

* **Abstract Factory**: Utilizado para criar famílias de objetos relacionados (neste caso, Cliente e Admin) através das classes ClienteFactory e AdminFactory.

* **Builder**: Aplicado na criação de objetos Veiculo, permitindo uma construção passo a passo e mais legível (VeiculoBuilder).

* **Prototype**: Usado em conjunto com a Factory (ClienteFactory), permitindo a criação de novos usuários (Cliente/Admin) através da clonagem de um protótipo.

---

## Padrões Estruturais

* **Adapter**: Aplicado no sistema de rastreamento GPS, onde GpsAdapter "traduz" a interface de um serviço externo (ExternalGpsService) para uma interface esperada pelo sistema (Veiculo).

* **Bridge**: Utilizado no sistema de notificações. A abstração (Notification) é separada de sua implementação (INotificationSender), permitindo que diferentes tipos de notificação (ex: ConfirmationNotification) sejam enviados por diferentes canais (ex: ConsoleSender, SmsSender) sem acoplamento.

* **Composite**: Aplicado no menu de relatórios gerenciais. Permite que tanto relatórios individuais (RelatorioLeaf) quanto sub-menus (RelatorioComposite) sejam tratados da mesma forma através da interface IRelatorioComponent.

---

## Padrões Comportamentais

* **Strategy**: Usado no método de pagamento (efetuar_pagamento). A classe Reserva (Contexto) delega o algoritmo de cálculo do pagamento para uma estratégia (IPaymentStrategy), permitindo que o usuário escolha dinamicamente entre PagamentoAVistaStrategy, PagamentoCartaoStrategy, etc.

* **Command**: Centraliza todas as ações do usuário (ex: CadastrarClienteCommand, ReservarVeiculoCommand) em objetos. O main.py (Invoker) apenas seleciona e executa o comando apropriado, sem conhecer a lógica interna de cada ação.

* **Iterator**: Aplicado na classe GerenciarVeiculo. Permite percorrer a coleção de veículos de forma controlada (ex: filtrando por padrão apenas os disponíveis) sem expor a lista interna.

---

🛡️ Tratamento de Erros e Exceções
Para aumentar a robustez e a manutenibilidade do código, o sistema implementa um tratamento de exceções customizadas para gerenciar erros de regras de negócio.

Isso separa a lógica de identificação do erro (na camada de modelo/dados) da lógica de apresentação do erro (na camada de visão/controlador).

Criação de Exceções Customizadas: Foi criado um arquivo exceptions.py que define erros de negócio específicos, como CpfJaCadastradoError, ReservaJaPagaError, VeiculoIndisponivelError, etc., todos herdando de uma classe base AppError.

``` bash
   # Em exceptions.py (arquivo novo)
   class AppError(Exception):
       """Classe base para todas as exceções personalizadas da aplicação."""
       pass
   
   class CpfJaCadastradoError(AppError):
       """Lançada ao tentar cadastrar um CPF que já existe."""
       pass
   
   class ReservaJaPagaError(AppError):
       """Lançada ao tentar modificar ou cancelar uma reserva que já foi paga."""
       pass
   
   # ... (e outras exceções)
```

Lançamento (Raise): As classes de lógica (ex: GerenciarCliente em clientes.py, Reserva em reserva.py) agora lançam (raise) essas exceções específicas quando uma regra de negócio é violada (ex: raise CpfJaCadastradoError(...)).

``` bash
   # Em Project_ab2/clientes.py
   # (necessário: from exceptions import CpfJaCadastradoError)
   class GerenciarCliente(Singleton):
       def cadastrar_cliente(self):
           # ... (lógica para pegar nome e cpf) ...
   
           if cpf in [c.cpf for c in self.clientes]:
               # Lança a exceção específica em vez de só imprimir
               raise CpfJaCadastradoError("CPF já cadastrado! Por favor, utilize outro CPF.")
           else:
               novo_cliente = ClienteFactory().criar_usuario(nome, cpf)
               self.clientes.append(novo_cliente)
               print("\nCliente cadastrado com sucesso! \n")
```

Captura (Try...Except): As classes "controladoras" (ex: CadastrarClienteCommand em comandos.py e a função login em main.py) são responsáveis por capturar (try...except) essas exceções específicas e apresentar uma mensagem amigável ao usuário, sem que o programa quebre.

```bash
   # Em Project_ab2/main.py
   # (necessário: from exceptions import CpfJaCadastradoError)
   def login():
       while True:
           # ... (menu de login) ...
           if escolha == '2':
               try:
                   # Tenta executar a ação que pode falhar
                   ger_cli.cadastrar_cliente()
                   input("Pressione Enter para fazer o login...")
               except CpfJaCadastradoError as e:
                   # Captura o erro específico e trata
                   print(f"\n[ERRO NO CADASTRO]: {e}")
                   input("Pressione Enter para tentar novamente...")
```

---

## 💸 Gestão de Caução e Reembolso

A política de pagamentos e reembolsos do sistema foi implementada de forma simples e direta:

1.  **Cobrança do Caução**: Ao efetuar o pagamento de uma reserva, um valor fixo de **caução (depósito de segurança)** é adicionado ao total. Este valor serve como garantia contra possíveis danos ao veículo.

2.  **Processo de Reembolso**: O reembolso está centralizado na devolução do veículo. Ao final do aluguel, o sistema pergunta se ocorreram novos danos:
    * **Sem danos**: O sistema informa que o **caução será reembolsado integralmente**.
    * **Com danos**: O sistema informa que o **caução será retido** para cobrir os custos, e o incidente é registrado.

3.  **Limitações**: O sistema **não processa reembolsos de aluguéis já pagos** em caso de cancelamento. Esta funcionalidade, em um sistema real, exigiria integração com uma API de pagamentos (Stripe, PagSeguro, etc.) para realizar estornos. Por isso, cancelamentos só são permitidos **antes do pagamento**.

---

## 🔑 Login

* **Cliente:** Faça login usando um **CPF cadastrado** (ex: `12345678900`).
* **Admin:** Para acessar o painel administrativo, digite `admin` no campo de CPF e use a senha `admin`.

---

## 🚀 Execução

Para rodar o sistema, execute o arquivo principal no seu terminal:

```bash
python main.py

```




