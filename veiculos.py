from datetime import datetime
import random
from clientes import Singleton

# Adapter
class ExternalGpsService:
    def __init__(self):
        self._locations = {}

    def _get_or_create_location(self, placa: str):
        if placa not in self._locations:
            self._locations[placa] = {
                "lat": random.uniform(-23.5, -23.6),
                "lon": random.uniform(-46.6, -46.7)
            }
        return self._locations[placa]

    def fetch_coords(self, placa_veiculo: str) -> dict:
        print("-> [API Externa] Buscando coordenadas...")
        return self._get_or_create_location(placa_veiculo)

    def update_coords(self, placa_veiculo: str):
        print("-> [API Externa] Veículo se moveu. Atualizando coordenadas...")
        location = self._get_or_create_location(placa_veiculo)
        location['lat'] += random.uniform(-0.01, 0.01)
        location['lon'] += random.uniform(-0.01, 0.01)

class GpsAdapter: # Adapter
    def __init__(self, gps_service: ExternalGpsService, placa: str):
        self._adaptee = gps_service
        self._placa = placa
 
    @property 
    def localizacao(self) -> str:
        print("-> [Adapter] Chamando API externa e formatando o resultado...")
        coords = self._adaptee.fetch_coords(self._placa)
        return f"Lat: {coords['lat']:.6f}, Lon: {coords['lon']:.6f} (Via API Externa)"

    def simular_movimentacao(self):
        print("-> [Adapter] Repassando simulação de movimento para a API externa...")
        self._adaptee.update_coords(self._placa)

class Veiculo:
    def __init__(self, modelo='', placa='', ano='', valor=0.0):
        self._modelo = modelo
        self._placa = placa
        self._ano = ano
        self._valor = valor
        self._disponivel = True
        self._manutencao = []
        gps_service = ExternalGpsService()
        self._gps_tracker = GpsAdapter(gps_service, self.placa) # Adapter

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
        return self._gps_tracker.localizacao # Adapter

    def simular_movimentacao(self):
        self._gps_tracker.simular_movimentacao()

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

class VeiculoBuilder: # Build
    def __init__(self):
        self._veiculo = Veiculo()
    
    def com_modelo(self, modelo):
        self._veiculo._modelo = modelo
        return self
    
    def com_placa(self, placa):
        self._veiculo._placa = placa
        return self
    
    def com_ano(self, ano):
        self._veiculo._ano = ano
        return self
    
    def com_valor(self, valor):
        self._veiculo._valor = valor
        return self
    
    def build(self):
        return self._veiculo

class GerenciarVeiculo(Singleton):
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self.veiculos = []
        self._initialized = True

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

        # Build
        novo = (VeiculoBuilder()
                .com_modelo(modelo)
                .com_placa(placa)
                .com_ano(ano)
                .com_valor(valor)
                .build())
        self.veiculos.append(novo)
        print("Veículo cadastrado com sucesso! \n")

    def listar_veiculos(self):
        print("\n=== VEÍCULOS DISPONÍVEIS ===")
        disponiveis = [v for v in self.veiculos if v.disponivel]
        if not disponiveis:
            print("Nenhum veículo disponível no momento.")
            return
        for i, v in enumerate(disponiveis, start=1):
            print(f"{i} - Modelo: {v.modelo} | Placa: {v.placa} | Ano: {v.ano} | R${v.valor:.2f}/dia")

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