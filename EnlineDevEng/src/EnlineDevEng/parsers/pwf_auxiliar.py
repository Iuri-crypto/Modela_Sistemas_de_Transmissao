
from copy   import deepcopy
from numpy  import zeros
from pandas import DataFrame as DF
import      pandas as pd
import operator
import importlib.resources
import yaml
from typing import Dict, Any
import numpy as np

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .pwf_parser import DadosRedePWF


pd.set_option("future.no_silent_downcasting", True)

 


# def dbsh(rede: DadosRedePWF):
#     """Leitura dos dados de bancos de capacitores e/ou reatores individualizados conectados a barras CA ou linhas de 
#         transmissão.
        
#     Args
#         rede
#     """
#     rede.dbsh1["from"] = list()
#     rede.dbsh1["operacao"] = list()
#     rede.dbsh1["to"] = list()
#     rede.dbsh1["circuito"] = list()
#     rede.dbsh1["modo_controle"] = list()
#     rede.dbsh1["tensao_minima"] = list()
#     rede.dbsh1["tensao_maxima"] = list()
#     rede.dbsh1["barra_controlada"] = list()
#     rede.dbsh1["injecao_reativa_inicial"] = list()
#     rede.dbsh1["tipo_controle"] = list()
#     rede.dbsh1["apagar"] = list()
#     rede.dbsh1["extremidade"] = list()
#     rede.dbsh1["ndbsh2"] = list()
#     rede.dbsh2["grupo_banco"] = list()
#     rede.dbsh2["operacao"] = list()
#     rede.dbsh2["estado"] = list()
#     rede.dbsh2["unidades"] = list()
#     rede.dbsh2["unidades_operacao"] = list()
#     rede.dbsh2["capacitor_reator"] = list()
#     rede.dbsh2["manobravel"] = list()
#     idx = 0

#     while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
#         linha = rede.linhas[rede.idx_linha]
        
#         if linha[0] == rede.comentario:
#             pass 
        
#         elif rede.linhas[rede.idx_linha - 1][:] == rede.dbsh1["ruler"]:
#             rede.dbsh1["from"].append(linha[:5].strip())
#             rede.dbsh1["operacao"].append(linha[6].strip())
#             rede.dbsh1["to"].append(linha[8:13].strip())
#             rede.dbsh1["circuito"].append(linha[14:16].strip())
#             rede.dbsh1["modo_controle"].append(linha[17].strip())
#             rede.dbsh1["tensao_minima"].append(linha[19:23].strip())
#             rede.dbsh1["tensao_maxima"].append(linha[24:28].strip())
#             rede.dbsh1["barra_controlada"].append(linha[29:34].strip())
#             rede.dbsh1["injecao_reativa_inicial"].append(linha[35:41].strip())
#             rede.dbsh1["tipo_controle"].append(linha[42].strip())
#             rede.dbsh1["apagar"].append(linha[44].strip())
#             rede.dbsh1["extremidade"].append(linha[46:51].strip())
        
#         elif rede.linhas[rede.idx_linha - 1][:] == rede.dbsh2["ruler"]:
#             rede.dbsh1["ndbsh2"].append(linha[:5].strip())
#             linha = rede.linhas[rede.idx_linha]
            
#             while rede.linhas[rede.idx_linha].strip() != "FBAN":
#                 if linha[0] == rede.comentario:
#                     pass 
#                 else:
#                     rede.dbsh2["grupo_banco"].append(linha[:2].strip())
#                     rede.dbsh2["operacao"].append(linha[4].strip())
#                     rede.dbsh2["estado"].append(linha[6].strip())
#                     rede.dbsh2["unidades"].append(linha[8:11].strip())
#                     rede.dbsh2["unidades_operacao"].append(linha[12:15].strip())
#                     rede.dbsh2["capacitor_reator"].append(linha[16:22].strip())
#                     rede.dbsh2["manobravel"].append(linha[23].strip())
#                 rede.dbsh1["ndbsh2"][idx] += 1
#                 rede.idx_linha += 1
#             idx += 1
        
#         rede.idx_linha += 1
        
#     rede.dbsh1DF = DF(data=rede.dbsh1)
#     rede.dbsh1 = deepcopy(rede.dbsh1DF)
#     rede.dbsh1DF = rede.dbsh1DF.replace(r"^\s*$", "0", regex=True)
#     rede.dbsh1DF = rede.dbsh1DF.astype(
#         {
#             "from": "int",
#             "operacao": "object",
#             "to": "int",
#             "circuito": "int",
#             "modo_controle": "object",
#             "tensao_minima": "int",
#             "tensao_maxima": "int",
#             "barra_controlada": "int",
#             "injecao_reativa_inicial": "float",
#             "tipo_controle": "object",
#             "apagar": "object",
#             "extremidade": "int",
#         }
#     )

#     rede.dbsh2DF = DF(data=rede.dbsh2)
#     rede.dbsh2 = deepcopy(rede.dbsh2DF)
#     rede.dbsh2DF = rede.dbsh2DF.replace(r"^\s*$", "0", regex=True)
#     rede.dbsh2DF = rede.dbsh2DF.astype(
#         {
#             "grupo_banco": "int",
#             "operacao": "object",
#             "estado": "object",
#             "unidades": "int",
#             "unidades_operacao": "int",
#             "capacitor_reator": "float",
#             "manobravel": "object",
#         }
#     )
#     if rede.dbsh1DF.empty or rede.dbsh2DF.empty:
#         ## ERROR - VERMELHO
#         raise ValueError(
#             "\033[91mERROR: Falha na leitura de codigo de execucao `DBSH`!\033[0m"
#         )
#     else:
#         rede.codigos["DBSH"] = True

        

        
        
        
# def daga(rede: DadosRedePWF):
#     """Leitura dos dados de fatores de alteração do nível de geração ativa do sistema
    
#     Args
#         rede
#     """
#     rede.daga["tipo_do_elemento_1"] = list()
#     rede.daga["identificacao_do_elemento_1"] = list()
#     rede.daga["condicao_1"] = list()
#     rede.daga["tipo_do_elemento_2"] = list()
#     rede.daga["identificacao_do_elemento_2"] = list()
#     rede.daga["condicao_principal"] = list()
#     rede.daga["tipo_do_elemento_3"] = list()
#     rede.daga["identificacao_do_elemento_3"] = list()
#     rede.daga["condicao_2"] = list()
#     rede.daga["tipo_do_elemento_4"] = list()
#     rede.daga["identificacao_do_elemento_4"] = list()
#     rede.daga["fator_de_geracao_ativa"] = list()


#     while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
#         linha = rede.linhas[rede.idx_linha]
        
#         if linha[0] == rede.comentario:
#             pass 
        
#         else:
#             # Adicionando às listas (ou dicionário de dados)
#             rede.daga["tipo_elemento_1"].append(linha[0:4].strip())
#             rede.daga["identificacao_elemento_1"].append(linha[5:10].strip())
#             rede.daga["condicao_1"].append(linha[11].strip())

#             rede.daga["tipo_elemento_2"].append(linha[13:17].strip())
#             rede.daga["identificacao_elemento_2"].append(linha[18:23].strip())
#             rede.daga["condicao_principal"].append(linha[24].strip())

#             rede.daga["tipo_elemento_3"].append(linha[26:30].strip())
#             rede.daga["identificacao_elemento_3"].append(linha[31:36].strip())
#             rede.daga["condicao_2"].append(linha[37].strip())

#             rede.daga["tipo_elemento_4"].append(linha[39:43].strip())
#             rede.daga["identificacao_elemento_4"].append(linha[44:49].strip())

#             rede.daga["fator_de_geracao_ativa"].append(linha[50:56].strip())
            
        
#         rede.idx_linha += 1
        
#     # DataFrame dos Dados de Elo CC
#     rede.dagaDF = DF(data=rede.daga)
#     rede.daga = deepcopy(rede.dagaDF)
#     rede.dagaDF = rede.dagaDF.replace(r"^\s*$", "0", regex=True)
#     rede.dagaDF = rede.dagaDF.astype(
#         {
#         "tipo_elemento_1": "object",
#         "identificacao_elemento_1": "object",
#         "condicao_1": "object",

#         "tipo_elemento_2": "object",
#         "identificacao_elemento_2": "object",
#         "condicao_principal": "object",

#         "tipo_elemento_3": "object",
#         "identificacao_elemento_3": "object",
#         "condicao_2": "object",

#         "tipo_elemento_4": "object",
#         "identificacao_elemento_4": "object",

#         "fator_de_geracao_ativa": "object"
#         }
#     )

#     if rede.dagaDF.empty:
#         ## ERROR - VERMELHO
#         raise ValueError(
#             "\033[91mERROR: Falha na leitura de codigo de execucao `DAGA`!\033[0m"
#         )
#     else:
#         rede.codigos["DAGA"] = True
        
        
        
        

# def daeb(rede: DadosRedePWF):
#     """Leitura dos dados de alteração de estado operativo de Barra CA
    
#     Args
#         rede
#     """
#     rede.daeb["tipo_do_elemento_1"] = list()
#     rede.daeb["identificacao_do_elemento_1"] = list()
#     rede.daeb["condicao_1"] = list()
#     rede.daeb["tipo_do_elemento_2"] = list()
#     rede.daeb["identificacao_do_elemento_2"] = list()
#     rede.daeb["condicao_principal"] = list()
#     rede.daeb["tipo_do_elemento_3"] = list()
#     rede.daeb["identificacao_do_elemento_3"] = list()
#     rede.daeb["condicao_2"] = list()
#     rede.daeb["tipo_do_elemento_4"] = list()
#     rede.daeb["identificacao_do_elemento_4"] = list()
#     rede.daeb["estado_operativo_barra"] = list()
 
    
#     while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
#         linha = rede.linhas[rede.idx_linha]
        
#         if linha[0] == rede.comentario:
#             pass 
        
#         else:
#             # Adicionando às listas (ou dicionário de dados)
#             rede.daeb["tipo_elemento_1"].append(linha[0:4].strip())
#             rede.daeb["identificacao_elemento_1"].append(linha[5:10].strip())
#             rede.daeb["condicao_1"].append(linha[11:12].strip())

#             rede.daeb["tipo_elemento_2"].append(linha[13:17].strip())
#             rede.daeb["identificacao_elemento_2"].append(linha[18:23].strip())
#             rede.daeb["condicao_principal"].append(linha[24:25].strip())

#             rede.daeb["tipo_elemento_3"].append(linha[26:30].strip())
#             rede.daeb["identificacao_elemento_3"].append(linha[31:36].strip())
#             rede.daeb["condicao_2"].append(linha[37:38].strip())

#             rede.daeb["tipo_elemento_4"].append(linha[39:43].strip())
#             rede.daeb["identificacao_elemento_4"].append(linha[44:49].strip())

#             rede.daeb["estado_operativo_barra"].append(linha[50:51].strip())
            
        
#         rede.idx_linha += 1
        
#     # DataFrame dos Dados de Elo CC
#     rede.daebDF = DF(data=rede.daeb)
#     rede.daeb = deepcopy(rede.daebDF)
#     rede.daebDF = rede.daebDF.replace(r"^\s*$", "0", regex=True)
#     rede.daebDF = rede.daebDF.astype(
#         {
#         "tipo_elemento_1": "object",
#         "identificacao_elemento_1": "object",
#         "condicao_1": "object",

#         "tipo_elemento_2": "object",
#         "identificacao_elemento_2": "object",
#         "condicao_principal": "object",

#         "tipo_elemento_3": "object",
#         "identificacao_elemento_3": "object",
#         "condicao_2": "object",

#         "tipo_elemento_4": "object",
#         "identificacao_elemento_4": "object",

#         "estado_operativo_barra": "object"
#         }
#     )

#     if rede.daebDF.empty:
#         ## ERROR - VERMELHO
#         raise ValueError(
#             "\033[91mERROR: Falha na leitura de codigo de execucao `DAEB`!\033[0m"
#         )
#     else:
#         rede.codigos["DAEB"] = True
        
        
        

# def dagr(rede: DadosRedePWF):
#     """Leitura de dados de agregadores genéricos.
    
#     Args
#         rede:
    
#     Exemplo:
    
#         DAGR
#         (AG (         D E S C R I C A O        )
#         1 Estado                               
#         (ID O (       Nome de Identificacao      )
#         1   Acre                                                           
#         FAGR
#         99999
#     """
#     rede.dagr1["numero"]    = list()
#     rede.dagr1["descricao"] = list()
#     rede.dagr1["ndagr2"]    = list()
#     rede.dagr2["numero"]    = list()
#     rede.dagr2["operacao"]  = list()
#     rede.dagr2["descricao"] = list()
#     idx = 0
    
#     # percorre linhas
#     while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
#         if rede.linhas[rede.idx_linha][0] == rede.comentario:
#             pass 
        
#         elif rede.linhas[rede.idx_linha - 1][:] == rede.dagr1["ruler"]:
#             rede.dagr1["numero"].append(rede.linhas[rede.idx_linha][:3])
#             rede.dagr1["descricao"].append(rede.linhas[rede.idx_linha][4:40])
        
#         elif rede.linhas[rede.idx_linha - 1][:] == rede.dagr2["ruler"]:
#             rede.dagr1["ndagr2"].append(0)
            
#             # percorre colunas
#             while rede.linhas[rede.idx_linha].strip() != "FAGR":
#                 if rede.linhas[rede.idx_linha][0] == rede.comentario:
#                     pass 
                
#                 else:
#                     rede.dagr2["numero"].append(rede.linhas[rede.idx_linha][:3])
#                     rede.dagr2["operacao"].append(rede.linhas[rede.idx_linha][4])
#                     rede.dagr2["descricao"].append(rede.linhas[rede.idx_linha][6:42])
                
#                 rede.dagr1["ndagr2"][idx] += 1
#                 rede.idx_linha += 1
#             idx += 1
#         rede.idx_linha += 1
        
#     # Conversão dos dicionários para dataframes
#     rede.dagr1DF = DF(data=rede.dagr1)
#     rede.dagr1   = deepcopy(rede.dagr1DF)
#     rede.dagr1DF = rede.dagr1DF.replace(r"^\s*$", "0", regex=True)
#     rede.dagr1DF = rede.dagr1.astype({"numero": "int", "descricao": "str"})
    
#     rede.dagr2DF = DF(data=rede.dagr2)
#     rede.dagr2   = deepcopy(rede.dagr2DF)
#     rede.dagr2DF = rede.dagr2DF.replace(r"^\s*$", "0", regex=True)
#     rede.dagr2DF = rede.dagr2.astype({"numero": "int", "operacao": "str", "descricao": "str"})
    
#     if rede.dagr1DF.empty or rede.dagr2DF.empty:
#         ## ERROR - VERMELHO
#         raise ValueError ("\033[91mERROR: Falha na leitura de codigo de execucao 'DAGR'!\033[0m")
#     else:
#         rede.codigos["DAGR"] = True 
    


# def danc(rede: DadosRedePWF):
#     """Leitura de dados de alteração do nível de carregamento
    
#     Args
#         rede
        
#     Exemplo:
#         DANC
#         (Are ) ( Pk % ) ( Qk % ) ( Bsk % )       <-- rede.danc["ruler"] (Régua)
#             5      10.0      5.0       0.0       <-- Dados
#         99999
#     """
#     rede.danc["area"]                = list()
#     rede.danc["fator_carga_ativa"]   = list()
#     rede.danc["fator_carga_reativa"] = list()
#     rede.danc["fator_shunt_barra"]   = list()
    
#     while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
#         linha = rede.linhas[rede.idx_linha]
        
#         if linha[0] == rede.comentario:
#             pass 
        
