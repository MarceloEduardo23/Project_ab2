# comandos.py

from abc import ABC, abstractmethod
from datetime import datetime
from exceptions import AppError, ReservaNaoPagaError, VeiculoIndisponivelError, CpfJaCadastradoError

# Padrão Composite:
class IRelatorioComponent(ABC):
    @abstractmethod
    def execute(self):
        pass
    @abstractmethod
    def get_titulo(self) -> str:
        pass    

# =============================================================================
# --- Interface do Comando ---
# =============================================================================
class ICommand(ABC):
    @abstractmethod
    def execute(self):
        pass

# =============================================================================
# --- Comandos do Administrador ---
# =============================================================================

# Padrão Composite:
class RelatorioLeaf(IRelatorioComponent, ICommand):
    def __init__(self, titulo: str, receiver_func):
        self._titulo = titulo
        self._receiver_func = receiver_func

    def execute(self):
        self._receiver_func()

    def get_titulo(self) -> str:
        return self._titulo
    
class RelatorioComposite(IRelatorioComponent):
    def __init__(self, titulo: str):
        self._titulo = titulo
        self._filhos = []

    def add(self, componente: IRelatorioComponent):
        self._filhos.append(componente)

    def get_titulo(self) -> str:
        return self._titulo

    def execute(self):
        while True:
            print(f"\n--- Menu de Relatórios: {self._titulo} ---")
            for i, rel in enumerate(self._filhos, 1):
                print(f"{i} - {rel.get_titulo()}")
            print("0 - Voltar")
            escolha = input("Escolha: ").strip()

            if escolha == '0':
                break
            try:
                idx = int(escolha) - 1
                if 0 <= idx < len(self._filhos):
                    self._filhos[idx].execute() 
                else:
                    print("Opção inválida.")
            except ValueError:
                print("Entrada inválida.")

#####

class CadastrarClienteCommand(ICommand):
    def __init__(self, ger_cli):
        self._ger_cli = ger_cli
    def execute(self):
        try:
            self._ger_cli.cadastrar_cliente()
        except CpfJaCadastradoError as e:
            print(f"\n[ERRO NO CADASTRO]: {e}")

class CadastrarVeiculoCommand(ICommand):
    def __init__(self, ger_vei):
        self._ger_vei = ger_vei
    def execute(self):
        self._ger_vei.cadastrar_veiculo()

class ListarVeiculosCommand(ICommand):
    def __init__(self, ger_vei):
        self._ger_vei = ger_vei
    def execute(self):
        self._ger_vei.listar_veiculos()

class AdminExibirContratoCommand(ICommand):
    def __init__(self, ger_res, ger_cli):
        self._ger_res = ger_res
        self._ger_cli = ger_cli
    def execute(self):
        cpf = input("Digite o CPF do cliente para exibir contrato(s): ").strip()
        contratos = [r for r in self._ger_res.reservas if r.cpf == cpf]
        cliente = next((c for c in self._ger_cli.clientes if c.cpf == cpf), None)
        if cliente and contratos:
            for r in contratos:
                r.exibir_contrato(cliente)
        else:
            print("Nenhum contrato encontrado para este CPF.")

class RegistrarManutencaoCommand(ICommand):
    def __init__(self, ger_vei):
        self._ger_vei = ger_vei
    def execute(self):
        placa = input("Digite a placa do veículo: ").strip().upper()
        veic = next((v for v in self._ger_vei.veiculos if v.placa == placa), None)
        if veic:
            veic.registrar_manutencao()
        else:
            print("Veículo não encontrado.")

class ListarIncidentesCommand(ICommand):
    def __init__(self, ger_res):
        self._ger_res = ger_res
    def execute(self):
        placa = input("Digite a placa para listar incidentes: ").strip().upper()
        self._ger_res.listar_incidentes_por_placa(placa)

class ListarManutencoesCommand(ICommand):
    def __init__(self, ger_vei):
        self._ger_vei = ger_vei
    def execute(self):
        placa = input("Digite a placa para listar manutenções: ").strip().upper()
        veic = next((v for v in self._ger_vei.veiculos if v.placa == placa), None)
        if veic:
            veic.listar_manutencoes()
        else:
            print("Veículo não encontrado.")

class ListarClientesCommand(ICommand):
    def __init__(self, ger_cli):
        self._ger_cli = ger_cli
    def execute(self):
        self._ger_cli.listar_clientes()

