import os
from datetime import datetime, timedelta
from clientes import Singleton
from abc import ABC, abstractclassmethod, abstractmethod

# PADRÃO STRATEGY
class IPaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, total_diarias: float, caucao: float) -> float:
        pass

class PagamentoAVistaStrategy(IPaymentStrategy):
    def process_payment(self, total_diarias: float, caucao: float) -> float:
        valor_com_desconto = total_diarias * 0.90
        print(f"INFO: Desconto de 10% para pagamento à vista aplicado sobre as diárias.")
        return valor_com_desconto + caucao

class PagamentoCartaoStrategy(IPaymentStrategy):
    def process_payment(self, total_diarias: float, caucao: float) -> float:
        print("INFO: Pagamento com cartão selecionado (sem desconto adicional).")
        return total_diarias + caucao
        
class PagamentoPixStrategy(IPaymentStrategy):
    """
    Uma nova estratégia! Pagamento via PIX com 5% de desconto.
    """
    def process_payment(self, total_diarias: float, caucao: float) -> float:
        valor_com_desconto = total_diarias * 0.95
        print(f"INFO: Desconto de 5% para pagamento via PIX aplicado sobre as diárias.")
        return valor_com_desconto + caucao
# implementor
class INotificationSender(ABC):
    @abstractclassmethod
    def send(self, message: str):
        pass

# Concrete Implementors
class ConsoleSender(INotificationSender):
    def send(self, message: str):
        print("\n--- [NOTIFICAÇÃO VIA CONSOLE] ---")
        print(message)
        print("----------------------------------\n")

class EmailSender(INotificationSender):
    """Simula o envio de uma notificação por email."""
    def send(self, message: str):
        print("\n--- [SIMULANDO ENVIO DE EMAIL] ---")
        print(f"Para: cliente@email.com")
        print(f"Assunto: Novidades da sua Reserva")
        print(f"Corpo: {message}")
        print("----------------------------------\n")
        
class SmsSender(INotificationSender):
    """Simula o envio de uma notificação por SMS."""
    def send(self, message: str):
        print(f"\n--- [SMS PARA +5511999998888]: {message} ---\n")

# Abstraction
class Notification:
    def __init__(self, sender: INotificationSender):
        self._sender = sender
    def send_message(self, message: str):
        self._sender.send(message)

# Refined Abstractions
class ConfirmationNotification(Notification):
    def __init__(self, sender: INotificationSender, reserva):
        super().__init__(sender)
        self._reserva = reserva
    def notify(self):
        message = (f"Olá! Sua reserva para o veículo {self._reserva.modelo} "
                   f"por {self._reserva.dias} dias foi confirmada com sucesso. "
                   f"Valor total: R${self._reserva.total:.2f}")
        print("-> Preparando notificação de confirmação...")
        self.send_message(message)

class PaymentNotification(Notification):
    def __init__(self, sender: INotificationSender, reserva):
        super().__init__(sender)
        self._reserva = reserva
    def notify(self):
        message = (f"Seu pagamento no valor de R${self._reserva.total + self._reserva.VALOR_CAUCAO:.2f} "
                   f"para a reserva do veículo {self._reserva.modelo} foi processado. Obrigado!")
        print("-> Preparando notificação de pagamento...")
        self.send_message(message)

class Reserva:
    VALOR_CAUCAO = 250.00

    def __init__(self):
        self._cpf = ''
        self._placa = ''
        self._modelo = ''
        self._dias = 0
        self._total = 0.0
        self._deposito = 0.0
        self._incidentes = []
        self._pago = False
        self._finalizada = False
        self._avaliacao = None
        self._comentario = None

    @property
    def cpf(self): return self._cpf
    @property
    def placa(self): return self._placa
    @property
    def modelo(self): return self._modelo
    @property
    def dias(self): return self._dias
    @property
    def total(self): return self._total
    @property
    def pago(self): return self._pago
    @property
    def finalizada(self): return self._finalizada
    @property
    def incidentes(self): return self._incidentes

    @dias.setter
    def dias(self, valor): self._dias = valor
    @total.setter
    def total(self, valor): self._total = valor

    def fazer_reserva(self, cliente, veiculo, dias):
        if not cliente or not veiculo or dias <= 0:
            print("Dados inválidos para reserva.")
            return

        self._cpf = cliente.cpf
        self._placa = veiculo.placa
        self._modelo = veiculo.modelo
        self._dias = dias
        
        total_bruto = veiculo.valor * dias
        desconto_longa_duracao = 0.0
        if dias >= 7:
            desconto_longa_duracao = total_bruto * 0.10
            print(f"INFO: Desconto de longa duração (10%) aplicado: -R$ {desconto_longa_duracao:.2f}")

        self.total = total_bruto - desconto_longa_duracao
        self._deposito = self.VALOR_CAUCAO
        veiculo.disponivel = False
        
        print(f"\nReserva realizada com sucesso para {cliente.nome}.")
        print(f"Valor das diárias (com desconto, se aplicável): R${self.total:.2f}")
        print(f"Caução a ser pago: R${self._deposito:.2f}")

