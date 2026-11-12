

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
    bus:      pd.DataFrame
    load:     pd.DataFrame
    gen:      pd.DataFrame
    shunt:    pd.DataFrame
    ext_grid: pd.DataFrame
    line:     pd.DataFrame
    trafo:    pd.DataFrame
    
    res_bus:      pd.DataFrame
    res_ext_grid: pd.DataFrame
    res_line:     pd.DataFrame
    res_trafo:    pd.DataFrame
    res_load:     pd.DataFrame
    res_shunt:    pd.DataFrame
    res_gen:      pd.DataFrame
        
    _empty_res_bus:      pd.DataFrame
    _empty_res_ext_grid: pd.DataFrame
    _empty_res_line:     pd.DataFrame
    _empty_res_trafo:    pd.DataFrame
    _empty_res_load:     pd.DataFrame
    _empty_res_shunt:    pd.DataFrame
    _empty_res_gen:      pd.DataFrame
    
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
            