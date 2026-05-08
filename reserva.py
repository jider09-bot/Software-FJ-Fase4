"""
Módulo de Reservas del Sistema Software FJ
Integra clientes, servicios, duración y estados.
Manejo completo de excepciones con bloques try/except/else/finally
"""

import datetime
from entidades_base import EntidadBase, Catalogo
from excepciones import (
    ReservaInvalidaError, OperacionNoPermitidaError,
    ServicioNoDisponibleError, CalculoInconsistenteError,
    ParametroInvalidoError
)
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala
from logger import log


class Reserva(EntidadBase):
    """
    Clase que integra un cliente con un servicio por una duración determinada.
    Gestiona el ciclo de vida: PENDIENTE → CONFIRMADA → COMPLETADA / CANCELADA
    Implementa manejo robusto de excepciones en cada transición de estado.
    """

    ESTADOS = {"PENDIENTE", "CONFIRMADA", "COMPLETADA", "CANCELADA", "ERROR"}
    MOTIVOS_CANCELACION = {
        "CLIENTE": "Solicitud del cliente",
        "SERVICIO": "Servicio no disponible",
        "PAGO": "Problema de pago",
        "ADMIN": "Cancelación administrativa",
        "OTRO": "Otro motivo"
    }

    def __init__(self, cliente, servicio, horas, *, cantidad=1,
                 con_iva=True, descuento_porcentaje=0.0, notas=""):
        super().__init__(f"Reserva-{cliente.id}-{servicio.id}")
        self._cliente = None
        self._servicio = None
        self._horas = None
        self._cantidad = None
        self._estado = "PENDIENTE"
        self._con_iva = con_iva
        self._descuento_porcentaje = descuento_porcentaje
        self._costo_calculado = None
        self._notas = str(notas).strip()
        self._fecha_confirmacion = None
        self._fecha_completado = None
        self._fecha_cancelacion = None
        self._motivo_cancelacion = None
        self._errores_procesamiento = []

        # Asignaciones con validación
        self._asignar_cliente(cliente)
        self._asignar_servicio(servicio)
        self.horas = horas
        self.cantidad = cantidad

        log.debug("Reserva", f"Instancia creada [{self._id}] → Cliente: {cliente.nombre} | Servicio: {servicio.nombre}")

    # ---- Propiedades ----

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def horas(self):
        return self._horas

    @horas.setter
    def horas(self, valor):
        try:
            valor = float(valor)
        except (TypeError, ValueError):
            raise ParametroInvalidoError("Las horas deben ser un valor numérico", "horas")
        if valor <= 0:
            raise ParametroInvalidoError("Las horas deben ser mayores a cero", "horas")
        if valor > 720:  # Máximo 30 días
            raise ParametroInvalidoError("Las horas no pueden superar 720 (30 días)", "horas")
        self._horas = valor

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):
        try:
            valor = int(valor)
        except (TypeError, ValueError):
            raise ParametroInvalidoError("La cantidad debe ser un entero", "cantidad")
        if valor < 1:
            raise ParametroInvalidoError("La cantidad debe ser al menos 1", "cantidad")
        self._cantidad = valor

    @property
    def estado(self):
        return self._estado

    @property
    def costo_calculado(self):
        return self._costo_calculado

    @property
    def esta_activa(self):
        return self._estado in {"PENDIENTE", "CONFIRMADA"}

    # ---- Métodos privados de asignación ----

    def _asignar_cliente(self, cliente):
        from cliente import Cliente
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("Se requiere una instancia válida de Cliente")
        if not cliente.activo:
            raise ReservaInvalidaError(f"El cliente '{cliente.nombre}' está inactivo")
        self._cliente = cliente

    def _asignar_servicio(self, servicio):
        from servicios import Servicio
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("Se requiere una instancia válida de Servicio")
        self._servicio = servicio

    # ---- Ciclo de vida de la reserva ----

    def calcular_costo_previo(self, **kwargs_extra):
        """
        Calcula el costo antes de confirmar.
        Usa try/except/else para manejar el cálculo de forma segura.
        """
        try:
            self._servicio.verificar_disponibilidad(self._horas)
            costo = self._servicio.calcular_costo(
                self._horas,
                con_iva=self._con_iva,
                descuento_porcentaje=self._descuento_porcentaje,
                cantidad=self._cantidad,
                **kwargs_extra
            )
        except (ServicioNoDisponibleError, CalculoInconsistenteError, ParametroInvalidoError) as e:
            log.error("Reserva", f"[{self._id}] Error calculando costo: {e}", e)
            raise ReservaInvalidaError(
                f"No se pudo calcular el costo de la reserva: {e}"
            ) from e
        else:
            self._costo_calculado = costo
            log.debug("Reserva", f"[{self._id}] Costo calculado: ${costo:,.2f}")
            return costo

    def confirmar(self, **kwargs_extra):
        """
        Confirma la reserva.
        Usa try/except/else/finally para garantizar registro del intento.
        """
        log.info("Reserva", f"[{self._id}] Intentando confirmar...")

        if self._estado != "PENDIENTE":
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva en estado '{self._estado}'. "
                f"Solo se pueden confirmar reservas PENDIENTES.",
                operacion="confirmar"
            )

        try:
            # Verificar disponibilidad del servicio
            self._servicio.verificar_disponibilidad(self._horas)

            # Verificaciones específicas por tipo de servicio
            if isinstance(self._servicio, AlquilerEquipo):
                self._servicio.verificar_stock(self._cantidad)

            # Calcular costo final
            self.calcular_costo_previo(**kwargs_extra)

        except (ServicioNoDisponibleError, ReservaInvalidaError) as e:
            self._estado = "ERROR"
            self._errores_procesamiento.append(str(e))
            log.error("Reserva", f"[{self._id}] Confirmación fallida: {e}", e)
            raise ReservaInvalidaError(
                f"Reserva [{self._id}] no pudo confirmarse: {e}"
            ) from e

        except Exception as e:
            self._estado = "ERROR"
            self._errores_procesamiento.append(f"Error inesperado: {e}")
            log.critico("Reserva", f"[{self._id}] Error inesperado en confirmación", e)
            raise

        else:
            # Solo se ejecuta si no hubo excepciones
            self._estado = "CONFIRMADA"
            self._fecha_confirmacion = datetime.datetime.now()
            self._servicio.registrar_nueva_reserva()

            # Reservar unidades si es equipo
            if isinstance(self._servicio, AlquilerEquipo):
                self._servicio.reservar_unidades(self._cantidad)

            # Registrar en historial del cliente
            self._cliente.agregar_reserva(self._id)

            log.evento("Reserva", "CONFIRMAR",
                       f"OK | [{self._id}] | Cliente: {self._cliente.nombre} | "
                       f"Servicio: {self._servicio.nombre} | Costo: ${self._costo_calculado:,.2f}")

        finally:
            # Siempre se ejecuta, haya error o no
            log.debug("Reserva", f"[{self._id}] Proceso de confirmación finalizado. Estado: {self._estado}")

        return self._costo_calculado

    def cancelar(self, motivo="CLIENTE", descripcion_extra=""):
        """
        Cancela la reserva.
        Usa try/except/finally para garantizar liberación de recursos.
        """
        log.info("Reserva", f"[{self._id}] Intentando cancelar (motivo: {motivo})...")

        if self._estado not in {"PENDIENTE", "CONFIRMADA"}:
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva en estado '{self._estado}'",
                operacion="cancelar"
            )

        if motivo not in self.MOTIVOS_CANCELACION:
            motivo = "OTRO"

        try:
            # Liberar recursos si estaba confirmada
            if self._estado == "CONFIRMADA":
                self._servicio.liberar_reserva()
                if isinstance(self._servicio, AlquilerEquipo):
                    self._servicio.liberar_unidades(self._cantidad)

        except Exception as e:
            log.advertencia("Reserva", f"[{self._id}] Error al liberar recursos durante cancelación: {e}", e)
            # No re-lanzamos: la cancelación debe proceder aunque falle la liberación

        finally:
            self._estado = "CANCELADA"
            self._fecha_cancelacion = datetime.datetime.now()
            self._motivo_cancelacion = motivo
            desc = f"{self.MOTIVOS_CANCELACION[motivo]}"
            if descripcion_extra:
                desc += f" - {descripcion_extra}"
            log.evento("Reserva", "CANCELAR",
                       f"OK | [{self._id}] | Motivo: {desc}")

    def completar(self):
        """
        Marca la reserva como completada y acumula puntos al cliente.
        """
        if self._estado != "CONFIRMADA":
            raise OperacionNoPermitidaError(
                f"Solo se pueden completar reservas CONFIRMADAS. Estado actual: '{self._estado}'",
                operacion="completar"
            )

        try:
            if self._costo_calculado is None:
                raise ReservaInvalidaError("No hay costo calculado para completar la reserva")

            puntos = self._cliente.acumular_puntos(self._costo_calculado)
            self._servicio.liberar_reserva()

            if isinstance(self._servicio, AsesoriaEspecializada):
                self._servicio.completar_sesion()
            if isinstance(self._servicio, AlquilerEquipo):
                self._servicio.liberar_unidades(self._cantidad)

        except Exception as e:
            log.error("Reserva", f"[{self._id}] Error al completar la reserva: {e}", e)
            raise

        else:
            self._estado = "COMPLETADA"
            self._fecha_completado = datetime.datetime.now()
            log.evento("Reserva", "COMPLETAR",
                       f"OK | [{self._id}] | Cliente: {self._cliente.nombre} | "
                       f"Puntos acumulados: +{puntos} (Total: {self._cliente.puntos_fidelidad})")

    # ---- Métodos abstractos ----

    def validar(self):
        if not self._cliente or not self._servicio or self._horas is None:
            raise ReservaInvalidaError("Reserva incompleta: falta cliente, servicio o duración")
        return True

    def describir(self):
        costo_str = f"${self._costo_calculado:,.2f}" if self._costo_calculado else "Pendiente"
        return (f"Reserva [{self._id}] | Estado: {self._estado} | "
                f"Cliente: {self._cliente.nombre} | Servicio: {self._servicio.nombre} | "
                f"Horas: {self._horas} | Cantidad: {self._cantidad} | Costo: {costo_str}")

    def resumen(self):
        """Resumen detallado de la reserva"""
        lineas = [
            f"{'─' * 55}",
            f"  RESERVA ID  : {self._id}",
            f"  Estado      : {self._estado}",
            f"  Cliente     : {self._cliente.nombre} [{self._cliente.id}]",
            f"  Servicio    : {self._servicio.nombre}",
            f"  Tipo        : {self._servicio.__class__.__name__}",
            f"  Duración    : {self._horas} hora(s)",
            f"  Cantidad    : {self._cantidad} unidad(es)",
            f"  Con IVA     : {'Sí' if self._con_iva else 'No'}",
            f"  Descuento   : {self._descuento_porcentaje}%",
            f"  Costo Total : {'$' + f'{self._costo_calculado:,.2f}' if self._costo_calculado else 'Sin calcular'}",
            f"  Creada      : {self._fecha_creacion.strftime('%Y-%m-%d %H:%M')}",
        ]
        if self._fecha_confirmacion:
            lineas.append(f"  Confirmada  : {self._fecha_confirmacion.strftime('%Y-%m-%d %H:%M')}")
        if self._fecha_cancelacion:
            lineas.append(f"  Cancelada   : {self._fecha_cancelacion.strftime('%Y-%m-%d %H:%M')}")
            lineas.append(f"  Motivo      : {self.MOTIVOS_CANCELACION.get(self._motivo_cancelacion, '')}")
        if self._notas:
            lineas.append(f"  Notas       : {self._notas}")
        lineas.append(f"{'─' * 55}")
        return "\n".join(lineas)


class CatalogoReservas(Catalogo):
    """Repositorio central de reservas del sistema"""

    def __init__(self):
        super().__init__("CatalogoReservas")

    def agregar(self, reserva):
        if not isinstance(reserva, Reserva):
            raise TypeError("Solo se pueden agregar instancias de Reserva")
        try:
            reserva.validar()
            super().agregar(reserva)
            log.evento("CatalogoReservas", "AGREGAR_RESERVA", f"OK | {reserva.describir()}")
            return reserva
        except Exception as e:
            log.error("CatalogoReservas", f"Fallo al agregar reserva: {e}", e)
            raise

    def buscar(self, criterio):
        """Busca reservas por nombre de cliente (parcial)"""
        criterio_lower = criterio.lower()
        return [
            r for r in self._items.values()
            if criterio_lower in r.cliente.nombre.lower()
        ]

    def listar_por_estado(self, estado):
        """Filtra reservas por estado"""
        return [r for r in self._items.values() if r.estado == estado]

    def listar_por_cliente(self, cliente_id):
        """Retorna todas las reservas de un cliente"""
        return [r for r in self._items.values() if r.cliente.id == cliente_id]
