# 🚗 AV Rental Car System

Este é um sistema estruturado de **locação de veículos**, desenvolvido em Python como parte da disciplina de Projeto de Software.

O sistema oferece funcionalidades completas como cadastro de clientes e veículos, realização de reservas, controle de manutenções, pagamentos (à vista ou parcelado com juros), devolução de veículos, avaliação da experiência de aluguel, registro de incidentes e geração automática de contrato de locação.

---

## ✅ Funcionalidades implementadas

* ✅ **Cadastro de clientes** (nome e CPF com verificação de duplicidade)
* ✅ **Cadastro de veículos** (modelo, placa, ano, valor por dia e disponibilidade)
* ✅ **Listagem de veículos disponíveis**
* ✅ **Reserva de veículos** (com verificação de cliente cadastrado e veículo disponível)
* ✅ **Exibição de contrato de locação**
* ✅ **Efetuar pagamento**:

  * À vista (10% de desconto)
  * Parcelado (até 3x sem juros; de 4x até 12x com juros compostos de 5% a.m.)
* ✅ **Registrar manutenção** (data, descrição e custo)
* ✅ **Relatar incidente** (data e descrição)
* ✅ **Avaliação do aluguel** (nota de 1 a 5 e comentário)
* ✅ **Devolução do veículo** (libera o veículo e opcionalmente registra manutenção e avaliação)
* ✅ **Listagem de manutenções realizadas em um veículo**
* ✅ **Login de usuários** (autenticação por CPF para clientes e credencial para admin)
* ✅ **Perfis diferenciados (Cliente/Admin)**

  * Cliente: efetuar reservas, visualizar histórico, avaliar serviço.
  * Admin: cadastrar veículos, registrar manutenções, consultar relatórios e gerenciar reservas.
* ✅ **Histórico de reservas finalizadas** (com avaliações, incidentes e contratos disponíveis)
* ✅ **Relatórios gerenciais (Admin)**

  * Estatísticas de utilização da frota
  * Histórico de manutenções
  * Controle de pagamentos realizados e pendentes

---

## 📚 Estrutura do Código

### 🧱 Classes principais:

* `clientes`: gerencia dados de clientes e autenticação.
* `veiculos`: gerencia dados dos veículos, disponibilidade e manutenções.
* `reserva`: gerencia reservas, pagamentos, devoluções, incidentes, avaliações e relatórios.

### 🔧 Funções principais

* `cadastrar_cliente()`
* `cadastrar_veiculo()`
* `listar_veiculos()`
* `fazer_reserva()`
* `buscar_reserva_por_cpf()`
* `efetuar_pagamento()`
* `registrar_manutencao()`
* `relatar_incidente()`
* `avaliar_aluguel()`
* `devolver_veiculo()`
* `exibir_contrato()`
* `historico_cliente()`
* `estatisticas_utilizacao()`
* `historico_manutencoes()`
* `controle_pagamentos()`
* `menu()` – Interface principal de interação com o sistema

---

## 📌 Modelagem dos dados

A modelagem é simples e direta, com cada classe encapsulando seus próprios atributos e comportamentos, promovendo **coerência e reuso das funções**.

* **Cliente**

  * Nome
  * CPF

* **Veículo**

  * Modelo
  * Placa
  * Ano
  * Valor por dia
  * Disponibilidade
  * Manutenções

* **Reserva**

  * CPF do cliente
  * Placa e modelo do veículo
  * Dias alugados
  * Total
  * Pagamento (status e forma)
  * Incidentes
  * Avaliação

---

## 🔑 Login

* **Cliente:** faça login usando o **CPF cadastrado**.
* **Admin:** para acessar o painel administrativo, digite `admin` no campo de CPF e use a senha `admin`.

---

## 🚀 Execução

Para rodar o sistema:

# Clone o repositório
git clone https://github.com/arthurvalves/ProjectPS-OO.git

# Entre na pasta do projeto
cd ProjectPS-OO

# Execute o sistema
```bash
python main.py
```


