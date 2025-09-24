# C:\Users\ResTIC16\Desktop\PJ\ProjectPS-OO\reserva.py

import os
from datetime import datetime, timedelta

# NENHUMA IMPORTAÇÃO DO 'main' AQUI EM CIMA

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

    def efetuar_pagamento(self):
        # <<< MUDANÇA CRUCIAL AQUI
        # A importação é feita aqui dentro, apenas quando a função é chamada.
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

        total_a_pagar = total_diarias + self._deposito
        print(f"\nTotal das diárias (com descontos): R$ {total_diarias:.2f}")
        print(f"Valor do caução: R$ {self._deposito:.2f}")
        print(f"TOTAL A PAGAR: R$ {total_a_pagar:.2f}")

        while True:
            opcao = input("Pagamento à vista (1) ou parcelado (2)? ").strip()
            if opcao == '1':
                valor_com_desconto = total_diarias * 0.9 + self._deposito
                print(f"Desconto de 10% nas diárias aplicado. Total a pagar: R${valor_com_desconto:.2f}")
                confirmar = input("Confirmar pagamento? (s/n) ").lower()
                if confirmar == 's':
                    self._pago = True
                    print("Pagamento efetuado com sucesso!")
                break
            elif opcao == '2':
                # Implementação de parcelamento
                print("Parcelamento indisponível no momento.")
                break
            else:
                print("Opção inválida.")
    
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

class Gerenciar_Reserva:
    def __init__(self):
        self.reservas = []

    def fazer_reserva(self, cliente, veiculo, dias):
        nova_reserva = Reserva()
        nova_reserva.fazer_reserva(cliente, veiculo, dias)
        self.reservas.append(nova_reserva)

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