def inscribirse(actividad, fecha, horario, participantes):
    # Verificar términos y condiciones
    for participante in participantes:
        if not acepta_terminos(participante):
            return {"ok": False, "mensaje": "Debe aceptar los términos y condiciones"}

    # Verificar cupos
    if not actividad.tiene_cupos(fecha, horario):
        return {"ok": False, "mensaje": "No hay cupos disponibles"}
    
    # Verificar vestimenta si es necesario
    if actividad.requiere_vestimenta:
        for participante in participantes:
            if "talle_vestimenta" not in participante:
                return {"ok": False, "mensaje": "Debe indicar el talle de la vestimenta requerida"}

    # Realizar la inscripción
    if actividad.inscribir_participante(fecha, horario):
        return {"ok": True, "mensaje": "Inscripción exitosa"}
    return {"ok": False, "mensaje": "Error en la inscripción"}

def acepta_terminos(participante):
    return participante.get("acepta_terminos", False)


