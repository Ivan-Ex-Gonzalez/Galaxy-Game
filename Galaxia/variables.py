import pygame as pg
import os


ubi_juego = os.path.dirname(__file__)
#IMAGENES
ubi_imagenes = os.path.join(ubi_juego,"imagenes")
ubi_disparos = os.path.join(ubi_imagenes,"disparos")
ubi_icono = os.path.join(ubi_imagenes,"icono")
ubi_efectos = os.path.join(ubi_imagenes,"efectos")
ubi_fondos = os.path.join(ubi_imagenes,"fondos")
ubi_botones = os.path.join(ubi_imagenes,"botones")
ubi_mensajes = os.path.join(ubi_imagenes,"mensajes")
#IMAGENES\NAVES
ubi_naves = os.path.join(ubi_imagenes,"naves")
ubi_nave_aliada = os.path.join(ubi_naves,"nave_aliada")
ubi_naves_enemigas = os.path.join(ubi_naves,"naves_enemigas")
#SONIDOS
ubi_sonidos = os.path.join(ubi_juego,"sonidos")
ubi_musicas = os.path.join(ubi_sonidos,"musicas")
#SONIDOS\EFECTOS_SONIDO
ubi_efectos_sonido = os.path.join(ubi_sonidos,"efectos_sonido")
ubi_disparos_sonido = os.path.join(ubi_efectos_sonido,"disparos")
ubi_explosiones = os.path.join(ubi_efectos_sonido,"explosiones")
ubi_hits = os.path.join(ubi_efectos_sonido,"hits")
#FUENTE
ubi_fuente = os.path.join(ubi_juego,"fuente")
fuente = os.path.join(ubi_fuente,"Retro Gaming.ttf")
#SQL
sql_puntos = os.path.join(ubi_juego,"Puntos.db")

#MUSICAS
pg.mixer.init()
musica_menu =  pg.mixer.Sound(os.path.join(ubi_musicas,"menu.ogg"))
musica_fondo = pg.mixer.Sound(os.path.join(ubi_musicas,"musica_fondo.mp3"))
musica_final = pg.mixer.Sound(os.path.join(ubi_musicas,"musica_final.mp3"))
musica_victoria =  pg.mixer.Sound(os.path.join(ubi_musicas,"victoria.mp3"))
musicas = [musica_menu,musica_fondo,musica_final,musica_victoria]

#EFECTOS DE SONIDO
disparo_jugador =  pg.mixer.Sound(os.path.join(ubi_disparos_sonido,"disparo_aliado.wav"))
sonido_disparo_enemigo = pg.mixer.Sound(os.path.join(ubi_disparos_sonido,"disparo_enemigo.wav"))
hit_jugador =  pg.mixer.Sound(os.path.join(ubi_hits,"hit_jugador.wav"))
puum =  pg.mixer.Sound(os.path.join(ubi_explosiones,"explosion1.wav"))
efectos_de_sonido = [disparo_jugador,sonido_disparo_enemigo,hit_jugador,puum]

#GRUPOS
disparos = pg.sprite.Group()
disparos_enemigos = pg.sprite.Group()
player = pg.sprite.Group()
enemigos = pg.sprite.Group()
explosiones = pg.sprite.Group()
botones = pg.sprite.Group()
botones_score = pg.sprite.Group()
grupo_puntaje_final = pg.sprite.Group()
grupo_settings = pg.sprite.Group()
volume = pg.sprite.Group()


#IMAGEN
imagen_ventana = os.path.join(ubi_fondos,"ventana.png")
imagen_tabla = os.path.join(ubi_fondos,"tabla.png")
imagen_icono = os.path.join(ubi_icono,"icono.png")
imagen_fondo = os.path.join(ubi_fondos,"fondo_espacio.png")
perdiste = os.path.join(ubi_mensajes,"perdiste.png")
ganaste = os.path.join(ubi_mensajes,"ganaste.png")

#Resoluciones
resuluciones = ["426 x 240", "640 x 360", " 854 x 480", "1280 x 720", "1920 x 1080"]
anc_pant = [426 , 640 ,  854 , 1280 , 1920 ]
alt_pant = [240, 360,  480, 720, 1080]
