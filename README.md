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