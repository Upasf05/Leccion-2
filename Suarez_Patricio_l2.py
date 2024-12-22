import tkinter as tk #Librería Tkinter para interfaces gráficas
from tkinter import messagebox, simpledialog #Importar ventanas de mensaje


#Clases de cuenta con distintos tipos
class Cuenta: #Clase-objeto para una cuenta bancaria
    def __init__(self, titular, numero_cuenta, saldo_inicial=0):Método para configurar y activar valores
        self.titular = titular #Usuario titular de la cuenta
        self.numero_cuenta = numero_cuenta #Número de cuenta
        self.saldo = saldo_inicial #Saldo inicial de la cuenta

    def depositar(self, monto): #Método para depósito
        if monto <= 0: #Función if
            return "Error: Monto no válido." #Valor no válido si es negativo
        self.saldo += monto #Ejecutar la operación depósito
        return "Depósito realizado exitosamente." #Mensaje de que se ha completado la operación

    def retirar(self, monto): #Método para retiro
        if monto <= 0: #Función if
            return "Error: Monto no válido." #Valor no válido si es negativo
        if monto > self.saldo: #Error si el monto del usuario es menor a la cantidad a retirar
            return "Error: Fondos insuficientes."
        self.saldo -= monto #Ejecutar la operación retiro
        return "Retiro realizado exitosamente." #Mensaje de que se ha completado la operación

    def consultar_saldo(self): #Método para consultar el saldo
        return self.saldo #Función de return para devolver un valor existente


class CuentaCorriente(Cuenta): #Clase para tipo de cuenta corriente
    def __init__(self, titular, numero_cuenta, saldo_inicial=0): #Método para configurar la clase
        super().__init__(titular, numero_cuenta, saldo_inicial) #Llamar y activar el método en la clase


class CuentaAhorros(Cuenta): #Clase para cuenta de ahorros
    def __init__(self, titular, numero_cuenta, saldo_inicial=0, tasa_interes=0.02): #Método para configurar la clase
        super().__init__(titular, numero_cuenta, saldo_inicial) #Llamar y activar el método en la clase
        self.tasa_interes = tasa_interes #Definir valor

    def calcular_intereses(self): #Función para intereses
        intereses = self.saldo * self.tasa_interes #Definir valor de intereses
        self.saldo += intereses #Cómo los intereses influyen en el saldo
        return intereses #Devolver valor de intereses


class CuentaPlazoFijo(Cuenta): #Clase para cuenta de plazo fijo
    def __init__(self, titular, numero_cuenta, saldo_inicial=0, plazo=30, tasa_interes=0.05): #Método para configuar la clase
        super().__init__(titular, numero_cuenta, saldo_inicial) #Llamar y activar el método en la clase
        self.plazo = plazo #Definir el valor de plazo
        self.tasa_interes = tasa_interes #Definir el valor de la tasa de intereses


#Clase para manejar los usuarios
class Usuario: #Clase para un usuario cuando inicia sesión
    def __init__(self, nombre, password): #Método para configurar la clase
        self.nombre = nombre #Definir variable nombre
        self.password = password #Definir variable contraseña
        self.cuentas = []  # Lista de cuentas asociadas al usuario


#Clase global para manejar datos
class Data:#Clase que almacena información de usuarios
    usuarios = []  # Lista para almacenar usuarios registrados
    cuenta_actual = 1000  # Inicializa el número de cuenta


