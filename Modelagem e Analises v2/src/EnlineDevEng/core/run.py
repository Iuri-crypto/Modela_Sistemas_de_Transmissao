

from pathlib import Path
from typing import Any, Union
from .adm import BasePowerFlowSolver, BaseNetworkParser, BaseNetworkFileBuilder
from EnlineDevEng.models.builder import NetworkBuilder
import EnlineDevEng as ede 
from EnlineDevEng.utils.auxiliary import EnlineDevEngNet
#from EnlineDevEng.models.pwf_builder import 





def runpf(
    input_data: Union[EnlineDevEngNet, Path],
    algorithm: str = "nr",
    **kwargs 
) -> Any:
    
    """
    
    """
    
    # 1
    if isinstance(input_data, Path):
        file_path = Path(input_data)
        parser = BaseNetworkParser.get_parser(file_path=file_path)
        net = ede.create_empty_network()
        parser.parse(net=net, filepath=file_path)
        file_builder = BaseNetworkFileBuilder.get_builder(file_path=file_path)
        file_builder.network_build(net=net)
        
    
    # 2 - Converte os dados de entrada para modelos elétricos
    grid_model = NetworkBuilder.build(net)
    
    
    # 3 - Busca o solver
    solver = BasePowerFlowSolver.get_solver(algorithm, **kwargs)
    
    
    # 4 - Executa a solução 
    solver.solve(grid=grid_model)
    
    
    # 5 - Armazena os dados em net
    
    
    return net