# Ejercicio de termómetro convertidor, ahora con pygame

import pygame, sys
from pygame.locals import *

class Termometro():
    
    def __init__(self):
        self.disfraz = pygame.image.load("images/Termometro.jpg")
        
    def convertir(self, grados, unidadFinal):
        
        if unidadFinal == "F":
            resultado = grados * 9 / 5 +32
        elif unidadFinal == "C":
            resultado = (grados-32) * 5 / 9
        else:
            resultado = grados
        
        return "{:10.2f}".format(resultado)
        

class Selector():
    __tipoUnidad = None
    
    def __init__(self, unidad="C"):
        self.__disfraz = []
        self.__disfraz.append(pygame.image.load("images/TermometroF.jpg"))
        self.__disfraz.append(pygame.image.load("images/TermometroC.jpg"))
        
        self.__tipoUnidad = unidad
    
    def unidadGS(self, unidad=None):
        if unidad == None:
            return self.__tipoUnidad
        else:
            self.__tipoUnidad = unidad
    
    def getDisfraz(self):
        if self.__tipoUnidad == "F":
            return self.__disfraz[0]
        else:
            return self.__disfraz[1]
    
    def change(self):

            if self.__tipoUnidad == "F":
                self.__tipoUnidad = "C"
            else:
                self.__tipoUnidad = "F"
        

class entradaValor():
    
    __valor = 0
    __strValor = ""    # OJO QUE EL STRING es lo que se renderiza y pinta
    __position = [120,80]
    __size = [150,30]
    __contadorPunto=0
    
    def __init__(self, valor=0):     
        pygame.font.init()
        self.__font = pygame.font.SysFont("Arial", 24)   # pygame.font permite poner textos
        self.valorGetSet(valor)

    def onEvent(self, event):
        if event.type == KEYDOWN:
            #Número y que quepa o coma (punto) y no hay otro

            if (event.unicode in "0123456789" and len(self.__strValor)<=10) or (event.unicode == "." and self.__contadorPunto==0):
                self.__strValor += event.unicode
                self.valorGetSet(self.__strValor)
                if event.unicode == ".":
                    self.__contadorPunto +=1
            elif event.key == K_BACKSPACE:
                self.__strValor = self.__strValor[:-1]
                self.valorGetSet(self.__strValor)
                if self.__strValor[-1] == ".":
                    self.__contadorPunto -=1

    def render(self):
        # Para el texto hacen falta dos objetos: El recuadro y el propio texto, superpuestos
        
        # Qué, si se expande y el color. Con esta isntrucción pasamos de texto a la imagen a pintar
        textBlock = self.__font.render(self.__strValor, True, (74,74,74))  #strValor porque SOLO sabe pintar cadenas
        rectangulo = textBlock.get_rect()
        rectangulo.left = self.__position[0]
        rectangulo.top = self.__position[1]
        rectangulo.size = self.__size
        return {
            "fondo": rectangulo,
            "texto": textBlock}
    
    
    def valorGetSet(self, val = None):
        if val == None:
            return self.__valor
        else:
            val = str(val)
            try:
                self.__valor = float(val)
                self.__strValor = val
                if "." in self.__strValor:
                    self.__contadorPunto=1
                else:
                    self.__contadorPunto=0
            except:
                pass
    
    def anchoGetSet(self, val = None):
        if val == None:
            return self.__size[0]
        else:
            try:
                self.__size[0] = int(val)
            except:
                pass       

    def altoGetSet(self, val = None):
        if val == None:
            return self.__size[1]
        else:
            try:
                self.__size[1] = int(val)
            except:
                pass    

    def sizeGetSet(self, val = None):
        if val == None:
            return self.__size
        else:
            try:
                w=int(val[0])
                h=int(val[1])                          
                self.__size = [w,h]
            except:
                pass

    def posXGetSet(self, val = None):
        if val == None:
            return self.__position[0]
        else:
            try:
                self.__position[0] = int(val)
            except:
                pass       

    def posYGetSet(self, val = None):
        if val == None:
            return self.__position[1]
        else:
            try:
                self.__position[1] = int(val)
            except:
                pass 

    def positionGetSet(self, val = None):
        if val == None:
            return self.__position
        else:
            try:
                w=int(val[0])
                h=int(val[1])                          
                self.__position = [w,h]
            except:
                pass  

 

class mainApp():
    termometro = None
    entrada = None
    selector = None
    
    def __init__(self):
        self.__screen = pygame.display.set_mode((300,450))
        pygame.display.set_caption("Termómetro")
        self.__screen.fill((244,236,203))
        
        self.termometro=Termometro()
        self.entrada = entradaValor()
        self.entrada.positionGetSet((120,80))
        self.entrada.sizeGetSet((150,30))
        
        self.selector = Selector()
        

    def __onClose(self):
        pygame.quit()
        sys.exit()

    def start(self):
        
        introducido=""
        
        
        # Ciclo básico videojuego: Capturar eventos, acciones relacionadas y repintar pantalla.
        # Siempre será igual, aunque cambien los eventos lo que sea
        while True:                              
            for evento in pygame.event.get():
                if evento.type == QUIT:
                    self.__onClose()
                self.entrada.onEvent(evento)
                
                if evento.type == MOUSEBUTTONDOWN:                        # Hay click, convertir
                    self.selector.change()
                    grados = self.entrada.valorGetSet()
                    nuevaUnidad = self.selector.unidadGS()
                    nuevaT = self.termometro.convertir(grados,nuevaUnidad)
                    self.entrada.valorGetSet(nuevaT)

            # Pintamos el fondo de pantalla (nada saldrá hasta el flip)
            self.__screen.fill((244,236,203))                              # Fondo pa pintar encima

            # Pintamos el termómetro
            self.__screen.blit(self.termometro.disfraz,(30,20))            # Pinta el termómetro
            
             # Crea rectángulo blanco con datos y "foto" del texto (string del número), que están en un dict
            cuadro = self.entrada.render()
            
            # Crea y pinta el recuadro con el fondo del dict
            pygame.draw.rect(self.__screen,(255,255,255), cuadro["fondo"])
            
            self.__screen.blit(cuadro["texto"], self.entrada.positionGetSet())  #Pinta el texto del recuadro (del dict)
            
            # Pintamos el selector:
            self.__screen.blit(self.selector.getDisfraz(), (120, 200))
            
            # Refrescamos lo que se ve
            pygame.display.flip()
            
    

if __name__ == "__main__":
    pygame.init()
    miApp = mainApp()
    miApp.start()
    
        

    
    