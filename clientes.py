import os
from abc import ABC, abstractmethod
import copy

class Singleton:
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instancia = super().__new__(cls)
            cls._instances[cls] = instancia
        return cls._instances[cls]

class Pessoa:
    def __init__(self, nome='', cpf=''):
        self._nome = nome
        self._cpf = cpf

    # Prototype
    def clone(self):
        return copy.deepcopy(self)

    @property
    def cpf(self):
        return self._cpf

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, novo_nome):
        if novo_nome.strip():
            self._nome = novo_nome
        else:
            print("Nome inválido")

class Cliente(Pessoa):
    def __init__(self, nome='', cpf=''):
        super().__init__(nome, cpf)
        self.permissoes = [
            'reservar_veiculo',
            'ver_historico',
            'avaliar_aluguel',
            'relatar_incidente',
            'devolver_veiculo'
        ]

    def __str__(self):
        return f"Cliente: {self.nome} | CPF: {self.cpf}"


class Admin(Pessoa):
    def __init__(self, nome='', cpf='', cargo='Administrador', nivel_acesso=1):
        super().__init__(nome, cpf)
        self.cargo = cargo
        self.nivel_acesso = nivel_acesso
        self.permissoes = [
            'cadastrar_cliente',
            'cadastrar_veiculo',
            'listar_veiculos',
            'reservar_veiculo',
            'efetuar_pagamento',
            'registrar_manutencao',
            'relatar_incidente',
            'devolver_veiculo',
            'relatorios_gerenciais'
        ]

    def __str__(self):
        return (f"Administrador: {self.nome} | CPF: {self.cpf} | "
                f"Cargo: {self.cargo} | Nível: {self.nivel_acesso}")

# Abs. Factory com prototype

class AbstractUsuarioFactory(ABC):
    @abstractmethod
    def criar_usuario(self, nome, cpf):
        pass

class ClienteFactory(AbstractUsuarioFactory):
    def __init__(self):
        self._prototype = Cliente()

    def criar_usuario(self, nome, cpf):
        novo_cliente = self._prototype.clone()
        novo_cliente._nome = nome
        novo_cliente._cpf = cpf
        return novo_cliente
    
class AdminFactory(AbstractUsuarioFactory):
    def __init__(self):
        self._prototype = Admin()

    def criar_usuario(self, nome, cpf):
        novo_admin = self._prototype.clone()
        novo_admin._nome = nome
        novo_admin._cpf = cpf
        return novo_admin
    

class GerenciarCliente(Singleton):
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self.clientes = []
        self._initialized = True

    def cadastrar_cliente(self):
        while True:
            nome = input("Nome: ")
            if not nome.replace(' ', '').isalpha():
                print("Nome inválido! Digite apenas letras e espaços.")
            else:
                break

        while True:
            cpf = input("CPF: ")
            if len(cpf) != 11 or not cpf.isdigit():
                print("CPF inválido! Deve conter 11 dígitos numéricos.")
            else:
                break

        if cpf in [c.cpf for c in self.clientes]:
            print("CPF já cadastrado! Por favor, utilize outro CPF.")
            return
        else:
            novo_cliente = ClienteFactory().criar_usuario(nome, cpf)
            self.clientes.append(novo_cliente)
            print("\nCliente cadastrado com sucesso! \n")

    def listar_clientes(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=== LISTA DE CLIENTES CADASTRADOS ===\n")
        if not self.clientes:
            print("Nenhum cliente cadastrado.\n")
            return

        for idx, c in enumerate(self.clientes, 1):
            print(f"{idx} - Nome: {c.nome} | CPF: {c.cpf}")