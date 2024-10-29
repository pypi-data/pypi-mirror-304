import requests
from enum import Enum

class IntegracaoStatus(Enum):
    IMPORTANDO = 4
    LIGADO = 2
    DESLIGADO = 3
    ERRO = 1
    SEM_ARQUIVOS = 8

class EnumProcesso(Enum):
    INTEGRACAO = 0


def putRequestFunction(status: IntegracaoStatus, enumProcesso: EnumProcesso, enumBanco: int):
    """
    Envia duas requisições HTTP PUT para atualizar o status de um processo e registrar o horário da atualização.

    Parâmetros:
    ----------
    status : IntegracaoStatus
        Um valor da enumeração `IntegracaoStatus` que representa o status do processo a ser atualizado.
    enumProcesso : int
        Um número inteiro que representa o ID do processo a ser atualizado.
    enumBanco : int
        Um número inteiro que representa o ID do banco a ser atualizado.
    """
    horaFeita = f'http://172.16.10.6:8443/acompanhamentoTotal/horaFeita/{enumProcesso}/{enumBanco}'
    URLnovaApi = f'http://172.16.10.6:8443/acompanhamentoTotal/processoAndBancoStatus/{enumProcesso}/{enumBanco}'

    data = { "status": status.value }
    headers = { "Content-Type": "application/json" }
    
    response = requests.put(URLnovaApi, headers=headers, json=data)
    requests.put(horaFeita)

    if response.status_code == 200:
        print("Requisição PUT bem-sucedida!")
        print("Resposta:", response.json())
    else:
        print(f"Falha na requisição PUT. Código de status: {response.status_code}")
        print("Resposta:", response.text)
