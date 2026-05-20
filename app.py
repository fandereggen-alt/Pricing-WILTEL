import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE PÁGINA E IDENTIDAD CORPORATIVA WILTEL
st.set_page_config(page_title="Pricing Wiltel", layout="wide", initial_sidebar_state="expanded")

# Inyección de estilos CSS para lograr el formato de Tablero Corporativo Wiltel
st.markdown("""
    <style>
    .main { background-color: #f4f6f9; }
    [data-testid="stSidebar"] { background-color: #003366; }
    [data-testid="stSidebar"] .stMarkdown p { color: white; font-weight: bold; }
    h1, h2, h3, h4 { color: #003366; font-family: 'Arial', sans-serif; }
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

# Parámetros Comerciales Iniciales
if 'comercial_params' not in st.session_state:
    st.session_state.comercial_params = {
        "tc": 1420.0,
        "pb_objetivo": 6,
        "costo_fact": 8.0
    }

# Carteras de Productos (Modificables dinámicamente en Pestaña 2: Administración Comercial)
if 'db_internet' not in st.session_state:
    st.session_state.db_internet = ["Ninguno", "WILTEL 25 MB", "WILTEL 50 MB", "WILTEL 150 MB", "WILTEL 300 MB"]

if 'db_tv' not in st.session_state:
    st.session_state.db_tv = ["Ninguno", "WILTEL TV HD", "FULL TV HD", "PLAYME TV HD", "PLAYME FULL BOX"]

if 'db_telefonia' not in st.session_state:
    st.session_state.db_telefonia = ["Ninguno", "Línea Hogar Básica"]

# Administración de Costos (USD sin IVA) - Pestaña 4
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
    st.markdown("## 🌐 MENÚ PRINCIPAL")
    opcion_menu = st.radio(
        "Seleccione Entorno:",
        [
            "1- Tablero de Simulación Comercial",
            "2- Administración Comercial",
            "3- Administración Técnica",
            "4- Administración de Costos"
        ]
    )
    st.sidebar.markdown("---")
    st.sidebar.caption("Wiltel Comunicaciones S.A. | CPQ Engine 2026")

# ==============================================================================
# 1- PESTAÑA: TABLERO DE SIMULACIÓN COMERCIAL
# ==============================================================================
if opcion_menu == "1- Tablero de Simulación Comercial":
    st.title("Pricing Wiltel")
    
    # Contenedor 1: Configuración Comercial
    st.markdown('<div class="wiltel-container">', unsafe_allow_html=True)
    st.subheader("Configuración Comercial")
    col_cc1, col_cc2, col_cc3 = st.columns(3)
    with col_cc1:
        segmento = st.selectbox("Segmento de Cliente", ["Consumidor Final (Con IVA)", "Corporativo (Neto sin IVA)"])
    with col_cc2:
        moneda = st.selectbox("Moneda de Cotización", ["Pesos ARS", "Dólares USD"])
    with col_cc3:
        st.info("📢 Precios finales expresados en $ con IVA incluido para Consumidor Final, y en la moneda elegida sin IVA para Corporativo.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Contenedor 2: Combo
    st.markdown('<div class="wiltel-container">', unsafe_allow_html=True)
    st.subheader("Combo")
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        prod_internet = st.selectbox("Caja 1: Internet", st.session_state.db_internet)
    with col_p2:
        prod_tv = st.selectbox("Caja 2: TV", st.session_state.db_tv)
    with col_p3:
        prod_tel = st.selectbox("Caja 3: Telefonía", st.session_state.db_telefonia)
    
    st.markdown("**Caja