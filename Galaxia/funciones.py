import pygame as pg
import sqlite3
import sys
import os
import clases as Cla
import Colores as Col
import variables as vari

#ubi_juego = os.path.dirname(__file__)

def sin_vida_parte_uno(jugador):
    if Cla.dat_jue.sin_vida_parte == 1:
        vari.enemigos.empty()
        vari.disparos.empty()
        vari.disparos_enemigos.empty()
        reprodutor(2)
        jugador.ultimo = pg.time.get_ticks()
        jugador.delay = 10
        Cla.dat_jue.sin_vida_parte = 2

def sin_vida_parte_dos(jugador):
    if Cla.dat_jue.sin_vida_parte == 2:
        jugador.actual = pg.time.get_ticks()
        jugador.reposicion = 1
        if jugador.actual - jugador.ultimo >= jugador.delay:
            if jugador.rect.centerx < Cla.dat_jue.mitad_ventana_x:
                jugador.rect.centerx += jugador.reposicion
            elif jugador.rect.centerx > Cla.dat_jue.mitad_ventana_x:
                jugador.rect.centerx -= jugador.reposicion
            #else:
            #    jugador.reposicion = 2
            if jugador.rect.centery < Cla.dat_jue.mitad_ventana_y:
                jugador.rect.centery += jugador.reposicion
            elif jugador.rect.centery > Cla.dat_jue.mitad_ventana_y:
                jugador.rect.centery -= jugador.reposicion
            #else:
            #    jugador.reposicion = 2
            jugador.ultimo = jugador.actual
            if jugador.rect.centerx == Cla.dat_jue.mitad_ventana_x and jugador.rect.centery == Cla.dat_jue.mitad_ventana_y:
                Cla.dat_jue.sin_vida_parte = 3
################################ aca te quedaste
def sin_vida_parte_tres(jugador):
    if Cla.dat_jue.sin_vida_parte == 3 and Cla.dat_jue.traba_explosion:
        explosion = Cla.Explosion(jugador.rect.center)
        explosion.delay = 250
        vari.explosiones.add(explosion)
        Cla.dat_jue.traba_explosion = False
        jugador.kill()
        final= True
        return final
    final = False
    return final

#COLISIONES
def colisiones_melee(colision,enemigo_nuevo,jugador,):
     if colision:
            for enemigo_actual in colision:
                enemigo_actual.kill()
                Cla.dat_jue.puntos_actuales -= enemigo_nuevo.puntos
                Cla.dat_jue.vida_jugador -= jugador.perdida_vida
                vari.puum.play()
                explosion = Cla.Explosion(enemigo_actual.rect.center)
                vari.explosiones.add(explosion)
                vari.enemigos.remove(enemigo_actual)

def colision_disparos_aliados(colision_balas,enemigo_nuevo,explosiones):
      if colision_balas:
            for enemigo_actual in colision_balas:
                Cla.dat_jue.puntos_actuales += enemigo_nuevo.puntos
                vari.puum.play()
                explosion = Cla.Explosion(enemigo_actual.rect.center)
                explosiones.add(explosion)

def colision_disparos_enemigos(colision_balas_enemigas,enemigo_nuevo,jugador):
     if colision_balas_enemigas:
            Cla.dat_jue.puntos_actuales -= enemigo_nuevo.puntos
            Cla.dat_jue.vida_jugador -= jugador.perdida_vida
            vari.hit_jugador.play()


#CUENTA REGRESIVA
def cuenta_regresiva(tick_actual,ultimo_tick,boton_jugar):
    Cla.dat_jue.tiempo_de_juego -= 1
    ultimo_tick = tick_actual
    if Cla.dat_jue.tiempo_de_juego == 0:
        boton_jugar.apagar()
        vari.disparos.empty()
        vari.disparos_enemigos.empty()
        vari.enemigos.empty()
        vari.player.empty()
        Cla.dat_jue.puntuacion_final = True
        Cla.dat_jue.tipo_final = 1
    return ultimo_tick


