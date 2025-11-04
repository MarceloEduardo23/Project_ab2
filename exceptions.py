class AppError(Exception):
    """Classe base para todas as exceções personalizadas da aplicação."""
    pass

# --- Exceções de Clientes e Veículos ---

class CpfJaCadastradoError(AppError):
    """Lançada ao tentar cadastrar um CPF que já existe."""
    pass

class PlacaJaCadastradaError(AppError):
    """Lançada ao tentar cadastrar uma Placa que já existe."""
    pass

class VeiculoIndisponivelError(AppError):
    """Lançada ao tentar reservar um veículo que não está disponível."""
    pass

class VeiculoNaoEncontradoError(AppError):
    """Lançada ao tentar operar sobre um veículo que não está na lista."""
    pass

# --- Exceções de Reserva ---

class ReservaJaPagaError(AppError):
    """Lançada ao tentar modificar ou cancelar uma reserva que já foi paga."""
    pass

class ReservaNaoPagaError(AppError):
    """Lançada ao tentar devolver um veículo cuja reserva ainda não foi paga."""
    pass

class DadosInvalidosError(AppError):
    """Lançada quando dados essenciais para uma operação estão faltando."""
    pass