#Clase principal de la aplicación
class AppBanco(tk.Tk): #Clase con las funciones de interfaz
    def __init__(self): #Método para configurar la clase
        super().__init__() #Llamar y activar el método
        self.title("BANCO COMPU SUR") #Título al inicio de la ventana
        self.geometry("400x400") #Resolución de la ventana
        self.configure(bg='blue') #Color de fondo
        self.current_frame = None #Para mantener una ventana en ejecución
        self.usuario_actual = None #Usuario que ha iniciado sesión
        self.show_iniciar_sesion() #Mostrar la ventana de inicio de sesión al iniciar el programa

    def show_iniciar_sesion(self): #Método para el inicio de sesión
        if self.current_frame: #Ajustar la ventana en ejecución
            self.current_frame.destroy() #Destruir la función una vez se ajustó la ventana
        self.current_frame = IniciarSesion(self) #Importar la interfaz de la clase IniciarSesion 
        self.current_frame.pack() #Colocar los elementos de la clase importada

    def show_registrar_usuario(self): #Método para el registro de usuario
        if self.current_frame: #Ajustar la ventana en ejecución
            self.current_frame.destroy() #Destruir la función una vez se ajustó la ventana
        self.current_frame = RegistrarUsuario(self) #Importar la interfaz de la clase RegistrarUsuario
        self.current_frame.pack() #Colocar los elementos de la clase importada

    def show_operaciones_bancarias(self, usuario): #Método para la ventana principal del programa
        if self.current_frame: #Ajustar la ventana en ejecución 
            self.current_frame.destroy() #Destruir la función una vez se ajustó la ventana
        self.current_frame = OperacionesBancarias(self, usuario) #Importar la interfaz de la clase Operaciones bancarias
        self.current_frame.pack() #Colocar los elementos de la clase importada


#Ventana de inicio de sesión
class IniciarSesion(tk.Frame): #Clase para la ventana de inicio de sesión
    def __init__(self, parent): #Método para configurar la clase
        super().__init__(parent) #Llamar y activar el método
        self.parent = parent
        self.configure(bg='blue') #Color de fondo de la ventana

        tk.Label(self, text="BANCO COMPU SUR", bg='blue', fg='white', font=("Arial", 16, "bold")).pack(pady=10) #Título al inicio de la ventana
        tk.Label(self, text="Usuario:", bg='blue', fg='white') .pack(pady=5)#Texto de Usuario
        self.usuario_entry = tk.Entry(self) #Leer el nombre de usuario
        self.usuario_entry.pack(pady=5)

        tk.Label(self, text="Contraseña:", bg='blue', fg='white') .pack(pady=5) #Texto de Contraseña 
        self.password_entry = tk.Entry(self, show="*") #Leer la contraseña y cubrirla mientras se introduce
        self.password_entry.pack(pady=5)

        tk.Button(self, text="Iniciar Sesión", bg='green', fg='white', command=self.inicio_sesion).pack(pady=10) #Botón de inicio de sesión
        tk.Button(self, text="Registrar Usuario", bg='green', fg='white', command=parent.show_registrar_usuario).pack(pady=5) #Botón de registro de usuario

    def inicio_sesion(self): #Método para ejecutar el inicio de sesión
        usuario = self.usuario_entry.get().strip() #Usuario introducido
        password = self.password_entry.get().strip() #Contraseña introducida

        #Buscar el usuario por nombre y contraseña
        usuario_actual = next((user for user in Data.usuarios if user.nombre == usuario and user.password == password), None)

        if usuario_actual: #Verificar si el usuario y contraseña introducidos son correctos o no
            self.parent.usuario_actual = usuario_actual
            self.parent.show_operaciones_bancarias(usuario_actual)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")


