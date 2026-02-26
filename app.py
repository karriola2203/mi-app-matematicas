import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

# Configuración profesional para Blackboard UPC
st.set_page_config(page_title="Taller UPC: Recta Tangente", layout="wide")

st.title("🏛️ Taller Interactivo: Construcción de la Recta Tangente")
st.caption("Docente: Karina Arriola | Facultad de Arquitectura UPC")

# --- BARRA LATERAL CON LEYENDA ---
with st.sidebar:
    st.header("⌨️ Guía de Escritura")
    st.info("""
    Para escribir tu función usa:
    * **Producto:** `2*x`
    * **División:** `1/x`
    * **Potencia:** `x^2` o `x**2`
    """)
    
    u_f = st.text_input("Define f(x):", "x^2 - 4")
    ux0 = st.number_input("Punto de abscisa (x0):", value=2.0)
    
    x_s = sp.symbols('x')
    try:
        f_limpio = u_f.replace("^", "**")
        f_s = sp.sympify(f_limpio)
        st.markdown("---")
        st.write("**Vista Previa Matemática:**")
        st.latex(sp.latex(f_s))
    except:
        st.error("Error en la función. Revisa la Guía de Escritura.")
        st.stop()

# --- LÓGICA DE CÁLCULO (CON REDONDEO SEGURO) ---
y0_val = round(float(f_s.subs(x_s, ux0)), 2)
df_s = sp.diff(f_s, x_s)
m_val = round(float(df_s.subs(x_s, ux0)), 2)
b_val = round(float(y0_val - (m_val * ux0)), 2)

# --- ENUNCIADO ---
st.markdown(f"""
> **Enunciado:** Determine la ecuación de la recta tangente a la gráfica de la función 
> $f(x) = {sp.latex(f_s)}$ en el punto de abscisa $x_0 = {ux0}$.
""")

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("📝 Resolución Paso a Paso")
    
    # PASO 1: ORDENADA Y0
    with st.container(border=True):
        st.write("**Paso 1: Punto de Tangencia**")
        # Quitamos el valor predeterminado 0.0 para que no interfiera
        u_y0 = st.number_input(f"Halla $y_0 = f({ux0})$:", key="y0_u", step=1.0, format="%f")
        
        # Validación con tolerancia (abs < 0.01 permite 0 exacto)
        if abs(u_y0 - y0_val) < 0.01:
            st.success("¡Correcto! ✅")
            check1 = True
        else:
            st.error("Incorrecto ❌")
            st.info(f"**Retro:** Sustituye $x = {ux0}$ en $f(x)$. Resultado esperado: {int(y0_val) if y0_val.is_integer() else y0_val}")
            check1 = False

    # PASO 2: PENDIENTE M
    if check1:
        with st.container(border=True):
            st.write("**Paso 2: Pendiente (m)**")
            u_m = st.number_input(f"Halla $m = f'({ux0})$:", key="m_u", step=1.0, format="%f")
            if abs(u_m - m_val) < 0.01:
                st.success("¡Correcto! ✅")
                check2 = True
            else:
                st.error("Incorrecto ❌")
                st.info(f"**Retro:** Evalúa la derivada $f'(x) = {sp.latex(df_s)}$ en $x = {ux0}$.")
                check2 = False
    else:
        check2 = False

    # PASO 3: HALLAR B
    if check2:
        with st.container(border=True):
            st.write("**Paso 3: Ordenada al origen (b)**")
            st.write("Sustituye en $y = mx + b$:")
            st.latex(f"{y0_val} = ({m_val})({ux0}) + b")
            u_b = st.number_input("Despeja b:", key="b_u", step=1.0, format="%f")
            if abs(u_b - b_val) < 0.01:
                st.success("¡Correcto! ✅")
                check3 = True
            else:
                st.error("Incorrecto ❌")
                st.info(f"**Retro:** $b = {y0_val} - ({m_val} \cdot {ux0})$")
                check3 = False
    else:
        check3 = False

    # PASO 4: ECUACIÓN FINAL
    desbloqueo = False
    if check3:
        with st.container(border=True):
            st.write("**Paso 4: Ecuación de la Recta**")
            u_eq = st.text_input("Escribe la ecuación (ej. y=4x-8):")
            
            if u_eq:
                # Limpieza de texto para validar (quitamos espacios y pasamos a minúsculas)
                u_eq_clean = u_eq.replace(" ", "").lower()
                # Creamos versiones en texto de los valores para comparar
                m_txt = str(int(m_val)) if m_val.is_integer() else str(round(m_val, 1))
                b_txt = str(int(abs(b_val))) if b_val.is_integer() else str(round(abs(b_val), 1))
                
                if m_txt in u_eq_clean and b_txt in u_eq_clean:
                    st.success("¡Ecuación Validada! 🚀")
                    desbloqueo = True
                else:
                    st.error("Incorrecto ❌")
                    st.info(f"Usa los valores hallados: $y = {m_val}x {'+' if b_val >= 0 else ''} {b_val}$")

# --- GRÁFICA Y CORTES ---
with col2:
    if desbloqueo:
        st.subheader("📊 Gráfica y Cortes")
        cx = -b_val / m_val if m_val != 0 else 0
        cy = b_val
        st.latex(f"Cortes \ con \ ejes: \ X({cx:.2f}, 0) \ ; \ Y(0, {cy:.2f})")

        xp = np.linspace(ux0-5, ux0+5, 400)
        f_n = sp.lambdify(x_s, f_s, 'numpy')
        yp = f_n(xp)
        yt = m_val * xp + b_val

        fig = go.Figure()
        fig.add_hline(y=0, line_color="black")
        fig.add_vline(x=0, line_color="black")
        fig.add_trace(go.Scatter(x=xp, y=yp, name="f(x)", line=dict(color='#003366', width=4)))
        fig.add_trace(go.Scatter(x=xp, y=yt, name="Tangente", line=dict(color='red', dash='dash')))
        fig.add_trace(go.Scatter(x=[ux0, 0, cx], y=[y0_val, cy, 0], mode='markers', marker=dict(color='orange', size=12, symbol='diamond'), name="Puntos clave"))
        
        st.plotly_chart(fig, use_container_width=True)
        st.balloons()
    else:
        st.warning("⚠️ Completa los pasos para desbloquear el gráfico.")
