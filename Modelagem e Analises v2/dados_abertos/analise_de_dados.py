
import yaml
import pandas as pd
from pathlib import Path

class Analise_de_Dados:
    
    def __init__(self, arquivos: dict[str, Path], caminho_schema: Path):
        self.arquivos       = arquivos 
        self.caminho_schema = caminho_schema   
        self.schema         = dict()
        
        

    def carrega(self) -> dict[str, pd.DataFrame]:
        """Carrega planilhas Excel.
        
        Returns:
            >> dict[str, pd.DataFrame] <<: Dicionário [dataframes] em que cada chave é o nome\
            da planilha e cada valor é o dataframe correspondente.
        
        Raises:
            FileNotFoundError: Se algum dos arquivos configurados não existir.
        
        """
        dataframes = {}
        
        for arquivo_nome, caminho in self.arquivos.items():
            if not caminho.is_file:
                raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
            dataframes[arquivo_nome] = pd.read_excel(caminho)
    
        if not self.caminho_schema.is_file:
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
        
        with open(self.caminho_schema, "r", encoding="utf-8") as f:
            self.schema = yaml.safe_load(f)
            
        return dataframes
                
    
    
    def tipar_dados(self, dataframes: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
        """Converte as colunas dos dataframes conforme os tipos configurados.
        
        Para cada Dataframe em "dataframe", procura no dicionário "schema" 
        a configuração correpondente e converte as colunas indicadas.
        
        Args:
             dataframes: Dicionário de dataframes. Cada chave identifica um dataframe.
             shema: Dicionário com os tipos esperados.
            
        Returns:
             Um dicionário [dataframes] com os dataframes tipados.
        
        Raises:
             KeyError: Se faltar faltar a configuração de um dataframe ou alguma
                coluna configurada não existir nele.
             ValueError: Se não for possível converter uma coluna para o tipo
                configurado.
        """
        for nome_df, df in dataframes.items():
            if nome_df not in self.schema:
                raise KeyError(f"Não existe configuração de tipos para '{nome_df}' no schema")
            
            tipos_e_colunas = self.schema.get(nome_df)
            for coluna, tipo in tipos_e_colunas.items():
                try:
                    df[coluna] = df[coluna].astype(tipo)
                except (TypeError, ValueError) as erro:
                    raise ValueError(f"Falha ao converter '{nome_df}.{coluna}' para '{tipo}'") from erro
                
            dataframes[nome_df] = df 
            
        return dataframes
    
    
    
    
 