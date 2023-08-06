import helpers 
import database as db
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel, WARNING

class CenterMixin:
    """Clase que construye la ventana de interfaz grafica"""
    def CentrarVentana(self):
        """Metodo para centrar la ventana"""
        self.update()
        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int(ws/2 - w/2)
        y = int(hs/2 - h/2)        
        self.geometry(f"{w}x{h}+{x}+{y}")

class VentanaCrearCliente(Toplevel, CenterMixin):
    """Clase que construye la ventana para crear clientes"""
    def __init__(self, parent):
        """Metodo constructor de la ventana"""
        super().__init__(parent)
        self.title('Crear Cliente')
        self.build()
        self.CentrarVentana()
        self.transient(parent)
        self.grab_set()

    def build(self):
        """Metodo para construir la tabla de clientes en interfaz grafica"""
        marco=Frame(self)
        marco.pack(padx=20, pady=10)

        Label(marco, text='DNI (2 Int 1 Upper Char)').grid(row=0,column=0)
        Label(marco, text='Nombre (2 - 30 Char)').grid(row=0,column=1)
        Label(marco, text='Apellido (2 - 30 Char)').grid(row=0,column=2)

        dni = Entry(marco)
        dni.grid(row=1,column=0)
        dni.bind('<KeyRelease>', lambda event: self.validar(event,0))
        nombre = Entry(marco)
        nombre.grid(row=1,column=1)
        nombre.bind('<KeyRelease>', lambda event: self.validar(event,1))
        apellido = Entry(marco)
        apellido.grid(row=1,column=2)
        apellido.bind('<KeyRelease>', lambda event: self.validar(event,2))

        frame = Frame(self)
        frame.pack(pady=10)

        crear = Button(frame, text='Crear', command=self.crear_cliente)
        crear.configure(state=DISABLED)
        crear.grid(row=0, column=0)
        Button(frame,text='Cancelar',command=self.cerrar).grid(row=0, column=1)

        self.validaciones = [0, 0, 0]
        self.crear = crear
        self.nombre = nombre
        self.dni = dni
        self.apellido = apellido


    def crear_cliente(self):
        """Metodo de clase para crear clientes"""
        self.master.tabla.insert(
                parent='', index='end', iid=self.dni.get(),
                values=(self.dni.get(), self.nombre.get(), self.apellido.get()))
        db.Clientes.crear(self.dni.get(), self.nombre.get(), self.apellido.get())
        self.cerrar()

    def cerrar(self):
        """Metodo de clase para cerrar ventana"""
        self.destroy()
        self.update()
    
    def validar(self,event,index):
        """Metodo de clase para validar clientes"""
        valor = event.widget.get()
        valido = helpers.dni_valido(valor, db.Clientes.lista) if index == 0 \
            else (valor.isalpha() and len(valor) >= 2 and len(valor) <= 30)
        event.widget.configure({'bg':'Green' if valido else 'Red'})

        self.validaciones[index] = valido
        self.crear.config(state=NORMAL if self.validaciones == [1, 1, 1] else DISABLED)

