from .pwf import LeitorPWF
from .opcoes import opcoespwf, exportar_objetos_para_xlsx
from pathlib import Path 


def pwfconfiguracao(nome_sistema_pwf):
    """Carregamento do diretório, extração dos comendos
    de linha e ajuste de opções de simulação de fluxo de potência
    estático.
    
    Args
        rede
    """
    nome_pasta_saida_dfs = "output"
    path_pwf = Path(__file__).resolve().parent.parent / "pwfs" / nome_sistema_pwf
    
    
    dados_rede_PWF = LeitorPWF(path_pwf).carregar()
    opcoespwf(dados_rede_PWF)
    exportar_objetos_para_xlsx(dados_rede_PWF, nome_pasta_saida_dfs)
    