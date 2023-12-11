import pygame
import threading
import time

# Inicialização do Pygame
pygame.init()

semaforo_1= threading.Semaphore(2)
semaforo_2= threading.Semaphore(2)

mutex1 = threading.Lock()
mutex2 = threading.Lock()
mutex3 = threading.Lock()
mutex4 = threading.Lock()
mutex5 = threading.Lock()


# Definição de cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Configurações da janela
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simulação de Trens")

# Tamanho do passo para os trens
STEP = 5
TRAIN_SIZE = 20  # Tamanho dos trens

# Classe para representar um trem
class Train:
    def __init__(self, name, route, color, speed):
        self.name = name
        self.route = route
        self.color = color
        self.speed = speed
        self.position = 0
        self.x, self.y = route[0]  # Posição inicial do trem
        self.xStart, self.yStart = route[0]  # Ponto inicial do percurso
        self.xEnd, self.yEnd = route[-1]  # Ponto final do percurso
        self.mutex = threading.Lock()

    def move(self):
        
        while True:
            self.test()
            if self.x < self.xEnd and self.y == self.yStart:
                self.x += STEP
            elif self.x == self.xEnd and self.y < self.yEnd:
                self.y += STEP
            elif self.x > self.xStart and self.y == self.yEnd:
                self.x -= STEP
            else:
                self.y -= STEP
            time.sleep(1 / self.speed)

    def test(self):
        if self.name == "Trem1":
            if self.x == 400 and self.y == 200: #L3
                semaforo_1.acquire()
                mutex1.acquire()
            if self.x == 260 and self.y == 200: #L4
                mutex2.acquire()
                semaforo_1.release()
                if mutex1.locked():
                    mutex1.release()
            if self.x == 100 and self.y == 200:#L5
                if mutex2.locked():   
                    mutex2.release()

    
        if self.name == "Trem2": 
            if self.x == 100 and self.y == 200:
                semaforo_1.acquire()
                mutex2.acquire()
            if self.x ==250 and self.y == 200:
                mutex3.acquire()
                semaforo_1.release()
                if mutex2.locked():
                    mutex2.release()
            if self.x == 250 and self.y == 300:
                semaforo_2.acquire()
                mutex4.acquire()
                if mutex3.locked():
                    mutex3.release()
            if self.x == 100 and self.y == 300:
                semaforo_2.release()
                if mutex4.locked():
                    mutex4.release()
        
        if self.name == "Trem3":
            if self.x == 400 and self.y == 300:
                semaforo_2.acquire()
                mutex5.acquire()
            if self.x == 250 and self.y == 300:
                mutex3.acquire()
                semaforo_2.release()
                if mutex5.locked():
                    mutex5.release()
            if self.x == 250 and self.y == 200:
                semaforo_1.acquire()
                mutex1.acquire()
                if mutex3.locked():
                    mutex3.release()
            if self.x == 400 and self.y == 200:
                semaforo_1.release()
                if mutex1.locked():
                    mutex1.release()
        
        if self.name == "Trem4":
            if self.x == 100 and self.y == 300:
                semaforo_2.acquire()
                mutex4.acquire()
            if self.x == 250 and self.y ==300:
                mutex5.acquire()
                semaforo_2.release()
                if mutex4.locked():
                    mutex4.release()
            if self.x == 400 and self.y == 300:
                if mutex5.locked():
                    mutex5.release()
             



               



    def run(self):
        self.move()

    


# Função para desenhar os trens e trilhos na tela
def draw_trains(trains):
    screen.fill(BLACK)

    # Desenhar trilhos
    #for i in range(len(trains[0].route) - 1):
    #    pygame.draw.lines(screen, WHITE, False, [trains[0].route[i], trains[0].route[i + 1]], 2)
    #pygame.draw.lines(screen, WHITE, False, [trains[0].route[-1], trains[0].route[0]], 2)
    for i in range(len(trains[0].route) - 1):
        pygame.draw.lines(screen, WHITE, False, trains[i].route, 2)

    pygame.draw.lines(screen, WHITE, False, [(100, 100),(100,300),(400,300),(400,400),(100,400),(100,300)], 2)

    # Desenhar trens
    for train in trains:
        pygame.draw.rect(screen, train.color, (int(train.x - TRAIN_SIZE/2), int(train.y - TRAIN_SIZE/2), TRAIN_SIZE, TRAIN_SIZE))

    pygame.display.flip()

# Função principal
def main():
    # Definindo rotas
    route_trem1 = [(100, 100), (400, 100), (400, 200), (400, 200)]
    route_trem2 = [(100, 200), (100, 200), (250, 200), (250, 300)]
    route_trem3 = [(250, 200), (400, 200), (400, 300), (400, 300)]
    route_trem4 = [(100, 300), (100, 300), (400, 300), (400, 400)]

    # Inicializando os trens
    train1 = Train("Trem1", route_trem1, GREEN, 27)
    train2 = Train("Trem2", route_trem2, WHITE, 25)
    train3 = Train("Trem3", route_trem3, BLUE, 26)
    train4 = Train("Trem4", route_trem4, RED, 20)

    # Criando threads para os trens
    thread_train1 = threading.Thread(target=train1.run)
    thread_train2 = threading.Thread(target=train2.run)
    thread_train3 = threading.Thread(target=train3.run)
    thread_train4 = threading.Thread(target=train4.run)

    # Inicializando a tela
    screen.fill(BLACK)
    pygame.display.flip()

    # Inicializando threads antes do loop principal
    thread_train1.start()
    thread_train2.start()
    thread_train3.start()
    thread_train4.start()

    # Loop principal
    while True:  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        draw_trains([train1, train2, train3, train4])

if __name__ == "__main__":
    main()
