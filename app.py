import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go
import random

st.set_page_config(page_title="Cálculo Arquitectónico - Profe Karina", layout="wide")

# --- LÓGICA DEL RETO (Funciones e^x, sin, cos) ---
def generar_reto_avanzado():
    x = sp.symbols('x')
    a = random.randint(2, 5)
    tipo = random.choice(['exp', 'sin', 'cos', 'poly'])
    
    if tipo == 'exp':
        f = sp.exp(a * x)
    elif tipo == 'sin':
        f = sp.sin(x / a)
    elif tipo == 'cos':
        f = sp.cos(a * x)
    else:
        f = (a-1) * x**2
        
    x0 = random.randint(0, 2)
    df = sp.diff(f, x)
    m_sol = float(df.subs(x, x0))
    return f, x0, df, m_sol

# Inicializar estados
if 'aciertos' not in st.session_state:
    st.session_state.update({'aciertos': 0, 'intentos': 0})
if 'reto_f' not in st.session_state:
    f, x0, df, m = generar_reto_avanzado()
    st.session_state.update({'reto_f': f, 'reto_x0': x0, 'reto_df': df, 'reto_m': m})

st.title("🏛️ Laboratorio de Cálculo - Profe Karina")
st.subheader("Facultad de Arquitectura")

tab1, tab2 = st.tabs(["📐 Visualizador Paso a Paso", "🎮 Reto y Calificación"])

with tab1:
    st.header("Análisis Geométrico")
    c1, c2 = st.columns([2, 1])
    with c1: u_f = st.text_input("Función f(x):", "exp(2*x)", key="v_f")
    with c2: ux0 = st.number_input("Punto x0:", value=0.0, step=0.5, key="v_x")

    try:
        x_s = sp.symbols('x')
        f_s = sp.sympify(u_f.replace("e*", "exp").replace("^", "*"))
        df_s = sp.diff(f_s, x_s)
        y0, m = float(f_s.subs(x_s, ux0)), float(df_s.subs(x_s, ux0))
        b = y0 - (m * ux0)

        st.info(f"*Ecuación de la recta:* y = {m:.2f}x {'+' if b>=0 else '-'} {abs(b):.2f}")
        
        f_n = sp.lambdify(x_s, f_s, 'numpy')
        xp = np.linspace(ux0-3, ux0+3, 400)
        yp = f_n(xp)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=xp, y=yp, name="Estructura"))
        fig.add_trace(go.Scatter(x=xp, y=m*(xp-ux0)+y0, name="Tangente", line=dict(dash='dash', color='red')))
        st.plotly_chart(fig, use_container_width=True)
    except: st.error("Usa exp(x) para e^x.")

with tab2:
    st.header("🎮 Desafío de Rendimiento")
    st.sidebar.metric("Aciertos", st.session_state.aciertos)
    st.sidebar.metric("Intentos", st.session_state.intentos)
    
    st.write("Calcula la pendiente para esta función de diseño:")
    st.latex(f"f(x) = {sp.latex(st.session_state.reto_f)}")
    st.write(f"En el punto: *x0 = {st.session_state.reto_x0}*")

    ans_df = st.text_input("1. Derivada f'(x):")
    ans_m = st.number_input("2. Valor de la pendiente m:", step=0.01)

    if st.button("Enviar Respuesta"):
        st.session_state.intentos += 1
        try:
            user_df = sp.sympify(ans_df.replace("^", "**"))
            es_df_ok = sp.simplify(user_df - st.session_state.reto_df) == 0
            es_m_ok = abs(ans_m - st.session_state.reto_m) < 0.1
            
            if es_df_ok and es_m_ok:
                st.success("¡Excelente! Cálculo exacto.")
                st.session_state.aciertos += 1
                st.balloons()
            else:
                st.error(f"Incorrecto. f'(x) = {st.session_state.reto_df} y m = {st.session_state.reto_m:.2f}")
        except: st.warning("Error de formato.")

    if st.button("Siguiente Reto ➡️"):
        f, x0, df, m = generar_reto_avanzado()
        st.session_state.update({'reto_f': f, 'reto_x0': x0, 'reto_df': df, 'reto_m': m})
        st.rerun()
