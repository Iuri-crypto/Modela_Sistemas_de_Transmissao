

from EnlineDevEng.utils.auxiliary import EnlineDevEngNet
from EnlineDevEng.core.adm import Base__NetworkFileBuilder
import EnlineDevEng 
import pandas as pd
from numpy import nan


class PWFInjectorBuilder(Base__NetworkFileBuilder):
    
    """
    Lê a estrutura 'net.DadosRede' (extraída pelo PWFNetworkParser)
    e injeta automaticamente os elementos via 'ede.create_' do EnlineDevEng.
    """
    
    extensions = ["pwf"]
    
    def network_build(
        self, 
        net: EnlineDevEngNet, 
        ede: EnlineDevEng,
        add_disable_elements: bool = False
    ):
        
        """
        Popula o objeto 'net' com todas as tabelas extraídas
        do PWF.
        """
        
        DadosRede = net.DadosRede
        
        # DADOS DE BARRA DO ANAREDE
        if not DadosRede.dbarDF.empty:
            self._inject_bus_AC(net, ede, DadosRede.dbarDF, add_disable_elements)
            self._inject_balanced_load(net, ede, DadosRede.dbarDF, add_disable_elements)
            self._inject_balanced_generation(net, ede, DadosRede.dbarDF, add_disable_elements)
            self._inject_bus_shunt(net, ede, DadosRede.dbarDF, add_disable_elements)
        
        
        if not DadosRede.dlinDF.empty:
            self._inject_line_AC(net, ede, DadosRede.dlinDF, add_disable_elements)
            self._inject_transformer(net, ede, DadosRede.dlinDF, add_disable_elements)
            
        
        # elif not DadosRede.dshlDF.empty:
        #     self._inject_line_shunt(net, ede, DadosRede.dbarDF, add_disable_elements)
        
        
        # elif not DadosRede.dcerDF.empty:
        #     self._inject_statcom(net, ede, DadosRede.dbarDF, add_disable_elements)
                    
        
        
    
    def _inject_bus_AC(
        self, 
        net: EnlineDevEngNet,
        ede: EnlineDevEng,
        df: pd.DataFrame,
        add_disable_elements: bool = True
    ):
        """
        Cria os barramentos AC
        """
        
        for _, dados in df.iterrows():
            
            vn               = dados["tensao"]
            numero           = dados["numero"]
            tipo             = dados["tipo"]
            barra_controlada = dados["barra_controlada"]
            in_service       = dados["estado"]
            
            # Barra em Operação
            in_service = True if in_service == "L" else False
            if not add_disable_elements and not in_service: continue
            
            ede.create_bus(
                net=net,
                vn=vn,
                numero=numero,
                tipo=tipo,
                barra_controlada=barra_controlada,
                in_service=in_service
            )
    
    
    def _inject_balanced_load(
        self, 
        net: EnlineDevEngNet,
        ede: EnlineDevEng,
        df: pd.DataFrame,
        add_disable_elements: bool = False
    ):
        """
        """
        
        for _, dados in df.iterrows():
                    
            bus        = dados["numero"]
            p_mw       = dados["carga_ativa"]
            q_mvar     = dados["carga_reativa"]
            in_service = dados["estado"]
            tipo       = dados["tipo"]
            
            if tipo != "pq": continue
            
            # Carga em Operação ?
            in_service = True if in_service == "L" else False
            if not add_disable_elements and not in_service: continue
            
            ede.create_load(
                net=net,
                bus=bus,
                q_mvar=q_mvar,
                p_mw=p_mw,
                in_service=in_service
            )
            
    
    def _inject_balanced_generation(
        self, 
        net: EnlineDevEngNet,
        ede: EnlineDevEng,
        df: pd.DataFrame,
        add_disable_elements: bool = False
    ):
        """
        """
        
        for _, dados in df.iterrows():
                            
            bus        = dados["numero"]
            p_mw       = dados["geracao_ativa"]
            vm         = dados["tensao"]
            in_service = dados["estado"]
            pf         = dados["fator_de_potencia_nominal"]
            tipo       = dados["tipo"]
                     
            if tipo != "pv": continue
            
            # Gerador em Operação ?
            in_service = True if in_service == "L" else False
            if not add_disable_elements and not in_service: continue
            
            
            # Potência aparente
            sn_mva = p_mw / pf
            
            ede.create_gen(
                net=net,
                bus=bus,
                p_mw=p_mw,
                vm=vm,
                sn_mva=sn_mva,
                in_service=in_service
            )
        
            
    def _inject_bus_shunt(
        self,
        net: EnlineDevEngNet, 
        ede: EnlineDevEng,
        df: pd.DataFrame,
        add_disable_elements: bool = False
    ):
        """
        """
        
        for _, dados in df.iterrows():
                           
            bus        = dados["numero"]
            q_mvar     = dados["capacitor_reator"]
            vn         = dados["tensao"]
            in_service = dados["estado"]
            
            if q_mvar == 0.0: continue
                    
            # Shunt em operação ?
            in_service = True if in_service == "L" else False
            if not add_disable_elements and not in_service: continue
            
            ede.create_shunt(
                net=net,
                bus=bus,
                q_mvar=q_mvar,
                vn=vn,
                in_service=in_service
            )
                
            
            
    def _inject_line_AC(
        self,
        net: EnlineDevEngNet,
        ede: EnlineDevEng,
        df: pd.DataFrame, 
        add_disable_elements: bool = False
    ):
        """
        """
        
        for _, dados in df.iterrows():
                            
            from_bus   = dados["da_barra"]
            to_bus     = dados["para_barra"]
            r_percent  = dados["resistencia"]
            x_percent  = dados["reatancia"]
            b_percent  = dados["susceptancia"]
            in_service = dados["estado"]
            tap        = dados["tap"]
            
            if pd.notna(tap): continue
                        
            in_service = True if in_service == "L" else False
            if not add_disable_elements and not in_service: continue
            
            ede.create_line(
                net=net,
                from_bus=from_bus,
                to_bus=to_bus,
                length_km=1.0,
                r_percent=r_percent,
                x_percent=x_percent,
                b_percent=b_percent,
                in_service=in_service
            )
                    
            
    def _inject_transformer(
        self, 
        net: EnlineDevEngNet, 
        ede: EnlineDevEng,
        df: pd.DataFrame, 
        add_disable_elements: bool = False
    ):
        """
        """
        
        for _, dados in df.iterrows():
                            
            from_bus   = dados["da_barra"]
            to_bus     = dados["para_barra"]
            r_percent  = dados["resistencia"]
            x_percent  = dados["reatancia"]
            b_percent  = dados["susceptancia"]
            shift_degree = dados["defasagem"]
            tap_min    = dados["tap_minimo"]
            tap_max    = dados["tap_maximo"]
            tap        = dados["tap"]
            num_taps   = dados["numero_de_taps"]
            barra_controlada = dados["barra_controlada"]
            in_service = dados["estado"]
            
            if pd.isna(tap): continue
                        
            # Trafo em Operação ?
            in_service = True if in_service == "L" else False
            if not add_disable_elements and not in_service: continue
            
            ede.create_trafo(
                net=net,
                from_bus=from_bus,
                to_bus=to_bus,
                r_percent=r_percent,
                x_percent=x_percent,
                b_percent=b_percent,
                shift_degree=shift_degree,
                tap_min=tap_min,
                tap_max=tap_max,
                tap_pos=tap,
                num_taps=num_taps,
                barra_controlada=barra_controlada,
                in_service=in_service
            )
                    
        
    # def _inject_line_shunt(self, net: EnlineDevEngNet, ede: EnlineDevEng,
    #                              df: pd.DataFrame, add_disable_elements: bool = False):
    #     """
    #     """
        
    #     for _, dados in df.iterrows:
                            
    #         bus        = dados["numero"]
    #         p_mw       = dados["carga_ativa"]
    #         q_mvar     = dados["carga_reativa"]
    #         in_service = dados["estado"]
                        
    #         in_service = True if in_service == "L" else False
    #         if not add_disable_elements and not in_service: continue
            
    #         ede.create_load(
    #             net=net,
    #             bus=bus,
    #             q_mvar=q_mvar,
    #             p_mw=p_mw,
    #             in_service=in_service
    #         )
        
    
    
    # def _inject_statcom(self, net: EnlineDevEngNet, ede: EnlineDevEng,
    #                              df: pd.DataFrame, add_disable_elements: bool = False):
    #     """
    #     """
        
    #     for _, dados in df.iterrows:
                            
    #         bus        = dados["numero"]
    #         p_mw       = dados["carga_ativa"]
    #         q_mvar     = dados["carga_reativa"]
    #         in_service = dados["estado"]
                        
    #         in_service = True if in_service == "L" else False
    #         if not add_disable_elements and not in_service: continue
            
    #         ede.create_load(
    #             net=net,
    #             bus=bus,
    #             q_mvar=q_mvar,
    #             p_mw=p_mw,
    #             in_service=in_service
    #         )
            
                
    