class VentanaEditarCliente(Toplevel, CenterMixin):
    """Clase que construye la ventana para modificar clientes"""
    def __init__(self, parent):
        """Metodo constructor de la ventana"""
        super().__init__(parent)
        self.title('Actualizar Cliente')
        self.build()
        self.CentrarVentana()
        self.transient(parent)
        self.grab_set()

    def build(self):
        """Metodo para construir la tabla de clientes en interfaz grafica"""
        marco=Frame(self)
        marco.pack(padx=20, pady=10)

        Label(marco, text='DNI (--No Editable--)').grid(row=0,column=0)
        Label(marco, text='Nombre (2 - 30 Char)').grid(row=0,column=1)
        Label(marco, text='Apellido (2 - 30 Char)').grid(row=0,column=2)

        dni = Entry(marco)
        dni.grid(row=1,column=0)        
        nombre = Entry(marco)
        nombre.grid(row=1,column=1)
        nombre.bind('<KeyRelease>', lambda event: self.validar(event,0))
        apellido = Entry(marco)
        apellido.grid(row=1,column=2)
        apellido.bind('<KeyRelease>', lambda event: self.validar(event,1))

        cliente = self.master.tabla.focus() 
        campos = self.master.tabla.item(cliente, 'values')
        dni.insert(0,campos[0])
        dni.config(state=DISABLED)
        nombre.insert(0,campos[1])
        apellido.insert(0,campos[2])


        frame = Frame(self)
        frame.pack(pady=10)

        actualizar = Button(frame, text='Actualizar', command=self.actualizar_cliente)        
        actualizar.grid(row=0, column=0)
        Button(frame,text='Cancelar',command=self.cerrar).grid(row=0, column=1)

        self.validaciones = [1, 1]
        self.actualizar = actualizar
        self.nombre = nombre
        self.dni = dni
        self.apellido = apellido


    def actualizar_cliente(self):
        """Metodo para actualizar clientes"""
        cliente = self.master.tabla.focus()
        self.master.tabla.item(cliente, values=(
            self.dni.get(), self.nombre.get(), self.apellido.get()))
        db.Clientes.modificar(self.dni.get(), self.nombre.get(), self.apellido.get())
        self.cerrar()

    def cerrar(self):
        self.destroy()
        self.update()
    
    def validar(self,event,index):
        valor = event.widget.get()
        valido = (valor.isalpha() and len(valor) >= 2 and len(valor) <= 30)
        event.widget.configure({'bg':'Green' if valido else 'Red'})

        self.validaciones[index] = valido
        self.actualizar.config(state=NORMAL if self.validaciones == [1, 1] else DISABLED)        

class VentanaPrincipal(Tk, CenterMixin):
    def __init__(self):
        super().__init__()
        self.title("Gestor de clientes [CSprog87]")
        self.build()
        self.CentrarVentana()
        

    def build(self):
        marco = Frame(self)
        marco.pack()
        
        tabla = ttk.Treeview(marco)
        tabla['columns'] = ('DNI', 'Nombre', 'Apellido')
        

        tabla.column('#0',width=0,stretch=NO)
        tabla.column('DNI', anchor=CENTER)
        tabla.column('Nombre', anchor=CENTER)
        tabla.column('Apellido', anchor=CENTER)

        tabla.heading('DNI', text='DNI', anchor=CENTER)
        tabla.heading('Nombre', text='Nombre', anchor=CENTER)
        tabla.heading('Apellido', text='Apellido', anchor=CENTER)

        scrollbar = Scrollbar(marco)
        scrollbar.pack(side=RIGHT, fill=Y)

        tabla['yscrollcommand'] = scrollbar.set

        for cliente in db.Clientes.lista:
            tabla.insert(
                parent='', index='end', iid=cliente.dni,
                values=(cliente.dni, cliente.nombre, cliente.apellido))
        tabla.pack()

        frame = Frame(self)
        frame.pack(pady=20)

        Button(frame, text='Crear', command=self.crear).grid(row=0, column=0)
        Button(frame, text='Modificar', command=self.editar).grid(row=0, column=1)
        Button(frame, text='Borrar', command=self.borrar).grid(row=0, column=2)

        self.tabla = tabla

    def borrar(self):
        cliente = self.tabla.focus()
        if cliente:
            campos = self.tabla.item(cliente, 'values')
            confirmar = askokcancel(
                title='Confirmar borrado',
                message=f'¿Borrar {campos[1]} {campos[2]}?',
                icon=WARNING)
            if confirmar:
                self.tabla.delete(cliente)
                db.Clientes.borrar(campos[0])
    
    def crear(self):
        VentanaCrearCliente(self)
    
    def editar(self):
        if self.tabla.focus():
            VentanaEditarCliente(self)

if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()

