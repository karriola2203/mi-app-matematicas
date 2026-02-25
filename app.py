import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Cálculo Arquitectónico - Profe Karina", layout="wide")

st.title("🏛️ Laboratorio de Rectas Tangentes")
st.subheader("Facultad de Arquitectura | Profe: Karina Arriola")

# --- ENTRADA DE DATOS ---
col_in1, col_in2 = st.columns([2, 1])

with col_in1:
    user_f = st.text_input("1. Define la función f(x):", "x**2 - 2*x")

with col_in2:
    x0_val = st.number_input("2. Valor de abscisa (x0):", value=1.0, step=0.1)

try:
    # Lógica Matemática
    x = sp.symbols('x')
    # Limpiamos la entrada del usuario
    f_input = user_f.replace("^", "**")
    f_sym = sp.sympify(f_input)
    df_sym = sp.diff(f_sym, x)
    
    # Cálculos en el punto x0
    y0_val = float(f_sym.subs(x, x0_val))
    m_val = float(df_sym.subs(x, x0_val))
    b_val = y0_val - (m_val * x0_val)
    
    st.markdown("---")
    st.write("### 📝 Desarrollo Matemático Paso a Paso")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.info("*Paso 1: Punto de Tangencia*")
        st.latex(f"f({x0_val}) = {y0_val:.2f}")
        st.write(f"Punto: P({x0_val}, {y0_val:.2f})")

    with c2:
        st.info("*Paso 2: Pendiente*")
        st.latex(f"f'(x) = {sp.latex(df_sym)}")
        st.latex(f"m = {m_val:.2f}")

    with c3:
        st.info("*Paso 3: Ecuación*")
        st.latex(f"y - y_0 = m(x - x_0)")
        signo = "+" if b_val >= 0 else "-"
        st.latex(f"y = {m_val:.2f}x {signo} {abs(b_val):.2f}")

    # --- GRÁFICA ---
    f_num = sp.lambdify(x, f_sym, 'numpy')
    x_plot = np.linspace(x0_val - 5, x0_val + 5, 400)
    y_plot = f_num(x_plot)
    y_tan = m_val * (x_plot - x0_val) + y0_val

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_plot, y=y_plot, name="f(x)", line=dict(color='blue', width=3)))
    fig.add_trace(go.Scatter(x=x_plot, y=y_tan, name="Tangente", line=dict(color='red', dash='dash')))
    fig.add_trace(go.Scatter(x=[x0_val], y=[y0_val], mode='markers', marker=dict(size=12, color='black')))

    fig.update_layout(xaxis_title="Eje X", yaxis_title="Eje Y", height=500)
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error("Error en la fórmula. Revisa los paréntesis y usa * para multiplicar.")
