import random
import pygame

pygame.init()

class Animal:
    def __init__(self, energia, tiempo_vida):
        self.energia = energia
        self.tiempo_vida = tiempo_vida

    def moverse(self):
        self.energia -= 1  

    def reproducirse(self):
        self.energia -= 2  

    def envejecer(self):
        self.tiempo_vida -= 1  

class Predador(Animal):
    def __init__(self, energia, tiempo_vida):
        super().__init__(energia, tiempo_vida)

    def cazar(self):
        self.energia += 10

    def morir(self):
        return self.energia <= 0 or self.tiempo_vida <= 0

class Presa(Animal):
    def __init__(self, energia, tiempo_vida):
        super().__init__(energia, tiempo_vida)

    def alimentarse(self):
        self.energia += 5

    def morir(self):
        return self.energia <= 0 or self.tiempo_vida <= 0

class Ecosistema:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.matriz = [[None for _ in range(columnas)] for _ in range(filas)]
        self.comida = [[0 for _ in range(columnas)] for _ in range(filas)]  
        self.turnos_para_comida = 5  
        self.turno_actual = 0

    def inicializar_ecosistema(self, num_predadores, num_presas):
        print("Inicializando ecosistema...") 
        for _ in range(num_predadores):
            x, y = self.encontrar_celda_vacia()
            self.matriz[x][y] = Predador(energia=20, tiempo_vida=10)

        for _ in range(num_presas):
            x, y = self.encontrar_celda_vacia()
            self.matriz[x][y] = Presa(energia=10, tiempo_vida=8)

        
        self.distribuir_comida()

    def distribuir_comida(self):
        
        for _ in range((self.filas * self.columnas) // 5):  
            x, y = random.randint(0, self.filas - 1), random.randint(0, self.columnas - 1)
            self.comida[x][y] += 1

    def generar_comida_periodica(self):
        
        if self.turno_actual % self.turnos_para_comida == 0:
            print("Generando nueva comida en el ecosistema...")
            self.distribuir_comida()

    def encontrar_celda_vacia(self):
        while True:
            x = random.randint(0, self.filas - 1)
            y = random.randint(0, self.columnas - 1)
            if self.matriz[x][y] is None:
                return x, y

    def mover_animal(self, x, y):
        animal = self.matriz[x][y]
        if animal:
            dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
            nuevo_x, nuevo_y = x + dx, y + dy

            if 0 <= nuevo_x < self.filas and 0 <= nuevo_y < self.columnas:
                objetivo = self.matriz[nuevo_x][nuevo_y]

                if isinstance(animal, Predador) and isinstance(objetivo, Presa):
                    print(f"Predador en ({x}, {y}) cazó a una presa en ({nuevo_x}, {nuevo_y})")
                    animal.cazar()
                    self.matriz[nuevo_x][nuevo_y] = animal
                    self.matriz[x][y] = None
                elif objetivo is None:
                    print(f"Animal movido de ({x}, {y}) a ({nuevo_x}, {nuevo_y})")
                    animal.moverse()
                    self.matriz[nuevo_x][nuevo_y] = animal
                    self.matriz[x][y] = None

    def alimentar_presas(self):
        
        for x in range(self.filas):
            for y in range(self.columnas):
                animal = self.matriz[x][y]
                if isinstance(animal, Presa) and self.comida[x][y] > 0:
                    print(f"Presa en ({x}, {y}) comió comida en la celda")
                    animal.alimentarse()
                    self.comida[x][y] -= 1

    def actualizar_ecosistema(self):
        print("Actualizando ecosistema...")  
        for x in range(self.filas):
            for y in range(self.columnas):
                animal = self.matriz[x][y]
                if animal:
                    animal.envejecer()
                    if animal.morir():
                        print(f"Animal en ({x}, {y}) ha muerto")
                        self.matriz[x][y] = None
                    else:
                        self.mover_animal(x, y)

        self.alimentar_presas()
        self.reproduccion()
        self.turno_actual += 1
        self.generar_comida_periodica()

    def reproduccion(self):
        for x in range(self.filas):
            for y in range(self.columnas):
                animal = self.matriz[x][y]
                if animal:
                    dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
                    nuevo_x, nuevo_y = x + dx, y + dy

                    if 0 <= nuevo_x < self.filas and 0 <= nuevo_y < self.columnas and self.matriz[nuevo_x][nuevo_y] is None:
                        if isinstance(animal, Presa) and animal.energia > 5:
                            print(f"Nueva presa nacida en ({nuevo_x}, {nuevo_y})")
                            animal.reproducirse()
                            self.matriz[nuevo_x][nuevo_y] = Presa(energia=7, tiempo_vida=8)
                        elif isinstance(animal, Predador) and animal.energia > 10:
                            print(f"Nuevo predador nacido en ({nuevo_x}, {nuevo_y})")
                            animal.energia -= 5  
                            animal.reproducirse()
                            self.matriz[nuevo_x][nuevo_y] = Predador(energia=10, tiempo_vida=12)

    def dibujar_ecosistema(self, screen, celda_size):
        for x in range(self.filas):
            for y in range(self.columnas):
                celda = self.matriz[x][y]
                color = (255, 255, 255)  # Vacío (blanco)
                if isinstance(celda, Predador):
                    color = (255, 0, 0)  # Predador (rojo)
                elif isinstance(celda, Presa):
                    color = (0, 255, 0)  # Presa (verde)
                elif self.comida[x][y] > 0:
                    color = (255, 255, 0)  # Comida (amarillo)
                pygame.draw.rect(screen, color, (y * celda_size, x * celda_size, celda_size, celda_size))
                pygame.draw.rect(screen, (0, 0, 0), (y * celda_size, x * celda_size, celda_size, celda_size), 1)


celda_size = 50
info_pantalla = pygame.display.Info()
ancho_ventana = info_pantalla.current_w
altura_ventana = info_pantalla.current_h

columnas = ancho_ventana // celda_size
filas = altura_ventana // celda_size

screen = pygame.display.set_mode((columnas * celda_size, filas * celda_size))
pygame.display.set_caption("Simulación del Ecosistema")

# Inicialización del ecosistema
ecosistema = Ecosistema(filas, columnas)
ecosistema.inicializar_ecosistema(num_predadores=10, num_presas=20)

# Bucle principal
reloj = pygame.time.Clock()
ejecutando = True

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    ecosistema.actualizar_ecosistema()

    screen.fill((0, 0, 0))  
    ecosistema.dibujar_ecosistema(screen, celda_size)
    pygame.display.flip()

    reloj.tick(2)

pygame.quit()
