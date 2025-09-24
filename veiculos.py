# C:\Users\ResTIC16\Desktop\PJ\ProjectPS-OO\veiculos.py

from datetime import datetime
import random

class Veiculo:
    def __init__(self, modelo='', placa='', ano='', valor=0.0):
        self._modelo = modelo
        self._placa = placa
        self._ano = ano
        self._valor = valor
        self._disponivel = True
        self._manutencao = []
        # Simulação de GPS: Coordenadas iniciais aleatórias (Ex: São Paulo)
        self._latitude = random.uniform(-23.5, -23.6)
        self._longitude = random.uniform(-46.6, -46.7)

    @property
    def modelo(self):
        return self._modelo
    @property
    def placa(self):
        return self._placa
    @property
    def ano(self):
        return self._ano
    @property
    def valor(self):
        return self._valor
    @property
    def disponivel(self):
        return self._disponivel

    @disponivel.setter
    def disponivel(self, valor):
        self._disponivel = valor

    @property
    def manutencao(self):
        return self._manutencao

    @property
    def localizacao(self):
        """Propriedade para obter a localização atual do veículo."""
        return f"Lat: {self._latitude:.6f}, Lon: {self._longitude:.6f}"

    def simular_movimentacao(self):
        """Simula a movimentação do veículo alterando levemente suas coordenadas."""
        self._latitude += random.uniform(-0.01, 0.01)
        self._longitude += random.uniform(-0.01, 0.01)

    def registrar_manutencao(self):
        desc = input(f"Descreva a manutenção do veículo {self._modelo} ({self._placa}): ").strip()
        while True:
            data = input("Data da manutenção (dd/mm/aaaa): ").strip()
            try:
                data_obj = datetime.strptime(data, "%d/%m/%Y")
                data_f = data_obj.strftime("%d/%m/%Y")
                break
            except ValueError:
                print("Data inválida! Use o formato correto dd/mm/aaaa.")

        while True:
            custo_input = input("Custo da manutenção: R$ ").replace(',', '.')
            try:
                custo = float(custo_input)
                if custo < 0:
                    print("O custo não pode ser negativo.")
                    continue
                break
            except ValueError:
                print("Por favor, digite um valor numérico válido para o custo.")

        self._manutencao.append({'descricao': desc, 'data': data_f, 'custo': custo})
        print("Manutenção registrada com sucesso!\n")

    def listar_manutencoes(self):
        if not self._manutencao:
            print(f"O veículo {self._modelo} ({self._placa}) não possui manutenções.\n")
            return
        print(f"Manutenções do veículo {self._modelo} ({self._placa}):")
        for i, m in enumerate(self._manutencao, 1):
            print(f"{i}. Data: {m['data']} | Desc: {m['descricao']} | Custo: R${m['custo']:.2f}")


class GerenciarVeiculo:
    def __init__(self):
        self.veiculos = []

    def cadastrar_veiculo(self):
        modelo = input("Modelo: ").title()
        while True:
            placa = input("Placa: ").upper()
            if len(placa) == 7 and placa not in [v.placa for v in self.veiculos]:
                break
            print("Placa inválida ou já cadastrada!")

        while True:
            try:
                ano = (input("Ano: "))
                if len(ano) == 4 and ano.isdigit() and 1960 < int(ano) <= datetime.now().year + 1:
                    break
                else:
                    print(f"O ano deve ser válido! (1961 - {datetime.now().year + 1})")
            except ValueError:
                print("Entrada inválida! Digite um número válido.")

        while True:
            try:
                valor = float(input("Valor por dia: "))
                if valor > 0:
                    break
                else:
                    print("O valor deve ser maior que zero.")
            except ValueError:
                print("Entrada inválida! Digite um número válido.")

        novo = Veiculo(modelo, placa, ano, valor)
        self.veiculos.append(novo)
        print("Veículo cadastrado com sucesso! \n")

    def listar_veiculos(self):
        print("\n=== VEÍCULOS DISPONÍVEIS ===")
        disponiveis = [v for v in self.veiculos if v.disponivel]
        if not disponiveis:
            print("Nenhum veículo disponível no momento.")
            return
        for i, v in enumerate(disponiveis, start=1):
            print(f"{i} - Modelo: {v.modelo} | Ano: {v.ano} | R${v.valor:.2f}/dia")

    def estatisticas_utilizacao(self):
        total = len(self.veiculos)
        if total == 0:
            print("\nNenhum veículo cadastrado na frota.")
            return
        disponiveis = sum(1 for v in self.veiculos if v.disponivel)
        alugados = total - disponiveis
        print(f"\nTotal de veículos: {total}")
        print(f"Disponíveis: {disponiveis}")
        print(f"Alugados: {alugados}\n")

    def historico_manutencoes(self):
        print("\n=== HISTÓRICO GERAL DE MANUTENÇÕES ===")
        manutencoes_existentes = False
        for v in self.veiculos:
            if v.manutencao:
                manutencoes_existentes = True
                print(f"\nVeículo: {v.modelo} ({v.placa})")
                for m in v.manutencao:
                    print(f"- Data: {m['data']} | Descrição: {m['descricao']} | Custo: R${m['custo']:.2f}")
        if not manutencoes_existentes:
            print("Nenhum registro de manutenção encontrado na frota.")