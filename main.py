"""
╔══════════════════════════════════════════════════════════════════════════════╗
║         SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ                          ║
║         Clientes · Servicios · Reservas                                    ║
║         Simulación de 10+ Operaciones con Manejo de Excepciones            ║
╚══════════════════════════════════════════════════════════════════════════════╝

Equipo: Grupo 5 estudiantes
Paradigma: Orientado a Objetos con Python
"""

import sys
from logger import log
from cliente import Cliente, CatalogoClientes
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada, CatalogoServicios
from reserva import Reserva, CatalogoReservas
from excepciones import (
    SoftwareFJError, ClienteInvalidoError, ServicioNoDisponibleError,
    ReservaInvalidaError, ParametroInvalidoError, CalculoInconsistenteError,
    OperacionNoPermitidaError, CapacidadExcedidaError
)


# ─────────────────────────────────────────────────────────────────────────────
# Utilidades de presentación
# ─────────────────────────────────────────────────────────────────────────────

def titulo(texto, nivel=1):
    if nivel == 1:
        print(f"\n{'═' * 70}")
        print(f"  {texto}")
        print(f"{'═' * 70}")
    elif nivel == 2:
        print(f"\n  {'─' * 60}")
        print(f"    {texto}")
        print(f"  {'─' * 60}")
    else:
        print(f"\n    ▶ {texto}")


def resultado_ok(texto):
    print(f"      ✔  {texto}")


def resultado_error(texto):
    print(f"      ✖  {texto}")


def separador():
    print()


