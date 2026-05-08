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
