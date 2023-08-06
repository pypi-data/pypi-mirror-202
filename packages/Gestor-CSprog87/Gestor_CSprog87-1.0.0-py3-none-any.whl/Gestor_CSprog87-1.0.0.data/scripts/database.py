import csv
import config

class Cliente:
    """Clase para definir la creacion de los parametros de los clientes"""
    
    def __init__(self, dni, nombre, apellido):
        """Constructor de clase"""        
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    def __str__(self):
        """Redefine str para la clase"""
        return f"({self.dni}) {self.nombre} {self.apellido}"
    
class Clientes:
    """Clase para crear la lista a partir del fichero con metodos de busqueda
    creacion, modificacion, borrado y guardado"""

    lista = []
    with open(config.DATABASE_PATH, newline='\n') as fichero:
        lector = csv.reader(fichero, delimiter=';')
        for dni, nombre, apellido in lector:
            cliente = Cliente(dni, nombre, apellido)
            lista.append(cliente)

    @staticmethod
    def buscar(dni):
        """Metodo de clase para buscar clientes"""
        for cliente in Clientes.lista:
            if cliente.dni == dni:
                return cliente
            
    @staticmethod
    def crear(dni, nombre, apellido):
        """Metodo de clase para crear clientes"""
        cliente = Cliente(dni, nombre, apellido)
        Clientes.lista.append(cliente)
        Clientes.guardar()
        return cliente
    
    @staticmethod
    def modificar(dni, nombre, apellido):
        """Metodo de clase para modificar clientes"""
        for indice,cliente in enumerate(Clientes.lista):
            if cliente.dni == dni:
                Clientes.lista[indice].nombre = nombre
                Clientes.lista[indice].apellido = apellido
                Clientes.guardar()
                return Clientes.lista[indice]
    
    @staticmethod
    def borrar(dni):
        """Metodo de clase para borrar clientes"""
        for indice,cliente in enumerate(Clientes.lista):
            if cliente.dni == dni:
                cliente = Clientes.lista.pop(indice) 
                Clientes.guardar()             
                return cliente
            
    @staticmethod
    def guardar():
        """Metodo de clase para guardar clientes"""
        with open(config.DATABASE_PATH, 'w',newline='\n') as fichero:
            escritor = csv.writer(fichero, delimiter=';')
            for cliente in Clientes.lista:
                escritor.writerow((cliente.dni, cliente.nombre, cliente.apellido))
