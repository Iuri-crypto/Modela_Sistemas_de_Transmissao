


from EnlineDevEng.utils.auxiliary import PowerSystemsNet
from EnlineDevEng.utils.populate import _set_entries



def create_trafo(
    net: PowerSystemsNet,
    name: str,
    hv_bus: float,
    lv_bus: float,
    sn_mva: float,
    vn_hv_kv: float,
    vn_lv_kv: float,
    vk_percent: float,
    vkr_percent: float,
    pfe_kw: float,
    i0_percent: float,
    shift_degree: float,
    tap_side: str,
    tap_neutral: float,
    tap_min: float,
    tap_max: float,
    tap_step_percent: float,
    tap_step_degree: float,
    tap_pos: float,
    in_service: bool = True
):
    
    """
    Adiciona um transformador na tabela net["trafo"].
    
    Parâmetros:
        net: A rede PowerSystems em que o elemento é criado
        name: Nome do transformador
        hv_bus: ID da barra em alta tensão que o trafo é conectado.
        lv_bus: ID da barra de baixa tensão que o trafo é conectado.
        sn_mva: Potência aparente.
        vn_hv_kv: Tensão no lado de alta tensão.
        vn_lv_kv: Tensão no lado de baixa tensão.
        vk_percent: Tensão de curto circuito relativa.
        vkr_percent: parte real da tensão de curto circuito.
        pfe_kw: Perdas no ferro em kw.
        i0_percent: Perdas em malha aberta em percentual da corrente nominal.
        shift_degree: Ângulo de defasagem do transformador.
        tap_side: Posição do comutador de taps ("hv", "lv").
        tap_neutral: Posição do tap na qual a relação de transformação é igual à relação entre as tensões nominais.
        tap_max: Posição máxima permitida para o tap.
        tap_min: Posição miníma permitida para o tap.
        tap_step_percent: Tamanho do passo do tap para a magnitude da tensão em percentual.
        tap_step_degree: Tamanho do passo do tap para o ângulo de fase.
        tap_pos: Posição atual do tap. O padrão é a posição neutra.
        in_service: True se o trafo estiver em operação, 
                    False se estiver fora de operação.
                    
    Returns:
        None 
    
    Example:
        >>> create_transformer_from_parameters(
        >>>     net, hv_bus=0, lv_bus=1, name="trafo1", sn_mva=40, vn_hv_kv=110, vn_lv_kv=10, vk_percent=10,
        >>>     vkr_percent=0.3, pfe_kw=30, i0_percent=0.1, shift_degree=30
        >>> )
    """
    
    entries = {
        "name": name,
        "hv_bus": hv_bus,
        "lv_bus": lv_bus,
        "sn_mva": sn_mva,
        "vn_hv_kv": vn_hv_kv,
        "vn_lv_kv": vn_lv_kv,
        "vk_percent": vk_percent,
        "vkr_percent": vkr_percent,
        "pfe_kw": pfe_kw,
        "i0_percent": i0_percent,
        "shift_degree": shift_degree,
        "tap_side": tap_side,
        "tap_neutral": tap_neutral,
        "tap_min": tap_min,
        "tap_max": tap_max,
        "tap_step_percent": tap_step_percent,
        "tap_step_degree": tap_step_degree,
        "tap_pos": tap_pos,
        "in_service": in_service
    }
    
    _set_entries(net, "trafo", entries=entries)