#Ventana de registro de usuario
class RegistrarUsuario(tk.Frame): #Clase para la ventana de registro
    def __init__(self, parent): #Método para configurar la clase, repetir los mismos parámetros que en la anterior ventana
        super().__init__(parent)
        self.parent = parent
        self.configure(bg='blue')

        #Repetir la misma coloración de botones de la anterior ventana
        tk.Label(self, text="BANCO COMPU SUR", bg='blue', fg='white', font=("Arial", 16, "bold")).pack(pady=10) #Título al inicio de la ventana
        tk.Label(self, text="Nombre de Usuario:", bg='blue', fg='white').pack(pady=5)
        self.nombre_entry = tk.Entry(self) #Registrar nombre de usuario
        self.nombre_entry.pack(pady=5)

        tk.Label(self, text="Contraseña:", bg='blue', fg='white').pack(pady=5)
        self.password_entry = tk.Entry(self, show="*") #Registrar y cubrir contraseña
        self.password_entry.pack(pady=5)

        tk.Label(self, text="Saldo Inicial (en $):", bg='blue', fg='white').pack(pady=5)
        self.saldo_entry = tk.Entry(self) #Definir el saldo inicial
        self.saldo_entry.pack(pady=5)

        tk.Label(self, text="Tipo de Cuenta:", bg='blue', fg='white').pack(pady=5) #Definir el tipo de cuenta
        self.tipo_cuenta = tk.StringVar(value="Corriente") #Menú despegable, tendrá tres tipos de cuenta, la corriente será por defecto
        opcion_menu = tk.OptionMenu(self, self.tipo_cuenta, "Corriente", "Ahorros", "Plazo Fijo") #Tipos de cuenta
        opcion_menu.config(bg='green', fg='white', activebackground='darkgreen', activeforeground='white') #Colorear el menú despegable
        opcion_menu['menu'].config(bg='green', fg='white') #Completar la coloración
        opcion_menu.pack(pady=5)

        tk.Button(self, text="Registrar", bg='green', fg='white', command=self.registrar_usuario).pack(pady=10) #Repetir la coloración de botones ya usada
        tk.Button(self, text="Volver", bg='green', fg='white', command=parent.show_iniciar_sesion).pack(pady=5)

    def registrar_usuario(self): #Método para ejecutar el registro de un usuario
        nombre = self.nombre_entry.get().strip() #Registrar los datos introducidos
        password = self.password_entry.get().strip()
        saldo = self.saldo_entry.get().strip()
        tipo = self.tipo_cuenta.get()

        if not nombre or not password or not saldo: #Verificar que todos los campos estén rellenados
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return

        try: #Impedir registro de un saldo negativo
            saldo = float(saldo)
            if saldo < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "El saldo inicial debe ser un número válido no negativo")
            return

        # Crear un nuevo usuario y asignar la cuenta
        nuevo_usuario = Usuario(nombre, password) #Crear el usuario con el nombre y contraseña elegidos

        numero_cuenta = Data.cuenta_actual #Otorgar un número de cuenta según el orden de registro
        Data.cuenta_actual += 1 #Si el primer usuario creado en el programa el número de cuenta será 1

        if tipo == "Corriente": #Asignar el tipo de cuenta
            cuenta = CuentaCorriente(nombre, numero_cuenta, saldo)
        elif tipo == "Ahorros":
            cuenta = CuentaAhorros(nombre, numero_cuenta, saldo)
        else:
            cuenta = CuentaPlazoFijo(nombre, numero_cuenta, saldo)

        nuevo_usuario.cuentas.append(cuenta) #Agregar la cuenta al programa
        Data.usuarios.append(nuevo_usuario) #Almacenar los datos

        messagebox.showinfo( #Mensaje de registro exitoso
            "Registro",
            f"Usuario registrado exitosamente\nNúmero de cuenta: {numero_cuenta}\nSaldo inicial: ${saldo:.2f}\nTipo de cuenta: {tipo}",
        )
        self.parent.show_iniciar_sesion() #Devolver a la ventana de inicio de sesión


