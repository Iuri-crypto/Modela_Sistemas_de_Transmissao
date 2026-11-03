


import sys
from pathlib import Path 

DIRETORIO_RAIZ = Path(__file__).resolve().parent.parent 
if str(DIRETORIO_RAIZ) not in sys.path:
    sys.path.insert(0, str(DIRETORIO_RAIZ))
    
import pandapower as pp 
import pandapower.control  as control
import pandas as pd
import numpy as np
import math

from pwf_to_df.source.main import leitor_pwf

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)




class FluxoPotencia:
    def __init__(
            self, saida_simulacoes="resultados",
            salvar_dados_barra=False,
            salvar_dados_linha=False,
            snapshot=True
        ):
        
        self.pasta_simulacoes = saida_simulacoes
        self.salvar_dados_barra = salvar_dados_barra
        self.salvar_dados_linha = salvar_dados_linha
        self.snapshot = snapshot
        
        
    def fluxo_de_potencia(
        self, net: pp.pandapowerNet = None
    ):
        if self.snapshot:
            pp.runpp(
                    net,
                    algorithm="nr",
                    calculate_voltage_angles=True,
                    #max_iteration=100,
                    #tolerance_mva=1e-6,
                    #run_control=False,
                    #distributed_slack=False, 
                    #enforce_p_lims=False, 
                    #enforce_q_lims=False,
                )
            
        if self.salvar_dados_barra:
            df = self.relatorio_debar(net)
            
            self.salvar_resultados(
                    df,
                    self.pasta_simulacoes,
                    tipo="dbar",
                    extensao="xlsx",
                )
            
        # if self.salvar_dados_linha:
        #     self.relatorio_delin(net)
            
    
    def relatorio_debar(
        self, net
    ):
        res_bus = net.res_bus.copy()
        bus_info = net.bus.copy()
        
        df_barras = pd.DataFrame({
            "Barra": bus_info.index,
            "Nome": bus_info["name"] if "name" in bus_info.columns else "",
            "V_kV_Nominal": bus_info["vn_kv"],
            "V_pu": res_bus["vm_pu"],
            "V_kV_Operacao": res_bus["vm_pu"] * bus_info["vn_kv"],
            "Angulo_graus": res_bus["va_degree"]
        })
        return df_barras
        
        
    # def relatorio_delin(self, net):
    #     pass 
    
    
    def salvar_resultados(
        self, df: pd.DataFrame, pasta: str, tipo: str, extensao: str
    ):
        dir_ = Path(__file__).resolve().parent / pasta 
        dir_.mkdir(parents=True, exist_ok=True)
        dir_ = dir_ / f"{tipo}.{extensao}"
        
        if extensao == "xlsx":
            df.to_excel(dir_, index=False, engine="openpyxl")
        
    
class DadosRede:
    def __init__(self):
        self.dir_output = Path(__file__).resolve().parent.parent / "pwf_to_df" / "output"
        self.dataframes = {}
    
    
    def CarregaDados(self):
        # chama o código de leitura do pwf
        leitor_pwf()
        
        # agora carrega os arquivos
        for arquivo in self.dir_output.glob("*.xlsx"):
            if arquivo.name.startswith("~$"): 
                continue 
            
            self.dataframes[arquivo.stem] = pd.read_excel(arquivo)
            print(f"\033[91mCarregado: {arquivo.name}\033[0m")
            


