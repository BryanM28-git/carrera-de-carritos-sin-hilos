import random

numvehiculos = 10
colores = ["red", "blue", "green", "orange", "purple", "brown", "deeppink", "teal", "gold", "dimgray"]


class Vehiculo:
    def __init__(self, canvas, carril, numero, color, carrera):
        self.canvas = canvas
        self.carril = carril
        self.numero = numero
        self.color = color
        self.carrera = carrera
        self.tag = f"vehiculo{numero}"

        self.posicion = carrera.inicio
        self.velocidad = 0
        self.intervalo = 0
        self.vueltas = 0
        self.tiempo = 0.0
        self.tiempofinal = None
        self.timer = None
        self.direccion = 1

        self.sortearvelocidad()
        self.dibujar()

    def sortearvelocidad(self):
        self.velocidad = random.randint(2, 6)
        self.intervalo = random.randint(40, 100)

    def dibujar(self):
        izquierda = self.posicion
        centro = self.carril
        etiqueta = self.tag

        self.canvas.create_rectangle(izquierda, centro - 10, izquierda + 35, centro + 10, fill=self.color, outline="white", tags=etiqueta)
        self.canvas.create_polygon(izquierda + 8, centro - 10, izquierda + 15, centro - 18, izquierda + 28, centro - 18, izquierda + 34, centro - 10, fill=self.color, outline="white", tags=etiqueta)
        self.canvas.create_oval(izquierda + 5, centro + 5, izquierda + 13, centro + 13, fill="black", tags=etiqueta)
        self.canvas.create_oval(izquierda + 25, centro + 5, izquierda + 33, centro + 13, fill="black", tags=etiqueta)
        self.canvas.create_text(izquierda + 18, centro, text=str(self.numero), fill="white", font=("Arial", 9, "bold"), tags=etiqueta)

    def cancelartimer(self):
        if self.timer is not None:
            self.canvas.after_cancel(self.timer)
            self.timer = None

    def iniciar(self):
        self.timer = self.canvas.after(self.intervaloreal(), self.mover)

    def intervaloreal(self):
        return max(1, int(self.intervalo / self.carrera.factor))

    def mover(self):
        if self.tiempofinal is not None:
            return

        paso = self.velocidad * self.direccion
        self.canvas.move(self.tag, paso, 0)
        self.posicion += paso
        self.tiempo += self.intervalo / 1000

        if self.direccion == 1 and self.posicion >= self.carrera.meta:
            self.canvas.move(self.tag, self.carrera.meta - self.posicion, 0)
            self.posicion = self.carrera.meta
            self.direccion = -1
            self.sortearvelocidad()

        elif self.direccion == -1 and self.posicion <= self.carrera.inicio:
            self.canvas.move(self.tag, self.carrera.inicio - self.posicion, 0)
            self.posicion = self.carrera.inicio
            self.vueltas += 1

            if self.vueltas >= self.carrera.vueltas:
                self.tiempofinal = self.tiempo
                self.timer = None
                return

            self.direccion = 1
            self.sortearvelocidad()

        self.timer = self.canvas.after(self.intervaloreal(), self.mover)

    def reiniciar(self):
        self.cancelartimer()
        self.canvas.move(self.tag, self.carrera.inicio - self.posicion, 0)
        self.posicion = self.carrera.inicio
        self.vueltas = 0
        self.tiempo = 0.0
        self.tiempofinal = None
        self.direccion = 1
        self.sortearvelocidad()
