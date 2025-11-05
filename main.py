import os
from datetime import datetime
from clientes import GerenciarCliente, ClienteFactory, AdminFactory
from veiculos import GerenciarVeiculo, Veiculo, VeiculoBuilder
from reserva import Gerenciar_Reserva, Reserva
from comandos import *
from exceptions import CpfJaCadastradoError

# "Banco de dados" de Cupons de Desconto VIVE AQUI AGORA
PROMO_CODES = {
    "BEMVINDO15": ('perc', 0.15),
    "FERIAS50": ('fixo', 50.00)
}

ger_cli = GerenciarCliente()
ger_vei = GerenciarVeiculo()
ger_res = Gerenciar_Reserva()

# Dados iniciais para teste
if not any(v.placa == 'ABC1234' for v in ger_vei.veiculos):
    v_base1 = VeiculoBuilder().com_modelo('Fiat Mobi').com_placa('ABC1234').com_ano('2022').com_valor(95.50).build()
    v_base2 = VeiculoBuilder().com_modelo('Hyundai HB20').com_placa('DEF5678').com_ano('2023').com_valor(120.00).build()
    ger_vei.veiculos.extend([v_base1, v_base2])

if not any(c.cpf == '12345678900' for c in ger_cli.clientes):
    c_base = ClienteFactory().criar_usuario(nome='Arthur Alves', cpf='12345678900')
    ger_cli.clientes.append(c_base)

ADMIN_USER = "admin"
ADMIN_PASS = "admin"

def login():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=== BEM-VINDO AO AV RENTAL CAR ===")
        print("1 - Login")
        print("2 - Cadastre-se")
        print("0 - Sair")
        escolha = input("Escolha uma opção: ").strip()

        if escolha == '1':
            entrada = input("Digite seu CPF: ").strip().lower()

            if entrada == ADMIN_USER:
                senha = input("Digite a senha do administrador: ").strip()
                if senha == ADMIN_PASS:
                    admin = AdminFactory().criar_usuario(nome='Administrador', cpf='00000000000')
                    print("Login de admin bem-sucedido!")
                    input("Pressione Enter para continuar...")
                    return 'admin', admin
                else:
                    print("Senha incorreta!")
                    input("Pressione Enter para tentar novamente...")
                    continue

            elif entrada.isdigit() and len(entrada) == 11:
                cliente = next((c for c in ger_cli.clientes if c.cpf == entrada), None)
                if cliente:
                    print(f"Bem-vindo, {cliente.nome}!")
                    input("Pressione Enter para continuar...")
                    return 'cliente', cliente
                else:
                    print("CPF não cadastrado. Cadastre-se na tela inicial.")
                    input("Pressione Enter para voltar...")
            else:
                print("Entrada inválida! Digite um CPF válido (11 dígitos) ou 'admin'.")
                input("Pressione Enter para tentar novamente...")

        elif escolha == '2':
            try: 
                ger_cli.cadastrar_cliente()
                input("Pressione Enter para fazer login...")
            except CpfJaCadastradoError as e:
                print(f"\n[ERRO NO CADASTRO]: {e}")
                input("Pressione Enter para tentar novamente...")

        elif escolha == '0':
            print("Saindo do sistema...")
            exit()
        else:
            print("Opção inválida!")
            input("Pressione Enter para tentar novamente...")