#         else:
#             rede.danc["area"].append(linha[:5])
#             rede.danc["fator_carga_ativa"].append(linha[5:12])
#             rede.danc["fator_carga_reativa"].append(linha[12:19])
#             rede.danc["fator_shunt_barra"].append(linha[19:24])
        
#         rede.idx_linha += 1
        
#     # Dataframes dos Dados de Alteração do Nível de Carregamento
#     rede.dancDF = DF(data=rede.danc)
#     rede.danc   = deepcopy(rede.dancDF)
#     rede.dancDF = rede.dancDF.replace(r"^\s*$", "0", regex=True)
#     rede.dancDF = rede.dancDF.astype({"area"               : "int", 
#                                       "fator_carga_ativa"  : "float",
#                                       "fator_carga_reativa": "float",
#                                       "fator_shunt_barra"  : "float"})
    
#     if rede.dagr1DF.empty or rede.dagr2DF.empty:
#         ## ERROR - VERMELHO
#         raise ValueError ("\033[91mERROR: Falha na leitura de codigo de execucao 'DANC'!\033[0m")
#     else:
#         rede.codigos["DANC"] = True 
        
        

# def danc_acls(rede: DadosRedePWF):
#     """Leitura de dados de alteração do nível de carregamento.
    
#     Args
#         rede
        
#     Exemplo:
    
        
#     """
#     rede.danc["tipo_elemento_1"]          = list()
#     rede.danc["identificacao_elemento_1"] = list()
#     rede.danc["condicao_elemento_1"]      = list()
#     rede.danc["tipo_elemento_2"]          = list()
#     rede.danc["identificacao_elemento_2"] = list()
#     rede.danc["condicao_elemento_2"]      = list()
#     rede.danc["tipo_elemento_3"]          = list()
#     rede.danc["identificacao_elemento_3"] = list()
#     rede.danc["condicao_elemento_3"]      = list()
#     rede.danc["tipo_elemento_4"]          = list()
#     rede.danc["identificacao_elemento_4"] = list()
#     rede.danc["fator_carga_ativa"]        = list()
#     rede.danc["fator_carga_reativa"]      = list()
#     rede.danc["fator_shunt_barra"]        = list()
    
#     while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
#         linha = rede.linhas[rede.idx_linha]
            
#         if linha[0] == rede.fim_bloco:
#             pass 
        
#         else:
#             rede.danc["tipo_elemento_1"].append(linha[:4])
#             rede.danc["identificacao_elemento_1"].append(linha[5:10])
#             rede.danc["condicao_elemento_1"].append(linha[11])
#             rede.danc["tipo_elemento_2"].append(linha[13:17])
#             rede.danc["identificacao_elemento_2"].append(linha[18:23])
#             rede.danc["condicao_elemento_2"].append(linha[24])
#             rede.danc["tipo_elemento_3"].append(linha[26:30])
#             rede.danc["identificacao_elemento_3"].append(linha[31:36])
#             rede.danc["condicao_elemento_3"].append(linha[37])
#             rede.danc["tipo_elemento_4"].append(linha[39:43])
#             rede.danc["identificacao_elemento_4"].append(linha[44:49])
#             rede.danc["fator_carga_ativa"].append(linha[50:56])
#             rede.danc["fator_carga_reativa"].append(linha[57:63])
#             rede.danc["fator_shunt_barra"].append(linha[64:70])
        
#         rede.idx_linha += 1
        
#     # Dataframes dos Dados de Alteração do Nível de Carregamento
#     rede.dancDF = DF(data=rede.danc)
#     rede.danc   = deepcopy(rede.dancDF)
#     rede.dancDF = rede.dancDF.replace(r"^\s*$", "0", regex=True)
#     rede.dancDF = rede.dancDF.astype({"tipo_incremento_1"       : "int",
#                                     "identificacao_incremento_1": "int",
#                                     "condicao_incremento_1"     : "object",
#                                     "tipo_incremento_2"         : "int",
#                                     "identificacao_incremento_2": "int",
#                                     "condicao_incremento_2"     : "object",
#                                     "tipo_incremento_3"         : "int",
#                                     "identificacao_incremento_3": "int",
#                                     "condicao_incremento_3"     : "object",
#                                     "tipo_incremento_4"         : "int",
#                                     "identificacao_incremento_4": "int",
#                                     "fator_carga_ativa"         : "float",
#                                     "fator_carga_reativa"       : "float",
#                                     "fator_shunt_barra"         : "float"})
    
#     if rede.dagr1DF.empty or rede.dagr2DF.empty:
#         ## ERROR - VERMELHO
#         raise ValueError ("\033[91mERROR: Falha na leitura de codigo de execucao 'DANC'!\033[0m")
#     else:
#         rede.codigos["DANC"] = True 
            

# def dare(rede: DadosRedePWF):
#     """Leitura de dados de intercâmbio de potência ativa entre áreas

#     Args:
#         rede 
#     """
#     rede.dare["numero"] = list()
#     rede.dare["intercambio_liquido"] = list()
#     rede.dare["nome"] = list()
#     rede.dare["intercambio_minimo"] = list()
#     rede.dare["intercambio_maximo"] = list()
    
#     while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
#         linha = rede.linhas[rede.idx_linha]
        
#         if linha[0] == rede.comentario:
#             pass 
        
#         else:
#             rede.dare["numero"].append(linha[:3])
#             rede.dare["intercambio_liquido"].append(linha[7:13])
#             rede.dare["nome"].append(linha[18:54])
#             rede.dare["intercambio_minimo"].append(linha[55:61])
#             rede.dare["intercambio_maximo"].append(linha[62:68])
        
#         rede.idx_linha += 1
    
    
#     # Dataframes dos Dados de Intercâmbio de Potência Ativa entre areas
#     rede.dareDF = DF(data=rede.dare)
#     rede.dare   = deepcopy(rede.dareDF)
#     rede.dareDF = rede.dareDF.replace(r"^\s*$", "0", regex=True)
#     rede.dareDF = rede.dareDF.astype({"numero"                : "int", 
#                                         "intercambio_liquido" : "float",
#                                         "nome"                : "str",
#                                         "intercambio_minimo"  : "float",
#                                         "intercambio_maximo"  : "float"})
    
#     if rede.dareDF.empty:
#         ## ERROR - VERMELHO
#         raise ValueError ("\033[91mERROR: Falha na leitura de codigo de execucao 'DARE'!\033[0m")
#     else:
#         rede.codigos["DARE"] = True 
        
      
        