class RelatoriosGerenciaisCommand(ICommand):
    def __init__(self, ger_vei, ger_res):
        self._menu_relatorios = RelatorioComposite("Relatórios Gerenciais")
        grupo_frota = RelatorioComposite("Relatórios de Frota")
        grupo_frota.add(RelatorioLeaf("Estatísticas da frota", ger_vei.estatisticas_utilizacao))
        grupo_frota.add(RelatorioLeaf("Histórico geral de manutenções", ger_vei.historico_manutencoes))
        rel_pagamentos = RelatorioLeaf("Controle de pagamentos", ger_res.controle_pagamentos)
        self._menu_relatorios.add(grupo_frota)
        self._menu_relatorios.add(rel_pagamentos)
        
    def execute(self):
        self._menu_relatorios.execute()

class GerenciarOfertasCommand(ICommand):
    def __init__(self, gerenciar_ofertas_func):
        self._gerenciar_ofertas_func = gerenciar_ofertas_func
    def execute(self):
        self._gerenciar_ofertas_func()

class RastrearVeiculoCommand(ICommand):
    def __init__(self, ger_vei):
        self._ger_vei = ger_vei
    def execute(self):
        placa = input("Digite a placa do veículo para rastrear: ").strip().upper()
        veic = next((v for v in self._ger_vei.veiculos if v.placa == placa), None)
        if veic:
            veic.simular_movimentacao()
            print(f"Localização atual do {veic.modelo} ({veic.placa}): {veic.localizacao}")
            print("(Nota: Esta é uma simulação.)")
        else:
            print("Veículo não encontrado.")

# =============================================================================
# --- Comandos do Cliente ---
# =============================================================================

class ReservarVeiculoCommand(ICommand):
    def __init__(self, ger_res, ger_vei, usuario):
        self._ger_res, self._ger_vei, self._usuario = ger_res, ger_vei, usuario
    def execute(self):
        self._ger_vei.listar_veiculos()
        veiculos_disp = [v for v in self._ger_vei.veiculos if v.disponivel]
        if not veiculos_disp: return
        try:
            escolha = int(input("Escolha o número do veículo: "))
            if 1 <= escolha <= len(veiculos_disp):
                veiculo = veiculos_disp[escolha-1]
                dias = int(input("Por quantos dias deseja alugar? "))
                if dias > 0: self._ger_res.fazer_reserva(self._usuario, veiculo, dias)
                else: print("Quantidade de dias deve ser maior que zero.")
            else: print("Opção inválida.")
        except (ValueError, IndexError): print("Entrada inválida.")

class ExibirContratoCommand(ICommand):
    def __init__(self, ger_res, usuario):
        self._ger_res, self._usuario = ger_res, usuario
    def execute(self):
        contratos = [r for r in self._ger_res.reservas if r.cpf == self._usuario.cpf]
        if contratos:
            for r in contratos: r.exibir_contrato(self._usuario)
        else: print("Nenhuma reserva encontrada.")

class EfetuarPagamentoCommand(ICommand):
    def __init__(self, ger_res, usuario):
        self._ger_res, self._usuario = ger_res, usuario
    def execute(self):
        r_list = [r for r in self._ger_res.reservas if r.cpf == self._usuario.cpf and not r.pago]
        if not r_list: print("Nenhuma reserva em aberto para pagamento."); return
        print("\n=== SUAS RESERVAS EM ABERTO ===")
        for idx, r in enumerate(r_list, 1):
            print(f"{idx}. Veículo: {r.modelo} | Placa: {r.placa} | Dias: {r.dias} | Total: R${r.total + r.VALOR_CAUCAO:.2f}")
        try:
            escolha = int(input("Escolha o número da reserva para pagar: "))
            if 1 <= escolha <= len(r_list): r_list[escolha-1].efetuar_pagamento()
            else: print("Opção inválida.")
        except (ValueError, IndexError): print("Entrada inválida.")

class RelatarIncidenteCommand(ICommand):
    def __init__(self, ger_res, usuario):
        self._ger_res, self._usuario = ger_res, usuario
    def execute(self):
        r_list = [r for r in self._ger_res.reservas if r.cpf == self._usuario.cpf and not r.finalizada]
        if not r_list: print("Nenhuma reserva em andamento para relatar incidente."); return
        print("\n=== SUAS RESERVAS EM ANDAMENTO ===")
        for idx, r in enumerate(r_list, 1): print(f"{idx}. Veículo: {r.modelo} | Placa: {r.placa}")
        try:
            escolha = int(input("Escolha a reserva para relatar o incidente: "))
            if 1 <= escolha <= len(r_list):
                r = r_list[escolha - 1]
                data = datetime.now().strftime("%d/%m/%Y")
                descricao = input("Descrição do incidente: ").strip()
                r.adicionar_incidente(data, descricao)
            else: print("Opção inválida.")
        except (ValueError, IndexError): print("Entrada inválida.")

