from veiculos import Veiculo
import os
from datetime import datetime, timedelta

class Reserva:
    
    def __init__(self):
        self._cpf = ''
        self._placa = ''
        self._modelo = ''
        self._dias = 0
        self._total = 0.0
        self._incidentes = []
        self._pago = False
        self._finalizada = False
        self._avaliacao = None
        self._comentario = None

    @property
    def pago(self):
        return self._pago

    @pago.setter
    def pago(self, valor):
        if isinstance(valor, bool):
            self._pago = valor
        else:
            print("Valor inválido para pago. Use True ou False.")
            
    @property
    def finalizada(self):
        return self._finalizada

    @finalizada.setter
    def finalizada(self, valor):
        if isinstance(valor, bool):
            self._finalizada = valor
        else:
            print("Valor inválido para finalizada. Use True ou False.")

    @property
    def incidentes(self):
        return self._incidentes


    def fazer_reserva(self, cliente, veiculo, dias):
        if not cliente or not veiculo or dias <= 0:
            print("Dados inválidos para reserva.")
            return

        self.cpf = cliente.cpf
        self.placa = veiculo.placa
        self.modelo = veiculo.modelo
        self.dias = dias
        self.total = veiculo.valor * dias
        veiculo.disponivel = False
        print(f"Reserva realizada com sucesso para {cliente.nome}. Total: R${self.total:.2f}")

    def efetuar_pagamento(self):
        if self.pago:
            print("Pagamento já realizado.")
            return

        print(f"Total da reserva: R$ {self.total:.2f}")
        while True:
            opcao = input("Pagamento à vista (1) ou parcelado (2)? ").strip()
            if opcao == '1':
                desc = self.total * 0.9
                print(f"Desconto de 10% aplicado. Total a pagar: R${desc:.2f}")
                confirmar = input("Confirmar pagamento? (s/n) ").lower()
                if confirmar == 's':
                    self.pago = True
                    print("Pagamento efetuado com sucesso!")
                break
            elif opcao == '2':
                print("Parcelamos em até 12x. Até 3x sem juros!\n")
                while True:
                    try:
                        parcelas = int(input("Número de parcelas (1 a 12): "))
                        if 1 <= parcelas <= 12:
                            break
                        else:
                            print("Escolha um valor entre 1 e 12.")
                    except ValueError:
                        print("Digite um número válido.")
                for i in range(1, parcelas+1):
                    if parcelas <= 3:
                        valor_parcela = self.total / parcelas
                    else:
                        valor_parcela = (self.total / parcelas) * (1 + 0.05) ** i
                    print(f"Parcela {i}: R${valor_parcela:.2f}")
                confirmar = input("Confirmar pagamento? (s/n) ").lower()
                if confirmar == 's':
                    self.pago = True
                    print("Pagamento efetuado com sucesso!")
                break
            else:
                print("Opção inválida.")

    def devolver_veiculo(self, lista_veiculos, lista_reservas):
        if not self.pago:
            print("Não é possível devolver o veículo antes de efetuar o pagamento total da reserva.\n")
            return

        veiculo = next((v for v in lista_veiculos if v.placa == self.placa), None)
        if not veiculo:
            print("Veículo não encontrado!\n")
            return

        veiculo.disponivel = True
        print(f"\nVeículo {veiculo.modelo} ({veiculo.placa}) devolvido com sucesso!\n")

        # Registro de manutenção
        while True:
            opcao = input("Deseja registrar alguma manutenção para este veículo? (s/n): ").strip().lower()
            if opcao == 's':
                veiculo.registrar_manutencao()
                break
            elif opcao == 'n':
                break
            else:
                print("Digite uma opção válida (s/n).")

        # Avaliação do aluguel
        while True:
            avaliar = input("Deseja avaliar o aluguel? (s/n): ").strip().lower()
            if avaliar == 's':
                self.avaliar_aluguel()
                break
            elif avaliar == 'n':
                break
            else:
                print("Digite uma opção válida (s/n).")


        # Marcar como finalizada (não remover da lista)
        self.finalizada = True

        # Limpar tela e exibir resumo completo
        os.system('cls')
        print("===== Resumo da Reserva =====")
        print(f"Cliente (CPF): {self.cpf}")
        print(f"Veículo: {self.modelo}")
        print(f"Dias alugados: {self.dias}")
        print(f"Valor total pago: R$ {self.total:.2f}")

        if veiculo.manutencao:
            print("\nManutenções realizadas neste veículo durante a reserva:")
            for i, m in enumerate(veiculo.manutencao, 1):
                print(f"{i}. Data: {m['data']} | Descrição: {m['descricao']} | Custo: R${m['custo']}")

        # Somente exibe avaliação se existir
        if hasattr(self, 'avaliacao'):
            print(f"\nAvaliação do aluguel: Nota {self.avaliacao}")
            if hasattr(self, 'comentario') and self.comentario:
                print(f"Comentário: {self.comentario}")

        print("\nSeu histórico de reservas:")
        historico = [r for r in lista_reservas if hasattr(r, 'cpf') and r.cpf == self.cpf]
        if not historico:
            print("Nenhuma reserva encontrada para este CPF.\n")
        else:
            for idx, r in enumerate(historico, 1):
                status = "Finalizada" if getattr(r, 'finalizada', False) else "Em andamento"
                print(f"{idx}. Veículo: {r.modelo} | Placa: {r.placa} | Dias: {r.dias} | Total: R${r.total:.2f} | Status: {status}")


    def avaliar_aluguel(self):
        if not self.pago:
            print("Você só pode avaliar o aluguel após efetuar o pagamento da reserva.\n")
            return

        while True:
            try:
                nota = int(input("Dê uma nota de 1 a 5 para o aluguel: "))
                if 1 <= nota <= 5:
                    break
                else:
                    print("Digite uma nota entre 1 e 5.")
            except ValueError:
                print("Por favor, digite um número válido.")

        comentario = input("Deseja deixar um comentário? (opcional): ").strip()
        self.avaliacao = nota
        self.comentario = comentario
        print("Avaliação registrada com sucesso!\n")

    def exibir_contrato(self, cliente):
        data_inicio = datetime.now()
        data_fim = data_inicio + timedelta(days=self.dias)
        print("\n========== CONTRATO DE LOCAÇÃO ==========")
        print(f"Cliente: {cliente.nome} | CPF: {cliente.cpf}")
        print(f"Veículo: {self.modelo} | Placa: {self.placa} | Valor diário: R${self.total/self.dias:.2f}")
        print(f"Período: {self.dias} dias | Total: R${self.total:.2f}")
        print(f"Pagamento: {'Pago' if self.pago else 'A definir'}")
        print(f"Data de devolução prevista: {data_fim.strftime('%d/%m/%Y')}")
        print("========================================\n")

    def adicionar_incidente(self, data, descricao):
        self._incidentes.append({'data': data, 'descricao': descricao})
        print("Incidente registrado com sucesso!")

