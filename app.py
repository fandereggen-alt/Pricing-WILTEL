import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE PÁGINA E IDENTIDAD CORPORATIVA WILTEL
st.set_page_config(page_title="Pricing Wiltel", layout="wide", initial_sidebar_state="expanded")

# Inyección de estilos CSS para lograr el formato de Tablero Corporativo (Letras blancas en Sidebar y Tarjetas)
st.markdown("""
    <style>
    .main { background-color: #f4f6f9; }
    [data-testid="stSidebar"] { background-color: #003366; }
    
    /* Forzar texto blanco puro y legible en el menú lateral */
    [data-testid="stSidebar"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label { 
        color: #ffffff !important; 
        font-weight: 500;
    }
    h1, h2, h3, h4 { color: #003366; font-family: 'Arial', sans-serif; }
    
    /* Contenedores tipo Tarjetas por sección (Sin divisores rígidos de línea) */
    .wiltel-card {
        background-color: #ffffff;
        padding: 22px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.04);
        margin-bottom: 25px;
        border-left: 5px solid #003366;
    }
    /* Formato corporativo unificado para Sliders */
    .stSlider > div [data-baseweb="slider"] { background-color: #ff823a; }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZACIÓN DE LA BASE DE DATOS EN MEMORIA (Session State) ---

# Parámetros Estratégicos Comerciales Iniciales
if 'comercial_params' not in st.session_state:
    st.session_state.comercial_params = {"tc": 1420.0, "pb_objetivo": 6, "costo_fact": 8.0}

# Cartera de Productos (Listas dinámicas en filas, modificables en Pestaña 2)
if 'db_internet' not in st.session_state: st.session_state.db_internet = ["Ninguno", "WILTEL 25 MB", "WILTEL 50 MB", "WILTEL 150 MB", "WILTEL 300 MB"]
if 'db_tv' not in st.session_state: st.session_state.db_tv = ["Ninguno", "WILTEL TV HD", "FULL TV HD", "PLAYME TV HD", "PLAYME FULL BOX"]
if 'db_telefonia' not in st.session_state: st.session_state.db_telefonia = ["Ninguno", "Línea Hogar Básica"]
if 'db_adicionales' not in st.session_state: st.session_state.db_adicionales = ["WILTEL ON", "MESH", "PAQUETE FUTBOL", "PAQUETE TV PREMIUM", "ALMACENAMIENTO CLOUD"]

# Maestro de Insumos y Costos (USD sin IVA) - Pestaña 4
if 'costo_mo' not in st.session_state: st.session_state.costo_mo = 47.36

if 'mat_ftth' not in st.session_state:
    st.session_state.mat_ftth = [
        {"Ítem": "DROP FTTH-SM 01 HILO", "Cantidad": 150.0, "Costo Unitario USD": 0.044, "IVA %": 21.0},
        {"Ítem": "CONECTOR RAPIDO SC/APC", "Cantidad": 2.0, "Costo Unitario USD": 1.20, "IVA %": 21.0},
        {"Ítem": "HEBILLA DE ACERO", "Cantidad": 4.0, "Costo Unitario USD": 0.15, "IVA %": 21.0},
        {"Ítem": "FLEJE DE ACERO", "Cantidad": 5.0, "Costo Unitario USD": 0.30, "IVA %": 21.0},
        {"Ítem": "SOPORTE B", "Cantidad": 2.0, "Costo Unitario USD": 1.80, "IVA %": 21.0},
        {"Ítem": "PATCHCORD SC/APC-SC/APC", "Cantidad": 1.0, "Costo Unitario USD": 2.50, "IVA %": 21.0}
    ]

if 'mat_coaxil' not in st.session_state:
    st.session_state.mat_coaxil = [
        {"Ítem": "CABLE RG-6 TRISHIELD s/p", "Cantidad": 20.0, "Costo Unitario USD": 0.31, "IVA %": 21.0},
        {"Ítem": "FICHA COMPRESION RG-6 PPC", "Cantidad": 4.0, "Costo Unitario USD": 0.80, "IVA %": 21.0},
        {"Ítem": "DIVISOR PPC 2 VIAS 1Ghz", "Cantidad": 1.0, "Costo Unitario USD": 3.20, "IVA %": 21.0},
        {"Ítem": "DIVISOR PPC 3 VIAS 1Ghz", "Cantidad": 0.0, "Costo Unitario USD": 4.50, "IVA %": 21.0},
        {"Ítem": "ATENUADOR F (FAM) de 8Db", "Cantidad": 1.0, "Costo Unitario USD": 2.60, "IVA %": 21.0}
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

if 'db_costos_directos' not in st.session_state:
    st.session_state.db_costos_directos = [
        {"Concepto": "Chip de datos WILTEL ON 1GB", "Costo USD": 5.00, "IVA %": 21.0, "Margen Deseado %": 20.0},
        {"Concepto": "Chip WILTEL ON 5GB", "Costo USD": 9.50, "IVA %": 21.0, "Margen Deseado %": 25.0},
        {"Concepto": "Paquete TV FÚTBOL", "Costo USD": 8.00, "IVA %": 21.0, "Margen Deseado %": 15.0},
        {"Concepto": "Paquete TV PREMIUM", "Costo USD": 6.50, "IVA %": 21.0, "Margen Deseado %": 15.0},
        {"Concepto": "Almacenamiento Cloud 50GB", "Costo USD": 2.00, "IVA %": 21.0, "Margen Deseado %": 30.0}
    ]

# Matriz Dinámica de Reglas Técnicas (Pestaña 3)
if 'reglas_tecnicas' not in st.session_state:
    st.session_state.reglas_tecnicas = [
        {"Disparador (Venta)": "FULL TV HD", "Tipo Imputación": "Equipo", "Elemento Asignado": "STB mod HC-C730 (Beacon)", "Requiere Bolsa Coaxil": True},
        {"Disparador (Venta)": "PLAYME FULL BOX", "Tipo Imputación": "Equipo", "Elemento Asignado": "STB mod HC-C730 (Beacon)", "Requiere Bolsa Coaxil": False},
        {"Disparador (Venta)": "WILTEL TV HD", "Tipo Imputación": "Bolsa Materiales", "Elemento Asignado": "Paquete Coaxil", "Requiere Bolsa Coaxil": True},
        {"Disparador (Venta)": "PLAYME TV HD", "Tipo Imputación": "Bolsa Materiales", "Elemento Asignado": "Paquete Coaxil", "Requiere Bolsa Coaxil": True},
        {"Disparador (Venta)": "WILTEL ON", "Tipo Imputación": "Costo Directo + HW", "Elemento Asignado": "Chip de datos WILTEL ON 1GB", "Requiere Bolsa Coaxil": False},
        {"Disparador (Venta)": "MESH", "Tipo Imputación": "Equipo", "Elemento Asignado": "ZXHN H3601N (Router)", "Requiere Bolsa Coaxil": False},
        {"Disparador (Venta)": "PAQUETE FÚTBOL", "Tipo Imputación": "Costo Directo", "Elemento Asignado": "Paquete TV FÚTBOL", "Requiere Bolsa Coaxil": False},
        {"Disparador (Venta)": "PAQUETE TV PREMIUM", "Tipo Imputación": "Costo Directo", "Elemento Asignado": "Paquete TV PREMIUM", "Requiere Bolsa Coaxil": False}
    ]

# --- MENÚ LATERAL DE NAVEGACIÓN CORPORATIVA ---
with st.sidebar:
    st.image("https://www.wiltel.com.ar/wp-content/uploads/2021/04/wiltel_blanco.png", width=190, errors="ignore")
    st.markdown("<p style='font-size:12px; margin-top:-15px; margin-bottom:20px; text-align:center;'>Wiltel Comunicaciones S.A.</p>", unsafe_allow_html=True)
    
    opcion_menu = st.radio(
        "Navegación del Sistema:",
        [
            "1- Tablero de Simulación Comercial",
            "2- Administración Comercial",
            "3- Administración Técnica",
            "4- Administración de Costos"
        ]
    )
    st.markdown("---")
    st.caption("CPQ Pricing Engine v2026")

# ==============================================================================
# 1- PESTAÑA: TABLERO DE SIMULACIÓN COMERCIAL
# ==============================================================================
if opcion_menu == "1- Tablero de Simulación Comercial":
    st.title("Pricing Wiltel")
    
    # Tarjeta: Configuración Comercial
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Configuración Comercial")
    col_cc1, col_cc2 = st.columns(2)
    with col_cc1:
        segmento = st.selectbox("Segmento de Cliente", ["B2C", "B2B"])
    with col_cc2:
        moneda = st.selectbox("Moneda de Cotización", ["Pesos ARS", "Dólares USD"])
    
    # Ubicación del aviso solicitada abajo de los selectores de segmento y moneda
    st.markdown("""
    <p style='font-size:13px; color:#64748b; margin-top:10px;'>
    ⚠️ <strong>Precios de instalación y abonos expresados en:</strong><br>
    • $ con IVA incluido para B2C<br>
    • Moneda seleccionada sin IVA para B2B
    </p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Tarjeta: Combo
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Combo")
    col_cmb1, col_cmb2, col_cmb3 = st.columns(3)
    with col_cmb1:
        prod_internet = st.selectbox("Internet", st.session_state.db_internet)
    with col_cmb2:
        prod_tv = st.selectbox("TV", st.session_state.db_tv)
    with col_cmb3:
        prod_tel = st.selectbox("Telefonía", st.session_state.db_telefonia)
    
    st.markdown("**Adicionales Disponibles (Selección Múltiple Simultánea)**")
    col_a1, col_a2, col_a3, col_a4 = st.columns(4)
    with col_a1: add_wiltel_on = st.checkbox("WILTEL ON")
    with col_a2: add_mesh = st.checkbox("MESH")
    with col_a3: add_futbol = st.checkbox("PAQUETE FÚTBOL")
    with col_a4: add_premium = st.checkbox("PAQUETE TV PREMIUM")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- RESOLUCIÓN MATEMÁTICA INTERNA DEL MOTOR POR REGLAS ---
    tc_local = st.session_state.comercial_params["tc"]
    costo_fact_local = st.session_state.comercial_params["costo_fact"] / 100.0
    pb_obj_local = st.session_state.comercial_params["pb_objetivo"]
    
    eq_cost_dict = {x['Equipo']: float(x['Costo USD']) for x in st.session_state.db_equipos}
    costo_hardware_usd = 0.0
    requiere_coaxil_por_regla = False
    
    # Carga de Hardware Obligatorio Base de Internet
    if prod_internet != "Ninguno":
        costo_hardware_usd += eq_cost_dict.get("ONT GPON ZXHN F6201B", 35.60)
    
    # Mapeo de elementos seleccionados en combo para procesar la matriz dinámica
    elementos_activos = []
    if prod_tv != "Ninguno": elementos_activos.append(prod_tv)
    if add_wiltel_on: elementos_activos.append("WILTEL ON")
    if add_mesh: elementos_activos.append("MESH")
    if add_futbol: elementos_activos.append("PAQUETE FÚTBOL")
    if add_premium: elementos_activos.append("PAQUETE TV PREMIUM")
    
    # Lógica de exclusividad MESH nativo
    es_150_mesh_plan = "150 MB MESH" in prod_internet
    
    for r in st.session_state.reglas_tecnicas:
        if r["Disparador (Venta)"] in elementos_activos:
            if r["Tipo Imputación"] == "Equipo":
                costo_hardware_usd += eq_cost_dict.get(r["Elemento Asignado"], 0.0)
            if r["Requiere Bolsa Coaxil"]:
                # Upgrade automático de la ONT por televisión cableada
                costo_hardware_usd = eq_cost_dict.get("ONT GPON ZXHN F6600R", 49.40)
                if prod_tv == "FULL TV HD": costo_hardware_usd += eq_cost_dict.get("STB mod HC-C730 (Beacon)", 35.00)
                requiere_coaxil_por_regla = True
            if r["Disparador (Venta)"] == "WILTEL ON":
                costo_hardware_usd += eq_cost_dict.get("DONGLE WILTEL ON", 28.60) + eq_cost_dict.get("MINI UPS WILTEL ON", 20.67)

    # Forzar hardware Mesh Nativo si aplica
    if es_150_mesh_plan:
        costo_hardware_usd = eq_cost_dict.get("ONT GPON ZXHN F601", 24.50) + (eq_cost_dict.get("Tenda NOVA MX3", 28.41) * 2)

    # Sumatoria dinámica indexada de las bolsas de materiales editables
    subtotal_ftth_usd = sum(float(x.get('Cantidad', 0)) * float(x.get('Costo Unitario USD', 0)) for x in st.session_state.mat_ftth if x.get('Cantidad'))
    subtotal_coaxil_usd = sum(float(x.get('Cantidad', 0)) * float(x.get('Costo Unitario USD', 0)) for x in st.session_state.mat_coaxil if x.get('Cantidad')) if requiere_coaxil_por_regla else 0.0
    
    inversion_kit_usd = st.session_state.costo_mo + costo_hardware_usd + subtotal_ftth_usd + subtotal_coaxil_usd
    inversion_kit_local = inversion_kit_usd * tc_local if moneda == "Pesos ARS" else inversion_kit_usd

    # Tarjeta: Combinación de Oferta (Pricing)
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Combinación de Oferta")
    col_pr1, col_pr2 = st.columns(2)
    with col_pr1:
        pct_recUniforme = st.slider("% de la inversión en cliente a recuperar como costo de instalación", 0, 100, 35) / 100.0
        cargo_neto = inversion_kit_local * pct_recUniforme
        saldo_a_amortizar = inversion_kit_local - cargo_neto
        
        divisor = (1.0 - costo_fact_local)
        cargo_instalacion_final = (cargo_neto / divisor) * (1.21 if segmento == "B2C" else 1.0)
        st.metric("Cargo de Instalación Mínimo Referencial", f"{'$' if moneda == 'Pesos ARS' else 'USD'} {cargo_instalacion_final:,.2f}")

    # RESOLUCIÓN PERMANENTE DE VARIABLES DE COSTOS DIRECTOS (Saneado definitivo de nombres)
    costo_directo_mensual_moneda = 0.0
    contribucion_marginal_local = 0.0
    cd_maestro_dict = {x['Concepto']: x for x in st.session_state.db_costos_directos}
    
    def procesar_costo_directo(concepto):
        if concepto in cd_maestro_dict:
            c_usd = float(cd_maestro_dict[concepto]["Costo USD"])
            m_pct = float(cd_maestro_dict[concepto]["Margen Deseado %"]) / 100.0
            c_local = c_usd * (tc_local if moneda == "Pesos ARS" else 1.0)
            precio_final_serv = c_local / (1.0 - m_pct) if m_pct < 1.0 else c_local
            return c_local, (precio_final_serv - c_local)
        return 0.0, 0.0

    if add_wiltel_on:
        c, m = procesar_costo_directo("Chip de datos WILTEL ON 1GB")
        costo_directo_mensual_moneda += c; contribucion_marginal_local += m
    if add_futbol:
        c, m = procesar_costo_directo("Paquete TV FÚTBOL")
        costo_directo_mensual_moneda += c; contribucion_marginal_local += m
    if add_premium:
        c, m = procesar_costo_directo("Paquete TV PREMIUM")
        costo_directo_mensual_moneda += c; contribucion_marginal_local += m

    # Cálculo base del abono mínimo referencial público exigido
    amortizacion_mensual_neta = (saldo_a_amortizar / pb_obj_local) + costo_directo_mensual_moneda + contribucion_marginal_local
    abono_minimo_final = (amortizacion_mensual_neta / divisor) * (1.21 if segmento == "B2C" else 1.0)

    with col_pr2:
        abono_comercial_lista = st.slider("Abono Mensual Regular de Lista (Para Simular)", int(abono_minimo_final * 0.4), int(abono_minimo_final * 2.5), int(abono_minimo_final))
        st.metric("Abono Mensual Mínimo Sugerido", f"{'$' if moneda == 'Pesos ARS' else 'USD'} {abono_minimo_final:,.2f}")
    st.markdown('</div>', unsafe_allow_html=True)

    # Tarjeta: Configuración de Escalas Promocionales (4 Tramos con Cajas Desplegables)
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Configuración de Escalas Promocionales")
    col_t1, col_t2, col_t3, col_t4 = st.columns(4)
    with col_t1:
        st.markdown("**Tramo 1**")
        meses_t1 = st.selectbox("Duración T1 (Meses)", [0,1,2,3,4,5,6,8,12], index=3)
        dto_t1 = st.slider("Descuento T1 (%)", 0, 100, 40, key="ds1") / 100.0
    with col_t2:
        st.markdown("**Tramo 2**")
        meses_t2 = st.selectbox("Duración T2 (Meses)", [0,1,2,3,4,5,6,8,12], index=7)
        dto_t2 = st.slider("Descuento T2 (%)", 0, 100, 20, key="ds2") / 100.0
    with col_t3:
        st.markdown("**Tramo 3**")
        meses_t3 = st.selectbox("Duración T3 (Meses)", [0,1,2,3,4,5,6,8,12], index=0)
        dto_t3 = st.slider("Descuento T3 (%)", 0, 100, 0, key="ds3") / 100.0
    with col_t4:
        st.markdown("**Tramo 4**")
        meses_t4 = st.selectbox("Duración T4 (Meses)", [0,1,2,3,4,5,6,8,12], index=0)
        dto_t4 = st.slider("Descuento T4 (%)", 0, 100, 0, key="ds4") / 100.0
    st.markdown('</div>', unsafe_allow_html=True)

    # --- SIMULACIÓN DEL FLUJO PARA PAYBACK REAL (Saneado completo de variables fijas) ---
    saldo_pendiente = saldo_a_amortizar
    payback_real = 0.0
    
    for mes in range(1, 37):
        if saldo_pendiente <= 0: break
        
        if mes <= meses_t1: precio_mes = abono_comercial_lista * (1.0 - dto_t1)
        elif mes <= (meses_t1 + meses_t2): precio_mes = abono_comercial_lista * (1.0 - dto_t2)
        elif mes <= (meses_t1 + meses_t2 + meses_t3): precio_mes = abono_comercial_lista * (1.0 - dto_t3)
        elif mes <= (meses_t1 + meses_t2 + meses_t3 + meses_t4): precio_mes = abono_comercial_lista * (1.0 - dto_t4)
        else: precio_mes = abono_comercial_lista
            
        precio_neto = (precio_mes / (1.21 if segmento == "B2C" else 1.0)) * divisor
        caja_amortizacion = precio_neto - costo_directo_mensual_moneda
        
        if caja_amortizacion > 0:
            if saldo_pendiente > caja_amortizacion:
                saldo_pendiente -= caja_amortizacion
                payback_real += 1.0
            else:
                payback_real += (saldo_pendiente / caja_amortizacion)
                saldo_pendiente = 0
        else:
            payback_real = 99.0
            break

    # Tarjeta: Validación Comercial
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Validación Comercial")
    if payback_real == 99.0:
        st.error("🔴 Semáforo Oferta: El precio promocional fijado es inviable porque no cubre los costos directos mínimos.")
    elif payback_real > pb_obj_local:
        st.error(f"🔴 Semáforo Oferta: RECHAZADO - El Payback Real es de {payback_real:.1f} meses. Supera tu límite estratégico de {pb_obj_local} meses.")
    else:
        st.success(f"🟢 Semáforo Oferta: APROBADO - El Payback Real es de {payback_real:.1f} meses. Oferta comercial financieramente sustentable.")
        
    st.caption(f"📊 Desglose Técnico Financiero del Kit: Inversión en Calle: USD {inversion_kit_usd:,.2f} (Equipos: USD {costo_hardware_usd:,.2f} | Bolsa FTTH: USD {subtotal_ftth_usd:,.2f} | Bolsa Coaxil: USD {subtotal_coaxil_usd:,.2f})")
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 2- PESTAÑA: ADMINISTRACIÓN COMERCIAL
# ==============================================================================
elif opcion_menu == "2- Administración Comercial":
    st.title("Administración Comercial")
    
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Parámetros Estratégicos")
    col_pcom1, col_pcom2, col_pcom3 = st.columns(3)
    with col_pcom1: st.session_state.comercial_params["tc"] = st.number_input("Tipo de Cambio Oficial (ARS/USD)", value=st.session_state.comercial_params["tc"], step=10.0)
    with col_pcom2: st.session_state.comercial_params["pb_objetivo"] = st.number_input("Payback Máximo Objetivo (Meses)", value=st.session_state.comercial_params["pb_objetivo"], min_value=1)
    with col_pcom3: st.session_state.comercial_params["costo_fact"] = st.number_input("Costo de Facturación (%)", value=st.session_state.comercial_params["costo_fact"], step=0.5)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Opciones de Productos")
    st.write("Agregá, modificá o eliminá productos de las listas interactivas verticales sin tocar código.")
    
    col_g1, col_g2, col_g3, col_g4 = st.columns(4)
    with col_g1:
        st.markdown("**Internet**")
        df_i = pd.DataFrame(st.session_state.db_internet, columns=["Producto"])
        res_i = st.data_editor(df_i, num_rows="dynamic", key="m_ed_i_v6")
        st.session_state.db_internet = res_i["Producto"].tolist()
    with col_g2:
        st.markdown("**TV**")
        df_t = pd.DataFrame(st.session_state.db_tv, columns=["Producto"])
        res_t = st.data_editor(df_t, num_rows="dynamic", key="m_ed_t_v6")
        st.session_state.db_tv = res_t["Producto"].tolist()
    with col_g3:
        st.markdown("**Telefonía**")
        df_tl = pd.DataFrame(st.session_state.db_telefonia, columns=["Producto"])
        res_tl = st.data_editor(df_tl, num_rows="dynamic", key="m_ed_tl_v6")
        st.session_state.db_telefonia = res_tl["Producto"].tolist()
    with col_g4:
        st.markdown("**Adicionales**")
        df_ad = pd.DataFrame(st.session_state.db_adicionales, columns=["Adicional"])
        res_ad = st.data_editor(df_ad, num_rows="dynamic", key="m_ed_ad_v6")
        st.session_state.db_adicionales = res_ad["Adicional"].tolist()
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 3- PESTAÑA: ADMINISTRACIÓN TÉCNICA
# ==============================================================================
elif opcion_menu == "3- Administración Técnica":
    st.title("Administración Técnica")
    
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Matriz Lógica de Vinculación de Kits y Reglas Técnicas")
    st.write("Configurá qué producto de venta dispara hardware del depósito o requiere activación de bolsa Coaxil:")
    
    df_reglas = pd.DataFrame(st.session_state.reglas_tecnicas)
    df_reglas_edit = st.data_editor(df_reglas, num_rows="dynamic", key="m_ed_reglas_v6")
    st.session_state.reglas_tecnicas = df_reglas_edit.to_dict('records')
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 4- PESTAÑA: ADMINISTRACIÓN DE COSTOS
# ==============================================================================
elif opcion_menu == "4- Administración de Costos":
    st.title("Administración de Costos")
    st.caption("⚠️ Valores expresados en **USD sin IVA**.")
    
    # Secciones una debajo de la otra de forma obligatoria para evitar desplazamientos horizontales
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Sección 1: Costos de Materiales, Equipos y Mano de Obra")
    
    st.session_state.costo_mo = st.number_input("Mano de Obra General de Instalación (USD)", value=st.session_state.costo_mo, step=1.0)
    st.markdown("---")
    
    st.markdown("#### Paquete de Materiales FTTH")
    df_f = pd.DataFrame(st.session_state.mat_ftth)
    df_f["Costo Unitario USD"] = df_f["Costo Unitario USD"].map(lambda x: float(x))
    df_f_edit = st.data_editor(df_f, num_rows="dynamic", key="ed_ftth_v6")
    st.session_state.mat_ftth = df_f_edit.to_dict('records')
    
    st.markdown("#### Paquete de Materiales Coaxil")
    df_c = pd.DataFrame(st.session_state.mat_coaxil)
    df_c["Costo Unitario USD"] = df_c["Costo Unitario USD"].map(lambda x: float(x))
    df_c_edit = st.data_editor(df_c, num_rows="dynamic", key="ed_coaxil_v6")
    st.session_state.mat_coaxil = df_c_edit.to_dict('records')
    
    st.markdown("#### Maestro de Equipos")
    df_eq = pd.DataFrame(st.session_state.db_equipos)
    df_eq_edit = st.data_editor(df_eq, num_rows="dynamic", key="ed_eq_v6")
    st.session_state.db_equipos = df_eq_edit.to_dict('records')
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Sección 2: Costos Directos")
    st.write("Gestión de costos recurrentes mensuales e insumos junto con el margen comercial deseado.")
    df_cd = pd.DataFrame(st.session_state.db_costos_directos)
    df_cd_edit = st.data_editor(df_cd, num_rows="dynamic", key="ed_cd_v6")
    st.session_state.db_costos_directos = df_cd_edit.to_dict('records')
    st.markdown('</div>', unsafe_allow_html=True)