
import pandas as pd 
import numpy  as np
import sys 
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path 




def r(x, n=2):
    if np.isnan(x) or np.isinf(x):
        return x
    return float(Decimal(str(x)).quantize(Decimal(f"1e-{n}"), ROUND_HALF_UP))


MAPA_TIPOS_BARRA = {"pq": 0, "pqv": 0, "pv": 1, "vt": 2, "pq_lim_v": 3}
MAPA_ESTADO = {"L": "LIG"}




class Subsystem2():
    
    
    @classmethod
    def calculator(
        cls,
        net,
        formato="json",
        dir_output: Path | str | None = None
    ):
        # if dir_output is None:
        #     PROJECT_ROOT = Path(__file__).resolve().parents[3]
        #     dir_output   = PROJECT_ROOT / "output" / "reports"
        #     dir_output.mkdir(parents=True, exist_ok=True)
        
        if dir_output is None:
            main_mod = sys.modules.get("__main__")
            if main_mod is not None and getattr(main_mod, "__file__", None):
                # Caso 1: Executado via script .py (ex: python testador.py)
                base_dir = Path(main_mod.__file__).resolve().parent
            else:
                # Caso 2: Executado via Jupyter Notebook (.ipynb) ou terminal interativo
                base_dir = Path.cwd().resolve()

            dir_output = base_dir / "output" / "reports"
        else:
            dir_output = Path(dir_output).resolve()

        dir_output.mkdir(parents=True, exist_ok=True)
                    
        
                    
        cls.rbar(net)
        cls.rlin(net)
        #cls.rtra(net)
        
        
        if not net.DadosRede.dgerDF.empty:
            cls.rger(net)
            cls.rgel(net)
            
        
        
        rbar : pd.DataFrame = net.RBAR
        rlin : pd.DataFrame = net.RLIN 
        rger : pd.DataFrame = net.RGER
        rgel : pd.DataFrame = net.RGEL
        #rtra : pd.DataFrame = net.RTRA
        
        if formato == "json":
            rbar.to_json(dir_output / "rbar.json", orient="records", indent=4, force_ascii=False)
            rlin.to_json(dir_output / "rlin.json", orient="records", indent=4, force_ascii=False)
            rger.to_json(dir_output / "rger.json", orient="records", indent=4, force_ascii=False)
            rgel.to_json(dir_output / "rgel.json", orient="records", indent=4, force_ascii=False)
           # rtra.to_json(dir_output / "rtra.json", orient="records", indent=4, force_ascii=False)
        
        
        
              
        
    
    @classmethod
    def rbar(cls, net):

        cte: dict = net.DadosRede.cte
        dbar: pd.DataFrame = net.DadosRede.dbarDF
        data = net.data
        n_bus = len(dbar)

        mask_p        = np.zeros(n_bus, dtype=bool)
        mask_q        = np.zeros(n_bus, dtype=bool)
        mask_pq_lim_v = np.zeros(n_bus, dtype=bool)
        mask_pv_lim_q = np.zeros(n_bus, dtype=bool)

        mask_p[data.idx_p]               = True
        mask_q[data.idx_q]               = True
        mask_pq_lim_v[data.pq_lim_v_idx] = True
        mask_pv_lim_q[data.pv_lim_q_idx] = True

        # Classificação mutuamente exclusiva dos estados finais
        mask_slack       = ~mask_p
        mask_pq          = mask_p & mask_q & ~mask_pq_lim_v & ~mask_pv_lim_q
        mask_pv          = mask_p & ~mask_q & ~mask_pq_lim_v
        mask_pv_q_extrap = mask_pv_lim_q & mask_q           # PV que extrapolou Q e virou PQ (-1)
        mask_pq_v_normal = mask_pq_lim_v & mask_q           # PQ com limite de V dentro da faixa (3)
        mask_pq_v_extrap = mask_pq_lim_v & ~mask_q          # PQ que extrapolou V e virou PV (-3)

        # Montagem da coluna Tipo da Barra conforme convenção numérica
        tipo_barra_rbar = np.zeros(n_bus, dtype=int)        # 0: PQ padrão
        tipo_barra_rbar[mask_pv]          = 1               # 1: PV
        tipo_barra_rbar[mask_slack]       = 2               # 2: Slack (Vθ)
        tipo_barra_rbar[mask_pq_v_normal] = 3               # 3: PQ com limite de tensão (não extrapolada)
        tipo_barra_rbar[mask_pv_q_extrap] = -1              # -1: PV extrapolada (virou PQ)
        tipo_barra_rbar[mask_pq_v_extrap] = -3              # -3: PQ com limite de tensão extrapolada

        v_pu    = np.asarray(data.v, dtype=np.float64)
        ang_rad = np.asarray(data.t, dtype=np.float64)
        ang_deg = np.rad2deg(ang_rad)

        v_complex = v_pu * np.exp(1j * ang_rad)
        i_complex = data.Ybus_csr @ v_complex
        s_inj_mva = (v_complex * np.conj(i_complex)) * cte["BMVA"]

        p_inj_mw   = s_inj_mva.real
        q_inj_mvar = s_inj_mva.imag

        p_carga_mw       = dbar["carga_ativa"].to_numpy(dtype=np.float64, copy=True)
        q_carga_mvar     = dbar["carga_reativa"].to_numpy(dtype=np.float64, copy=True)
        q_shunt_nom_mvar = dbar["capacitor_reator"].to_numpy(dtype=np.float64, copy=True)
        q_shunt_mvar     = q_shunt_nom_mvar * (v_pu ** 2)

        p_geracao_mw   = dbar["geracao_ativa"].to_numpy(dtype=np.float64, copy=True)
        q_geracao_mvar = dbar["geracao_reativa"].to_numpy(dtype=np.float64, copy=True)

        p_geracao_mw   = p_inj_mw + p_carga_mw
        q_geracao_mvar = q_inj_mvar + q_carga_mvar

        vn_kv = dbar["tensao_para_definicao_de_carga"].to_numpy(dtype=np.float64, copy=True) / 1000
        zeros = np.zeros(n_bus, dtype=np.float64)

        df_rbar = pd.DataFrame({
            "Número"                        : dbar["numero"],
            "Área"                          : dbar["area"],
            "Nome"                          : dbar["nome"],
            "Tensão (p.u.)"                 : v_pu,
            "Ângulo (graus)"                : ang_deg,
            "Carga Ativa (MW)"              : p_carga_mw,
            "Carga Reativa (Mvar)"          : q_carga_mvar,
            "Geração Ativa (MW)"            : p_geracao_mw,
            "Geração Reativa (Mvar)"        : q_geracao_mvar,
            "Shunt (Mvar)"                  : q_shunt_mvar,
            "Potência Ativa Elo DC (MW)"    : zeros,
            "Potência Reativa Elo DC (Mvar)": zeros,
            "Injeção Equivalente (MW)"      : zeros,
            "Injeção Equivalente (Mvar)"    : zeros,
            "Motor de Indução (MW)"         : zeros,
            "Motor de Indução (Mvar)"       : zeros,
            "Tipo da Barra"                 : tipo_barra_rbar,
            "Tensão (kV)"                   : vn_kv,
            "CER (Mvar)"                    : zeros,
            "Shunt de Linha (Mvar)"         : zeros,
            "Estado Operativo"              : dbar["estado"].map(MAPA_ESTADO),
        })

        cols_float = df_rbar.select_dtypes(include="float").columns
        df_rbar[cols_float] = df_rbar[cols_float].map(r)

        net.RBAR = df_rbar
            
            
    


    @classmethod
    def rlin(cls, net):
        MAPA_ESTADO = {"L": "LIG", "D": "DESL"}

        cte: dict = net.DadosRede.cte
        RBAR: pd.DataFrame = net.RBAR
        dbar: pd.DataFrame = net.DadosRede.dbarDF
        dlin: pd.DataFrame = net.DadosRede.dlinDF

        s_base = float(cte["BMVA"])
        
        # Mapeamento dos valores exatos (float64) direto do solver (net.data)
        numeros_barras = dbar["numero"].to_numpy(dtype=int)
        mapa_v_exato = dict(zip(numeros_barras, np.asarray(net.data.v, dtype=np.float64)))
        mapa_t_exato = dict(zip(numeros_barras, np.asarray(net.data.t, dtype=np.float64)))  # já em radianos

        # Garante acesso rápido aos dados de RBAR e à coluna 'area' de dbar
        rbar_com_area = RBAR.copy()
        if "Área" not in rbar_com_area.columns:
            mapa_area = dict(zip(dbar["numero"], dbar["area"]))
            rbar_com_area["Área"] = rbar_com_area["Número"].map(mapa_area)

        dict_dbar = rbar_com_area.set_index("Número").to_dict(orient="index")

        def r(x, n=2):
            if pd.isna(x) or np.isinf(x):
                return x
            return float(Decimal(str(x)).quantize(Decimal(f"1e-{n}"), ROUND_HALF_UP))

        def i_km(akm, ykm, y_sh, Ek, phikm, Em):
            ikm = ((1.0 / akm) ** 2 * ykm + y_sh) * Ek - (ykm / (akm * np.exp(-1j * phikm))) * Em
            return ikm

        def i_mk(akm, ykm, y_sh, Ek, phikm, Em):
            imk = -(ykm / (akm * np.exp(1j * phikm))) * Ek + (ykm + y_sh) * Em
            return imk

        def s_km(Ek, ikm):
            return Ek * np.conj(ikm) * s_base

        def s_mk(Em, imk):
            return Em * np.conj(imk) * s_base

        def s_perda(smk, skm):
            return smk + skm

        def fluxo_percentual(s_mva, capacidade_nominal):
            if capacidade_nominal <= 0:
                return 0.0
            return (s_mva / capacidade_nominal) * 100.0

        def fluxo_percentual_v(fluxo_pct, Vk):
            if Vk <= 0:
                return 0.0
            return fluxo_pct / Vk

        # Listas de saída
        numero_barra_de, nome_barra_de, numero_area_de = [], [], []
        tipo, tensao_kv, tensao_pu, angulo_graus = [], [], [], []
        geracao_ativa_mw, geracao_reativa_mvar = [], []
        injecao_equivalente_mw, injecao_equivalente_mvar = [], []
        carga_ativa_mw, carga_reativa_mvar = [], []
        potencia_ativa_elo_cc_mw, potencia_reativa_elo_cc_mvar = [], []
        motor_de_inducao_mw, motor_de_inducao_mvar = [], []
        numero_para_barra, nome_barra_para, numero_area_para = [], [], []
        numero_do_circuito = []
        fluxo_mw, fluxo_mvar, fluxo_mva = [], [], []
        fluxo_pct_list, fluxo_pct_v_list = [], []
        cap_nominal_list, cap_emergencia_list, cap_equipamento_list = [], [], []
        tap_list, defasagem_list, tie_line_list = [], [], []
        perda_ativa_list, perda_reativa_list = [], []
        tensao_ca_list, angulo_ca_list = [], []
        estado_op_list, estado_de_list, estado_para_list = [], [], []

        def registrar_fluxo(
            num_de, num_para, circ, s_fluxo, f_pct, f_pct_v,
            cap_nom, cap_emg, cap_eqp, tap_val, defas_val,
            is_tie, p_loss, q_loss, est_op, est_de, est_para
        ):
            b_de = dict_dbar[num_de]
            b_para = dict_dbar[num_para]

            numero_barra_de.append(num_de)
            nome_barra_de.append(b_de["Nome"])
            numero_area_de.append(b_de["Área"])
            tipo.append(b_de["Tipo da Barra"])
            tensao_kv.append(b_de["Tensão (kV)"])
            tensao_pu.append(b_de["Tensão (p.u.)"])
            angulo_graus.append(b_de["Ângulo (graus)"])
            geracao_ativa_mw.append(b_de["Geração Ativa (MW)"])
            geracao_reativa_mvar.append(b_de["Geração Reativa (Mvar)"])
            injecao_equivalente_mw.append(b_de["Injeção Equivalente (MW)"])
            injecao_equivalente_mvar.append(b_de["Injeção Equivalente (Mvar)"])
            carga_ativa_mw.append(b_de["Carga Ativa (MW)"])
            carga_reativa_mvar.append(b_de["Carga Reativa (Mvar)"])
            # Atenção ao nome da coluna no RBAR ("Elo DC" vs "Elo CC")
            potencia_ativa_elo_cc_mw.append(b_de.get("Potência Ativa Elo DC (MW)", 0.0))
            potencia_reativa_elo_cc_mvar.append(b_de.get("Potência Reativa Elo DC (Mvar)", 0.0))
            motor_de_inducao_mw.append(int(b_de.get("Motor de Indução (MW)", 0)))
            motor_de_inducao_mvar.append(b_de.get("Motor de Indução (Mvar)", 0.0))

            numero_para_barra.append(num_para)
            nome_barra_para.append(b_para["Nome"])
            numero_area_para.append(b_para["Área"])
            numero_do_circuito.append(circ)

            fluxo_mw.append(s_fluxo.real)
            fluxo_mvar.append(s_fluxo.imag)
            fluxo_mva.append(abs(s_fluxo))
            fluxo_pct_list.append(f_pct)
            fluxo_pct_v_list.append(f_pct_v)

            cap_nominal_list.append(cap_nom)
            cap_emergencia_list.append(cap_emg)
            cap_equipamento_list.append(cap_eqp)
            tap_list.append(tap_val)
            defasagem_list.append(defas_val)
            tie_line_list.append(is_tie)

            perda_ativa_list.append(p_loss)
            perda_reativa_list.append(q_loss)
            tensao_ca_list.append(0.00)
            angulo_ca_list.append(0.00)

            estado_op_list.append(est_op)
            estado_de_list.append(est_de)
            estado_para_list.append(est_para)

        for _, dados in dlin.iterrows():
            num_de = int(dados["da_barra"])
            num_para = int(dados["para_barra"])
            circ = int(dados["circuito"])

            b_de = dict_dbar[num_de]
            b_para = dict_dbar[num_para]

            # Fasores complexos de tensão (módulo * e^(j*ângulo))
            # Usa a precisão completa do solver para calcular correntes e fluxos
            Vk = mapa_v_exato[num_de]
            Vm = mapa_v_exato[num_para]
            Ek = Vk * np.exp(1j * mapa_t_exato[num_de])
            Em = Vm * np.exp(1j * mapa_t_exato[num_para])

            r_pu = float(dados["resistencia"]) / 100.0
            x_pu = float(dados["reatancia"]) / 100.0
            b_sh_pu = (float(dados["susceptancia"]) / 2.0) / s_base

            tap_val = float(dados["tap"]) 
            defas_deg = float(dados["defasagem"]) 
            phikm = np.deg2rad(defas_deg)

            capacidade_nominal = float(dados["capacidade_normal"]) 
            capacidade_emergencia = float(dados["capacidade_em_emergencia"]) 
            capacidade_do_equipamento = float(dados["capacidade_do_equipamento"]) 

            estado_operativo = MAPA_ESTADO.get(str(dados["estado"]).strip(), "LIG")
            estado_operativo_lado_de = MAPA_ESTADO.get(str(dados.get("abertura_da_barra", "L")).strip(), "LIG")
            estado_operativo_lado_para = MAPA_ESTADO.get(str(dados.get("abertura_para_barra", "L")).strip(), "LIG")

            is_tie = 0 if b_de["Área"] != b_para["Área"] else 1

            if estado_operativo == "LIG":
                z_serie = r_pu + 1j * x_pu
                ykm = 1.0 / z_serie if abs(z_serie) > 0 else 0.0 + 0.0j
                y_sh = 1j * b_sh_pu

                ikm = i_km(tap_val, ykm, y_sh, Ek, phikm, Em)
                imk = i_mk(tap_val, ykm, y_sh, Ek, phikm, Em)

                skm = s_km(Ek, ikm)
                smk = s_mk(Em, imk)
                perda_complexa = s_perda(smk, skm)
            else:
                skm = 0.0 + 0.0j
                smk = 0.0 + 0.0j
                perda_complexa = 0.0 + 0.0j

            s_fluxo_pct_km = fluxo_percentual(abs(skm), capacidade_nominal)
            s_fluxo_pct_mk = fluxo_percentual(abs(smk), capacidade_nominal)

            s_fluxo_pct_v_km = fluxo_percentual_v(s_fluxo_pct_km, Vk)
            s_fluxo_pct_v_mk = fluxo_percentual_v(s_fluxo_pct_mk, Vm)

            # Sentido 1: DE -> PARA
            registrar_fluxo(
                num_de, num_para, circ, skm, s_fluxo_pct_km, s_fluxo_pct_v_km,
                capacidade_nominal, capacidade_emergencia, capacidade_do_equipamento,
                tap_val, defas_deg, is_tie, perda_complexa.real, perda_complexa.imag,
                estado_operativo, estado_operativo_lado_de, estado_operativo_lado_para
            )

            # Sentido 2: PARA -> DE
            registrar_fluxo(
                num_para, num_de, circ, smk, s_fluxo_pct_mk, s_fluxo_pct_v_mk,
                capacidade_nominal, capacidade_emergencia, capacidade_do_equipamento,
                tap_val, defas_deg, is_tie, perda_complexa.real, perda_complexa.imag,
                estado_operativo, estado_operativo_lado_para, estado_operativo_lado_de
            )

        df_rlin = pd.DataFrame({
            "Número Barra DE"                  : numero_barra_de,
            "Nome Barra DE"                    : nome_barra_de,
            "Número Área DE"                   : numero_area_de,
            "Tipo"                             : tipo,
            "Tensão (kV)"                      : tensao_kv,
            "Tensão (p.u.)"                    : tensao_pu,
            "Ângulo (graus)"                   : angulo_graus,
            "Geração Ativa (MW)"               : geracao_ativa_mw,
            "Geração Reativa (Mvar)"           : geracao_reativa_mvar,
            "Injeção Equivalente (MW)"         : injecao_equivalente_mw,
            "Injeção Equivalente (Mvar)"       : injecao_equivalente_mvar,
            "Carga Ativa (MW)"                 : carga_ativa_mw,
            "Carga Reativa (Mvar)"             : carga_reativa_mvar,
            "Potência Ativa Elo CC (MW)"       : potencia_ativa_elo_cc_mw,
            "Potência Reativa Elo CC (Mvar)"   : potencia_reativa_elo_cc_mvar,
            "Motor de Indução (MW)"            : motor_de_inducao_mw,
            "Motor de Indução (Mvar)"          : motor_de_inducao_mvar,
            "Número Barra PARA"                : numero_para_barra,
            "Nome Barra PARA"                  : nome_barra_para,
            "Número Área PARA"                 : numero_area_para,
            "Número do Circuito"               : numero_do_circuito,
            "Fluxo (MW)"                       : fluxo_mw,
            "Fluxo (Mvar)"                     : fluxo_mvar,
            "Fluxo (MVA)"                      : fluxo_mva,
            "Fluxo (%)"                        : fluxo_pct_list,
            "Fluxo (%)/Tensão Barra DE"        : fluxo_pct_v_list,
            "Capac. Aparente Nominal (MVA)"    : cap_nominal_list,
            "Capac. Aparente Emergência (MVA)" : cap_emergencia_list,
            "Capac. Equipamento (MVA)"         : cap_equipamento_list,
            "TAP (p.u.)"                       : tap_list,
            "Defasamento (graus)"              : defasagem_list,
            "Tie-Line"                         : tie_line_list,
            "Perda Ativa (MW)"                 : perda_ativa_list,
            "Perda Reativa (Mvar)"             : perda_reativa_list,
            "Tensão Circuito Aberto (p.u.)"    : tensao_ca_list,
            "Ângulo Circuito Aberto (p.u.)"    : angulo_ca_list,
            "Estado Operativo"                 : estado_op_list,
            "Estado Operativo - Lado DE"       : estado_de_list,
            "Estado Operativo - Lado PARA"     : estado_para_list,
        })

        cols_float = df_rlin.select_dtypes(include="float").columns
        df_rlin[cols_float] = df_rlin[cols_float].map(r)

        

        net.RLIN = df_rlin
                
    
    
    
    @classmethod
    def rger(cls, net):
        # : dict          = net.DadosRede.cte
        dbar: pd.DataFrame = net.DadosRede.dbarDF
        dger: pd.DataFrame = net.DadosRede.dgerDF
        RBAR = net.RBAR
        data               = net.data
        bus_type           = data.bus_type
        idx_q              = set(data.idx_q)
        bus_map            = data.bus_map
        inv_bus_map        = {v: k for k, v in bus_map.items()}


        dbar_dict = dbar.set_index("numero").to_dict(orient="index")
        dger_dict = dger.set_index("numero").to_dict(orient="index") 
        RBAR_dict = RBAR.set_index("Número").to_dict(orient="index") 

        linhas = []

        for idx, btype in enumerate(bus_type):
            
            num_barra = inv_bus_map[idx]
            row_rbar  = RBAR_dict[num_barra]
            tipo_barra = row_rbar["Tipo da Barra"]
            
            if tipo_barra not in [1, -1, 2, -3]: 
                continue 
            
            
            if tipo_barra in [-3, 2]:
                if tipo_barra == -3:
                    row_dger  = {
                        "geracao_ativa_minima": 0.0,
                        "geracao_ativa_maxima": 99999,
                        "fator_de_participacao": 0.0
                    }
                else:
                    row_dger  = {
                        "geracao_ativa_minima": 0.0,
                        "geracao_ativa_maxima": 9999,
                        "fator_de_participacao": 0.0
                    }
                
            elif tipo_barra in [1, -1]:
                row_dger  = dger_dict.get(num_barra)
            
            row_dbar  = dbar_dict[num_barra]
            row_rbar  = RBAR_dict.get(num_barra)

            v_pu    = row_rbar.get("Tensão (p.u.)")
            ang_deg = row_rbar.get("Ângulo (graus)")
            pg      = row_rbar.get("Geração Ativa (MW)")
            pmin    = row_dger.get("geracao_ativa_minima")
            pmax    = row_dger.get("geracao_ativa_maxima")

            qg      = row_rbar.get("Geração Reativa (Mvar)")
            qmin    = row_dbar["geracao_reativa_minima"]
            qmax    = row_dbar["geracao_reativa_maxima"]

            if np.isclose(pg, pmin, atol=1e-3): lim_ati = "I"
            elif np.isclose(pg, pmax, atol=1e-3): lim_ati = "S"
            else: lim_ati = ""

            if np.isclose(qg, qmin, atol=1e-3): lim_rea = "I"
            elif np.isclose(qg, qmax, atol=1e-3): lim_rea = "S"
            else: lim_rea = ""

            barra_cont = int(row_dbar["barra_controlada"])
            parti_ger  = float(row_dger.get("fator_de_participacao"))

            linhas.append({
                "Número da Barra"           : num_barra,
                "Nome da Barra"             : row_dbar["nome"],
                "Tipo da Barra"             : tipo_barra,
                "Tensão (p.u.)"             : v_pu,
                "Ângulo (graus)"            : ang_deg,
                "Geração Ativa Min(MW)"     : pmin,
                "Geração Ativa (MW)"        : pg,
                "Geração Ativa Max(MW)"     : pmax,
                "Geração Reativa Min (Mvar)": qmin,
                "Geração Reativa (Mvar)"    : qg,
                "Geração Reativa Max (Mvar)": qmax,
                "Limite Ativo (MW)"         : lim_ati,
                "Limite Reativo (Mvar)"     : lim_rea,
                "Participação Geração"      : parti_ger,
                #"Participação Equivalente"  : 0.0,
                "Barra Controlada"          : barra_cont,
                #"Barra Controlada (MVA)"    : float(barra_cont),
                "Estado Operativo"          : MAPA_ESTADO.get(row_dbar["estado"]),
            })

        df_rger = pd.DataFrame(linhas)

        if not df_rger.empty:
            cols_float = df_rger.select_dtypes(include="float").columns
            df_rger[cols_float] = df_rger[cols_float].map(r)

        net.RGER = df_rger
        
        
        
        
    @classmethod
    def rgel(cls, net):
        # : dict          = net.DadosRede.cte
        dbar: pd.DataFrame = net.DadosRede.dbarDF
        dger: pd.DataFrame = net.DadosRede.dgerDF
        RBAR = net.RBAR
        data               = net.data
        bus_type           = data.bus_type
        idx_q              = set(data.idx_q)
        bus_map            = data.bus_map
        inv_bus_map        = {v: k for k, v in bus_map.items()}


        dbar_dict = dbar.set_index("numero").to_dict(orient="index")
        dger_dict = dger.set_index("numero").to_dict(orient="index") 
        RBAR_dict = RBAR.set_index("Número").to_dict(orient="index") 

        linhas = []

        for idx, btype in enumerate(bus_type):
                    
            num_barra = inv_bus_map[idx]
            row_rbar  = RBAR_dict[num_barra]
            tipo_barra = row_rbar["Tipo da Barra"]
            
            if tipo_barra not in [-1, -3]: 
                continue 
            
            
            if tipo_barra in [-3]:
                row_dger  = {
                    "geracao_ativa_minima": 0.0,
                    "geracao_ativa_maxima": 99999,
                    "fator_de_participacao": 0.0
                }
                
            elif tipo_barra in [-1]:
                row_dger  = dger_dict.get(num_barra)
            
            row_dbar  = dbar_dict[num_barra]
            row_rbar  = RBAR_dict.get(num_barra)

            v_pu    = row_rbar.get("Tensão (p.u.)")
            ang_deg = row_rbar.get("Ângulo (graus)")
            pg      = row_rbar.get("Geração Ativa (MW)")
            pmin    = row_dger.get("geracao_ativa_minima")
            pmax    = row_dger.get("geracao_ativa_maxima")

            qg      = row_rbar.get("Geração Reativa (Mvar)")
            qmin    = row_dbar["geracao_reativa_minima"]
            qmax    = row_dbar["geracao_reativa_maxima"]

            if np.isclose(pg, pmin, atol=1e-3): lim_ati = "I"
            elif np.isclose(pg, pmax, atol=1e-3): lim_ati = "S"
            else: lim_ati = ""

            if np.isclose(qg, qmin, atol=1e-3): lim_rea = "I"
            elif np.isclose(qg, qmax, atol=1e-3): lim_rea = "S"
            else: lim_rea = ""

            barra_cont = int(row_dbar["barra_controlada"])
            parti_ger  = float(row_dger.get("fator_de_participacao"))

            linhas.append({
                "Número da Barra"           : num_barra,
                "Nome da Barra"             : row_dbar["nome"],
                "Tipo da Barra"             : tipo_barra,
                "Tensão (p.u.)"             : v_pu,
                "Ângulo (graus)"            : ang_deg,
                "Geração Ativa Min(MW)"     : pmin,
                "Geração Ativa (MW)"        : pg,
                "Geração Ativa Max(MW)"     : pmax,
                "Geração Reativa Min (Mvar)": qmin,
                "Geração Reativa (Mvar)"    : qg,
                "Geração Reativa Max (Mvar)": qmax,
                "Limite Ativo (MW)"         : lim_ati,
                "Limite Reativo (Mvar)"     : lim_rea,
                "Participação Geração"      : parti_ger,
                #"Participação Equivalente"  : 0.0,
                "Barra Controlada"          : barra_cont,
                #"Barra Controlada (MVA)"    : float(barra_cont),
                "Estado Operativo"          : MAPA_ESTADO.get(row_dbar["estado"]),
            })

        df_rgel = pd.DataFrame(linhas)

        if not df_rgel.empty:
            cols_float = df_rgel.select_dtypes(include="float").columns
            df_rgel[cols_float] = df_rgel[cols_float].map(r)

        net.RGEL = df_rgel
                    