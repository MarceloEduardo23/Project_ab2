from datetime import datetime

class Veiculo:
    def __init__(self, modelo='', placa='', ano='', valor=0.0):
        self._modelo = modelo
        self._placa = placa
        self._ano = ano
        self._valor = valor
        self._disponivel = True
        self._manutencao = []
        
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
            print(f"{i}. Data: {m['data']} | Desc: {m['descricao']} | Custo: R${m['custo']}")


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
                if len(ano) == 4 and ano.isdigit() and 1960 < int(ano) < 2030:
                    break
                else:
                    print("O ano deve ser válido! (1951 - 2029)")
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
        print("=== Veículos disponíveis ===")
        for i, v in enumerate(self.veiculos, start=1):
            if v.disponivel:
                print(f"{i} - Modelo: {v.modelo} | Ano: {v.ano} | R${v.valor}/dia")
                
    def estatisticas_utilizacao(self):
        total = len(self.veiculos)
        disponiveis = sum(1 for v in self.veiculos if v.disponivel)
        alugados = total - disponiveis
        print(f"\nTotal de veículos: {total}")
        print(f"Disponíveis: {disponiveis}")
        print(f"Alugados: {alugados}\n")
    
    def historico_manutencoes(self):
        print("\n=== Histórico de Manutenções ===\n")
        for v in self.veiculos:
            if v.manutencao:
                print(f"Veículo: {v.modelo} ({v.placa})")
                for m in v.manutencao:
                    print(f"- Data: {m['data']} | Descrição: {m['descricao']} | Custo: R${m['custo']:.2f}")
                print()


