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
    * **Raíz:** `sqrt(x)`
    """)
    
    st.header("✍️ Editor")
    u_f = st.text_input("Define f(x):", "x^2 - 4")
    ux0 = st.number_input("Punto de abscisa (x0):", value=2.0)
    
    x_s = sp.symbols('x')
    try:
        # Reemplazamos ^ por ** para que Sympy lo entienda internamente
        f_limpio = u_f.replace("^", "**")
        f_s = sp.sympify(f_limpio)
        st.markdown("---")
        st.write("**Vista Previa Matemática:**")
        st.latex(sp.latex(f_s))
    except:
        st.error("Error en la función. Revisa la Guía de Escritura.")
        st.stop()
    
    ayuda = st.toggle("Activar modo Tutor (Pistas)")

# --- LÓGICA DE CÁLCULO ---
y0_val = float(f_s.subs(x_s, ux0))
df_s = sp.diff(f_s, x_s)
m_val = float(df_s.subs(x_s, ux0))
b_val = float(y0_val - (m_val * ux0))

# --- ENUNCIADO DINÁMICO ---
st.markdown(f"""
> **Enunciado:** Determine la ecuación de la recta tangente a la gráfica de la función 
> $f(x) = {sp.latex(f_s)}$ en el punto de abscisa $x_0 = {ux0}$.
""")

# --- FLUJO INTERACTIVO ---
col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("📝 Resolución Paso a Paso")
    
    # PASO 1: ORDENADA Y0
    with st.container(border=True):
        st.write("**Paso 1: Punto de Tangencia**")
        u_y0 = st.number_input(f"Halla $y_0 = f({ux0})$:", value=0.0, step=0.1, key="y0_u")
        check1 = abs(u_y0 - y0_val) < 0.1
        if check1: st.success("¡y0 correcto! ✅")

    # PASO 2: PENDIENTE M
    if check1:
        with st.container(border=True):
            st.write("**Paso 2: Pendiente**")
            u_m = st.number_input(f"Halla $m = f'({ux0})$:", value=0.0, step=0.1, key="m_u")
            check2 = abs(u_m - m_val) < 0.1
            if check2: st.success("¡m correcto! ✅")
    else:
        st.lock_button("Paso 2 bloqueado", icon="🔒")

    # PASO 3: HALLAR B
    if 'check2' in locals() and check2:
        with st.container(border=True):
            st.write("**Paso 3: Ordenada al origen (b)**")
            st.write("Reemplaza en $y = mx + b$:")
            st.latex(f"{y0_val:.2f} = ({m_val:.2f})({ux0}) + b")
            u_b = st.number_input("Despeja e ingresa b:", value=0.0, step=0.1, key="b_u")
            check3 = abs(u_b - b_val) < 0.1
            if check3: st.success("¡b correcto! ✅")
    else:
        st.lock_button("Paso 3 bloqueado", icon="🔒")

    # PASO 4: ECUACIÓN FINAL
    desbloqueo = False
    if 'check3' in locals() and check3:
        with st.container(border=True):
            st.write("**Paso 4: Ecuación de la Recta**")
            u_eq = st.text_input("Escribe tu ecuación (ej. y=2x+4):")
            
            # Validación flexible: buscamos que los números m y b estén en el texto
            if u_eq:
                m_txt = f"{m_val:.1f}".replace(".0", "")
                b_txt = f"{abs(b_val):.1f}".replace(".0", "")
                
                # Verificamos si los valores de m y b aparecen en la cadena
                if m_txt in u_eq and b_txt in u_eq:
                    st.success("¡Ecuación validada! 🚀")
                    desbloqueo = True
                else:
                    st.warning("Asegúrate de incluir m y b correctos en tu ecuación.")
    else:
        st.lock_button("Paso 4 bloqueado", icon="🔒")

# --- GRÁFICA Y CORTES ---
with col2:
    if desbloqueo:
        st.subheader("📊 Gráfica y Cortes")
        cx = -b_val / m_val if m_val != 0 else 0
        cy = b_val
        
        st.latex(f"Cortes: \ X({cx:.2f}, 0) \ | \ Y(0, {cy:.2f})")

        # Preparar datos gráfica
        f_n = sp.lambdify(x_s, f_s, 'numpy')
        xp = np.linspace(ux0-5, ux0+5, 400)
        yp = f_n(xp)
        yt = m_val * xp + b_val

        fig = go.Figure()
        fig.add_hline(y=0, line_color="black")
        fig.add_vline(x=0, line_color="black")
        
        # Curva
        fig.add_trace(go.Scatter(x=xp, y=yp, name="f(x)", line=dict(color='#003366', width=4)))
        
        # Tangente
        fig.add_trace(go.Scatter(x=xp, y=yt, name="Tangente", line=dict(color='red', dash='dash')))
        
        # Puntos de interés
        fig.add_trace(go.Scatter(x=[ux0, 0, cx], y=[y0_val, cy, 0], mode='markers', 
                                 marker=dict(color='orange', size=12, symbol='diamond'), 
                                 name="Puntos clave"))
        
        fig.update_layout(plot_bgcolor='white', height=500, margin=dict(l=0,r=0,b=0,t=40))
        st.plotly_chart(fig, use_container_width=True)
        st.balloons()
    else:
        st.warning("⚠️ El gráfico se mostrará cuando valides la ecuación en el Paso 4.")
        st.image("https://via.placeholder.com/600x400.png?text=Completa+los+pasos+para+ver+el+grafico")
