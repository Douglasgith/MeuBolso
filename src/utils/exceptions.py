from fastapi import HTTPException, status

class AppException(HTTPException):
    #classe base craida para tratar exceções
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

    
class RegistroNaoEncontradoException(AppException):
    #Exceção para quando um registro não é encontrado no banco de dados
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro não encontrado"
            )

class ErroNoBancoDeDadosException(AppException):
    #Exceção para quando ocorre um erro no banco de dados
    def __init__(self, detail: str = "Erro no banco de dados"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro no banco de dados"
            )
class ErroNaBuscaPorMesException(AppException):
    #Exceção para quando ocorre um erro na busca por mês
    def __init__(self, detail: str = "Erro na busca por mês"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro na busca por mês"
            )