class DevolverVeiculoCommand(ICommand):
    def __init__(self, ger_res, ger_vei, usuario):
        self._ger_res, self._ger_vei, self._usuario = ger_res, ger_vei, usuario
    def execute(self):
        r_list = [r for r in self._ger_res.reservas if r.cpf == self._usuario.cpf and r.pago and not r.finalizada]
        if not r_list: print("Nenhuma reserva paga e ativa para devolução."); return
        print("\n=== SUAS RESERVAS ATIVAS PARA DEVOLUÇÃO ===")
        for idx, r in enumerate(r_list, 1): print(f"{idx}. Veículo: {r.modelo} | Placa: {r.placa}")
        try:
            escolha = int(input("Escolha o número da reserva para devolver: "))
            if 1 <= escolha <= len(r_list): r_list[escolha-1].devolver_veiculo(self._ger_vei.veiculos)
            else: print("Opção inválida.")
        except (ReservaNaoPagaError, VeiculoIndisponivelError) as e:
            print(f"\n[ERRO NA DEVOLUÇÃO]: {e}")
        except AppError as e:
            print(f"\n[ERRO]: {e}")
        except (ValueError, IndexError):
            print("Entrada inválida.")

class HistoricoReservasCommand(ICommand):
    def __init__(self, ger_res, usuario):
        self._ger_res, self._usuario = ger_res, usuario
    def execute(self):
        historico = [r for r in self._ger_res.reservas if r.cpf == self._usuario.cpf]
        if not historico: print("Nenhum histórico de reservas encontrado."); return
        print("\n=== SEU HISTÓRICO DE RESERVAS ===")
        for r in historico:
            status = "Finalizada" if r.finalizada else ("Paga" if r.pago else "Pendente")
            print(f"\nVeículo: {r.modelo} ({r.placa}) - Status: {status}")
            print(f"  Período: {r.dias} dias | Total (diárias): R${r.total:.2f}")
            if r.finalizada and r._avaliacao:
                print(f"  Sua Avaliação: Nota {r._avaliacao} - '{r._comentario}'")

class ModificarReservaCommand(ICommand):
    def __init__(self, ger_res, ger_vei, usuario):
        self._ger_res, self._ger_vei, self._usuario = ger_res, ger_vei, usuario
    def execute(self):
        r_list = [r for r in self._ger_res.reservas if r.cpf == self._usuario.cpf and not r.pago and not r.finalizada]
        if not r_list: print("Nenhuma reserva não paga disponível para modificação."); return
        print("\n=== SUAS RESERVAS NÃO PAGAS ===")
        for idx, r in enumerate(r_list, 1): print(f"{idx}. Veículo: {r.modelo} | Placa: {r.placa} | Dias: {r.dias}")
        try:
            escolha = int(input("Escolha o número da reserva para modificar: "))
            if 1 <= escolha <= len(r_list): self._ger_res.modificar_reserva(r_list[escolha-1], self._ger_vei.veiculos)
            else: print("Opção inválida.")
        except (ValueError, IndexError): print("Entrada inválida.")

class CancelarReservaCommand(ICommand):
    def __init__(self, ger_res, ger_vei, usuario):
        self._ger_res, self._ger_vei, self._usuario = ger_res, ger_vei, usuario
    def execute(self):
        r_list = [r for r in self._ger_res.reservas if r.cpf == self._usuario.cpf and not r.pago and not r.finalizada]
        if not r_list: print("Nenhuma reserva não paga disponível para cancelamento."); return
        print("\n=== SUAS RESERVAS NÃO PAGAS ===")
        for idx, r in enumerate(r_list, 1): print(f"{idx}. Veículo: {r.modelo} | Placa: {r.placa}")
        try:
            escolha = int(input("Escolha o número da reserva para cancelar: "))
            if 1 <= escolha <= len(r_list): self._ger_res.cancelar_reserva(r_list[escolha-1], self._ger_vei.veiculos)
            else: print("Opção inválida.")
        except (ValueError, IndexError): print("Entrada inválida.")