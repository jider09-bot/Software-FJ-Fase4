"""
Módulo de logging para el Sistema Software FJ
Registra eventos, errores y operaciones en archivo de logs
"""

import os
import datetime


class Logger:
    """Clase para gestión de logs del sistema"""

    NIVELES = {"DEBUG": 0, "INFO": 1, "ADVERTENCIA": 2, "ERROR": 3, "CRITICO": 4}

    def __init__(self, archivo_log="sistema_softwarefj.log", nivel_minimo="DEBUG"):
        self.archivo_log = archivo_log
        self.nivel_minimo = nivel_minimo
        self._inicializar_archivo()

    def _inicializar_archivo(self):
        try:
            with open(self.archivo_log, "a", encoding="utf-8") as f:
                separador = "=" * 70
                f.write(f"\n{separador}\n")
                f.write(f"  SESIÓN INICIADA: {self._timestamp()}\n")
                f.write(f"  Sistema: Software FJ - Gestión Integral\n")
                f.write(f"{separador}\n\n")
        except OSError as e:
            print(f"[ADVERTENCIA] No se pudo inicializar el archivo de logs: {e}")

    def _timestamp(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _escribir(self, nivel, modulo, mensaje, excepcion=None):
        if self.NIVELES.get(nivel, 0) < self.NIVELES.get(self.nivel_minimo, 0):
            return
        try:
            with open(self.archivo_log, "a", encoding="utf-8") as f:
                linea = f"[{self._timestamp()}] [{nivel:12s}] [{modulo:20s}] {mensaje}"
                f.write(linea + "\n")
                if excepcion:
                    f.write(f"  >>> Excepción: {type(excepcion).__name__}: {excepcion}\n")
        except OSError:
            pass  # El log nunca debe detener la aplicación

    def debug(self, modulo, mensaje):
        self._escribir("DEBUG", modulo, mensaje)

    def info(self, modulo, mensaje):
        self._escribir("INFO", modulo, mensaje)
        print(f"  ✔  [{modulo}] {mensaje}")

    def advertencia(self, modulo, mensaje, excepcion=None):
        self._escribir("ADVERTENCIA", modulo, mensaje, excepcion)
        print(f"  ⚠  [{modulo}] ADVERTENCIA: {mensaje}")

    def error(self, modulo, mensaje, excepcion=None):
        self._escribir("ERROR", modulo, mensaje, excepcion)
        print(f"  ✖  [{modulo}] ERROR: {mensaje}")
        if excepcion:
            print(f"       Causa: {type(excepcion).__name__}: {excepcion}")

    def critico(self, modulo, mensaje, excepcion=None):
        self._escribir("CRITICO", modulo, mensaje, excepcion)
        print(f"  !! [{modulo}] CRÍTICO: {mensaje}")
        if excepcion:
            print(f"       Causa: {type(excepcion).__name__}: {excepcion}")

    def evento(self, modulo, operacion, resultado):
        """Registra un evento de operación del sistema"""
        self._escribir("INFO", modulo, f"OPERACIÓN '{operacion}' → {resultado}")


# Instancia global del logger
log = Logger()
