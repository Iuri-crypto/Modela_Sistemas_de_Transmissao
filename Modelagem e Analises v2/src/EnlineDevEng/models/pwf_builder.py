

from EnlineDevEng.utils.auxiliary import EnlineDevEngNet
from EnlineDevEng.core.adm import BaseNetworkFileBuilder
import EnlineDevEng 
import pandas as pd


class PWFInjectorBuilder(BaseNetworkFileBuilder):
    
    """
    Lê a estrutura 'net.DadosRede' (extraída pelo PWFNetworkParser)
    e injeta automaticamente os elementos via 'pp.create_' do EnlineDevEng.
    """
    
    extensions = ["pwf"]
    
    def network_build(self, net: EnlineDevEngNet, ede: EnlineDevEng):
        
        """
        Popula o objeto 'net' com todas as tabelas extraídas
        do PWF.
        """
        
        DadosRede = net.DadosRede
        
        # DADOS DE BARRA DO ANAREDE
        if not DadosRede.dbarDF.empty:
            self._inject_buses_AC(net, ede, DadosRede.dbarDF)
            self._inject_balanced_load(net, ede, DadosRede.dbarDF)
            self._inject_balanced_generation(net, ede, DadosRede.dbarDF)
            self._inject_bus_shunt(net, ede, DadosRede.dbarDF)
            
        
        elif not DadosRede.dcerDF.empty:
            self._inject_statcom(net, ede, DadosRede.dbarDF)
            
        
        elif not DadosRede.dlinDF.empty:
            self._inject_line_AC(net, ede, DadosRede.dbarDF)
            self._inject_transformer(net, ede, DadosRede.dbarDF)
            
                    
        elif not DadosRede.dshlDF.empty:
            self._inject_line_shunt(net, ede, DadosRede.dbarDF)
        
        
        
    
    def _inject_bus_AC(self, net: EnlineDevEngNet, ede: EnlineDevEng,
                         df: pd.DataFrame):
        """
        Crias os barramentos AC
        """
    
    
    def _inject_balanced_load(self, net: EnlineDevEngNet, ede: EnlineDevEng,
                             df: pd.DataFrame):
        """
        Crias os barramentos AC
        """
    
    
    def _inject_balanced_generation(self, net: EnlineDevEngNet, ede: EnlineDevEng,
                             df: pd.DataFrame):
        """
        Crias os barramentos AC
        """
            
    def _inject_bus_shunt(self, net: EnlineDevEngNet, ede: EnlineDevEng,
                             df: pd.DataFrame):
        """
        Crias os barramentos AC
        """
            
    def _inject_statcom(self, net: EnlineDevEngNet, ede: EnlineDevEng,
                             df: pd.DataFrame):
        """
        Crias os barramentos AC
        """
            
    def _inject_line_AC(self, net: EnlineDevEngNet, ede: EnlineDevEng,
                             df: pd.DataFrame):
        """
        Crias os barramentos AC
        """
            
    def _inject_transformer(self, net: EnlineDevEngNet, ede: EnlineDevEng,
                             df: pd.DataFrame):
        """
        Crias os barramentos AC
        """
        
    def _inject_line_shunt(self, net: EnlineDevEngNet, ede: EnlineDevEng,
                                 df: pd.DataFrame):
        """
        Crias os barramentos AC
        """
        
        
    