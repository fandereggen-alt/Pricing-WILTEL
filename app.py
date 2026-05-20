import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN E IDENTIDAD VISUAL CORPORATIVA WILTEL
st.set_page_config(page_title="Pricing Wiltel", layout="wide", initial_sidebar_state="expanded")

# Inyección de estilos CSS para Tablero de Control Corporativo (Minimalista)
st.markdown("""
    <style>
    .main { background-color: #f4f6f9; }
    [data-testid="stSidebar"] { background-color: #003366; min-width: 300px; }
    
    /* Menú lateral: Una sola línea blanca */
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
    
    /* Tarjetas con línea gris superior */
    .wiltel-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 4px;
        border-top: 3px solid #d1d5db;
        margin-bottom: 25px;
    }
    
    /* Estilo blanco para Sidebar */
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #ffffff !important;
        font-size: 14px !important;
    }

    /* Sliders Wiltel Naranja */
    .stSlider > div [data-baseweb="slider"] { background-color: #ff823a; }
    
    /* Textos referenciales pequeños */
    .ref-text { font-size: 12px; color: #6b7280; font-style: italic; }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZACIÓN DE LA BASE DE DATOS EN MEMORIA ---

if 'comercial_params' not in st.session_state:
    st.session_state.comercial_params = {
        "tc": 1420.0, "pb_objetivo": 6, "costo_fact": 8.0, "pct_recupero_obj": 35.0
    }

# Carteras de Productos
if 'db_internet' not in st.session_state: st.session_state.db_internet = ["WILTEL 25 MB", "WILTEL 50 MB", "WILTEL 150 MB", "WILTEL 300 MB", "Ninguno"]
if 'db_tv' not in st.session_state: st.session_state.db_tv = ["Ninguno", "WILTEL TV HD", "FULL TV HD", "PLAYME TV HD", "PLAYME FULL BOX"]
if 'db_telefonia' not in st.session_state: st.session_state.db_telefonia = ["Ninguno", "Línea Hogar Básica"]
if 'db_adicionales' not in st.session_state: st.session_state.db_adicionales = ["WILTEL ON", "MESH", "PAQUETE FUTBOL", "PAQUETE TV PREMIUM"]

# Maestro de Equipos e Insumos
if 'costo_mo' not in st.session_state: st.session_state.costo_mo = 47.36
if 'iva_mo' not in st.session_state: st.session_state.iva_mo = 21.0

if 'mat_ftth' not in st.session_state:
    st.session_state.mat_ftth = [
        {"Ítem": "DROP FTTH", "Cantidad": 150.0, "Costo Unitario USD": 0.044, "IVA %": 21.0},
        {"Ítem": "CONECTORES", "Cantidad": 2.0, "Costo Unitario USD": 1.20, "IVA %": 21.0}
    ]

if 'mat_coaxil' not in st.session_state:
    st.session_state.mat_coaxil = [
        {"Ítem": "CABLE RG-6", "Cantidad": 20.0, "Costo Unitario USD": 0.31, "IVA %": 21.0},
        {"Ítem": "FICHAS", "Cantidad": 4.0, "Costo Unitario USD": 0.80, "IVA %": 21.0}
    ]

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

# MATRIZ DE REGLAS LÓGICAS (3 CAPAS)
if 'reglas_3capas' not in st.session_state:
    st.session_state.reglas_3capas = [
        {"Capa": "1-Base", "Internet": "Cualquiera", "TV": "Ninguno", "Adicional": "Ninguno", "Acción": "ASIGNAR", "Ítem": "ONT GPON ZXHN F6201B"},
        {"Capa": "2-TV", "Internet": "Cualquiera", "TV": "WILTEL TV HD", "Adicional": "Cualquiera", "Acción": "UPGRADE", "Ítem": "ONT GPON ZXHN F6600R"},
        {"Capa": "2-TV", "Internet": "Cualquiera", "TV": "FULL TV HD", "Adicional": "Cualquiera", "Acción": "SUMAR", "Ítem": "STB mod HC-C730 (Beacon)"},
        {"Capa": "3-Modif", "Internet": "WILTEL 150 MB", "TV": "Ninguno", "Adicional": "MESH", "Acción": "REEMPLAZAR KIT", "Ítem": "ONT GPON ZXHN F601 + 2 Tenda MX3"},
        {"Capa": "3-Modif", "Internet": "Cualquiera", "TV": "Cualquiera", "Adicional": "WILTEL ON", "Acción": "SUMAR", "Ítem": "DONGLE + MINI UPS"}
    ]

if 'db_costos_directos' not in st.session_state:
    st.session_state.db_costos_directos = [
        {"Concepto": "Chip datos WILTEL ON 1GB", "Costo USD": 5.00, "Margen %": 20.0},
        {"Concepto": "Paquete TV FÚTBOL", "Costo USD": 8.00, "Margen %": 15.0}
    ]

# --- MENÚ LATERAL ---
with st.sidebar:
    st.markdown('<div class="sidebar-title">Wiltel Comunicaciones S.A.</div>', unsafe_allow_html=True)
    opcion_menu = st.radio(
        "",
        [
            "Simulación Comercial",
            "Tablero Administración Comercial",
            "Tablero Administración Técnica",
            "Tablero Administración de Costos"
        ]
    )

def fmt_ars(v): return f"$ {v:,.2f}"
def fmt_usd(v): return f"USD {v:,.2f}"

# ==============================================================================
# 1- SIMULACIÓN COMERCIAL
# ==============================================================================
if opcion_menu == "Simulación Comercial":
    st.title("Simulación Comercial")
    
    # Tarjeta 1: Configuración Comercial
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Configuración Comercial")
    col1, col2 = st.columns(2)
    with col1: segmento = st.selectbox("Segmento de Cliente", ["B2C", "B2B"])
    with col2:
        moneda_opts = ["Pesos ARS"] if segmento == "B2C" else ["Pesos ARS", "Dólares USD"]
        moneda = st.selectbox("Moneda de Cotización", moneda_opts)
    st.markdown("""<p class='ref-text'>⚠️ Precios expresados en: $ con IVA incluido para B2C | Moneda seleccionada sin IVA para B2B</p>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Tarjeta 2: Combo
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Combo")
    c1, c2, c3 = st.columns(3)
    with c1: prod_int = st.selectbox("Internet", st.session_state.db_internet, index=2)
    with c2: prod_tv = st.selectbox("TV", st.session_state.db_tv, index=1)
    with c3: prod_tel = st.selectbox("Telefonía", st.session_state.db_telefonia, index=0)
    
    st.markdown("**Adicionales Disponibles**")
    a1, a2, a3, a4 = st.columns(4)
    with a1: add_on = st.checkbox("WILTEL ON")
    with a2: add_mesh = st.checkbox("MESH")
    with a3: add_futbol = st.checkbox("PAQUETE FÚTBOL")
    with a4: add_premium = st.checkbox("PAQUETE TV PREMIUM")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- MOTOR DE REGLAS 3 CAPAS (Lógica de Hardware) ---
    tc = st.session_state.comercial_params["tc"]
    costo_fact_local = st.session_state.comercial_params["costo_fact"] / 100.0
    pb_obj_local = st.session_state.comercial_params["pb_objetivo"]
    
    eq_cost = {x['Equipo']: x['Costo USD'] for x in st.session_state.db_equipos}
    eq_iva = {x['Equipo']: x['IVA %']/100 for x in st.session_state.db_equipos}
    
    costo_hw_usd = 0.0
    iva_hw_usd = 0.0
    lleva_coaxil = False

    # Capa 1: Base (Internet)
    if prod_int != "Ninguno":
        base_ont = "ONT GPON ZXHN F6201B"
        costo_hw_usd = eq_cost.get(base_ont, 0.0)
        iva_hw_usd = costo_hw_usd * eq_iva.get(base_ont, 0.21)

    # Capa 2: TV
    if prod_tv != "Ninguno":
        # Upgrade por TV
        costo_hw_usd = eq_cost.get("ONT GPON ZXHN F6600R", 49.40)
        iva_hw_usd = costo_hw_usd * eq_iva.get("ONT GPON ZXHN F6600R", 0.21)
        lleva_coaxil = True
        if prod_tv == "FULL TV HD":
            costo_hw_usd += eq_cost.get("STB mod HC-C730 (Beacon)", 35.00)
            iva_hw_usd += 35.00 * 0.21

    # Capa 3: Modificadores y Excepciones
    if add_mesh:
        if prod_int == "WILTEL 150 MB" and prod_tv == "Ninguno":
            # REEMPLAZAR KIT
            costo_hw_usd = eq_cost.get("ONT GPON ZXHN F601", 24.50) + (eq_cost.get("Tenda NOVA MX3", 28.41) * 2)
            iva_hw_usd = (24.50 * 0.21) + (28.41 * 2 * 0.21)
        else:
            costo_hw_usd += eq_cost.get("ZXHN H3601N (Router)", 35.60)
            iva_hw_usd += 35.60 * 0.21

    if add_on:
        costo_hw_usd += eq_cost.get("DONGLE WILTEL ON", 28.60) + eq_cost.get("MINI UPS WILTEL ON", 20.67)
        iva_hw_usd += (28.60 + 20.67) * 0.21

    # Packs de Materiales
    neto_ftth = sum(x['Cantidad'] * x['Costo Unitario USD'] for x in st.session_state.mat_ftth)
    iva_ftth = sum(x['Cantidad'] * x['Costo Unitario USD'] * (x['IVA %']/100) for x in st.session_state.mat_ftth)
    neto_coax = sum(x['Cantidad'] * x['Costo Unitario USD'] for x in st.session_state.mat_coaxil) if lleva_coaxil else 0
    iva_coax = sum(x['Cantidad'] * x['Costo Unitario USD'] * (x['IVA %']/100) for x in st.session_state.mat_coaxil) if lleva_coaxil else 0

    total_neto_usd = st.session_state.costo_mo + costo_hw_usd + neto_ftth + neto_coax
    iva_promedio = (iva_hw_usd + iva_ftth + iva_coax + (st.session_state.costo_mo * 0.21)) / total_neto_usd
    
    inversion_local = total_neto_usd * tc if moneda == "Pesos ARS" else total_neto_usd

    # Tarjeta 3: Combinación de Oferta
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Combinación de Oferta")
    p1, p2 = st.columns(2)
    
    divisor = (1.0 - costo_fact_local)
    iva_aplicable = (1.0 + iva_promedio) if segmento == "B2C" else 1.0

    with p1:
        pct_rec = st.slider("% Inversión a recuperar", 0, 100, int(st.session_state.comercial_params["pct_recupero_obj"]))
        cargo_publico = (inversion_local * (pct_rec/100) / divisor) * iva_aplicable
        st.write(f"### **Cargo asociado:** {fmt_ars(cargo_publico) if moneda=='Pesos ARS' else fmt_usd(cargo_publico)}")
        st.markdown(f"<p class='ref-text'>Calculado sobre inversión de {fmt_usd(total_neto_usd)}</p>", unsafe_allow_html=True)

    saldo_amortizar = inversion_local - (inversion_local * (pct_rec/100))
    # Equilibrio: (Saldo / Payback) + Costos directos (Simulado 5 USD costo directo)
    equilibrio = ((saldo_amortizar / pb_obj_local) / divisor) * iva_aplicable

    with p2:
        abono_lista = st.slider("Abono Mensual Regular de Lista", 5000, 150000, 39424 if moneda=="Pesos ARS" else 40)
        st.write(f"### **Abono sugerido (Equilibrio):** {fmt_ars(equilibrio) if moneda=='Pesos ARS' else fmt_usd(equilibrio)}")
        st.markdown(f"<p class='ref-text'>Abono necesario para saldar el kit en {pb_obj_local} meses.</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Tarjeta 4: Escalas Promocionales
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

    # --- SIMULACIÓN REAL DE PAYBACK ---
    saldo = saldo_amortizar
    pb_real = 0.0
    for mes in range(1, 49):
        if saldo <= 0: break
        # Precio del mes
        if mes <= m1: cur_dto = d1
        elif mes <= (m1+m2): cur_dto = d2
        elif mes <= (m1+m2+m3): cur_dto = d3
        elif mes <= (m1+m2+m3+m4): cur_dto = d4
        else: cur_dto = 0
        
        precio_n = (abono_lista * (1-(cur_dto/100)) / iva_aplicable) * divisor
        # Descontamos 5 USD de tránsito IP promedio
        recaudo = precio_n - (5 * tc if moneda=="Pesos ARS" else 5)
        if recaudo > 0:
            if saldo > recaudo:
                saldo -= recaudo
                pb_real += 1
            else:
                pb_real += (saldo / recaudo)
                saldo = 0
        else:
            pb_real = 99
            break

    # Tarjeta 5: Validación
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Validación Comercial")
    if pb_real <= pb_obj_local:
        st.success(f"🟢 Semáforo Oferta: APROBADO | Payback Real: {pb_real:.1f} meses")
    else:
        st.error(f"🔴 Semáforo Oferta: RECHAZADO | Payback Real: {pb_real:.1f} meses")
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 2- ADMINISTRACIÓN COMERCIAL
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
        res_i = st.data_editor(pd.DataFrame(st.session_state.db_internet, columns=["Producto"]), num_rows="dynamic", key="ed_i", height=200)
        st.session_state.db_internet = res_i["Producto"].tolist()
        st.write("**Telefonía**")
        res_tel = st.data_editor(pd.DataFrame(st.session_state.db_telefonia, columns=["Producto"]), num_rows="dynamic", key="ed_tel", height=150)
        st.session_state.db_telefonia = res_tel["Producto"].tolist()
    with r2:
        st.write("**TV**")
        res_tv = st.data_editor(pd.DataFrame(st.session_state.db_tv, columns=["Producto"]), num_rows="dynamic", key="ed_tv", height=200)
        st.session_state.db_tv = res_tv["Producto"].tolist()
        st.write("**Adicionales**")
        res_ad = st.data_editor(pd.DataFrame(st.session_state.db_adicionales, columns=["Producto"]), num_rows="dynamic", key="ed_ad", height=150)
        st.session_state.db_adicionales = res_ad["Producto"].tolist()
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 3- ADMINISTRACIÓN TÉCNICA
# ==============================================================================
elif opcion_menu == "Tablero Administración Técnica":
    st.title("Administración Técnica")
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Matriz de Reglas Lógicas (Motor 3 Capas)")
    st.write("Defina la lógica de asignación, upgrade o reemplazo de equipos según la combinación de productos.")
    res_reglas = st.data_editor(pd.DataFrame(st.session_state.reglas_3capas), num_rows="dynamic", use_container_width=True)
    st.session_state.reglas_3capas = res_reglas.to_dict('records')
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 4- ADMINISTRACIÓN DE COSTOS
# ==============================================================================
elif opcion_menu == "Tablero Administración de Costos":
    st.title("Administración de Costos")
    st.caption("⚠️ Valores en USD sin IVA")
    conf = {"Costo Unitario USD": st.column_config.NumberColumn(format="USD %.2f"), "Costo USD": st.column_config.NumberColumn(format="USD %.2f")}
    
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Maestro de Equipos")
    res_eq = st.data_editor(pd.DataFrame(st.session_state.db_equipos), num_rows="dynamic", column_config=conf, use_container_width=True)
    st.session_state.db_equipos = res_eq.to_dict('records')
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("pack materiales FTTH")
    res_f = st.data_editor(pd.DataFrame(st.session_state.mat_ftth), num_rows="dynamic", column_config=conf, use_container_width=True)
    st.session_state.mat_ftth = res_f.to_dict('records')
    st.markdown(f"**Importe total del pack:** `USD {sum(x['Cantidad']*x['Costo Unitario USD'] for x in st.session_state.mat_ftth):,.2f}`")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("pack de materiales coaxil")
    res_c = st.data_editor(pd.DataFrame(st.session_state.mat_coaxil), num_rows="dynamic", column_config=conf, use_container_width=True)
    st.session_state.mat_coaxil = res_c.to_dict('records')
    st.markdown(f"**Importe total del pack:** `USD {sum(x['Cantidad']*x['Costo Unitario USD'] for x in st.session_state.mat_coaxil):,.2f}`")
    st.markdown('</div>', unsafe_allow_html=True)