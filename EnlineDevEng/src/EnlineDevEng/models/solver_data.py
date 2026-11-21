

from dataclasses  import dataclass, field
from scipy.sparse import dok_matrix, csr_matrix
from typing       import Optional
import numpy as np



@dataclass(slots=True)
class SolverData:
    
    """
  
    """
    
    Ybus     : Optional[dok_matrix] = None
    Ybus_csr : Optional[csr_matrix] = None
    S_esp    : Optional[np.ndarray] = None
    v        : Optional[np.ndarray] = None
    t        : Optional[np.ndarray] = None
    tap      : Optional[np.ndarray] = None
    bus_type : Optional[np.ndarray] = None     
    
    pv_idx   : Optional[np.ndarray] = None     
    pq_idx   : Optional[np.ndarray] = None     
    vt_idx   : Optional[np.ndarray] = None      
    q_min    : Optional[np.ndarray] = None
    q_max    : Optional[np.ndarray] = None
    v_esp    : Optional[np.ndarray] = None 
    idx_q    : Optional[np.ndarray] = None
    idx_p    : Optional[np.ndarray] = None
    #pqv_idx  : Optional[np.ndarray] = None      
    
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
    
    
    
    