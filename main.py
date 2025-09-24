import os
from datetime import datetime
from clientes import GerenciarCliente, Cliente, Admin
from veiculos import GerenciarVeiculo, Veiculo
from reserva import Gerenciar_Reserva, Reserva

ger_cli = GerenciarCliente()
ger_vei = GerenciarVeiculo()
ger_res = Gerenciar_Reserva()

if not any(v.placa == 'OBJ9821' for v in ger_vei.veiculos):
    v_base = Veiculo(modelo='Gol', placa='OBJ9821', ano='2021', valor=176.50)
    ger_vei.veiculos.append(v_base)

ADMIN_USER = "admin"
ADMIN_PASS = "admin"

def login():
    """Login simplificado: admin ou cliente"""
    while True:
        os.system('cls')
        print("\n=== BEM-VINDO AO AV RENTAL CAR ===")
        print("1 - Login")
        print("2 - Cadastre-se")
        print("0 - Sair")
        escolha = input("Escolha uma opção: ").strip()

        if escolha == '1':
            entrada = input("Digite seu CPF: ").strip().lower()

            if entrada == 'admin':
                senha = input("Digite a senha do administrador: ").strip()
                if senha == ADMIN_PASS:
                    admin = Admin(nome='Administrador', cpf='00000000000')
                    print("Login de admin bem-sucedido!")
                    input("Pressione Enter para continuar...")
                    return 'admin', None
                else:
                    print("Senha incorreta!")
                    input()
                    continue

            elif entrada.isdigit() and len(entrada) == 11:
                cliente = next((c for c in ger_cli.clientes if c.cpf == entrada), None)
                if cliente:
                    print(f"Bem-vindo, {cliente.nome}!")
                    input("Pressione Enter para continuar...")
                    return 'cliente', cliente
                else:
                    print("CPF não cadastrado. Deseja se cadastrar? (s/n)")
                    resp = input().strip().lower()
                    if resp == 's':
                        ger_cli.cadastrar_cliente()
                        novo_cliente = ger_cli.clientes[-1]
                        print(f"Cadastro realizado! Bem-vindo, {novo_cliente.nome}!")
                        input("Pressione Enter para continuar...")
                        return 'cliente', novo_cliente
                    else:
                        print("Voltando à tela de login...")
                        input()
                        continue
            else:
                print("Entrada inválida! Digite um CPF válido (11 dígitos).")
                input()

        elif escolha == '2':
            ger_cli.cadastrar_cliente()
            novo_cliente = ger_cli.clientes[-1]
            print(f"Cadastro realizado! Bem-vindo, {novo_cliente.nome}!")
            input("Pressione Enter para continuar...")
            return 'cliente', novo_cliente

        elif escolha == '0':
            print("Saindo do sistema...")
            exit()
        else:
            print("Opção inválida!")
            input()


def menu():
    while True:
        tipo_usuario, cliente_logado = login()

        while True:
            os.system('cls')
            print("\n" + "="*50)
            print("                 AV RENTAL CAR")
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
10 - Sair
                """)
            else:
                print("""
