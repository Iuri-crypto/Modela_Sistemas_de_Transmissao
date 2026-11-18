



from EnlineDevEng.core.adm import Base__PowerFlowSolver


from typing              import Any
from math                import sin, cos
from scipy.sparse        import bmat, csr_matrix, lil_matrix
from scipy.sparse.linalg import spsolve
import numpy as np    



class NewthonRaphsonSolver(Base__PowerFlowSolver):
    aliases = ["nr"]
    
    def __init__(
        self, 
        net: Any,
        tolerancia:  float = 1e-6, 
        maxiterations: int = 20
    ):
        
        self.net           = net
        self.tolerancia    = tolerancia
        self.maxiterations = maxiterations
        
        self.init_matrices()
        

    
    def solve(
        self
    ):
        
        Ybus_csr  = self.net.data.Ybus_csr
        S_esp     = self.net.data.S_esp
        v         = self.net.data.v 
        t         = self.net.data.t
        bus_type  = self.net.data.bus_type 
        num_buses = self.net.data.num_buses
        H         = self.net.data.H
        N         = self.net.data.N
        M         = self.net.data.M
        L         = self.net.data.L
        dP        = self.net.data.dP
        dQ        = self.net.data.dQ
         
        indptr    = Ybus_csr.indptr
        indices   = Ybus_csr.indices
        G         = Ybus_csr.data.real
        B         = Ybus_csr.data.imag 
        P_esp     = S_esp.real 
        Q_esp     = S_esp.imag
        idx_p     = np.where(np.isin(bus_type, ['pq', 'pv']))[0]
        idx_q     = np.where(np.isin(bus_type, ['pq']))[0]
        
    
        
        for iteration in range(1, self.maxiterations + 1):
            
            for k in range(num_buses):   
                inicio = indptr[k]
                fim    = indptr[k+1]
                
                P_calc_k = 0.0
                Q_calc_k = 0.0
                Gkk = 0.0
                Bkk = 0.0
                    
                for idx in range(inicio, fim):
                    m   = indices[idx]
                    Gkm = G[idx]
                    Bkm = B[idx]
                    
                    dT     = t[k] - t[m]
                    sin_dt = sin(dT)
                    cos_dt = cos(dT)
                    
                    # Acumula P e Q calculados (inclui k == m, onde sin(0)=0 e cos(0)=1)
                    P_calc_k += v[m] * (Gkm * cos_dt + Bkm * sin_dt)
                    Q_calc_k += v[m] * (Gkm * sin_dt - Bkm * cos_dt)
                    
                    if k == m:
                        Gkk = Gkm
                        Bkk = Bkm
                    else:
                        # Elementos fora da diagonal (k != m)
                        H[k, m] =  v[k] * v[m] * (Gkm * sin_dt - Bkm * cos_dt)
                        N[k, m] =  v[k]        * (Gkm * cos_dt + Bkm * sin_dt)
                        M[k, m] = -v[k] * v[m] * (Gkm * cos_dt + Bkm * sin_dt)
                        L[k, m] =  v[k]        * (Gkm * sin_dt - Bkm * cos_dt)
                
                # Multiplica pela tensão da barra k para obter a potência injetada final
                P_inj_k = v[k] * P_calc_k
                Q_inj_k = v[k] * Q_calc_k
                
                # Elementos da diagonal principal (k == m) usando P e Q CALCULADOS
                H[k, k] = -(v[k]**2) * Bkk - Q_inj_k
                N[k, k] =   v[k]     * Gkk + (P_inj_k / v[k])
                M[k, k] = -(v[k]**2) * Gkk + P_inj_k
                L[k, k] =  -v[k]     * Bkk + (Q_inj_k / v[k])
                    
                # Mismatch
                dP[k] = P_esp[k] - P_inj_k
                dQ[k] = Q_esp[k] - Q_inj_k
        
        
            dM    = np.concatenate((dP[idx_p], dQ[idx_q]))
            H_red = H[np.ix_(idx_p, idx_p)]
            N_red = N[np.ix_(idx_p, idx_q)]
            M_red = M[np.ix_(idx_q, idx_p)]
            L_red = L[np.ix_(idx_q, idx_q)]

            J     = bmat([[csr_matrix(H_red), csr_matrix(N_red)],
                          [csr_matrix(M_red), csr_matrix(L_red)]],
                    format='csr')
            
            # Resolução do Sistema Linear J * dx = dM
            dx    = spsolve(J, dM)
            
            # Atualização das varíaveis de estado
            t[idx_p] += dx[:len(idx_p)]
            v[idx_q] += dx[len(idx_p):]
            
            if (max(dM) < self.tolerancia) or (iteration > self.maxiterations):
                break 
        
    
    
    
    
    
    
    
    def init_matrices(
        self
    ):
        num_buses = self.net.data.num_buses
        self.net.data.H = lil_matrix((num_buses, num_buses), dtype=np.float64)
        self.net.data.N = lil_matrix((num_buses, num_buses), dtype=np.float64)
        self.net.data.M = lil_matrix((num_buses, num_buses), dtype=np.float64)
        self.net.data.L = lil_matrix((num_buses, num_buses), dtype=np.float64)
        self.net.data.Q = lil_matrix((num_buses, num_buses), dtype=np.float64)
        self.net.data.R = lil_matrix((num_buses, num_buses), dtype=np.float64)
        
        self.net.data.dP = np.zeros(num_buses, dtype=np.float64)
        self.net.data.dQ = np.zeros(num_buses, dtype=np.float64)
        
        
        
        
        
        