class Gerenciar_Reserva:
    def __init__(self):
        self._reservas = []  # atributo privado

    @property
    def reservas(self):
        return self._reservas
    
    def fazer_reserva(self, cliente, veiculo, dias):
        if not cliente or not veiculo or dias <= 0:
            print("Dados inválidos para reserva.")
            return
        nova_reserva = Reserva()
        nova_reserva.fazer_reserva(cliente, veiculo, dias)
        self._reservas.append(nova_reserva)

    def buscar_reserva_por_cpf(self, cpf):
        return [r for r in self._reservas if r.cpf == cpf]

    def historico_cliente(self, cpf, cliente=None):
        historico = [r for r in self._reservas if r.cpf == cpf]
        if not historico:
            print("Nenhuma reserva encontrada para este CPF.\n")
            return
        print("\n=== HISTÓRICO DE RESERVAS ===")
        for idx, r in enumerate(historico, 1):
            status = "Finalizada" if r.finalizada or r.pago else "Em andamento"
            print(f"\nReserva {idx} - Status: {status}")
            print(f"Veículo: {r.modelo} | Placa: {r.placa} | Dias: {r.dias} | Total: R${r.total:.2f}")
            if cliente:
                print(f"Cliente: {cliente.nome} | CPF: {cliente.cpf}")
            if r.avaliacao:
                print(f"Avaliação: {r.avaliacao}")
                if r.comentario:
                    print(f"Comentário: {r.comentario}")
            if r.incidentes:
                print("Incidentes:")
                for inc in r.incidentes:
                    print(f"- Data: {inc['data']} | Descrição: {inc['descricao']}")
            print("=" * 50)

    def efetuar_pagamento(self, cpf, placa):
        r = next((res for res in self._reservas if res.cpf == cpf and res.placa == placa), None)
        if r:
            r.efetuar_pagamento()
        else:
            print("Reserva não encontrada.")

    def devolver_reserva(self, cpf, placa, veiculos):
        r = next((res for res in self._reservas if res.cpf == cpf and res.placa == placa), None)
        if r:
            veiculo = next((v for v in veiculos if v.placa == placa), None)
            if veiculo:
                r.devolver_veiculo(veiculo)
            else:
                print("Veículo não encontrado.")
        else:
            print("Reserva não encontrada.")

    def registrar_avaliacao(self, cpf, placa):
        r = next((res for res in self._reservas if res.cpf == cpf and res.placa == placa), None)
        if r:
            r.avaliar_aluguel()
        else:
            print("Reserva não encontrada.")

    def controle_pagamentos(self):
        pendentes = [r for r in self._reservas if not r.pago]
        print("\n=== Pagamentos pendentes ===")
        for r in pendentes:
            print(f"{r.cpf} - {r.modelo} - R${r.total:.2f}")
            
    def registrar_incidente(self, cpf, placa, data, descricao):
            reserva = next((r for r in self._reservas if r.cpf == cpf and r.placa == placa), None)
            if reserva:
                reserva.adicionar_incidente(data, descricao)
            else:
                print("Reserva não encontrada.")

    def listar_incidentes_por_placa(self, placa):
        reservas = [r for r in self._reservas if r.placa == placa]
        if not reservas:
            print(f"Nenhuma reserva encontrada para a placa {placa}.")
            return

        for r in reservas:
            print(f"\nIncidentes da reserva do veículo {r.modelo} ({r.placa}):")
            if r.incidentes:  # usa a propriedade
                for idx, inc in enumerate(r.incidentes, 1):
                    print(f"{idx}. Data: {inc['data']} | Descrição: {inc['descricao']}")
            else:
                print("Nenhum incidente registrado nesta reserva.")