################################
def ventanas(pantalla):
    ventana = pg.image.load(vari.imagen_ventana).convert_alpha()
    ventana = pg.transform.scale(ventana,(Cla.dat_jue.ancho_ventana - Cla.dat_jue.un_cauarto_ventana_x ,Cla.dat_jue.alto_ventana - Cla.dat_jue.un_cauarto_ventana_y))
    pantalla.blit(ventana,(Cla.dat_jue.un_cauarto_ventana_x // 2,Cla.dat_jue.un_cauarto_ventana_y // 2))

def ventanita(pantalla):
    ventana = pg.image.load(vari.imagen_ventana).convert_alpha()
    ventana = pg.transform.scale(ventana,(Cla.dat_jue.mitad_ventana_x ,Cla.dat_jue.mitad_ventana_y))
    pantalla.blit(ventana,(Cla.dat_jue.mitad_ventana_x// 2,Cla.dat_jue.mitad_ventana_y // 2))

def tabla(pantalla,x,y,largo,alto):
    tabla = pg.image.load(vari.imagen_tabla).convert_alpha()
    tabla = pg.transform.scale(tabla,(largo,alto))
    pantalla.blit(tabla,(x,y))
    
def ver_puntajes(pantalla):
    posicion = 1
    posiciony = Cla.dat_jue.un_cauarto_ventana_y
    with sqlite3.connect(vari.sql_puntos) as conexion:
        cursor=conexion.execute("SELECT * FROM Puntajes ORDER BY puntaje DESC LIMIT 5")
        mostrar_texto(pantalla,f"POSICION", Cla.dat_jue.ancho_ventana // 4.5, posiciony - posiciony//20, Cla.dat_jue.TAMANO_LETRA)
        mostrar_texto(pantalla,f"NOMBRE", Cla.dat_jue.ancho_ventana // 2.3, posiciony - posiciony//20, Cla.dat_jue.TAMANO_LETRA)
        mostrar_texto(pantalla,f"PUNTOS ", Cla.dat_jue.ancho_ventana // 1.5, posiciony - posiciony//20, Cla.dat_jue.TAMANO_LETRA)
        for fila in cursor:
            posiciony += Cla.dat_jue.TAMANO_LETRA * 2
            mostrar_texto(pantalla,f"{posicion}", Cla.dat_jue.ancho_ventana // 3.85, posiciony, Cla.dat_jue.TAMANO_LETRA)
            mostrar_texto(pantalla,f"{fila[1]}", Cla.dat_jue.ancho_ventana // 2.20, posiciony, Cla.dat_jue.TAMANO_LETRA)
            mostrar_texto(pantalla,f"{fila[2]}", Cla.dat_jue.ancho_ventana // 1.49, posiciony, Cla.dat_jue.TAMANO_LETRA)
            posicion += 1

def mostrar_texto(pantalla,texto, x, y, tamaño= Cla.dat_jue.TAMANO_LETRA, color=Col.WHITE):
    # Crear una instancia de la fuente
    font = pg.font.Font(vari.fuente, tamaño)

    # Renderizar el texto en una superficie
    text_surface = font.render(texto, True, color)

    # Copiar el texto en la ventana principal del juego
    pantalla.blit(text_surface, (x, y))

def mostrar_puntos_finales(pantalla,boton_jugar, boton_cruz):
    vari.grupo_puntaje_final.add(boton_cruz)
    Cla.dat_jue.puntuacion_final = True
    ventanas(pantalla)
    ver_puntajes(pantalla)
    boton_jugar.bool = False
    if Cla.dat_jue.win:
        ultimo_mombre(pantalla)
    if boton_cruz.bool:
        boton_cruz.apagar()
        Cla.dat_jue.puntuacion_final = False

#Sonidos
def reprodutor(numero):
    if Cla.dat_jue.traba_musical != numero:
        for musica in vari.musicas:
            musica.stop()
        vari.musicas[numero].play(-1)
    Cla.dat_jue.traba_musical = numero

#CONTROLADORES DE VOLUMEN
def control_volumen(volumen):
    for musica in vari.musicas:
            musica.set_volume(volumen)

def control_volumen_efectos(volumen):
    for sonido in vari.efectos_de_sonido:
            sonido.set_volume(volumen)

#DRAWS
def draws(pantalla):
    vari.grupo_puntaje_final.draw(pantalla)
    vari.botones.draw(pantalla)
    vari.disparos_enemigos.draw(pantalla)
    vari.disparos.draw(pantalla)
    vari.enemigos.draw(pantalla)
    vari.player.draw(pantalla)
    vari.explosiones.draw(pantalla)
    vari.botones_score.draw(pantalla)
    vari.grupo_settings.draw(pantalla)
    vari.volume.draw(pantalla)
    

#UPDATES
def updates():
    vari.grupo_puntaje_final.update()
    vari.disparos.update()
    vari.player.update()
    vari.enemigos.update()
    vari.explosiones.update()
    vari.disparos_enemigos.update() 
    vari.botones.update()     
    vari.botones_score.update()
    vari.grupo_settings.update()
    vari.volume.update()

#SALIR?
def salir():
    lista_de_eventos = pg.event.get()
    for evento in lista_de_eventos:
         if evento.type == pg.QUIT:
            sys.exit() 

def fondo_en_movimiento(pantalla,fondo):
    fondo_y_relativa = Cla.dat_jue.fondo_y % Cla.dat_jue.alto_ventana
    pantalla.blit(fondo, (0,fondo_y_relativa - Cla.dat_jue.alto_ventana))
    if fondo_y_relativa < Cla.dat_jue.ancho_ventana:
        pantalla.blit(fondo, (0,fondo_y_relativa)) 
    Cla.dat_jue.fondo_y += 5

def agregar_puntos_a_tabla():
    with sqlite3.connect(vari.sql_puntos) as conexion:
        try:
            sentencia = """ create table Puntajes
                            (
                                    id integer primary key autoincrement,
                                    nombre text,
                                    puntaje integer
                            )
                        """
            conexion.execute(sentencia)
            print("Se creo la tabla de Puntajes")
        except sqlite3.OperationalError:
            print("La tabla Puntajes ya existe")
        
        try:
            conexion.execute("insert into Puntajes (nombre, puntaje) values (?, ?)", (Cla.dat_jue.nombre, Cla.dat_jue.puntos_actuales))
            conexion.commit()
        except :
            print("Error")

def escribir():
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            sys.exit() 
        elif evento.type == pg.KEYDOWN:
                if evento.key == pg.K_BACKSPACE:
                    Cla.dat_jue.nombre = Cla.dat_jue.nombre[:-1]
                else:
                    Cla.dat_jue.nombre += evento.unicode

def pedir_nombre(pantalla,boton_ok):
    reprodutor(3)
    Cla.dat_jue.win = True
    ventanita(pantalla)
    mostrar_texto(pantalla,"INGRESE SU NOMBRE", Cla.dat_jue.ancho_ventana * 5 // 12, Cla.dat_jue.un_cauarto_ventana_y + Cla.dat_jue.TAMANO_LETRA, Cla.dat_jue.TAMANO_LETRA)
    pg.draw.rect(pantalla,(255,255,255), (Cla.dat_jue.ancho_ventana // 3 ,Cla.dat_jue.mitad_ventana_y,Cla.dat_jue.ancho_ventana // 3,Cla.dat_jue.mitad_ventana_y // 12))
    mostrar_texto(pantalla,Cla.dat_jue.nombre, Cla.dat_jue.ancho_ventana // 3, Cla.dat_jue.mitad_ventana_y, Cla.dat_jue.TAMANO_LETRA, Col.BLACK)            
    escribir()
    vari.grupo_puntaje_final.add(boton_ok)
    if boton_ok.bool:
        agregar_puntos_a_tabla()
        Cla.dat_jue.tipo_final = 0
        boton_ok.apagar() 
        boton_ok.kill()

def ultimo_mombre(pantalla):
    with sqlite3.connect(vari.sql_puntos) as conexion:
        cursor = conexion.cursor()

        # Obtener la última fila de la tabla "Puntajes"
        cursor.execute("SELECT * FROM Puntajes ORDER BY id DESC LIMIT 1")
        ultima_fila = cursor.fetchone()

        # Ejecutar la consulta para obtener la posición de la fila buscada
        cursor.execute("""
            SELECT COUNT(*) FROM (
                SELECT * FROM Puntajes ORDER BY puntaje DESC
            ) AS subquery
            WHERE puntaje > ? OR (puntaje = ? AND id < ?)
            """, (ultima_fila[2], ultima_fila[2], ultima_fila[0]))
        posicion = cursor.fetchone()[0]
        mostrar_texto(pantalla,f"TU:", Cla.dat_jue.ancho_ventana // 5, Cla.dat_jue.alto_ventana - Cla.dat_jue.un_cauarto_ventana_y, Cla.dat_jue.TAMANO_LETRA)
        mostrar_texto(pantalla,f"{posicion+1}", Cla.dat_jue.ancho_ventana // 3.85, Cla.dat_jue.alto_ventana - Cla.dat_jue.un_cauarto_ventana_y, Cla.dat_jue.TAMANO_LETRA)
        mostrar_texto(pantalla,f"{ultima_fila[1]}", Cla.dat_jue.ancho_ventana // 2.20, Cla.dat_jue.alto_ventana - Cla.dat_jue.un_cauarto_ventana_y, Cla.dat_jue.TAMANO_LETRA)
        mostrar_texto(pantalla,f"{ultima_fila[2]}", Cla.dat_jue.ancho_ventana // 1.49, Cla.dat_jue.alto_ventana - Cla.dat_jue.un_cauarto_ventana_y, Cla.dat_jue.TAMANO_LETRA)

def botones_atras_adelante(x,y, separacion = 0):
    boton_back = Cla.Boton("back", x, y)
    boton_forward = Cla.Boton("forward", x + Cla.dat_jue.ancho_ventana//13 + separacion, y)
    return boton_back, boton_forward

def menu_settings(pantalla,boton_back1, boton_forward1,boton_cruz,boton_setting,boton_music,boton_sound):
    vari.botones.empty()
    ventanas(pantalla)
    cambio = cambiar_resolucion(pantalla,boton_back1, boton_forward1)
    if cambio:
        cambio = False
        pantalla = pg.display.set_mode((Cla.dat_jue.ancho_ventana,Cla.dat_jue.alto_ventana))
        vari.grupo_settings.empty()
        Cla.dat_jue.cambio_res = True
    if boton_cruz.bool:
        boton_cruz.apagar()
        boton_setting.apagar()
        vari.volume.empty()
    control_musica(pantalla,boton_music,boton_sound)
    vari.grupo_settings.add(boton_music,boton_sound,boton_back1,boton_forward1,boton_cruz)

def control_musica(pantalla,boton_music,boton_sound):
    if boton_music.bool:
        boton_music.bool = False
        Cla.dat_jue.cam_vol = boton_music
        Cla.dat_jue.tipo_vol = Cla.dat_jue.music
        Cla.dat_jue.bandera_volumen = 0
        Cla.dat_jue.mantener_musica = not Cla.dat_jue.mantener_musica
        Cla.dat_jue.mantener_sonido= False
        vari.volume.empty()
    if boton_sound.bool:
        boton_sound.bool = False
        Cla.dat_jue.cam_vol = boton_sound
        Cla.dat_jue.tipo_vol = Cla.dat_jue.sound
        Cla.dat_jue.bandera_volumen = 0
        Cla.dat_jue.mantener_sonido= not Cla.dat_jue.mantener_sonido
        Cla.dat_jue.mantener_musica = False
        vari.volume.empty()
    if Cla.dat_jue.mantener_musica or Cla.dat_jue.mantener_sonido:
        control_musica_sonido(pantalla)
        
        

def control_musica_sonido(pantalla):
    if Cla.dat_jue.mantener_musica or Cla.dat_jue.mantener_sonido:
        tabla(pantalla,Cla.dat_jue.cam_vol.rect.centerx-Cla.dat_jue.cam_vol.tamaño[0]*0.5,Cla.dat_jue.cam_vol.rect.bottom,Cla.dat_jue.mitad_ventana_x 
              * 0.15,Cla.dat_jue.cam_vol.tamaño[1])
        if Cla.dat_jue.mantener_musica:
            mostrar_texto(pantalla,f"{int(Cla.dat_jue.music * 10)}", Cla.dat_jue.cam_vol.rect.centerx-Cla.dat_jue.cam_vol.tamaño[0]
                          *0.25, Cla.dat_jue.cam_vol.rect.bottom + Cla.dat_jue.cam_vol.rect.bottom * 0.05,Cla.dat_jue.TAMANO_LETRA*2)
        else:
            mostrar_texto(pantalla,f"{int(Cla.dat_jue.sound * 10)}", Cla.dat_jue.cam_vol.rect.centerx-Cla.dat_jue.cam_vol.tamaño[0]
                          *0.25, Cla.dat_jue.cam_vol.rect.bottom + Cla.dat_jue.cam_vol.rect.bottom * 0.05,Cla.dat_jue.TAMANO_LETRA*2)
        if Cla.dat_jue.bandera_volumen == 0:
            Cla.dat_jue.boton_down,Cla.dat_jue.boton_up = botones_atras_adelante(Cla.dat_jue.cam_vol.rect.centerx-Cla.dat_jue.cam_vol.tamaño[0],
                                                                                 Cla.dat_jue.cam_vol.rect.centery + Cla.dat_jue.cam_vol.tamaño[1],Cla.dat_jue.mitad_ventana_x * 0.15)  
            vari.volume.add(Cla.dat_jue.boton_down,Cla.dat_jue.boton_up)
        Cla.dat_jue.bandera_volumen = 1
        if Cla.dat_jue.boton_down.bool and Cla.dat_jue.tipo_vol > 0:
            if Cla.dat_jue.mantener_musica:
                Cla.dat_jue.music -= 0.1
            else:
                Cla.dat_jue.sound -= 0.1
            Cla.dat_jue.boton_down.bool = False         
        if Cla.dat_jue.boton_up.bool and Cla.dat_jue.tipo_vol < 1:
            Cla.dat_jue.boton_up.bool = False
            if Cla.dat_jue.mantener_musica:
                Cla.dat_jue.music += 0.1
            else:
                Cla.dat_jue.sound += 0.1
        

    

def cambiar_resolucion(pantalla,back, forward):
    cambio = False
    tabla(pantalla, Cla.dat_jue.ancho_ventana * 0.35,Cla.dat_jue.alto_ventana * 0.55,Cla.dat_jue.mitad_ventana_x * 0.6, Cla.dat_jue.mitad_ventana_y * 0.2)
    mostrar_texto(pantalla,f"{vari.anc_pant[Cla.dat_jue.res_actual]} x {vari.alt_pant[Cla.dat_jue.res_actual]}", Cla.dat_jue.ancho_ventana * 0.4, Cla.dat_jue.alto_ventana * 0.57, Cla.dat_jue.TAMANO_LETRA * 2)
    if back.bool and Cla.dat_jue.res_actual > 0:
        back.bool = False
        Cla.dat_jue.res_actual -= 1
        cambio = True
    if forward.bool and Cla.dat_jue.res_actual < 4:
        forward.bool = False
        Cla.dat_jue.res_actual += 1
        cambio = True
    if cambio:
        Cla.dat_jue.ancho_ventana = vari.anc_pant[Cla.dat_jue.res_actual]
        Cla.dat_jue.alto_ventana = vari.alt_pant[Cla.dat_jue.res_actual]
    return cambio
    

def vaciar_grupos(disparos,disparos_enemigos,player,enemigos,explosiones,botones,botones_score,grupo_puntaje_final,grupo_settings):
    disparos.empty()
    disparos_enemigos.empty()
    player.empty()
    enemigos.empty()
    explosiones.empty()
    botones.empty()
    botones_score.empty()
    grupo_puntaje_final.empty()
    grupo_settings.empty()

def menu_principal(boton_jugar,boton_puntos,boton_setting,boton_salir):
    reprodutor(0)
    vari.botones.add(boton_jugar,boton_puntos,boton_setting,boton_salir)
    vari.grupo_puntaje_final.empty()
    vari.grupo_settings.empty()
    Cla.dat_jue.reset()
    if boton_salir.bool:
        sys.exit() 