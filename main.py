import pygame
import threading
import time

# Inicialização do Pygame
pygame.init()

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

# Classe para representar um trem
class Train:
    def __init__(self, name, route, color, speed):
        self.name = name
        self.route = route
        self.color = color
        self.speed = speed
        self.position = 0
        self.mutex = threading.Lock()

# Função para desenhar os trens e trilhos na tela
def draw_trains(trains):
    screen.fill(BLACK)

    # Desenhar trilhos
    pygame.draw.lines(screen, WHITE, False, [(100, 100), (400, 100), (400, 200), (100, 200)], 2)
    pygame.draw.lines(screen, WHITE, False, [(100, 200), (100, 300), (250, 300), (250, 200), (400, 200), (400, 300)], 2)
    pygame.draw.lines(screen, WHITE, False, [(100, 400), (100, 300), (400, 300), (400, 400)], 2)

    # Adicionando trilhos para o trem verde
    pygame.draw.lines(screen, WHITE, False, [(400, 200), (800, 200)], 2)
    pygame.draw.lines(screen, WHITE, False, [(100, 100), (100, 600), (800, 600), (800, 200)], 2)

    # Desenhar trens
    for train in trains:
        pygame.draw.circle(screen, train.color, train.route[train.position], 20)

    pygame.display.flip()

# Função que simula o movimento de um trem
def move_train(train):
    while True:
        time.sleep(1 / train.speed)
        with train.mutex:
            train.position = (train.position + 1) % len(train.route)

# Função principal
def main():
    # Definindo rotas
    route_trem1 = [(100, 100), (400, 100), (400, 200), (100, 200)]
    route_trem2 = [(100, 300), (100, 200), (250, 200), (250, 300)]
    route_trem3 = [(250, 200), (400, 200), (400, 300), (250, 300)]
    route_trem4 = [(100, 400), (100, 300), (400, 300), (400, 400)]

    # Inicializando os trens
    train1 = Train("Trem1", route_trem1, GREEN, 2)
    train2 = Train("Trem2", route_trem2, WHITE, 1)
    train3 = Train("Trem3", route_trem3, BLUE, 3)
    train4 = Train("Trem4", route_trem4, RED, 2)

    # Criando threads para os trens
    thread_train1 = threading.Thread(target=move_train, args=(train1,))
    thread_train2 = threading.Thread(target=move_train, args=(train2,))
    thread_train3 = threading.Thread(target=move_train, args=(train3,))
    thread_train4 = threading.Thread(target=move_train, args=(train4,))

    # Inicializando a tela
    screen.fill(BLACK)
    pygame.display.flip()

    # Inicializando threads
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
