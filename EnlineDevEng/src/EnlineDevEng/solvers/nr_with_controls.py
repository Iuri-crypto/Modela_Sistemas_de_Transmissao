

from EnlineDevEng.core.adm import BasePowerFlowSolver
from typing import Any
import numpy as np
from math import sin, cos
from scipy.sparse import bmat, csr_matrix, lil_matrix
from scipy.sparse.linalg import spsolve



class NewthonRaphsonSolver(BasePowerFlowSolver):
    aliases = ["nr_with_controls"]
    
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
        P_esp     = self.net.data.S_esp.real
        Q_esp     = self.net.data.S_esp.imag
        v         = self.net.data.v 
        t         = self.net.data.t
        bus_type  = self.net.data.bus_type 
        num_buses = self.net.data.num_buses
        H         = self.net.data.H
        N         = self.net.data.N
        M         = self.net.data.M
        L         = self.net.data.L
        Q         = self.net.data.Q
        R         = self.net.data.R
        dP        = self.net.data.dP
        dQ        = self.net.data.dQ
         
        indptr    = Ybus_csr.indptr
        indices   = Ybus_csr.indices
        G         = Ybus_csr.data.real
        B         = Ybus_csr.data.imag 
       
        idx_p     = np.where(np.isin(bus_type, ['pq', 'pv']))[0]
        idx_q     = np.where(np.isin(bus_type, ['pq']))[0]
        
        trafo     = self.net.trafo
        
    
        
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
            
            if max(dM) < self.tolerancia:
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
        
        
        

# def solve(self):
#         Ybus_csr  = self.net.data.Ybus_csr
#         S_esp     = self.net.data.S_esp
#         v         = self.net.data.v 
#         t         = self.net.data.t
#         bus_type  = self.net.data.bus_type.copy()
#         num_buses = self.net.data.num_buses
        
#         H = self.net.data.H
#         N = self.net.data.N
#         M = self.net.data.M
#         L = self.net.data.L
#         dP = self.net.data.dP
#         dQ = self.net.data.dQ

#         # Dados dos transformadores com controle automático de tap (LTC)
#         # Supondo arrays/listas em self.net.data para os trafos controlados:
#         # tap_from (k), tap_to (m), tap_ctrl_bus (c), tap_val (a), tap_v_esp,
#         # tap_g (g_km série), tap_b (b_km série), tap_shift (phi_km em rad),
#         # tap_min, tap_max
#         trafos = self.net.data.ltc_trafos  
#         num_ltc = len(trafos.tap_val)
        
#         # Matrizes Q (dP/da) e R (dQ/da) com dimensão (num_buses, num_ltc)
#         Q_tap = lil_matrix((num_buses, num_ltc), dtype=np.float64)
#         R_tap = lil_matrix((num_buses, num_ltc), dtype=np.float64)
        
#         # Ativa o controle: fixa V da barra controlada e muda tipo para 'pqv'
#         ativos = np.ones(num_ltc, dtype=bool)
#         for idx_t in range(num_ltc):
#             c = trafos.ctrl_bus[idx_t]
#             v[c] = trafos.v_esp[idx_t]
#             bus_type[c] = 'pqv'

#         P_esp = S_esp.real 
#         Q_esp = S_esp.imag

#         for iteration in range(1, self.maxiterations + 1):
#             # Atualiza índices a cada iteração (caso algum tap atinja limite e vire PQ)
#             idx_p = np.where(np.isin(bus_type, ['pq', 'pv', 'pqv']))[0][cite: 2]
#             idx_q = np.where(np.isin(bus_type, ['pq', 'pqv']))[0][cite: 2]
#             idx_v = np.where(bus_type == 'pq')[0][cite: 2]  # PQV fica de fora de dV!
#             idx_a = np.where(ativos)[0]

#             indptr  = Ybus_csr.indptr
#             indices = Ybus_csr.indices
#             G       = Ybus_csr.data.real
#             B       = Ybus_csr.data.imag 

#             # 1. LOOP PRINCIPAL DAS BARRAS (Inalterado!)
#             for k in range(num_buses):   
#                 inicio = indptr[k]
#                 fim    = indptr[k+1]
                
#                 P_calc_k = 0.0
#                 Q_calc_k = 0.0
#                 Gkk = 0.0
#                 Bkk = 0.0
                    
#                 for idx in range(inicio, fim):
#                     m   = indices[idx]
#                     Gkm = G[idx]
#                     Bkm = B[idx]
                    
#                     dT     = t[k] - t[m]
#                     sin_dt = sin(dT)
#                     cos_dt = cos(dT)
                    
#                     P_calc_k += v[m] * (Gkm * cos_dt + Bkm * sin_dt)
#                     Q_calc_k += v[m] * (Gkm * sin_dt - Bkm * cos_dt)
                    