# Dentro da classe Reserva, substitua o método inteiro:

    def efetuar_pagamento(self):
        from main import PROMO_CODES
        
        if self.pago:
            print("Pagamento já realizado.")
            return

        total_diarias = self.total
        
        cupom = input("Você possui um cupom de desconto? (Deixe em branco se não tiver): ").upper()
        if cupom and cupom in PROMO_CODES:
            tipo, valor = PROMO_CODES[cupom]
            desconto_cupom = 0
            if tipo == 'perc':
                desconto_cupom = self.total * valor
                print(f"Cupom '{cupom}' aplicado! Desconto de {valor*100:.0f}%: -R$ {desconto_cupom:.2f}")
            elif tipo == 'fixo':
                desconto_cupom = valor
                print(f"Cupom '{cupom}' aplicado! Desconto de R$ {desconto_cupom:.2f}")
            
            total_diarias -= desconto_cupom
            if total_diarias < 0: total_diarias = 0
        elif cupom:
            print("Cupom inválido ou expirado.")

        print(f"\nTotal das diárias (com descontos de cupom, se houver): R$ {total_diarias:.2f}")
        print(f"Valor do caução: R$ {self._deposito:.2f}")

        # --- A MÁGICA DO STRATEGY ACONTECE AQUI ---
        
        # Mapeia a entrada do usuário para a classe da Estratégia
        payment_strategies = {
            '1': PagamentoAVistaStrategy,
            '2': PagamentoCartaoStrategy,
            '3': PagamentoPixStrategy
        }
        
        strategy = None
        while not strategy:
            print("\nEscolha a forma de pagamento:")
            print("1 - À Vista (10% de desconto nas diárias)")
            print("2 - Cartão de Crédito")
            print("3 - PIX (5% de desconto nas diárias)")
            opcao = input("Opção: ").strip()

            if opcao in payment_strategies:
                # Cria a instância da estratégia escolhida
                strategy_class = payment_strategies[opcao]
                strategy = strategy_class()
            else:
                print("Opção inválida. Tente novamente.")
        
        # O 'Contexto' (Reserva) usa o objeto da estratégia para calcular o valor.
        # Ele não sabe qual algoritmo está sendo executado, apenas que ele existe.
        total_a_pagar = strategy.process_payment(total_diarias, self._deposito)

        print(f"\nTOTAL FINAL A PAGAR: R$ {total_a_pagar:.2f}")

        confirmar = input("Confirmar pagamento? (s/n) ").lower()
        if confirmar == 's':
            self._pago = True
            print("Pagamento efetuado com sucesso!")
            
            # (Opcional, mas mantém a consistência do padrão Bridge que fizemos antes)
            sender_sms = SmsSender()
            notificacao_pagamento = PaymentNotification(sender_sms, self)
            notificacao_pagamento.notify()
        else:
            print("Pagamento cancelado.")
    
    def devolver_veiculo(self, lista_veiculos):
        if not self.pago:
            print("Não é possível devolver o veículo antes de efetuar o pagamento.\n")
            return

        veiculo = next((v for v in lista_veiculos if v.placa == self.placa), None)
        if not veiculo:
            print("Veículo não encontrado!\n")
            return

        status_reembolso = ""
        incidente_devolucao = input("Houve algum novo dano ou incidente com o veículo? (s/n) ").lower()
        if incidente_devolucao == 's':
            print(f"O valor do caução será retido para cobrir os danos.")
            self.registrar_incidente_devolucao()
            status_reembolso = f"Status do Caução: Retido (R${self._deposito:.2f}) para cobrir novos danos."
        else:
            status_reembolso = f"Status do Caução: Reembolsado integralmente (R${self._deposito:.2f})."

        veiculo.disponivel = True
        self._finalizada = True
        
        avaliar = input("Deseja avaliar o aluguel? (s/n): ").strip().lower()
        if avaliar == 's':
            self.avaliar_aluguel()

        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "="*50)
        print("              RESUMO DA DEVOLUÇÃO")
        print("="*50)
        print(f"Veículo {veiculo.modelo} ({veiculo.placa}) devolvido com sucesso!")
        print(status_reembolso)
        print("="*50 + "\n")

    def avaliar_aluguel(self):
        while True:
            try:
                nota = int(input("Dê uma nota de 1 a 5 para o aluguel: "))
                if 1 <= nota <= 5: break
                else: print("Digite uma nota entre 1 e 5.")
            except ValueError: print("Por favor, digite um número válido.")
        
        self._comentario = input("Deseja deixar um comentário? (opcional): ").strip()
        self._avaliacao = nota
        print("Avaliação registrada com sucesso!\n")

    def exibir_contrato(self, cliente):
        # Simula data de retirada como sendo "dias" atrás a partir de agora
        data_retirada = datetime.now() - timedelta(days=self.dias)
        data_devolucao_prevista = data_retirada + timedelta(days=self.dias)
        print("\n========== CONTRATO DE LOCAÇÃO ==========")
        print(f"Cliente: {cliente.nome} | CPF: {cliente.cpf}")
        print(f"Veículo: {self.modelo} | Placa: {self.placa}")
        print(f"Período: {self.dias} dias | Valor Diárias: R${self.total:.2f}")
        print(f"Valor Caução: R${self._deposito:.2f}")
        print(f"Pagamento: {'Pago' if self.pago else 'Pendente'}")
        print(f"Data de Retirada: {data_retirada.strftime('%d/%m/%Y')}")
        print(f"Data de Devolução Prevista: {data_devolucao_prevista.strftime('%d/%m/%Y')}")
        print("="*50 + "\n")

    def adicionar_incidente(self, data, descricao):
        self._incidentes.append({'data': data, 'descricao': descricao})
        print("Incidente registrado com sucesso!")

    def registrar_incidente_devolucao(self):
        data = datetime.now().strftime("%d/%m/%Y")
        descricao = input("Descreva o dano/incidente ocorrido: ")
        self.adicionar_incidente(data, descricao)

