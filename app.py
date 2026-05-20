import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE PÁGINA E IDENTIDAD CORPORATIVA
st.set_page_config(page_title="Pricing Wiltel", layout="wide", initial_sidebar_state="expanded")

# Inyección de estilos CSS para lograr el formato de Tablero Corporativo Wiltel
st.markdown("""
    <style>
    .main { background-color: #f4f6f9; }
    [data-testid="stSidebar"] { background-color: #003366; }
    [data-testid="stSidebar"] .stMarkdown p { color: white; font-weight: bold; }
    h1, h2, h3, h4 { color: #003366; font-family: 'Helvetica Neue', Arial, sans-serif; }
    .wiltel-container {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border-left: 5px solid #003366;
    }
    .stButton>button { background-color: #003366; color: white; border-radius: 4px; width: 100%; }
    .stCheckbox label p { font-size: 15px; font-weight: 500; }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZACIÓN DE LA BASE DE DATOS MUTABLE (Session State) ---

# Parámetros Comerciales
if 'comercial_params' not in st.session_state:
    st.session_state.comercial_params = {
        "tc": 1420.0,
        "pb_objetivo": 6,
        "costo_fact": 8.0
    }

# Carteras de Productos (Modificables en Administración Comercial)
if 'db_internet' not in st.session_state:
    st.session_state.db_internet = ["Ninguno", "WILTEL 25 MB", "WILTEL 50 MB", "WILTEL 150 MB", "WILTEL 300 MB"]

if 'db_tv' not in st.session_state:
    st.session_state.db_tv = ["Ninguno", "WILTEL TV HD", "FULL TV HD", "PLAYME TV HD", "PLAYME FULL BOX"]

if 'db_telefonia' not in st.session_state:
    st.session_state.db_telefonia = ["Ninguno", "Línea Hogar Básica"]

if 'db_adicionales' not in st.session_state:
    st.session_state.db_adicionales = ["WILTEL ON", "MESH", "PAQUETE FUTBOL", "PAQUETE TV PREMIUM", "ALMACENAMIENTO CLOUD"]

# Administración de Costos (USD sin IVA)
if 'costo_mo' not in st.session_state: st.session_state.costo_mo = 47.36
if 'iva_mo' not in st.session_state: st.session_state.iva_mo = 21.0

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

# --- MENÚ LATERAL DE NAVEGACIÓN CORPORATIVA ---
with st.sidebar:
    st.image("https://www.wiltel.com.ar/wp-content/uploads/2021/04/wiltel_blanco.png", width=180, errors="ignore")
    st.markdown("### Menú de Navegación")
    opcion_menu = st.radio(
        "Ir a pestaña:",
        [
            "🎮 Tablero de Simulación Comercial",
            "🏢 Administración Comercial",
            "🛠️ Administración Técnica",
            "💲 Administración de Costos"
        ]
    )
    st.sidebar.markdown("---")
    st.sidebar.caption("Wiltel Comunicaciones S.A. | Departamento de Pricing v2026")

# ==============================================================================
# 1. PESTAÑA: TABLERO DE SIMULACIÓN COMERCIAL
# ==============================================================================
if opcion_menu == "🎮 Tablero de Simulación Comercial":
    st.title("Pricing Wiltel")
    
    # Contenedor: Configuración Comercial
    st.markdown('<div class="wiltel-container">', unsafe_allow_html=True)
    st.subheader("Configuración Comercial")
    col_cc1, col_cc2, col_cc3 = st.columns(3)
    with col_cc1:
        segmento = st.selectbox("Segmento de Cliente", ["Consumidor Final (Con IVA)", "Corporativo (Neto sin IVA)"])
    with col_cc2:
        moneda = st.selectbox("Moneda de Cotización", ["Pesos ARS", "Dólares USD"])
    with col_cc3:
        st.caption("📢 *Nota de Facturación:* Consumidor Final calcula en ARS con IVA incluido. Corporativo en la moneda elegida Neto sin IVA.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Contenedor: Combo
    st.markdown('<div class="wiltel-container">', unsafe_allow_html=True)
    st.subheader("Combo")
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        prod_internet = st.selectbox("Caja 1: Internet", st.session_state.db_internet)
    with col_p2:
        prod_tv = st.selectbox("Caja 2: TV", st.session_state.db_tv)
    with col_p3:
        prod_tel = st.selectbox("Caja 3: Telefonía", st.session_state.db_telefonia)
    
    st.markdown("**Caja 4: Adicionales (Selección Múltiple simultánea)**")
    col_add1, col_add2, col_add3, col_add4 = st.columns(4)
    
    # Lógica de Restricción Cruzada Nativa (Wiltel 150 MB MESH bloquea Adicional Mesh)
    es_150_mesh_plan = "150 MB MESH" in prod_internet
    
    with col_add1:
        add_wiltel_on = st.checkbox("WILTEL ON")
    with col_add2:
        if es_150_mesh_plan:
            st.checkbox("MESH", value=False, disabled=True, help="El plan de Internet ya cuenta con Mesh integrado.")
            add_mesh = False
        else:
            add_mesh = st.checkbox("MESH")
    with col_add3:
        add_futbol = st.checkbox("PAQUETE FÚTBOL")
    with col_add4:
        add_premium = st.checkbox("PAQUETE TV PREMIUM")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- RESOLUCIÓN TÉCNICA DEL KIT DETRÁS DE ESCENA VÍA REGLAS ---
    tc_local = st.session_state.comercial_params["tc"]
    costo_fact_local = st.session_state.comercial_params["costo_fact"] / 100.0
    pb_obj_local = st.session_state.comercial_params["pb_objetivo"]
    
    # Inicialización de costos base extraídos desde las configuraciones técnicas y de costos
    eq_dict = {item['Equipo']: float(item['Costo USD']) for item in st.session_state.db_equipos}
    
    total_hw_usd = 0.0
    lleva_coaxil = False
    
    # Reglas de Inclusión de Equipamiento de Fibra e Internet
    if es_150_mesh_plan:
        total_hw_usd += eq_dict.get("ONT GPON ZXHN F601", 24.50) + (eq_dict.get("Tenda NOVA MX3", 28.41) * 2)
    elif prod_internet != "Ninguno":
        total_hw_usd += eq_dict.get("ONT GPON ZXHN F6201B", 35.60)
        
    # Reglas de TV e Inclusión de bolsa Coaxil
    if prod_tv in ["WILTEL TV HD", "FULL TV HD", "PLAYME TV HD"]:
        if not es_mesh_nativo and prod_internet != "Ninguno":
            total_hw_usd = eq_dict.get("ONT GPON ZXHN F6600R", 49.40) # Upgrade automático de ONT
        lleva_coaxil = True
        
    if prod_tv == "FULL TV HD":
        total_hw_usd += eq_dict.get("STB mod HC-C730 (Beacon)", 35.00)
        
    # Reglas de Adicionales Activos
    if add_wiltel_on:
        total_hw_usd += eq_dict.get("DONGLE WILTEL ON", 28.60) + eq_dict.get("MINI UPS WILTEL ON", 20.67)
    if add_mesh:
        total_hw_usd += eq_dict.get("ZXHN H3601N (Router)", 35.60)

    # Costeo dinámico de materiales según las tablas editables fila por fila
    subtotal_ftth_usd = sum(float(m['Cantidad']) * float(m['Costo Unitario USD']) for m in st.session_state.mat_ftth if m.get('Cantidad') and m.get('Costo Unitario USD'))
    subtotal_coaxil_usd = sum(float(m['Cantidad']) * float(m['Costo Unitario USD']) for m in st.session_state.mat_coaxil if m.get('Cantidad') and m.get('Costo Unitario USD')) if lleva_coaxil else 0.0
    
    inversion_kit_usd = st.session_state.costo_mo + total_hw_usd + subtotal_ftth_usd + subtotal_coaxil_usd
    inversion_kit_local = inversion_kit_usd * tc_local if moneda == "Pesos ARS" else inversion_kit_usd

    # --- COMBINACIÓN DE OFERTA (Pricing) ---
    st.markdown('<div class="wiltel-container">', unsafe_allow_html=True)
    st.subheader("Combinación de Oferta")
    
    col_pr1, col_pr2 = st.columns(2)
    with col_pr1:
        pct_recupero = st.slider("% de Inversión Inicial a recuperar como Cargo de Instalación", 0, 100, 35) / 100.0
        cargo_instalacion_neto = inversion_kit_local * pct_recupero
        saldo_a_amortizar = inversion_kit_local - cargo_instalacion_neto
        
        # Aplicación inversa de impuestos y facturación (Grossing up)
        divisor = (1.0 - costo_fact_local)
        cargo_instalacion_final = (cargo_instalacion_neto / divisor) * (1.21 if segmento == "Consumidor Final (Con IVA)" else 1.0)
        st.metric("Cargo de Instalación Mínimo Referencial", f"{'$' if moneda == 'Pesos ARS' else 'USD'} {cargo_instalacion_final:,.2f}")

    # Lógica de Costos Directos Vinculados + Margen de Contribución Comercial
    costo_directo_recurrente_local = 0.0
    contribucion_marginal_local = 0.0
    cd_dict = {item['Concepto']: item for item in st.session_state.db_costos_directos}
    
    def acumular_cd(concepto_nombre):
        if concepto_nombre in cd_dict:
            c_usd = float(cd_dict[concepto_nombre]["Costo USD"])
            m_pct = float(cd_dict[concepto_nombre]["Margen Deseado %"]) / 100.0
            c_local = c_usd * (tc_local if moneda == "Pesos ARS" else 1.0)
            precio_serv = c_local / (1.0 - m_pct) if m_pct < 1.0 else c_local
            return c_local, (precio_serv - c_local)
        return 0.0, 0.0

    if add_wiltel_on:
        c, m = acumular_cd("Chip de datos WILTEL ON 1GB")
        costo_directo_recurrente_local += c; contribucion_marginal_local += m
    if add_futbol:
        c, m = acumular_cd("Paquete TV FÚTBOL")
        costo_directo_recurrente_local += c; contribucion_marginal_local += m
    if add_premium:
        c, m = acumular_cd("Paquete TV PREMIUM")
        costo_directo_recurrente_local += c; contribucion_marginal_local += m

    # Cálculo del abono de lista mínimo exigido para saldar el kit
    amortizacion_mensual_neta = (saldo_a_amortizar / pb_obj_local) + costo_directo_recurrente_local + contribucion_marginal_local
    abono_minimo_final = (amortizacion_mensual_neta / divisor) * (1.21 if segmento == "Consumidor Final (Con IVA)" else 1.0)

    with col_pr2:
        abono_comercial_lista = st.slider("Abono Mensual Regular de Lista (Para Simular)", int(abono_minimo_final * 0.4), int(abono_minimo_final * 2.5), int(abono_minimo_final))
        st.metric("Abono Mensual Mínimo Sugerido", f"{'$' if moneda == 'Pesos ARS' else 'USD'} {abono_minimo_final:,.2f}")
    st.markdown('</div>', unsafe_allow_html=True)

    # Contenedor: Configuración de Escalas Promocionales
    st.markdown('<div class="wiltel-container">', unsafe_allow_html=True)
    st.subheader("Configuración de Escalas Promocionales")
    col_d1, col_d2, col_d3, col_d4 = st.columns(4)
    with col_d1:
        meses_t1 = st.slider("Duración Escala 1 (Meses)", 0, 12, 4)
    with col_d2:
        dto_t1 = st.slider("Descuento Escala 1 (%)", 0, 100, 40) / 100.0
    with col_d3:
        meses_t2 = st.slider("Duración Escala 2 (Meses)", 0, 12, 8)
    with col_d4:
        dto_t2 = st.slider("Descuento Escala 2 (%)", 0, 100, 20) / 100.0
    st.markdown('</div>', unsafe_allow_html=True)

    # --- VALIDACIÓN COMERCIAL (Cálculo del Flujo de Fondos Real) ---
    saldo_pendiente = saldo_a_amortizar
    payback_real = 0.0
    
    for mes in range(1, 37):
        if saldo_pendiente <= 0: break
        
        # Evaluar el precio según el tramo de la escala promocional
        if mes <= meses_t1:
            precio_mes = abono_comercial_lista * (1.0 - dto_t1)
        elif mes <= (meses_t1 + meses_t2):
            precio_mes = abono_comercial_lista * (1.0 - dto_t2)
        else:
            precio_mes = abono_comercial_lista
            
        # Grossing down de impuestos
        precio_neto = (precio_mes / (1.21 if segmento == "Consumidor Final (Con IVA)" else 1.0)) * divisor
        caja_amortizacion = precio_neto - costo_directo_recurrente_local
        
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

    # Contenedor: Validación Comercial (Semáforo Oferta)
    st.markdown('<div class="wiltel-container">', unsafe_allow_html=True)
    st.subheader("Validación Comercial")
    if payback_real == 99.0:
        st.error("🔴 ALERTA CRÍTICA: El precio fijado en las escalas no cubre los costos directos mínimos.")
    elif payback_real > pb_obj_local:
        st.error(f"🔴 RECHAZADO: El Payback Real es de {payback_real:.1f} meses. Supera tu objetivo estratégico de {pb_obj_local} meses.")
    else:
        st.success(f"🟢 APROBADO: El Payback Real es de {payback_real:.1f} meses. Cumple con el objetivo de {pb_obj_local} meses.")
        
    st.info(f"📋 **Desglose Técnico Financiero del Kit:** Inversión en Calle: { '$' if moneda == 'Pesos ARS' else 'USD' } {inversion_kit_local:,.2f} | Insumos de Hardware: USD {total_hw_usd:,.2f} | Paquete de Materiales FTTH: USD {subtotal_ftth_usd:,.2f} | Paquete de Materiales Coaxil: USD {subtotal_coaxil_usd:,.2f}")
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 2. PESTAÑA: ADMINISTRACIÓN COMERCIAL
# ==============================================================================
elif opcion_menu == "🏢 Administración Comercial":
    st.title("Administración Comercial")
    
    st.markdown('<div class="wiltel-container">', unsafe_allow_html=True)
    st.subheader("Parámetros Estratégicos de Control Financiero")
    col_pcom1, col_pcom2, col_pcom3 = st.columns(3)
    with col_pcom1:
        st.session_state.comercial_params["tc"] = st.number_input("Tipo de Cambio Oficial (ARS/USD)", value=st.session_state.comercial_params["tc"], step=10.0)
    with col_pcom2:
        st.session_state.comercial_params["pb_objetivo"] = st.number_input("Payback Máximo Objetivo (Meses)", value=st.session_state.comercial_params["pb_objetivo"], min_value=1)
    with col_pcom3:
        st.session_state.comercial_params["costo_fact"] = st.number_input("Costo de Facturación y Carga Impositiva (%)", value=st.session_state.comercial_params["costo_fact"], step=0.5)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="wiltel-container">', unsafe_allow_html=True)
    st.subheader("Gestor de Cartera de Productos (Opciones de Cajas Desplegables)")
    st.write("Agregá, eliminá o renombrá productos. Los cambios impactarán automáticamente en el simulador.")
    
    col_g1, col_g2, col_g3 = st.columns(3)
    with col_g1:
        txt_internet = st.text_area("Opciones de Caja 1: Internet (Separadas por comas)", value=", ".join(st.session_state.db_internet))
        st.session_state.db_internet = [x.strip() for x in txt_internet.split(",") if x.strip()]
    with col_g2:
        txt_tv = st.text_area("Opciones de Caja 2: TV (Separadas por comas)", value=", ".join(st.session_state.db_tv))
        st.session_state.db_tv = [x.strip() for x in txt_tv.split(",") if x.strip()]
    with col_g3:
        txt_tel = st.text_area("Opciones de Caja 3: Telefonía (Separadas por comas)", value=", ".join(st.session_state.db_telefonia))
        st.session_state.db_telefonia = [x.strip() for x in txt_tel.split(",") if x.strip()]
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 3. PESTAÑA: ADMINISTRACIÓN DE COSTOS
# ==============================================================================
elif opcion_menu == "💲 Administración de Costos":
    st.title("Administración de Costos")
    st.caption("⚠️ Todos los valores ingresados en esta sección deben expresarse en **USD sin IVA**.")
    
    st.markdown('<div class="wiltel-container">', unsafe_allow_html=True)
    st.subheader("Sección 1: Costos de Materiales, Equipos y Mano de Obra")
    
    st.session_state.costo_mo = st.number_input("Mano de Obra General de Instalación (USD)", value=st.session_state.costo_mo, step=1.0)
    
    col_edit1, col_edit2 = st.columns(2)
    with col_edit1:
        st.markdown("#### Paquete de Materiales FTTH")
        df_f = pd.DataFrame(st.session_state.mat_ftth)
        df_f_edit = st.data_editor(df_f, num_rows="dynamic", key="ed_ftth_final")
        st.session_state.mat_ftth = df_f_edit.to_dict('records')
    with col_edit2:
        st.markdown("#### Paquete de Materiales Coaxil")
        df_c = pd.DataFrame(st.session_state.mat_coaxil)
        df_c_edit = st.data_editor(df_c, num_rows="dynamic", key="ed_coaxil_final")
        st.session_state.mat_coaxil = df_c_edit.to_dict('records')
        
    st.markdown("#### Matriz Maestra de Costos de Equipos (Comodatos)")
    df_eq = pd.DataFrame(st.session_state.db_equipos)
    df_eq_edit = st.data_editor(df_eq, num_rows="dynamic", key="ed_eq_final")
    st.session_state.db_equipos = df_eq_edit.to_dict('records')
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="wiltel-container">', unsafe_allow_html=True)
    st.subheader("Sección 2: Costos Directos Recurrentes")
    st.write("Detalle de costos fijos de insumos por servicios provistos mensualmente.")
    df_cd = pd.DataFrame(st.session_state.db_costos_directos)
    df_cd_edit = st.data_editor(df_cd, num_rows="dynamic", key="ed_cd_final")
    st.session_state.db_costos_directos = df_cd_edit.to_dict('records')
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 4. PESTAÑA: ADMINISTRACIÓN TÉCNICA
# ==============================================================================
elif opcion_menu == "🛠️ Administración Técnica":
    st.title("Administración Técnica")
    
    st.markdown('<div class="wiltel-container">', unsafe_allow_html=True)
    st.subheader("Reglas Lógicas de Negocio para el Armado Automatizado de Kits")
    st.info("💡 Las siguientes reglas técnicas se encuentran programadas de forma nativa en el motor de cálculo y mapean las dependencias complejas cruzadas:")
    
    st.markdown("""
    * **REGLA INTERNET MESH:** Si el Combo incluye `WILTEL 150 MB MESH`, el sistema asigna automáticamente la **ONT F601 + 2 unidades de Tenda NOVA MX3**. Además, bloquea por seguridad que el comercial sume un adicional Mesh redundante.
    * **REGLA ONT TV HD:** Si el Combo incorpora cualquier opción de TV por cable (`WILTEL TV HD`, `FULL TV HD` o `PLAYME TV HD`), el sistema descarta la ONT básica e incluye de forma automatizada la **ONT GPON ZXHN F6600R** de alta gama.
    * **REGLA DECO STB HD:** El decodificador **STB mod HC-C730** se añade de manera exclusiva al kit técnico si se selecciona el producto físico **FULL TV HD** o **PLAYME FULL BOX**.
    * **REGLA PAQUETES DE MATERIALES:** La bolsa **FTTH (Fibra)** se carga por defecto en el 100% de las ventas. La bolsa **Coaxil (USD 15.20)** se activa de forma inteligente únicamente si el combo contiene productos de TV cableada.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="wiltel-container">', unsafe_allow_html=True)
    st.subheader("Mapeo de Costos Directos Asociados")
    st.write("Las reglas lógicas vinculan los adicionales tildados por el comercial con la matriz de costos directos recurrentes y aplican los márgenes comerciales fijados:")
    st.markdown("""
    1. **Adicional WILTEL ON:** Activa en el abono mensual el impacto del *Chip de datos WILTEL ON 1GB* más su margen.
    2. **Adicional PAQUETE FÚTBOL:** Sincroniza el costo de la señal proveedora directamente en la simulación del flujo mes a mes.
    3. **Adicional PAQUETE TV PREMIUM:** Imputa el costo unitario de las señales premium y recalcula la viabilidad del semáforo.
    """)
    st.caption("⚙️ En la próxima fase de base de datos relacional, podrás linkear nuevas reglas mediante un constructor visual de condiciones.")
    st.markdown('</div>', unsafe_allow_html=True)