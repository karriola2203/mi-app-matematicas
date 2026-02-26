import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

# Configuración profesional para Blackboard UPC
st.set_page_config(page_title="Taller UPC: Desafío Geométrico", layout="wide")

st.title("🏛️ Taller Interactivo: Construcción de la Recta Tangente")
st.caption("Docente: Karina Arriola | Facultad de Arquitectura UPC")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("✍️ Editor de Función")
    u_f = st.text_input("Define f(x):", "x**2 - 4")
    ux0 = st.number_input("Punto de análisis x0:", value=2.0)
    
    x_s = sp.symbols('x')
    try:
        # Limpiamos la entrada para evitar errores de sintaxis
        f_limpio = u_f.replace("^", "**")
        f_s = sp.sympify(f_limpio)
        st.markdown("---")
        st.write("**Vista Previa LaTeX:**")
        st.latex(sp.latex(f_s))
    except:
        st.error("Error en la función. Usa '*' para multiplicar y '**' para potencia.")
        st.stop()
    
    ayuda = st.toggle("Activar modo Tutor (Pistas)")

# --- LÓGICA DE CÁLCULO ---
# Usamos float() explícito para evitar problemas de tipos de Sympy
y0_val = float(f_s.subs(x_s, ux0))
df_s = sp.diff(f_s, x_s)
m_val = float(df_s.subs(x_s, ux0))
b_val = float(y0_val - (m_val * ux0))

# --- FLUJO POR PASOS ---
col1, col2 = st.columns([1, 1.5])

with col1:
    st.info("🎯 **Misión:** Reemplaza los datos en $y = mx + b$ para hallar la recta.")
    
    # PASO 1
    with st.container(border=True):
        st.markdown("**1. Hallar el Punto de Tangencia**")
        u_y0 = st.number_input(f"Calcula y0 = f({ux0}):", value=0.0, format="%.2f")
        check1 = abs(u_y0 - y0_val) < 0.1
        if check1: st.success("¡Punto Correcto! ✅")

    # PASO 2
    if check1:
        with st.container(border=True):
            st.markdown("**2. Hallar la Pendiente (m)**")
            u_m = st.number_input("Calcula m = f'(x0):", value=0.0, format="%.2f")
            check2 = abs(u_m - m_val) < 0.1
            if check2: st.success("¡Pendiente Correcta! ✅")
    else:
        st.lock_button("Paso 2 bloqueado", icon="🔒")

    # PASO 3: REEMPLAZO EN Y = MX + B
    if 'check2' in locals() and check2:
        with st.container(border=True):
            st.markdown("**3. Hallar el valor de b**")
            st.write("Sustituye en la ecuación:")
            st.latex(f"{y0_val:.2f} = ({m_val:.2f})({ux0}) + b")
            u_b = st.number_input("Despeja e ingresa b:", value=0.0, format="%.2f")
            check3 = abs(u_b - b_val) < 0.1
            if check3: st.success("¡Valor de b Correcto! ✅")
    else:
        st.lock_button("Paso 3 bloqueado", icon="🔒")

    # PASO 4: ECUACIÓN FINAL
    desbloqueo = False
    if 'check3' in locals() and check3:
        with st.container(border=True):
            st.markdown("**4. Ecuación de la Recta**")
            u_eq = st.text_input("Escribe la ecuación completa:", placeholder="ej: y = 4x - 8")
            if u_eq:
                # Verificación flexible de la ecuación
                if str(round(m_val,1)) in u_eq and str(round(abs(b_val),1)) in u_eq:
                    st.success("¡Ecuación Validada! 🚀")
                    desbloqueo = True
    else:
        st.lock_button("Paso 4 bloqueado", icon="🔒")

# --- GRÁFICA Y CORTES ---
with col2:
    if desbloqueo:
        st.subheader("📊 Análisis Geométrico Final")
        cx = -b_val / m_val if m_val != 0 else 0
        cy = b_val
        st.write(f"**Cortes con los ejes:** X: ({cx:.2f}, 0) | Y: (0, {cy:.2f})")

        # Gráfica
        f_n = sp.lambdify(x_s, f_s, 'numpy')
        xp = np.linspace(ux0-5, ux0+5, 400)
        yp = f_n(xp)
        yt = m_val * xp + b_val

        fig = go.Figure()
        fig.add_hline(y=0, line_color="black")
        fig.add_vline(x=0, line_color="black")
        fig.add_trace(go.Scatter(x=xp, y=yp, name="f(x)", line=dict(color='#003366', width=4)))
        fig.add_trace(go.Scatter(x=xp, y=yt, name="Tangente", line=dict(color='red', dash='dash')))
        fig.add_trace(go.Scatter(x=[ux0, 0, cx], y=[y0_val, cy, 0], mode='markers', marker=dict(color='orange', size=12), name="Puntos Clave"))
        
        fig.update_layout(plot_bgcolor='white', height=500)
        st.plotly_chart(fig, use_container_width=True)
        st.balloons()
    else:
        st.warning("⚠️ Completa los pasos para ver la gráfica.")
