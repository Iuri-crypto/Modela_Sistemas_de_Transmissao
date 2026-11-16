
from numpy import dtype 


def get_struture_dict() -> dict:
    """
    Esta função retorna um dicionário da estrutura da rede
    """
    
    return {
        "bus": {
            "name": dtype(object),
            "vn": "f8",
            'numero': "UInt32",
            'tipo': dtype(object),
            "in_service": "bool",
        },
        
        "load": {
            "name": dtype(object),
            "bus": "UInt32",
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
            "bus": "UInt32",
            "p_mw": "f8",
            "vm": "f8",
            "sn_mva": "f8",
            "in_service": "bool",
        },
        
        "shunt": {
            "bus": "UInt32",
            "name": dtype(object),
            "q_mvar": "f8",
            "p_mw": "f8",
            "vn": "f8",
            "in_service": "bool"
        },
        
        "ext_grid": {
            "name": dtype(object),
            "bus": "UInt32",
            "vm_pu": "f8",
            "va_degree": "f8",
        },
        
        "line": {
            "name": dtype(object),
            "from_bus": "UInt32",
            "to_bus": "UInt32",
            "length_km": "f8",
            "r_percent": "f8",
            "x_percent": "f8",
            "b_percent": "f8",
            "in_service": "bool",
        },
        
        "trafo": {
            "name": dtype(object),
            "from_bus": "UInt32",
            "to_bus": "UInt32",
            "r_percent": "f8",
            "x_percent": "f8",
            "b_percent": "f8",
            "shift_degree": "f8",
            "tap_min": "f8",
            "tap_max": "f8",
            "num_taps": "f8",
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