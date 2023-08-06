import re
import os
import platform

def limpiar_pantalla():
    """Limpia la pantalla del sistema"""
    os.system('cls') if platform.system() == 'Windows' else os.system('clear')
    
def leer_texto(longitud_min=0, longitud_max=100, mensaje=None):
    """Funcion que permite leer texto introducido con verificador de longitud de DNI"""
    print(mensaje) if mensaje else None
    while True:
        texto = input("> ")
        if len(texto) < longitud_min or len(texto) > longitud_max:
            print("Longitud DNI incorrecta")           
        elif len(texto) >= longitud_min and len(texto) <= longitud_max:
            return texto

def dni_valido(dni, lista):
    """Verificador de formato de texto para DNI y si DNI ya existe"""
    if not re.match('[0-9]{2}[A-Z]$',dni):
        print("Formato DNI incorrecto")
        return False
    for cliente in lista:
        if cliente.dni == dni:
            print("DNI pertenece a otro cliente")
            return False        
    return True

