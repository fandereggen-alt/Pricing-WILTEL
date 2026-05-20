import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN E IDENTIDAD VISUAL CORPORATIVA WILTEL
st.set_page_config(page_title="Pricing Wiltel", layout="wide", initial_sidebar_state="expanded")

# Inyección de estilos CSS para Tablero de Control Limpio (Tarjetas con línea gris superior)
st.markdown("""
    <style>
    .main { background-color: #f4f6f9; }
    [data-testid="stSidebar"] { background-color: #003366; min-width: 300px; }
    
    /* Texto del menú lateral: una sola línea, blanco */
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
    
    /* Contenedores tipo Tarjetas con línea gris superior sutil */
    .wiltel-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 4px;
        border-top: 2px solid #d1d5db;
        margin-bottom: 25px;
    }
    
    /* Forzar radio buttons y textos del menú lateral en blanco */
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
        color: #ffffff !important;
        font-size: 15px !important;
    }

    /* Sliders corporativos naranjas Wiltel */
    .stSlider > div [data-baseweb="slider"] { background-color: #ff823a; }
    
    /* Textos referenciales pequeños */
    .ref-text { font-size: 12px; color: #6b7280; }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZACIÓN DE LA BASE DE DATOS EN MEMORIA (Session State) ---

# Parámetros Estratégicos Comerciales
if 'comercial_params' not in st.session_state:
    st.session_state.comercial_params = {
        "tc": 1420.0, 
        "pb_objetivo": 6, 
        "costo_fact": 8.0,
        "pct_recupero_obj": 35.0
    }

# Cartera de Productos (Modificables en pestaña 2)
if 'db_internet' not in st.session_state: st.session_state.db_internet = ["WILTEL 25 MB", "WILTEL 50 MB", "WILTEL 150 MB", "WILTEL 300 MB", "Ninguno"]
if 'db_tv' not in st.session_state: st.session_state.db_tv = ["Ninguno", "WILTEL TV HD", "FULL TV HD", "PLAYME TV HD", "PLAYME FULL BOX"]
if 'db_telefonia' not in st.session_state: st.session_state.db_telefonia = ["Ninguno", "Línea Hogar Básica"]
if 'db_adicionales' not in st.session_state: st.session_state.db_adicionales = ["WILTEL ON", "MESH", "PAQUETE FUTBOL", "PAQUETE TV PREMIUM", "ALMACENAMIENTO CLOUD"]

# Mano de Obra e IVA
if 'costo_mo' not in st.session_state: st.session_state.costo_mo = 47.36
if 'iva_mo' not in st.session_state: st.session_state.iva_mo = 21.0

# Pack Materiales FTTH (Dinámico e interactivo con IVA individual)
if 'mat_ftth' not in st.session_state:
    st.session_state.mat_ftth = [
        {"Ítem": "DROP FTTH-SM 01 HILO", "Cantidad": 150.0, "Costo Unitario USD": 0.044, "IVA %": 21.0},
        {"Ítem": "CONECTOR RAPIDO SC/APC", "Cantidad": 2.0, "Costo Unitario USD": 1.20, "IVA %": 21.0},
        {"Ítem": "HEBILLA DE ACERO", "Cantidad": 4.0, "Costo Unitario USD": 0.15, "IVA %": 21.0},
        {"Ítem": "FLEJE DE ACERO", "Cantidad": 5.0, "Costo Unitario USD": 0.30, "IVA %": 21.0},
        {"Ítem": "SOPORTE B", "Cantidad": 2.0, "Costo Unitario USD": 1.80, "IVA %": 21.0},
        {"Ítem": "PATCHCORD SC/APC-SC/APC", "Cantidad": 1.0, "Costo Unitario USD": 2.50, "IVA %": 21.0}
    ]

# Pack Materiales Coaxil (Dinámico e interactivo con IVA individual)
if 'mat_coaxil' not in st.session_state:
    st.session_state.mat_coaxil = [
        {"Ítem": "CABLE RG-6 TRISHIELD s/p", "Cantidad": 20.0, "Costo Unitario USD": 0.31, "IVA %": 21.0},
        {"Ítem": "FICHA COMPRESION RG-6 PPC", "Cantidad": 4.0, "Costo Unitario USD": 0.80, "IVA %": 21.0},
        {"Ítem": "DIVISOR PPC 2 VIAS 1Ghz", "Cantidad": 1.0, "Costo Unitario USD": 3.20, "IVA %": 21.0},
        {"Ítem": "DIVISOR PPC 3 VIAS 1Ghz", "Cantidad": 0.0, "Costo Unitario USD": 4.50, "IVA %": 21.0},
        {"Ítem": "ATENUADOR F (FAM) de 8Db", "Cantidad": 1.0, "Costo Unitario USD": 2.60, "IVA %": 21.0}
    ]

# Maestro de Equipos (Con IVA por equipo)
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

# Costos Directos Recurrentes
if 'db_costos_directos' not in st.session_state:
    st.session_state.db_costos_directos = [
        {"Concepto": "Chip de datos WILTEL ON 1GB", "Costo USD": 5.00, "Margen Deseado %": 20.0},
        {"Concepto": "Chip WILTEL ON 5GB", "Costo USD": 9.50, "Margen Deseado %": 25.0},
        {"Concepto": "Paquete TV FÚTBOL", "Costo USD": 8.00, "Margen Deseado %": 15.0},
        {"Concepto": "Paquete TV PREMIUM", "Costo USD": 6.50, "Margen Deseado %": 15.0},
        {"Concepto": "Almacenamiento Cloud 50GB", "Costo USD": 2.00, "Margen Deseado %": 30.0}
    ]

# Matriz Base del Motor de 3 Capas (Configurable)
if 'reglas_tecnicas' not in st.session_state:
    st.session_state.reglas_tecnicas = [
        {"Internet": "WILTEL 150 MB", "TV": "Ninguno", "Adicional": "Ninguno", "Equipo Base": "ONT GPON ZXHN F6201B", "Requiere Coaxil": "No"},
        {"Internet": "Cualquiera", "TV": "WILTEL TV HD", "Adicional": "Ninguno", "Equipo Base": "ONT GPON ZXHN F6600R", "Requiere Coaxil": "Sí"},
        {"Internet": "Cualquiera", "TV": "FULL TV HD", "Adicional": "Ninguno", "Equipo Base": "ONT GPON ZXHN F6600R", "Requiere Coaxil": "Sí"},
        {"Internet": "WILTEL 150 MB", "TV": "Ninguno", "Adicional": "MESH", "Equipo Base": "ONT GPON ZXHN F601", "Requiere Coaxil": "No"}
    ]

# --- MENÚ LATERAL UNIFICADO EN UNA SOLA LÍNEA ---
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
    st.markdown("---")
    st.caption("CPQ Pricing Engine v2026")

# Funciones globales de formateo
def fmt_usd(val): return f"USD {val:,.2f}"
def fmt_ars(val): return f"$ {val:,.2f}"

# ==============================================================================
# 1- SIMULACIÓN COMERCIAL
# ==============================================================================
if opcion_menu == "Simulación Comercial":
    st.title("Simulación Comercial")
    
    # Tarjeta 1: Configuración Comercial
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Configuración Comercial")
    col_cc1, col_cc2 = st.columns(2)
    with col_cc1:
        segmento = st.selectbox("Segmento de Cliente", ["B2C", "B2B"])
    with col_cc2:
        opciones_moneda = ["Pesos ARS"] if segmento == "B2C" else ["Pesos ARS", "Dólares USD"]
        moneda = st.selectbox("Moneda de Cotización", opciones_moneda)
    
    st.markdown("""
    <p style='font-size:12px; color:#6b7280; margin-top:10px;'>
    ⚠️ <strong>Precios de instalación y abonos expresados en:</strong><br>
    • $ con IVA incluido para B2C<br>
    • Moneda seleccionada sin IVA para B2B
    </p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Tarjeta 2: Combo
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Combo")
    col_cmb1, col_cmb2, col_cmb3 = st.columns(3)
    with col_cmb1: prod_internet = st.selectbox("Internet", st.session_state.db_internet, index=2)
    with col_cmb2: prod_tv = st.selectbox("TV", st.session_state.db_tv, index=1)
    with col_cmb3: prod_tel = st.selectbox("Telefonía", st.session_state.db_telefonia, index=0)
    
    st.markdown("**Adicionales Disponibles**")
    col_a1, col_a2, col_a3, col_a4 = st.columns(4)
    with col_a1: add_wiltel_on = st.checkbox("WILTEL ON")
    with col_a2: add_mesh = st.checkbox("MESH")
    with col_a3: add_futbol = st.checkbox("PAQUETE FÚTBOL")
    with col_a4: add_premium = st.checkbox("PAQUETE TV PREMIUM")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- RESOLUCIÓN MATEMÁTICA INTERNA DEL MOTOR POR 3 CAPAS ---
    tc = st.session_state.comercial_params["tc"]
    costo_fact_pct = st.session_state.comercial_params["costo_fact"] / 100.0
    pb_objetivo = st.session_state.comercial_params["pb_objetivo"]
    
    eq_cost_dict = {x['Equipo']: float(x['Costo USD']) for x in st.session_state.db_equipos}
    eq_iva_dict = {x['Equipo']: float(x['IVA %']) / 100.0 for x in st.session_state.db_equipos}
    
    costo_hardware_usd = 0.0
    iva_acumulado_hardware_usd = 0.0
    requiere_coaxil = False

    # Capa 1 y 2: Evaluación cruzada de conectividad base + TV
    if prod_tv in ["WILTEL TV HD", "FULL TV HD", "PLAYME TV HD"]:
        nombre_ont = "ONT GPON ZXHN F6600R"
        requiere_coaxil = True
    elif "150 MB" in prod_internet and add_mesh:
        nombre_ont = "ONT GPON ZXHN F601"
    else:
        nombre_ont = "ONT GPON ZXHN F6201B" if prod_internet != "Ninguno" else "Ninguno"

    if nombre_ont != "Ninguno":
        costo_hardware_usd += eq_cost_dict.get(nombre_ont, 0.0)
        iva_acumulado_hardware_usd += eq_cost_dict.get(nombre_ont, 0.0) * eq_iva_dict.get(nombre_ont, 0.21)

    if prod_tv == "FULL TV HD":
        costo_hardware_usd += eq_cost_dict.get("STB mod HC-C730 (Beacon)", 0.0)
        iva_acumulado_hardware_usd += eq_cost_dict.get("STB mod HC-C730 (Beacon)", 0.0) * eq_iva_dict.get("STB mod HC-C730 (Beacon)", 0.21)

    # Capa 3: Modificadores por Adicionales Activos
    if add_wiltel_on:
        costo_hardware_usd += eq_cost_dict.get("DONGLE WILTEL ON", 0.0) + eq_cost_dict.get("MINI UPS WILTEL ON", 0.0)
        iva_acumulado_hardware_usd += (eq_cost_dict.get("DONGLE WILTEL ON", 0.0) * eq_iva_dict.get("DONGLE WILTEL ON", 0.21)) + (eq_cost_dict.get("MINI UPS WILTEL ON", 0.0) * eq_iva_dict.get("MINI UPS WILTEL ON", 0.21))
    if add_mesh:
        if "150 MB" in prod_internet:
            costo_hardware_usd += eq_cost_dict.get("Tenda NOVA MX3", 0.0) * 2
            iva_acumulado_hardware_usd += (eq_cost_dict.get("Tenda NOVA MX3", 0.0) * eq_iva_dict.get("Tenda NOVA MX3", 0.21)) * 2
        else:
            costo_hardware_usd += eq_cost_dict.get("ZXHN H3601N (Router)", 0.0)
            iva_acumulado_hardware_usd += eq_cost_dict.get("ZXHN H3601N (Router)", 0.0) * eq_iva_dict.get("ZXHN H3601N (Router)", 0.21)

    # Lógica de IVA dinámico para Pack de Materiales FTTH
    subtotal_ftth_neto = sum(float(x['Cantidad']) * float(x['Costo Unitario USD']) for x in st.session_state.mat_ftth if x.get('Cantidad'))
    iva_ftth_usd = sum(float(x['Cantidad']) * float(x['Costo Unitario USD']) * (float(x['IVA %']) / 100.0) for x in st.session_state.mat_ftth if x.get('Cantidad'))
    
    # Lógica de IVA dinámico para Pack de Materiales Coaxil
    subtotal_coaxil_neto = sum(float(x['Cantidad']) * float(x['Costo Unitario USD']) for x in st.session_state.mat_coaxil if x.get('Cantidad')) if requiere_coaxil else 0.0
    iva_coaxil_usd = sum(float(x['Cantidad']) * float(x['Costo Unitario USD']) * (float(x['IVA %']) / 100.0) for x in st.session_state.mat_coaxil if x.get('Cantidad')) if requiere_coaxil else 0.0

    # Consolidación del IVA del Kit Completo para desgloses Ponderados
    costo_mo_neto = st.session_state.costo_mo
    iva_mo_usd = costo_mo_neto * (st.session_state.iva_mo / 100.0)

    total_kit_neto_usd = costo_mo_neto + costo_hardware_usd + subtotal_ftth_neto + subtotal_coaxil_neto
    total_iva_kit_usd = iva_mo_usd + iva_acumulado_hardware_usd + iva_ftth_usd + iva_coaxil_usd
    iva_ponderado_kit = (total_iva_kit_usd / total_kit_neto_usd) if total_kit_neto_usd > 0 else 0.21

    inversion_kit_local = total_kit_neto_usd * tc if moneda == "Pesos ARS" else total_kit_neto_usd

    # Tarjeta 3: Combinación de Oferta
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Combinación de Oferta")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        pct_recupero = st.slider("% de la inversión en cliente a recuperar como costo de instalación", 0, 100, int(st.session_state.comercial_params["pct_recupero_obj"])) / 100.0
        cargo_instalacion_neto = inversion_kit_local * pct_recupero
        saldo_a_amortizar = inversion_kit_local - cargo_instalacion_neto
        
        divisor_imp = (1.0 - costo_fact_local)
        cargo_publico_final = (cargo_instalacion_neto / divisor_imp) * (1.0 + iva_ponderado_kit if segmento == "B2C" else 1.0)
        
        # Muestra el valor en ARS o USD según corresponda
        str_cargo = fmt_ars(cargo_publico_final) if moneda == "Pesos ARS" else fmt_usd(cargo_publico_final)
        st.write(f"### **Cargo de Instalación:** {str_cargo}")
        st.markdown("<p class='ref-text'>Valor de folleto calculado dinámicamente con el promedio de IVA de los insumos seleccionados.</p>", unsafe_allow_html=True)

    # Costos Directos Recurrentes
    costo_directo_mensual_local = 0.0
    contribucion_marginal_local = 0.0
    cd_dict = {x['Concepto']: x for x in st.session_state.db_costos_directos}
    
    def calcular_impacto_cd(concepto_str):
        if concepto_str in cd_dict:
            c_usd = float(cd_dict[concepto_str]["Costo USD"])
            m_pct = float(cd_dict[concepto_str]["Margen Deseado %"]) / 100.0
            c_loc = c_usd * (tc if moneda == "Pesos ARS" else 1.0)
            precio_neto_interno = c_loc / (1.0 - m_pct) if m_pct < 1.0 else c_loc
            return c_loc, (precio_neto_interno - c_loc)
        return 0.0, 0.0

    if add_wiltel_on:
        c, m = calcular_impacto_cd("Chip de datos WILTEL ON 1GB")
        costo_directo_mensual_local += c; contribucion_marginal_local += m
    if add_futbol:
        c, m = calcular_impacto_cd("Paquete TV FÚTBOL")
        costo_directo_mensual_local += c; contribucion_marginal_local += m
    if add_premium:
        c, m = calcular_impacto_cd("Paquete TV PREMIUM")
        costo_directo_mensual_local += c; contribucion_marginal_local += m

    # Cálculo matemático puro del Punto de Equilibrio Exigido
    amortizacion_mensual_exigida = (saldo_a_amortizar / pb_objetivo) + costo_directo_mensual_local + contribucion_marginal_local
    abono_equilibrio_sugerido = (amortizacion_mensual_exigida / divisor_imp) * (1.21 if segmento == "B2C" else 1.0)

    with col_p2:
        abono_simulado_regular = st.slider("Abono Mensual Regular de Lista (Para Simular)", int(abono_equilibrio_sugerido*0.4), int(abono_equilibrio_sugerido*2.5), int(abono_equilibrio_sugerido))
        str_abono_sug = fmt_ars(abono_equilibrio_sugerido) if moneda == "Pesos ARS" else fmt_usd(abono_equilibrio_sugerido)
        st.write(f"### **Abono de Equilibrio Objetivo:** {str_abono_sug}")
        st.markdown(f"<p class='ref-text'>Este abono logra equilibrar exactamente la instalación cobrada para saldar el kit en {pb_objetivo} meses.</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Tarjeta 4: Configuración de Escalas Promocionales (Visual Minimalista Solicitada)
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Configuración de Escalas Promocionales")
    col_t1, col_t2, col_t3, col_t4 = st.columns(4)
    with col_t1:
        st.markdown("**Tramo 1**")
        meses_t1 = st.selectbox("duración (meses)", [0,1,2,3,4,6,12], index=3, key="m_t1")
        dto_t1 = st.slider("descuento", 0, 100, 40, key="d_t1") / 100.0
    with col_t2:
        st.markdown("**Tramo 2**")
        meses_t2 = st.selectbox("duración (meses)", [0,1,2,3,4,6,12], index=0, key="m_t2")
        dto_t2 = st.slider("descuento", 0, 100, 20, key="d_t2") / 100.0
    with col_t3:
        st.markdown("**Tramo 3**")
        meses_t3 = st.selectbox("duración (meses)", [0,1,2,3,4,6,12], index=0, key="m_t3")
        dto_t3 = st.slider("descuento", 0, 100, 0, key="d_t3") / 100.0
    with col_t4:
        st.markdown("**Tramo 4**")
        meses_t4 = st.selectbox("duración (meses)", [0,1,2,3,4,6,12], index=0, key="m_t4")
        dto_t4 = st.slider("descuento", 0, 100, 0, key="d_t4") / 100.0
    st.markdown('</div>', unsafe_allow_html=True)

    # --- SIMULACIÓN DEL FLUJO MES A MES VINCULANDO LAS ESCALAS AL PAYBACK REAL ---
    saldo_pendiente_kit = saldo_a_amortizar
    payback_real_calculado = 0.0
    inviable_operativo = False
    
    for mes in range(1, 49):
        if saldo_pendiente_kit <= 0: break
        
        # Evaluar el precio neto que efectivamente ingresa a caja según la escala activa
        if mes <= meses_t1: precio_folleto_mes = abono_simulado_regular * (1.0 - dto_t1)
        elif mes <= (meses_t1 + meses_t2): precio_folleto_mes = abono_simulado_regular * (1.0 - dto_t2)
        elif mes <= (meses_t1 + meses_t2 + meses_t3): precio_folleto_mes = abono_simulado_regular * (1.0 - dto_t3)
        elif mes <= (meses_t1 + meses_t2 + meses_t3 + meses_t4): precio_folleto_mes = abono_simulado_regular * (1.0 - dto_t4)
        else: precio_folleto_mes = abono_simulado_regular
            
        # Desglose de impuestos a la inversa para ver la caja neta libre
        precio_neto_empresa = (precio_folleto_mes / (1.21 if segmento == "B2C" else 1.0)) * divisor_imp
        recaudación_limpia_mes = precio_neto_empresa - costo_directo_mensual_local
        
        if recaudación_limpia_mes > 0:
            if saldo_pendiente_kit > recaudación_limpia_mes:
                saldo_pendiente_kit -= recaudación_limpia_mes
                payback_real_calculado += 1.0
            else:
                payback_real_calculado += (saldo_pendiente_kit / recaudación_limpia_mes)
                saldo_pendiente_kit = 0
        else:
            inviable_operativo = True
            break

    # Tarjeta 5: Validación Comercial
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Validación Comercial")
    if inviable_operativo:
        st.error("🔴 Semáforo Oferta: RECHAZADO - La escala promocional baja el abono por debajo de los costos directos fijos del servicio.")
    elif payback_real_calculated := payback_real_calculado if not inviable_operativo else 99.0:
        if payback_real_calculated > pb_objetivo:
            st.error(f"🔴 Semáforo Oferta: RECHAZADO - Las promociones estiran el Payback Real a {payback_real_calculated:.1f} meses. Supera tu objetivo de {pb_objetivo} meses.")
        else:
            st.success(f"🟢 Semáforo Oferta: APROBADO - Payback Real de {payback_real_calculated:.1f} meses. Cumple la meta estratégica.")
            
    st.caption(f"Desglose de Costo de Materiales y Equipos: Total Neto del Kit: USD {total_kit_neto_usd:,.2f} | IVA Promedio del Kit: {iva_ponderado_kit*100:.1f}%")
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 2- TABLERO ADMINISTRACIÓN COMERCIAL (Cuadrícula 2x2 Ordenada)
# ==============================================================================
elif opcion_menu == "Tablero Administración Comercial":
    st.title("Administración Comercial")
    
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Parámetros Estratégicos")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.session_state.comercial_params["tc"] = st.number_input("Tipo de Cambio", value=st.session_state.comercial_params["tc"])
    with c2: st.session_state.comercial_params["pb_objetivo"] = st.number_input("Payback Objetivo (Meses)", value=st.session_state.comercial_params["pb_objetivo"])
    with c3: st.session_state.comercial_params["costo_fact"] = st.number_input("Costo de Facturación (%)", value=st.session_state.comercial_params["costo_fact"])
    with c4: st.session_state.comercial_params["pct_recupero_obj"] = st.number_input("% Recupero Inversión Obj. (Slider)", value=st.session_state.comercial_params["pct_recupero_obj"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Opciones de Productos")
    
    # Cuadrícula 2x2 perfecta solicitada para visualización completa
    fila1_col1, fila1_col2 = st.columns(2)
    with fila1_col1:
        st.markdown("**Internet**")
        df_i = pd.DataFrame(st.session_state.db_internet, columns=["Producto"])
        res_i = st.data_editor(df_i, num_rows="dynamic", key="grid_int", height=200, use_container_width=True)
        st.session_state.db_internet = res_i["Producto"].tolist()
    with fila1_col2:
        st.markdown("**TV**")
        df_t = pd.DataFrame(st.session_state.db_tv, columns=["Producto"])
        res_t = st.data_editor(df_t, num_rows="dynamic", key="grid_tv", height=200, use_container_width=True)
        st.session_state.db_tv = res_t["Producto"].tolist()
        
    fila2_col1, fila2_col2 = st.columns(2)
    with fila2_col1:
        st.markdown("**Telefonía**")
        df_tl = pd.DataFrame(st.session_state.db_telefonia, columns=["Producto"])
        res_tl = st.data_editor(df_tl, num_rows="dynamic", key="grid_tel", height=150, use_container_width=True)
        st.session_state.db_telefonia = res_tl["Producto"].tolist()
    with fila2_col2:
        st.markdown("**Adicionales**")
        df_ad = pd.DataFrame(st.session_state.db_adicionales, columns=["Adicional"])
        res_ad = st.data_editor(df_ad, num_rows="dynamic", key="grid_add", height=150, use_container_width=True)
        st.session_state.db_adicionales = res_ad["Adicional"].tolist()
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 3- TABLERO ADMINISTRACIÓN TÉCNICA (Matriz de Reglas)
# ==============================================================================
elif opcion_menu == "Tablero Administración Técnica":
    st.title("Administración Técnica")
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Matriz Lógica de Vinculación de Kits y Reglas Técnicas")
    st.write("Configurá los escenarios anidados cruzados para definir qué combinaciones disparan hardware del depósito:")
    df_reglas = pd.DataFrame(st.session_state.reglas_tecnicas)
    df_reglas_edit = st.data_editor(df_reglas, num_rows="dynamic", key="grid_reglas", use_container_width=True)
    st.session_state.reglas_tecnicas = df_reglas_edit.to_dict('records')
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 4- TABLERO ADMINISTRACIÓN DE COSTOS (Ubicación vertical con totales al pie)
# ==============================================================================
elif opcion_menu == "Tablero Administración de Costos":
    st.title("Administración de Costos")
    st.caption("⚠️ Valores en USD sin IVA")
    
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Sección 1: Costos de Materiales, Equipos y Mano de Obra")
    st.session_state.costo_mo = st.number_input("Mano de Obra General de Instalación (USD)", value=st.session_state.costo_mo, step=1.0)
    
    # Formateo rígido de moneda USD solicitado
    conf_moneda = {"Costo Unitario USD": st.column_config.NumberColumn(format="USD %.2f"), "Costo USD": st.column_config.NumberColumn(format="USD %.2f")}
    
    # Pack 1: FTTH
    st.markdown("---")
    st.markdown("#### pack materiales FTTH")
    df_f = pd.DataFrame(st.session_state.mat_ftth)
    df_f_edit = st.data_editor(df_f, num_rows="dynamic", column_config=conf_moneda, key="ed_ftth_final", use_container_width=True)
    st.session_state.mat_ftth = df_f_edit.to_dict('records')
    
    # Importe al pie solicitado
    tot_ftth_usd = sum(float(x.get('Cantidad', 0)) * float(x.get('Costo Unitario USD', 0)) for x in st.session_state.mat_ftth if x.get('Cantidad'))
    st.markdown(f"**Importe total del pack materiales FTTH diseñado:** `USD {tot_ftth_usd:,.2f}`")
    
    # Pack 2: Coaxil (Ubicado abajo obligatoriamente)
    st.markdown("---")
    st.markdown("#### pack de materiales coaxil")
    df_c = pd.DataFrame(st.session_state.mat_coaxil)
    df_c_edit = st.data_editor(df_c, num_rows="dynamic", column_config=conf_moneda, key="ed_coaxil_final", use_container_width=True)
    st.session_state.mat_coaxil = df_c_edit.to_dict('records')
    
    # Importe al pie solicitado
    tot_coaxil_usd = sum(float(x.get('Cantidad', 0)) * float(x.get('Costo Unitario USD', 0)) for x in st.session_state.mat_coaxil if x.get('Cantidad'))
    st.markdown(f"**Importe total del pack de materiales coaxil diseñado:** `USD {tot_coaxil_usd:,.2f}`")
    
    # Maestro de Equipos
    st.markdown("---")
    st.markdown("#### Maestro de Equipos")
    df_eq = pd.DataFrame(st.session_state.db_equipos)
    df_eq_edit = st.data_editor(df_eq, num_rows="dynamic", column_config=conf_moneda, key="ed_eq_final", use_container_width=True)
    st.session_state.db_equipos = df_eq_edit.to_dict('records')
    st.markdown('</div>', unsafe_allow_html=True)

    # Sección 2: Costos Directos
    st.markdown('<div class="wiltel-card">', unsafe_allow_html=True)
    st.subheader("Sección 2: Costos Directos")
    df_cd = pd.DataFrame(st.session_state.db_costos_directos)
    df_cd_edit = st.data_editor(df_cd, num_rows="dynamic", column_config=conf_moneda, key="ed_cd_final", use_container_width=True)
    st.session_state.db_costos_directos = df_cd_edit.to_dict('records')
    st.markdown('</div>', unsafe_allow_html=True)