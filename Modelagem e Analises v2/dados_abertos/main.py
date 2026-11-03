
from pathlib import Path 
from ferramenta.analise_de_dados import Analise_de_Dados


raiz_projeto   = Path(__file__).resolve().parent.parent
pasta_dados    = raiz_projeto / "bases de dados"
caminho_schema = Path(__file__).resolve().parent / "schema.yaml"


# Base de dados
arquivos = {"Subestações_ONS"       : pasta_dados / "bases de dados" / "Dados da ONS"   / "Integração de Instalações"  / "Subestações da Rede em Operação.xlsx",
            "Linhas_Transmissão_ONS": pasta_dados / "bases de dados" / "Dados da ONS"   / "Integração de Instalações"  / "Linhas de Transmissão da Rede em Operação.xlsx",
            "Controle_Reativo_ONS"  : pasta_dados / "bases de dados" / "Dados da ONS"   / "Integração de Instalações"  / "Equipamentos de Controle de Reativos.xlsx",
            "Geração_ONS"           : pasta_dados / "bases de dados" / "Dados da ONS"   / "Integração de Instalações"  / "Capacidade Instalada de Geração.xlsx",
            "Transformadores_ONS"   : pasta_dados / "bases de dados" / "Dados da ONS"   / "Integração de Instalações"  / "Capacidade de Transformação da Rede Básica.xlsx",
            "Geração_ANEEL"         : pasta_dados / "bases de dados" / "Dados da ANEEL" / "Integração de Instalações"  / "siga-empreendimentos-geracao.xlsx"}



# Tratamento dos Dados
analise        = Analise_de_Dados(arquivos, caminho_schema)
dataframes     = analise.carrega()
dados          = analise.tipar_dados(dataframes=dataframes)