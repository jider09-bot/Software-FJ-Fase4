from abc import ABC, abstractmethod

# --- Excepciones Personalizadas ---
class SoftwareFJError(Exception):
    pass

class DatosInvalidosError(SoftwareFJError):
    pass

class ServicioNoDisponibleError(SoftwareFJError):
    pass

class CalculoInconsistenteError(SoftwareFJError):
    pass


# --- Clases Base y Entidades ---
class EntidadBase(ABC):
    def __init__(self, id_entidad):
        self._id = id_entidad

    @abstractmethod
    def mostrar_detalles(self):
        pass


class Cliente(EntidadBase):
    def __init__(self, id_entidad, nombre, documento):
        super().__init__(id_entidad)
        self.nombre = nombre
        self.documento = documento  # Asignarlo asi activa la validacion del setter

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        # Validacion: El documento no puede estar vacio ni ser menor a 5 digitos
        if not valor or len(str(valor)) < 5:
            raise DatosInvalidosError(f"El documento '{valor}' no es valido para el cliente {self.nombre}.")
        self.__documento = str(valor)

    def mostrar_detalles(self):
        return f"Cliente: {self.nombre} | ID: {self._id} | CC: {self.__documento}"


# --- Bloque de prueba (Los companeros pueden borrar esto despues) ---
if __name__ == "__main__":
    try:
        # Prueba exitosa
        cliente1 = Cliente(1, "Carlos Perez", "1087654321")
        print(cliente1.mostrar_detalles())
        
        # Prueba que fuerza el error personalizado
        cliente_invalido = Cliente(2, "Usuario Fallido", "123") 
    except DatosInvalidosError as e:
        print(f"Error capturado en prueba: {e}")