#Ventana de operaciones bancarias
class OperacionesBancarias(tk.Frame):
    def __init__(self, parent, usuario):#Método para configurar la clase
        super().__init__(parent) #Llamar y activar el método
        self.parent = parent
        self.usuario = usuario #Colocar al usuario
        self.configure(bg='blue') #Repetir el color de fondo como en las anteriores ventanas

        tk.Label(self, text="BANCO COMPU SUR", bg='blue', fg='white', font=("Arial", 16, "bold")).pack(pady=10) #Título
        tk.Label(self, text=f"Bienvenido, {self.usuario.nombre}", bg='blue', fg='white').pack(pady=10) #Saludar al usuario

        self.saldo_label = tk.Label(self, text=f"Saldo actual: ${self.usuario.cuentas[0].consultar_saldo():.2f}", bg='blue', fg='white') #Mostrar saldo del usuario
        self.saldo_label.pack(pady=10)

        #Botones de acciones 
        tk.Button(self, text="Depositar", bg='green', fg='white', command=self.depositar).pack(pady=5) #Depósito
        tk.Button(self, text="Retirar", bg='green', fg='white', command=self.retirar).pack(pady=5) #Retiro
        tk.Button(self, text="Transferir", bg='green', fg='white', command=self.transferir).pack(pady=5) #Transferencia
        tk.Button(self, text="Cerrar sesión", bg='green', fg='white', command=self.cerrar_sesion).pack(pady=10) #Salir de la cuenta

    def actualizar_saldo(self): #Acción para actualizar el saldo tras cada acción
        saldo = self.usuario.cuentas[0].consultar_saldo()
        self.saldo_label.config(text=f"Saldo actual: ${saldo:.2f}")

    def consultar_saldo(self): #Acción que muestra el saldo a partir de la acción de arriba
        self.mostrar_factura("Consulta de Saldo", "Consulta realizada exitosamente.")
        self.actualizar_saldo()

    def depositar(self): #Método o acción para depositar
        self.transaccion("Depositar", "Cantidad a depositar:")

    def retirar(self): #Método o acción para retirar
        self.transaccion("Retirar", "Cantidad a retirar:")

    def transferir(self): #Acción para tranferir a otra cuenta
        ventana = tk.Toplevel(self)
        ventana.title("Transferencia")
        ventana.geometry("300x250")

        tk.Label(ventana, text="ID de la cuenta destino:").pack(pady=5) #ID de la cuenta a la que se quiere transferir 
        id_entry = tk.Entry(ventana)
        id_entry.pack(pady=5)

        tk.Label(ventana, text="Cantidad a transferir:").pack(pady=5) #Cantidad que se pasará a otra cuenta
        monto_entry = tk.Entry(ventana)
        monto_entry.pack(pady=5)

        def realizar_transferencia(): #Método para transferir
            try:
                cuenta_destino = int(id_entry.get())
                monto = float(monto_entry.get())

                # Buscar cuenta de destino
                cuenta_origen = self.usuario.cuentas[0]
                if cuenta_destino == cuenta_origen.numero_cuenta: #Evitar transferencias a una misma cuenta
                    raise ValueError("No se puede transferir a la misma cuenta.")

                cuenta_destino = next(
                    (cuenta for cuenta in Data.usuarios[cuenta_destino].cuentas if cuenta.numero_cuenta == cuenta_destino),
                    None
                )
                if cuenta_destino: #Verificar si existe la cuenta de destino
                    resultado = cuenta_origen.retirar(monto)
                    if "Error" in resultado:
                        messagebox.showerror("Error", resultado)
                    else:
                        cuenta_destino.depositar(monto) #Realizar la transferencia
                        messagebox.showinfo("Transferencia", "Transferencia realizada con éxito.") #Transferencia existosa si la cuenta existe y el monto es suficiente
                    ventana.destroy()
                    self.actualizar_saldo() #Actualizar el saldo después de la transferencia
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

        tk.Button(ventana, text="Realizar Transferencia", command=realizar_transferencia).pack(pady=10) #Botón para ejecutar la transferencia

    def mostrar_factura(self, titulo, mensaje): #Mostrar factura tras una operación
        messagebox.showinfo(titulo, mensaje)

    def transaccion(self, titulo, mensaje): #Método para transacciones (dépositos y retiros)
        ventana = tk.Toplevel(self)
        ventana.title(titulo)
        ventana.geometry("300x200") #Tamaño de la ventana

        tk.Label(ventana, text=mensaje).pack(pady=5)
        monto_entry = tk.Entry(ventana)
        monto_entry.pack(pady=5)

        def realizar_transaccion(): #Método para ejecutar las transacciones
            try:
                monto = float(monto_entry.get())
                if monto <= 0: #Evitar la introducción de valores negativos
                    raise ValueError("El monto debe ser mayor que cero")
                cuenta_origen = self.usuario.cuentas[0]
                if titulo == "Depositar": #Distinguir los tipos de operación según el botón pulsado en el menú OperacionesBancarias
                    cuenta_origen.depositar(monto)
                else:
                    cuenta_origen.retirar(monto)
                messagebox.showinfo("Éxito", f"{titulo} realizado con éxito")
                ventana.destroy()
                self.actualizar_saldo()  # Actualizar el saldo después de la transacción
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

        tk.Button(ventana, text=titulo, command=realizar_transaccion).pack(pady=10)

    def cerrar_sesion(self): #Método para salir de una cuenta
        self.parent.show_iniciar_sesion()

if __name__ == "__main__": #Llamar y activar el programa
    app = AppBanco()
    app.mainloop()
