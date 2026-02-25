[11:47 a.m., 25/2/2026] Karina: import streamlit as st
import sympy as sp
import random
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Arquitectura y Cálculo - Profe Karina", layout="wide")

# --- ENCABEZADO ---
st.title("🏛️ Cálculo para la Arquitectura")
st.subheader("Facultad de Arquitectura | Profe: Karina Arriola")

# --- LÓGICA DEL QUIZ ---
def generar_ejercicio():
    x = sp.symbols('x')
    n = random.randint(2, 4)
    a = random.randint(1, 8)
    funciones = [a * x*n, a * sp.cos(x), x*n + a*x, sp.sin(a*x)]
    f = random.choice(funciones)
    df = sp.diff(f, x)
    return f, df

if 'ejercicio' not in st.session_state:
    st.session_state.ejercicio, st.session_state.solucion = generar_ejercicio()

# --- PESTAÑAS ---
tab1, tab2 = st.tabs(["📐 V…
[11:55 a.m., 25/2/2026] Karina: import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Cálculo Arquitectónico - Profe Karina", layout="wide")

st.title("🏛️ Laboratorio de Rectas Tangentes")
st.subheader("Facultad de Arquitectura | Profe: Karina Arriola")

# --- ENTRADA DE DATOS ---
col_in1, col_in2 = st.columns([2, 1])

with col_in1:
    user_f = st.text_input("1. Define la forma de la estructura f(x):", "x**2 - 2*x")

with col_in2:
    # Entrada para el valor exacto de x
    x0_val = st.number_input("2. Valor de abscisa (x0):", value=1.0, step=0.1)

try:
    # Lógica Matemática
    x = sp.symbols('x')
    f_sym = sp.sympify(user_f.replace("^", "**"))
    df_sym = sp.diff(f_sym, x)
    
    # Cálculos en el punto x0
    y0_val = float(f_sym.subs(x, x0_val))
    m_val = float(df_sym.subs(x, x0_val))
    
    # Ecuación de la recta tangente simplificada: y = mx + b -> b = y0 - m*x0
    b_val = y0_val - (m_val * x0_val)
    
    # --- MOSTRAR PASO A PASO ---
    st.markdown("---")
    st.write("### 📝 Desarrollo Matemático")
    
    col_step1, col_step2, col_step3 = st.columns(3)
    
    with col_step1:
        st.info("*Paso 1: Punto de Tangencia*")
        st.latex(f"f({x0_val}) = {y0_val:.2f}")
        st.write(f"Punto: $P({x0_val}, {y0_val:.2f})$")

    with col_step2:
        st.info("*Paso 2: Pendiente (Derivada)*")
        st.latex(f"f'(x) = {sp.latex(df_sym)}")
        st.latex(f"m = f'({x0_val}) = {m_val:.2f}")

    with col_step3:
        st.info("*Paso 3: Ecuación de la Recta*")
        st.latex(f"y - y_0 = m(x - x_0)")
        st.latex(f"y - {y0_val:.2f} = {m_val:.2f}(x - {x0_val})")
        # Mostrar forma simplificada
        signo = "+" if b_val >= 0 else "-"
        st.latex(f"y = {m_val:.2f}x {signo} {abs(b_val):.2f}")

    # --- GRÁFICA INTERACTIVA ---
    f_num = sp.lambdify(x, f_sym, 'numpy')
    
    # Rango de la gráfica centrado en x0
    x_range = np.linspace(x0_val - 5, x0_val + 5, 400)
    y_range = f_num(x_range)
    y_tangente = m_val * (x_range - x0_val) + y0_val

    fig = go.Figure()
    # Curva original
    fig.add_trace(go.Scatter(x=x_range, y=y_range, name="Estructura f(x)", line=dict(color='#1f77b4', width=3)))
    # Recta tangente
    fig.add_trace(go.Scatter(x=x_range, y=y_tangente, name="Recta Tangente", line=dict(color='#d62728', dash='dash')))
    # Punto de tangencia
    fig.add_trace(go.Scatter(x=[x0_val], y=[y0_val], mode='markers', marker=dict(size=12, color='black'), name="Punto P"))

    fig.update_layout(
        title=f"Visualización en x = {x0_val}",
        xaxis_title="Eje X (Metros/Unidades)",
        yaxis_title="Eje Y (Altura)",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error("Hubo un error en la expresión. Revisa que esté bien escrita.")
