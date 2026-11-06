
from numpy import dtype 


def get_struture_dict() -> dict:
    """
    Esta função retorna um dicionário da estrutura da rede
    """
    
    return {
        "bus": {
            "name": dtype(object),
            "vn_kv": "f8",
            "in_service": "bool",
        },
        
        "load": {
            "name": dtype(object),
            "bus": "u4",
            "p_mw": "f8",
            "q_mvar": "f8",
            "const_z_p_percent": "f8",
            "const_i_p_percent": "f8",
            "const_z_q_percent": "f8",
            "const_i_q_percent": "f8",
            "in_service": "bool",
        },
        
        "gen": {
            "name": dtype(object),
            "bus": "u4",
            "p_mw": "f8",
            "vm_pu": "f8",
            "sn_mva": "f8",
            "in_service": "bool",
        },
        
        "shunt": {
            "bus": "u4",
            "name": dtype(object),
            "q_mvar": "f8",
            "p_mw": "f8",
            "vn_kv": "f8",
            "in_service": "bool"
        },
        
        "ext_grid": {
            "name": dtype(object),
            "bus": "u4",
            "vm_pu": "f8",
            "va_degree": "f8",
        },
        
        "line": {
            "name": dtype(object),
            "from_bus": "u4",
            "to_bus": "u4",
            "length_km": "f8",
            "r_ohm_per_km": "f8",
            "x_ohm_per_km": "f8",
            "c_nf_per_km": "f8",
            "in_service": "bool",
        },
        
        "trafo": {
            "name": dtype(object),
            "hv_bus": "u4",
            "lv_bus": "u4",
            "sn_mva": "f8",
            "vn_hv_kv": "f8",
            "vn_lv_kv": "f8",
            "vk_percent": "f8",
            "vkr_percent": "f8",
            "pfe_kw": "f8",
            "i0_percent": "f8",
            "shift_degree": "f8",
            "tap_side": dtype(object),
            "tap_neutral": "f8",
            "tap_min": "f8",
            "tap_max": "f8",
            "tap_step_percent": "f8",
            "tap_step_degree": "f8",
            "tap_pos": "f8",
            "in_service": "bool",
        },
        
        # Tabelas vazias de resultados
        #=================================================
        "_empty_res_bus": {
            "vm_pu": "f8",
            "va_degree": "f8",
            "p_mw": "f8",
            "q_mvar": "f8",
        },
        
        "_empty_res_ext_grid": {
            "p_mw": "f8",
            "q_mvar": "f8",
        },
        
        "_empty_res_line": {
            "p_from_mw": "f8",
            "q_from_mvar": "f8",
            "p_to_mw": "f8",
            "q_to_mvar": "f8",
        },
        
        "_empty_res_trafo": {
            "p_hv_mw": "f8",
            "q_hv_mvar": "f8",
            "p_lv_mw": "f8",
            "q_lv_mvar": "f8",
        },
        
        "_empty_res_load": {
            "p_mw": "f8",
            "q_mvar": "f8",
        },
        
        "_empty_res_shunt": {
            "p_mw": "f8",
            "q_mvar": "f8",
            "vm_pu": "f8",
        },
        
        "_empty_res_gen": {
            "p_mw": "f8",
            "q_mvar": "f8",
            "va_degree": "f8",
            "vm_pu": "f8",
        },
        
        "name": "",
        "f_hz": 60.0,
        "sn_mva": 100.0
    }