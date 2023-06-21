import pygame as pg
import random
import os
import variables as vari

ubi_juego = os.path.dirname(__file__)
#IMAGENES
ubi_imagenes = os.path.join(ubi_juego,"imagenes")
ubi_disparos = os.path.join(ubi_imagenes,"disparos")
ubi_icono = os.path.join(ubi_imagenes,"icono")
ubi_efectos = os.path.join(ubi_imagenes,"efectos")
ubi_fondos = os.path.join(ubi_imagenes,"fondos")
ubi_botones = os.path.join(ubi_imagenes,"botones")
#IMAGENES\NAVES
ubi_naves = os.path.join(ubi_imagenes,"naves")
ubi_nave_aliada = os.path.join(ubi_naves,"nave_aliada")
ubi_naves_enemigas = os.path.join(ubi_naves,"naves_enemigas")
#________________________________________________________________
class Datos_del_juego:
    def __init__(self):
        self.ancho_ventana = 1280
        self.alto_ventana = 720
        self.mitad_ventana_x =  self.ancho_ventana // 2
        self.mitad_ventana_y =  self.alto_ventana // 2
        self.un_cauarto_ventana_x = self.mitad_ventana_x // 2
        self.un_cauarto_ventana_y = self.mitad_ventana_y // 2
        self.ancho_nave = self.ancho_ventana // 15
        self.alto_nave = int(self.alto_ventana // 6.6)
        self.TAMANO_LETRA = self.alto_ventana // 40
        self.cant_enemigos = 5
        self.puntaje_estado = False
        self.traba_musical = -1
        self.puntuacion_final = False
        self.fondo_y = 0
        self.res_actual = 3
        self.cambio_res = True
        self.mantener_setting = 0
        self.mantener_musica = False
        self.mantener_sonido = False
        self.cam_vol = None
        #self.tipo_vol = None
        self.boton_down = None
        self.boton_up = None
        self.music = 0.1
        self.sound = 0.1
        self.bandera_volumen = 0

    def reset(self):
        self.sin_vida_parte = 1
        self.puntos_actuales = 0
        self.tiempo_de_juego = 60
        self.nombre = ""
        self.puntuacion_final = False
        self.vida_jugador = 100
        self.traba_explosion = True 
        self.tipo_final = 0
        self.win = False
    
    def resolucion(self):
        self.mitad_ventana_x =  self.ancho_ventana // 2
        self.mitad_ventana_y =  self.alto_ventana // 2
        self.un_cauarto_ventana_x = self.mitad_ventana_x // 2
        self.un_cauarto_ventana_y = self.mitad_ventana_y // 2
        self.ancho_nave = self.ancho_ventana // 15
        self.alto_nave = int(self.alto_ventana // 6.6)
        self.TAMANO_LETRA = self.mitad_ventana_y // 20

dat_jue = Datos_del_juego()
#JUGADOR
class Jugador(pg.sprite.Sprite):
    
    def __init__(self):

        super().__init__()

        self.image = pg.image.load(os.path.join(ubi_nave_aliada,"nave1.png")).convert_alpha()

        self.image = pg.transform.scale(self.image, (dat_jue.ancho_nave , dat_jue.alto_nave ))

        self.rect =self.image.get_rect()
        self.radius = dat_jue.ancho_nave / 2

        self.rect.center = (dat_jue.ancho_ventana // 2,dat_jue.alto_ventana - dat_jue.alto_ventana / 4)

        self.velocidad_x = 0
        self.velocidad_y = 0

        self.perdida_vida = 5

        self.cadencia = 300
        self.ultimo = pg.time.get_ticks()

    def update(self) -> None:
        
        #Si no toco nada ¡No te muevas!
        self.velocidad_x = 0
        self.velocidad_y = 0

        teclas = pg.key.get_pressed()
        if dat_jue.vida_jugador > 0:
            if teclas[pg.K_LEFT] and self.rect.left > 0:
                self.velocidad_x = -15
            if teclas[pg.K_RIGHT] and self.rect.right < dat_jue.ancho_ventana:
                self.velocidad_x = +15
            if teclas[pg.K_UP] and self.rect.top > 0:
                self.velocidad_y = -15
            if teclas[pg.K_DOWN] and self.rect.bottom < dat_jue.alto_ventana:
                self.velocidad_y = +15
            if teclas[pg.K_SPACE]:
                self.actual = pg.time.get_ticks()
                if self.actual - self.ultimo >= self.cadencia:
                    self.disparar()
                    self.ultimo = self.actual
        
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
    
        

    
    def disparar(self):
        self.bala = Disparos(self.rect.centerx, self.rect.top)
        vari.disparos.add(self.bala)
        vari.disparo_jugador.play()       
#ENEMIGO
class Enemigos(pg.sprite.Sprite):
    def __init__(self):

        super().__init__()

        self.image = pg.image.load(os.path.join(ubi_naves_enemigas,"enemigo1.png")).convert_alpha()

        self.image = pg.transform.scale(self.image, (dat_jue.ancho_nave, dat_jue.alto_nave))

        self.rect =self.image.get_rect()
        self.radius = dat_jue.ancho_nave // 2

        #HITBOX
        #pg.draw.circle(self.image,(0,150,150) , self.rect.center, self.radius)

        self.rect.x = random.choice([-dat_jue.ancho_nave, dat_jue.ancho_ventana + dat_jue.ancho_nave])
        self.rect.y = random.randrange(dat_jue.alto_ventana - dat_jue.mitad_ventana_y - dat_jue.alto_nave)

        self.velocidad_x = random.randrange(1,10)
        self.velocidad_y = random.randrange(1,3)
        
        self.puntos = 500

        self.ultimo = pg.time.get_ticks()

        

    def update(self) -> None:
        if self.rect.centerx < 0 and self.velocidad_x < 0 or self.rect.centerx > dat_jue.ancho_ventana and self.velocidad_x > 0:
            self.velocidad_x *= -1
        
        if self.rect.left < 0 and self.rect.right < dat_jue.ancho_ventana and self.velocidad_x < 0:
            self.velocidad_x *= -1
            self.rect.x += self.velocidad_x
        if self.rect.left > 0 and self.rect.right > dat_jue.ancho_ventana and self.velocidad_x > 0:
            self.velocidad_x *= -1
            self.rect.x += self.velocidad_x
        
        self.rect.x += self.velocidad_x
        
        if self.rect.top > 0 and self.rect.bottom < dat_jue.mitad_ventana_y:
            self.rect.y += self.velocidad_y
        else:
            self.velocidad_y *= -1
            self.rect.y += self.velocidad_y
        self.cadencia = random.randrange(1000,4000)
        self.actual = pg.time.get_ticks()
        if self.actual - self.ultimo >= self.cadencia:
            self.disparar()
            self.ultimo = self.actual

        

    def disparar(self):
        self.bala = Disparos(self.rect.centerx, self.rect.bottom, 1)
        vari.disparos_enemigos.add(self.bala)
        vari.sonido_disparo_enemigo.play()
#EXPLOSION
class Explosion(pg.sprite.Sprite):
        
        def __init__(self,ubicacion):
            super().__init__()

            self.delay = 100
            self.explociones = []
            self.frame = 0
            self.image = self.image = pg.image.load(os.path.join(ubi_efectos,f"explosion{self.frame}.png")).convert_alpha()
            self.image = pg.transform.scale(self.image, (dat_jue.alto_nave, dat_jue.alto_nave))
            self.rect = self.image.get_rect()
            self.rect.center = ubicacion

            self.anterior = pg.time.get_ticks()

        def update(self):
            self.actual = pg.time.get_ticks()
            if self.actual - self.anterior >= self.delay:
                self.anterior = self.actual
                self.frame += 1
                if self.frame == 5:
                    self.kill()
                else:
                    self.image = self.image = pg.image.load(os.path.join(ubi_efectos,f"explosion{self.frame}.png")).convert_alpha()
                    self.image = pg.transform.scale(self.image, (dat_jue.alto_nave, dat_jue.alto_nave))
#DISPAROS
class Disparos(pg.sprite.Sprite):
    def __init__(self, x, y,tipo = 0):
        super().__init__()
        self.tipo = tipo
        self.tipos_disparos = (["disparo1.png","disparo2.png"],["disparo_enemigo1.png","disparo_enemigo2.png"])
        self.image = pg.image.load(os.path.join(ubi_disparos,self.tipos_disparos[self.tipo][0])).convert_alpha()
        #self.image = pg.image.load(r"games\imagenes_de_galaxia\laser_1.png").convert_alpha()
        self.image = pg.transform.scale(self.image,(dat_jue.ancho_ventana // 53,dat_jue.alto_ventana // 25))
        self.delay = 150
        self.rect =self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.anterior = pg.time.get_ticks()
        self.bandera = 0

    def update(self):
        self.actual = pg.time.get_ticks()
        if self.actual - self.anterior >= self.delay:
            self.anterior = self.actual
            if self.bandera == 0:
                self.bandera = 1
            else:
                self.bandera = 0
            self.image = pg.image.load(os.path.join(ubi_disparos,self.tipos_disparos[self.tipo][self.bandera])).convert_alpha()
            self.image = pg.transform.scale(self.image,(dat_jue.ancho_ventana // 53,dat_jue.alto_ventana // 25))
        if self.tipo == 0:
            self.rect.y -= 10
        else:
            self.rect.y += 10

        if self.rect.bottom < 0 or self.rect.top > dat_jue.alto_ventana:
            self.kill()
#BOTON
class Boton(pg.sprite.Sprite):     
    def __init__(self, tipo, x, y, tipo_tamaño = 1) -> None:
        super().__init__()
        self.tipo = tipo
        try:
            self.image = pg.image.load(os.path.join(ubi_botones,f"{self.tipo}1.png")).convert_alpha()
        except:
            print("no hay imagen valida")
            self.image = pg.image.load(os.path.join(ubi_botones,"cruz1.png")).convert_alpha()
        self.apretado = False
        self.bool = False
        self.posimouse = (-1,-1)
        if tipo_tamaño == 1:
            self.tamaño = (dat_jue.ancho_ventana//13,dat_jue.alto_ventana//10)
        else:
            self.tamaño = (dat_jue.ancho_ventana//6,dat_jue.alto_ventana//12)
        self.image = pg.transform.scale(self.image, self.tamaño)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        

        

    def update(self):
        
        mouse = pg.mouse.get_pressed()
        if mouse[0]:
                self.posimouse = pg.mouse.get_pos()
        
        if self.rect.collidepoint(self.posimouse):
            try:
                self.image = pg.image.load(os.path.join(ubi_botones,f"{self.tipo}2.png")).convert_alpha()
            except:
                print("no hay imagen valida")
                self.image = pg.image.load(os.path.join(ubi_botones,"cruz2.png")).convert_alpha()
            if not mouse[0]:
                self.apretado = True
        if not mouse[0] and not self.rect.collidepoint(self.posimouse):
            try:
                self.image = pg.image.load(os.path.join(ubi_botones,f"{self.tipo}1.png")).convert_alpha()
            except:
                print("no hay imagen valida")
                self.image = pg.image.load(os.path.join(ubi_botones,"cruz1.png")).convert_alpha()
        if self.apretado:
            try:
                self.image = pg.image.load(os.path.join(ubi_botones,f"{self.tipo}1.png")).convert_alpha()
            except:
                print("no hay imagen valida")
                self.image = pg.image.load(os.path.join(ubi_botones,"cruz1.png")).convert_alpha()
            self.bool = not self.bool
            self.apretado = False
            self.posimouse = (-1,-1)
        
        self.image = pg.transform.scale(self.image, self.tamaño)
    
    def apagar(self):
        self.bool = False