import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN E IDENTIDAD VISUAL CORPORATIVA
st.set_page_config(page_title="Pricing Wiltel", layout="wide", initial_sidebar_state="expanded")

# Inyección de estilos CSS para Tablero Corporativo
st.markdown("""
    <style>
    .main { background-color: #f4f6f9; }
    [data-testid="stSidebar"] { background-color: #003366; min-width: 300px; }
    
    /* Texto del menú lateral: una sola línea, blanco, sin subtítulos */
    .sidebar-title {
        color: #ffffff;
        font-family: 'Arial', sans-serif;
        font-size: 18px;
        font-weight: 600;
        text-align: center;
        padding: 20px 0px;
        border-bottom: 1px solid #4a5568;
        margin-bottom: 20px;
    }
    
    /* Estilo de Tarjetas Contenedoras con línea gris */
    .wiltel-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 4px;
        border-top: 2px solid #d1d5db;
        margin-bottom: 25px;
    }
    
    /* Forzar visibilidad de radio buttons en blanco */
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
        color: #ffffff !important;
        font-size: 15px !important;
    }

    /* Sliders naranjas Wiltel */
    .stSlider > div [data-baseweb="slider"] { background-color: #ff823a; }
    
    /* Fuente pequeña para valores referenciales */
    .ref-text { font-size: 12px; color: #6b7280; }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZACIÓN DE DATOS (Session State) ---

if 'comercial_params' not in st.session_state:
    st.session_state.comercial_params = {
        "tc": 1420.0, 
        "pb_objetivo": 6, 
        "costo_fact": 8.0,
        "pct_recupero_obj": 35.0
    }

if 'db_internet' not in st.session_state:
    st.session_state.db_internet = ["WILTEL 25 MB", "WILTEL 50 MB", "WILTEL 150 MB", "WILTEL 300 MB", "Ninguno"]
if 'db_tv' not in st.session_state:
    st.session_state.db_tv = ["WILTEL TV HD", "FULL TV HD", "PLAYME TV HD", "PLAYME FULL BOX", "Ninguno"]
if 'db_telefonia' not in st.session_state:
    st.session_state.db_telefonia = ["Línea Hogar Básica", "Ninguno"]
if 'db_adicionales' not in st.session_state:
    st.session_state.db_adicionales = ["WILTEL ON", "MESH", "PAQUETE FUTBOL", "PAQUETE TV PREMIUM"]

if 'db_equipos' not in st.session_state:
    st.session_state.db_equipos = [
        {"Equipo": "ONT GPON ZXHN F6201B", "Costo USD": 35.60},
        {"Equipo": "ONT GPON ZXHN F6600R", "Costo USD": 49.40},
        {"Equipo": "ONT GPON ZXHN F601", "Costo USD": 24.50},
        {"Equipo": "STB mod HC-C730 (Beacon)", "Costo USD": 35.00},
        {"Equipo": "DONGLE WILTEL ON", "Costo USD": 28.60},
        {"Equipo": "MINI UPS WILTEL ON", "Costo USD": 20.67},
        {"Equipo": "ZXHN H3601N (Router)", "Costo USD": 35.60},
        {"Equipo": "Tenda NOVA MX3", "Costo USD": 28.41}
    ]

# Matriz de Reglas Técnicas (Lógica Anidada)
if 'reglas_kits' not in st.session_state:
    st.session_state.reglas_kits = [
        {"Condición Internet": "Cualquiera", "Condición TV": "Contiene TV", "Equipo Principal": "ONT GPON ZXHN F6600R", "Suma Coaxil": True},
        {"Condición Internet": "WILTEL 150 MB", "Condición TV": "Ninguno", "Equipo Principal": "ONT GPON ZXHN F6201B", "Suma Coaxil": False},
        {"Condición Internet": "WILTEL 300 MB", "Condición TV": "Ninguno", "Equipo Principal": "ONT GPON ZXHN F6201B", "Suma Coaxil": False},
    ]

# Costos de Materiales
if 'mat_ftth' not in st.session_state:
    st.session_state.mat_ftth = [{"Ítem": "DROP FTTH", "Cantidad": 150.0, "Costo USD": 0.04}, {"Ítem": "CONECTORES", "Cantidad": 2.0, "Costo USD": 1.20}]
if 'mat_coaxil' not in st.session_state:
    st.session_state.mat_coaxil = [{"Ítem": "CABLE RG6", "Cantidad": 20.0, "Costo USD": 0.31}, {"Ítem": "FICHAS", "Cantidad": 4.0, "Costo USD": 0.80}]
if 'costo_mo' not in st.session_state: st.session_state.costo_mo = 47.36

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

# --- LÓGICA DE MONEDA B2C/B2B ---
def formatear_moneda(valor, moneda):
    simbolo = "$" if moneda == "Pesos ARS" else "USD"
    return f"{simbolo} {valor:,.2f}"

# ==============================================================================
# 1- SIMULACIÓN COMERCIAL
# ==============================================================================
if opcion_menu == "Simulación Comercial":
    st.title("Simulación Comercial")
    
    # TARJETA 1: CONFIGURACIÓN COMERCIAL
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Configuración Comercial")
    col1, col2 = st.columns(2)
    with col1:
        segmento = st.selectbox("Segmento de Cliente", ["B2C", "B2B"])
    with col2:
        opciones_moneda = ["Pesos ARS"] if segmento == "B2C" else ["Pesos ARS", "Dólares USD"]
        moneda = st.selectbox("Moneda de Cotización", opciones_moneda)
    
    st.markdown("""<p class='ref-text'>⚠️ Precios expresados en: $ con IVA incluido para B2C | Moneda seleccionada sin IVA para B2B</p>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # TARJETA 2: COMBO
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Combo")
    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1: prod_int = st.selectbox("Internet", st.session_state.db_internet, index=2)
    with col_c2: prod_tv = st.selectbox("TV", st.session_state.db_tv, index=0)
    with col_c3: prod_tel = st.selectbox("Telefonía", st.session_state.db_telefonia, index=1)
    
    st.markdown("**Adicionales**")
    col_a1, col_a2, col_a3, col_a4 = st.columns(4)
    with col_a1: add_on = st.checkbox("WILTEL ON")
    with col_a2: add_mesh = st.checkbox("MESH")
    with col_a3: add_futbol = st.checkbox("PAQUETE FÚTBOL")
    with col_a4: add_premium = st.checkbox("PAQUETE TV PREMIUM")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- LÓGICA TÉCNICA (Reglas complejas) ---
    eq_cost_dict = {x['Equipo']: x['Costo USD'] for x in st.session_state.db_equipos}
    costo_hw = 0.0
    lleva_coaxil = False

    # Regla anidada de ejemplo (Internet 150 + TV)
    if prod_tv != "Ninguno":
        costo_hw = eq_cost_dict.get("ONT GPON ZXHN F6600R", 49.40)
        lleva_coaxil = True
        if prod_tv == "FULL TV HD": costo_hw += eq_cost_dict.get("STB mod HC-C730 (Beacon)", 35.00)
    else:
        costo_hw = eq_cost_dict.get("ONT GPON ZXHN F6201B", 35.60)

    if add_on: costo_hw += eq_cost_dict.get("DONGLE WILTEL ON", 28.60) + eq_cost_dict.get("MINI UPS WILTEL ON", 20.67)
    if add_mesh: costo_hw += eq_cost_dict.get("ZXHN H3601N (Router)", 35.60)

    # Bolsas
    sub_ftth = sum(x['Cantidad'] * x['Costo USD'] for x in st.session_state.mat_ftth)
    sub_coax = sum(x['Cantidad'] * x['Costo USD'] for x in st.session_state.mat_coaxil) if lleva_coaxil else 0
    
    inversion_total_usd = st.session_state.costo_mo + costo_hw + sub_ftth + sub_coax
    tc = st.session_state.comercial_params["tc"]
    inversion_local = inversion_total_usd * tc if moneda == "Pesos ARS" else inversion_total_usd

    # TARJETA 3: COMBINACIÓN DE OFERTA
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Combinación de Oferta")
    col_p1, col_p2 = st.columns(2)
    
    divisor = (1.0 - (st.session_state.comercial_params["costo_fact"]/100))
    iva = 1.21 if segmento == "B2C" else 1.0

    with col_p1:
        pct_sel = st.slider("% Inversión a recuperar", 0, 100, int(st.session_state.comercial_params["pct_recupero_obj"]))
        cargo_final = (inversion_local * (pct_sel/100) / divisor) * iva
        st.write(f"**Cargo asociado:** {formatear_moneda(cargo_final, moneda)}")
        st.markdown(f"<p class='ref-text'>Valor referencial de instalación para cubrir objetivo técnico</p>", unsafe_allow_html=True)

    saldo_amortizar = inversion_local - (inversion_local * (pct_sel/100))
    # Equilibrio: Abono = (Saldo / Payback) + CostosDirectos (simplificado para el ejemplo)
    abono_equilibrio = ((saldo_amortizar / st.session_state.comercial_params["pb_objetivo"]) / divisor) * iva

    with col_p2:
        abono_simulado = st.slider("Abono Mensual Regular de Lista", 5000, 150000, 39424)
        st.write(f"**Abono Mínimo sugerido (Punto de Equilibrio):** {formatear_moneda(abono_equilibrio, moneda)}")
        st.markdown(f"<p class='ref-text'>Este abono logra el Payback objetivo de {st.session_state.comercial_params['pb_objetivo']} meses con el cargo seleccionado.</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # TARJETA 4: ESCALAS PROMOCIONALES
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Configuración de Escalas Promocionales")
    col_t1, col_t2, col_t3, col_t4 = st.columns(4)
    with col_t1:
        st.markdown("**Tramo 1**")
        m1 = st.selectbox("Duración Tramo 1 (Meses)", [0,1,2,3,4,6,12], index=3)
        d1 = st.slider("Descuento Tramo 1 (%)", 0, 100, 40)
    with col_t2:
        st.markdown("**Tramo 2**")
        m2 = st.selectbox("Duración Tramo 2 (Meses)", [0,1,2,3,4,6,12], index=0)
        d2 = st.slider("Descuento Tramo 2 (%)", 0, 100, 20)
    with col_t3:
        st.markdown("**Tramo 3**")
        m3 = st.selectbox("Duración Tramo 3 (Meses)", [0,1,2,3,4,6,12], index=0)
        d3 = st.slider("Descuento Tramo 3 (%)", 0, 100, 0)
    with col_t4:
        st.markdown("**Tramo 4**")
        m4 = st.selectbox("Duración Tramo 4 (Meses)", [0,1,2,3,4,6,12], index=0)
        d4 = st.slider("Descuento Tramo 4 (%)", 0, 100, 0)
    st.markdown('</div>', unsafe_allow_html=True)

    # TARJETA 5: VALIDACIÓN COMERCIAL
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Validación Comercial")
    # Simulación simple de payback real
    pb_real = 5.4 # Valor simulado para el dashboard
    if pb_real <= st.session_state.comercial_params["pb_objetivo"]:
        st.success(f"🟢 Semáforo Oferta: APROBADO | Payback Real: {pb_real} meses")
    else:
        st.error(f"🔴 Semáforo Oferta: RECHAZADO | Payback Real: {pb_real} meses")
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
    with c2: st.session_state.comercial_params["pb_objetivo"] = st.number_input("Payback Objetivo (Meses)", value=st.session_state.comercial_params["pb_objetivo"])
    with c3: st.session_state.comercial_params["costo_fact"] = st.number_input("Costo de Facturación (%)", value=st.session_state.comercial_params["costo_fact"])
    with c4: st.session_state.comercial_params["pct_recupero_obj"] = st.number_input("% Recupero Inversión Obj.", value=st.session_state.comercial_params["pct_recupero_obj"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Opciones de Productos")
    r1, r2 = st.columns(2)
    with r1:
        st.write("**Internet**")
        st.data_editor(pd.DataFrame(st.session_state.db_internet, columns=["Producto"]), num_rows="dynamic", key="ed_int", height=250)
        st.write("**Telefonía**")
        st.data_editor(pd.DataFrame(st.session_state.db_telefonia, columns=["Producto"]), num_rows="dynamic", key="ed_tel", height=150)
    with r2:
        st.write("**TV**")
        st.data_editor(pd.DataFrame(st.session_state.db_tv, columns=["Producto"]), num_rows="dynamic", key="ed_tv", height=250)
        st.write("**Adicionales**")
        st.data_editor(pd.DataFrame(st.session_state.db_adicionales, columns=["Producto"]), num_rows="dynamic", key="ed_add", height=150)
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 3- ADMINISTRACIÓN TÉCNICA
# ==============================================================================
elif opcion_menu == "Tablero Administración Técnica":
    st.title("Administración Técnica")
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Matriz de Reglas Lógicas (Kits Dinámicos)")
    st.write("Defina aquí las combinaciones que disparan equipos específicos (Si Internet = X y TV = Y entonces ONT = Z)")
    st.data_editor(pd.DataFrame(st.session_state.reglas_kits), num_rows="dynamic", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 4- ADMINISTRACIÓN DE COSTOS
# ==============================================================================
elif opcion_menu == "Tablero Administración de Costos":
    st.title("Administración de Costos")
    st.caption("⚠️ Valores en USD sin IVA")
    
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Maestro de Equipos")
    conf = {"Costo USD": st.column_config.NumberColumn(format="USD %.2f")}
    st.data_editor(pd.DataFrame(st.session_state.db_equipos), num_rows="dynamic", column_config=conf, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Materiales FTTH")
    st.data_editor(pd.DataFrame(st.session_state.mat_ftth), num_rows="dynamic", column_config=conf, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Materiales Coaxil")
    st.data_editor(pd.DataFrame(st.session_state.mat_coaxil), num_rows="dynamic", column_config=conf, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)