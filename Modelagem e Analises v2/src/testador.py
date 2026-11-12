



import EnlineDevEng as ede 


net = ede.create_empty_network(
    name="IEEE 14", 
    f_hz=60.0,
    sn_mva=100.0
)


ede.create_bus(
    net=net, 
    vn_kv=138.0,
    name="BARRA 01",
    in_service=True
)

ede.create_ext_grid(
    net=net,
    name="Slack",
    bus=1,
    vm_pu=1.0,
    va_degree=0.0
)

ede.create_line(
    net=net,
    name="Linha_01",
    from_bus=1,
    to_bus=2,
    length_km=1.0,
    r_ohm_per_km=0.1,
    x_ohm_per_km=0.5,
    c_nf_per_km=5.0,
    in_service=True
)



ede.create_gen(
    net=net,
    name="Gerador_01",
    bus=2,
    p_mw=5.0,
    vm_pu=1.0,
    sn_mva=6.0,
    in_service=True
)


ede.create_load(
    net=net,
    name="Carga_01",
    bus=2,
    p_mw=1.0,
    q_mvar=0.2,
    const_i_p_percent=0.0,
    const_i_q_percent=0.0,
    const_z_p_percent=0.0,
    const_z_q_percent=0.0,
    in_service=True
)

ede.create_shunt(
    net=net,
    bus=2,
    q_mvar=0.2,
    vn_kv=138.0,
    p_mw=0.0,
    name="Shunt_01",
    in_service=True
)


ede.create_trafo(
    net=net,
    name="TRAFO_01",
    hv_bus=2,
    lv_bus=3,
    sn_mva=10,
    vn_hv_kv=138.0,
    vn_lv_kv=69.0,
    vk_percent=1.0,
    vkr_percent=0.8,
    pfe_kw=50,
    i0_percent=0.1,
    shift_degree=0.0,
    tap_side="hv",
    tap_neutral=1.0,
    tap_max=1.1,
    tap_min=0.9,
    tap_step_percent=0.625,
    tap_step_degree=0.1,
    tap_pos=1.0,
    in_service=True
)

ede.runpf(
    net=net,
    algorithm="nr"
)



# Segunda opção
##########################################
import EnlineDevEng as ede 


file = "C:\Users\muril\OneDrive\Documentos\Estagio ENLINE - atividades\Modelagem e Analises v2\src\tests\ieee14_v1.pwf"
ede.runpf(
    net=net,
    dir_file=file,
    algorithm="nr"
)
##########################################

print(net)

































import pandapower as pp


net = pp.create_empty_network()
pp.runpp()