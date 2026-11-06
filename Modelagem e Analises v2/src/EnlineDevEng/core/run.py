


from typing import Any
from .adm import BasePowerFlowSolver
from EnlineDevEng.models.builder import NetworkBuilder



def runpf(
    net: Any,
    algorithm: str = "nr",
    is_file: bool = True,
    dir_file: str = None,
    extension: str = None,
    **kwargs 
) -> Any:
    
    """
    
    """
    
    # 1
    if is_file == True:
        # chamar parser e enviar dados para net
        pass 
    
    # 2 - Converte os dados de entrada para modelos elétricos
    grid_model = NetworkBuilder.build(net)
    
    
    # 3 - Busca o solver
    solver = BasePowerFlowSolver.get_solver(
        algorithm,
        **kwargs
    )
    
    
    # 4 - Executa a solução 
    solver.solve(grid=grid_model)
    
    
    # 5 - Armazena os dados em net
    
    
    return net