class Gerenciar_Reserva(Singleton):
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        
        self.reservas = []
        self._initialized = True

    def fazer_reserva(self, cliente, veiculo, dias):
        nova_reserva = Reserva()
        nova_reserva.fazer_reserva(cliente, veiculo, dias)
        self.reservas.append(nova_reserva)
        # Canal 1: Console
        sender_console = ConsoleSender()
        notificacao_console = ConfirmationNotification(sender_console, nova_reserva)
        notificacao_console.notify()
        
        # Canal 2: Email (a notificação não muda, só o "enviador")
        sender_email = EmailSender()
        notificacao_email = ConfirmationNotification(sender_email, nova_reserva)
        notificacao_email.notify()

    def cancelar_reserva(self, reserva, lista_veiculos):
        if reserva.pago:
            print("\nNão é possível cancelar uma reserva que já foi paga.")
            return

        veiculo = next((v for v in lista_veiculos if v.placa == reserva.placa), None)
        if veiculo:
            veiculo.disponivel = True

        self.reservas.remove(reserva)
        print("\nReserva cancelada com sucesso!")

    def modificar_reserva(self, reserva, lista_veiculos):
        if reserva.pago:
            print("\nNão é possível modificar uma reserva que já foi paga.")
            return

        veiculo = next((v for v in lista_veiculos if v.placa == reserva.placa), None)
        if not veiculo:
            print("Veículo da reserva não encontrado.")
            return

        try:
            novos_dias = int(input(f"A reserva atual é de {reserva.dias} dias. Digite a nova quantidade de dias: "))
            if novos_dias <= 0:
                print("A quantidade de dias deve ser positiva.")
                return
            
            # Recalcula o total com base nos novos dias e aplica desconto se necessário
            total_bruto = veiculo.valor * novos_dias
            desconto_longa_duracao = 0.0
            if novos_dias >= 7:
                desconto_longa_duracao = total_bruto * 0.10

            reserva.dias = novos_dias
            reserva.total = total_bruto - desconto_longa_duracao
            
            print("\nReserva modificada com sucesso!")
            print(f"Novo período: {reserva.dias} dias. Novo total das diárias: R${reserva.total:.2f}")

        except ValueError:
            print("Entrada inválida. Digite um número de dias.")

    def listar_incidentes_por_placa(self, placa):
        reservas_veiculo = [r for r in self.reservas if r.placa == placa]
        if not reservas_veiculo:
            print(f"Nenhuma reserva encontrada para a placa {placa}.")
            return
        
        print(f"\nIncidentes do veículo de placa {placa}:")
        incidentes_encontrados = False
        for r in reservas_veiculo:
            if r.incidentes:
                incidentes_encontrados = True
                for idx, inc in enumerate(r.incidentes, 1):
                    print(f"- Cliente (CPF {r.cpf}) em {inc['data']}: {inc['descricao']}")
        
        if not incidentes_encontrados:
            print("Nenhum incidente registrado para este veículo.")

    def controle_pagamentos(self):
        pendentes = [r for r in self.reservas if not r.pago and not r.finalizada]
        pagas = [r for r in self.reservas if r.pago]
        
        print("\n=== CONTROLE DE PAGAMENTOS ===")
        print("\n--- Pagamentos Pendentes ---")
        if not pendentes:
            print("Nenhum pagamento pendente.")
        else:
            for r in pendentes:
                print(f"Cliente (CPF {r.cpf}) - Veículo {r.modelo} - R${r.total + r.deposito:.2f}")
        
        print("\n--- Pagamentos Realizados ---")
        if not pagas:
            print("Nenhum pagamento realizado.")
        else:
             for r in pagas:
                 print(f"Cliente (CPF {r.cpf}) - Veículo {r.modelo} - R${r.total + r.deposito:.2f}")