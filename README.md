Proyecto de programación Fase 4 - Sistema de reservas
# Proyecto Fase 4 - Sistema de Reservas "Software FJ"

## 👥 Integrantes del Equipo
* Jaider Yair Morales Pantoja
* Nelson Bryan Rosero Vásquez
* Frankin Ademar Ruiz Torres
* Edison David López Mirama

## 📝 Descripción del Proyecto
Este repositorio contiene el desarrollo de la Fase 4 para la empresa Software FJ. Es un sistema basado en Programación Orientada a Objetos en Python, diseñado sin bases de datos, el objetivo principal del proyecto es aplicar conceptos de herencia, polimorfismo, encapsulamiento y, sobre todo, implementar un manejo robusto de excepciones para que el programa siga funcionando ante cualquier error.

## 📂 Archivos y Avances del Código
Hasta el momento, el sistema está dividido en módulos para facilitar el trabajo en equipo. Estos son los archivos desarrollados y su función:

### 1. `cliente_y_excepciones.py`
Este archivo contiene la base del sistema y las reglas de seguridad:
* **Excepciones Personalizadas:** Creamos clases de error propias (como `DatosInvalidosError` o `CalculoInconsistenteError`) para capturar fallos sin que la aplicación se cierre.
* **Clase Abstracta `EntidadBase`:** Es la plantilla general del sistema creada con la librería `abc`.
* **Clase `Cliente`:** Representa a los usuarios. Aquí aplicamos encapsulamiento protegiendo el documento de identidad. Antes de guardar el documento, el sistema valida que no esté vacío y que tenga al menos 5 caracteres.

### 2. `servicios.py`
Aquí manejamos el catálogo de lo que ofrece la empresa:
* **Clase Abstracta `Servicio`:** Define cómo debe ser un servicio en general.
* **Herencia y Polimorfismo:** Creamos las subclases `ServicioSala`, `ServicioEquipo` y `ServicioAsesoria`. Cada una calcula su costo de forma diferente (por ejemplo, el equipo tiene un descuento si se alquila por 5 días o más, y la asesoría tiene un cobro fijo extra por honorarios).

### 3. `reserva.py`
Este archivo gestiona el ciclo de vida completo de una reserva:
**Clase `Reserva`**: Une un Cliente con un Servicio y maneja los estados: **PENDIENTE → CONFIRMADA → COMPLETADA o CANCELADA**.
**Confirmación con** `try/except/else/finally`: El bloque try verifica disponibilidad y calcula el costo; el else confirma la reserva si todo salió bien; el finally garantiza que siempre quede registro en el log.
**Encadenamiento de excepciones:** Si ocurre un ServicioNoDisponibleError, se relanza como ReservaInvalidaError usando raise ... from e, conservando la causa original.

### 4. `main.py`
Este es el punto de entrada del sistema donde se simulan todas las operaciones:
**Simulación de 20 operaciones:** Divididas en tres bloques — clientes, servicios y reservas — mezclando casos exitosos e inválidos para demostrar que el sistema no se cae ante errores.
**Manejo global de excepciones:** El programa principal usa `try/except` para capturar `KeyboardInterrupt` y cualquier Exception inesperada, cerrando el sistema de forma ordenada.
**Resumen final:** Al terminar, imprime el total de clientes, servicios y reservas registradas clasificadas por estado.
Simulaciones de Clientes: Se realizan pruebas con clientes válidos e inválidos para verificar las validaciones del documento y el correcto manejo de excepciones personalizadas.
Simulaciones de Servicios: Se prueban distintos tipos de servicios (ServicioSala, ServicioEquipo y ServicioAsesoria) validando cálculos de costos, disponibilidad y restricciones de uso.
Simulaciones de Reservas: Se crean reservas exitosas y fallidas para comprobar el funcionamiento de confirmaciones, cancelaciones y procesamiento de pagos.
Manejo de Excepciones: Durante las simulaciones se generan errores controlados como duraciones negativas, servicios no disponibles y datos faltantes, garantizando que el sistema continúe funcionando sin detenerse.
Validación de Robustez: Las 10 simulaciones permiten demostrar que el sistema mantiene estabilidad, registra errores y responde correctamente ante diferentes escenarios reales.

### 5. `logger.py`
Este archivo es el sistema de registro de eventos:
**Clase Logger:** Guarda en el archivo `sistema_softwarefj`.log todos los eventos importantes de la ejecución, conservando el historial entre sesiones.
**Niveles de Registro:** Clasifica cada evento en cinco niveles de severidad: `DEBUG, INFO, ADVERTENCIA, ERROR y CRITICO.`
**Protección ante fallos:** Si ocurre un error al escribir en el archivo, se ignora silenciosamente para que el logger nunca provoque el cierre del sistema.
