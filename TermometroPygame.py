# Ejercicio de termómetro convertidor, ahora con pygame

import pygame, sys
from pygame.locals import *

class mainApp():
    termometro = None
    entrada = None
    selector = None
    
    def __init__(self):
        self.__screen = pygame.display.set_mode((300,450))
        pygame.display.set_caption("Termómetro")
        self.__screen.fill((244,236,203))

    def __onClose(self):
        pygame.quit()
        sys.exit()

    def start(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == QUIT:
                    self.__onClose()
            
            pygame.display.flip()
    

if __name__ == "__main__":
    pygame.init()
    miApp = mainApp()
    miApp.start()
    
        

    
    