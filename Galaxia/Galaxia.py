import pygame as pg

# Importar archivos
import clases as Cla
import funciones as func
import variables as vari


FPS = 60

#________________________________________________________________

pg.init()

pantalla = pg.display.set_mode((Cla.dat_jue.ancho_ventana,Cla.dat_jue.alto_ventana))
pg.display.set_caption("Galaxy")

icono = pg.image.load(vari.imagen_icono)
pg.display.set_icon(icono)

clock = pg.time.Clock()

ultimo_tick = pg.time.get_ticks()

while True:
    ################################
    func.control_volumen(Cla.dat_jue.music)
    func.control_volumen_efectos(Cla.dat_jue.sound)

    func.salir()
      

    if Cla.dat_jue.cambio_res:
    #OBJETOS
        #BOTONES
        boton_muestra = Cla.Boton("play",0,0)
        boton_jugar = Cla.Boton("play", Cla.dat_jue.ancho_ventana * 0.5, Cla.dat_jue.alto_ventana*0.4,2)
        boton_salir = Cla.Boton("exit", Cla.dat_jue.ancho_ventana * 0.5, Cla.dat_jue.alto_ventana*0.6,2)
        boton_puntos = Cla.Boton("score", Cla.dat_jue.ancho_ventana - boton_muestra.rect.width // 2, boton_muestra.rect.height // 2)
        boton_cruz = Cla.Boton("cruz", Cla.dat_jue.ancho_ventana - Cla.dat_jue.ancho_ventana//6, Cla.dat_jue.alto_ventana//6)
        boton_ok = Cla.Boton("ok", Cla.dat_jue.ancho_ventana * 0.5 , Cla.dat_jue.alto_ventana * 0.75)
        boton_setting = Cla.Boton("setting",Cla.dat_jue.ancho_ventana - boton_muestra.rect.width * 1.5, boton_muestra.rect.height // 2)
        boton_music = Cla.Boton("music", Cla.dat_jue.ancho_ventana * 0.31 , Cla.dat_jue.alto_ventana * 0.35)
        boton_sound = Cla.Boton("sound", Cla.dat_jue.ancho_ventana * 0.69 , Cla.dat_jue.alto_ventana * 0.35)
        boton_back1,boton_forward1 = func.botones_atras_adelante(Cla.dat_jue.ancho_ventana * 0.31,Cla.dat_jue.alto_ventana * 0.6,Cla.dat_jue.ancho_ventana * 0.5 * 0.60)
        func.vaciar_grupos(vari.disparos,vari.disparos_enemigos,vari.player,vari.enemigos,vari.explosiones,vari.botones,vari.botones_score,vari.grupo_puntaje_final,vari.grupo_settings)
        Cla.dat_jue.cambio_res = False
        Cla.dat_jue.mantener_setting += 1
        Cla.dat_jue.resolucion()
        fondo = pg.image.load(vari.imagen_fondo).convert()
        fondo = pg.transform.scale(fondo,(Cla.dat_jue.ancho_ventana,Cla.dat_jue.alto_ventana))
        #JUGADOR
        jugador = Cla.Jugador()

        if Cla.dat_jue.mantener_setting > 1:
            boton_setting.bool = True
    #fondo
    func.fondo_en_movimiento(pantalla,fondo)
    
    #IF de el juego entero
    if boton_jugar.bool and not Cla.dat_jue.puntuacion_final :
        #si te moris:
        
        if Cla.dat_jue.vida_jugador <= 0:
            func.sin_vida_parte_uno(jugador)
            func.sin_vida_parte_dos(jugador)
            Cla.dat_jue.puntuacion_final  = func.sin_vida_parte_tres(jugador)


        else:
            func.reprodutor(1)
            if not vari.enemigos:
                for i in range(Cla.dat_jue.cant_enemigos):
                    enemigo_nuevo = Cla.Enemigos()  
                    vari.enemigos.add(enemigo_nuevo)
            if not vari.player:
                vari.player.add(jugador)

            #Timer
            tick_actual = pg.time.get_ticks()
            if tick_actual - ultimo_tick >= 1000 and Cla.dat_jue.tiempo_de_juego != 0:
                ultimo_tick = func.cuenta_regresiva(tick_actual,ultimo_tick,boton_jugar)



            ###############################
            colision = pg.sprite.spritecollide(jugador, vari.enemigos, False, pg.sprite.collide_circle)
            colision_balas = pg.sprite.groupcollide(vari.disparos, vari.enemigos, True, True, pg.sprite.collide_circle)
            colision_balas_enemigas = pg.sprite.spritecollide(jugador, vari.disparos_enemigos, True, pg.sprite.collide_circle)
            func.colision_disparos_enemigos(colision_balas_enemigas,enemigo_nuevo,jugador)
            func.colisiones_melee(colision,enemigo_nuevo,jugador)   
            func.colision_disparos_aliados(colision_balas,enemigo_nuevo,vari.explosiones)

            puntos_str = str(Cla.dat_jue.puntos_actuales)

            func.mostrar_texto(pantalla,f"POINTS = {puntos_str.zfill(7)}", 0, 0)
            func.mostrar_texto(pantalla,f"HP %{Cla.dat_jue.vida_jugador}", Cla.dat_jue.ancho_ventana * 0.90, Cla.dat_jue.alto_ventana - Cla.dat_jue.TAMANO_LETRA *2)
            func.mostrar_texto(pantalla,f"TIME = {Cla.dat_jue.tiempo_de_juego}", Cla.dat_jue.ancho_ventana * 0.45, 0)
            vari.botones.empty()
        
        
    #MENU ENTERO
     #PUNTOS  
    elif not Cla.dat_jue.puntuacion_final:
        if boton_puntos.bool:
            vari.botones.empty()
            vari.botones_score.add(boton_cruz)
            func.ventanas(pantalla)
            try:
                func.ver_puntajes(pantalla)
            except:
                func.mostrar_texto(pantalla,"SIN DATOS", Cla.dat_jue.ancho_ventana * 0.40, Cla.dat_jue.alto_ventana * 0.45, Cla.dat_jue.TAMANO_LETRA * 2)
            
            if boton_cruz.bool:
                boton_puntos.apagar()
                boton_cruz.apagar()
                vari.botones_score.empty()

        #SETTINGS
        elif boton_setting.bool:
            func.menu_settings(pantalla,boton_back1, boton_forward1,boton_cruz,boton_setting,boton_music,boton_sound)
        else:
            #Menu Principal
            func.menu_principal(boton_jugar,boton_puntos,boton_setting,boton_salir)
    #puntos
    elif Cla.dat_jue.puntuacion_final and not vari.explosiones:
        if Cla.dat_jue.tipo_final == 0:
            func.mostrar_puntos_finales(pantalla,boton_jugar, boton_cruz)
        elif Cla.dat_jue.tipo_final == 1:
            func.pedir_nombre(pantalla,boton_ok)
    #DRAWS
    func.draws(pantalla)

    #UPDATES
    func.updates()
    pg.display.flip()
    clock.tick(FPS)
    



pg.quit()