import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

# Configuración profesional para Blackboard UPC
st.set_page_config(page_title="Taller UPC: Desafío Geométrico", layout="wide")

st.title("🏛️ Taller Interactivo: Construcción de la Recta Tangente")
st.caption("Docente: Karina Arriola | Facultad de Arquitectura UPC")

# --- BARRA LATERAL (ENTRADA Y PREVIEW) ---
with st.sidebar:
    st.header("✍️ Editor de Función")
    u_f = st.text_input("Define f(x):", "x**2 - 4")
    ux0 = st.number_input("Punto de análisis x0:", value=2.0)
    
    x_s = sp.symbols('x')
    try:
        f_s = sp.sympify(u_f.replace("^", "**"))
        st.markdown("---")
        st.write("**Vista Previa Matemática (LaTeX):**")
        st.latex(sp.latex(f_s))
    except:
        st.error("Error en la función")
        st.stop()
    
    st.markdown("---")
    ayuda = st.toggle("Activar modo Tutor (Pistas)")

# --- LÓGICA DE CÁLCULO INTERNO ---
y0_val = float(f_s.subs(x_s, ux0))
df_s = sp.diff(f_s, x_s)
m_val = float(df_s.subs(x_s, ux0))
b_val = y0_val - (m_val * ux0)

# --- FLUJO INTERACTIVO POR PASOS ---
col1, col2 = st.columns([1, 1.5])

with col1:
    st.info("🎯 **Misión:** Reemplaza los datos en $y = mx + b$ para hallar la recta.")
    
    # PASO 1: PUNTO Y0
    with st.container(border=True):
        st.markdown("**1. Hallar el Punto de Tangencia**")
        u_y0 = st.number_input(f"Calcula $y_0$ evaluando $f({ux0})$:", format="%.2f", key="y0_user")
        check1 = abs(u_y0 - y0_val) < 0.05
        if check1: 
            st.success(f"Punto Hallado: $P({ux0}, {y0_val:.2f})$ ✅")
        elif ayuda: 
            st.caption("Pista: Sustituye el valor de x en la función original.")

    # PASO 2: PENDIENTE M
    if check1:
        with st.container(border=True):
            st.markdown("**2. Hallar la Pendiente (m)**")
            u_m = st.number_input("Calcula $m = f'(x_0)$:", format="%.2f", key="m_user")
            check2 = abs(u_m - m_val) < 0.05
            if check2: 
                st.success(f"Pendiente Hallada: $m = {m_val:.2f}$ ✅")
            elif ayuda: 
                st.latex(f"f'(x) = {sp.latex(df_s)}")
                st.caption("Deriva y reemplaza x por el valor de x0.")
    else:
        st.lock_button("Paso 2 bloqueado", icon="🔒")

    # PASO 3: HALLAR B POR REEMPLAZO EN Y=MX+B
    if 'check2' in locals() and check2:
        with st.container(border=True):
            st.markdown("**3. Hallar el valor de b**")
            st.write("Sustituye los valores conocidos en $y = mx + b$:")
            st.latex(f"{y0_val:.2f} = ({m_val:.2f})({ux0}) + b")
            
            u_b = st.number_input("Despeja e ingresa el valor de b:", format="%.2f", key="b_user")
            check3 = abs(u_b - b_val) < 0.05
            if check3: 
                st.success(f"Valor Hallado: $b = {b_val:.2f}$ ✅")
            elif ayuda:
                st.info(f"Despeje: $b = {y0_val:.2f} - ({m_val*ux0:.2f})$")
    else:
        st.lock_button("Paso 3 bloqueado", icon="🔒")

   # --- PASO 4: ECUACIÓN FINAL (CORRECCIÓN DE ERROR) ---
if 'check3' in locals() and check3:
    with st.container(border=True):
        st.markdown("**4. Ecuación de la Recta**")
        u_eq = st.text_input("Escribe la ecuación completa:", placeholder="ej: y = 4x - 8")
        
        # Inicializamos desbloqueo para evitar el AttributeError
        desbloqueo = False 
        
        if u_eq:
            # Convertimos a string para evitar errores de tipo
            m_str = str(round(m_val, 1))
            b_abs_str = str(round(abs(b_val), 1))
            
            if m_str in u_eq and b_abs_str in u_eq:
                st.success("¡Ecuación Correcta! 🚀")
                desbloqueo = True
            else:
                st.error("Los valores no coinciden con tus pasos anteriores.")
else:
    desbloqueo = False

# --- RESULTADO Y GRÁFICA (CON PROTECCIÓN DE ATRIBUTOS) ---
with col2:
    # Verificamos que 'desbloqueo' sea True y que las variables existan
    if 'desbloqueo' in locals() and desbloqueo:
        try:
            st.subheader("📊 Resultados y Representación")
            
            cx = -b_val / m_val if m_val != 0 else 0
            cy = b_val
            
            st.write("📍 **Cortes de la recta con los ejes:**")
            st.latex(f"Eje \ Y: (0, {cy:.2f}) \quad | \quad Eje \ X: ({cx:.2f}, 0)")

            # Gráfica con manejo de errores
            f_n = sp.lambdify(x_s, f_s, 'numpy')
            xp = np.linspace(ux0-5, ux0+5, 400)
            yp = f_n(xp)
            yt = m_val * xp + b_val

            fig = go.Figure()
            fig.add_hline(y=0, line_color="black")
            fig.add_vline(x=0, line_color="black")
            fig.add_trace(go.Scatter(x=xp, y=yp, name="Curva f(x)"))
            fig.add_trace(go.Scatter(x=xp, y=yt, name="Tangente", line=dict(dash='dash')))
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error al generar la gráfica: {e}")
    else:
        st.warning("⚠️ Completa los pasos de la izquierda.")
-----------------------------------------
Función: {u_f} en x0 = {ux0}
1. Punto de Tangencia: ({ux0}, {y0_val:.2f})
2. Pendiente (m): {m_val:.2f}
3. Ordenada (b): {b_val:.2f}
4. Ecuación Final: y = {m_val:.2f}x + ({b_val:.2f})
5. Cortes: Eje X en ({cx:.2f}, 0) | Eje Y en (0, {cy:.2f})
-----------------------------------------"""
        st.text_area("Copia este desarrollo para el Foro de Blackboard:", reporte, height=180)

    else:
        st.warning("⚠️ Completa los 4 pasos de la izquierda para ver el análisis técnico.")
        st.image("https://via.placeholder.com/800x500.png?text=Completa+el+despeje+de+b+y+la+ecuación", use_container_width=True)
