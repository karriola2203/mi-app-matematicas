import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go
import random

st.set_page_config(page_title="Arquitectura: Análisis Geométrico", layout="wide")

# --- FUNCIONES DE APOYO ---
def generar_reto_pro():
    x = sp.symbols('x')
    a = random.randint(2, 4)
    tipo = random.choice(['exp', 'sin', 'cos', 'ln'])
    if tipo == 'exp': f = sp.exp(a * x)
    elif tipo == 'sin': f = sp.sin(x / a)
    elif tipo == 'cos': f = sp.cos(a * x)
    else: f = sp.log(x + 1) if random.random() > 0.5 else x**2 - a
    
    x0 = random.randint(0, 2)
    df = sp.diff(f, x)
    try: m_sol = float(df.subs(x, x0))
    except: m_sol = 0.0
    return f, x0, df, m_sol

if 'aciertos' not in st.session_state:
    st.session_state.update({'aciertos': 0, 'intentos': 0})
if 'reto_f' not in st.session_state:
    f, x0, df, m = generar_reto_pro()
    st.session_state.update({'reto_f': f, 'reto_x0': x0, 'reto_df': df, 'reto_m': m})

st.title("🏛️ Análisis Geométrico Profesional")
st.caption(f"Docente: Karina Arriola | Facultad de Arquitectura")

tab1, tab2 = st.tabs(["📐 Estación de Análisis", "🎮 Quizz de Precisión"])

with tab1:
    col_main, col_side = st.columns([3, 1])
    
    with col_side:
        st.subheader("Editor de Funciones")
        st.write("Copia y pega estos formatos:")
        st.code("exp(5*x)\nsin(x/2)\nlog(x)\nx**2 - 4")
        u_f = st.text_input("Función f(x):", "x**2 - 4")
        ux0 = st.number_input("Punto de tangencia (x0):", value=2.0)

    with col_main:
        try:
            x_s = sp.symbols('x')
            f_s = sp.sympify(u_f.replace("^", "**"))
            df_s = sp.diff(f_s, x_s)
            
            # Puntos de corte
            raices = sp.solve(f_s, x_s)
            corte_y = f_s.subs(x_s, 0)
            
            # Datos del punto de tangencia
            y0 = float(f_s.subs(x_s, ux0))
            m = float(df_s.subs(x_s, ux0))
            
            # Gráfica mejorada
            f_n = sp.lambdify(x_s, f_s, 'numpy')
            xp = np.linspace(float(ux0)-5, float(ux0)+5, 500)
            yp = f_n(xp)
            
            fig = go.Figure()
            # Ejes X e Y resaltados
            fig.add_hline(y=0, line_width=2, line_color="black")
            fig.add_vline(x=0, line_width=2, line_color="black")
            
            # Curva principal
            fig.add_trace(go.Scatter(x=xp, y=yp, name="f(x)", line=dict(color='#003366', width=4)))
            
            # Recta Tangente
            yt = m * (xp - ux0) + y0
            fig.add_trace(go.Scatter(x=xp, y=yt, name="Recta Tangente", line=dict(color='#FF4B4B', dash='dash')))
            
            # Marcadores de Puntos de Corte
            for r in raices:
                if r.is_real:
                    fig.add_trace(go.Scatter(x=[float(r)], y=[0], mode='markers', 
                                           marker=dict(color='green', size=10), name="Raíz"))
            
            fig.add_trace(go.Scatter(x=[ux0], y=[y0], mode='markers', 
                                   marker=dict(color='orange', size=12, symbol='diamond'), name="Punto Tangencia"))

            fig.update_layout(
                xaxis=dict(showgrid=True, gridcolor='LightGray', zeroline=False),
                yaxis=dict(showgrid=True, gridcolor='LightGray', zeroline=False),
                plot_bgcolor='white',
                height=600,
                title=f"Análisis de {u_f}"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.success(f"Ecuación: y = {m:.2f}(x - {ux0}) + {y0:.2f}")
        except:
            st.warning("Escribe una función válida para comenzar el análisis.")

with tab2:
    # (Lógica del Quizz similar a la anterior pero con la estética mejorada)
    st.header("🎮 Evaluación de Pendientes")
    st.latex(f"f(x) = {sp.latex(st.session_state.reto_f)}")
    st.info(f"Calcula la pendiente en x0 = {st.session_state.reto_x0}")
    
    # Campo de respuesta
    user_m = st.number_input("Ingresa el valor de m:", format="%.2f")
    
    if st.button("Validar"):
        st.session_state.intentos += 1
        if abs(user_m - st.session_state.reto_m) < 0.1:
            st.success("¡Excelente precisión!")
            st.session_state.aciertos += 1
            st.balloons()
        else:
            st.error(f"Valor esperado: {st.session_state.reto_m:.2f}")
    
    if st.button("Siguiente Ejercicio"):
        f, x0, df, m = generar_reto_pro()
        st.session_state.update({'reto_f': f, 'reto_x0': x0, 'reto_df': df, 'reto_m': m})
        st.rerun()
