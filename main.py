import os
from datetime import datetime
from clientes import GerenciarCliente, ClienteFactory, AdminFactory
from veiculos import GerenciarVeiculo, Veiculo, VeiculoBuilder
from reserva import Gerenciar_Reserva, Reserva

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
            ger_cli.cadastrar_cliente()
            input("Pressione Enter para fazer o login...")

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
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n" + "="*50)
            print("              AV RENTAL CAR")
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

            if tipo_usuario == 'admin':
                if opcao == '1': ger_cli.cadastrar_cliente()
                elif opcao == '2': ger_vei.cadastrar_veiculo()
                elif opcao == '3': ger_vei.listar_veiculos()
                elif opcao == '4':
                    cpf = input("Digite o CPF do cliente para exibir contrato(s): ").strip()
                    contratos = [r for r in ger_res.reservas if r.cpf == cpf]
                    cliente = next((c for c in ger_cli.clientes if c.cpf == cpf), None)
                    if cliente and contratos:
                        for r in contratos: r.exibir_contrato(cliente)
                    else: print("Nenhum contrato encontrado para este CPF.")
                elif opcao == '5':
                    placa = input("Digite a placa do veículo: ").strip().upper()
                    veic = next((v for v in ger_vei.veiculos if v.placa == placa), None)
                    if veic: veic.registrar_manutencao()
                    else: print("Veículo não encontrado.")
                elif opcao == '6':
                    placa = input("Digite a placa para listar incidentes: ").strip().upper()
                    ger_res.listar_incidentes_por_placa(placa)
                elif opcao == '7':
                    placa = input("Digite a placa para listar manutenções: ").strip().upper()
                    veic = next((v for v in ger_vei.veiculos if v.placa == placa), None)
                    if veic: veic.listar_manutencoes()
                    else: print("Veículo não encontrado.")
                elif opcao == '8': ger_cli.listar_clientes()
                elif opcao == '9':
                    print("\n1 - Estatísticas da frota\n2 - Histórico geral de manutenções\n3 - Controle de pagamentos")
                    escolha_rel = input("Escolha: ").strip()
                    if escolha_rel == '1': ger_vei.estatisticas_utilizacao()
                    elif escolha_rel == '2': ger_vei.historico_manutencoes()
                    elif escolha_rel == '3': ger_res.controle_pagamentos()
                    else: print("Opção inválida.")
                elif opcao == '10': gerenciar_ofertas()
                elif opcao == '11':
                    placa = input("Digite a placa do veículo para rastrear: ").strip().upper()
                    veic = next((v for v in ger_vei.veiculos if v.placa == placa), None)
                    if veic:
                        veic.simular_movimentacao()
                        print(f"Localização atual do {veic.modelo} ({veic.placa}): {veic.localizacao}")
                        print("(Nota: Esta é uma simulação.)")
                    else: print("Veículo não encontrado.")
                elif opcao == '12': print("Fazendo logout..."); break
                else: print("Opção inválida.")
            
            else:
                if opcao == '1':
                    ger_vei.listar_veiculos()
                    veiculos_disp = [v for v in ger_vei.veiculos if v.disponivel]
                    if veiculos_disp:
                        try:
                            escolha = int(input("Escolha o número do veículo: "))
                            if 1 <= escolha <= len(veiculos_disp):
                                veiculo_escolhido = veiculos_disp[escolha-1]
                                dias = int(input("Por quantos dias deseja alugar? "))
                                if dias > 0: ger_res.fazer_reserva(usuario_logado, veiculo_escolhido, dias)
                                else: print("Quantidade de dias deve ser maior que zero.")
                            else: print("Opção inválida.")
                        except (ValueError, IndexError): print("Entrada inválida.")
                elif opcao == '2':
                    contratos = [r for r in ger_res.reservas if r.cpf == usuario_logado.cpf]
                    if contratos:
                        for r in contratos: r.exibir_contrato(usuario_logado)
                    else: print("Nenhuma reserva encontrada.")
                elif opcao == '3':
                    r_list = [r for r in ger_res.reservas if r.cpf == usuario_logado.cpf and not r.pago]
                    if not r_list: print("Nenhuma reserva em aberto para pagamento.")
                    else:
                        print("\n=== SUAS RESERVAS EM ABERTO ===")
                        for idx, r in enumerate(r_list, 1):
                            print(f"{idx}. Veículo: {r.modelo} | Placa: {r.placa} | Dias: {r.dias} | Total: R${r.total + Reserva.VALOR_CAUCAO:.2f}")
                        try:
                            escolha = int(input("Escolha o número da reserva para pagar: "))
                            if 1 <= escolha <= len(r_list): r_list[escolha-1].efetuar_pagamento()
                            else: print("Opção inválida.")
                        except (ValueError, IndexError): print("Entrada inválida.")
                elif opcao == '4':
                    r_list = [r for r in ger_res.reservas if r.cpf == usuario_logado.cpf and not r.finalizada]
                    if not r_list: print("Nenhuma reserva em andamento para relatar incidente.")
                    else:
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
                elif opcao == '5':
                    r_list = [r for r in ger_res.reservas if r.cpf == usuario_logado.cpf and r.pago and not r.finalizada]
                    if not r_list: print("Nenhuma reserva paga e ativa para devolução.")
                    else:
                        print("\n=== SUAS RESERVAS ATIVAS PARA DEVOLUÇÃO ===")
                        for idx, r in enumerate(r_list, 1): print(f"{idx}. Veículo: {r.modelo} | Placa: {r.placa}")
                        try:
                            escolha = int(input("Escolha o número da reserva para devolver: "))
                            if 1 <= escolha <= len(r_list): r_list[escolha-1].devolver_veiculo(ger_vei.veiculos)
                            else: print("Opção inválida.")
                        except (ValueError, IndexError): print("Entrada inválida.")
                elif opcao == '6':
                    historico = [r for r in ger_res.reservas if r.cpf == usuario_logado.cpf]
                    if not historico: print("Nenhum histórico de reservas encontrado.")
                    else:
                        print("\n=== SEU HISTÓRICO DE RESERVAS ===")
                        for r in historico:
                            status = "Finalizada" if r.finalizada else ("Paga" if r.pago else "Pendente")
                            print(f"\nVeículo: {r.modelo} ({r.placa}) - Status: {status}")
                            print(f"  Período: {r.dias} dias | Total (diárias): R${r.total:.2f}")
                            if r.finalizada and r._avaliacao:
                                print(f"  Sua Avaliação: Nota {r._avaliacao} - '{r._comentario}'")
                elif opcao == '7':
                    r_list = [r for r in ger_res.reservas if r.cpf == usuario_logado.cpf and not r.pago and not r.finalizada]
                    if not r_list: print("Nenhuma reserva não paga disponível para modificação.")
                    else:
                        print("\n=== SUAS RESERVAS NÃO PAGAS ===")
                        for idx, r in enumerate(r_list, 1): print(f"{idx}. Veículo: {r.modelo} | Placa: {r.placa} | Dias: {r.dias}")
                        try:
                            escolha = int(input("Escolha o número da reserva para modificar: "))
                            if 1 <= escolha <= len(r_list): ger_res.modificar_reserva(r_list[escolha-1], ger_vei.veiculos)
                            else: print("Opção inválida.")
                        except (ValueError, IndexError): print("Entrada inválida.")
                elif opcao == '8':
                    r_list = [r for r in ger_res.reservas if r.cpf == usuario_logado.cpf and not r.pago and not r.finalizada]
                    if not r_list: print("Nenhuma reserva não paga disponível para cancelamento.")
                    else:
                        print("\n=== SUAS RESERVAS NÃO PAGAS ===")
                        for idx, r in enumerate(r_list, 1): print(f"{idx}. Veículo: {r.modelo} | Placa: {r.placa}")
                        try:
                            escolha = int(input("Escolha o número da reserva para cancelar: "))
                            if 1 <= escolha <= len(r_list): ger_res.cancelar_reserva(r_list[escolha-1], ger_vei.veiculos)
                            else: print("Opção inválida.")
                        except (ValueError, IndexError): print("Entrada inválida.")
                elif opcao == '9': print("Fazendo logout..."); break
                else: print("Opção inválida.")
            
            input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    menu()