class CriarRede(DadosRede, FluxoPotencia):
    """
    Elementos Modelados:
        1 - Barra CA
        2 - Linha CA
        3 - Carga
        4 - Gerador
        5 - Transformador 
        6 - Shunt (capacitor/reator) tanto de barra quanto de linha
        7 - Compensador estático de reativos
    """
    def __init__(self,
            saida_simulacoes="resultados",
            salvar_dados_barra=False,
            salvar_dados_linha=False,
            snapshot=True
            ):

        DadosRede.__init__(self)
        FluxoPotencia.__init__(
            self,
            saida_simulacoes=saida_simulacoes,
            salvar_dados_barra=salvar_dados_barra,
            salvar_dados_linha=salvar_dados_linha,
            snapshot=snapshot,
        )
        self.rede = None
        
    
    def despachar_modelagem(self):
        
        # Modelagem
        self.CarregaDados()
        self.inicializar_rede()
        for nome_df, df in self.dataframes.items():
            
            if nome_df.split(".")[0] == "dbarDF":
                self.Barra_CA(df)
                self.Carga_Simetrica(df)
                self.Geracao_Simetrica(df)
                self.Shunt_barra(df)
            
            elif nome_df.split(".")[0] == "dcerDF":
                self.CompensadorEstaticoReativo(df)
                
            elif nome_df.split(".")[0] == "dlinDF":
                self.Linhas_CA(df)
                self.Transformador(df)
                
            elif nome_df.split(".")[0] == "dshlDF":
                self.Shunt_linha(df)
                
    
        return self.rede 
    
    def inicializar_rede(self):
        self.rede = pp.create_empty_network()
        
        
    def Barra_CA(self, df: pd.DataFrame):
        """ Modelagem de barramento CA 
        
        >> Código de execução Implementados: DBAR, DGBT, DGLT
        >> Não implementados: 
        """
        
        dgbtDF = self.dataframes.get("dgbtDF")
        dgltDF = self.dataframes.get("dgltDF")
        
        for _, linha in df.iterrows():
            
            numero = int(linha["numero"])   # Esta coluna é obrigatória    
            estado = str(linha["estado"])
            grupo_base_tensao = str(linha["grupo_base_tensao"])
            nome = str(linha["nome"])       # Esta coluna é obrigatória
            grupo_limite_tensao = str(linha["grupo_limite_tensao"])
            area = str(linha["area"])       # Esta coluna é obrigatória
            
        
            if estado == "0":
                estado = True
            else:
                estado = self.estado(estado)

            try:
                filtro = dgbtDF[dgbtDF["grupo_base_tensao"] == grupo_base_tensao]
                vn_kv = float(filtro["tensao"].values[0])
                if vn_kv == 0.0:
                    vn_kv = 1.0
            except Exception as e:
                vn_kv = 1.0 # padrão anarede
            
            try:
                filtro = dgltDF[dgltDF["grupo_limite_tensao"] == grupo_limite_tensao]
                max_vm_pu = float(filtro["limite_maximo"].values[0])
                min_vm_pu = float(filtro["limite_minimo"].values[0])
                
                if max_vm_pu == 0.0: 
                    max_vm_pu = 1.05
                if min_vm_pu == 0.0:
                    min_vm_pu = 0.95
            except Exception as e:
                max_vm_pu = 1.05
                min_vm_pu = 0.95
            
         
            pp.create_bus(net=self.rede, 
                        vn_kv=vn_kv, 
                        name=nome,
                        index=numero,
                        #type="b",
                        #zone=area,
                        in_service=estado,
                        #max_vm_pu=max_vm_pu,
                        #min_vm_pu=min_vm_pu
                        )
            
            
    def Carga_Simetrica(self, df: pd.DataFrame):
        """Modelagem de Cargas Equilibradas 
        
        >> Código de execução implementados: DBAR
        >> Não implementados: DCAR, DANC, DINC, DAGR
        """
        for _, linha in df.iterrows():
            
            numero = int(linha["numero"]) # Esta coluna é obrigatória
            estado = str(linha["estado"])       
            demanda_ativa = float(linha["demanda_ativa"]) # Esta coluna é obrigatória
            demanda_reativa = float(linha["demanda_reativa"]) # Esta coluna é obrigatória
            
            
            if estado == "0":
                estado = True
            else:
                estado = self.estado(estado)
                
            
            if demanda_ativa == 0.0 and demanda_reativa == 0.0:
                continue 
            
            pp.create_load(self.rede, 
                            bus=numero,
                            p_mw=demanda_ativa,
                            q_mvar=demanda_reativa,
                            #in_service=estado
                            )
            
            
    def Geracao_Simetrica(self, df: pd.DataFrame):
        """ Modelagem de Geradores 
        
        >> Código de execução implementados: DBAR, DGER
        >> Não implementados: DAGA, DAEB, DCTG, DINJ
        """
        dgerDF = self.dataframes.get("dgerDF")
        
        for _, linha in df.iterrows():
            numero = int(linha["numero"]) # Esta coluna é obrigatória
            estado = str(linha["estado"]) 
            tipo = str(linha["tipo"])     # Esta coluna é obrigatória
            tensao = float(linha["tensao"]) 
            potencia_ativa = float(linha["potencia_ativa"]) # Esta coluna é obrigatória
            slack = None
            
            try:
                filtro = dgerDF[dgerDF["numero"] == numero]
                potencia_ativa_minima = float(filtro["potencia_ativa_minima"].values[0])
                potencia_ativa_maxima = float(filtro["potencia_ativa_maxima"].values[0])
                fator_participacao = float(filtro["fator_participacao"].values[0])
                fator_potencia_nominal = float(filtro["fator_potencia_nominal"].values[0])
                reatancia_maquina = float(filtro["reatancia_carga"].values[0])
                
               
                if fator_potencia_nominal == 0.0:
                    fator_potencia_nominal = 1
                if reatancia_maquina == 0.0:
                    reatancia_maquina = np.nan
                potencia_reativa_maxima = 99999 # padrão anarede
                potencia_reativa_minima = 0.0 # padrão anarede
            except Exception as e:
                fator_participacao = 0.0 # padrão anarede
                reatancia_maquina  = np.nan
                potencia_reativa_maxima = 99999 # padrão anarede
                potencia_reativa_minima = 0.0 # padrão anarede
                fator_potencia_nominal = 1
            
           
            if estado == "0":
                estado = True
                
            else:
                estado = self.estado(estado)
            
            if tensao in (0, 0.0):
                tensao = 1 # 1.0 pu
            else:
                tensao = tensao / 1000
                     
                        
            if tipo == "1":
                slack = False
                pp.create_gen(self.rede,
                                bus=numero,
                                p_mw=potencia_ativa,
                                vm_pu=tensao,
                                #slack_weight=fator_participacao,
                                #xdss_pu=reatancia_maquina,
                                #in_service=estado,
                                #max_p_mw=potencia_ativa_maxima,
                                #min_p_mw=potencia_ativa_minima,
                                max_q_mvar=999,
                                min_q_mvar=-999,
                                #cos_phi=fator_potencia_nominal,
                                #slack=slack
                            )
                
            elif tipo == "2":
                slack = True 
                pp.create_ext_grid(
                    self.rede, bus=numero, vm_pu=tensao, va_degree=0.0, name="Slack"
                )
                
            elif tipo == "0":
                continue 
            
            
            
        
            
            
    def Linhas_CA(self, df: pd.DataFrame):
        """Modelagem de linhas CA.
                    
        >> Código de Execução implementados: DLIN, DCTE, DBAR, DGBT, DCNV
        >> Não implementados: 
        """
        
        dcteDF = self.dataframes.get("dcteDF")
        dbarDF = self.dataframes.get("dbarDF")
        dgbtDF = self.dataframes.get("dgbtDF")
        dcnvDF = self.dataframes.get("dcnvDF")
        i = 0
        
        for _, linha in df.iterrows():
            de = int(linha["de"])                       # Esta coluna é obrigatória
            abertura_de = str(linha["abertura_de"])
            abertura_para = str(linha["abertura_para"])
            para = int(linha["para"])                  # Esta coluna é obrigatória
            estado = str(linha["estado"])
            resistencia = float(linha["resistencia"])  # Esta coluna é obrigatória
            reatancia = float(linha["reatancia"])      # Esta coluna é obrigatória
            susceptancia = float(linha["susceptancia"])   # Esta coluna é obrigatória
            capacidade_normal = float(linha["capacidade_normal"]) # MVA
            tap = float(linha["tap"]) # Esta coluna é obrigatória
            
            if tap not in (0, 0.0):
                continue # é trafo
            
            
            if abertura_de == "0":
                abertura_de = True 
            else:
                abertura_de = True if abertura_de == "L" else False
                
            if abertura_para == "0":
                abertura_para = True 
            else:
                abertura_para = True if abertura_para == "L" else False
                            
            if estado == "0":
                estado = True
            else:
                estado = self.estado(estado)
                            
                            
            try:
                linha = dcteDF[dcteDF["constante"] == "BASE"]
                MVA_BASE = float(linha["valor_constante"].values[0])
                if MVA_BASE == 0.0:
                    MVA_BASE = 100.0
            except Exception as e:
                MVA_BASE = 100.0
            
            try:
                linha2 = dbarDF[dbarDF["numero"] == de]
                grupo_base_tensao = linha2["grupo_base_tensao"].values[0]
                filtro = dgbtDF[dgbtDF["grupo_base_tensao"] == grupo_base_tensao]
                kV_BASE = float(filtro["tensao"].values[0])
                if kV_BASE == 0.0:
                    kV_BASE = 1.0
            except Exception as e:
                kV_BASE = 1.0
            
            
            try:
                f = float(dcnvDF["frequencia"].values[0])
                if f == 0.0:
                    f = 60
            except Exception as e:
                f = 60.0
                
              
            # Impedância Base e Admitância Base
            Z_BASE = kV_BASE**2 / MVA_BASE
            Y_BASE = 1 / Z_BASE
            
            r_total_ohm = (resistencia * Z_BASE) / 100
            x_total_ohm = (reatancia * Z_BASE) / 100
            b_total_ohms = (susceptancia * Y_BASE) / 100
            c_total_ohm = (b_total_ohms * 1e9) / (2 * math.pi * f)
            
            capacidade_normal = capacidade_normal if capacidade_normal not in (0, 0.0) else 99999 # MVA
            max_i_ka_norm = capacidade_normal / (math.sqrt(3) * kV_BASE)
                            
            
            pp.create_line_from_parameters(
                net=self.rede,
                from_bus=de,
                to_bus=para,
                length_km=1.0,
                r_ohm_per_km=r_total_ohm,
                x_ohm_per_km=x_total_ohm,
                c_nf_per_km=c_total_ohm,
                max_i_ka=1.0,
                #type="ol",
                in_service=estado,
                #parallel=False
                )
            
        
            pp.create_switch(net=self.rede,
                                bus=de,
                                element=i,
                                et="l",
                                closed=abertura_de,
                                type="CB"
                                )
            
            
                
            pp.create_switch(net=self.rede,
                            bus=para,
                            element=i,
                            et="l",
                            closed=abertura_para,
                            type="CB"
                            )
        
            i += 1
    
    def Transformador(self, df: pd.DataFrame):
        """Modelagem de Transformador.
                    
        >> Código de Execução Implementados: DLIN, DCTE, DBAR, DGBT, DCTR
        >> Não Implementados: DCNV
        """
        
        dcteDF = self.dataframes.get("dcteDF")
        dbarDF = self.dataframes.get("dbarDF")
        dgbtDF = self.dataframes.get("dgbtDF")
        dcnvDF = self.dataframes.get("dcnvDF")
        dctrDF = self.dataframes.get("dctrDF")
        

        for _, linha in df.iterrows():
            de = int(linha["de"])       # Esta coluna é obrigatória
            abertura_de = str(linha["abertura_de"])
            abertura_para = str(linha["abertura_para"])
            para = int(linha["para"])   # Esta coluna é obrigatória
            estado = str(linha["estado"])
            manobravel = str(linha["manobravel"])
            resistencia = float(linha["resistencia"]) # Esta coluna é obrigatória
            reatancia = float(linha["reatancia"])    # Esta coluna é obrigatória
            tap = float(linha["tap"])     # Esta coluna é obrigatória
            tap_minimo = float(linha["tap_minimo"])
            tap_maximo = float(linha["tap_maximo"])
            tap_defasagem = float(linha["tap_defasagem"])
            capacidade_normal = float(linha["capacidade_normal"]) # MVA
            
            if tap in (0, 0.0):
                continue # é lt
            
            
            if abertura_de == "0":
                abertura_de = True 
            else:
                abertura_de = True if abertura_de == "L" else False
                
            if abertura_para == "0":
                abertura_para = True 
            else:
                abertura_para = True if abertura_para == "L" else False
                
            try:
                linha = dcteDF[dcteDF["constante"] == "BASE"]
                MVA_BASE = float(linha["valor_constante"].values[0])
                if MVA_BASE == 0.0:
                    MVA_BASE = 100.0
            except Exception as e:
                MVA_BASE = 100.0
            
            try:
                linha2 = dbarDF[dbarDF["numero"] == de]
                grupo_base_tensao = linha2["grupo_base_tensao"].values[0]
                filtro = dgbtDF[dgbtDF["grupo_base_tensao"] == grupo_base_tensao]
                kV_BASE_primario = float(filtro["tensao"].values[0])
                
                linha3 = dbarDF[dbarDF["numero"] == para]
                grupo_base_tensao = linha3["grupo_base_tensao"].values[0]
                filtro = dgbtDF[dgbtDF["grupo_base_tensao"] == grupo_base_tensao]
                kV_BASE_secundario = float(filtro["tensao"].values[0])
            except Exception as e:
                kV_BASE_primario = 1.0
                kV_BASE_secundario = 1.0

                

            capacidade_normal = capacidade_normal if capacidade_normal not in (0, 0.0, "0", "0.0") else 500 # MVA   
            
            if estado == "0":
                estado = True                         
            else:
                estado = self.estado(estado)
            
            # Mudança de base (anararede -> trafo)
            Z_percentual = math.sqrt(resistencia**2 + reatancia**2)
            
            pfe_kw = 2 * capacidade_normal**0.7
            io_percent = 1 / (capacidade_normal**0.3)
        
            # Se esta coluna estiver prenchida então é trafo
            
            trafo_idx = pp.create_transformer_from_parameters(net=self.rede,
                                                hv_bus=de, # barra de alta tensão
                                                lv_bus=para, # barra de baixa tensão
                                                sn_mva=100, # potência aparente nominal
                                                vn_hv_kv=kV_BASE_primario, # Tensão nominal na alta tensão
                                                vn_lv_kv=kV_BASE_secundario, # Tensão nominal na baixa tensão
                                                pfe_kw=pfe_kw, # perdas no ferro kW
                                                i0_percent=io_percent, # corrente a vazio
                                                #vector_group=None, # grupo de ligação
                                                #shift_degree=tap_defasagem, # defasagem entre primário e secundário
                                                #tap_side="lv", # lado do comutador de taps
                                                tap_neutral=1.0, # posição neutra do tap
                                                #tap_max=tap_maximo,
                                                #tap_min=tap_minimo,
                                                tap_pos=tap, # posição atual do tap
                                                #tap_changer_type="Ratio", # especifica o tipo de comutador
                                                in_service=estado,
                                                #oltc=True,
                                                vk_percent=Z_percentual,
                                                vkr_percent=resistencia,
                                                tap_step_percent=0.625
                                                )
            
            
            automatico = True if manobravel in ("A", "0", "0.0") else False  
            if automatico:
                try:
                    linha = dctrDF[dctrDF["de"] == de]
                    de_t = linha["de"].values[0]
                    para_t = linha["para"].values[0]
                    
                    if (de_t == de) and (para_t == para):
                        vminpu = linha["tensao_minima"].values[0]
                        vmaxpu = linha["tensao_maxima"].values[0]
                        control.DiscreteTapControl(net=self.rede,
                                                element_index=trafo_idx,
                                                vm_lower_pu=vminpu,
                                                vm_upper_pu=vmaxpu,
                                                side="lv",
                                                element="trafo",
                                                tol=0.001,
                                                in_service=estado,
                                            
                                                )
                except Exception:
                    pass 
        
                            
            pp.create_switch(net=self.rede,
                            element=trafo_idx,
                            bus=de,
                            et="t",
                            closed=abertura_de,
                            type="CB"
                            )
            
            pp.create_switch(net=self.rede,
                            element=trafo_idx,
                            bus=para,
                            et="t",
                            closed=abertura_para,
                            type="CB"
                            )
                
    
    def Shunt_linha(self, df: pd.DataFrame):
        """Este bloco permite associar dispositivos shunt
        a elementos da rede.
                    
        Exemplo:
            >> Código de Execução Implementado: DSHL 
            >> Não implementados:
        """
        for _, linha in df.iterrows():
            from_ = int(linha["from"])
            to = int(linha["to"])
            shunt_from = float(linha["shunt_from"])
            shunt_to = float(linha["shunt_to"])
            estado_shunt_from = str(linha["estado_shunt_from"])
            estado_shunt_to = str(linha["estado_shunt_to"])
            
            
            if shunt_to==0.0 and shunt_from==0.0:
                continue 
            
             
            if estado_shunt_from == "0":
                estado_shunt_from = "L"
                
            if estado_shunt_to == "0":
                estado_shunt_to = "L"
            
            if estado_shunt_from == "L":
                pp.create_shunt(net=self.rede,
                                    bus=from_,
                                    q_mvar=-shunt_from,
                                    p_mw=0.0,
                                    step=1,
                                    max_step=1,
                                    in_service=True
                                    )
            
            if estado_shunt_to == "L":
                pp.create_shunt(net=self.rede,
                                bus=to,
                                q_mvar=-shunt_to,
                                p_mw=0.0,
                                step=1,
                                max_step=1,
                                in_service=True
                                )
                
    
    
    def Shunt_barra(self, df: pd.DataFrame):
        """Este bloco permite associar dispositivos shunt
        a elementos da rede.
                    
        Exemplo:
            >> Código de Execução Implementado: DBAR 
            >> Não implementados:
        """
        for _, linha in df.iterrows():
                    
            numero = int(linha["numero"])   # Esta coluna é obrigatória    
            estado = str(linha["estado"])
            shunt_barra = float(linha["shunt_barra"])
            
        
            if estado == "0":
                estado = True
            else:
                estado = self.estado(estado)

            if shunt_barra != 0.0:
                pp.create_shunt(net=self.rede,
                            bus=numero,
                            q_mvar=-shunt_barra,
                            p_mw=0.0,
                            step=1,
                            max_step=1,
                            in_service=True
                            )
        
            
    def CompensadorEstaticoReativo(self, df: pd.DataFrame):
        """Equipamento de eletrônica de potencia que varia continuamente 
        a sua injeção/absorção de potencia reativa para controlar a tensão
        do nó dentro de uma faixa especificada.
                    
        Exemplo:
            
            >> Código de Execução Implementados: DCER 
            >> Não implementados:   
            """
                            
        for _, linha in df.iterrows():
            barra = int(linha["barra"])            
            unidades = int(linha["unidades"])            
            barra_controlada = int(linha["barra_controlada"])
            potencia_reativa_minima = float(linha["potencia_reativa_minima"])
            potencia_reativa_maxima = float(linha["potencia_reativa_maxima"])
            estado = str(linha["estado"])
            
            
            if estado == "0":
                estado = True                         
            else:
                estado = self.estado(estado)
                
            if potencia_reativa_maxima == 0.0 and potencia_reativa_maxima==0.0:
                continue 
            
            pp.create_gen(
                        net=self.rede,
                        bus=barra,
                        p_mw=0.0,  # CER não injeta potência ativa
                        vm_pu=1.0,  # Setpoint de tensão a ser mantido pelo CER
                        min_q_mvar=potencia_reativa_minima * unidades,  # Limite de absorção reativa (indutivo, ex: -100 Mvar)
                        max_q_mvar=potencia_reativa_maxima * unidades,  # Limite de injeção reativa (capacitivo, ex: +150 Mvar)
                        in_service=estado,
                        controllable=True,
                    )
            
            
    # def CompensadorSerieControlavel(self, df: pd.DataFrame):
    #     """Define equipamentos FACTS de compensação serie, 
    #     cuja impedancia capacitiva/indutiva por ser ajustada
    #     dinamicamente para controlar o fluxo de potencia ativa
    #     na linha de transmissão.
                    
    #     Exemplo:
            
    #         >> Código de Execução Implementados: DCSC 
    #         >> Não implementados: 
    #         """
                    
    #     for _, linha in df.iterrows():
    #         de = int(linha["de"])
    #         para = int(linha["para"])
    #         estado = str(linha["estado"])
    #         proprietario = str(linha["proprietario"])
    #         bypass = str(linha["bypass"])
    #         reatancia_minima = str(linha["reatancia_minima"])
    #         reatancia_maxima = str(linha["reatancia_maxima"])
    #         reatancia_inicial = str(linha["reatancia_inicial"])
    #         modo_controle = str(linha["modo_controle"])
    #         especificado = str(linha["especificado"])
    #         extremidade = str(linha["extremidade"])
    #         estagios = str(linha["estagios"])
    #         capacidade_normal = str(linha["capacidade_normal"])
    #         capacidade_emergencia = str(linha["capacidade_emergencia"])
    #         capacidade = str(linha["capacidade"])
            
            
    #         if estado == "0":
    #             estado = True 
    #         else:
    #             estado = self.estado(estado)
                
            
    #         pp.create_impedance(net=self.rede,
    #                             from_bus=de,
    #                             to_bus=para,
    #                             rft_pu=1,
    #                             xft_pu=1,
    #                             sn_mva=100.0,
    #                             in_service=estado,
    #                             )
                
    # def InjecaoPotenciaBarra(self, df: pd.DataFrame):
    #     """Leitura dos dados de injeções de potências, shunts e
    #         fatores de participação de geração do modelo equivalente.
                    
    #     Exemplo:
    #             >> Código de Execução Implementados: DINJ 
    #     """
    
    #     for _, linha in df.iterrows():
    #         numero = str(linha["numero"])
    #         operacao = str(linha["operacao"])
    #         injecao_ativa_eq = str(linha["injecao_ativa_eq"])
    #         injecao_reativa_eq = str(linha["injecao_reativa_eq"])
    #         shunt_eq = str(linha["shunt_eq"])
    #         fator_participacao_eq = str(linha["fator_participacao_eq"])
            
            
            
    # def Barra_CC(self, df: pd.DataFrame):
    #     """Modela barramentos CC
        
    #         >> Código de Execução Implementados: DCBA
    #         >> Não Implementados: DELO
    #         """
        
    #     delo = self.dataframes["deloDF"]
        
    #     for _, linha in df.iterrows():
    #         numero = int(linha["numero"]) # Esta coluna é obrigatória
    #         nome = str(linha["nome"]) # Esta coluna é obrigatória
    #         tensao = float(linha["tensao"])    
            
    #         if tensao == 0.0:
    #             tensao = 1.0
            
    #         pp.create_bus_dc(net=self.rede,
    #                          vn_kv=tensao,
    #                          name=nome,
    #                          index=numero,
    #                          type="b",
    #                          in_service=True,
    #                          max_vm_pu=1.05,
    #                          min_vm_pu=0.95,
    #                          )
            
    # def Linhas_CC(self, df: pd.DataFrame):
    #     """ Modela linhas de transmissão CC
            
    #         >> Código de Execução Implementados: DCLI, DCBA, DELO
    #         >> Não Implementados: 
    #         """
                    
        
    #     for _, linha in df.iterrows():
    #         de = str(linha["de"])
    #         para = str(linha["para"])
    #         resistencia = float(linha["resistencia"])
    #         indutancia = float(linha["indutancia"])
    #         capacidade = float(linha["capacidade"]) # MW
            
            
    #         pp.create_line_dc(net=self.rede,
    #                           from_bus_dc=1,
    #                           to_bus_dc=1,
    #                           length_km=1,
    #                           index=1,
    #                           in_service=1,
                              
    #                           )
            
            
            
    # def ControleTensaoVariacaoTap(self, df: pd.DataFrame):
    #     """Controle de tensão por variação automática de tap.
                    
    #     Exemplo:
    #         Código de Execução: DTPF 
    #         DTPF CIRC
    #         (De ) (Pa ) Nc (De ) (Pa ) Nc (De ) (Pa ) Nc (De ) (Pa ) Nc (De ) (Pa ) Nc O
    #          1180 24000  2  1180 24000  1  3876  3880  1  3876 35357  1  3876  3882  1 A
    #         99999
    #     """
                    
        
    #     for _, linha in df.iterrows():
    #         tipo_elemento_1 = str(linha["tipo_elemento_1"])
    #         identificacao_elemento_1 = str(linha["identificacao_elemento_1"])
    #         condicao_elemento_1 = str(linha["condicao_elemento_1"])
    #         tipo_elemento_2 = str(linha["tipo_elemento_2"])
    #         identificacao_elemento_2 = str(linha["identificacao_elemento_2"])
    #         condicao_elemento_2 = str(linha["condicao_elemento_2"])
    #         tipo_elemento_3 = str(linha["tipo_elemento_3"])
    #         identificacao_elemento_3 = str(linha["identificacao_elemento_3"])
    #         condicao_elemento_3 = str(linha["condicao_elemento_3"])
    #         tipo_elemento_4 = str(linha["tipo_elemento_4"])
    #         identificacao_elemento_4 = str(linha["identificacao_elemento_4"])
    #         operacao = str(linha["operacao"])
    #         interligacao = str(linha["interligacao"])
            
            
            
    
             
    # def OpcoesControle(self, df: pd.DataFrame):
    #     """Liga ou desliga os controles.
                    
    #     Exemplo:
    #         Código de Execução: DOPC 
    #         DOPC IMPR
    #         (Op) E (Op) E (Op) E (Op) E (Op) E (Op) E (Op) E (Op) E (Op) E (Op) E
    #         QLIM L VLIM L CREM L CTAP L STEP L NEWT L RCVG L RMON L FILE L CONT L
    #         NOVO L CELO L MFCT L ATCR L CPHS L IANG L
    #         99999
    #     """
                    
    #     raise NotImplementedError(f"O método 'AlterarDadosBarraCC' ainda não está pronto. !")
        
    #     for _, linha in df.iterrows():
    #         opcao = str(linha["opcao"])
    #         padrao = str(linha["padrao"])
            
    # def MonitoratensaoBarra(self, df: pd.DataFrame):
    #     """Monitora a tensão de determinadas barras.
                    
    #     Exemplo:
    #         Código de Execução: DMET 
    #         ( Seleciona as barras das áreas 07, 09 e 11 para terem a tensão monitoradas ) 
    #         ( Além destas barras, todas aquelas que sofrerem variação de tensão superior ) 
    #         ( àquela especificada pela constante VART também passarão a ser monitoradas ) 
    #         ( 
    #         (tp) (no ) C (tp) (no ) C (tp) (no ) C (tp) (no ) O 
    #         AREA    07 A AREA    11 X AREA    08 E AREA    10 
    #         99999
    #     """
                    
    #     raise NotImplementedError(f"O método 'AlterarDadosBarraCC' ainda não está pronto. !")
        
    #     for _, linha in df.iterrows():
    #         tipo_elemento_1 = str(linha["tipo_elemento_1"])
    #         identificacao_elemento_1 = str(linha["identificacao_elemento_1"])
    #         condicao_elemento_1 = str(linha["condicao_elemento_1"])
    #         tipo_elemento_2 = str(linha["tipo_elemento_2"])
    #         identificacao_elemento_2 = str(linha["identificacao_elemento_2"])
    #         condicao_elemento_2 = str(linha["condicao_elemento_2"])
    #         tipo_elemento_3 = str(linha["tipo_elemento_3"])
    #         identificacao_elemento_3 = str(linha["identificacao_elemento_3"])
    #         condicao_elemento_3 = str(linha["condicao_elemento_3"])
    #         tipo_elemento_4 = str(linha["tipo_elemento_4"])
    #         identificacao_elemento_4 = str(linha["identificacao_elemento_4"])
    #         operacao = str(linha["operacao"])
   
    
            
            
    # def DirecaoCarregamentoBarras(self, df: pd.DataFrame):
    #     """Dados de limites de Tensão.
                    
    #     Exemplo:
    #         Código de Execução: DINC 
            
    #         ( Determina que as cargas das áreas 07, 09 e 11 serão incrementadas através ) 
    #         ( de degraus de 0.5% na parcela ativa e de 0.3% na parcela reativa, até que ) 
    #         ( se atinja o carregamento máximo de 15% e 10%, respectivamente ) 
    #         ( 
    #         (tp) (no ) C (tp) (no ) C (tp) (no ) C (tp) (no ) O ( P ) ( Q ) (Pmx) (Qmx) 
    #         AREA    07 A AREA    11 X AREA    08 E AREA    10     0.5   0.3   15. 10. 
    #         99999
    #     """
                    
    #     raise NotImplementedError(f"O método 'AlterarDadosBarraCC' ainda não está pronto. !")
        
    #     for _, linha in df.iterrows():
    #         tipo_incremento_1 = str(linha["tipo_incremento_1"])
    #         identificacao_incremento_1 = str(linha["identificacao_incremento_1"])
    #         condicao_incremento_1 = str(linha["condicao_incremento_1"])
    #         tipo_incremento_2 = str(linha["tipo_incremento_2"])
    #         identificacao_incremento_2 = str(linha["identificacao_incremento_2"])
    #         condicao_incremento_2 = str(linha["condicao_incremento_2"])
    #         tipo_incremento_3 = str(linha["tipo_incremento_3"])
    #         identificacao_incremento_3 = str(linha["identificacao_incremento_3"])
    #         condicao_incremento_3 = str(linha["condicao_incremento_3"])
    #         tipo_incremento_4 = str(linha["tipo_incremento_4"])
    #         identificacao_incremento_4 = str(linha["identificacao_incremento_4"])
    #         condicao_incremento_4 = str(linha["condicao_incremento_4"])
    #         passo_incremento_potencia_ativa = float(linha["passo_incremento_potencia_ativa"])
    #         passo_incremento_potencia_reativa = float(linha["passo_incremento_potencia_reativa"])
    #         maximo_incremento_potencia_ativa = float(linha["maximo_incremento_potencia_ativa"])
    #         maximo_incremento_potencia_reativa = float(linha["maximo_incremento_potencia_reativa"])
    #         tratamento_incremento_potencia_ativa = float(linha["tratamento_incremento_potencia_ativa"])
    #         tratamento_incremento_potencia_reativa = float(linha["tratamento_incremento_potencia_reativa"])
            
            
    # def DadosLimiteTensao(self, df: pd.DataFrame):
    #     """Dados de limites de Tensão.
                    
    #     Exemplo:
    #         Código de execução: DGLT
            
    #         DGLT
    #         (G (Vmn) (Vmx) (Vmne (Vmxe
    #          2   .95  1.05   .95  1.05
    #         99999
    #     """
                    
    #     raise NotImplementedError(f"O método 'AlterarDadosBarraCC' ainda não está pronto. !")
        
    #     for _, linha in df.iterrows():
    #         grupo_limite_tensao = str(linha["grupo_limite_tensao"])
    #         limite_minimo = float(linha["limite_minimo"])
    #         limite_maximo = float(linha["limite_maximo"])
    #         limite_minimo_E = float(linha["limite_minimo_E"])
    #         limite_maximo_E = float(linha["limite_maximo_E"])
            
            
    # def DadosComplementaresGeracao(self, df: pd.DataFrame):
    #     """Dados de limites de geração de potência ativa e fatores
    #     de participação de barras de geração.
                    
    #     Exemplo:
    #         Código de execução: DGER
            
    #     """
                    
    #     raise NotImplementedError(f"O método 'AlterarDadosBarraCC' ainda não está pronto. !")
        
    #     for _, linha in df.iterrows():
    #         numero = str(linha["numero"])
    #         operacao = str(linha["operacao"])
    #         potencia_ativa_minima = float(linha["potencia_ativa_minima"])
    #         potencia_ativa_maxima = float(linha["potencia_ativa_maxima"])
    #         fator_participacao = float(linha["fator_participacao"])
    #         fator_participacao_controle_remoto = float(linha["fator_participacao_controle_remoto"])
    #         fator_potencia_nominal = float(linha["fator_potencia_nominal"])
    #         fator_servico_armadura = float(linha["fator_servico_armadura"])
    #         fator_servico_rotor = float(linha["fator_servico_rotor"])
    #         angulo_maximo_carga = float(linha["angulo_maximo_carga"])
    #         reatancia_maquina = float(linha["reatancia_maquina"])
    #         potencia_aparente_nominal = float(linha["potencia_aparente_nominal"])
    #         estatismo = float(linha["estatismo"])
                
    # def baseTensaoBarrasCA(self, df: pd.DataFrame):
    #     """Dados de base de tensão de barra CA.
                    
    #     Exemplo:
    #         Código de execução: DGBT
            
    #         DGBT
    #         (G ( kV)
    #          Z  999.
    #         99999
    #     """
                    
    #     raise NotImplementedError(f"O método 'AlterarDadosBarraCC' ainda não está pronto. !")
        
    #     for _, linha in df.iterrows():
    #         grupo = str(linha["grupo"])
    #         tensao = float(linha["tensao"])
            
    # def DadosEloCC(self, df: pd.DataFrame):
    #     """Dados de elo CC.
                    
    #     Exemplo:
    #         Código de execução: DELO
            
    #         DELO
    #         (No) O ( V ) ( P ) (   Identificacao  ) M E
    #         1    600. 1566. POLO 1 F.IG - IBIUNA N L  
    #         99999
    #     """
                    
    #     raise NotImplementedError(f"O método 'AlterarDadosBarraCC' ainda não está pronto. !")
        
    #     for _, linha in df.iterrows():
    #         numero = str(linha["numero"])
    #         operacao = str(linha["operacao"])
    #         tensao = float(linha["tensao"])
    #         BMVA = float(linha["BMVA"])
    #         nome = str(linha["nome"])
    #         modo_high = str(linha["modo_high"])
    #         estado = str(linha["estado"])
            
    # def DadosComplementaresTrafos(self, df: pd.DataFrame):
    #     """Dados complementares de transformadores.
                    
    #     Exemplo:
    #             Código de execução: DCTR
    #         DCTR
    #         (Nf ) O (Nt ) Nc Vmin Vmax C M (Fmin) (Fmax) C ( Vsp) (Ext) Ns (IdCurvaPts)
    #         2157    2147  1                 -30.    30. P 64.395  2157 
    #         99999
    #         """
                    
    #     raise NotImplementedError(f"O método 'AlterarDadosBarraCC' ainda não está pronto. !")
        
    #     for _, linha in df.iterrows():
    #         de = str(linha["de"])
    #         operacao = str(linha["operacao"])
    #         para = str(linha["para"])
    #         circuito = str(linha["circuito"])
    #         tensao_minima = float(linha["tensao_minima"])
    #         tensao_maxima = float(linha["tensao_maxima"])
    #         tipo_controle_1 = str(linha["tipo_controle_1"])
    #         modo_controle = str(linha["modo_controle"])
    #         fase_minima = float(linha["fase_minima"])
    #         fase_maxima = float(linha["fase_maxima"])
    #         tipo_controle_2 = str(linha["tipo_controle_2"])
    #         valor_especificado = float(linha["valor_especificado"])
    #         extremidade = str(linha["extremidade"])
    #         taps = float(linha["taps"])
            
    # def Constantes(self, df: pd.DataFrame):
    #     """Informações de elementos para contingência.
                    
    #     Exemplo:
            
    #         """
                    
    #     raise NotImplementedError(f"O método 'AlterarDadosBarraCC' ainda não está pronto. !")
        
    #     for _, linha in df.iterrows():
    #         identificacao = str(linha["identificacao"])
    #         operacao = str(linha["operacao"])
    #         prioridade = str(linha["prioridade"])
    #         nome = str(linha["nome"])
    #         ndctg2 = str(linha["ndctg2"])
    #         tipo = str(linha["tipo"])
    #         de = str(linha["de"])
    #         para = str(linha["para"])
    #         circuito = str(linha["circuito"])
    #         extremidade = str(linha["extremidade"])
    #         variacao_geracao_ativa = float(linha["variacao_geracao_ativa"])
    #         variacao_geracao_ativa_minima = float(linha["variacao_geracao_ativa_minima"])
    #         variacao_geracao_ativa_maxima = float(linha["variacao_geracao_ativa_maxima"])
    #         variacao_geracao_reativa = float(linha["variacao_geracao_reativa"])
    #         variacao_geracao_reativa_minima = float(linha["variacao_geracao_reativa_minima"])
    #         variacao_geracao_reativa_maxima = float(linha["variacao_geracao_reativa_maxima"])
    #         variacao_fator_participacao = float(linha["variacao_fator_participacao"])
    #         grupo = float(linha["grupo"])
    #         unidades = float(linha["unidades"])
            
    # def Constantes(self, df: pd.DataFrame):
    #     """Leitura e modificação de constantes utilizadas no progama.
                    
    #     Exemplo:
            
    #         Código de Execução: DCTE 
    #         DCTE
    #         (Mn) ( Val) (Mn) ( Val) (Mn) ( Val) (Mn) ( Val) (Mn) ( Val) (Mn) ( Val) 
    #         BASE   100. DASE   100. TEPA    .01 EXST    .04 TETP     5. TBPA     5.
    #         99999
                
    #         """
                    
    #     # raise NotImplementedError(f"O método 'AlterarDadosBarraCC' ainda não está pronto. !")
        
    #     for _, linha in df.iterrows():
    #         constante = str(linha["constante"])
    #         valor_constante = float(linha["valor_constante"])
    #         constante = str(linha["constante"])
    #         valor_constante = float(linha["valor_constante"])
    #         constante = str(linha["constante"])
    #         valor_constante = float(linha["valor_constante"])
    #         constante = str(linha["constante"])
    #         valor_constante = float(linha["valor_constante"])
    #         constante = str(linha["constante"])
    #         valor_constante = float(linha["valor_constante"])
    #         constante = str(linha["constante"])
    #         valor_constante = float(linha["valor_constante"])
            
    
            
    # def DadosEstacoesConversoras(self, df: pd.DataFrame):
    #     """Define a especificação detalhada e individual das estações
    #     conversoras que compoem os elos CC.
                    
    #     Exemplo:
            
    #         Código de Execução: DCNV 
    #         DCNV
    #         (No) O (CA ) (CC) (EL) T p (Ino) (Xc ) (Vfs) (Snt) (Rra) (Lra) (CCC) Fr
    #             1    3639   10   30 R 4 2610.  17.8 127.4  471.    0.  
    #         99999
                
    #         """
                    
    #     raise NotImplementedError(f"O método 'AlterarDadosBarraCC' ainda não está pronto. !")
        
    #     for _, linha in df.iterrows():
    #         numero = str(linha["numero"])
    #         operacao = str(linha["operacao"])
    #         barra_CA = str(linha["barra_CA"])
    #         barra_CC = str(linha["barra_CC"])
    #         barra_neutra = str(linha["barra_neutra"])
    #         modo_operacao = float(linha["modo_operacao"])
    #         pontes = float(linha["pontes"])
    #         corrente = float(linha["corrente"])
    #         reatancia_comutacao = float(linha["reatancia_comutacao"])
    #         tensao_secundario = float(linha["tensao_secundario"])
    #         potencia_transformador = float(linha["potencia_transformador"])
    #         resistencia_reator = float(linha["resistencia_reator"])
    #         indutancia_reator = float(linha["indutancia_reator"])
    #         capacitancia = float(linha["capacitancia"])
    #         frequencia = float(linha["frequencia"])
                    
    
            
    
                
                
                
    # def ControleConversoresCACC(self, df: pd.DataFrame):
    #     """Bloco de dados responsável por configurar e modelar
    #     elos de corrente contínua e seus conversores de rede.
                    
    #     Exemplo:
            
    #         Código de Execução: DCCV 
    #         DCCV
    #         (No) O FMC (Vsp) (Marg (IMax (Dsp) (Dtn) (Dtm) (Tmn) (Tmx) (S (Vmn (Tmh) (Ttr)
    #            1     P 989.6       .0014   15.    5. 84.99  .925  1.25     975 1.237    1.
    #         99999
                
    #         """
                    
    #     raise NotImplementedError(f"O método 'AlterarDadosBarraCC' ainda não está pronto. !")
        
    #     for _, linha in df.iterrows():
    #         # Número de identificação da Barra CC
    #         numero = str(linha["numero"])
            
    #         # A ou 0 (Adição de dados), M ou 2 (Modificação de dados), E ou 1 (Eliminação de dados)
    #         operacao = str(linha["operacao"])
            
    #         # F (conversor de folga), N (conversor normal)
    #         folga = str(linha["folga"])
            
    #         # G (controle de gamma), T (controle da tensão da barra CA de interface)
    #         modo_controle_inversor = str(linha["modo_controle_inversor"])
            
    #         # C (conversor com controle de corrente constante), P (conversor com controle de potencia constante)
    #         tipo_controle_conversor = str(linha["tipo_controle_conversor"])
            
    #         # Valor em A se for o controle for de corrente ou em MW se o controle for de potência
    #         valor_especificado = float(linha["valor_especificado"])
            
    #         # Margem de corrente do inversor em % da corrente nominal
    #         margem_corrente = float(linha["margem_corrente"])
            
    #         # Margem de sobrecorrente permitida em % da corrente nominal
    #         maxima_sobrecorrente = float(linha["maxima_sobrecorrente"])
            
    #         # Ângulo desejado de disparo, extinçao ou margem em graus
    #         angulo_conversor = float(linha["angulo_conversor"])
            
    #         # Angulo minimo de disparo, extinçao ou margem em graus
    #         angulo_conversor_minimo = float(linha["angulo_conversor_minimo"])
            
    #         # Angulo maximo de disparo, extinçao ou margem em graus
    #         angulo_conversor_maximo = float(linha["angulo_conversor_maximo"])
            
    #         # Tap minimo do transformador conversor
    #         tap_transformador_minimo = float(linha["tap_transformador_minimo"])
            
    #         # Tap maximo do transformador conversor
    #         tap_transformador_maximo = float(linha["tap_transformador_maximo"])
            
    #         # Número do passos do tap do transformador
    #         tap_transformador_numero = float(linha["tap_transformador_numero"])
            
    #         # Abaixo desta tensão o conversor começa a operar com controle de corrente
    #         tensao_cc_minima = float(linha["tensao_cc_minima"])
            
    #         # Tap para operar em alto consumo  de reativo
    #         tap_high = float(linha["tap_high"])
            
    #         # Tap quando operando em tensão reduzida
    #         tap_reduzido = float(linha["tap_reduzido"])
            
    
            
    # def ModeloZipCargas(self, df: pd.DataFrame):
    #     """Modelar a dependência da carga em relação à tensão (Modelagem Zip).
                    
    #     Exemplo:
            
    #         Código de Execução: DCAR 
    #         (Modelagem da carga em 100% Z constante de todas as barras das áreas) 
    #         (07, 09 e 11) 
    #         (tp) (no ) C (tp) (no ) C (tp) (no ) C (tp) (no ) O (A) (B) (C) (D) (Vfl) 
    #         AREA    07 A AREA    11 X AREA    08 E AREA    10     0 100   0 100  60.0 
    #         99999
                
    #         """
                    
    #     raise NotImplementedError(f"O método 'Barramento_CA' ainda não está pronto. !")
        
    #     for _, linha in df.iterrows():
    #         # BARR (barra) | AREA (area) | TENS (base de tensão) | AG01...(agregador)
    #         tipo_elemento_1 = linha["tipo_elemento_1"].astype(str)
            
    #         # Número da barra ou Àrea (DBAR) | Base de tensão (DGBT)
    #         identificacao_elemento_1 = linha["identificacao_elemento_1"].astype(str)
            
    #         # A (intervalo) | E (união)
    #         condicao_elemento_1 = linha["condicao_elemento_1"].astype(str)
            
    #         # BARR (barra) | AREA (area) | TENS (base de tensão) | AG01...(agregador)
    #         tipo_elemento_2 = linha["tipo_elemento_2"].astype(str)
            
    #         # Número da barra ou Àrea (DBAR) | Base de tensão (DGBT)
    #         identificacao_elemento_2 = linha["identificacao_elemento_2"].astype(str)
            
    #         # X (diferença C1 e C2) | E (união C1 e C2) | S (interseção C1 e C2)
    #         condicao_elemento_2 = linha["condicao_elemento_2"].astype(str)
            
    #         # BARR (barra) | AREA (area) | TENS (base de tensão) | AG01...(agregador)
    #         tipo_elemento_3 = linha["tipo_elemento_3"].astype(str)
            
    #         # Número da barra ou Àrea (DBAR) | Base de tensão (DGBT)
    #         identificacao_elemento_3 = linha["identificacao_elemento_3"].astype(str)
            
    #         # A (intervalo) | E (união)
    #         condicao_elemento_3 = linha["condicao_elemento_3"].astype(str)
            
    #         # BARR (barra) | AREA (area) | TENS (base de tensão) | AG01...(agregador)
    #         tipo_elemento_4 = linha["tipo_elemento_4"].astype(str)
            
    #         # Número da barra ou Àrea (DBAR) | Base de tensão (DGBT)
    #         identificacao_elemento_4 = linha["identificacao_elemento_4"].astype(str)
            
    #         # Parcela de carga ativa que varia linearmente com a tensão em %
    #         parametro_A = linha["parametro_A"].astype(float)
            
    #         # Parcela de carga ativa que varia quadraticamente com a tensão em %
    #         parametro_B = linha["parametro_B"].astype(float)
            
    #         # Parcela de carga reativa que varia linearmente com a tensão em %
    #         parametro_C = linha["parametro_C"].astype(float)
            
    #         # Parcela de carga reativa que varia quadraticamente com a tensão em %
    #         parametro_D = linha["parametro_D"].astype(float)
            
    #         # Valor de tensão abaixo do qual a carga é modelada como impedância constante em %
    #         tensao_limite = linha["tensao_limite"].astype(float)                 
    
    # def AlteracaoNivelCarregamentoDanc(self, df: pd.DataFrame):
    #     """Dados de Alteração do Nível de carregamento, utilizado para aplicar
    #         fatores percentuais de escalonamento ou modificar montantes globais de carga
    #         ativa/reativa e shunts de barra de uma região da rede de forma direta.
        
    #     Formato SEM a opção ACLS (Entrada Direta por Àrea)
        
    #         -> Quando executa DANC a alteração é:
            
    #     Exemplo:
    #         DANC
    #         (Area) (Fat P%) (Fat Q%) (Fat Sh%)
    #         001    110.0    110.0    100.0
    #         002     90.0     90.0    100.0
    #         99999
        
        
    #     Formato COM a opção ACLS (Uso da Linguagem de Seleção)
        
    #         -> É possível filtrar as barras que sofrerão o escalonamento
    
    #         Exemplo:
    #             DANC ACLS
    #             (tp) (num) C (tp) (num) C (tp) (num) C (tp) (num)   (Fat P%) (Fat Q%) (Fat Sh%)
    #             AREA    03 E TENS   138                              105.0    105.0    100.0
    #             99999
            
    #     """
        
    #     raise NotImplementedError(f"O método 'AlteracaoNivelCarregamento' ainda não está pronta. !")
        
    #     # Danc Acls ?
    #     if "tipo_incremento_1" in df.columns:
            
    #         for idx, linha in df.iterrows():
                
    #             # BARR (barra) | AREA (area) | TENS (base de tensão) | AG01...(agregador)
    #             tipo_elemento_1 = linha["tipo_elemento_1"].astype(str)
                
    #             # Número da barra ou Àrea (DBAR) | Base de tensão (DGBT)
    #             identificacao_elemento_1 = linha["identificacao_elemento_1"].astype(str)
                
    #             # A (intervalo) | E (união)
    #             condicao_elemento_1 = linha["condicao_elemento_1"].astype(str)
                
    #             # BARR (barra) | AREA (area) | TENS (base de tensão) | AG01...(agregador)
    #             tipo_elemento_2 = linha["tipo_elemento_2"].astype(str)
                
    #             # Número da barra ou Àrea (DBAR) | Base de tensão (DGBT)
    #             identificacao_elemento_2 = linha["identificacao_elemento_2"].astype(str)
                
    #             # X (diferença C1 e C2) | E (união C1 e C2) | S (interseção C1 e C2)
    #             condicao_elemento_2 = linha["condicao_elemento_2"].astype(str)
                
    #             # BARR (barra) | AREA (area) | TENS (base de tensão) | AG01...(agregador)
    #             tipo_elemento_3 = linha["tipo_elemento_3"].astype(str)
                
    #             # Número da barra ou Àrea (DBAR) | Base de tensão (DGBT)
    #             identificacao_elemento_3 = linha["identificacao_elemento_3"].astype(str)
                
    #             # A (intervalo) | E (união)
    #             condicao_elemento_3 = linha["condicao_elemento_3"].astype(str)
                
    #             # BARR (barra) | AREA (area) | TENS (base de tensão) | AG01...(agregador)
    #             tipo_elemento_4 = linha["tipo_elemento_4"].astype(str)
                
    #             # Número da barra ou Àrea (DBAR) | Base de tensão (DGBT)
    #             identificacao_elemento_4 = linha["identificacao_elemento_4"].astype(str)
                
    #             # Fator multiplicativo percentual da potência ativa das cargas selecionadas
    #             fator_carga_ativa = linha["fator_carga_ativa"].astype(float)
                
    #             # Fator multiplicativo percentual da potência reativa das cargas selecionadas
    #             fator_carga_reativa = linha["fator_carga_reativa"].astype(float)
                
    #             # Fator multiplicativo percentual dos valores nominais dos capacitores/reatores selecionadas
    #             fator_shunt_barra = linha["fator_shunt_barra"].astype(float)
        
    #     # Danc ?
    #     else:
    #         for idx, linha in df.iterrows():
                
    #             # Fator multiplicativo percentual da potência ativa das cargas selecionadas
    #             fator_carga_ativa = linha["fator_carga_ativa"].astype(float)
                
    #             # Fator multiplicativo percentual da potência reativa das cargas selecionadas
    #             fator_carga_reativa = linha["fator_carga_reativa"].astype(float)
                
    #             # Fator multiplicativo percentual dos valores nominais dos capacitores/reatores selecionadas
    #             fator_shunt_barra = linha["fator_shunt_barra"].astype(float)

    # def IntercambioPotenciaAtivaEntreAreas(self, df: pd.DataFrame):
    #     """Tem como função principal declarar as áreas operacionais do sistema elétrico
    #     e definir as diretrizes do intercâmbio de potência ativa entre elas.
        
    #     Exemplo:
    #         DARE
    #         (Ar    (Xchg)     (      Identificacao da area       ) (Xmin) (Xmax)
    #         1        0.       RS - 525 kV                                        
    #         2        0.       RS - 230 kV        
    #         99999
            
    #     """
        
    #     raise NotImplementedError(f"O método 'IntercambioPotenciaAtivaEntreAreas' ainda não está pronta. !")
        

    #     for _, linha in df.iterrows():
            
    #         # Número da área. (Relaciona-se com a coluna area em DBAR)
    #         numero = linha["numero"].astype(str)

    #         # Valor líquido do intercâmbio entre áreas (+ Exportação, - Importação)
    #         intercambio_liquido = linha["intercambio_liquido"].astype(float)
            
    #         # Identificação alfanumérica da área
    #         nome = linha["nome"].astype(str)
            
    #         # Valor líquido Minímo do intercâmbio entre áreas (+ Exportação, - Importação)
    #         intercambio_minimo = linha["intercambio_minimo"].astype(float)
            
    #         # Valor líquido Máximo do intercâmbio entre áreas (+ Exportação, - Importação)
    #         intercambio_maximo = linha["intercambio_maximo"].astype(float)
            
            
    
                    
    def estado(self, estado):
        estado = True if estado in ("L") else False
        return estado 




