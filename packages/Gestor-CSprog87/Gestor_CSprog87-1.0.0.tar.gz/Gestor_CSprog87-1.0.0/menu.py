import os
import helpers
import database as db

def iniciar():
    """Inicializador del menu del gestor"""
    while True:
        helpers.limpiar_pantalla()

        print("=================================")
        print(" Bienvenido al Gestor [CSprog87] ")
        print("=================================")
        print("[1] Listar los clientes          ")
        print("[2] Buscar un cliente            ")
        print("[3] Añadir un cliente            ")
        print("[4] Modificar un cliente         ")
        print("[5] Borrar un cliente            ")
        print("[6] Cerrar el Gestor             ")
        print("=================================")

        opcion = input("> ")
        helpers.limpiar_pantalla()

        if opcion == "1":
            print("Listando los clientes...\n")
            for cliente in db.Clientes.lista:
                print(cliente)
                
        elif opcion == "2":
            print("Buscando un cliente...\n")
            dni = helpers.leer_texto(3, 3, "DNI (2 INT 1 CHAR)").upper()
            cliente = db.Clientes.buscar(dni)
            print(cliente) if cliente else print ("Cliente no encontrado")                
                
        elif opcion == "3":
            print("Añadiendo un cliente...\n")            
            dni = None
            while True:
                dni = helpers.leer_texto(3, 3, "DNI (2 INT 1 CHAR)").upper()
                if helpers.dni_valido(dni,db.Clientes.lista):
                    break
                
            nombre = helpers.leer_texto(2, 30, "NOMBRE (2 A 30 CHAR)").capitalize()
            apellido = helpers.leer_texto(2, 30, "APELLIDO (2 A 30 CHAR)").capitalize()
            db.Clientes.crear(dni, nombre, apellido)
            print("Cliente añadido correctamente")
            
        elif opcion == "4":
            print("Modificando un cliente...\n")
            dni = helpers.leer_texto(3, 3, "DNI (2 INT 1 CHAR)").upper()
            cliente = db.Clientes.buscar(dni)
            if cliente:
                nombre = helpers.leer_texto(2, 30, f"NOMBRE (2 A 30 CHAR) [{cliente.nombre}]").capitalize()
                apellido = helpers.leer_texto(2, 30, f"APELLIDO (2 A 30 CHAR)[{cliente.apellido}]").capitalize()
                db.Clientes.modificar(cliente.dni, nombre, apellido)
                print("Cliente modificado correctamente")
            else:
                print("Cliente no encotrado") 
            
        elif opcion == "5":
            print("Borrando un cliente...\n")
            dni = helpers.leer_texto(3, 3, "DNI (2 INT 1 CHAR)").upper()
            print("Cliente borrado") if db.Clientes.borrar(dni) else print("Cliente no encontrado")

        elif opcion == "6":
            print("Saliendo...\n")
            break
        input("\nPresiona ENTER para continuar...")

        

    