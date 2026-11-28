



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
        tolerancia_controles: float = 1e-3,
        maxiterations: int = 20
    ):
        
        self.net           = net
        self.tolerancia    = tolerancia
        self.tolerancia_controles = tolerancia_controles
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
        
        idx_q       = self.net.data.idx_q
        idx_q_lim_v = self.net.data.pq_lim_v_idx.copy()
        idx_p       = self.net.data.idx_p        
        
        q_min     = self.net.data.q_min
        q_max     = self.net.data.q_max
        v_esp     = self.net.data.v_esp
        
        bmva         = self.net.DadosRede.cte["BMVA"]
        qlst         = self.net.DadosRede.cte["QLST"]
        tlpr         = self.net.DadosRede.cte["TLPR"]
        tlvc         = self.net.DadosRede.cte["TLVC"]
        tepa         = self.net.DadosRede.cte["TEPA"]
        tepr         = self.net.DadosRede.cte["TEPR"]
        
        q_carga_pu   = self.net.DadosRede.dbarDF["carga_reativa"].to_numpy(dtype=np.float64) / bmva
        q_geracao_pu = self.net.DadosRede.dbarDF["geracao_reativa"].to_numpy(dtype=np.float64) / bmva
        
        v_min     = self.net.data.v_min
        v_max     = self.net.data.v_max
        
        iter_nr    = 0
        iter_controle = 0
        
        for iteration in range(1, self.maxiterations + 1):
            iter_nr = iteration
                
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
            
            
            if (np.max(np.abs(dM)) < qlst):
                
                # # --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
                # #                              Monticelli - 6.3. Controle de tensão em barras PV [12]
                            
                trocas_controle_v_barras_pv = self.controle_q_barras_pv(
                    Q_esp, idx_q, bus_type, q_min, q_max, v, v_esp, q_carga_pu, bmva, tlpr, tlvc
                )
                
                
                # # --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
                # #                              Monticelli - 6.4 Limite de Tensão em barras PQ [10. 12]
                            
                trocas_limite_v_barras_pq = self.limite_v_barras_pq(
                    Q_esp, idx_q, bus_type, v, v_esp, q_geracao_pu, q_carga_pu,  bmva, v_min, v_max, tlvc,
                    q_min, q_max, tlpr, idx_q_lim_v
                )

            
            
            convergencia = self.avaliar_convergencia(dP[idx_p], dQ[idx_q], tepa, tepr, iteration)
            if convergencia:
                break
    
    
    
    
    def avaliar_convergencia(
        self,
        dp,
        dq,
        tepa,
        tepr,
        iteration,
    ):
        # Avaliar convergência dos resíduos de potência ativa e reativa
        dp = np.max(np.abs(dp))
        dq = np.max(np.abs(dq))
        
        etapa_1 = False
        
        if (dp <= tepa) and (dq <= tepr):
            etapa_1 = True 
        
        if etapa_1 and (iteration <= self.maxiterations):
            return True 
        
        else:
            return False
        
        
    
    def controle_q_barras_pv(
        self,
        Q_esp: np.ndarray,
        idx_q: list[int], 
        bus_type: np.ndarray, 
        q_min: np.ndarray, 
        q_max: np.ndarray,
        v_cal: np.ndarray,
        v_esp: np.ndarray,
        q_carga_pu: np.ndarray,
        bmva: float,
        tlpr: float,
        tlvc: float
    ):
        q_geracao_pu = self.q_cal(bmva, tipo_bar="pv")
        trocas       = 0
        
        for idx in range(len(bus_type)):
            if bus_type[idx] != "pv":
                continue
                
            qcal_k = q_geracao_pu[idx]
            qmin_k = q_min[idx]
            qmax_k = q_max[idx]
            vcal   = v_cal[idx]
            vesp   = v_esp[idx]
            
            esta_como_pq = idx in idx_q
            
            # 1. BARRA OPERANDO COMO PV -> Verifica violação de limites de reativo
            if not esta_como_pq:
                if (qcal_k + tlpr) < qmin_k:
                    idx_q.append(idx)
                    idx_q.sort()
                    # Injeção líquida em p.u. = (Geração_min - Carga) 
                    Q_esp[idx] = (qmin_k - q_carga_pu[idx]) 
                    trocas     += 1
                    
                elif (qcal_k - tlpr) > qmax_k:
                    idx_q.append(idx)
                    idx_q.sort()
                    # Injeção líquida em p.u. = (Geração_max - Carga) 
                    Q_esp[idx] = (qmax_k - q_carga_pu[idx]) 
                    trocas     += 1
            
         
            
            # 2. BARRA SATURADA COMO PQ -> Verifica se pode voltar para PV
            else:
                travada_no_max = np.isclose(Q_esp[idx], (qmax_k - q_carga_pu[idx]))
                travada_no_min = np.isclose(Q_esp[idx], (qmin_k - q_carga_pu[idx]))
                
                if travada_no_max and ((vcal - tlvc) > vesp):
                    idx_q.remove(idx)
                    v_cal[idx] = vesp
                    trocas     += 1
                    
                elif travada_no_min and ((vcal + tlvc) < vesp):
                    idx_q.remove(idx)
                    v_cal[idx] = vesp
                    trocas     += 1
                    
        return trocas 
    
    
    
    
    def limite_v_barras_pq(
        self,
        Q_esp: np.ndarray,
        idx_q: list[int], 
        bus_type: np.ndarray, 
        v_cal: np.ndarray,
        v_esp: np.ndarray,
        q_geracao_pu: np.ndarray,
        q_carga_pu: np.ndarray,
        bmva: float,
        v_min,
        v_max,
        tlvc,
        q_min,
        q_max,
        tlpr,
        idx_q_lim_v
    ):
        q_geracao_pu = self.q_cal(bmva, tipo_bar="pq_lim_v")
        trocas       = 0
        
        for idx in range(len(bus_type)):
            if bus_type[idx] != "pq_lim_v":
                continue
                
            QgeracaoPu = q_geracao_pu[idx]
            #Qesp   = Q_esp[idx]
            vcal   = v_cal[idx]
            #vesp   = v_esp[idx]
            vmin   = v_min[idx]
            vmax   = v_max[idx]
            qmin   = q_min[idx]
            qmax   = q_max[idx]
            
            esta_como_pq = idx in idx_q_lim_v
            
            # 1. BARRA OPERANDO COMO PQ -> Verifica a violação dos limites de tensão
            if esta_como_pq:
                if ((QgeracaoPu - tlpr) >= qmin) and ((QgeracaoPu + tlpr) <= qmax):
                    if (vcal + tlvc) < vmin:
                        idx_q.remove(idx)
                        idx_q_lim_v.remove(idx)
                        idx_q.sort()
                        v_cal[idx] = vmin
                        trocas     += 1
                        
                    elif (vcal - tlvc) > vmax:
                        idx_q.remove(idx)
                        idx_q_lim_v.remove(idx)
                        idx_q.sort()
                        v_cal[idx] = vmax
                        trocas     += 1
            
            # 2. BARRA SATURADA COMO PV -> Verifica se pode voltar para PQ
            else:
                travada_no_max = np.isclose(vcal, vmax)
                travada_no_min = np.isclose(vcal, vmin)
                
                if travada_no_max and ((QgeracaoPu + tlpr) < qmin):
                    idx_q.append(idx)
                    idx_q_lim_v.append(idx)
                    idx_q.sort()
                    Q_esp[idx] = (qmin - q_carga_pu[idx]) 
                    trocas     += 1
                    
                elif travada_no_min and ((QgeracaoPu - tlpr) > qmax):
                    idx_q.append(idx)
                    idx_q_lim_v.append(idx)
                    idx_q.sort()
                    Q_esp[idx] = (qmax - q_carga_pu[idx]) 
                    trocas     += 1
                    
        return trocas     
        
    
    
    def q_cal(self, bmva, tipo_bar: str):
        data      = self.net.data
        dbar      = self.net.DadosRede.dbarDF
        
        v_pu    = np.asarray(data.v, dtype=np.float64)
        ang_rad = np.asarray(data.t, dtype=np.float64)
        
        v_complex = v_pu * np.exp(1j * ang_rad)
        i_complex = data.Ybus_csr @ v_complex 
        s_inj_pu = (v_complex * np.conj(i_complex)) 
        
        q_inj_pu     = s_inj_pu.imag 
        q_carga_pu   = dbar["carga_reativa"].to_numpy(dtype=np.float64, copy=True) / bmva        
        tipo_barra   = dbar["tipo"].to_numpy()
        
        q_geracao_pu = dbar["geracao_reativa"].to_numpy(dtype=np.float64, copy=True)
        
        if tipo_bar == "pv":
            mask_pv = tipo_barra == "pv"
            
            q_geracao_pu[mask_pv] = (
                q_inj_pu[mask_pv] + q_carga_pu[mask_pv] 
            )
            
        elif tipo_bar == "pq":
            mask_pq = tipo_barra == "pq"
                    
            q_geracao_pu[mask_pq] = (
                q_inj_pu[mask_pq] + q_carga_pu[mask_pq] 
            )
            
        return q_geracao_pu
    
    

    
    
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
        
        
        
        
        
        