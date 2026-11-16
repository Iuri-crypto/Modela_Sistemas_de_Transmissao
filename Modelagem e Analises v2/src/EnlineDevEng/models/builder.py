

from typing import Any
import pandas as pd
from EnlineDevEng.core.adm import BaseNetworkBuilder

from scipy.sparse import dok_matrix
import cmath 
import numpy as np
import math 

    

class NetworkBuilder(BaseNetworkBuilder):
    
    """
    Lê os dataframes crus do objeto 'net', mapeia
    topologia, calcula impedâncias/admitâncias e 
    gera a matriz Ybus esparsa
    """
    
    
    def __init__(
        self,
        net: Any,
        ede: Any,
        data: Any
    ):
        self.net = net 
        self.ede = ede 
        self.data = data
    
    
    
    @classmethod
    def build(
        cls,
        net: Any,
        ede: Any,
        data: Any
    ):
        """
        Ponto de entrada público. Mantém a assinatura estática
        mas delega todo o processamento para uma instância isolada.
        """
        
        builder = cls(net=net, ede=ede, data=data)
        return builder._build()
    
    
    def _build(
        self
    ):
        self.apply_bus_map()                                         
        self.write_num_buses()
        self.write_vtheta_initial()
        self.write_S_esp()
        self.write_bus_types()                                      
        
        # --- --- --- --- --- --- --- --- --- --- --- --- 
        # 1 - Montagem da Ybus
        # --- --- --- --- --- --- --- --- --- --- --- --- 
        self.create_ybus()
        
        # --- --- --- --- --- --- --- --- --- --- --- --- 
        # 2 - Salvando toda a estrutura de dados 
        # (dados para o solver especificadamente)
        # no objeto principal: net
        # --- --- --- --- --- --- --- --- --- --- --- ---
        self.net.data = self.data 
        
        
    
    def create_ybus(
        self
    ):
        self.write_Ybus_initial() 
        s_mva    = self.net.DadosRede.cte["BMVA"]
        
        
        # Contribuição das LTs
        for _, dados in self.net.line.iterrows():
            if dados["in_service"] == False: continue
            

            akm         = 1                    # tap da LT
            Phikm       = 0                    # defasagem da LT
                            
            k           = dados["from_bus"] 
            m           = dados["to_bus"]  
            r_km        = dados["r_percent"] / 100         # pu
            x_km        = dados["x_percent"] / 100         # pu
            bsh_km      = dados["b_percent"] / (s_mva * 2) # pu
            
            y_km        = 1.0 / complex(r_km, x_km)
                            
            self.data.Ybus[k, m] += - akm * cmath.exp(-1j * Phikm) * y_km # Ykm 
            self.data.Ybus[m, k] += - akm * cmath.exp( 1j * Phikm) * y_km # Ymk 

            self.data.Ybus[m, m] += 1j * bsh_km + akm**2 * y_km   # Ykk 
            self.data.Ybus[k, k] += 1j * bsh_km + y_km            # Ymm 
        
        
        # Contribuição dos Trafos
        for _, dados in self.net.trafo.iterrows():      
            if dados["in_service"] == False: continue
            
                                            
            k           = dados["from_bus"] 
            m           = dados["to_bus"]            
            r_km        = dados["r_percent"] / 100         # pu
            x_km        = dados["x_percent"] / 100         # pu
            bsh_km      = dados["b_percent"] / (s_mva * 2) # pu
            Phikm       = dados["shift_degree"]            # Defasagem em graus
            akm         = dados["tap_pos"]                 # posição atual do tap
            
            Phikm       = math.radians(Phikm)
            y_km        = 1.0 / complex(r_km, x_km)
            
            self.data.Ybus[k, m] += - akm * cmath.exp(-1j * Phikm) * y_km # Ykm 
            self.data.Ybus[m, k] += - akm * cmath.exp( 1j * Phikm) * y_km # Ymk 

            
            self.data.Ybus[m, m] += 1j * bsh_km + akm**2 * y_km   # Ykk 
            self.data.Ybus[k, k] += 1j * bsh_km + y_km            # Ymm 
        
        
        # Contribuição do Shunt de barra (capacitores/reatores -> FIXOS E CHAVEADOS APENAS!!!)
        for _, dados in self.net.shunt.iterrows():      
            if dados["in_service"] == False: continue
            
                                            
            k           = dados["bus"] 
            bsh_k       = dados["q_mvar"] / s_mva # [pu]                  
            
            self.data.Ybus[k, k] += 1j * bsh_k 
        
        
        # Conversão para estrutura esparça
        self.data.Ybus_csr = self.Ybus_CSR()                          
            
            

    
    def bus_order(
       self
    ):
        ids = []
        for _, data in self.net.bus.iterrows():
            ids.append(data["numero"])
            
        for i in range(len(ids)):
            self.data.bus_map[ids[i]] = i
    
    
    def apply_bus_map(
        self
    ):
        self.bus_order()
        bus_map                    = self.data.bus_map
        self.net.bus["numero"]     = self.net.bus["numero"].map(bus_map)
        self.net.load["bus"]       = self.net.load["bus"].map(bus_map)
        self.net.gen["bus"]        = self.net.gen["bus"].map(bus_map)
        self.net.shunt["bus"]      = self.net.shunt["bus"].map(bus_map)
        self.net.line["from_bus"]  = self.net.line["from_bus"].map(bus_map)
        self.net.line["to_bus"]    = self.net.line["to_bus"].map(bus_map)
        self.net.trafo["from_bus"] = self.net.trafo["from_bus"].map(bus_map)
        self.net.trafo["to_bus"]   = self.net.trafo["to_bus"].map(bus_map)


    def write_bus_types(
        self
    ):
        self.data.bus_type = self.net.bus["tipo"]
        self.data.pq_idx = self.net.bus.loc[self.net.bus["tipo"] == "pq", "numero"].to_numpy(dtype=int)
        self.data.pv_idx = self.net.bus.loc[self.net.bus["tipo"] == "pv", "numero"].to_numpy(dtype=int)
        self.data.vt_idx = self.net.bus.loc[self.net.bus["tipo"] == "vt", "numero"].to_numpy(dtype=int)
        
    
    def write_num_buses(
        self
    ):
        self.data.num_buses = len(self.net.bus)
    
    
    def write_vtheta_initial(
        self
    ):
        self.data.v = self.net.bus["vn"].to_numpy(dtype=float) / 1000
        self.data.t = np.zeros_like(self.data.v, dtype=float)
        
    def write_Ybus_initial(
        self
    ):
        num_buses = len(self.net.bus)
        self.data.Ybus = dok_matrix((num_buses, num_buses), dtype=complex)
        
    
    def Ybus_CSR(
        self
    ):
        return self.data.Ybus.tocsr()
    
        
        
    def write_S_esp(
        self
    ):
        s_mva    = self.net.DadosRede.cte["BMVA"]
        num_buses = len(self.net.bus)
        
        p_load = np.zeros(num_buses, dtype=float)
        q_load = np.zeros(num_buses, dtype=float)

        cargas = self.net.load
        np.add.at(p_load, cargas["bus"].to_numpy(dtype=int), cargas["p_mw"].to_numpy(dtype=float))
        np.add.at(q_load, cargas["bus"].to_numpy(dtype=int), cargas["q_mvar"].to_numpy(dtype=float))

        p_gen = np.zeros(num_buses, dtype=float)
        q_gen = np.zeros(num_buses, dtype=float)

        geradores = self.net.gen
        np.add.at(p_gen, geradores["bus"].to_numpy(dtype=int), geradores["p_mw"].to_numpy(dtype=float))
        # np.add.at(q_gen, geradores["bus"].to_numpy(dtype=int), geradores["q_mvar"].to_numpy(dtype=float))

        # Potência complexa líquida em pu
        S_esp = ((p_gen - p_load) + 1j * (q_gen - q_load)) / s_mva
        self.data.S_esp = S_esp
        
    

        
        
    
        
        
    