def dbar(rede: DadosRedePWF):
    """Leitura de dados de barra.
    
    Args
        rede
    """
    rede.dbar["numero"] = list()
    rede.dbar["operacao"] = list()
    rede.dbar["estado"] = list()
    rede.dbar["tipo"] = list()
    rede.dbar["grupo_de_base_de_tensao"] = list()
    rede.dbar["nome"] = list()
    rede.dbar["grupo_de_limite_de_tensao"] = list()
    rede.dbar["tensao"] = list()
    rede.dbar["angulo"] = list()
    rede.dbar["geracao_ativa"] = list()
    rede.dbar["geracao_reativa"] = list()
    rede.dbar["geracao_reativa_minima"] = list()
    rede.dbar["geracao_reativa_maxima"] = list()
    rede.dbar["barra_controlada"] = list()
    rede.dbar["carga_ativa"] = list()
    rede.dbar["carga_reativa"] = list()
    rede.dbar["capacitor_reator"] = list()
    rede.dbar["area"] = list()
    rede.dbar["tensao_para_definicao_de_carga"] = list()
    rede.dbar["modo_de_visualizacao"] = list()
    rede.dbar["agregador_1"] = list()
    rede.dbar["agregador_2"] = list()
    rede.dbar["agregador_3"] = list()
    rede.dbar["agregador_4"] = list()
    rede.dbar["agregador_5"] = list()
    rede.dbar["agregador_6"] = list()
    rede.dbar["agregador_7"] = list()
    rede.dbar["agregador_8"] = list()
    rede.dbar["agregador_9"] = list()
    rede.dbar["agregador_10"] = list()
    
    while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
        linha = rede.linhas[rede.idx_linha]
        
        if linha[0] == rede.comentario:
            pass 
        
        else:
            rede.dbar["numero"].append(linha[:5].strip())
            rede.dbar["operacao"].append(linha[5].strip())
            rede.dbar["estado"].append(linha[6].strip())
            rede.dbar["tipo"].append(linha[7].strip())
            rede.dbar["grupo_de_base_de_tensao"].append(linha[8:10].strip())
            rede.dbar["nome"].append(linha[10:22].split(" ")[0].strip())
            rede.dbar["grupo_de_limite_de_tensao"].append(linha[22:24].strip())
            rede.dbar["tensao"].append(linha[24:28].strip())
            rede.dbar["angulo"].append(linha[28:32].strip())
            rede.dbar["geracao_ativa"].append(linha[32:37].strip())
            rede.dbar["geracao_reativa"].append(linha[37:42].strip())
            rede.dbar["geracao_reativa_minima"].append(linha[42:47].strip())
            rede.dbar["geracao_reativa_maxima"].append(linha[47:52].strip())
            rede.dbar["barra_controlada"].append(linha[52:58].strip())
            rede.dbar["carga_ativa"].append(linha[58:63].strip())
            rede.dbar["carga_reativa"].append(linha[63:68].strip())
            rede.dbar["capacitor_reator"].append(linha[68:73].strip())
            rede.dbar["area"].append(linha[73:76].strip())
            rede.dbar["tensao_para_definicao_de_carga"].append(linha[76:80].strip())
            rede.dbar["modo_de_visualizacao"].append(linha[80].strip())
            rede.dbar["agregador_1"].append(linha[81:84].strip())
            rede.dbar["agregador_2"].append(linha[84:87].strip())
            rede.dbar["agregador_3"].append(linha[87:90].strip())
            rede.dbar["agregador_4"].append(linha[90:93].strip())
            rede.dbar["agregador_5"].append(linha[93:96].strip())
            rede.dbar["agregador_6"].append(linha[96:99].strip())
            rede.dbar["agregador_7"].append(linha[99:102].strip())
            rede.dbar["agregador_8"].append(linha[102:105].strip())
            rede.dbar["agregador_9"].append(linha[105:108].strip())
            rede.dbar["agregador_10"].append(linha[108:111].strip())
            
        rede.idx_linha += 1
        
    
    # DataFrame dos Dados de Barra
    rede.dbarDF = DF(data=rede.dbar)
    rede.dbar = deepcopy(rede.dbarDF)
    rede.dbarDF = rede.dbarDF.replace(r"^\s*$", np.nan, regex=True)
    rede.dbarDF = rede.dbarDF.astype(
        {
            "numero": "Int64",
            "operacao": "object",
            "estado": "object",
            "tipo": "Int64",
            "grupo_de_base_de_tensao": "object",
            "nome": "str",
            "grupo_de_limite_de_tensao": "object",
            "tensao": "float",
            "angulo": "float",
            "geracao_ativa": "float",
            "geracao_reativa": "float",
            "geracao_reativa_minima": "float",
            "geracao_reativa_maxima": "float",
            "barra_controlada": "object",
            "carga_ativa": "float",
            "carga_reativa": "float",
            "capacitor_reator": "float",
            "area": "Int64",
            "tensao_para_definicao_de_carga": "float",
            "modo_de_visualizacao": "Int64",
            "agregador_1": "object",
            "agregador_2": "object",
            "agregador_3": "object",
            "agregador_4": "object",
            "agregador_5": "object",
            "agregador_6": "object",
            "agregador_7": "object",
            "agregador_8": "object",
            "agregador_9": "object",
            "agregador_10": "object",
        }
    )
    if rede.dbarDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de codigo de execucao `DBAR`!\033[0m")
    else:
        rede.codigos["DBAR"] = True
        
        
        
        
# def dcar(rede: DadosRedePWF):
#     """Leitura de Args A, B, C e D que estabelecem a curva de variação de carga em relação
#     a magnitude de tensão nas barras
    
#     Args
#         rede
#     """
#     rede.dcar["tipo_elemento_1"] = list()
#     rede.dcar["identificacao_elemento_1"] = list()
#     rede.dcar["condicao_elemento_1"] = list()
#     rede.dcar["tipo_elemento_2"] = list()
#     rede.dcar["identificacao_elemento_2"] = list()
#     rede.dcar["condicao_elemento_2"] = list()
#     rede.dcar["tipo_elemento_3"] = list()
#     rede.dcar["identificacao_elemento_3"] = list()
#     rede.dcar["condicao_elemento_3"] = list()
#     rede.dcar["tipo_elemento_4"] = list()
#     rede.dcar["identificacao_elemento_4"] = list()
#     rede.dcar["operacao"] = list()
#     rede.dcar["parametro_A"] = list()
#     rede.dcar["parametro_B"] = list()
#     rede.dcar["parametro_C"] = list()
#     rede.dcar["parametro_D"] = list()
#     rede.dcar["tensao_limite"] = list()
    
#     while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
#         linha = rede.linhas[rede.idx_linha]
        
#         if linha[0] == rede.comentario:
#             pass 
        
#         else:
#             rede.dcar["tipo_elemento_1"].append(linha[:4])
#             rede.dcar["identificacao_elemento_1"].append(linha[5:10])
#             rede.dcar["condicao_elemento_1"].append(linha[11])
#             rede.dcar["tipo_elemento_2"].append(linha[13:17])
#             rede.dcar["identificacao_elemento_2"].append(linha[18:23])
#             rede.dcar["condicao_elemento_2"].append(linha[24])
#             rede.dcar["tipo_elemento_3"].append(linha[26:30])
#             rede.dcar["identificacao_elemento_3"].append(linha[31:36])
#             rede.dcar["condicao_elemento_3"].append(linha[37])
#             rede.dcar["tipo_elemento_4"].append(linha[39:43])
#             rede.dcar["identificacao_elemento_4"].append(linha[44:49])
#             rede.dcar["operacao"].append(linha[50])
#             rede.dcar["parametro_A"].append(linha[52:55])
#             rede.dcar["parametro_B"].append(linha[56:59])
#             rede.dcar["parametro_C"].append(linha[60:63])
#             rede.dcar["parametro_D"].append(linha[64:67])
#             rede.dcar["tensao_limite"].append(rede.cte["VFLD"] 
#                                               if linha[68:72] == 4 * " " 
#                                               else linha[68:72])
#         rede.idx_linha += 1
        
#     # DataFrame dos dados de Variacao do Tipo de Carga
#     rede.dcarDF = DF(data=rede.dcar)
#     rede.dcarDF = deepcopy(rede.dcarDF)
#     rede.dcarDF = rede.dcarDF.replace(r"^\s*$", "0", regex=True)
#     rede.dcarDF = rede.dcarDF.astype(
#         {
#             "tipo_elemento_1": "object",
#             "identificacao_elemento_1": "int",
#             "condicao_elemento_1": "object",
#             "tipo_elemento_2": "object",
#             "identificacao_elemento_2": "int",
#             "condicao_elemento_2": "object",
#             "tipo_elemento_3": "object",
#             "identificacao_elemento_3": "int",
#             "condicao_elemento_3": "object",
#             "tipo_elemento_4": "object",
#             "identificacao_elemento_4": "int",
#             "operacao": "object",
#             "parametro_A": "int",
#             "parametro_B": "int",
#             "parametro_C": "int",
#             "parametro_D": "int",
#             "tensao_limite": "float",
#         }
#     )
#     if rede.dcarDF.empty:
#         ## ERROR - VERMELHO
#         raise ValueError(
#             "\033[91mERROR: Falha na leitura de codigo de execucao `DCAR`!\033[0m")
#     else:
#         rede.codigos["DCAR"] = True
        
        
# def dcba(rede: DadosRedePWF):
#     """Leitura de dados de barra CC.
    
#     Args
#         rede
#     """
#     rede.dcba["numero"] = list()
#     rede.dcba["operacao"] = list()
#     rede.dcba["tipo"] = list()
#     rede.dcba["polaridade"] = list()
#     rede.dcba["nome"] = list()
#     rede.dcba["grupo_limite_tensao"] = list()
#     rede.dcba["tensao"] = list()
#     rede.dcba["eletrodo_terra"] = list()
#     rede.dcba["numero_elo_cc"] = list()
    
#     while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
#         linha = rede.linhas[rede.idx_linha]
        
#         if linha[0] == rede.comentario:
#             pass 
        
#         else:
#             rede.dcba["numero"].append(linha[:4])
#             rede.dcba["operacao"].append(linha[5])
#             rede.dcba["tipo"].append(linha[7])
#             rede.dcba["polaridade"].append(linha[8])
#             rede.dcba["nome"].append(linha[9:21])
#             rede.dcba["grupo_limite_tensao"].append(linha[21:23])
#             rede.dcba["tensao"].append(linha[23:28])
#             rede.dcba["eletrodo_terra"].append(linha[66:71])
#             rede.dcba["numero_elo_cc"].append(linha[71:75])
        
#         rede.idx_linha += 1
        
#     # DataFrame dos Dados de Barra CC
#     rede.dcbaDF = DF(data=rede.dcba)
#     rede.dcba = deepcopy(rede.dcbaDF)
#     rede.dcbaDF = rede.dcbaDF.replace(r"^\s*$", "0", regex=True)
#     rede.dcbaDF = rede.dcbaDF.astype(
#         {
#             "numero": "int",
#             "operacao": "object",
#             "tipo": "int",
#             "polaridade": "object",
#             "nome": "str",
#             "grupo_limite_tensao": "object",
#             "tensao": "float",
#             "eletrodo_terra": "object",
#             "numero_elo_cc": "int",
#         }
#     )
#     if rede.dcbaDF.empty:
#         ## ERROR - VERMELHO
#         raise ValueError(
#             "\033[91mERROR: Falha na leitura de codigo de execucao `DCBA`!\033[0m")
#     else:
#         rede.codigos["DCBA"] = True
        
        
# def dccv(rede: DadosRedePWF):
#     """Leitura de dados de controle de conversores CA/CC
    
#     Args
#         rede
#     """
#     rede.dccv["numero"] = list()
#     rede.dccv["operacao"] = list()
#     rede.dccv["folga"] = list()
#     rede.dccv["modo_controle_inversor"] = list()
#     rede.dccv["tipo_controle_conversor"] = list()
#     rede.dccv["valor_especificado"] = list()
#     rede.dccv["margem_corrente"] = list()
#     rede.dccv["maxima_sobrecorrente"] = list()
#     rede.dccv["angulo_conversor"] = list()
#     rede.dccv["angulo_conversor_minimo"] = list()
#     rede.dccv["angulo_conversor_maximo"] = list()
#     rede.dccv["tap_transformador_minimo"] = list()
#     rede.dccv["tap_transformador_maximo"] = list()
#     rede.dccv["tap_transformador_numero"] = list()
#     rede.dccv["tensao_cc_minima"] = list()
#     rede.dccv["tap_high"] = list()
#     rede.dccv["tap_reduzido"] = list()
    
#     while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
#         linha = rede.linhas[rede.idx_linha]
        
#         if linha[0] == rede.comentario:
#             pass 
        
#         else:
#             rede.dccv["numero"].append(linha[:4])
#             rede.dccv["operacao"].append(linha[5])
#             rede.dccv["folga"].append(linha[7])
#             rede.dccv["modo_controle_inversor"].append(linha[8])
#             rede.dccv["tipo_controle_conversor"].append(linha[9])
#             rede.dccv["valor_especificado"].append(linha[11:16])
#             rede.dccv["margem_corrente"].append(linha[17:22])
#             rede.dccv["maxima_sobrecorrente"].append(linha[23:28])
#             rede.dccv["angulo_conversor"].append(linha[29:34])
#             rede.dccv["angulo_conversor_minimo"].append(linha[35:40])
#             rede.dccv["angulo_conversor_maximo"].append(linha[41:46])
#             rede.dccv["tap_transformador_minimo"].append(linha[47:52])
#             rede.dccv["tap_transformador_maximo"].append(linha[53:58])
#             rede.dccv["tap_transformador_numero"].append(linha[59:61])
#             rede.dccv["tensao_cc_minima"].append(linha[62:66])
#             rede.dccv["tap_high"].append(linha[67:72])
#             rede.dccv["tap_reduzido"].append(linha[73:78])
        
#         rede.idx_linha += 1
        
#     # DataFrame dos Dados de Controle de Conversores de Tensao CC
#     rede.dccvDF = DF(data=rede.dccv)
#     rede.dccv = deepcopy(rede.dccvDF)
#     rede.dccvDF = rede.dccvDF.replace(r"^\s*$", "0", regex=True)
#     rede.dccvDF = rede.dccvDF.astype(
#         {
#             "numero": "int",
#             "operacao": "object",
#             "folga": "object",
#             "modo_controle_inversor": "object",
#             "tipo_controle_conversor": "object",
#             "valor_especificado": "float",
#             "margem_corrente": "float",
#             "maxima_sobrecorrente": "float",
#             "angulo_conversor": "float",
#             "angulo_conversor_minimo": "float",
#             "angulo_conversor_maximo": "float",
#             "tap_transformador_minimo": "float",
#             "tap_transformador_maximo": "float",
#             "tap_transformador_numero": "int",
#             "tensao_cc_minima": "float",
#             "tap_high": "object",
#             "tap_reduzido": "object",
#         }
#     )

#     if rede.dccvDF.empty:
#         ## ERROR - VERMELHO
#         raise ValueError(
#             "\033[91mERROR: Falha na leitura de codigo de execucao `DCCV`!\033[0m")
#     else:
#         rede.codigos["DCCV"] = True
        
        
# def dcer(rede: DadosRedePWF):
#     """Leitura de dados de compensadores estáticos de potência reativa.
    
#     Args
#         rede
#     """
#     rede.dcer["barra"] = list()
#     rede.dcer["operacao"] = list()
#     rede.dcer["grupo_base"] = list()
#     rede.dcer["unidades"] = list()
#     rede.dcer["barra_controlada"] = list()
#     rede.dcer["droop"] = list()
#     rede.dcer["potencia_reativa"] = list()
#     rede.dcer["potencia_reativa_minima"] = list()
#     rede.dcer["potencia_reativa_maxima"] = list()
#     rede.dcer["controle"] = list()
#     rede.dcer["estado"] = list()
#     rede.dcer["modo_correcao_limites"] = list()
    
#     while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
#         linha = rede.linhas[rede.idx_linha]
        
#         if linha[0] == rede.comentario:
#             pass 
        
#         else:
#             rede.dcer["barra"].append(linha[:5])
#             rede.dcer["operacao"].append(linha[6])
#             rede.dcer["grupo_base"].append(linha[8:10])
#             rede.dcer["unidades"].append(linha[11:13])
#             rede.dcer["barra_controlada"].append(linha[14:19])
#             rede.dcer["droop"].append(linha[20:26])
#             rede.dcer["potencia_reativa"].append(linha[27:32])
#             rede.dcer["potencia_reativa_minima"].append(linha[32:37])
#             rede.dcer["potencia_reativa_maxima"].append(linha[37:42])
#             rede.dcer["controle"].append(linha[43])
#             rede.dcer["estado"].append(linha[45])
#             rede.dcer["modo_correcao_limites"].append(linha[47])
            
#         rede.idx_linha += 1
        
#     # DataFrame dos Dados dos Compensadores Estaticos de Potencia Reativa
#     rede.dcerDF = DF(data=rede.dcer)
#     rede.dcer = deepcopy(rede.dcerDF)
#     rede.dcerDF = rede.dcerDF.replace(r"^\s*$", "0", regex=True)
#     rede.dcerDF = rede.dcerDF.astype(
#         {
#             "barra": "int",
#             "operacao": "object",
#             "grupo_base": "object",
#             "unidades": "int",
#             "barra_controlada": "int",
#             "droop": "float",
#             "potencia_reativa": "float",
#             "potencia_reativa_minima": "float",
#             "potencia_reativa_maxima": "float",
#             "controle": "object",
#             "estado": "object",
#         }
#     )
#     if rede.dcerDF.empty:
#         ## ERROR - VERMELHO
#         raise ValueError(
#             "\033[91mERROR: Falha na leitura de codigo e execucao `DCER`!\033[0m"
#         )
#     else:
#         rede.codigos["DCER"] = True
    
        

# def dcli(rede: DadosRedePWF):
#     """Leitura de dados de linhas de transmissão CC
    
#     Args
#         rede
#     """
#     rede.dcli["de"] = list()
#     rede.dcli["operacao"] = list()
#     rede.dcli["para"] = list()
#     rede.dcli["circuito"] = list()
#     rede.dcli["proprietario"] = list()
#     rede.dcli["resistencia"] = list()
#     rede.dcli["indutancia"] = list()
#     rede.dcli["capacidade"] = list()        
    
#     while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
#         linha = rede.linhas[rede.idx_linha]
        
#         if linha[0] == rede.comentario:
#             pass 
        
#         else:
#             rede.dcli["de"].append(linha[:4])
#             rede.dcli["operacao"].append(linha[5])
#             rede.dcli["para"].append(linha[8:12])
#             rede.dcli["circuito"].append(linha[12:14])
#             rede.dcli["proprietario"].append(linha[15])
#             rede.dcli["resistencia"].append(linha[17:23])
#             rede.dcli["indutancia"].append(linha[23:29])
#             rede.dcli["capacidade"].append(linha[60:64])
        
#         rede.idx_linha += 1
        
#     # DataFrame dos Dados de Linhas de Transmissao CC
#     rede.dcliDF = DF(data=rede.dcli)
#     rede.dcli = deepcopy(rede.dcliDF)
#     rede.dcliDF = rede.dcliDF.replace(r"^\s*$", "0", regex=True)
#     rede.dcliDF = rede.dcliDF.astype(
#         {
#             "de": "int",
#             "operacao": "object",
#             "para": "int",
#             "circuito": "int",
#             "proprietario": "object",
#             "resistencia": "float",
#             "indutancia": "float",
#             "capacidade": "float",
#         }
#     )

#     if rede.dcliDF.empty:
#         ## ERROR - VERMELHO
#         raise ValueError(
#             "\033[91mERROR: Falha na leitura de codigo de execucao `DCLI`!\033[0m"
#         )
#     else:
#         rede.codigos["DCLI"] = True
        
        
# def dcnv(rede: DadosRedePWF):
#     """Leitura de dados de conversores CA/CC
    
#     Args
#         rede
#     """
#     rede.dcnv["numero"] = list()
#     rede.dcnv["operacao"] = list()
#     rede.dcnv["barra_CA"] = list()
#     rede.dcnv["barra_CC"] = list()
#     rede.dcnv["barra_neutra"] = list()
#     rede.dcnv["modo_operacao"] = list()
#     rede.dcnv["pontes"] = list()
#     rede.dcnv["corrente"] = list()
#     rede.dcnv["reatancia_comutacao"] = list()
#     rede.dcnv["tensao_secundario"] = list()
#     rede.dcnv["potencia_transformador"] = list()
#     rede.dcnv["resistencia_reator"] = list()
#     rede.dcnv["indutancia_reator"] = list()
#     rede.dcnv["capacitancia"] = list()
#     rede.dcnv["frequencia"] = list()
    
#     while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
#         linha = rede.linhas[rede.idx_linha]
        
#         if linha[0] == rede.comentario:
#             pass 
        
#         else:
#             rede.dcnv["numero"].append(linha[:4])
#             rede.dcnv["operacao"].append(linha[5])
#             rede.dcnv["barra_CA"].append(linha[7:12])
#             rede.dcnv["barra_CC"].append(linha[13:17])
#             rede.dcnv["barra_neutra"].append(linha[18:22])
#             rede.dcnv["modo_operacao"].append(linha[23])
#             rede.dcnv["pontes"].append(linha[25])
#             rede.dcnv["corrente"].append(linha[27:32])
#             rede.dcnv["reatancia_comutacao"].append(linha[33:38])
#             rede.dcnv["tensao_secundario"].append(linha[39:44])
#             rede.dcnv["potencia_transformador"].append(linha[45:50])
#             rede.dcnv["resistencia_reator"].append(linha[51:56])
#             rede.dcnv["indutancia_reator"].append(linha[57:62])
#             rede.dcnv["capacitancia"].append(linha[63:68])
#             rede.dcnv["frequencia"].append(linha[69:71])
        
#         rede.idx_linha += 1
    
#     # DataFrame dos Dados de Conversores CA/CC
#     rede.dcnvDF = DF(data=rede.dcnv)
#     rede.dcnv = deepcopy(rede.dcnvDF)
#     rede.dcnvDF = rede.dcnvDF.replace(r"^\s*$", "0", regex=True)
#     rede.dcnvDF = rede.dcnvDF.astype(
#         {
#             "numero": "int",
#             "operacao": "object",
#             "barra_CA": "int",
#             "barra_CC": "int",
#             "barra_neutra": "int",
#             "modo_operacao": "object",
#             "pontes": "int",
#             "corrente": "float",
#             "reatancia_comutacao": "float",
#             "tensao_secundario": "float",
#             "potencia_transformador": "float",
#             "resistencia_reator": "float",
#             "indutancia_reator": "float",
#             "capacitancia": "float",
#             "frequencia": "float",
#         }
#     )

#     if rede.dcnvDF.empty:
#         ## ERROR - VERMELHO
#         raise ValueError(
#             "\033[91mERROR: Falha na leitura de codigo de execucao `DCNV`!\033[0m"
#         )
#     else:
#         rede.codigos["DCNV"] = True
        

# def dcsc(rede: DadosRedePWF):
#     """Leitura de dados de compensador série controlável
    
#     Args
#         rede
#     """
#     rede.dcsc["de"] = list()
#     rede.dcsc["operacao"] = list()
#     rede.dcsc["para"] = list()
#     rede.dcsc["circuito"] = list()
#     rede.dcsc["estado"] = list()
#     rede.dcsc["proprietario"] = list()
#     rede.dcsc["bypass"] = list()
#     rede.dcsc["reatancia_minima"] = list()
#     rede.dcsc["reatancia_maxima"] = list()
#     rede.dcsc["reatancia_inicial"] = list()
#     rede.dcsc["modo_controle"] = list()
#     rede.dcsc["especificado"] = list()
#     rede.dcsc["extremidade"] = list()
#     rede.dcsc["estagios"] = list()
#     rede.dcsc["capacidade_normal"] = list()
#     rede.dcsc["capacidade_emergencia"] = list()
#     rede.dcsc["capacidade"] = list()
#     rede.dcsc["agreg1"] = list()
#     rede.dcsc["agreg2"] = list()
#     rede.dcsc["agreg3"] = list()
#     rede.dcsc["agreg4"] = list()
#     rede.dcsc["agreg5"] = list()
#     rede.dcsc["agreg6"] = list()
#     rede.dcsc["agreg7"] = list()
#     rede.dcsc["agreg8"] = list()
#     rede.dcsc["agreg9"] = list()
#     rede.dcsc["agreg10"] = list()
    
#     while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
#         linha = rede.linhas[rede.idx_linha]
        
#         if linha[0] == rede.comentario:
#             pass 
        
#         else:
#             rede.dcsc["de"].append(linha[:5])
#             rede.dcsc["operacao"].append(linha[6])
#             rede.dcsc["para"].append(linha[9:14])
#             rede.dcsc["circuito"].append(linha[14:16])
#             rede.dcsc["estado"].append(linha[16])
#             rede.dcsc["proprietario"].append(linha[17])
#             rede.dcsc["bypass"].append(linha[18])
#             rede.dcsc["reatancia_minima"].append(linha[25:31])
#             rede.dcsc["reatancia_maxima"].append(linha[31:37])
#             rede.dcsc["reatancia_inicial"].append(linha[37:43])
#             rede.dcsc["modo_controle"].append(linha[43])
#             rede.dcsc["especificado"].append(linha[45:51])
#             rede.dcsc["extremidade"].append(linha[52:57])
#             rede.dcsc["estagios"].append(linha[57:60])
#             rede.dcsc["capacidade_normal"].append(linha[60:64])
#             rede.dcsc["capacidade_emergencia"].append(linha[64:68])
#             rede.dcsc["capacidade"].append(linha[68:72])
#             rede.dcsc["agreg1"].append(linha[72:75])
#             rede.dcsc["agreg2"].append(linha[75:78])
#             rede.dcsc["agreg3"].append(linha[78:81])
#             rede.dcsc["agreg4"].append(linha[81:84])
#             rede.dcsc["agreg5"].append(linha[84:87])
#             rede.dcsc["agreg6"].append(linha[87:90])
#             rede.dcsc["agreg7"].append(linha[90:93])
#             rede.dcsc["agreg8"].append(linha[93:96])
#             rede.dcsc["agreg9"].append(linha[96:99])
#             rede.dcsc["agreg10"].append(linha[99:102])
            
#         rede.idx_linha += 1
        
#     # DataFrame dos Dados de Compensador Serie Controlavel
#     rede.dcscDF = DF(data=rede.dcsc)
#     rede.dcsc = deepcopy(rede.dcscDF)
#     rede.dcscDF = rede.dcscDF.replace(r"^\s*$", "0", regex=True)
#     rede.dcscDF = rede.dcscDF.astype(
#         {
#             "de": "int",
#             "operacao": "object",
#             "para": "int",
#             "circuito": "int",
#             "estado": "object",
#             "proprietario": "object",
#             "bypass": "object",
#             "reatancia_minima": "float",
#             "reatancia_maxima": "float",
#             "reatancia_inicial": "float",
#             "modo_controle": "object",
#             "especificado": "object",
#             "extremidade": "object",
#             "estagios": "int",
#             "capacidade_normal": "float",
#             "capacidade_emergencia": "float",
#             "capacidade": "float",
#             "agreg1": "int",
#             "agreg2": "int",
#             "agreg3": "int",
#             "agreg4": "int",
#             "agreg5": "int",
#             "agreg6": "int",
#             "agreg7": "int",
#             "agreg8": "int",
#             "agreg9": "int",
#             "agreg10": "int",
#         }
#     )

#     if rede.dcscDF.empty:
#         ## ERROR - VERMELHO
#         raise ValueError(
#             "\033[91mERROR: Falha na leitura de codigo de execucao `DCSC`!\033[0m"
#         )
#     else:
#         rede.codigos["DCSC"] = True
        

def dcte(rede: DadosRedePWF):
    """Leitura de dados de constantes.
    
    Args
        rede
    """
    rede.dcte["constante"] = list()
    rede.dcte["valor_constante"] = list()
    
    while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
        linha = rede.linhas[rede.idx_linha]
        
        if linha[0] == rede.comentario:
            pass 
        
        else:
            rede.dcte["constante"].append(linha[:4].strip())
            rede.dcte["valor_constante"].append(linha[5:11].strip())
            rede.dcte["constante"].append(linha[12:16].strip())
            rede.dcte["valor_constante"].append(linha[17:23].strip())
            rede.dcte["constante"].append(linha[24:28].strip())
            rede.dcte["valor_constante"].append(linha[29:35].strip())
            rede.dcte["constante"].append(linha[36:40].strip())
            rede.dcte["valor_constante"].append(linha[41:47].strip())
            rede.dcte["constante"].append(linha[48:52].strip())
            rede.dcte["valor_constante"].append(linha[53:59].strip())
            rede.dcte["constante"].append(linha[60:64].strip())
            rede.dcte["valor_constante"].append(linha[65:71].strip())
        
        rede.idx_linha += 1
        
    # DataFrame dos Dados de Constantes
    rede.dcteDF = DF(data=rede.dcte)
    rede.dcte = deepcopy(rede.dcteDF)
    rede.dcteDF = rede.dcteDF.replace(r"^\s*$", np.nan, regex=True)
    rede.dcteDF = rede.dcteDF.astype(
        {
            "constante": "object",
            "valor_constante": "float",
        }
    )
    if rede.dcteDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de codigo de execucao `DCTE`!\033[0m"
        )
    else:
        rede.codigos["DCTE"] = True

        
        

# def dctg(rede: DadosRedePWF):
#     """Leitura de lista de casos de contingência.
    
#     Args
#         rede
#     """
#     rede.dctg1["identificacao"] = list()
#     rede.dctg1["operacao"] = list()
#     rede.dctg1["prioridade"] = list()
#     rede.dctg1["nome"] = list()
#     rede.dctg1["ndctg2"] = list()
#     rede.dctg2["tipo"] = list()
#     rede.dctg2["de"] = list()
#     rede.dctg2["para"] = list()
#     rede.dctg2["circuito"] = list()
#     rede.dctg2["extremidade"] = list()
#     rede.dctg2["variacao_geracao_ativa"] = list()
#     rede.dctg2["variacao_geracao_ativa_minima"] = list()
#     rede.dctg2["variacao_geracao_ativa_maxima"] = list()
#     rede.dctg2["variacao_geracao_reativa"] = list()
#     rede.dctg2["variacao_geracao_reativa_minima"] = list()
#     rede.dctg2["variacao_geracao_reativa_maxima"] = list()
#     rede.dctg2["variacao_fator_participacao"] = list()
#     rede.dctg2["grupo"] = list()
#     rede.dctg2["unidades"] = list()
#     idx = 0
    
#     while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
#         linha = rede.linhas[rede.idx_linha]
        
#         if linha[0] == rede.comentario:
#             pass 
        
#         elif rede.linhas[rede.idx_linha - 1][:] == rede.dctg1["ruler"]:
#             rede.dctg1["identificacao"].append(linha[:4])
#             rede.dctg1["operacao"].append(linha[5])
#             rede.dctg1["prioridade"].append(linha[7:9])
#             rede.dctg1["nome"].append(linha[10:56])
        
#         elif rede.linhas[rede.idx_linha - 1][:] == rede.dctg2["ruler"]:
#             rede.dctg1["ndctg2"].append(0)
            
#             while rede.linhas[rede.idx_linha].strip() != "FCAS":
#                 linha_ = rede.linhas[rede.idx_linha]
                
#                 if linha_[0] == rede.comentario:
#                     pass 
                
#                 else:
#                     rede.dctg2["tipo"].append(linha_[:4])
#                     rede.dctg2["de"].append(linha_[5:10])
#                     rede.dctg2["para"].append(linha_[11:16])
#                     rede.dctg2["circuito"].append(linha_[17:19])
#                     rede.dctg2["extremidade"].append(linha_[20:25])
#                     rede.dctg2["variacao_geracao_ativa"].append(linha_[26:31])
#                     rede.dctg2["variacao_geracao_ativa_minima"].append(linha_[32:37])
#                     rede.dctg2["variacao_geracao_ativa_maxima"].append(linha_[38:43])
#                     rede.dctg2["variacao_geracao_reativa"].append(linha_[44:49])
#                     rede.dctg2["variacao_geracao_reativa_minima"].append(linha_[50:55])
#                     rede.dctg2["variacao_geracao_reativa_maxima"].append(linha_[56:61])
#                     rede.dctg2["variacao_fator_participacao"].append(linha_[62:67])
#                     rede.dctg2["grupo"].append(linha_[68:70])
#                     rede.dctg2["unidades"].append(linha_[71:74])
                
#                 rede.dctg1["ndctg2"][idx] += 1
#                 rede.idx_linha += 1
#             idx += 1
#         rede.idx_linha += 1
        
    
#     # DataFrame dos Dados de Agregadores Genericos
#     rede.dctg1DF = DF(data=rede.dctg1)
#     rede.dctg1 = deepcopy(rede.dctg1DF)
#     rede.dctg1DF = rede.dctg1DF.replace(r"^\s*$", "0", regex=True)
#     rede.dctg1DF = rede.dctg1DF.astype(
#         {
#             "identificacao": "int",
#             "operacao": "object",
#             "prioridade": "int",
#             "nome": "object",
#         }
#     )

#     rede.dctg2DF = DF(data=rede.dctg2)
#     rede.dctg2 = deepcopy(rede.dctg2DF)
#     rede.dctg2DF = rede.dctg2DF.replace(r"^\s*$", "0", regex=True)
#     rede.dctg2DF = rede.dctg2DF.astype(
#         {
#             "tipo": "object",
#             "de": "int",
#             "para": "int",
#             "circuito": "int",
#             "extremidade": "object",
#             "variacao_geracao_ativa": "float",
#             "variacao_geracao_ativa_minima": "float",
#             "variacao_geracao_ativa_maxima": "float",
#             "variacao_geracao_reativa": "float",
#             "variacao_geracao_reativa_minima": "float",
#             "variacao_geracao_reativa_maxima": "float",
#             "variacao_fator_participacao": "float",
#         }
#     )
#     if rede.dctg1DF.empty or rede.dctg2DF.empty:
#         ## ERROR - VERMELHO
#         raise ValueError(
#             "\033[91mERROR: Falha na leitura de codigo de execucao `DCTG`!\033[0m"
#         )
#     else:
#         rede.codigos["DCTG"] = True
        

# def dctr(rede: DadosRedePWF):
#     """Leitura de dados complementares de transformadores
    
#     Args
#         rede
#     """
#     rede.dctr["de"] = list()
#     rede.dctr["operacao"] = list()
#     rede.dctr["para"] = list()
#     rede.dctr["circuito"] = list()
#     rede.dctr["tensao_minima"] = list()
#     rede.dctr["tensao_maxima"] = list()
#     rede.dctr["tipo_controle_1"] = list()
#     rede.dctr["modo_controle"] = list()
#     rede.dctr["fase_minima"] = list()
#     rede.dctr["fase_maxima"] = list()
#     rede.dctr["tipo_controle_2"] = list()
#     rede.dctr["valor_especificado"] = list()
#     rede.dctr["extremidade"] = list()
#     rede.dctr["taps"] = list()
    
#     while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
#         linha = rede.linhas[rede.idx_linha]
        
#         if linha[0] == rede.comentario:
#             pass 
        
#         else:
#             rede.dctr["de"].append(linha[:5])
#             rede.dctr["operacao"].append(linha[6])
#             rede.dctr["para"].append(linha[8:13])
#             rede.dctr["circuito"].append(linha[14:16])
#             rede.dctr["tensao_minima"].append(linha[17:21])
#             rede.dctr["tensao_maxima"].append(linha[22:26])
#             rede.dctr["tipo_controle_1"].append(linha[27])
#             rede.dctr["modo_controle"].append(linha[29])
#             rede.dctr["fase_minima"].append(linha[31:37])
#             rede.dctr["fase_maxima"].append(linha[38:44])
#             rede.dctr["tipo_controle_2"].append(linha[45])
#             rede.dctr["valor_especificado"].append(linha[47:53])
#             rede.dctr["extremidade"].append(linha[54:59])
#             rede.dctr["taps"].append(linha[60:62])
            
#         rede.idx_linha += 1
        
#     # DataFrame dos Dados Complementares de Transformadores
#     rede.dctrDF = DF(data=rede.dctr)
#     rede.dctr = deepcopy(rede.dctrDF)
#     rede.dctrDF = rede.dctrDF.replace(r"^\s*$", "0", regex=True)
#     rede.dctrDF = rede.dctrDF.astype(
#         {
#             "de": "int",
#             "operacao": "object",
#             "para": "int",
#             "circuito": "int",
#             "tensao_minima": "float",
#             "tensao_maxima": "float",
#             "tipo_controle_1": "object",
#             "modo_controle": "object",
#             "fase_minima": "float",
#             "fase_maxima": "float",
#             "tipo_controle_2": "object",
#             "valor_especificado": "float",
#             "extremidade": "object",
#             "taps": "int",
#         }
#     )

#     if rede.dctrDF.empty:
#         ## ERROR - VERMELHO
#         raise ValueError(
#             "\033[91mERROR: Falha na leitura de codigo de execucao `DCTR`!\033[0m"
#         )
#     else:
#         rede.codigos["DCTR"] = True
        
        

# def delo(rede: DadosRedePWF):
#     """Leitura de dados de elo CC
    
#     Args
#         rede
#     """
#     rede.delo["numero"] = list()
#     rede.delo["operacao"] = list()
#     rede.delo["tensao"] = list()
#     rede.delo["BMVA"] = list()
#     rede.delo["nome"] = list()
#     rede.delo["modo_high"] = list()
#     rede.delo["estado"] = list()
    
#     while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
#         linha = rede.linhas[rede.idx_linha]
        
#         if linha[0] == rede.comentario:
#             pass 
        
#         else:
#             rede.delo["numero"].append(linha[:4])
#             rede.delo["operacao"].append(linha[5])
#             rede.delo["tensao"].append(linha[7:12])
#             rede.delo["BMVA"].append(linha[13:18])
#             rede.delo["nome"].append(linha[19:39])
#             rede.delo["modo_high"].append(linha[40])
#             rede.delo["estado"].append(linha[42])
        
#         rede.idx_linha += 1
        
#     # DataFrame dos Dados de Elo CC
#     rede.deloDF = DF(data=rede.delo)
#     rede.delo = deepcopy(rede.deloDF)
#     rede.deloDF = rede.deloDF.replace(r"^\s*$", "0", regex=True)
#     rede.deloDF = rede.deloDF.astype(
#         {
#             "numero": "int",
#             "operacao": "object",
#             "tensao": "float",
#             "BMVA": "float",
#             "nome": "object",
#             "modo_high": "object",
#             "estado": "object",
#         }
#     )

#     if rede.deloDF.empty:
#         ## ERROR - VERMELHO
#         raise ValueError(
#             "\033[91mERROR: Falha na leitura de codigo de execucao `DELO`!\033[0m"
#         )
#     else:
#         rede.codigos["DELO"] = True
            
            
def dgbt(rede: DadosRedePWF):
    """Leitura de dados de grupos de base de tensão de barras CA.
    
    Args
        rede
    """
    rede.dgbt["grupo"] = list()
    rede.dgbt["tensao"] = list()
    
    while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
        linha = rede.linhas[rede.idx_linha]
        
        if linha[0] == rede.comentario:
            pass 
        
        else:
            rede.dgbt["grupo"].append(linha[:2].strip())
            rede.dgbt["tensao"].append(linha[3:8].strip())
        
        rede.idx_linha += 1
    
    # DataFrame dos Dados de Intercâmbio de Potencia Ativa entre areas
    rede.dgbtDF = DF(data=rede.dgbt)
    rede.dgbt = deepcopy(rede.dgbtDF)
    rede.dgbtDF = rede.dgbtDF.replace(r"^\s*$", np.nan, regex=True)
    rede.dgbtDF = rede.dgbtDF.astype(
        {
            "grupo": "object",
            "tensao": "float",
        }
    )
    if rede.dgbtDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de codigo de execucao `DGBT`!\033[0m"
        )
    else:
        rede.codigos["DGBT"] = True

   

def dger(rede: DadosRedePWF):
    """Leitura de dados de geradores.
    
    Args
        rede
    """
    rede.dger["numero"] = list()
    rede.dger["operacao"] = list()
    rede.dger["geracao_ativa_minima"] = list()
    rede.dger["geracao_ativa_maxima"] = list()
    rede.dger["fator_de_participacao"] = list()
    rede.dger["fator_de_participacao_de_controle_remoto"] = list()
    rede.dger["fator_de_potencia_nominal"] = list()
    rede.dger["fator_de_servico_armadura"] = list()
    rede.dger["fator_de_servico_rotor"] = list()
    rede.dger["angulo_de_carga"] = list()
    rede.dger["reatancia_de_maquina"] = list()
    rede.dger["potencia_aparente_nominal"] = list()
    rede.dger["estatismo"] = list()
    
    while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
        linha = rede.linhas[rede.idx_linha]
        
        if linha[0] == rede.comentario:
            pass 
        
        else:
            rede.dger["numero"].append(linha[:5].strip())
            rede.dger["operacao"].append(linha[6].strip())
            rede.dger["geracao_ativa_minima"].append(linha[8:14].strip())
            rede.dger["geracao_ativa_maxima"].append(linha[15:21].strip())
            rede.dger["fator_de_participacao"].append(linha[22:27].strip())
            rede.dger["fator_de_participacao_de_controle_remoto"].append(linha[28:33].strip())
            rede.dger["fator_de_potencia_nominal"].append(linha[34:39].strip())
            rede.dger["fator_de_servico_armadura"].append(linha[40:44].strip())
            rede.dger["fator_de_servico_rotor"].append(linha[45:49].strip())
            rede.dger["angulo_de_carga"].append(linha[50:54].strip())
            rede.dger["reatancia_de_maquina"].append(linha[55:60].strip())
            rede.dger["potencia_aparente_nominal"].append(linha[61:66].strip())
            rede.dger["estatismo"].append(linha[66:72].strip())
        
        rede.idx_linha += 1
    
    # DataFrame dos Dados de Geradores
    rede.dgerDF = DF(data=rede.dger)
    rede.dger = deepcopy(rede.dgerDF)
    rede.dgerDF = rede.dgerDF.replace(r"^\s*$", np.nan, regex=True)
    rede.dgerDF = rede.dgerDF.astype(
        {
            "numero": "Int64",
            "operacao": "object",
            "geracao_ativa_minima": "float",
            "geracao_ativa_maxima": "float",
            "fator_de_participacao": "float",
            "fator_de_participacao_de_controle_remoto": "float",
            "fator_de_potencia_nominal": "float",
            "fator_de_servico_armadura": "float",
            "fator_de_servico_rotor": "float",
            "angulo_de_carga": "float",
            "reatancia_de_maquina": "float",
            "potencia_aparente_nominal": "float",
            "estatismo": "float",
        }
    )
    if rede.dgerDF.empty:  
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de codigo de execucao `DGER`!\033[0m"
        )
    else:
        rede.codigos["DGER"] = True

       
        

def dglt(rede: DadosRedePWF):
    """Leitura de dados de grupos de limites de tensão.
    
    Args
        rede
    """
    rede.dglt["grupo"] = list()
    rede.dglt["limite_minimo"] = list()
    rede.dglt["limite_maximo"] = list()
    rede.dglt["limite_minimo_em_emergencia"] = list()
    rede.dglt["limite_maximo_em_emergencia"] = list()

    while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
        linha = rede.linhas[rede.idx_linha]
        
        if linha[0] == rede.comentario:
            pass 
        
        else:
            rede.dglt["grupo"].append(linha[:2].strip())
            rede.dglt["limite_minimo"].append(linha[3:8].strip())
            rede.dglt["limite_maximo"].append(linha[9:14].strip())
            rede.dglt["limite_minimo_em_emergencia"].append(linha[15:20].strip())
            rede.dglt["limite_maximo_em_emergencia"].append(linha[21:26].strip())
            
        rede.idx_linha += 1
    
    # DataFrame dos Dados de Intercâmbio de Potencia Ativa entre areas
    rede.dgltDF = DF(data=rede.dglt)
    rede.dglt = deepcopy(rede.dgltDF)
    rede.dgltDF = rede.dgltDF.replace(r"^\s*$", np.nan, regex=True)
    rede.dgltDF = rede.dgltDF.astype(
        {
            "grupo": "object",
            "limite_minimo": "float",
            "limite_maximo": "float",
            "limite_minimo_em_emergencia": "float",
            "limite_maximo_em_emergencia": "float",
        }
    )
    if rede.dgltDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de codigo de execucao `DGLT`!\033[0m"
        )
    else:
        rede.codigos["DGLT"] = True



# def dinc(rede: DadosRedePWF):
#     """Leitura de dados de incremento do nível de carregamento.
    
#     Args
#         rede
#     """
#     rede.dinc["tipo_incremento_1"] = list()
#     rede.dinc["identificacao_incremento_1"] = list()
#     rede.dinc["condicao_incremento_1"] = list()
#     rede.dinc["tipo_incremento_2"] = list()
#     rede.dinc["identificacao_incremento_2"] = list()
#     rede.dinc["condicao_incremento_2"] = list()
#     rede.dinc["tipo_incremento_3"] = list()
#     rede.dinc["identificacao_incremento_3"] = list()
#     rede.dinc["condicao_incremento_3"] = list()
#     rede.dinc["tipo_incremento_4"] = list()
#     rede.dinc["identificacao_incremento_4"] = list()
#     rede.dinc["condicao_incremento_4"] = list()
#     rede.dinc["passo_incremento_potencia_ativa"] = list()
#     rede.dinc["passo_incremento_potencia_reativa"] = list()
#     rede.dinc["maximo_incremento_potencia_ativa"] = list()
#     rede.dinc["maximo_incremento_potencia_reativa"] = list()
#     rede.dinc["tratamento_incremento_potencia_ativa"] = list()
#     rede.dinc["tratamento_incremento_potencia_reativa"] = list()
    
#     while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
#         linha = rede.linhas[rede.idx_linha]
        
#         if linha[0] == rede.comentario:
#             pass 
        
#         else:
#             rede.dinc["tipo_incremento_1"].append(linha[:4])
#             rede.dinc["identificacao_incremento_1"].append(linha[5:10])
#             rede.dinc["condicao_incremento_1"].append(linha[11])
#             rede.dinc["tipo_incremento_2"].append(linha[13:17])
#             rede.dinc["identificacao_incremento_2"].append(linha[18:23])
#             rede.dinc["condicao_incremento_2"].append(linha[24])
#             rede.dinc["tipo_incremento_3"].append(linha[26:30])
#             rede.dinc["identificacao_incremento_3"].append(linha[31:36])
#             rede.dinc["condicao_incremento_3"].append(linha[37])
#             rede.dinc["tipo_incremento_4"].append(linha[39:43])
#             rede.dinc["identificacao_incremento_4"].append(linha[44:49])
#             rede.dinc["condicao_incremento_4"].append(linha[50])
#             rede.dinc["passo_incremento_potencia_ativa"].append(linha[52:57])
#             rede.dinc["passo_incremento_potencia_reativa"].append(linha[58:63])
#             rede.dinc["maximo_incremento_potencia_ativa"].append(linha[64:69])
#             rede.dinc["maximo_incremento_potencia_reativa"].append(linha[70:75])
#             rede.dinc["tratamento_incremento_potencia_ativa"].append(False if linha[64:69] != "" else True)
#             rede.dinc["tratamento_incremento_potencia_reativa"].append(False if linha[70:75] != "" else True)
            
#         rede.idx_linha += 1
        
#     # DataFrame dos dados de Incremento do Nivel de Carregamento
#     rede.dincDF = DF(data=rede.dinc)
#     rede.dinc = deepcopy(rede.dincDF)
#     rede.dincDF = rede.dincDF.replace(r"^\s*$", "0", regex=True)
#     rede.dincDF = rede.dincDF.astype(
#         {
#             "tipo_incremento_1": "object",
#             "identificacao_incremento_1": "int",
#             "condicao_incremento_1": "object",
#             "tipo_incremento_2": "object",
#             "identificacao_incremento_2": "int",
#             "condicao_incremento_2": "object",
#             "tipo_incremento_3": "object",
#             "identificacao_incremento_3": "int",
#             "condicao_incremento_3": "object",
#             "tipo_incremento_4": "object",
#             "identificacao_incremento_4": "int",
#             "condicao_incremento_4": "object",
#             "passo_incremento_potencia_ativa": "float",
#             "passo_incremento_potencia_reativa": "float",
#             "maximo_incremento_potencia_ativa": "float",
#             "maximo_incremento_potencia_reativa": "float",
#             "tratamento_incremento_potencia_ativa": "bool",
#             "tratamento_incremento_potencia_reativa": "bool",
#         }
#     )
#     if rede.dincDF.empty:
#         ## ERROR - VERMELHO
#         raise ValueError(
#             "\033[91mERROR: Falha na leitura de codigo de execucao `DINC`!\033[0m"
#         )
#     else:
#         rede.codigos["DINC"] = True

      
      

# def dinj(rede: DadosRedePWF):
#     """Leitura de dados de injeções de potências, shunts e fatores de 
#     participação de geração do modelo equivalente
    
#     Args
#         rede
#     """
#     rede.dinj["numero"] = list()
#     rede.dinj["operacao"] = list()
#     rede.dinj["injecao_ativa_eq"] = list()
#     rede.dinj["injecao_reativa_eq"] = list()
#     rede.dinj["shunt_eq"] = list()
#     rede.dinj["fator_participacao_eq"] = list()
    
#     while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
#         linha = rede.linhas[rede.idx_linha]
        
#         if linha[0] == rede.comentario:
#             pass 
        
#         else:
#             rede.dinj["numero"].append(linha[:5])
#             rede.dinj["operacao"].append(linha[6])
#             rede.dinj["injecao_ativa_eq"].append(linha[8:15])
#             rede.dinj["injecao_reativa_eq"].append(linha[15:22])
#             rede.dinj["shunt_eq"].append(linha[22:29])
#             rede.dinj["fator_participacao_eq"].append(linha[29:36])
            
#         rede.idx_linha += 1
        
#     # DataFrame dos Dados de Injecao de Potencias, Shunts e Fatores de Participacao de Geracao do Modelo Equivalente
#     rede.dinjDF = DF(data=rede.dinj)
#     rede.dinj = deepcopy(rede.dinjDF)
#     rede.dinjDF = rede.dinjDF.replace(r"^\s*$", "0", regex=True)
#     rede.dinjDF = rede.dinjDF.astype(
#         {
#             "numero": "int",
#             "operacao": "object",
#             "injecao_ativa_eq": "float",
#             "injecao_reativa_eq": "float",
#             "shunt_eq": "float",
#             "fator_participacao_eq": "float",
#         }
#     )
#     if rede.dinjDF.empty:
#         ## ERROR - VERMELHO
#         raise ValueError(
#             "\033[91mERROR: Falha na leitura de codigo de execucao `DINJ`!\033[0m"
#         )
#     else:
#         rede.codigos["DINJ"] = True
        
        
def dlin(rede: DadosRedePWF):
    """Leitura de dados de linha de transmissão CA
    
    Args
        rede
    """
    rede.dlin["da_barra"] = list()
    rede.dlin["abertura_da_barra"] = list()
    rede.dlin["operacao"] = list()
    rede.dlin["abertura_para_barra"] = list()
    rede.dlin["para_barra"] = list()
    rede.dlin["circuito"] = list()
    rede.dlin["estado"] = list()
    rede.dlin["proprietario"] = list()
    rede.dlin["modo_de_controle"] = list()
    rede.dlin["resistencia"] = list()
    rede.dlin["reatancia"] = list()
    rede.dlin["susceptancia"] = list()
    rede.dlin["tap"] = list()
    rede.dlin["tap_minimo"] = list()
    rede.dlin["tap_maximo"] = list()
    rede.dlin["defasagem"] = list()
    rede.dlin["barra_controlada"] = list()
    rede.dlin["capacidade_normal"] = list()
    rede.dlin["capacidade_em_emergencia"] = list()
    rede.dlin["numero_de_taps"] = list()
    rede.dlin["capacidade_do_equipamento"] = list()
    rede.dlin["agregador_1"] = list()
    rede.dlin["agregador_2"] = list()
    rede.dlin["agregador_3"] = list()
    rede.dlin["agregador_4"] = list()
    rede.dlin["agregador_5"] = list()
    rede.dlin["agregador_6"] = list()
    rede.dlin["agregador_7"] = list()
    rede.dlin["agregador_8"] = list()
    rede.dlin["agregador_9"] = list()
    rede.dlin["agregador_10"] = list()
    rede.dlin["numero_de_unidades"] = list()
    rede.dlin["numero_de_unidades_em_operacao"] = list()
    
    while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
        linha = rede.linhas[rede.idx_linha]
        
        if linha[0] == rede.comentario:
            pass 
        
        else:
            rede.dlin["da_barra"].append(linha[:5].strip())
            rede.dlin["abertura_da_barra"].append(linha[5].strip())
            rede.dlin["operacao"].append(linha[7].strip())
            rede.dlin["abertura_para_barra"].append(linha[9].strip())
            rede.dlin["para_barra"].append(linha[10:15].strip())
            rede.dlin["circuito"].append(linha[15:17].strip())
            rede.dlin["estado"].append(linha[17].strip())
            rede.dlin["proprietario"].append(linha[18].strip())
            rede.dlin["modo_de_controle"].append(linha[19].strip())
            rede.dlin["resistencia"].append(linha[20:26].strip())
            rede.dlin["reatancia"].append(linha[26:32].strip())
            rede.dlin["susceptancia"].append(linha[32:38].strip())
            rede.dlin["tap"].append(linha[38:43].strip())
            rede.dlin["tap_minimo"].append(linha[43:48].strip())
            rede.dlin["tap_maximo"].append(linha[48:53].strip())
            rede.dlin["defasagem"].append(linha[53:58].strip())
            rede.dlin["barra_controlada"].append(linha[58:64].strip())
            rede.dlin["capacidade_normal"].append(linha[64:68].strip())
            rede.dlin["capacidade_em_emergencia"].append(linha[68:72].strip())
            rede.dlin["numero_de_taps"].append(linha[72:74].strip())
            rede.dlin["capacidade_do_equipamento"].append(linha[74:78].strip())
            rede.dlin["agregador_1"].append(linha[78:81].strip())
            rede.dlin["agregador_2"].append(linha[81:84].strip())
            rede.dlin["agregador_3"].append(linha[84:87].strip())
            rede.dlin["agregador_4"].append(linha[87:90].strip())
            rede.dlin["agregador_5"].append(linha[90:93].strip())
            rede.dlin["agregador_6"].append(linha[93:96].strip())
            rede.dlin["agregador_7"].append(linha[96:99].strip())
            rede.dlin["agregador_8"].append(linha[99:102].strip())
            rede.dlin["agregador_9"].append(linha[102:105].strip())
            rede.dlin["agregador_10"].append(linha[105:108].strip())
            rede.dlin["numero_de_unidades"].append(linha[109:112].strip())
            rede.dlin["numero_de_unidades_em_operacao"].append(linha[113:116].strip())
            
        rede.idx_linha += 1
        
    # DataFrame dos Dados de Linha
    rede.dlinDF = DF(data=rede.dlin)
    rede.dlin = deepcopy(rede.dlinDF)
    rede.dlinDF = rede.dlinDF.replace(r"^\s*$", np.nan, regex=True)
    rede.dlinDF = rede.dlinDF.astype(
        {
            "da_barra": "Int64",
            "abertura_da_barra": "object",
            "operacao": "object",
            "abertura_para_barra": "object",
            "para_barra": "Int64",
            "circuito": "object",
            "estado": "object",
            "proprietario": "object",
            "modo_de_controle": "object",
            "resistencia": "float",
            "reatancia": "float",
            "susceptancia": "float",
            "tap": "float",
            "tap_minimo": "float",
            "tap_maximo": "float",
            "defasagem": "float",
            "barra_controlada": "Int64",
            "capacidade_normal": "float",
            "capacidade_em_emergencia": "float",
            "numero_de_taps": "Int64",
            "capacidade_do_equipamento": "float",
            "agregador_1": "object",
            "agregador_2": "object",
            "agregador_3": "object",
            "agregador_4": "object",
            "agregador_5": "object",
            "agregador_6": "object",
            "agregador_7": "object",
            "agregador_8": "object",
            "agregador_9": "object",
            "agregador_10": "object",
            "numero_de_unidades": "Int64",
            "numero_de_unidades_em_operacao": "Int64"
        }
    )
    if rede.dlinDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de codigo de execucao `DLIN`!\033[0m"
        )
    else:
        rede.codigos["DLIN"] = True

      
    
        
def dopc(rede: DadosRedePWF):
    """Leitura de dados de código de opções de controle e execução
    padrão.
    
    Args
        rede
    """
    rede.dopc["opcao"] = list()
    rede.dopc["padrao"] = list()
    
    while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
        linha = rede.linhas[rede.idx_linha]
        
        if linha[0] == rede.comentario:
            pass 
        
        else:
            try:
                rede.dopc["opcao"].append(linha[:4].strip())
                rede.dopc["padrao"].append(linha[5].strip())
                rede.dopc["opcao"].append(linha[7:11].strip())
                rede.dopc["padrao"].append(linha[12].strip())
                rede.dopc["opcao"].append(linha[14:18].strip())
                rede.dopc["padrao"].append(linha[19].strip())
                rede.dopc["opcao"].append(linha[21:25].strip())
                rede.dopc["padrao"].append(linha[26].strip())
                rede.dopc["opcao"].append(linha[28:32].strip())
                rede.dopc["padrao"].append(linha[33].strip())
                rede.dopc["opcao"].append(linha[35:39].strip())
                rede.dopc["padrao"].append(linha[40].strip())
                rede.dopc["opcao"].append(linha[42:46].strip())
                rede.dopc["padrao"].append(linha[47].strip())
                rede.dopc["opcao"].append(linha[49:53].strip())
                rede.dopc["padrao"].append(linha[54].strip())
                rede.dopc["opcao"].append(linha[56:60].strip())
                rede.dopc["padrao"].append(linha[61].strip())
                rede.dopc["opcao"].append(linha[63:67].strip())
                rede.dopc["padrao"].append(linha[68].strip())
            except:
                rede.dopc["opcao"] = rede.dopc["opcao"][:-1]
                break 
        
        rede.idx_linha += 1 
        
    # DataFrame dos Dados de Constantes
    rede.dopcDF = DF(data=rede.dopc)
    rede.dopc = deepcopy(rede.dopcDF)
    rede.dopcDF = rede.dopcDF.replace(r"^\s*$", np.nan, regex=True)
    rede.dopcDF = rede.dopcDF.astype(
        {
            "opcao": "object",
            "padrao": "object",
        }
    )
    if rede.dopcDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de codigo de execucao `DOPC`!\033[0m"
        )
    else:
        rede.codigos["DOPC"] = True

        
        
        
# def dshl(rede: DadosRedePWF):
#     """Leitura de dados de dispositivos shunt de circuito CA
    
#     Args
#         rede
#     """
#     rede.dshl["from"] = list()
#     rede.dshl["operacao"] = list()
#     rede.dshl["to"] = list()
#     rede.dshl["circuito"] = list()
#     rede.dshl["shunt_from"] = list()
#     rede.dshl["shunt_to"] = list()
#     rede.dshl["estado_shunt_from"] = list()
#     rede.dshl["estado_shunt_to"] = list()
    
#     while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
#         linha = rede.linhas[rede.idx_linha]
        
#         if linha[0] == rede.comentario:
#             pass 
        
#         else:
#             rede.dshl["from"].append(linha[:5])
#             rede.dshl["operacao"].append(linha[6])
#             rede.dshl["to"].append(linha[9:14])
#             rede.dshl["circuito"].append(linha[14:16])
#             rede.dshl["shunt_from"].append(linha[17:23])
#             rede.dshl["shunt_to"].append(linha[23:29])
#             rede.dshl["estado_shunt_from"].append(linha[30:32])
#             rede.dshl["estado_shunt_to"].append(linha[33:35])
        
#         rede.idx_linha += 1
        
#     # DataFrame dos Dados de Constantes
#     rede.dshlDF = DF(data=rede.dshl)
#     rede.dshl = deepcopy(rede.dshlDF)
#     rede.dshlDF = rede.dshlDF.replace(r"^\s*$", "0", regex=True)
#     rede.dshlDF = rede.dshlDF.astype(
#         {
#             "from": "int",
#             "operacao": "object",
#             "to": "int",
#             "circuito": "object",
#             "shunt_from": "float",
#             "shunt_to": "float",
#             "estado_shunt_from": "object",
#             "estado_shunt_to": "object",
#         }
#     )
#     if rede.dshlDF.empty:
#         ## ERROR - VERMELHO
#         raise ValueError(
#             "\033[91mERROR: Falha na leitura de codigo de execucao `DSHL`!\033[0m"
#         )
#     else:
#         rede.codigos["DSHL"] = True
        
        
        
# def dtpf(rede: DadosRedePWF):
#     """Leitura de dados de fixação na aplicação do controle de tensão por
#     variação de tap.
    
#     Args
#         rede
#     """
#     rede.dtpf["tipo_elemento_1"] = list()
#     rede.dtpf["identificacao_elemento_1"] = list()
#     rede.dtpf["condicao_elemento_1"] = list()
#     rede.dtpf["tipo_elemento_2"] = list()
#     rede.dtpf["identificacao_elemento_2"] = list()
#     rede.dtpf["condicao_elemento_2"] = list()
#     rede.dtpf["tipo_elemento_3"] = list()
#     rede.dtpf["identificacao_elemento_3"] = list()
#     rede.dtpf["condicao_elemento_3"] = list()
#     rede.dtpf["tipo_elemento_4"] = list()
#     rede.dtpf["identificacao_elemento_4"] = list()
#     rede.dtpf["operacao"] = list()
#     rede.dtpf["interligacao"] = list()
    
#     while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
#         linha = rede.linhas[rede.idx_linha]
        
#         if linha[0] == rede.comentario:
#             pass 
        
#         else:
#             rede.dtpf["tipo_elemento_1"].append(linha[:4])
#             rede.dtpf["identificacao_elemento_1"].append(linha[5:10])
#             rede.dtpf["condicao_elemento_1"].append(linha[11])
#             rede.dtpf["tipo_elemento_2"].append(linha[13:17])
#             rede.dtpf["identificacao_elemento_2"].append(linha[18:23])
#             rede.dtpf["condicao_elemento_2"].append(linha[24])
#             rede.dtpf["tipo_elemento_3"].append(linha[26:30])
#             rede.dtpf["identificacao_elemento_3"].append(linha[31:36])
#             rede.dtpf["condicao_elemento_3"].append(linha[37])
#             rede.dtpf["tipo_elemento_4"].append(linha[39:43])
#             rede.dtpf["identificacao_elemento_4"].append(linha[44:49])
#             rede.dtpf["operacao"].append(linha[50])
#             rede.dtpf["interligacao"].append(linha[52])
        
#         rede.idx_linha += 1
        
#     # DataFrame dos dados de Fixacao na Aplicacao do Controle de Tensao por Variacao Automatica de Tap
#     rede.dtpfDF = DF(data=rede.dtpf)
#     rede.dtpf = deepcopy(rede.dtpfDF)
#     rede.dtpfDF = rede.dtpfDF.replace(r"^\s*$", "0", regex=True)
#     rede.dtpfDF = rede.dtpfDF.astype(
#         {
#             "tipo_elemento_1": "object",
#             "identificacao_elemento_1": "int",
#             "condicao_elemento_1": "object",
#             "tipo_elemento_2": "object",
#             "identificacao_elemento_2": "int",
#             "condicao_elemento_2": "object",
#             "tipo_elemento_3": "object",
#             "identificacao_elemento_3": "int",
#             "condicao_elemento_3": "object",
#             "tipo_elemento_4": "object",
#             "identificacao_elemento_4": "int",
#             "operacao": "object",
#             "interligacao": "float",
#         }
#     )
#     if rede.dtpfDF.empty:
#         ## ERROR - VERMELHO
#         raise ValueError(
#             "\033[91mERROR: Falha na leitura de codigo de execucao `DTPF`!\033[0m"
#         )
#     else:
#         rede.codigos["DTPF"] = True
        

# def dtpf_circ(rede: DadosRedePWF):
#     """Leitura de dados de fixação na aplicação do controle de tensão por
#     violação automática de tap.
    
#     Args
#         rede
#     """
            
#     rede.dtpf["de"] = list()
#     rede.dtpf["para"] = list()
#     rede.dtpf["circuito"] = list()
#     rede.dtpf["operacao"] = list()
    
#     while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
#         linha = rede.linhas[rede.idx_linha]
        
#         if linha[0] == rede.comentario:
#             pass 
        
#         else:
#             try:
#                 rede.dtpf["de"].append(linha[:5])
#                 rede.dtpf["para"].append(linha[6:11])
#                 rede.dtpf["circuito"].append(linha[12:14])
#                 rede.dtpf["operacao"].append(linha[75])
#                 rede.dtpf["de"].append(linha[15:20])
#                 rede.dtpf["para"].append(linha[21:26])
#                 rede.dtpf["circuito"].append(linha[27:29])
#                 rede.dtpf["operacao"].append(linha[75])
#                 rede.dtpf["de"].append(linha[30:35])
#                 rede.dtpf["para"].append(linha[36:41])
#                 rede.dtpf["circuito"].append(linha[42:44])
#                 rede.dtpf["operacao"].append(linha[75])
#                 rede.dtpf["de"].append(linha[45:50])
#                 rede.dtpf["para"].append(linha[51:56])
#                 rede.dtpf["circuito"].append(linha[57:59])
#                 rede.dtpf["operacao"].append(linha[75])
#                 rede.dtpf["de"].append(linha[60:65])
#                 rede.dtpf["para"].append(linha[66:71])
#                 rede.dtpf["circuito"].append(linha[72:74])
#                 rede.dtpf["operacao"].append(linha[75])
#             except:
#                 rede.dtpf["de"] = rede.dtpf["de"][:-1]
#                 break 
        
#         rede.idx_linha += 1
        
    
#     # DataFrame dos dados de Fixacao na Aplicacao do Controle de Tensao por Variacao Automatica de Tap
#     rede.dtpfDF = DF(data=rede.dtpf)
#     rede.dtpf   = deepcopy(rede.dtpfDF)
#     rede.dtpfDF = rede.dtpfDF.replace(r"^\s*$", "0", regex=True)
#     rede.dtpfDF = rede.dtpfDF.astype(
#         {
#             "de": "int",
#             "para": "int",
#             "circuito": "int",
#             "operacao": "object",
#         }
#     )
#     if rede.dtpfDF.empty:
#         ## ERROR - VERMELHO
#         raise ValueError(
#             "\033[91mERROR: Falha na leitura de codigo de execucao `DTPF`!\033[0m"
#         )
#     else:
#         rede.codigos["DTPF"] = True
        




# def dmet(rede: DadosRedePWF):
#     """Leitura de dados de monitoração para estabilidade de tensão
#     em barra CA
    
#     Args
#         rede
#     """
#     rede.dmet["tipo_elemento_1"] = list()
#     rede.dmet["identificacao_elemento_1"] = list()
#     rede.dmet["condicao_elemento_1"] = list()
#     rede.dmet["tipo_elemento_2"] = list()
#     rede.dmet["identificacao_elemento_2"] = list()
#     rede.dmet["condicao_elemento_2"] = list()
#     rede.dmet["tipo_elemento_3"] = list()
#     rede.dmet["identificacao_elemento_3"] = list()
#     rede.dmet["condicao_elemento_3"] = list()
#     rede.dmet["tipo_elemento_4"] = list()
#     rede.dmet["identificacao_elemento_4"] = list()
#     rede.dmet["operacao"] = list()
    
#     while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
#         linha = rede.linhas[rede.idx_linha]
        
#         if linha[0] == rede.comentario:
#             pass 
        
#         else:
#             rede.dmet["tipo_elemento_1"].append(linha[:4])
#             rede.dmet["identificacao_elemento_1"].append(linha[5:10])
#             rede.dmet["condicao_elemento_1"].append(linha[11])
#             rede.dmet["tipo_elemento_2"].append(linha[13:17])
#             rede.dmet["identificacao_elemento_2"].append(linha[18:23])
#             rede.dmet["condicao_elemento_2"].append(linha[24])
#             rede.dmet["tipo_elemento_3"].append(linha[26:30])
#             rede.dmet["identificacao_elemento_3"].append(linha[31:36])
#             rede.dmet["condicao_elemento_3"].append(linha[37])
#             rede.dmet["tipo_elemento_4"].append(linha[39:43])
#             rede.dmet["identificacao_elemento_4"].append(linha[44:49])
#             rede.dmet["operacao"].append(linha[50])
        
#         rede.idx_linha += 1
        
        
#     # DataFrame dos Dados de Monitoracao para Estabilidade de Tensao em Barra CA
#     rede.dmetDF = DF(data=rede.dmet)
#     rede.dmet = deepcopy(rede.dmetDF)
#     rede.dmetDF = rede.dmetDF.replace(r"^\s*$", "0", regex=True)
#     rede.dmetDF = rede.dmetDF.astype(
#         {
#             "tipo_elemento_1": "object",
#             "identificacao_elemento_1": "int",
#             "condicao_elemento_1": "object",
#             "tipo_elemento_2": "object",
#             "identificacao_elemento_2": "int",
#             "condicao_elemento_2": "object",
#             "tipo_elemento_3": "object",
#             "identificacao_elemento_3": "int",
#             "condicao_elemento_3": "object",
#             "tipo_elemento_4": "object",
#             "identificacao_elemento_4": "int",
#             "operacao": "object",
#         }
#     )
#     if rede.dmetDF.empty:
#         ## ERROR - VERMELHO
#         raise ValueError(
#             "\033[91mERROR: Falha na leitura de codigo de execucao `DMET`!\033[0m"
#         )
#     else:
#         rede.codigos["DMET"] = True



# def dmfl(rede: DadosRedePWF):
#     """Leitura de dados de monitoração de fluxo em circuito CA
    
#     Args
#         rede
#     """
#     rede.dmfl["tipo_elemento_1"] = list()
#     rede.dmfl["identificacao_elemento_1"] = list()
#     rede.dmfl["condicao_elemento_1"] = list()
#     rede.dmfl["tipo_elemento_2"] = list()
#     rede.dmfl["identificacao_elemento_2"] = list()
#     rede.dmfl["condicao_elemento_2"] = list()
#     rede.dmfl["tipo_elemento_3"] = list()
#     rede.dmfl["identificacao_elemento_3"] = list()
#     rede.dmfl["condicao_elemento_3"] = list()
#     rede.dmfl["tipo_elemento_4"] = list()
#     rede.dmfl["identificacao_elemento_4"] = list()
#     rede.dmfl["operacao"] = list()
#     rede.dmfl["interligacao"] = list()
    
#     while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
#         linha = rede.linhas[rede.idx_linha]
        
#         if linha[0] == rede.comentario:
#             pass 
        
#         else:
#             rede.dmfl["tipo_elemento_1"].append(linha[:4])
#             rede.dmfl["identificacao_elemento_1"].append(linha[5:10])
#             rede.dmfl["condicao_elemento_1"].append(linha[11])
#             rede.dmfl["tipo_elemento_2"].append(linha[13:17])
#             rede.dmfl["identificacao_elemento_2"].append(linha[18:23])
#             rede.dmfl["condicao_elemento_2"].append(linha[24])
#             rede.dmfl["tipo_elemento_3"].append(linha[26:30])
#             rede.dmfl["identificacao_elemento_3"].append(linha[31:36])
#             rede.dmfl["condicao_elemento_3"].append(linha[37])
#             rede.dmfl["tipo_elemento_4"].append(linha[39:43])
#             rede.dmfl["identificacao_elemento_4"].append(linha[44:49])
#             rede.dmfl["operacao"].append(linha[50])
#             rede.dmfl["interligacao"].append(linha[52])
           
#         rede.idx_linha += 1
        
    
#     # DataFrame dos dados de Monitoracao de Fluxo em Circuito CA
#     rede.dmflDF = DF(data=rede.dmfl)
#     rede.dmfl = deepcopy(rede.dmflDF)
#     rede.dmflDF = rede.dmflDF.replace(r"^\s*$", "0", regex=True)
#     rede.dmflDF = rede.dmflDF.astype(
#         {
#             "tipo_elemento_1": "object",
#             "identificacao_elemento_1": "int",
#             "condicao_elemento_1": "object",
#             "tipo_elemento_2": "object",
#             "identificacao_elemento_2": "int",
#             "condicao_elemento_2": "object",
#             "tipo_elemento_3": "object",
#             "identificacao_elemento_3": "int",
#             "condicao_elemento_3": "object",
#             "tipo_elemento_4": "object",
#             "identificacao_elemento_4": "int",
#             "operacao": "object",
#             "interligacao": "float",
#         }
#     )
#     if rede.dmflDF.empty:
#         ## ERROR - VERMELHO
#         raise ValueError(
#             "\033[91mERROR: Falha na leitura de codigo de execucao `DMFL`!\033[0m"
#         )
#     else:
#         rede.codigos["DMFL"] = True
        


# def dmfl_circ(rede: DadosRedePWF):
#     """Leitura de dados de monitoração de fluxo de circuito CA
    
#     Args
#         rede
#     """
#     rede.dmfl["de"] = list()
#     rede.dmfl["para"] = list()
#     rede.dmfl["circuito"] = list()
#     rede.dmfl["operacao"] = list()
    
#     while rede.linhas[rede.idx_linha].strip() not in rede.fim_bloco:
#         linha = rede.linhas[rede.idx_linha]
        
#         if linha[0] == rede.comentario:
#             pass 
        
#         else:
#             try:
#                 rede.dmfl["de"].append(linha[:5])
#                 rede.dmfl["para"].append(linha[6:11])
#                 rede.dmfl["circuito"].append(linha[12:14])
#                 rede.dmfl["operacao"].append(linha[75])
#                 rede.dmfl["de"].append(linha[15:20])
#                 rede.dmfl["para"].append(linha[21:26])
#                 rede.dmfl["circuito"].append(linha[27:29])
#                 rede.dmfl["operacao"].append(linha[75])
#                 rede.dmfl["de"].append(linha[30:35])
#                 rede.dmfl["para"].append(linha[36:41])
#                 rede.dmfl["circuito"].append(linha[42:44])
#                 rede.dmfl["operacao"].append(linha[75])
#                 rede.dmfl["de"].append(linha[45:50])
#                 rede.dmfl["para"].append(linha[51:56])
#                 rede.dmfl["circuito"].append(linha[57:59])
#                 rede.dmfl["operacao"].append(linha[75])
#                 rede.dmfl["de"].append(linha[60:65])
#                 rede.dmfl["para"].append(linha[66:71])
#                 rede.dmfl["circuito"].append(linha[72:74])
#                 rede.dmfl["operacao"].append(linha[75])
#             except:
#                 rede.dmfl["de"] = rede.dmfl["de"][:-1]
#                 break 
        
#         rede.idx_linha += 1
        
#     # DataFrame dos Dados de Constantes
#     rede.dmflDF = DF(data=rede.dmfl)
#     rede.dmfl = deepcopy(rede.dmflDF)
#     rede.dmflDF = rede.dmflDF.replace(r"^\s*$", "0", regex=True)
#     rede.dmflDF = rede.dmflDF.astype(
#         {
#             "de": "int",
#             "para": "int",
#             "circuito": "int",
#             "operacao": "object",
#         }
#     )

#     if rede.dmflDF.empty:
#         ## ERROR - VERMELHO
#         raise ValueError(
#             "\033[91mERROR: Falha na leitura de codigo de execucao `DMFL`!\033[0m"
#         )
#     else:
#         rede.codigos["DMFL"] = True
        
        
        
# def checkdanc(rede: DadosRedePWF):
#     """checa alteracao no nivel de carregamento

#     Args
#         rede:
#     """
#     # Variável
#     if rede.codigos["DANC"]:
#         for area in rede.dancDF["area"].values:
#             for idx, value in rede.dbarDF.iterrows():
#                 if value["area"] == area:
#                     rede.dbarDF.loc[idx, "demanda_ativa"] *= (
#                         1 + rede.dancDF["fator_carga_ativa"][0] / rede.cte["BMVA"]
#                     )
#                     rede.dbarDF.loc[idx, "demanda_reativa"] *= (
#                         1
#                         + rede.dancDF["fator_carga_reativa"][0] / rede.cte["BMVA"]
#                     )
#                     rede.dbarDF.loc[idx, "shunt_barra"] *= (
#                         1 + rede.dancDF["fator_shunt_barra"][0] / rede.cte["BMVA"]
#                     )





def opcoespwf(rede: DadosRedePWF):
    """configuracao de variaveis para processos de convergencia em analise e
    statica de fluxos de potencia determinacao dos valores padrao
    das constantes, variaveis de controle, variaveis de execucao, 
    variaveis de monitoramento e variaveis de relatorios

    Args
        rede:
    """
    rede.cte = dict(
        {
            "BMVA": 100.0,  # base de potencia para o sistema CA
            "DASE": 100.0,  # base de potencia default para o sistema CC
            "TEPA": 1e-3,  # tolerancia de convergencia de potencia ativa
            "TEPR": 1e-3,  # tolerancia de convergencia de potencia reativa
            "TLPR": 1e-3,  # tolerância para limite de geracao de potencia reativa
            "TLVC": 5e-3,  # tolerância para tensoes controladas
            "TLTC": 1e-4,  # tolerância para limite de tap de transformador
            "TETP": 5e-2,  # tolerância para erro de intercâmbio de potencia ativa entre areas
            "TBPA": 5e-2,  # tolerância para erro de redistribuicao de potencia ativa em contingencias de geracao/carga
            "TSFR": 1e-4,  # tolerância para deteccao de separacao fisica da rede eletrica
            "TUDC": 1e-5,  # tolerância de convergencia do erro de tensao em barra CC
            "TADC": 1e-4,  # tolerância para limite de ângulo de disparo/extincao de conversor
            "TPST": 2e-3,  # tolerância de erro de potencia reativa para aplicacao de variacao automatica de tap de transformador
            "QLST": 4e-3,  # tolerância de erro de potencia reativa para aplicacao de controle de limite de geracao de potencia reativa
            "EXST": 4e-3,  # tolerância de erro de potencia ativa para aplicacao de controle de intercâmbio de potencia ativa entre areas
            "TLPP": 1e-2,  # tolerância para a capacidade de carregamento de circuitos
            "TSBZ": 1e-4,  # tolerância para deteccao de variacao nula de fluxo de potencia ativa nos circuitos do sistema externo
            "TSBA": 5e-2,  # tolerância para deteccao de pequenas variacoes de fluxo de potencia ativa nos circuitos do sistema externo
            "PGER": 0.3,  # percentagem de geracao de potencia ativa a ser removida dos geradores do sistema interno para o calculo das variacoes de fluxo de potencia ativa nos circuitos do sistema externo
            "VFLD": 0.7,  # valor de tensao abaixo do qual a parcela de potencia constante das cargas funcionais passa a ser modelada como uma impedância constante
            "VART": 5e-2,  # variacao da tensao (em relacao ao caso base) a partir da qual uma barra passa a ser automaticamente monitorada no problema de fluxo de potencia continuado
            "TSTP": 33,  # número de steps do transformador com tap discreto
            "NDIR": 20,  # número de direcoes utilizado no processo de construcao da regiao de seguranca
            "STIR": 1,  # fator de divisao do passo atual de transferencia de geracao de potencia ativa quando ocorre alguma violacao no processo de construcao da regiao de seguranca
            "STTR": 5e-2,  # passo de transferencia de geracao de potencia ativa utilizado no processo de construcao da regiao de seguranca
            "TRPT": 1,  #  percentagem de geracao de potencia ativa utilizado no processo de construcao da regiao de seguranca
            "ZMIN": 1e-5,  # valor minimo do modulo de impedância dos circuitos CA
            "VDVN": 0.4,  # tensao minima para teste de divergencia automatica do caso
            "ICMN": 5e-4,  # valor minimo do incremento automatico de carga (utilizado como criterio de parada do metodo de fluxo de potencia continuado)
            "BFPO": 1e-2,  # valor minimo de injecao de potencia reativa de um banco shunt alocado pelo programa flupot
            "ZMAX": 5e2,  # tensao minima para teste de divergencia do caso
            "VDVM": 2.0,  # tensao maxima para teste de divergencia do caso
            "ASTP": 0.05,  # valor maximo de correcao de ângulo de fase da tensao durante o processo de solucao
            "VSTP": 5e-2,  # valor maximo de correcao de magnitude da tensao durante o processo de solucao
            "CSTP": 5e-2,  # valor maximo de correcao de susceptância do CSC durante o processo de solucao
            "DMAX": 5,  # numero maximo de vezes consecutivas que o fator de divisao FDIV pode ser aplicado (utilizado como criterio de parada do metodo de fluxo de potencia continuado)
            "TSDC": 0.02,  # valor maximo de correcao do tap do conversor do elo CC durante o processo de solucao
            "ASDC": 1,  # valor maximo de correcao do ângulo de disparo do conversor do elo CC durante o processo de solucao
            "ACIT": 30,  # numero maximo de iteracoes na solucao do fluxo de potencia CA
            "ICIT": 30,  # numero maximo de solucoes do fluxo de potencia a serem calculadas durante a execucao do problema de fluxo de potencia continuado
            "LPIT": 50,  # numero maximo de iteracoes do problema de programacao linear
            "LFLP": 10,  # numero maximo de iteracoes do problema de redespacho de potencia ativa
            "LFIT": 10,  # numero maximo de iteracoes na solucao da interface CA-CC
            "DCIT": 10,  # numero maximo de iteracoes na solucao do fluxo de potencia CC
            "VSIT": 10,  # numero maximo de iteracoes no ajuste da tensao em barra CC
            "LFCV": 1,  # número de iteracoes do metodo desacoplado rapido antes do inicio do processo de solucao pelo metodo de newton raphson
            "PDIT": 10,  # número de iteracoes na estimacao das perdas no modelo de fluxo de potencia linearizado
            "FDIV": 2,  # fator de reducao do incremento automatico de carga quando o problema de fluxo de potencia nao apresenta solucao durante a execucao do programa de fluxo de potencia continuado
            "ICMV": 5e-3,  # tamanho do passo inicial quando o parâmetro de continuacao muda de carregamento para o modulo de tensao
            "APAS": 0.9,  # determina o ponto a partir do qual o tamanho do passo do fluxo de potencia continuado parametrizado sera acelerado (% do carregamento maximo)
            "CPAR": 0.7,  # especifica o ponto de para do fluxo de potencia continuado parametrizado (% do carregamento maximo)
            "VAVT": 2e-2,  # criterio de variacao de tensao para a determinacao da rede complementar
            "VAVF": 5e-2,  # criterio de variacao de fluxo em funcao do carregamento nominal para a determinacao da rede complementar
            "VMVF": 15e-2,  # criterio de variacao de fluxo para a determinacao da rede complementar
            "VPVT": 2e-2,  # criterio de variacao de tensao para a terminacao da rede de simulacao - primeiro criterio
            "VPVF": 5e-2,  # criterio de variacao de fluxo em funcao do carregamento nominal para a determinacao da rede de simulacao - primeiro criterio
            "VPMF": 10e-2,  # criterio de variacao de fluxo para a determinacao da rede de simulacao - primeiro criterio
            # novas constantes adicionadas por JP
            "FBSE": 60.0,  # frequencia base do sep (criado por JP)
            "SIGA": 1e-6,  # tolerância da chave sigmoide SVC-A (criado por JP)
            "SIGQ": 1e-6,  # tolerância da chave sigmoide SVC-Q e QLIM (criado por JP)
            "SIGI": 1e-6,  # tolerância da chave sigmoide SVC-I (criado por JP)
            "SIGV": 1e-6,  # tolerância da chave sigmoide referente à variavel de tensao (criado por JP)
            "SIGK": 1e8,  # variavel de inclinacao da chave sigmoide (criado por JP)
            "FULL": 0,  # Curva completa do fluxo de potencia continuado (criado por JP)
            "VVAR": 1e-6,  # (criado por JP)
            "CTOL": 1e-7,  # tolerância para as variaveis de estado do metodo direto (canizares) (criado por JP)
        }
    )
    try:
        for idx, value in rede.dcteDF.iterrows():
            rede.cte[value.constante] = value.valor_constante
    except:
        rede.dcteDF = DF(
            {
                "constante": list(rede.cte.keys()),
                "valor_constante": list(rede.cte.values()),
            }
        )

    if rede.codigos["DINC"]:
        rede.cte["LMBD"] = rede.dincDF.loc[0, "passo_incremento_potencia_ativa"]
        rede.cte["cpfBeta"] = zeros(rede.nbus)
        if rede.codigos["DGER"]:
            for idx, value in rede.dgerDF.iterrows():
                # idx = value["numero"] - 1
                rede.cte["cpfBeta"][idx] = value.fator_participacao

    rede.ctrl = dict(
        {
            "CPHS": False,
            "CREM": False,
            "CSCA": False,
            "CTAP": False,
            "FREQ": False,
            "QLIM": False,
            "VLIM": False,
        }
    )
    rede.maskctrlcount = 0
    print("\033[96mOpcoes de controle escolhidas: ", end="")
    try:
        for idx, value in rede.dopcDF.iterrows():
            if (value.padrao == "L") and (value.opcao in rede.ctrl):
                rede.ctrl[value.opcao] = True
                rede.maskctrlcount += 1
                print(f"{value.opcao}", end=" ")
        print("\033[0m")
        if not any(rede.ctrl):
            print("\033[96mNenhuma opcao de controle foi escolhida.\033[0m")
    except:
        print("\033[96mNenhuma opcao de controle foi escolhida.\033[0m")

    rede.excc = dict(
        {
            "80CO": False,  # relatorios impressos em formato de 80 colunas
            "A0GI": False,  # gravacao automatica do arquivo de saida DGEI.dat durante etapa 1 de utilizacao do software ANAT0
            "ACCC": False,  # forca a reInicializacao do controle de tensao de dois ou mais elos de corrente continua do tipo ccc qie controlam a tensao da mesma barra CA pelo modo de tensao definido no codigo de execucao DCCV
            "ACFP": False,  # executa a analise de casos de fluxo de potencia atraves da impressao de relatorios que contem dados de transformadores que podem causar problemas à convergencia dos casos
            "ACLS": False,  # utilizada em conjunto com o codigo de execucao DANC, permite a especificacao da alteracao do carregamento atraves da linguagem de selecao
            "ADRE": False,  # indica que as restricoes lineares adicionais definidas no codigo de execucao DRES serao consideradas durante a solucao do problema de redespacho de potencia ativa
            "AGRE": False,  # utilizada com o codigo de execucao RELA, em conjunto com as opcoes para relatorios de equipamentos (RBAR, DADB, RLIN, DADL, RGER, RTRA, RLTC, RCSC, DADC, RSHB, RSHL, RBSH, RBSL, RFCR, RFQL), imprime o relatorio apenas dos agregadores e grupos selecionados de acordo com os campo de número de agregador e número de grupo do codigo de execucao DAGR
            "AGRF": False,  # utilizada com o codigo de execucao EXMT e com a opcao de execucao IDSA, atua nas etapas de agrupamento e incremento de geracao da ferramenta de identificacao de subareas e areas de modo a garantir que os elementos selecionados reduzam a folga do circuito de maior fator
            "ALPR": False,  # permite a alteracao da prioridade maxima de ativacao das variaveis de controle
            "AMOT": False,  # apos a execucao do processo de otimizacao pelo codigo de execucao EXOT, adiciona as modificacoes sugeridas pelo processo de otimizacao (FPO) ao caso em memoria
            "AREA": False,  # utilizada com o codigo de execucao RELA, permite selecionar a area ou as areas que serao impressas, de acordo com o campo número do codigo de execucao DARE
            "AREG": False,  # utilizada com o codigo de execucao ARQV, habilita o acrescimo automatico de registros ao arquivo historico
            "ASLK": False,
            "ATCR": False,
            "AUTO": False,
            "BPAR": False,
            "BPSI": False,
            "CBAS": False,
            "CCMT": False,
            "CELO": False,
            "CHAV": False,
            "CILH": False,
            "CINT": False,
            "CIRC": False,
            "CNF1": False,
            "CNF2": False,
            "CNF3": False,
            "CNF4": False,
            "CONT": False,
            "CONV": False,
            "CPB1": False,
            "CPB2": False,
            "CPER": False,
            "CPRI": False,
            "CTGS": False,
            "DIRB": False,
            "DIRT": False,
            "DMAB": False,
            "DMQA": False,
            "DMQR": False,
            "DMRE": False,
            "DPER": False,
            "ELIM": False,
            "EMOF": False,
            "EMRG": False,
            "EQPM": False,
            "ERRC": False,
            "ERRS": False,
            "ETP1": False,
            "ETP2": False,
            "EXPO": False,
            "EXSA": False,
            "FCTE": False,
            "FILE": False,
            "FINT": False,
            "FJAC": False,
            "FLAT": False,
            "FLEX": False,
            "FMCC": False,
            "FMCS": False,
            "FOBJ": False,
            "GICC": False,
            "GRAF": False,
            "GRAV": False,
            "GSAV": False,
            "HIST": False,
            "IANG": False,
            "ICMB": False,
            "ICRV": False,
            "IDSA": False,
            "IERR": False,
            "ILHA": False,
            "IMPO": False,
            "IMPR": False,
            "INDC": False,
            "INDV": False,
            "INIC": False,
            "INJF": False,
            "INMN": False,
            "JUMP": False,
            "LFDC": False,
            "LIST": False,
            "MANU": False,
            "MDEF": False,
            "NEWT": False,
            "NCAP": False,
            "NOVO": False,
            "OPEN": False,
            "ORDP": False,
            "ORDQ": False,
            "PARM": False,
            "PART": False,
            "PCTE": False,
            "PECO": False,
            "PERC": False,
            "PERD": False,
            "PESC": False,
            "PLEL": False,
            "PLTF": False,
            "PLTT": False,
            "PMIN": False,
            "PMVA": False,
            "POPE": False,
            "PVCT": False,
            "PVQV": False,
            "SIMU": False,
            "SNEW": False,
            "SPLI": False,
            "SQLI": False,
            "SQPR": False,
            "STEP": False,
            "STPO": False,
            "SUBS": False,
            "TABE": False,
            "TAPC": False,
            "TAPD": False,
            "TCIR": False,
            "TPER": False,
            "TRB1": False,
            "TRB2": False,
            "TRUN": False,
            "ULG2": False,
            "UNPG": False,
            "VABS": False,
            "VIRG": False,
            "VLCR": False,
            "VLDC": False,
            "VNUL": False,
        }
    )
    print("\033[96mOpcoes de execucao escolhidas: ", end="")
    try:
        for idx, value in rede.dopcDF.iterrows():
            if (value.opcao == "RCER") and (not rede.codigos["DCER"]):
                continue
            if (value.opcao == "FREQ") and (value.padrao == "L"):
                rede.freqjcount = 0
            if (value.padrao == "L") and (value.opcao in rede.excc):
                rede.excc[value.opcao] = True
                print(f"{value.opcao}", end=" ")
        print("\033[0m")
        if not any(rede.excc):
            print("\033[96mNenhuma opcao de execucao foi escolhida.\033[0m")
    except:
        print("\033[96mNenhuma opcao de controle foi escolhida.\033[0m")

    rede.monitor = dict(
        {
            "MFCT": False,
            "MOCF": False,
            "MOSF": False,
            "MOCG": False,
            "MOSG": False,
            "MOCT": False,
            "MOST": False,
            "MOCV": False,
        }
    )
    print("\033[96mOpcoes de monitoramento escolhidas: ", end="")
    try:
        for idx, value in rede.dopcDF.iterrows():
            if (value.padrao == "L") and (value.opcao in rede.monitor):
                rede.monitor[value.opcao] = True
                print(f"{value.opcao}", end=" ")
        print("\033[0m")
        if not any(rede.monitor):
            print("\033[96mNenhuma opcao de monitoramento foi escolhida.\033[0m")
    except:
        print("\033[96mNenhuma opcao de monitoramento foi escolhida.\033[0m")

    rede.report = dict(
        {
            "DADB": False,
            "DADC": False,
            "DADL": False,
            "RAGR": False,
            "RARE": False,
            "RARI": False,
            "RBAR": False,
            "RBEL": False,
            "RBEQ": False,
            "RBRC": False,
            "RBRS": False,
            "RBSH": False,
            "RBSI": False,
            "RBSL": False,
            "RCAI": False,
            "RCAR": False,
            "RCER": False,
            "RCMT": False,
            "RCON": False,
            "RCSC": False,
            "RCTE": False,
            "RCTG": False,
            "RCTR": False,
            "RCUR": False,
            "RCUS": False,
            "RCVC": False,
            "RCVG": False,
            "RDMS": False,
            "RDMT": False,
            "REMT": False,
            "REQV": False,
            "REST": False,
            "RETC": False,
            "RFCR": False,
            "RFQL": False,
            "RFRP": False,
            "RFXC": False,
            "RFXS": False,
            "RGBT": False,
            "RGER": False,
            "RGLT": False,
            "RILH": False,
            "RINT": False,
            "RLDC": False,
            "RLTP": False,
            "RLEQ": False,
            "RLIL": False,
            "RLIN": False,
            "RLTC": False,
            "RMAC": False,
            "RMIS": False,
            "RMON": False,
            "RMOT": False,
            "ROUT": False,
            "ROPC": False,
            "RPRL": False,
            "RREF": False,
            "RREM": False,
            "RRES": False,
            "RROP": False,
            "RRSI": False,
            "RRSU": False,
            "RSEL": False,
            "RSHB": False,
            "RSHL": False,
            "RSIS": False,
            "RSLP": False,
            "RTAB": False,
            "RTGR": False,
            "RTIE": False,
            "RTOT": False,
            "RTPF": False,
            "RTPL": False,
            "RTR3": False,
            "RTRA": False,
            "RTRP": False,
            "RTRU": False,
            "RVCO": False,
            "RVIO": False,
            "RVSA": False,
        }
    )
    print("\033[96mOpcoes de relatorio escolhidas: ", end="")
    try:
        for idx, value in rede.dopcDF.iterrows():
            if (value.padrao == "L") and (value.opcao in rede.report):
                rede.report[value.opcao] = True
                print(f"{value.opcao}", end=" ")
        print("\033[0m")
        if not any(rede.report):
            print("\033[96mNenhuma opcao de relatorio foi escolhida.\033[0m")
    except:
        print("\033[96mNenhuma opcao de relatorio foi escolhida.\033[0m")




class PosProcessadorPWF:
    
    """
    Classe por cruzar e enriquecer os dataframes extraídos
    do PWF, preenchendo colunas faltantes com base em 
    informações cruzadas entre os dataframes.
    """
    
   
    @classmethod
    def processar(cls, rede):
        
        # Carregamento do arquivo de configuração
        ref_recurso = importlib.resources.files("EnlineDevEng.parsers").joinpath(
                        "pwf_config.yaml")
        
        with ref_recurso.open("r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            
        
        # 1
        regras_gerais = config.get("regras_gerais")
        for regra in regras_gerais:
            cls._regra_geral(rede, regra)
        
        # 2
        regras_Individuais = config.get("regras_individuais")
        for regra in regras_Individuais:
            cls._regra_individual(rede, regra)
            
            
        regras_gerais = config.get("regras_gerais_2")
        for regra in regras_gerais:
            cls._regra_geral_2(rede, regra)
            
    
    
    @classmethod
    def _regra_geral(cls, rede, regra: Dict[str, Any]):
        """
        Executa o merge de um df auxiliar com um df alvo
        e armazena as coluna do merge do auxiliar 
        no df alvo.
        """
        nome_df_alvo = regra.get("df_alvo")
        df_alvo       = getattr(rede, nome_df_alvo, None)
        if df_alvo is None or df_alvo is np.nan or df_alvo.empty:
            return 
        
        valores_padrao = regra.get("valores_padrao_merge")
        mapa = {}
        
        for chave_valor in regra.get("colunas_coletar"):
            mapa.update(chave_valor)
                    
        try:
            df_aux = getattr(rede, regra.get("df_auxiliar"))
            col_chave_alvo = regra["coluna_merge_alvo"]
            col_chave_aux  = regra["coluna_merge_auxiliar"]
            
            cols_aux = [col for col in mapa.keys()
                        if col in df_aux.columns]
            
            cols_aux = list(set(cols_aux + col_chave_aux))
            
            df_aux = df_aux[cols_aux].drop_duplicates(subset=[col_chave_aux])
            
            dic_renomeiar = {}
            for col_origem in cols_aux:
                col_destino = mapa[col_origem]
                valor_padrao = valores_padrao.get(col_origem)
                df_aux[col_origem] = df_aux[col_origem].fillna(valor_padrao)
                dic_renomeiar[col_origem] = col_destino
            
            df_aux.rename(columns=dic_renomeiar, inplace=True)
            
            df_alvo = pd.merge(
                df_alvo,
                df_aux,
                left_on=col_chave_alvo,
                right_on=col_chave_aux,
                how="left"
            ).drop(columns=col_chave_aux)
            
        except Exception:
            try: # quando a coluna já existe
                for col_origem, col_destino in mapa.items():
                    valor_padrao = valores_padrao.get(col_origem)
                    mascara = df_alvo[col_origem].isna()
                    df_alvo.loc[mascara, col_destino] = valor_padrao

            except Exception:
                for col_origem, col_destino in mapa.items():
                    valor_padrao = valores_padrao.get(col_origem)
                    df_alvo[col_destino] = valor_padrao
                                    
        setattr(rede, nome_df_alvo, df_alvo)
        
        
        
    @classmethod
    def _regra_geral_2(cls, rede, regra: Dict[str, Any]):
        """
        Identifica barras controladas no DataFrame auxiliar (ex: dlinDF) apenas nos ramos
        que possuem tap válido (não nulo e não vazio) e atualiza o tipo dessas barras
        no DataFrame alvo (ex: dbarDF) para o valor especificado (ex: 'pqv').
        """
        if not isinstance(regra, dict):
            return

        nome_df_alvo = regra.get("df_alvo")
        df_alvo = getattr(rede, nome_df_alvo, None)
        if df_alvo is None or df_alvo is np.nan or df_alvo.empty:
            return

        nome_df_auxiliar = regra.get("df_auxiliar")
        df_auxiliar = getattr(rede, nome_df_auxiliar, None)
        if df_auxiliar is None or df_auxiliar is np.nan or df_auxiliar.empty:
            return

        col_num_alvo = regra["coluna_numero_df_alvo"]
        col_tipo_alvo = regra["coluna_tipo_df_alvo"]
        col_b_ctrl_aux = regra["coluna_barra_controlada_df_auxiliar"]
        col_tap_min_aux = regra["coluna_tap_min_df_auxiliar"]
        tipo_barra = regra["tipo_barra"]

        # Filtra linhas onde o tap não é None/NaN nem vazio (cobre coluna numérica ou string)
        tap_series = df_auxiliar[col_tap_min_aux]
        mascara_tap_valido = tap_series.notna() & (tap_series.astype(str).str.strip() != "")

        # Coleta os números únicos e válidos das barras controladas apenas nesses ramos
        barras_controladas = (
            df_auxiliar.loc[mascara_tap_valido, col_b_ctrl_aux]
            .dropna()
            .loc[lambda s: s != 0]
            .unique()
        )

        # Filtra no df_alvo e substitui o tipo
        mascara = df_alvo[col_num_alvo].isin(barras_controladas)
        df_alvo.loc[mascara, col_tipo_alvo] = tipo_barra

        setattr(rede, nome_df_alvo, df_alvo)
    
    
    
    @classmethod
    def _regra_individual(cls, rede, regra: Dict[str, Any]):
        """
        Executa autopreenchimento de padrões e regras Tipos 1 e 
        2 no df alvo.
        """
        
        nome_df = regra.get("df_alvo")
        df       = getattr(rede, nome_df, None)
        if df is None or df is np.nan or df.empty:
            return 
        
        
        valores_padrao = regra.get("valores_padrao_df_alvo")
        
        # preenche os np.nan com valor padrão
        for col, valor_padrao in valores_padrao.items():
            df[col] = df[col].fillna(valor_padrao)
            
        
        for sub_regra in (regra.get("regras_valores_padrao_df_alvo_tipo_1") or []):
            chave_coluna = next(k for k in sub_regra.keys() if k.startswith("coluna_alvo"))
            col_alvo = sub_regra[chave_coluna]
            
            condicao = sub_regra["condicao"]
            coluna_dependente = condicao["coluna_dependente"]
            operador = condicao["operador"]
            valor = condicao["valor"]
            
            valor_se_true = sub_regra["valor_se_verdadeiro"]
            valor_se_false = sub_regra["valor_se_falso"]
            
            mascara = operator.eq(df[coluna_dependente], valor)
            df[col_alvo] = np.where(mascara, valor_se_true, valor_se_false)
            
        
        for sub_regra in (regra.get("regras_valores_padrao_df_alvo_tipo_2") or []):
            chave_coluna = next(k for k in sub_regra.keys() if k.startswith("coluna_alvo"))
            col_alvo = sub_regra[chave_coluna]
            
            col_auxiliar = sub_regra["coluna_auxiliar"]
            
            mascara = df[col_alvo].isna()
            df[col_alvo] = np.where(mascara, df[col_auxiliar], df[col_alvo])
            
        
        for sub_regra in (regra.get("regras_valores_padrao_df_alvo_tipo_3") or []):
            col_alvo = sub_regra["coluna_alvo"]
            mapa_tipos_barra = {
                int(k): v
                for k, v in sub_regra.items()
                if k != "coluna_alvo"
            }
            
            df[col_alvo] = df[col_alvo].map(mapa_tipos_barra)
            
        
        for sub_regra in (regra.get("regra_5") or []):
            tapmin = sub_regra["coluna_tapmin"]
            tapmax = sub_regra["coluna_tapmax"]
            modo_de_controle = sub_regra["coluna_modo_de_controle"]
            
            mascara = df[tapmin].isna() | df[tapmax].isna()
            df[modo_de_controle] = np.where(mascara, "M", df[modo_de_controle])
            
        
        for sub_regra in (regra.get("regra_6") or []):
            barra_controlada = sub_regra["coluna_barra_controlada"]
            df[barra_controlada] = pd.to_numeric(df[barra_controlada], errors="coerce").abs().astype("UInt32")
            
                    
            
        setattr(rede, nome_df, df)
            
            
            