

from dataclasses import dataclass
import numpy as np
import scipy.sparse as sp
from typing import Dict, Any 



@dataclass(slots=True, frozen=True)
class GridModel:
    
    """
    Estrutura matemática imutável e vetorizada
    contendo apenas os dados necessários para
    os algoritmos numéricos.
    """
    
    Ybus: sp.csr_matrix       # Matriz de Admitância Nodal Esparsa
    Sbus: np.ndarray          # Vetor de Potências Aparentes injetadas
    V_theta: np.ndarray       # Vetor de tensões iniciais 
    pv_idx: np.ndarray        # Índice numérico das barras PV
    pq_idx: np.ndarray        # Índice numérico das barras PQ
    slack_idx: int            # Índice da barra slack
    bus_map: Dict[Any, int]   # Mapeamento do ID original da barra
    
    
    @property
    def num_buses(self) -> int:
        return len(self.V_theta)