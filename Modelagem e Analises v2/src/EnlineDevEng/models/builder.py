

from typing import Any
from EnlineDevEng.core.adm import BaseNetworkBuilder
from .grid_model import GridModel



class NetworkBuilder(BaseNetworkBuilder):
    
    """
    Lê os dataframes crus do objeto 'net', mapeia
    topologia, calcula impedâncias/admitâncias e 
    gera a matriz Ybus esparsa
    """
    
    def build(self, net: Any) -> GridModel:
        
        obj = GridModel()
        
        return obj 
    
    
    