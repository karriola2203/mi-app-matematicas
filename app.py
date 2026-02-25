import streamlit as st
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
tab1, tab2 = st.tabs(["📐 Visualizador de Curvas", "✍️ Desafío de Derivadas"])

with tab1:
    st.header("Análisis de Pendientes e Inclinación")
    st.write("Ingresa una función para analizar la pendiente de la recta tangente.")
    
    user_f_text = st.text_input("Escribe tu función (ejemplo: x*2 o sin(x)):", "x*2", key="input_viz")
    
    try:
        x_s = sp.symbols('x')
        f_s = sp.sympify(user_f_text.replace("^", "**"))
        df_s = sp.diff(f_s, x_s)
        
        # Mostrar fórmulas
        st.latex(f"f(x) = {sp.latex(f_s)}")
        st.latex(f"f'(x) = {sp.latex(df_s)}")
        
        # Slider para mover el punto
        val_x = st.slider("Mueve el punto para ver la pendiente m en la curva:", -5.0, 5.0, 0.0)
        
        # Cálculos numéricos
        f_n = sp.lambdify(x_s, f_s, 'numpy')
        df_n = sp.lambdify(x_s, df_s, 'numpy')
        
        xs = np.linspace(-5, 5, 250)
        ys = f_n(xs)
        y0 = float(f_n(val_x))
        m = float(df_n(val_x))
        
        # Recta tangente
        tangente = m * (xs - val_x) + y0

        # Gráfico con Plotly
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=xs, y=ys, name="Estructura (f(x))", line=dict(color='blue', width=3)))
        fig.add_trace(go.Scatter(x=xs, y=tangente, name=f"Tangente (m={m:.2f})", line=dict(color='red', dash='dash')))
        fig.add_trace(go.Scatter(x=[val_x], y=[y0], mode='markers', marker=dict(size=12, color='black'), name="Punto de análisis"))
        
        fig.update_layout(
            xaxis_title="Eje X",
            yaxis_title="Eje Y",
            hovermode="x unified",
            yaxis=dict(range=[min(ys)-2, max(ys)+2])
        )
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error("Error: Asegúrate de usar '' para multiplicar. Ejemplo: 3*x*2")

with tab2:
    st.header("¡Pon a prueba tu precisión!")
    st.latex(f"f(x) = {sp.latex(st.session_state.ejercicio)}")
    
    rta = st.text_input("Tu respuesta para f'(x):", key="input_quiz")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Validar Cálculo"):
            try:
                user_sol = sp.sympify(rta.replace("^", "**"))
                if sp.simplify(user_sol - st.session_state.solucion) == 0:
                    st.success("¡Excelente! Respuesta correcta.")
                    st.balloons()
                else:
                    st.error(f"La respuesta correcta era: {st.session_state.solucion}")
            except:
                st.warning("Usa formato matemático (ej. 2*x)")
    with col2:
        if st.button("Nuevo Reto ➡️"):
            st.session_state.ejercicio, st.session_state.solucion = generar_ejercicio()
            st.rerun()
