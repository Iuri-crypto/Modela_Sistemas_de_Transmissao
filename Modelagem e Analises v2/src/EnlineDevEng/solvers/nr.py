



from EnlineDevEng.core.adm import BasePowerFlowSolver
from EnlineDevEng.models.grid_model import GridModel


class NewthonRaphsonSolver(BasePowerFlowSolver):
    aliases = ["nr"]
    
    def __init__(
        self, 
        tolerancia:  float = 1e-6, 
        maxiterations: int = 20
    ):
        
        self.tolerancia = tolerancia
        self.maxiterations = maxiterations
        
    
    def solve(self, grid: GridModel, **kwargs):
         
        pass 