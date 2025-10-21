class Actividad:
    def __init__(self, nombre):
        self.nombre = nombre
        self.requiere_vestimenta = nombre in ["Palestra", "Escalada"]
        self.disponibilidad = {}  # {fecha: {horario: cupos}}

    def agregar_disponibilidad(self, fecha, horarios):
        """Agrega disponibilidad para una fecha específica.
        horarios es un diccionario de {hora: cupos_disponibles}"""
        self.disponibilidad[fecha] = horarios

    def tiene_cupos(self, fecha, horario):
        """Verifica si hay cupos disponibles para una fecha y horario específicos"""
        return (fecha in self.disponibilidad and 
                horario in self.disponibilidad[fecha] and 
                self.disponibilidad[fecha][horario] > 0)

    def inscribir_participante(self, fecha, horario):
        """Registra un participante en un horario específico"""
        if self.tiene_cupos(fecha, horario):
            self.disponibilidad[fecha][horario] -= 1
            return True
        return False 

    def crear_dia(self, fecha):
        """Crea un nuevo día con horarios predeterminados y 10 cupos por horario"""
        horarios_predeterminados = {
        "08:00": 10,
        "10:00": 10,
        "12:00": 10,
        "14:00": 10,
        "16:00": 10,
        "18:00": 10
        }
        if fecha not in self.disponibilidad:
            self.disponibilidad[fecha] = {}

        self.disponibilidad[fecha] = horarios_predeterminados
