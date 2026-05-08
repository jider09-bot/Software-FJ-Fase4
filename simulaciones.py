def main():
    print("=== SIMULACIONES SOFTWARE FJ ===")

    # 1️⃣ Cliente válido
    try:
        c1 = Cliente(1, "Juan Perez", "12345678")
        print("1 OK:", c1.mostrar_detalles())
    except Exception as e:
        print("1 ERROR:", e)

    # 2️⃣ Cliente inválido (documento corto)
    try:
        c2 = Cliente(2, "Error Cliente", "123")
        print("2 OK:", c2.mostrar_detalles())
    except Exception as e:
        print("2 ERROR:", e)

    # 3️⃣ Servicio válido (Sala)
    try:
        s1 = ServicioSala(1, "Sala VIP", 50000, 10)
        print("3 OK:", s1.mostrar_detalles())
    except Exception as e:
        print("3 ERROR:", e)

    # 4️⃣ Servicio con duración inválida
    try:
        total = s1.calcular_costo_total(-2)
        print("4 OK:", total)
    except Exception as e:
        print("4 ERROR:", e)

    # 5️⃣ Reserva válida
    try:
        r1 = Reserva(c1, s1, 2)
        r1.confirmar()
        print("5 OK: Reserva creada")
    except Exception as e:
        print("5 ERROR:", e)

    # 6️⃣ Reserva con duración negativa
    try:
        r2 = Reserva(c1, s1, -1)
        r2.confirmar()
    except Exception as e:
        print("6 ERROR:", e)

    # 7️⃣ Servicio no disponible
    try:
        s1.disponible = False
        r3 = Reserva(c1, s1, 1)
        r3.confirmar()
    except Exception as e:
        print("7 ERROR:", e)
    finally:
        s1.disponible = True  # lo dejamos usable otra vez

    # 8️⃣ Pago correcto
    try:
        r1.procesar_pago()
        print("8 OK: Pago realizado")
    except Exception as e:
        print("8 ERROR:", e)

    # 9️⃣ Cancelación de reserva
    try:
        r1.cancelar()
        print("9 OK: Reserva cancelada")
    except Exception as e:
        print("9 ERROR:", e)

    # 🔟 Error forzado (cliente y servicio None)
    try:
        r4 = Reserva(None, None, 1)
        r4.confirmar()
    except Exception as e:
        print("10 ERROR:", e)

    print("=== FIN DE SIMULACIONES ===")


if __name__ == "__main__":
    main()