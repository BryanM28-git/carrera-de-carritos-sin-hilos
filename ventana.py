import tkinter as tk
from tkinter import ttk
from operaciones import Vehiculo, numvehiculos, colores


class Carrera:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Gran Premio de Vehículos")
        self.ventana.geometry("1050x860")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="gray15")

        self.inicio = 70
        self.meta = 930
        self.vueltas = 3
        self.apuesta = 1
        self.factor = 1.0
        self.encarrera = False
        self.timerverificacion = None

        self.configurarestilo()

        tk.Label(ventana, text="GRAN PREMIO DE VEHÍCULOS", font=("Arial", 22, "bold"), bg="gray15", fg="gold").pack(pady=8)

        panel = tk.Frame(ventana, bg="gray15")
        panel.pack(pady=4)

        tk.Label(panel, text="Vueltas:", font=("Arial", 11), bg="gray15", fg="whitesmoke").grid(row=0, column=0, padx=5)
        self.entradavueltas = tk.Entry(panel, width=6, justify="center")
        self.entradavueltas.insert(0, "3")
        self.entradavueltas.grid(row=0, column=1, padx=5)

        tk.Label(panel, text=f"Apuesta (1-{numvehiculos}):", font=("Arial", 11), bg="gray15", fg="whitesmoke").grid(row=0, column=2, padx=5)
        self.entradaapuesta = tk.Entry(panel, width=6, justify="center")
        self.entradaapuesta.insert(0, "1")
        self.entradaapuesta.grid(row=0, column=3, padx=5)

        self.botonconfigurar = tk.Button(panel, text="Configurar", command=self.configurar, width=11)
        self.botonconfigurar.grid(row=0, column=4, padx=8)

        self.botoniniciar = tk.Button(panel, text="Iniciar carrera", command=self.iniciar, width=13)
        self.botoniniciar.grid(row=0, column=5, padx=5)

        tk.Button(panel, text="Reiniciar", command=self.reiniciar, width=11).grid(row=0, column=6, padx=5)

        self.slider = tk.Scale(panel, from_=0.25, to=3.0, resolution=0.25, orient="horizontal", length=160, label="Velocidad del juego", bg="gray15", fg="whitesmoke", troughcolor="darkslategray", highlightthickness=0, command=self.cambiarfactor)
        self.slider.set(1.0)
        self.slider.grid(row=0, column=7, padx=10)

        self.info = tk.Label(self.ventana, font=("Arial", 11, "bold"), bg="gray15", fg="whitesmoke")
        self.info.pack(pady=3)
        self.actualizarinfo()

        self.mensaje = tk.Label(self.ventana, text="", font=("Arial", 12, "bold"), bg="gray15", fg="gold")
        self.mensaje.pack(pady=2)

        tk.Label(ventana, text="Resultados", font=("Arial", 14, "bold"), bg="gray15", fg="gold").pack(pady=3)

        marco = tk.Frame(ventana, bg="gray15")
        marco.pack()

        self.tabla = ttk.Treeview(marco, columns=("posicion", "vehiculo", "tiempo", "vueltas"), show="headings", height=4, style="Carrera.Treeview")
        for columna, texto, ancho in (("posicion", "Posición", 110), ("vehiculo", "Vehículo", 130), ("tiempo", "Tiempo", 130), ("vueltas", "Vueltas", 110)):
            self.tabla.heading(columna, text=texto)
            self.tabla.column(columna, width=ancho, anchor="center")

        scroll = ttk.Scrollbar(marco, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        self.tabla.pack(side="left")
        scroll.pack(side="right", fill="y")

        self.canvas = tk.Canvas(ventana, width=1000, height=480, bg="forestgreen", highlightthickness=2, highlightbackground="gold")
        self.canvas.pack(pady=10)
        self.dibujarpista()

        self.vehiculos = []
        for carril in range(numvehiculos):
            self.vehiculos.append(Vehiculo(self.canvas, self.altura(carril), carril + 1, colores[carril], self))

    def configurarestilo(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Carrera.Treeview", background="darkslategray", fieldbackground="darkslategray", foreground="whitesmoke", rowheight=22)
        estilo.configure("Carrera.Treeview.Heading", background="gold", foreground="black", font=("Arial", 10, "bold"))

    @staticmethod
    def altura(carril):
        return 45 + carril * 44

    def dibujarpista(self):

        for carril in range(numvehiculos):
            centro = self.altura(carril)
            color = "gray23" if carril % 2 == 0 else "gray27"
            self.canvas.create_rectangle(30, centro - 22, 970, centro + 22, fill=color, outline="")

        self.canvas.create_line(30, 23, 970, 23, fill="white", width=3)
        self.canvas.create_line(30, 463, 970, 463, fill="white", width=3)

        for carril in range(numvehiculos - 1):
            borde = self.altura(carril) + 22
            self.canvas.create_line(30, borde, 970, borde, fill="gold", dash=(10, 8))

        self.canvas.create_line(self.inicio, 23, self.inicio, 463, fill="white", width=4)
        self.canvas.create_text(self.inicio, 11, text="SALIDA", font=("Arial", 9, "bold"), fill="white")

        lado = 11
        filas = (463 - 23) // lado
        for fila in range(filas):
            for columna in range(2):
                color = "white" if (fila + columna) % 2 == 0 else "black"
                izquierda = self.meta - lado + columna * lado
                arriba = 23 + fila * lado
                self.canvas.create_rectangle(izquierda, arriba, izquierda + lado, arriba + lado, fill=color, outline="")
        self.canvas.create_text(self.meta, 11, text="LLEGADA", font=("Arial", 9, "bold"), fill="white")

        for carril in range(numvehiculos):
            self.canvas.create_text(15, self.altura(carril), text=str(carril + 1), font=("Arial", 11, "bold"), fill="white")

    def actualizarinfo(self):
        self.info.config(text=f"Vueltas: {self.vueltas}     " f"Apuesta: Vehículo {self.apuesta}")

    def mostrarmensaje(self, texto, color="gold"):
        self.mensaje.config(text=texto, fg=color)

    def cambiarfactor(self, valor):
        self.factor = float(valor)

    def configurar(self):
        try:
            vueltas = int(self.entradavueltas.get())
            apuesta = int(self.entradaapuesta.get())
        except ValueError:
            self.mostrarmensaje("Error: ingrese números válidos.", "tomato")
            return False

        if vueltas < 1:
            self.mostrarmensaje("Error: las vueltas deben ser mayores que 0.", "tomato")
            return False

        if apuesta < 1 or apuesta > numvehiculos:
            self.mostrarmensaje(f"Error: la apuesta debe estar entre 1 y {numvehiculos}.", "tomato")
            return False

        self.vueltas = vueltas
        self.apuesta = apuesta
        self.actualizarinfo()
        return True

    def limpiartabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

    def bloquearcontroles(self, bloquear):
        estado = "disabled" if bloquear else "normal"
        self.botoniniciar.config(state=estado)
        self.botonconfigurar.config(state=estado)
        self.entradavueltas.config(state=estado)
        self.entradaapuesta.config(state=estado)

    def iniciar(self):
        if self.encarrera:
            return
        if not self.configurar():
            return

        self.cancelarverificacion()
        self.limpiartabla()
        self.mostrarmensaje("")

        for vehiculo in self.vehiculos:
            vehiculo.reiniciar()

        self.encarrera = True
        self.bloquearcontroles(True)

        for vehiculo in self.vehiculos:
            vehiculo.iniciar()

        self.timerverificacion = self.ventana.after(200, self.verificarfin)

    def cancelarverificacion(self):
        if self.timerverificacion is not None:
            self.ventana.after_cancel(self.timerverificacion)
            self.timerverificacion = None

    def verificarfin(self):
        terminados = sum(1 for vehiculo in self.vehiculos if vehiculo.tiempofinal is not None)

        if terminados < len(self.vehiculos):
            self.timerverificacion = self.ventana.after(200, self.verificarfin)
            return

        self.timerverificacion = None
        self.encarrera = False
        self.bloquearcontroles(False)
        self.mostrarresultados()

        ganador = min(self.vehiculos, key=lambda vehiculo: vehiculo.tiempofinal)

        if ganador.numero == self.apuesta:
            self.mostrarmensaje(f"¡Ganaste! El vehículo {ganador.numero} llegó primero.", "lawngreen")
        else:
            self.mostrarmensaje(f"Perdiste la apuesta. Ganó el vehículo {ganador.numero} (apostaste por el {self.apuesta}).", "tomato")

    def mostrarresultados(self):
        resultados = sorted(self.vehiculos, key=lambda vehiculo: vehiculo.tiempofinal)
        for posicion, vehiculo in enumerate(resultados, start=1):
            self.tabla.insert("", "end", values=(posicion, f"Vehículo {vehiculo.numero}", f"{vehiculo.tiempofinal:.2f} s", vehiculo.vueltas))

    def reiniciar(self):
        self.cancelarverificacion()

        for vehiculo in self.vehiculos:
            vehiculo.reiniciar()

        self.limpiartabla()
        self.mostrarmensaje("")
        self.encarrera = False
        self.bloquearcontroles(False)
        self.actualizarinfo()
