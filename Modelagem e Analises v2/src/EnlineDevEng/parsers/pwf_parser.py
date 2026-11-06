

from pathlib import Path 
from EnlineDevEng.core import BaseNetworkParser



class PWFNetworkParser(BaseNetworkParser):
    """
    Parser para arquivos de rede no formato ANAREDE (.pwf)
    """
    
    extensions = ["pwf"]
    
    
    def parse(self, net, filepath: Path, encoding: str = "latin-1"):
        pass 