def gerenciar_ofertas():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=== GERENCIADOR DE OFERTAS ESPECIAIS ===")
        if not PROMO_CODES:
            print("Nenhum cupom de desconto cadastrado.")
        else:
            print("Cupons ativos:")
            for codigo, (tipo, valor) in PROMO_CODES.items():
                if tipo == 'perc':
                    print(f"- {codigo}: {valor*100:.0f}% de desconto")
                else:
                    print(f"- {codigo}: R$ {valor:.2f} de desconto fixo")
        
        print("\n1 - Adicionar Novo Cupom")
        print("2 - Remover Cupom")
        print("0 - Voltar ao Menu Principal")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == '1':
            codigo = input("Digite o código do novo cupom (ex: PROMO20): ").upper()
            if codigo in PROMO_CODES:
                print("Este código já existe.")
            else:
                tipo = input("O desconto é percentual ('perc') ou fixo ('fixo')? ").lower()
                if tipo in ['perc', 'fixo']:
                    try:
                        valor_str = input("Digite o valor do desconto (ex: 0.2 para 20% ou 100 para R$100): ")
                        valor = float(valor_str)
                        PROMO_CODES[codigo] = (tipo, valor)
                        print("Cupom adicionado com sucesso!")
                    except ValueError:
                        print("Valor inválido.")
                else:
                    print("Tipo de desconto inválido. Use 'perc' ou 'fixo'.")
        elif opcao == '2':
            codigo = input("Digite o código do cupom a ser removido: ").upper()
            if codigo in PROMO_CODES:
                del PROMO_CODES[codigo]
                print("Cupom removido com sucesso!")
            else:
                print("Cupom não encontrado.")
        elif opcao == '0':
            break
        else:
            print("Opção inválida.")
        input("\nPressione Enter para continuar...")

def menu():
    while True:
        tipo_usuario, usuario_logado = login()

        # --- Dicionários de Comandos Completos ---
        admin_commands = {
            '1': CadastrarClienteCommand(ger_cli),
            '2': CadastrarVeiculoCommand(ger_vei),
            '3': ListarVeiculosCommand(ger_vei),
            '4': AdminExibirContratoCommand(ger_res, ger_cli),
            '5': RegistrarManutencaoCommand(ger_vei),
            '6': ListarIncidentesCommand(ger_res),
            '7': ListarManutencoesCommand(ger_vei),
            '8': ListarClientesCommand(ger_cli),
            '9': RelatoriosGerenciaisCommand(ger_vei, ger_res),
            '10': GerenciarOfertasCommand(gerenciar_ofertas),
            '11': RastrearVeiculoCommand(ger_vei)
        }
        client_commands = {
            '1': ReservarVeiculoCommand(ger_res, ger_vei, usuario_logado),
            '2': ExibirContratoCommand(ger_res, usuario_logado),
            '3': EfetuarPagamentoCommand(ger_res, usuario_logado),
            '4': RelatarIncidenteCommand(ger_res, usuario_logado),
            '5': DevolverVeiculoCommand(ger_res, ger_vei, usuario_logado),
            '6': HistoricoReservasCommand(ger_res, usuario_logado),
            '7': ModificarReservaCommand(ger_res, ger_vei, usuario_logado),
            '8': CancelarReservaCommand(ger_res, ger_vei, usuario_logado)
        }
        
        commands_map = admin_commands if tipo_usuario == 'admin' else client_commands
        logout_option = '12' if tipo_usuario == 'admin' else '9'

        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n" + "="*50)
            print("               AV RENTAL CAR")
            print("="*50)

            if tipo_usuario == 'admin':
                print("""
1  - Cadastrar cliente
2  - Cadastrar veículo
3  - Ver veículos disponíveis
4  - Exibir contrato de locação
5  - Registrar manutenção
6  - Listar incidentes do veículo
7  - Listar manutenções do veículo
8  - Visualizar todos os clientes cadastrados
9  - Relatórios gerenciais
10 - Gerenciar Ofertas Especiais
11 - Rastrear veículo (Simulação GPS)
12 - Logout
                """)
            else:
                print("""
1 - Reservar veículo
2 - Exibir contrato de locação
3 - Efetuar pagamento
4 - Relatar incidente
5 - Devolver veículo
6 - Histórico de reservas
7 - Modificar reserva
8 - Cancelar reserva
9 - Logout
                """)

            opcao = input("Escolha uma opção: ").strip()

            if opcao == logout_option:
                print("Fazendo logout...")
                break

            command = commands_map.get(opcao)
            if command:
                command.execute()
            else:
                print("Opção inválida.")
            
            input("\nPressione Enter para continuar...")
if __name__ == "__main__":
    menu()