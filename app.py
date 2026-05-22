import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN E IDENTIDAD VISUAL CORPORATIVA WILTEL
st.set_page_config(page_title="Pricing Wiltel", layout="wide", initial_sidebar_state="expanded")

# Inyección de estilos CSS
st.markdown("""
    <style>
    .main { background-color: #f4f6f9; }
    [data-testid="stSidebar"] { background-color: #003366; min-width: 300px; }
    .sidebar-title {
        color: #ffffff !important;
        font-family: 'Arial', sans-serif;
        font-size: 16px;
        font-weight: 600;
        text-align: center;
        padding: 20px 5px;
        border-bottom: 1px solid #4a5568;
        margin-bottom: 20px;
    }
    .wiltel-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 4px;
        border-top: 3px solid #d1d5db;
        margin-bottom: 25px;
    }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #ffffff !important;
        font-size: 14px !important;
    }
    .stSlider > div [data-baseweb="slider"] { background-color: #ff823a; }
    .ref-text { font-size: 12px; color: #6b7280; font-style: italic; }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZACIÓN DE DATOS CON CONTROL DE ESTADO ---
# Usamos session_state para que los cambios en tablas impacten de inmediato

if 'comercial_params' not in st.session_state:
    st.session_state.comercial_params = {"tc": 1420.0, "pb_objetivo": 6, "costo_fact": 8.0, "pct_recupero_obj": 35.0}

if 'db_internet' not in st.session_state: st.session_state.db_internet = ["WILTEL 25 MB", "WILTEL 50 MB", "WILTEL 150 MB", "WILTEL 300 MB", "Ninguno"]
if 'db_tv' not in st.session_state: st.session_state.db_tv = ["Ninguno", "WILTEL TV HD", "FULL TV HD", "PLAYME TV HD", "PLAYME FULL BOX"]
if 'db_telefonia' not in st.session_state: st.session_state.db_telefonia = ["Ninguno", "Línea Hogar Básica"]
if 'db_adicionales' not in st.session_state: st.session_state.db_adicionales = ["WILTEL ON", "MESH", "PAQUETE FUTBOL", "PAQUETE TV PREMIUM"]

if 'db_equipos' not in st.session_state:
    st.session_state.db_equipos = [
        {"Equipo": "ONT GPON ZXHN F6201B", "Costo USD": 35.60, "IVA %": 21.0},
        {"Equipo": "ONT GPON ZXHN F6600R", "Costo USD": 49.40, "IVA %": 21.0},
        {"Equipo": "ONT GPON ZXHN F601", "Costo USD": 24.50, "IVA %": 21.0},
        {"Equipo": "STB mod HC-C730 (Beacon)", "Costo USD": 35.00, "IVA %": 21.0},
        {"Equipo": "DONGLE WILTEL ON", "Costo USD": 28.60, "IVA %": 21.0},
        {"Equipo": "MINI UPS WILTEL ON", "Costo USD": 20.67, "IVA %": 21.0},
        {"Equipo": "ZXHN H3601N (Router)", "Costo USD": 35.60, "IVA %": 21.0},
        {"Equipo": "Tenda NOVA MX3", "Costo USD": 28.41, "IVA %": 21.0}
    ]

if 'mat_ftth' not in st.session_state:
    st.session_state.mat_ftth = [{"Ítem": "DROP FTTH", "Cantidad": 150.0, "Costo Unitario USD": 0.044, "IVA %": 21.0}, {"Ítem": "CONECTOR RAPIDO", "Cantidad": 2.0, "Costo Unitario USD": 1.20, "IVA %": 21.0}]
if 'mat_coaxil' not in st.session_state:
    st.session_state.mat_coaxil = [{"Ítem": "CABLE RG-6", "Cantidad": 20.0, "Costo Unitario USD": 0.31, "IVA %": 21.0}, {"Ítem": "FICHA COMPRESION", "Cantidad": 4.0, "Costo Unitario USD": 0.80, "IVA %": 21.0}]

if 'db_costos_directos' not in st.session_state:
    st.session_state.db_costos_directos = [
        {"Concepto": "Tránsito IP x Mega", "Costo Mensual USD": 1.50, "Asociado a": "Internet"},
        {"Concepto": "Derechos Señales TV", "Costo Mensual USD": 8.50, "Asociado a": "TV"},
        {"Concepto": "Chip Datos Wiltel On", "Costo Mensual USD": 5.00, "Asociado a": "WILTEL ON"}
    ]

if 'reglas_tecnicas' not in st.session_state:
    st.session_state.reglas_tecnicas = [
        {"Internet": "Cualquiera", "TV": "Ninguno", "Adicional": "Ninguno", "Acción": "ASIGNAR", "Ítem": "ONT GPON ZXHN F6201B"},
        {"Internet": "Cualquiera", "TV": "WILTEL TV HD", "Adicional": "Ninguno", "Acción": "UPGRADE", "Ítem": "ONT GPON ZXHN F6600R"}
    ]

# --- MENÚ LATERAL ---
with st.sidebar:
    st.markdown('<div class="sidebar-title">Wiltel Comunicaciones S.A.</div>', unsafe_allow_html=True)
    opcion_menu = st.radio("", ["Simulación Comercial", "Tablero Administración Comercial", "Tablero Administración Técnica", "Tablero Administración de Costos"])

# Funciones globales
def fmt_ars(v): return f"$ {v:,.2f}"
def fmt_usd(v): return f"USD {v:,.2f}"

# ==============================================================================
# 1- SIMULACIÓN COMERCIAL
# ==============================================================================
if opcion_menu == "Simulación Comercial":
    st.title("Simulación Comercial")
    
    # Tarjeta 1: Configuración
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Configuración Comercial")
    col1, col2 = st.columns(2)
    with col1: segmento = st.selectbox("Segmento de Cliente", ["B2C", "B2B"])
    with col2:
        moneda_opts = ["Pesos ARS"] if segmento == "B2C" else ["Pesos ARS", "Dólares USD"]
        moneda = st.selectbox("Moneda de Cotización", moneda_opts)
    st.markdown('</div>', unsafe_allow_html=True)

    # Tarjeta 2: Combo
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Combo")
    c1, c2, c3 = st.columns(3)
    with c1: prod_int = st.selectbox("Internet", st.session_state.db_internet, index=2)
    with c2: prod_tv = st.selectbox("TV", st.session_state.db_tv, index=0)
    with c3: prod_tel = st.selectbox("Telefonía", st.session_state.db_telefonia, index=0)
    
    st.markdown("**Adicionales Disponibles**")
    a1, a2, a3, a4 = st.columns(4)
    with a1: add_on = st.checkbox("WILTEL ON")
    with a2: add_mesh = st.checkbox("MESH")
    with a3: add_futbol = st.checkbox("PAQUETE FÚTBOL")
    with a4: add_premium = st.checkbox("PAQUETE TV PREMIUM")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- CÁLCULOS TÉCNICOS (3 CAPAS) ---
    tc = st.session_state.comercial_params["tc"]
    costo_fact_local = st.session_state.comercial_params["costo_fact"] / 100.0
    pb_obj_local = st.session_state.comercial_params["pb_objetivo"]
    
    eq_cost = {x['Equipo']: x['Costo USD'] for x in st.session_state.db_equipos}
    eq_iva = {x['Equipo']: x['IVA %']/100 for x in st.session_state.db_equipos}
    
    costo_hw_usd, iva_hw_usd = 0.0, 0.0
    lleva_coaxil = False

    # Lógica simplificada de capas (se nutre de las reglas de la pestaña técnica)
    if prod_tv != "Ninguno":
        ont = "ONT GPON ZXHN F6600R"
        lleva_coaxil = True
        if prod_tv == "FULL TV HD":
            costo_hw_usd += eq_cost.get("STB mod HC-C730 (Beacon)", 35.0)
            iva_hw_usd += 35.0 * 0.21
    elif "150 MB" in prod_int and add_mesh:
        ont = "ONT GPON ZXHN F601"
    else:
        ont = "ONT GPON ZXHN F6201B" if prod_int != "Ninguno" else "Ninguno"

    if ont != "Ninguno":
        c_ont = eq_cost.get(ont, 0.0)
        costo_hw_usd += c_ont
        iva_hw_usd += c_ont * eq_iva.get(ont, 0.21)

    if add_on:
        costo_hw_usd += eq_cost.get("DONGLE WILTEL ON", 28.6) + eq_cost.get("MINI UPS WILTEL ON", 20.67)
        iva_hw_usd += (28.6 + 20.67) * 0.21
    if add_mesh:
        if "150 MB" in prod_int and prod_tv == "Ninguno":
            costo_hw_usd += eq_cost.get("Tenda NOVA MX3", 28.41) * 2
            iva_hw_usd += (28.41 * 2) * 0.21
        else:
            costo_hw_usd += eq_cost.get("ZXHN H3601N (Router)", 35.6)
            iva_hw_usd += 35.6 * 0.21

    # Packs
    neto_f = sum(x['Cantidad'] * x['Costo Unitario USD'] for x in st.session_state.mat_ftth)
    iva_f = sum(x['Cantidad'] * x['Costo Unitario USD'] * (x['IVA %']/100) for x in st.session_state.mat_ftth)
    neto_c = sum(x['Cantidad'] * x['Costo Unitario USD'] for x in st.session_state.mat_coaxil) if lleva_coaxil else 0
    iva_c = sum(x['Cantidad'] * x['Costo Unitario USD'] * (x['IVA %']/100) for x in st.session_state.mat_coaxil) if lleva_coaxil else 0

    total_n_usd = 47.36 + costo_hw_usd + neto_f + neto_c # 47.36 es MO
    total_i_usd = (47.36 * 0.21) + iva_hw_usd + iva_f + iva_c
    iva_p = (total_i_usd / total_n_usd) if total_n_usd > 0 else 0.21
    
    inversion_l_neta = total_n_usd * tc if moneda == "Pesos ARS" else total_n_usd
    iva_factor = (1.0 + iva_p) if segmento == "B2C" else 1.0
    inversion_con_iva = inversion_l_neta * iva_factor

    # Tarjeta 3: Oferta
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Combinación de Oferta")
    p1, p2 = st.columns(2)
    divisor = (1.0 - costo_fact_local)

    with p1:
        pct_rec = st.slider("% Inversión a recuperar", 0, 100, int(st.session_state.comercial_params["pct_recupero_obj"]))
        c_inst = (inversion_l_neta * (pct_rec/100) / divisor) * iva_factor
        st.write(f"### **Costo de Instalación:** {fmt_ars(c_inst) if moneda=='Pesos ARS' else fmt_usd(c_inst)}")
        st.markdown(f"<p class='ref-text'>Calculado sobre inversión de {fmt_ars(inversion_con_iva) if moneda=='Pesos ARS' else fmt_usd(inversion_con_iva)} (IVA incluido)</p>", unsafe_allow_html=True)

    # Equilibrio
    saldo_a = inversion_l_neta * (1 - (pct_rec/100))
    # Sumar costos directos desde la tabla de Tab 4
    c_dir_neto = 0
    for cd in st.session_state.db_costos_directos:
        if (cd["Asociado a"] == "Internet" and prod_int != "Ninguno") or \
           (cd["Asociado a"] == "TV" and prod_tv != "Ninguno") or \
           (cd["Asociado a"] == cd["Asociado a"] and add_on and cd["Asociado a"] == "WILTEL ON"):
            c_dir_neto += cd["Costo Mensual USD"]
    
    c_dir_local = c_dir_neto * (tc if moneda=="Pesos ARS" else 1.0)
    ing_n_necesario = (saldo_a / pb_obj_local) + c_dir_local
    eq_final = (ing_n_necesario / divisor) * iva_factor

    with p2:
        abono_l = st.slider("Abono Mensual Regular de Lista", 5000, 180000, 39400, step=100)
        st.write(f"### **Abono Mínimo sugerido (Equilibrio):** {fmt_ars(eq_final) if moneda=='Pesos ARS' else fmt_usd(eq_final)}")
        st.markdown(f"<p class='ref-text'>Balancea la instalación y el payback en {pb_obj_local} meses (IVA Incluido).</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Tarjeta 4: Escalas
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Configuración de Escalas Promocionales")
    t1, t2, t3, t4 = st.columns(4)
    with t1:
        st.markdown("**Tramo 1**")
        m1 = st.selectbox("duración (meses)", [0,1,2,3,4,6,12], index=3, key="m1")
        d1 = st.slider("descuento", 0, 100, 40, key="d1")
    with t2:
        st.markdown("**Tramo 2**")
        m2 = st.selectbox("duración (meses)", [0,1,2,3,4,6,12], index=0, key="m2")
        d2 = st.slider("descuento", 0, 100, 20, key="d2")
    with t3:
        st.markdown("**Tramo 3**")
        m3 = st.selectbox("duración (meses)", [0,1,2,3,4,6,12], index=0, key="m3")
        d3 = st.slider("descuento", 0, 100, 0, key="d3")
    with t4:
        st.markdown("**Tramo 4**")
        m4 = st.selectbox("duración (meses)", [0,1,2,3,4,6,12], index=0, key="m4")
        d4 = st.slider("descuento", 0, 100, 0, key="d4")
    st.markdown('</div>', unsafe_allow_html=True)

    # SIMULACIÓN PAYBACK
    s_flujo = saldo_a
    pb_r = 0.0
    for mes in range(1, 49):
        if s_flujo <= 0: break
        if mes <= m1: cur_d = d1
        elif mes <= (m1+m2): cur_d = d2
        elif mes <= (m1+m2+m3): cur_d = d3
        elif mes <= (m1+m2+m3+m4): cur_d = d4
        else: cur_d = 0
        
        neto_m = (abono_l * (1-(cur_d/100)) / iva_factor) * divisor
        limpre = neto_m - c_dir_local
        if limpre > 0:
            if s_flujo > limpre:
                s_flujo -= limpre
                pb_r += 1
            else:
                pb_r += (s_flujo / limpre)
                s_flujo = 0
        else:
            pb_r = 99; break

    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Validación Comercial")
    if pb_r <= pb_obj_local: st.success(f"🟢 APROBADO | Payback Real: {pb_r:.1f} meses")
    else: st.error(f"🔴 RECHAZADO | Payback Real: {pb_r:.1f} meses")
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 2- ADMINISTRACIÓN COMERCIAL (Grid 2x2)
# ==============================================================================
elif opcion_menu == "Tablero Administración Comercial":
    st.title("Administración Comercial")
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Parámetros Estratégicos")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.session_state.comercial_params["tc"] = st.number_input("Tipo de Cambio", value=st.session_state.comercial_params["tc"])
    with c2: st.session_state.comercial_params["pb_objetivo"] = st.number_input("Payback Objetivo", value=st.session_state.comercial_params["pb_objetivo"])
    with c3: st.session_state.comercial_params["costo_fact"] = st.number_input("Carga Facturación (%)", value=st.session_state.comercial_params["costo_fact"])
    with c4: st.session_state.comercial_params["pct_recupero_obj"] = st.number_input("% Recupero Inversión", value=st.session_state.comercial_params["pct_recupero_obj"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Opciones de Productos")
    r1, r2 = st.columns(2)
    with r1:
        st.write("**Internet**")
        df_int = st.data_editor(pd.DataFrame(st.session_state.db_internet, columns=["Producto"]), num_rows="dynamic", key="ed_i")
        st.session_state.db_internet = df_int["Producto"].tolist()
        st.write("**Telefonía**")
        df_tel = st.data_editor(pd.DataFrame(st.session_state.db_telefonia, columns=["Producto"]), num_rows="dynamic", key="ed_tel")
        st.session_state.db_telefonia = df_tel["Producto"].tolist()
    with r2:
        st.write("**TV**")
        df_tv = st.data_editor(pd.DataFrame(st.session_state.db_tv, columns=["Producto"]), num_rows="dynamic", key="ed_tv")
        st.session_state.db_tv = df_tv["Producto"].tolist()
        st.write("**Adicionales**")
        df_add = st.data_editor(pd.DataFrame(st.session_state.db_adicionales, columns=["Producto"]), num_rows="dynamic", key="ed_add")
        st.session_state.db_adicionales = df_add["Producto"].tolist()
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 3- ADMINISTRACIÓN TÉCNICA (Dropdowns en Tablas)
# ==============================================================================
elif opcion_menu == "Tablero Administración Técnica":
    st.title("Administración Técnica")
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Matriz de Reglas Lógicas (Motor 3 Capas)")
    
    # Configuración de columnas con opciones desplegables
    conf_reglas = {
        "Internet": st.column_config.SelectboxColumn("Internet", options=st.session_state.db_internet + ["Cualquiera"]),
        "TV": st.column_config.SelectboxColumn("TV", options=st.session_state.db_tv + ["Cualquiera"]),
        "Adicional": st.column_config.SelectboxColumn("Adicional", options=st.session_state.db_adicionales + ["Cualquiera", "Ninguno"]),
        "Acción": st.column_config.SelectboxColumn("Acción", options=["ASIGNAR", "UPGRADE", "SUMAR", "REEMPLAZAR KIT"]),
        "Ítem": st.column_config.SelectboxColumn("Equipo/Pack a afectar", options=[x["Equipo"] for x in st.session_state.db_equipos] + ["Pack Coaxil", "DONGLE + MINI UPS", "ONT GPON ZXHN F601 + 2 Tenda MX3"])
    }
    
    df_reg = st.data_editor(pd.DataFrame(st.session_state.reglas_3capas), num_rows="dynamic", column_config=conf_reglas, use_container_width=True, key="ed_reglas_tec")
    st.session_state.reglas_3capas = df_reg.to_dict('records')
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 4- ADMINISTRACIÓN DE COSTOS (Sincronización Corregida)
# ==============================================================================
elif opcion_menu == "Tablero Administración de Costos":
    st.title("Administración de Costos")
    conf_c = {"Costo Unitario USD": st.column_config.NumberColumn(format="USD %.3f"), "Costo USD": st.column_config.NumberColumn(format="USD %.2f"), "Costo Mensual USD": st.column_config.NumberColumn(format="USD %.2f")}
    
    # Maestro de Equipos
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Maestro de Equipos")
    df_eq_ed = st.data_editor(pd.DataFrame(st.session_state.db_equipos), num_rows="dynamic", column_config=conf_c, use_container_width=True, key="ed_eq_cost")
    st.session_state.db_equipos = df_eq_ed.to_dict('records')
    st.markdown('</div>', unsafe_allow_html=True)

    # Packs
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("pack materiales FTTH")
    df_f_ed = st.data_editor(pd.DataFrame(st.session_state.mat_ftth), num_rows="dynamic", column_config=conf_c, use_container_width=True, key="ed_ftth_cost")
    st.session_state.mat_ftth = df_f_ed.to_dict('records')
    st.markdown(f"**Importe total del pack:** `USD {sum(x['Cantidad']*x['Costo Unitario USD'] for x in st.session_state.mat_ftth):,.2f}`")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("pack de materiales coaxil")
    df_c_ed = st.data_editor(pd.DataFrame(st.session_state.mat_coaxil), num_rows="dynamic", column_config=conf_c, use_container_width=True, key="ed_coax_cost")
    st.session_state.mat_coaxil = df_c_ed.to_dict('records')
    st.markdown(f"**Importe total del pack:** `USD {sum(x['Cantidad']*x['Costo Unitario USD'] for x in st.session_state.mat_coaxil):,.2f}`")
    st.markdown('</div>', unsafe_allow_html=True)

    # NUEVA SECCIÓN: COSTOS DIRECTOS
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Costos Directos (Mensuales)")
    st.write("Gastos fijos operativos que se restan del abono neto antes de amortizar la inversión.")
    df_cd_ed = st.data_editor(pd.DataFrame(st.session_state.db_costos_directos), num_rows="dynamic", column_config=conf_c, use_container_width=True, key="ed_cd_cost")
    st.session_state.db_costos_directos = df_cd_ed.to_dict('records')
    st.markdown('</div>', unsafe_allow_html=True)