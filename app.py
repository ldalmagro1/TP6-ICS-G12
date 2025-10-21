import streamlit as st
from actividad import Actividad
from inscripcion import inscribirse
from datetime import datetime, timedelta
import time

# Inicializar actividades
if 'actividades' not in st.session_state:
    st.session_state.actividades = {
        "Tirolesa": Actividad("Tirolesa"),
        "Palestra": Actividad("Palestra"),
        "Safari": Actividad("Safari"),
        "Jardinería": Actividad("Jardinería"),
    }
    # Agregar disponibilidad
    for actividad in st.session_state.actividades.values():
        for i in range(7):  # Agrega los próximos 7 días
            fecha = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
            actividad.crear_dia(fecha)

st.title("Inscripción a Actividades 🌲")

# Selección de actividad
actividad_nombre = st.selectbox("Elegí una actividad", list(st.session_state.actividades.keys()))
actividad = st.session_state.actividades[actividad_nombre]

# Selección de fecha
fecha = st.date_input(
    "Seleccioná la fecha",
    min_value=datetime.today(),
    max_value=datetime.today() + timedelta(days=6)
)
fecha_str = fecha.strftime("%Y-%m-%d")

# Selección de horario
if fecha_str in actividad.disponibilidad:
    horarios_disponibles = [h for h, cupos in actividad.disponibilidad[fecha_str].items() if cupos > 0]
    if not horarios_disponibles:
        st.warning("No hay horarios disponibles para esta fecha")
        st.stop()
    horario = st.selectbox("Elegí horario", horarios_disponibles)
else:
    st.warning("No hay disponibilidad para esta fecha")
    st.stop()

# Información del participante
st.subheader("Datos del participante")
nombre = st.text_input("Nombre completo")
edad = st.number_input("Edad", min_value=0, max_value=120)
acepta_tc = st.checkbox("Acepto términos y condiciones")

# Talle de vestimenta si es requerido
if actividad.requiere_vestimenta:
    talle = st.selectbox("Talle de vestimenta", ["S", "M", "L", "XL", "XXL"])
else:
    talle = None

# Inscripción
if st.button("Inscribirme"):
    # Validar campos requeridos
    if not nombre or not str(nombre).strip():
        st.error("Por favor ingrese un nombre válido")
        st.stop()
    
    if not edad or edad <= 0:
        st.error("Por favor ingrese una edad válida")
        st.stop()

    if not acepta_tc:
        st.error("Debe aceptar los términos y condiciones")
        st.stop()
    
    participante = {
        "nombre": nombre,
        "edad": edad,
        "acepta_terminos": acepta_tc
    }
    if talle:
        participante["talle_vestimenta"] = talle

    resultado = inscribirse(actividad, fecha_str, horario, [participante])
    
 # Muestra el resultado
    if resultado["ok"]:
        success_modal = st.empty()
        with success_modal.container():
            st.success("✅ Inscripción exitosa!")
            st.balloons()  
            time.sleep(2)
        
        # Limpia el modal y actualiza la actividad en el estado de la sesión
        success_modal.empty()
        st.session_state.actividades[actividad_nombre] = actividad
        st.rerun()
    else:
        st.error(resultado["mensaje"])

# Mostrar disponibilidad
st.subheader("Disponibilidad")
if fecha_str in actividad.disponibilidad:
    st.write("Cupos disponibles:")
    for hora, cupos in actividad.disponibilidad[fecha_str].items():
        st.write(f"- {hora}: {cupos} cupos")