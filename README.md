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
Para garantir um código flexível, manutenível e escalável, o sistema foi construído utilizando diversos Padrões de Projeto (Design Patterns). O projeto já contava com uma base sólida utilizando padrões como Singleton, Factory, Builder e Prototype. As seguintes modificações foram realizadas para aprimorar ainda mais a arquitetura:

* **Adapter**: Foi aplicado no sistema de rastreamento GPS.
   ``` bash
   # Em Project_ab2/veiculos.py
   
   # O Serviço Externo (Adaptee) com uma interface incompatível
   class ExternalGpsService:
       def fetch_coords(self, placa_veiculo: str) -> dict:
           print("-> [API Externa] Buscando coordenadas...")
           # ... lógica para buscar ou criar coordenadas ...
           return self._locations[placa]
   
   # O Adapter que traduz a interface
   class GpsAdapter:
       def __init__(self, gps_service: ExternalGpsService, placa: str):
           self._adaptee = gps_service
           self._placa = placa
    
       @property 
       def localizacao(self) -> str:
           print("-> [Adapter] Chamando API externa e formatando o resultado...")
           # Chama o método do adaptee
           coords = self._adaptee.fetch_coords(self._placa)
           # Formata a saída para a string esperada pelo cliente
           return f"Lat: {coords['lat']:.6f}, Lon: {coords['lon']:.6f} (Via API Externa)"
   
   # O Cliente (Veiculo) usa o Adapter sem saber da complexidade
   class Veiculo:
       def __init__(self, modelo='', placa='', ano='', valor=0.0):
           # ...
           gps_service = ExternalGpsService()
           # O Veiculo é instanciado com o GpsAdapter
           self._gps_tracker = GpsAdapter(gps_service, self.placa)
   
       @property
       def localizacao(self):
           # O Veiculo apenas chama .localizacao,
           # que é a interface simplificada pelo Adapter
           return self._gps_tracker.localizacao
      ```

* **Bridge**: Foi aplicado no sistema de notificações para clientes (confirmação de reserva, pagamento, etc.).

* **Composite**: Foi aplicado no menu de relatórios gerenciais, permitindo que sub-menus (Composite) e relatórios finais (Leaf) sejam tratados da mesma forma.

---

## Padrões Comportamentais

* **Strategy**: Foi aplicado no método de pagamento da classe Reserva.

* **Command**: Foi aplicado no menu principal e no tratamento das ações do usuário em main.py.

* **Iterator**: Foi aplicado na classe GerenciarVeiculo para fornecer uma forma de acessar a coleção de veículos (filtrando por padrão apenas os disponíveis) sem expor a estrutura de lista interna.

---

🛡️ Tratamento de Erros e Exceções
Para aumentar a robustez e a manutenibilidade do código, o sistema implementa um tratamento de exceções customizadas para gerenciar erros de regras de negócio.

Isso separa a lógica de identificação do erro (na camada de modelo/dados) da lógica de apresentação do erro (na camada de visão/controlador).

Criação de Exceções Customizadas: Foi criado um arquivo exceptions.py que define erros de negócio específicos, como CpfJaCadastradoError, ReservaJaPagaError, VeiculoIndisponivelError, etc., todos herdando de uma classe base AppError.

Lançamento (Raise): As classes de lógica (ex: GerenciarCliente em clientes.py, Reserva em reserva.py) agora lançam (raise) essas exceções específicas quando uma regra de negócio é violada (ex: raise CpfJaCadastradoError(...)).

Captura (Try...Except): As classes "controladoras" (ex: CadastrarClienteCommand em comandos.py e a função login em main.py) são responsáveis por capturar (try...except) essas exceções específicas e apresentar uma mensagem amigável ao usuário, sem que o programa quebre.

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

