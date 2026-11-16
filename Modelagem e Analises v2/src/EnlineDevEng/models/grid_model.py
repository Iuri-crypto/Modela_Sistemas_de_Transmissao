

from dataclasses import dataclass, field
import numpy as np
from scipy.sparse import dok_matrix, csr_matrix
from typing import Dict, Optional



@dataclass(slots=True)
class GridModel:
    
    """
    Dados Elétricos no formato adequado
    para o solver.
    """
    
    Ybus     : Optional[dok_matrix] = None
    Ybus_csr : Optional[csr_matrix] = None
    S_esp    : Optional[np.ndarray] = None
    v        : Optional[np.ndarray] = None
    t        : Optional[np.ndarray] = None
    tap      : Optional[np.ndarray] = None
    bus_type : Optional[np.ndarray] = None     
    
    pv_idx   : Optional[np.ndarray] = None      # Índice numérico das barras PV
    pq_idx   : Optional[np.ndarray] = None      # Índice numérico das barras PQ
    vt_idx   : Optional[np.ndarray] = None      # Índice da barra slack
    pqv_idx  : Optional[np.ndarray] = None      # indice numérico das barras com o controle de tap
    
    num_buses: Optional[np.ndarray] = None
    
    bus_map  : dict[int, int]       = field(default_factory=dict)
    H        : np.ndarray           = field(default_factory=lambda: np.empty((0, 0), dtype=np.float64))
    N        : np.ndarray           = field(default_factory=lambda: np.empty((0, 0), dtype=np.float64))
    M        : np.ndarray           = field(default_factory=lambda: np.empty((0, 0), dtype=np.float64))
    L        : np.ndarray           = field(default_factory=lambda: np.empty((0, 0), dtype=np.float64)) 
    Q        : np.ndarray           = field(default_factory=lambda: np.empty((0, 0), dtype=np.float64))
    R        : np.ndarray           = field(default_factory=lambda: np.empty((0, 0), dtype=np.float64))
    
    
    dP       : Optional[np.ndarray] = None      
    dQ       : Optional[np.ndarray] = None      
    
    
    
    