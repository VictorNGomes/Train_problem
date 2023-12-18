import pygame
import threading
import time
import pygame_gui

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
YELLOW = (255,255,0)

# Configurações da janela
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simulação de Trens")

# Tamanho do passo para os trens
STEP = 5
TRAIN_SIZE = 20  # Tamanho dos trens

# Classe para representar um trem
class Train:
    def __init__(self, name, route, color, speed,x_start,y_start):
        self.name = name
        self.route = route
        self.color = color
        self.speed = speed
        self.position = 0
        self.x, self.y = x_start,y_start  # Posição inicial do trem
        self.xStart, self.yStart = x_start,y_start  # Ponto inicial do percurso
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
                #semaforo_1.acquire()
                mutex2.acquire()
                mutex1.acquire()
            if self.x == 250 and self.y == 200: #L4
                #semaforo_1.release()
                #if mutex1.locked():
                mutex1.release()
            if self.x == 100 and self.y == 200:#L5
                if mutex2.locked():   
                    mutex2.release()

    
        if self.name == "Trem2": 
            if self.x == 100 and self.y == 200: #L5
                #if not mutex2.locked():
                mutex2.acquire()
            if self.x ==250 and self.y == 200: #L7
                mutex3.acquire()
                if mutex2.locked():
                    mutex2.release()
            if self.x == 250 and self.y == 300: #L8
                mutex4.acquire()
                mutex3.release()
            if self.x == 100 and self.y == 300:
                if mutex4.locked():    
                    mutex4.release()
        
        if self.name == "Trem3":
            if self.x == 400 and self.y == 300:
                mutex5.acquire()
            if self.x == 250 and self.y == 300:
                mutex3.acquire()
                if mutex5.locked():
                    mutex5.release()
            if self.x == 250 and self.y == 200:   
                #if not mutex1.locked():
                mutex1.acquire()
                if mutex3.locked():        
                    mutex3.release()
            if self.x == 400 and self.y == 200:
                if mutex1.locked():
                    mutex1.release()
        
        if self.name == "Trem4":
            if self.x == 100 and self.y == 300:
                #semaforo_2.acquire()
                mutex5.acquire()
                #if not mutex4.locked():
                mutex4.acquire()
            if self.x == 250  and self.y ==300:
                #mutex5.acquire()
                #semaforo_2.release()
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
        pygame.draw.lines(screen, WHITE, False, trains[i].route, 20)

    pygame.draw.lines(screen, WHITE, False, [(100, 100),(100,300),(400,300),(400,400),(100,400),(100,300)], 20)

    # Desenhar trens
    for train in trains:
        pygame.draw.rect(screen, train.color, (int(train.x - TRAIN_SIZE/2), int(train.y - TRAIN_SIZE/2), TRAIN_SIZE, TRAIN_SIZE))

    pygame.display.flip()

def initialize_gui(manager, trains):
    font = pygame.font.Font(None, 36)
    screen_width, _ = pygame.display.get_surface().get_size()

    for i, train in enumerate(trains):
        slider_rect = pygame.Rect(width - 210, 10 + i * 50, 200, 20)
        slider = pygame_gui.elements.UIHorizontalSlider(slider_rect, 1, (1, 50), manager=manager)
        #slider.set_value(train.speed)  # Set the initial value of the slider

        # Adjust X-coordinates to position the slider and label to the right
        label_rect = pygame.Rect(width - 420, 10 + i * 50, 200, 50)
        label = pygame_gui.elements.UILabel(relative_rect=label_rect,
                                             text=f"Speed {train.name}: {train.speed}", manager=manager)

        train.slider = slider
        train.label = label

# Função principal
def main():
    # Definindo rotas
    route_trem1 = [(100, 100), (400, 100), (400, 200), (400, 200)]
    route_trem2 = [(100, 200), (100, 200), (250, 200), (250, 300)]
    route_trem3 = [(250, 200), (400, 200), (400, 300), (400, 300)]
    route_trem4 = [(100, 300), (100, 300), (400, 300), (400, 400)]

    # Inicializando os trens
    train1 = Train("Trem1", route_trem1, GREEN, 27,100,100)
    train2 = Train("Trem2", route_trem2, YELLOW, 25,100,200)
    train3 = Train("Trem3", route_trem3, BLUE, 26,250,200)
    train4 = Train("Trem4", route_trem4, RED, 20,100,300)
    #mutex1.acquire()
    #mutex2.acquire()
    #mutex4.acquire()

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
    pygame.init()
    pygame.display.set_caption("Simulação de Trens")
    clock = pygame.time.Clock()
    manager = pygame_gui.UIManager((width, height))

    initialize_gui(manager, [train1, train2, train3, train4])

    # Loop principal
    while True:  
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            manager.process_events(event)

        for train in [train1, train2, train3, train4]:
            train.speed = int(train.slider.get_current_value())
            train.label.set_text(f"Speed {train.name}: {train.speed}")

        manager.update(time_delta)
        draw_trains([train1, train2, train3, train4])
        manager.draw_ui(screen)

        pygame.display.flip()
if __name__ == "__main__":
    main()