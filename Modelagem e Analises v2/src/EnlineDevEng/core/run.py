

from pathlib import Path
from typing import Any, Union
from .adm import BasePowerFlowSolver, BaseNetworkParser, BaseNetworkFileBuilder
from EnlineDevEng.models.builder import NetworkBuilder
import EnlineDevEng as ede 
from EnlineDevEng.utils.auxiliary import EnlineDevEngNet
#from EnlineDevEng.models.pwf_builder import 



# inicializações para funcionar a instanciação dinâmica
from EnlineDevEng.parsers.pwf_parser import PWFNetworkParser




def runpf(
    net       : EnlineDevEngNet        = None,
    dir_file  : Union[str, Path, None] = None,
    algorithm : str                    = "nr",
    **kwargs 
) -> Any:
    
    """
    
    """
    
    file_path = Path(f"{dir_file}")
    
    
    # 1 - Se dir_file existir, então será carregado os dados do arquivo.
    if isinstance(file_path, Path):
        
        # 1.1 - Seleção dinâmica da classe de Parser.
        parser = BaseNetworkParser.get_parser(file_path)
        
        # 1.2 - Inicializar estrutura de dados
        net    = ede.create_empty_network()
        
        # 1.3 - Leitura do arquivo
        parser.parse(net=net, filepath=file_path)
        
        # 1.4 - Instancia o Modelador adequado
        file_builder = BaseNetworkFileBuilder.get_builder(file_path)
        
        # 1.5 - Injeta os dados na estrutura de dataframe
        file_builder.network_build(net=net, ede=ede)
        
    
    # 2 - Calcula Impedâncias, Admitâncias...
    grid_model = NetworkBuilder.build(net=net, ede=ede)
    
    
    # 3 - Busca o solver (Newthon, Gauss, ...)
    solver = BasePowerFlowSolver.get_solver(algorithm, **kwargs)
    
    
    # 4 - Executa a solução 
    solver.solve(grid=grid_model)
    
    
    # 5 - Armazena os dados em net
    
    
    return net