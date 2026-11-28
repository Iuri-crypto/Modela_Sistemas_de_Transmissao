

import pandas as pd
import numpy as np
from typing import Any 



class ADict(dict):
    
    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(f"'EnlineDevEngNet' não possui o atributo '{item}'")
                    
    def __setattr__(self, key, value):
        self[key] = value 



class EnlineDevEngNet(ADict):
    """
    Construtor do EnlineDevEng
    O dicionário fornecido precisa conter os dataframes
    de dados da rede EnlineDevEng, por exemplo use o método
    da classe create_dataframes
    """
    
    # Autocomplete 
    # Dados Rede
    bus:      pd.DataFrame
    load:     pd.DataFrame
    gen:      pd.DataFrame
    shunt:    pd.DataFrame
    line:     pd.DataFrame
    trafo:    pd.DataFrame
    
    # Relatórios de Saída
    RBAR:     pd.DataFrame
    RLIN:     pd.DataFrame
    DADB:     pd.DataFrame
    DADL:     pd.DataFrame
    RGER:     pd.DataFrame
    RREF:     pd.DataFrame
    RTRA:     pd.DataFrame
    RLTC:     pd.DataFrame
    RSHB:     pd.DataFrame
    RBSH:     pd.DataFrame
    RSIS:     pd.DataFrame
    RARE:     pd.DataFrame
    RTOT:     pd.DataFrame
    RMIS:     pd.DataFrame
    RGLT:     pd.DataFrame
   
    # Cts básicas
    name:   str 
    f_hz:   float 
    sn_mva: float 
    
    
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
    
    @classmethod
    def create_dataframes(cls, data: dict) -> dict[str, pd.DataFrame]:
        """Cria e retorna um dicionario de dataframes."""
        for key in data:
            if isinstance(data[key], dict):
                data[key] = pd.DataFrame(columns=data[key].keys(),
                index=pd.Index([], dtype=np.int64)).astype(data[key])
        return data 
            