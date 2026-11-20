

from pathlib import Path
from typing  import Any, Union


from .adm                               import Base__PowerFlowSolver, Base__NetworkParser, Base__NetworkFileBuilder
from EnlineDevEng.models.builder        import EletricModelsBuilder
from EnlineDevEng.utils.auxiliary       import EnlineDevEngNet
from EnlineDevEng.models.solver_data    import SolverData
from EnlineDevEng.analysis.subsystem2 import Subsystem2
import EnlineDevEng as ede 

data = SolverData()



# inicializações para funcionar a instanciação dinâmica
from EnlineDevEng.parsers.pwf_parser import PWFNetworkParser 
from EnlineDevEng.solvers.nr         import NewthonRaphsonSolver



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
        
        # 1.1 - Instancia o Parser.
        parser = Base__NetworkParser.get_parser(file_path)
        
        # 1.2 - Inicializar estrutura de dados
        net    = ede.create_empty_network()
        
        # 1.3 - Leitura do arquivo
        parser.parse(net=net, filepath=file_path)
        
        # 1.4 - Instancia o Modelador adequado
        file_builder = Base__NetworkFileBuilder.get_builder(file_path)
        
        # 1.5 - Injeta os dados na estrutura de dataframe
        file_builder.network_build(net=net, ede=ede)
        
    
    # 2 - Calcula Impedâncias, Admitâncias...
    EletricModelsBuilder.build(net=net, ede=ede, data=data)
    
    
    # 3 - Busca o solver (Newthon, Gauss, ...)
    solver = Base__PowerFlowSolver.get_solver(net, algorithm, **kwargs)
    
    
    # 4 - Executa a solução 
    solver.solve()
    
    
    # 5 - Cálculo do Subsistema 2
    Subsystem2.calculator(net)
    
    
    
    return net