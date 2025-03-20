import arcade
from random import *

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

class Rectangle:#clase para los rectángulos
    def __init__(self,rect_x,rect_y,rect_width,rect_height,color):
        self.rect_x,self.rect_y,self.rect_width,self.rect_height,self.color=rect_x,rect_y,rect_width,rect_height,color
    def draw(self):
        arcade.draw_rectangle_filled(self.rect_x, self.rect_y, self.rect_width, self.rect_height, self.color)

class Out_line:#clase para el borde
    def __init__(self,line_x,line_y,line_width,line_height,line_color,line_g):
        self.line_x,self.line_y,self.line_width,self.line_height,self.line_color,self.line_g=line_x,line_y,line_width,line_height,line_color,line_g
    def draw(self):
        arcade.draw_rectangle_outline(self.line_x, self.line_y, self.line_width, self.line_height, self.line_color,self.line_g)

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.mostrar_mensaje = True
        self.color_transparente = (0, 200, 100, 150)
        arcade.set_background_color(arcade.color.ENGLISH_GREEN)

        #listas para los rectángulos
        self.rect_list=[]
        self.outline=[]
        #añadir los rectángulos a las listas (relleno y contorno)
        posiciones = [(500, 350, 200, 200), (700, 300, 200, 100), (300, 300, 200, 100), (300, 400, 200, 100),
                      (700, 400, 200, 100)]
        for pos in posiciones:
            self.rect_list.append(Rectangle(*pos, self.color_transparente))
            self.outline.append(Out_line(*pos, arcade.color.BLACK, 5))
        #variables usadas para la lógica del juego
        #jugador
        self.eleccion_jug = None
        self.posicion_jug = None
        self.gol_jug = 0
        self.turno_jug=True
        # bot
        self.eleccion_IA = None
        self.posicion_IA = None
        self.gol_IA = 0
        self.turno_IA=False
        # ronda y numero límite de rondas
        self.ronda = 1
        self.final = 5
        self.dibujar_rectangulo=True
        self.mensaje="Choose your SHOT!"
        self.clicks=0
        #Mostrar mensajes en pantalla
        self.textos_IA=False
        self.textos_IA2=False
        self.texto_gol=False
        self.texto_parada=False
        self.mensaje_final=False
        self.mf=""

    def on_draw(self):
        self.clear()
        # Dibujar el área en la que queremos detectar clics (ejemplo: un rectángulo)
        if self.dibujar_rectangulo:
            for rect in self.rect_list:
                rect.draw()
            for out in self.outline:
                out.draw()
        # Dibujar marcador

        arcade.draw_text(f"Ronda: {self.ronda}", 50, SCREEN_HEIGHT - 50, arcade.color.WHITE, 20)
        arcade.draw_text(f"Jugador: {self.gol_jug} - IA: {self.gol_IA}", 50, SCREEN_HEIGHT - 80,
                         arcade.color.WHITE, 20)

        #Listado de los mensajes que aparecen en pantalla
        if self.mostrar_mensaje:
            if not self.turno_IA:
                arcade.draw_text(self.mensaje, 390, 500, arcade.color.CYAN, 20)
            elif self.turno_IA:
                arcade.draw_text(self.mensaje, 390, 500, arcade.color.RED, 20)
        if self.textos_IA:
            arcade.draw_text("AI choosing move...", 395, 600, arcade.color.BLACK, 20)
        elif self.textos_IA2:
            arcade.draw_text("AI choosing shot...", 395, 600, arcade.color.BLACK, 20)
        if self.texto_gol:
            arcade.draw_text("GOAL", 465, 550, arcade.color.GOLD, 20)
        if self.texto_parada:
            arcade.draw_text("SAVED", 465, 550, arcade.color.SILVER, 20)
        if self.mensaje_final:
            arcade.draw_text(self.mf, 405, 450, arcade.color.WHITE, 30)
            arcade.draw_text("Match ended", 380, 350, arcade.color.WHITE, 30)


    def on_mouse_press(self, x, y, button, modifiers):#función que detecta los clicks y ejecuta funciones varias
        # bloquear el clickeo para no registrar más entradas hasta que se permita
        if not self.turno_jug:
            return

        valid_click = False

            # Definir posiciones de rectángulos
        opciones = [(500, 350, 200, 200, 2, None), (700, 300, 200, 100, 3, 2),
                    (300, 300, 200, 100, 1, 2), (300, 400, 200, 100, 1, 1),
                    (700, 400, 200, 100, 3, 1)]

        for rx, ry, rw, rh, eleccion, posicion in opciones:
            if (rx - rw / 2) <= x <= (rx + rw / 2) and (ry - rh / 2) <= y <= (ry + rh / 2):
                self.eleccion_jug = eleccion
                self.posicion_jug = posicion
                self.dibujar_rectangulo = False
                self.turno_jug = False
                valid_click = True
                print(self.eleccion_jug,self.posicion_jug)
                break


        if not valid_click:
            return
        else:
            self.clicks += 1

        #comienzo de la lógica de la IA
        if not self.turno_IA and self.clicks%2 != 0:
            arcade.schedule(self.bot_action_keeper,0)
        elif self.clicks%2==0 and self.clicks >0:
            self.turno_IA=False
            self.textos_IA2=True
            self.mostrar_mensaje=False
            arcade.schedule(self.comprobar_acciones_parada, 2)

    def generate_bot_choice(self):
        """Genera la elección y posición aleatoria del bot."""
        choice = randint(1, 3)
        position = randint(1, 2) if choice in (1, 3) else None
        return choice, position

    def bot_action_keeper(self,delta_time):#función para la lógica de portero de la IA
        """La IA Actúa como portero"""
        self.eleccion_IA = 0
        self.posicion_IA = 0
        self.textos_IA=True
        self.mostrar_mensaje=False
        self.eleccion_IA, self.posicion_IA = self.generate_bot_choice()
        arcade.unschedule(self.bot_action_keeper)
        arcade.schedule(self.comprobar_acciones_tiro, 2)
        arcade.schedule(self.bot_action_shoot, 3)

    def bot_action_shoot(self,delta_time):#función para la lógica de delantero/tirador de la IA
        """La IA Actúa como tirador"""
        self.mostrar_mensaje=True
        self.texto_gol=False
        self.texto_parada=False
        self.mensaje="Choose your MOVE!"
        self.eleccion_jug=None
        self.posicion_jug=None
        self.eleccion_IA, self.posicion_IA = self.generate_bot_choice()
        self.turno_jug=True
        self.dibujar_rectangulo=True
        arcade.unschedule(self.bot_action_shoot)

    def check_shot_result(self, shooter_choice, shooter_position, keeper_choice, keeper_position):
        """
        Devuelve una tupla (goal, saved):
          - goal: True si se marca gol.
          - saved: True si el disparo es parado.
        """
        if shooter_choice != keeper_choice:
            return True, False  # Gol anotado
        else:
            if shooter_choice in (1, 3):
                if shooter_position == keeper_position:
                    return False, True  # Parada
                else:
                    return True, False
            elif shooter_choice == 2:
                return False, True  # Siempre es parada

    def comprobar_acciones_tiro(self, delta_time):
        """Comprueba el resultado del tiro del jugador."""
        self.textos_IA = False
        goal, saved = self.check_shot_result(self.eleccion_jug, self.posicion_jug, self.eleccion_IA, self.posicion_IA)
        if goal:
            self.texto_gol = True
            self.gol_jug += 1
        else:
            self.texto_parada = True
        arcade.unschedule(self.comprobar_acciones_tiro)

    def comprobar_acciones_parada(self, delta_time):
        """Comprueba el resultado cuando el bot dispara y el jugador defiende."""
        self.textos_IA2 = False
        goal, saved = self.check_shot_result(self.eleccion_IA, self.posicion_IA, self.eleccion_jug, self.posicion_jug)
        if goal:
            self.texto_gol = True
            self.gol_IA += 1
        else:
            self.texto_parada = True
        arcade.unschedule(self.comprobar_acciones_parada)
        arcade.schedule(self.reset_set, 1)


    def reset_set(self,delta_time):#función para verificar si ha acabado el partido y, en caso contrario, resetear variables a su estado inicial para la siguiente ronda
        self.check_final_conditions()
        if self.ronda >= self.final:
            self.texto_gol = False
            self.texto_parada = False
            self.mostrar_mensaje = False
            self.mensaje_final=True
            if self.gol_jug > self.gol_IA:
                self.mf="You win!"
            elif self.gol_jug < self.gol_IA:
                self.mf="You lose"


            arcade.unschedule(self.reset_set)
            return  # No seguir si el juego ha terminado
        #reseteo de variables
        self.ronda += 1
        self.clicks=0
        self.texto_gol=False
        self.texto_parada=False
        self.mostrar_mensaje=True
        self.turno_jug=True
        self.dibujar_rectangulo=True
        self.mensaje = "Choose your SHOT!"
        arcade.unschedule(self.reset_set)

    def check_final_conditions(self):
        """Funcion para comprobar resultados específicos y evitar rondas innecesarias"""

        # Empate: se extiende el juego hasta desempate
        if self.ronda >= 5 and self.gol_jug == self.gol_IA:
            self.final += 1
        # Finalización anticipada en ciertos casos
        if self.ronda >= 3 and ((self.gol_jug == 3 and self.gol_IA == 0) or (self.gol_jug == 0 and self.gol_IA == 3)):
            self.ronda = self.final
        if self.ronda >= 4 and (
                (self.gol_jug == 4 and self.gol_IA in (1, 2)) or (self.gol_IA == 4 and self.gol_jug in (1, 2))):
            self.ronda = self.final
        if self.ronda >= 4 and ((self.gol_jug == 3 and self.gol_IA == 1) or (self.gol_jug == 1 and self.gol_IA == 3)):
            self.ronda = self.final

def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, "Penalti inazuma eleven")
    arcade.run()

main()