1  - Reservar veículo
2  - Exibir contrato de locação
3  - Efetuar pagamento
4  - Relatar incidente
5  - Devolver veículo
6  - Histórico de reservas
7  - Sair
                """)

            opcao = input("Escolha uma opção: ").strip()

            # ===== ADMIN =====
            if tipo_usuario == 'admin':
                if opcao == '1':
                    ger_cli.cadastrar_cliente()
                    
                elif opcao == '2':
                    ger_vei.cadastrar_veiculo()
                    
                elif opcao == '3':
                    ger_vei.listar_veiculos()
                    
                elif opcao == '4':
                    cpf = input("Digite o CPF para exibir contrato(s): ").strip()
                    cliente = next((c for c in ger_cli.clientes if c.cpf == cpf), None)
                    if cliente:
                        contratos = [r for r in ger_res.reservas if r.cpf == cpf]
                        if contratos:
                            for r in contratos:
                                r.exibir_contrato(cliente)
                                print("="*50)
                        else:
                            print("Nenhuma reserva encontrada.")
                    else:
                        print("Cliente não encontrado.")
                        
                elif opcao == '5':
                    placa = input("Digite a placa do veículo: ").strip().upper()
                    veic = next((v for v in ger_vei.veiculos if v.placa == placa), None)
                    if veic:
                        veic.registrar_manutencao()
                    else:
                        print("Veículo não encontrado.")
                        
                elif opcao == '6':
                    placa = input("Digite a placa do veículo para listar os incidentes: ").strip().upper()
                    ger_res.listar_incidentes_por_placa(placa)
                        
                elif opcao == '7':
                    placa = input("Digite a placa do veículo para listar suas manutenções: ").strip().upper()
                    veic = next((v for v in ger_vei.veiculos if v.placa == placa), None)
                    if veic:
                        veic.listar_manutencoes()
                    else:
                        print("Veículo não encontrado.")        
                
                elif opcao == '8':
                    ger_cli.listar_clientes()
                    
                elif opcao == '9':
                    print("1 - Estatísticas da frota\n2 - Histórico de manutenções\n3 - Controle de pagamentos")
                    escolha_rel = input("Escolha: ").strip()
                    if escolha_rel == '1':
                        ger_vei.estatisticas_utilizacao()
                    elif escolha_rel == '2':
                        ger_vei.historico_manutencoes()
                    elif escolha_rel == '3':
                        ger_res.controle_pagamentos()
                    else:
                        print("Opção inválida.")
                        
                elif opcao == '10':
                    print("Saindo do sistema...")
                    break
                else:
                    print("Opção inválida.")
            else:
                # ===== CLIENTE =====
                if opcao == '1':
                    # Listar veículos disponíveis
                    veiculos_disp = [v for v in ger_vei.veiculos if getattr(v, 'disponivel', True)]
                    if not veiculos_disp:
                        print("Nenhum veículo disponível para reserva.")
                    else:
                        print("\n=== VEÍCULOS DISPONÍVEIS ===")
                        for idx, v in enumerate(veiculos_disp, 1):
                            print(f"{idx}. Modelo: {v.modelo} | Placa: {v.placa} | Ano: {v.ano} | Valor: R${v.valor:.2f}")
                        try:
                            escolha = int(input("Escolha o número do veículo: "))
                            if 1 <= escolha <= len(veiculos_disp):
                                veiculo_escolhido = veiculos_disp[escolha-1]
                                dias = int(input("Por quantos dias deseja alugar? "))
                                if dias > 0:
                                    ger_res.fazer_reserva(cliente_logado, veiculo_escolhido, dias)
                                else:
                                    print("Quantidade de dias deve ser maior que zero.")
                            else:
                                print("Opção inválida.")
                        except ValueError:
                            print("Entrada inválida.")
                            
                elif opcao == '2':
                    contratos = [r for r in ger_res.reservas if r.cpf == cliente_logado.cpf]
                    if contratos:
                        for r in contratos:
                            r.exibir_contrato(cliente_logado)
                            print("="*50)
                    else:
                        print("Nenhuma reserva encontrada.")
                        
                elif opcao == '3':
                    r_list = [r for r in ger_res.reservas if r.cpf == cliente_logado.cpf and not r.pago]
                    if not r_list:
                        print("Nenhuma reserva em aberto para pagamento.")
                    else:
                        print("\n=== SUAS RESERVAS EM ABERTO ===")
                        for idx, r in enumerate(r_list, 1):
                            print(f"{idx}. Veículo: {r.modelo} | Placa: {r.placa} | Dias: {r.dias} | Total: R${r.total:.2f} | Pagamento: {'Pago' if r.pago else 'Pendente'}")
                        try:
                            escolha = int(input("Escolha o número da reserva para pagar: "))
                            if 1 <= escolha <= len(r_list):
                                r = r_list[escolha-1]
                                r.efetuar_pagamento()
                            else:
                                print("Opção inválida.")
                        except ValueError:
                            print("Entrada inválida.")
                            
                elif opcao == '4':
                    r_list = [r for r in ger_res.reservas if r.cpf == cliente_logado.cpf and not r.finalizada]

                    if not r_list:
                        print("Nenhuma reserva em andamento para relatar incidente.")
                    else:
                        print("\n=== SUAS RESERVAS EM ANDAMENTO ===")
                        for idx, r in enumerate(r_list, 1):
                            print(f"{idx}. Veículo: {r.modelo} | Placa: {r.placa} | Dias: {r.dias} | Pagamento: {'Pago' if r.pago else 'Pendente'}")

                        try:
                            escolha = int(input("Escolha o número da reserva para relatar incidente: "))
                            if 1 <= escolha <= len(r_list):
                                r = r_list[escolha-1]
                                while True:
                                    data = input("Data da manutenção (dd/mm/aaaa): ").strip()
                                    try:
                                        data_obj = datetime.strptime(data, "%d/%m/%Y")
                                        data_f = data_obj.strftime("%d/%m/%Y")
                                        break
                                    except ValueError:
                                        print("Data inválida! Use o formato correto dd/mm/aaaa.")
                                        
                                descricao = input("Descrição do incidente: ").strip()
                                ger_res.registrar_incidente(r.cpf, r.placa, data, descricao)
                            else:
                                print("Opção inválida.")
                        except ValueError:
                            print("Entrada inválida.")
                            
                elif opcao == '5':
                    r_list = [r for r in ger_res.reservas if r.cpf == cliente_logado.cpf and r.pago and not r.finalizada]
                    if not r_list:
                        print("Nenhuma reserva paga e em aberto para devolução.")
                    else:
                        print("\n=== SUAS RESERVAS PAGAS E EM ABERTO ===")
                        for idx, r in enumerate(r_list, 1):
                            print(f"{idx}. Veículo: {r.modelo} | Placa: {r.placa} | Dias: {r.dias}")
                        try:
                            escolha = int(input("Escolha o número da reserva para devolver: "))
                            if 1 <= escolha <= len(r_list):
                                r = r_list[escolha-1]
                                r.devolver_veiculo(ger_vei.veiculos, ger_res.reservas)
                            else:
                                print("Opção inválida.")
                        except ValueError:
                            print("Entrada inválida.")
                            
                elif opcao == '6':
                    print("\n=== HISTÓRICO DE RESERVAS ===")
                    historico = [r for r in ger_res.reservas if r.cpf == cliente_logado.cpf]
                    if not historico:
                        print("Nenhuma reserva encontrada para este CPF.\n")
                    else:
                        for idx, r in enumerate(historico, 1):
                            status = "Finalizada" if getattr(r, 'finalizada', False) or r.pago else "Em andamento"
                            print(f"\nReserva {idx} - Status: {status}")
                            print(f"Veículo: {r.modelo} | Placa: {r.placa} | Dias: {r.dias} | Total: R${r.total:.2f}")
                            print(f"Pagamento: {'Pago' if r.pago else 'Pendente'}")
                            if hasattr(r, 'avaliacao') and r.avaliacao:
                                print(f"Avaliação: {r.avaliacao}")
                                if hasattr(r, 'comentario') and r.comentario:
                                    print(f"Comentário: {r.comentario}")
                            if hasattr(r, 'incidentes') and r.incidentes:
                                print("Incidentes:")
                                for inc in r.incidentes:
                                    print(f"- Data: {inc['data']} | Descrição: {inc['descricao']}")
                            if status == "Finalizada":
                                print("(Contrato disponível na opção de contrato)")
                            print("=" * 50)
                            
                elif opcao == '7':
                    print("Saindo do sistema...")
                    break
                else:
                    print("Opção inválida.")
            input("\nPressione Enter para continuar...")


if __name__ == "__main__":
    menu()
