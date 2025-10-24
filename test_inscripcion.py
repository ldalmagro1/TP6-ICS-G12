import pytest
from inscripcion  import inscribirse
from actividad import Actividad

def test_no_acepta_terminos_y_condiciones():
    actividad = Actividad("Tirolesa")
    actividad.agregar_disponibilidad("2025-10-10", {"10:00": 5, "11:00": 0})
    resultado = inscribirse(actividad, "2025-10-10", "11:00", [{"nombre": "Toto", "acepta_terminos": False}])
    assert resultado["ok"] is False
    assert resultado["mensaje"] == "Debe aceptar los términos y condiciones"

def test_sin_cupos_para_fecha_horario():
    actividad = Actividad("Tirolesa")
    actividad.agregar_disponibilidad("2025-10-10", {"10:00": 0})
    resultado = inscribirse(
        actividad,
        "2025-10-10",
        "10:00",
        [{"nombre": "Toto", "acepta_terminos": True}]
    )
    assert resultado["ok"] is False
    assert resultado["mensaje"] == "No hay cupos disponibles"

def test_no_indica_talle_en_vestimenta_requerida():
    actividad = Actividad("Palestra")
    actividad.agregar_disponibilidad("2025-10-10", {"10:00": 5})
    resultado = inscribirse(actividad, "2025-10-10", "10:00", [{"nombre": "Toto", "acepta_terminos": True}])
    assert resultado["ok"] is False
    assert resultado["mensaje"] == "Debe indicar el talle de la vestimenta requerida"

def test_horario_no_disponible():
    actividad = Actividad("Tirolesa")
    actividad.crear_dia("2025-10-10")
    resultado = inscribirse(actividad, "2025-10-10", "06:00", [{"nombre": "Toto", "acepta_terminos": True}])
    assert resultado["ok"] is False
    assert resultado["mensaje"] == "No hay cupos disponibles"

#Probar inscribirse a una actividad sin ingresar talle de vestimenta porque la actividad no lo requiere (pasa)
def test_no_indica_talle_en_vestimenta_no_requerida():
    actividad = Actividad("Tirolesa")
    actividad.agregar_disponibilidad("2025-10-10", {"10:00": 5})
    resultado = inscribirse(actividad, "2025-10-10", "10:00", [{"nombre": "Toto", "acepta_terminos": True}])
    assert resultado["ok"] is True
    assert resultado["mensaje"] == "Inscripción exitosa"


#Probar inscribirse a una actividad del listado que poseen cupos disponibles, seleccionando un horario, ingresando los datos del visitante (nombre, DNI, edad, talla de la vestimenta si la actividad lo requiere) y aceptando los términos y condiciones (pasa) 
def test_inscripcion_exitosa():
    actividad = Actividad("Palestra")
    actividad.agregar_disponibilidad("2025-10-10", {"10:00": 5})
    resultado = inscribirse(actividad, "2025-10-10", "10:00", [{"nombre": "Toto", "acepta_terminos": True, "talle_vestimenta": "M"}])
    assert resultado["ok"] is True
    assert resultado["mensaje"] == "Inscripción exitosa"