# ─────────────────────────────────────────────────────────────────────────────
# BLOQUE PRINCIPAL DE SIMULACIÓN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    log.info("Main", "═══ Iniciando sistema Software FJ ═══")

    # Inicializar catálogos
    catalogo_clientes = CatalogoClientes()
    catalogo_servicios = CatalogoServicios()
    catalogo_reservas = CatalogoReservas()

    titulo("SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ")
    print("  Iniciando simulación de operaciones...\n")

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE 1: REGISTRO DE CLIENTES
    # ══════════════════════════════════════════════════════════════════════════
    titulo("BLOQUE 1 — REGISTRO DE CLIENTES (Válidos e Inválidos)", nivel=1)

    # Clientes que se guardan para uso posterior
    cliente_ana = None
    cliente_carlos = None
    cliente_lucia = None

    # ── OPERACIÓN 1: Cliente válido ──────────────────────────────────────────
    titulo("OP 1: Registro cliente válido — Ana Torres", nivel=2)
    try:
        ana = Cliente(
            nombre="Ana Torres Mendoza",
            email="ana.torres@empresa.co",
            telefono="+57 310 4567890",
            tipo_documento="CC",
            numero_documento="1023456789"
        )
        catalogo_clientes.agregar(ana)
        cliente_ana = ana
        resultado_ok(f"Cliente registrado: {ana}")
    except ClienteInvalidoError as e:
        resultado_error(f"Error de cliente: {e}")
        log.error("Main", "OP1 falló inesperadamente", e)
    finally:
        log.debug("Main", "OP1 finalizada")

    separador()

    # ── OPERACIÓN 2: Cliente con email inválido ──────────────────────────────
    titulo("OP 2: Registro cliente con email inválido", nivel=2)
    try:
        mal_cliente = Cliente(
            nombre="Pedro Gómez",
            email="pedro-sin-arroba",   # ← Email inválido
            telefono="3001234567",
            tipo_documento="CC",
            numero_documento="987654321"
        )
        catalogo_clientes.agregar(mal_cliente)
        resultado_ok(f"Registrado: {mal_cliente}")
    except ClienteInvalidoError as e:
        resultado_error(f"Capturado ClienteInvalidoError: {e}")
        log.advertencia("Main", "OP2: Email inválido rechazado correctamente", e)
    except SoftwareFJError as e:
        resultado_error(f"Error sistema: {e}")
    finally:
        log.debug("Main", "OP2 finalizada")

    separador()

    # ── OPERACIÓN 3: Segundo cliente válido ──────────────────────────────────
    titulo("OP 3: Registro cliente válido — Carlos Ríos", nivel=2)
    try:
        carlos = Cliente(
            nombre="Carlos Ríos Herrera",
            email="carlos.rios@tech.com",
            telefono="3157891234",
            tipo_documento="NIT",
            numero_documento="900123456-1"
        )
        catalogo_clientes.agregar(carlos)
        cliente_carlos = carlos
        resultado_ok(f"Cliente registrado: {carlos}")
    except ClienteInvalidoError as e:
        resultado_error(f"Error: {e}")
    finally:
        log.debug("Main", "OP3 finalizada")

    separador()

    # ── OPERACIÓN 4: Cliente con tipo de documento inválido ──────────────────
    titulo("OP 4: Registro cliente con tipo de documento inválido", nivel=2)
    try:
        Cliente(
            nombre="María López",
            email="maria@valido.com",
            telefono="3209876543",
            tipo_documento="DNI",   # ← Tipo no permitido en Colombia
            numero_documento="11223344"
        )
        resultado_ok("¡Advertencia! Cliente creado con tipo inválido (no debería ocurrir)")
    except ClienteInvalidoError as e:
        resultado_error(f"Capturado: {e}")
        log.advertencia("Main", "OP4: Tipo de documento inválido rechazado", e)
    finally:
        log.debug("Main", "OP4 finalizada")

    separador()

    # ── OPERACIÓN 5: Cliente válido — Lucía (se usará para asesoría) ─────────
    titulo("OP 5: Registro cliente válido — Lucía Fernández", nivel=2)
    try:
        lucia = Cliente(
            nombre="Lucía Fernández Vargas",
            email="lucia.fernandez@startup.io",
            telefono="+57-301-2345678",
            tipo_documento="CE",
            numero_documento="ABX123456"
        )
        catalogo_clientes.agregar(lucia)
        cliente_lucia = lucia
        resultado_ok(f"Cliente registrado: {lucia}")
    except ClienteInvalidoError as e:
        resultado_error(f"Error: {e}")
    finally:
        log.debug("Main", "OP5 finalizada")

    separador()

    # ── OPERACIÓN 6: Intentar registrar email duplicado ──────────────────────
    titulo("OP 6: Intento de email duplicado (ana.torres@empresa.co)", nivel=2)
    try:
        duplicado = Cliente(
            nombre="Ana Duplicada",
            email="ana.torres@empresa.co",  # ← Ya registrado en OP1
            telefono="3001112233",
            tipo_documento="CC",
            numero_documento="9988776655"
        )
        catalogo_clientes.agregar(duplicado)
        resultado_ok(f"Registrado: {duplicado}")
    except ClienteInvalidoError as e:
        resultado_error(f"Capturado duplicado: {e}")
        log.advertencia("Main", "OP6: Email duplicado rechazado correctamente", e)
    finally:
        log.debug("Main", "OP6 finalizada")

    separador()
    print(f"\n  Total clientes registrados: {catalogo_clientes.total}")

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE 2: CREACIÓN DE SERVICIOS
    # ══════════════════════════════════════════════════════════════════════════
    titulo("BLOQUE 2 — CREACIÓN DE SERVICIOS", nivel=1)

    sala_principal = None
    laptop_portatil = None
    asesoria_tech = None

    # ── OPERACIÓN 7: Crear sala de conferencias válida ───────────────────────
    titulo("OP 7: Creación de Sala de Conferencias Ejecutiva", nivel=2)
    try:
        sala = ReservaSala(
            nombre="Sala Ejecutiva Piso 8",
            descripcion="Sala de reuniones ejecutivas con vista panorámica y equipos de alta gama",
            precio_base_hora=150_000,
            capacidad_personas=20,
            tipo_sala="EJECUTIVA",
            tiene_proyector=True
        )
        catalogo_servicios.agregar(sala)
        sala_principal = sala
        resultado_ok(sala.describir())
    except (ParametroInvalidoError, SoftwareFJError) as e:
        resultado_error(f"Error al crear sala: {e}")
    finally:
        log.debug("Main", "OP7 finalizada")

    separador()

    # ── OPERACIÓN 8: Crear servicio de alquiler de equipos ───────────────────
    titulo("OP 8: Creación de Servicio de Alquiler Laptop", nivel=2)
    try:
        laptop = AlquilerEquipo(
            nombre="Laptop Corporativa Dell XPS",
            descripcion="Portátil de alto rendimiento para presentaciones y trabajo de campo",
            precio_base_hora=25_000,
            categoria="COMPUTADOR",
            unidades_disponibles=8,
            requiere_seguro=True
        )
        catalogo_servicios.agregar(laptop)
        laptop_portatil = laptop
        resultado_ok(laptop.describir())
    except (ParametroInvalidoError, SoftwareFJError) as e:
        resultado_error(f"Error al crear equipo: {e}")
    finally:
        log.debug("Main", "OP8 finalizada")

    separador()

    # ── OPERACIÓN 9: Crear asesoría tecnológica ──────────────────────────────
    titulo("OP 9: Creación de Servicio de Asesoría Tecnológica", nivel=2)
    try:
        asesoria = AsesoriaEspecializada(
            nombre="Asesoría Transformación Digital",
            descripcion="Consultoría especializada en arquitectura de software y transformación digital",
            precio_base_hora=200_000,
            area="TECNOLOGIA",
            nivel_expertise="EXPERTO",
            nombre_asesor="Dr. Juan Pérez Castro"
        )
        catalogo_servicios.agregar(asesoria)
        asesoria_tech = asesoria
        resultado_ok(asesoria.describir())
        resultado_ok(f"Tarifa efectiva: ${asesoria.tarifa_efectiva:,.0f}/hora")
    except (ParametroInvalidoError, SoftwareFJError) as e:
        resultado_error(f"Error al crear asesoría: {e}")
    finally:
        log.debug("Main", "OP9 finalizada")

    separador()

    # ── OPERACIÓN 10: Intentar crear servicio con precio negativo ────────────
    titulo("OP 10: Servicio con precio base negativo (inválido)", nivel=2)
    try:
        servicio_malo = ReservaSala(
            nombre="Sala Gratuita",
            descripcion="Sala sin costo, pero el precio base no puede ser cero o negativo",
            precio_base_hora=-5000,   # ← Precio inválido
            capacidad_personas=10,
            tipo_sala="REUNION"
        )
        catalogo_servicios.agregar(servicio_malo)
        resultado_ok(f"Creado: {servicio_malo.describir()}")
    except ParametroInvalidoError as e:
        resultado_error(f"Capturado ParametroInvalidoError: {e}")
        log.advertencia("Main", "OP10: Precio negativo rechazado correctamente", e)
    finally:
        log.debug("Main", "OP10 finalizada")

    separador()
    print(f"\n  Total servicios registrados: {catalogo_servicios.total}")

    # ══════════════════════════════════════════════════════════════════════════
    # BLOQUE 3: RESERVAS (Exitosas y Fallidas)
    # ══════════════════════════════════════════════════════════════════════════
    titulo("BLOQUE 3 — RESERVAS COMPLETAS", nivel=1)

    # ── OPERACIÓN 11: Reserva exitosa — Sala con audiovisual ─────────────────
    titulo("OP 11: Reserva de sala ejecutiva con audiovisual (Ana Torres)", nivel=2)
    reserva_ana = None
    try:
        if cliente_ana and sala_principal:
            reserva = Reserva(
                cliente=cliente_ana,
                servicio=sala_principal,
                horas=4,
                con_iva=True,
                descuento_porcentaje=10.0,
                notas="Presentación trimestral de resultados"
            )
            catalogo_reservas.agregar(reserva)

            costo = reserva.confirmar(con_audiovisual=True)
            reserva_ana = reserva
            resultado_ok(f"¡Reserva confirmada!")
            print(reserva.resumen())
        else:
            resultado_error("No se pudo crear la reserva: cliente o sala no disponibles")

    except ReservaInvalidaError as e:
        resultado_error(f"Reserva fallida: {e}")
        log.error("Main", "OP11 falló", e)
    except ServicioNoDisponibleError as e:
        resultado_error(f"Servicio no disponible: {e}")
    finally:
        log.debug("Main", "OP11 finalizada")

    separador()

    # ── OPERACIÓN 12: Reserva exitosa — Alquiler de equipos ──────────────────
    titulo("OP 12: Reserva de laptops (Carlos Ríos — 3 unidades)", nivel=2)
    reserva_carlos = None
    try:
        if cliente_carlos and laptop_portatil:
            reserva = Reserva(
                cliente=cliente_carlos,
                servicio=laptop_portatil,
                horas=8,
                cantidad=3,
                con_iva=True,
                notas="Capacitación interna equipo de ventas"
            )
            catalogo_reservas.agregar(reserva)
            costo = reserva.confirmar()
            reserva_carlos = reserva
            resultado_ok("¡Reserva confirmada!")
            print(reserva.resumen())
        else:
            resultado_error("No se pudo crear la reserva: cliente o equipo no disponibles")

    except (ReservaInvalidaError, CapacidadExcedidaError) as e:
        resultado_error(f"Reserva fallida: {e}")
    finally:
        log.debug("Main", "OP12 finalizada")

    separador()

    # ── OPERACIÓN 13: Reserva de asesoría corporativa ─────────────────────────
    titulo("OP 13: Asesoría tecnológica con descuento corporativo (Lucía)", nivel=2)
    reserva_lucia = None
    try:
        if cliente_lucia and asesoria_tech:
            reserva = Reserva(
                cliente=cliente_lucia,
                servicio=asesoria_tech,
                horas=6,
                con_iva=True,
                descuento_porcentaje=5.0,
                notas="Consultoría inicial de transformación digital"
            )
            catalogo_reservas.agregar(reserva)
            costo = reserva.confirmar(es_cliente_corporativo=True)  # +12% descuento corporativo
            reserva_lucia = reserva
            resultado_ok("¡Reserva confirmada!")
            print(reserva.resumen())
        else:
            resultado_error("No se pudo crear la reserva")

    except (ReservaInvalidaError, SoftwareFJError) as e:
        resultado_error(f"Reserva fallida: {e}")
    finally:
        log.debug("Main", "OP13 finalizada")

    separador()

    # ── OPERACIÓN 14: Intentar confirmar una reserva ya confirmada ────────────
    titulo("OP 14: Doble confirmación de reserva (inválido)", nivel=2)
    try:
        if reserva_ana:
            resultado_ok(f"Estado actual: {reserva_ana.estado}")
            reserva_ana.confirmar()  # ← Ya está CONFIRMADA, debe lanzar excepción
            resultado_ok("Reserva confirmada dos veces (no debería ocurrir)")
        else:
            resultado_error("No hay reserva disponible para esta prueba")
    except OperacionNoPermitidaError as e:
        resultado_error(f"Capturado OperacionNoPermitidaError: {e}")
        log.advertencia("Main", "OP14: Doble confirmación rechazada correctamente", e)
    finally:
        log.debug("Main", "OP14 finalizada")

    separador()

    # ── OPERACIÓN 15: Cancelar una reserva existente ──────────────────────────
    titulo("OP 15: Cancelación de reserva (Carlos Ríos)", nivel=2)
    try:
        if reserva_carlos:
            print(f"      Estado antes: {reserva_carlos.estado}")
            reserva_carlos.cancelar(motivo="CLIENTE", descripcion_extra="Agenda reorganizada")
            resultado_ok(f"Reserva cancelada. Estado: {reserva_carlos.estado}")
            resultado_ok(f"Unidades devueltas: {laptop_portatil.unidades_disponibles} disponibles")
        else:
            resultado_error("No hay reserva de Carlos disponible")
    except OperacionNoPermitidaError as e:
        resultado_error(f"Error: {e}")
    finally:
        log.debug("Main", "OP15 finalizada")

    separador()

    # ── OPERACIÓN 16: Reserva con exceso de horas ─────────────────────────────
    titulo("OP 16: Asesoría con duración excesiva (12h, máximo 8h)", nivel=2)
    try:
        if cliente_ana and asesoria_tech:
            reserva_mala = Reserva(
                cliente=cliente_ana,
                servicio=asesoria_tech,
                horas=12,   # ← Excede el máximo de 8h por sesión
                notas="Sesión inválida"
            )
            catalogo_reservas.agregar(reserva_mala)
            reserva_mala.confirmar()
            resultado_ok("Reserva confirmada (no debería ocurrir)")
        else:
            resultado_error("No hay recursos disponibles para esta prueba")
    except (ReservaInvalidaError, ServicioNoDisponibleError) as e:
        resultado_error(f"Capturado: {e}")
        log.advertencia("Main", "OP16: Horas excesivas rechazadas correctamente", e)
    except SoftwareFJError as e:
        resultado_error(f"Error sistema: {e}")
    finally:
        log.debug("Main", "OP16 finalizada")

    separador()

    # ── OPERACIÓN 17: Completar reserva de asesoría ───────────────────────────
    titulo("OP 17: Completar reserva de asesoría de Lucía", nivel=2)
    try:
        if reserva_lucia and reserva_lucia.estado == "CONFIRMADA":
            print(f"      Estado antes: {reserva_lucia.estado}")
            reserva_lucia.completar()
            resultado_ok(f"Reserva completada. Estado: {reserva_lucia.estado}")
            resultado_ok(f"Puntos de fidelidad de Lucía: {cliente_lucia.puntos_fidelidad}")
        else:
            estado = reserva_lucia.estado if reserva_lucia else "Sin reserva"
            resultado_error(f"Reserva no disponible para completar. Estado: {estado}")
    except (OperacionNoPermitidaError, ReservaInvalidaError) as e:
        resultado_error(f"Error: {e}")
    finally:
        log.debug("Main", "OP17 finalizada")

    separador()

    # ── OPERACIÓN 18: Stock insuficiente de equipos ───────────────────────────
    titulo("OP 18: Reserva de 20 laptops (solo hay 8 disponibles)", nivel=2)
    try:
        if cliente_lucia and laptop_portatil:
            reserva_stock = Reserva(
                cliente=cliente_lucia,
                servicio=laptop_portatil,
                horas=2,
                cantidad=20,   # ← Excede el stock disponible (8)
                notas="Solicitud de gran volumen"
            )
            catalogo_reservas.agregar(reserva_stock)
            reserva_stock.confirmar()
            resultado_ok("Reserva confirmada (no debería ocurrir)")
    except (ReservaInvalidaError, CapacidadExcedidaError) as e:
        resultado_error(f"Capturado: {e}")
        log.advertencia("Main", "OP18: Stock insuficiente rechazado correctamente", e)
    finally:
        log.debug("Main", "OP18 finalizada")

    separador()

    # ── OPERACIÓN 19: Verificar cálculos de costo (polimorfismo) ─────────────
    titulo("OP 19: Demostración polimorfismo — Cálculos de costo múltiples variantes", nivel=2)
    try:
        servicios_demo = [s for s in [sala_principal, laptop_portatil, asesoria_tech] if s]
        for srv in servicios_demo:
            print(f"\n      [{srv.__class__.__name__}] {srv.nombre}")
            c1 = srv.calcular_costo(2, con_iva=True, descuento_porcentaje=0)
            c2 = srv.calcular_costo(2, con_iva=False, descuento_porcentaje=0)
            c3 = srv.calcular_costo(2, con_iva=True, descuento_porcentaje=20)
            resultado_ok(f"2h con IVA:          ${c1:>12,.2f}")
            resultado_ok(f"2h sin IVA:          ${c2:>12,.2f}")
            resultado_ok(f"2h con IVA y 20%dto: ${c3:>12,.2f}")
    except (CalculoInconsistenteError, ParametroInvalidoError) as e:
        resultado_error(f"Error en cálculo: {e}")
    finally:
        log.debug("Main", "OP19 finalizada")

    separador()

    # ── OPERACIÓN 20: Cálculo con descuento fuera de rango ───────────────────
    titulo("OP 20: Cálculo con descuento inválido (75% — fuera del rango 0-50%)", nivel=2)
    try:
        if sala_principal:
            costo_invalido = sala_principal.calcular_costo(3, descuento_porcentaje=75.0)
            resultado_ok(f"Costo calculado: ${costo_invalido:,.2f} (no debería ocurrir)")
    except CalculoInconsistenteError as e:
        resultado_error(f"Capturado CalculoInconsistenteError: {e}")
        log.advertencia("Main", "OP20: Descuento fuera de rango rechazado", e)
    finally:
        log.debug("Main", "OP20 finalizada")

    # ══════════════════════════════════════════════════════════════════════════
    # RESUMEN FINAL DEL SISTEMA
    # ══════════════════════════════════════════════════════════════════════════
    titulo("RESUMEN FINAL DEL SISTEMA", nivel=1)

    print(f"  Clientes registrados    : {catalogo_clientes.total}")
    print(f"  Servicios registrados   : {catalogo_servicios.total}")
    print(f"  Reservas totales        : {catalogo_reservas.total}")

    # Estadísticas por estado
    for estado in ("PENDIENTE", "CONFIRMADA", "COMPLETADA", "CANCELADA", "ERROR"):
        cant = len(catalogo_reservas.listar_por_estado(estado))
        if cant > 0:
            print(f"    Reservas {estado:12s}: {cant}")

    print(f"\n  Servicios disponibles:")
    for srv in catalogo_servicios.listar_disponibles():
        print(f"    • {srv.describir()}")

    print(f"\n  Estado de clientes:")
    for cli in catalogo_clientes.listar_activos():
        print(f"    • {cli.describir()}")

    print(f"\n  Archivo de logs: sistema_softwarefj.log")

    titulo("Simulación completada exitosamente — Software FJ", nivel=1)
    log.info("Main", "═══ Simulación completada. Sistema estable. ═══")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.advertencia("Main", "Ejecución interrumpida por el usuario")
        print("\n\n  [Sistema detenido por el usuario]")
        sys.exit(0)
    except Exception as e:
        log.critico("Main", f"Error crítico no controlado: {e}", e)
        print(f"\n  [ERROR CRÍTICO] {e}")
        sys.exit(1)
