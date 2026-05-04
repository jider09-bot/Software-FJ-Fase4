from abc import ABC, abstractmethod

# Creamos este error por si meten horas o dias negativos
class CalculoInconsistenteError(Exception):
    pass

# Clase padre 
class Servicio(ABC):
    def __init__(self, id_entidad, nombre, costo_base):
        self._id = id_entidad
        self.nombre = nombre
        self.costo_base = costo_base
        self.disponible = True  

    @abstractmethod
    def calcular_costo_total(self, duracion, impuesto=0.0, descuento=0.0):
        pass

    @abstractmethod
    def mostrar_detalles(self):
        pass


# --- Clases hijas que heredan de Servicio ---

class ServicioSala(Servicio):
    def __init__(self, id_entidad, nombre, costo_base, capacidad):
        super().__init__(id_entidad, nombre, costo_base)
        self.capacidad = capacidad

    def calcular_costo_total(self, duracion, impuesto=0.0, descuento=0.0):
        if duracion <= 0:
            raise CalculoInconsistenteError("La duracion no puede ser cero o negativa")
        
        return (self.costo_base * duracion) + impuesto - descuento

    def mostrar_detalles(self):
        return f"Sala: {self.nombre}, Capacidad: {self.capacidad}, Precio: ${self.costo_base}"


class ServicioEquipo(Servicio):
    def __init__(self, id_entidad, nombre, costo_base, tipo):
        super().__init__(id_entidad, nombre, costo_base)
        self.tipo = tipo

    def calcular_costo_total(self, duracion, impuesto=0.0, descuento=0.0):
        if duracion <= 0:
            raise CalculoInconsistenteError("Los dias no pueden ser cero o negativos")
        
        # Si alquila por 5 dias o mas le damos 10% de descuento extra
        if duracion >= 5:
            descuento = descuento + (self.costo_base * 0.10)
            
        return (self.costo_base * duracion) + impuesto - descuento

    def mostrar_detalles(self):
        return f"Equipo: {self.nombre} ({self.tipo}), Precio: ${self.costo_base}"


class ServicioAsesoria(Servicio):
    def __init__(self, id_entidad, nombre, costo_base, especialista):
        super().__init__(id_entidad, nombre, costo_base)
        self.especialista = especialista

    def calcular_costo_total(self, duracion, impuesto=0.0, descuento=0.0):
        if duracion <= 0:
            raise CalculoInconsistenteError("Las horas no pueden ser cero o negativas")
            
        # Cobro extra por honorarios del especialista
        honorarios = 50.0
        return (self.costo_base * duracion) + honorarios + impuesto - descuento

    def mostrar_detalles(self):
        return f"Asesoria: {self.nombre} con {self.especialista}, Precio base: ${self.costo_base}"