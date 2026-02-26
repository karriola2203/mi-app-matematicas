import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

# Configuración de página para Blackboard
st.set_page_config(page_title="Taller UPC: Geometría de la Derivada", layout="wide")

st.title("🏛️ Taller Interactivo: Análisis de la Recta Tangente")
st.caption("Docente: Karina Arriola | Facultad de Arquitectura UPC")

# --- BARRA LATERAL: EDITOR CON VISTA PREVIA LATEX ---
with st.sidebar:
    st.header("✍️ Configuración del Ejercicio")
    u_input = st.text_input("1. Define tu función f(x):", value="x^2 - 4")
    ux0 = st.number_input("2. Punto de tangencia (x0):", value=2.0)
    
    # Procesamiento y Vista Previa
    x = sp.symbols('x')
    try:
        f_expr = sp.sympify(u_input.replace("^", "**"))
        st.markdown("---")
        st.write("**Vista Previa Matemática:**")
        st.latex(sp.latex(f_expr))
    except:
        st.error("Error en la escritura. Revisa los símbolos.")
        st.stop()
    
    st.markdown("---")
    ver_ayuda = st.checkbox("🆘 Ver ayuda/procedimiento")

# --- LÓGICA DE CÁLCULO (INTERNA) ---
df_expr = sp.diff(f_expr, x)
y0_val = float(f_expr.subs(x, ux0))
m_val = float(df_expr.subs(x, ux0))
b_val = y0_val - (m_val * ux0)

# --- CUERPO PRINCIPAL: INTERACCIÓN ---
col_taller, col_viz = st.columns([1.2, 1.8])

with col_taller:
    st.subheader("📝 Tu Desafío")
    st.write(f"Para la función en $x_0 = {ux0}$, encuentra la ecuación $y = mx + b$.")
    
    # PASO 1: Pendiente
    st.markdown("---")
    st.write("**Paso 1: Calcula la pendiente ($m$)**")
    user_m = st.number_input("Ingresa el valor de m:", format="%.2f", key="m_input")
    
    if ver_ayuda:
        st.info(f"Ayuda: Deriva la función e intenta sustituir $x$ por ${ux0}$.")
        st.latex(f"f'(x) = {sp.latex(df_expr)}")
    
    # PASO 2: Ordenada b
    st.markdown("---")
    st.write("**Paso 2: Calcula la ordenada al origen ($b$)**")
    st.caption("Fórmula: $b = y_0 - (m \cdot x_0)$")
    user_b = st.number_input("Ingresa el valor de b:", format="%.2f", key="b_input")

    if ver_ayuda:
        st.info(f"Punto de tangencia: $P({ux0}, {y0_val:.2f})$")
        st.latex(f"b = {y0_val:.2f} - ({m_val:.2f} \cdot {ux0})")

    # VALIDACIÓN
    if st.button("🚀 Validar mi Recta Tangente"):
        error_m = abs(user_m - m_val)
        error_b = abs(user_b - b_val)
        
        if error_m < 0.02 and error_b < 0.02:
            st.success("¡Excelente! Has encontrado la recta exacta.")
            st.balloons()
        else:
            if error_m >= 0.02: st.error(f"La pendiente 'm' no es correcta.")
            if error_b >= 0.02: st.error(f"La ordenada 'b' no es correcta.")
            st.warning("Revisa tus cálculos o activa el botón de 'Ver Ayuda'.")

with col_viz:
    # Mostramos los cortes de la TANGENTE
    st.subheader("📍 Análisis de Cortes (Recta)")
    
    # Corte Y: (0, b) | Corte X: (-b/m, 0)
    c_y = b_val
    c_x = -b_val / m_val if m_val != 0 else 0
    
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Corte Eje Y", f"(0, {c_y:.2f})")
    with c2:
        st.metric("Corte Eje X", f"({c_x:.2f}, 0)" if m_val != 0 else "N/A")

    # GRÁFICA INTERACTIVA
    f_n = sp.lambdify(x, f_expr, 'numpy')
    x_p = np.linspace(ux0 - 5, ux0 + 5, 400)
    y_f = f_n(x_p)
    y_t = m_val * x_p + b_val

    fig = go.Figure()
    # Ejes
    fig.add_hline(y=0, line_color="black")
    fig.add_vline(x=0, line_color="black")
    # Curvas
    fig.add_trace(go.Scatter(x=x_p, y=y_f, name="Función f(x)", line=dict(color='#003366', width=3)))
    fig.add_trace(go.Scatter(x=x_p, y=y_t, name="Recta Tangente", line=dict(color='#FF4B4B', dash='dash')))
    # Cortes
    fig.add_trace(go.Scatter(x=[0, c_x], y=[c_y, 0], mode='markers', 
                             marker=dict(color='green', size=12, symbol='x'), name="Cortes Tangente"))
    
    fig.update_layout(height=450, plot_bgcolor='white', title="Visualización Geométrica")
    st.plotly_chart(fig, use_container_width=True)

# --- REPORTE PARA BLACKBOARD ---
st.markdown("---")
if st.checkbox("Generar Reporte para Foro"):
    st.subheader("📋 Datos para tu participación")
    reporte = f"""ANÁLISIS GEOMÉTRICO UPC
Función: f(x) = {u_input} en x0 = {ux0}
----------------------------------------
Ecuación Tangente: y = {m_val:.2f}x {'+' if b_val>=0 else ''} {b_val:.2f}
Corte Y: (0, {c_y:.2f})
Corte X: ({c_x:.2f}, 0)
----------------------------------------
"""
    st.text_area("Copia y pega esto en Blackboard:", reporte, height=150)