#                     if k == m:
#                         Gkk = Gkm
#                         Bkk = Bkm
#                     else:
#                         H[k, m] =  v[k] * v[m] * (Gkm * sin_dt - Bkm * cos_dt)
#                         N[k, m] =  v[k]        * (Gkm * cos_dt + Bkm * sin_dt)
#                         M[k, m] = -v[k] * v[m] * (Gkm * cos_dt + Bkm * sin_dt)
#                         L[k, m] =  v[k]        * (Gkm * sin_dt - Bkm * cos_dt)
                
#                 P_inj_k = v[k] * P_calc_k
#                 Q_inj_k = v[k] * Q_calc_k
                
#                 H[k, k] = -(v[k]**2) * Bkk - Q_inj_k
#                 N[k, k] =   v[k]     * Gkk + (P_inj_k / v[k])
#                 M[k, k] = -(v[k]**2) * Gkk + P_inj_k
#                 L[k, k] =  -v[k]     * Bkk + (Q_inj_k / v[k])
                    
#                 dP[k] = P_esp[k] - P_inj_k
#                 dQ[k] = Q_esp[k] - Q_inj_k

#             # 2. NOVO LOOP: DERIVADAS EM RELAÇÃO AO TAP (Q_tap = dP/da e R_tap = dQ/da)[cite: 2]
#             Q_tap[:, :] = 0.0
#             R_tap[:, :] = 0.0
            
#             for col in idx_a:
#                 k   = trafos.from_bus[col]  # Barra sem tap (DE)
#                 m   = trafos.to_bus[col]    # Barra com tap (PARA - convenção ANAREDE)
#                 a   = trafos.tap_val[col]
#                 g   = trafos.g_series[col]
#                 b   = trafos.b_series[col]
#                 phi = trafos.shift[col]     # 0.0 se não for defasador

#                 ang = (t[k] - t[m]) + phi
#                 cos_ang = cos(ang)
#                 sin_ang = sin(ang)
#                 vk_vm   = v[k] * v[m]

#                 # Derivadas na barra k (from_bus, sem tap)
#                 Q_tap[k, col] = -vk_vm * (g * cos_ang + b * sin_ang)
#                 R_tap[k, col] =  vk_vm * (b * cos_ang - g * sin_ang)

#                 # Derivadas na barra m (to_bus, lado com tap a_km)
#                 Q_tap[m, col] =  2.0 * a * (v[m]**2) * g - vk_vm * (g * cos_ang - b * sin_ang)
#                 R_tap[m, col] = -2.0 * a * (v[m]**2) * b + vk_vm * (b * cos_ang + g * sin_ang)

#             # 3. MONTAGEM DA JACOBIANA AUMENTADA (6 BLOCOS)[cite: 2]
#             dM    = np.concatenate((dP[idx_p], dQ[idx_q]))
            
#             # Usa np.max(np.abs(dM)) para checar convergência antes de resolver
#             if np.max(np.abs(dM)) < self.tolerancia:
#                 break

#             H_red = H[np.ix_(idx_p, idx_p)][cite: 2]
#             N_red = N[np.ix_(idx_p, idx_v)][cite: 2]
#             Q_red = Q_tap[np.ix_(idx_p, idx_a)][cite: 2]

#             M_red = M[np.ix_(idx_q, idx_p)][cite: 2]
#             L_red = L[np.ix_(idx_q, idx_v)][cite: 2]
#             R_red = R_tap[np.ix_(idx_q, idx_a)][cite: 2]

#             J = bmat([
#                 [csr_matrix(H_red), csr_matrix(N_red), csr_matrix(Q_red)],
#                 [csr_matrix(M_red), csr_matrix(L_red), csr_matrix(R_red)]
#             ], format='csr')[cite: 2]
            
#             # 4. RESOLUÇÃO E ATUALIZAÇÃO DAS VARIÁVEIS DE ESTADO
#             dx = spsolve(J, dM)[cite: 2]
            
#             n_p = len(idx_p)
#             n_v = len(idx_v)
            
#             t[idx_p]            += dx[:n_p]
#             v[idx_v]            += dx[n_p : n_p + n_v]
#             trafos.tap_val[idx_a] += dx[n_p + n_v :]

#             # 5. VERIFICAÇÃO DE LIMITES E ATUALIZAÇÃO INCREMENTAL DA YBUS
#             for col in idx_a:
#                 a_novo = trafos.tap_val[col]
#                 a_min  = trafos.tap_min[col]
#                 a_max  = trafos.tap_max[col]

#                 # Se violar limite, trava o tap e reverte a barra PQV para PQ
#                 if a_novo > a_max or a_novo < a_min:
#                     a_novo = np.clip(a_novo, a_min, a_max)
#                     trafos.tap_val[col] = a_novo
#                     ativos[col] = False
#                     c = trafos.ctrl_bus[col]
#                     bus_type[c] = 'pq'

#                 # Atualiza as 4 posições da Ybus_csr com a diferença (novo - antigo)
#                 self._atualizar_ybus_trafo(Ybus_csr, trafos, col, a_novo)
        
        