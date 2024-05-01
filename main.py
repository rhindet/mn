
import pygame_gui
import random
import os
import pygame
# Define las dimensiones de la pantalla y el tamaño de las cartas
ANCHO = 1300
ALTO = 700
SCREEN_SIZE = (ANCHO, ALTO)
CARTA_ANCHO = 250
CARTA_ALTO = 100
FPS = 50
GAP = 20
# Define los colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
# Define la información de los niveles
niveles = [
    {'nombre': 'Fácil', 'cartas': 4, 'tiempo': 60},
    {'nombre': 'Medio', 'cartas': 8, 'tiempo': 45},
    {'nombre': 'Difícil', 'cartas': 20, 'tiempo': 30}
]

# Selecciona el nivel actual (empezamos en el nivel 0)
nivel_actual = 0
todos_los_niveles_completados = False
# Define las imágenes
IMAGENES = ['imagen1.png', 'imagen2.png', 'imagen3.png', 'imagen4.png', 'imagen5.png', 'imagen6.png','imagen7.png', 'imagen8.png', 'imagen9.png', 'imagen10.png', 'imagen11.png', 'imagen12.png']

# Define las preguntas y respuestas del Kahoot
preguntas_respuestas = [
    {
        'pregunta': '¿Cuál es el método numérico para encontrar raíces de ecuaciones?\n',
        'respuestas': ['Método de Bisección', 'Método de Newton-Raphson', 'Método de Euler', 'Método de Gauss-Seidel'],
        'correcta': 'Método de Newton-Raphson'
    },
    {
        'pregunta': '¿Cuál es el método numérico para interpolar datos?\n',
        'respuestas': ['Método de Lagrange', 'Método de Simpson', 'Método de Monte Carlo', 'Método de Runge-Kutta'],
        'correcta': 'Método de Lagrange'
    },
    {
        'pregunta': '¿Qué método se utiliza para resolver ecuaciones diferenciales ordinarias\nmediante la estimación de la pendiente en puntos sucesivos?\n',
        'respuestas': ['Método de Bisección', 'Método de Newton-Raphson', 'Método de Euler', 'Método de Gauss-Seidel'],
        'correcta': 'Método de Euler'
    },
    {
        'pregunta': '¿Cuál es el método utilizadopara resolver sistemas de ecuaciones lineales\nmediante la iteración hasta alcanzar una solución convergente?\n',
        'respuestas': ['Método de Bisección', 'Método de Newton-Raphson', 'Método de Euler', 'Método de Gauss-Seidel'],
        'correcta': 'Método de Gauss-Seidel'
    },
    {
        'pregunta': '¿Qué método numérico se emplea para calcular la integral de una función\naproximando áreas bajo una curva?\n',
        'respuestas': ['Método del Trapecio', 'Método de Simpson', 'Método de Euler', 'Método de Runge-Kutta'],
        'correcta': 'Método del Trapecio'
    },
    {
        'pregunta': '¿Cuál es el método que utiliza polinomios de grado bajo para ajustarse a un conjunto de datos?\n',
        'respuestas': ['Interpolación de Lagrange', 'Interpolación de Newton', 'Mínimos Cuadrados',
                       'Regresión Polinómica'],
        'correcta': 'Mínimos Cuadrados'
    },
    {
        'pregunta': '¿Qué técnica numérica se utiliza para estimar el valor de una función\nen un punto basándose en valores cercanos conocidos?\n',
        'respuestas': ['Interpolación', 'Regresión', 'Integración', 'Diferenciación'],
        'correcta': 'Interpolación'
    },
    {
        'pregunta': '¿Cuál es el método utilizado para aproximar la derivada de una función\nmediante diferencias finitas?\n',
        'respuestas': ['Diferenciación Numérica', 'Diferenciación Analítica', 'Interpolación de Lagrange',
                       'Regresión Lineal'],
        'correcta': 'Diferenciación Numérica'
    },
    {
        'pregunta': '¿Qué método numérico se emplea para resolver ecuaciones diferenciales parciales\nmediante una aproximación por pasos?\n',
        'respuestas': ['Método de Euler', 'Método de Runge-Kutta', 'Método de Diferencias Finitas',
                       'Método de Gauss-Seidel'],
        'correcta': 'Método de Diferencias Finitas'
    },
    {
        'pregunta': '¿Cuál es el método que ajusta una curva a un conjunto de datos minimizando la suma de los cuadrados de las diferencias entre los datos y la curva ajustada?\n',
        'respuestas': ['Interpolación de Lagrange', 'Interpolación de Newton', 'Mínimos Cuadrados', 'Regresión Lineal'],
        'correcta': 'Mínimos Cuadrados'
    },
    # Puedes continuar agregando más preguntas aquí
]

# Inicializa Pygame
pygame.init()
pygame.mixer.init()
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Memorama")
reloj = pygame.time.Clock()

# Carga las imágenes
imagenes_cargadas = [pygame.image.load(img) for img in IMAGENES]
imagenes_cargadas = [pygame.transform.scale(img, (CARTA_ANCHO, CARTA_ALTO)) for img in imagenes_cargadas]

# Duplica las imágenes para emparejarlas
cartas = imagenes_cargadas * 2
random.shuffle(cartas)


# Define la clase para las cartas
class Carta:
    def __init__(self, imagen, x, y):
        self.imagen = imagen
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.visible = False
        self.matched = False

    def draw(self):
        if self.visible or self.matched:
            ventana.blit(self.imagen, self.rect)
        else:
            pygame.draw.rect(ventana, BLANCO, self.rect)


# Crea las cartas
tablero = []
x_pos = 100
y_pos = 100
for imagen in cartas:

    carta = Carta(imagen, x_pos, y_pos)
    tablero.append(carta)
    x_pos += CARTA_ANCHO + GAP  # Añade el espacio entre cartas
    if x_pos >= ANCHO - CARTA_ANCHO:
        x_pos = 100
        y_pos += CARTA_ALTO + GAP


def abrir_pantalla_en_blanco():
    os.system("start \"\" blank.html")
def crear_nivel_10_cartas():
    # Selecciona 5 imágenes diferentes para el nuevo nivel
    imagenes_seleccionadas = random.sample(imagenes_cargadas, 5)
    # Duplica cada imagen para formar pares de tarjetas idénticas
    cartas = imagenes_seleccionadas * 2  # Duplica cada imagen
    random.shuffle(cartas)
    # Crea las cartas
    tablero.clear()  # Limpiar el tablero antes de añadir nuevas cartas
    x_pos = 100
    y_pos = 100
    for imagen in cartas:  # Utiliza todas las imágenes seleccionadas
        carta = Carta(imagen, x_pos, y_pos)
        tablero.append(carta)
        x_pos += CARTA_ANCHO + GAP  # Añade el espacio entre cartas
        if x_pos >= ANCHO - CARTA_ANCHO:
            x_pos = 100
            y_pos += CARTA_ALTO + GAP


def avanzar_nivel():

    global nivel_actual, nivel_label
    nivel_actual += 1
    nivel_label.set_text(f"Nivel: {nivel_actual}")


def show_perdiste_screen():
    # Inicializar la pantalla
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("¡Perdiste!")

    # Inicializar el administrador de GUI de pygame_gui
    gui_manager = pygame_gui.UIManager(SCREEN_SIZE)
    # Cargar la imagen de fondo
    background_image = pygame.image.load("gameOver.jpeg").convert()  # Cambia "gameOver.jpg" por la ruta de tu imagen

    # Escalar la imagen de fondo para que se ajuste a la pantalla
    background_image = pygame.transform.scale(background_image, SCREEN_SIZE)

    # Crear un botón para volver a la pantalla principal
    button_rect = pygame.Rect(550, 100, 200, 50)
    return_button = pygame_gui.elements.UIButton(relative_rect=button_rect,
                                                 text='Volver a la pantalla principal',
                                                 manager=gui_manager)

    # Bucle principal
    clock = pygame.time.Clock()
    running = True
    while running:
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == return_button:
                        # Aquí puedes agregar la lógica para volver a la pantalla principal

                        running = False  # Para salir del bucle y volver a la pantalla principal
                        pantalla_principal()
            gui_manager.process_events(event)

        gui_manager.update(clock.tick(60) / 1000.0)

        # Dibujar la imagen de fondo en la pantalla
        screen.blit(background_image, (0, 0))

        # Dibujar la interfaz gráfica de usuario
        gui_manager.draw_ui(screen)

        # Actualizar la pantalla
        pygame.display.flip()


# Define la función principal del juego
def main():
    global nivel_actual, terminado, nivel_label

    terminado = False  # Inicializa terminado aquí
    nivel_label = None

    fondo = pygame.image.load("fondo_memo.jpeg")
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

    while not terminado:
        # Inicializa el nivel actual
        nivel_info = niveles[nivel_actual]
        num_cartas = nivel_info['cartas']
        tiempo_limite = nivel_info['tiempo']

        # Si es el nivel 1, selecciona solo 4 imágenes
        if nivel_actual == 0:

            imagenes_seleccionadas = random.sample(imagenes_cargadas, num_cartas // 2)
            cartas = imagenes_seleccionadas + imagenes_seleccionadas

        elif nivel_actual == 1:
            nivel_label.set_text("Nivel : 1")

            imagenes_seleccionadas = random.sample(imagenes_cargadas, num_cartas // 2)
            cartas = imagenes_seleccionadas + imagenes_seleccionadas

        elif nivel_actual == 2:
            nivel_label.set_text("Nivel : 2")
            imagenes_seleccionadas = random.sample(imagenes_cargadas, num_cartas // 2)
            cartas = imagenes_seleccionadas + imagenes_seleccionadas

        # Crea las cartas
        tablero.clear()  # Limpiar el tablero antes de añadir nuevas cartas
        x_pos = 100
        y_pos = 100
        for imagen in cartas[:num_cartas]:  # Usar solo las primeras "num_cartas" imágenes
            carta = Carta(imagen, x_pos, y_pos)
            tablero.append(carta)
            x_pos += CARTA_ANCHO + GAP  # Añade el espacio entre cartas
            if x_pos >= ANCHO - CARTA_ANCHO:
                x_pos = 100
                y_pos += CARTA_ALTO + GAP

        # Restablece el juego para el nuevo nivel


        # Registra el tiempo inicial
        tiempo_inicial = pygame.time.get_ticks() + 60000

        # Restablece la puntuación y los intentos
        puntuacion = 0
        intentos = 0

        # Define la interfaz de usuario
        manager = pygame_gui.UIManager((ANCHO, ALTO))
        nivel_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((ANCHO // 2 - 50, 20), (200, 100)),
                                                  text=f'Nivel: {nivel_actual.__str__()}',
                                                  manager=manager)
        boton_reiniciar = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((ANCHO // 2 - 150, 10), (200, 30)),
                                                       text='Reiniciar Juego',
                                                       manager=manager)

        boton_reiniciar_todo = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((ANCHO // 2 + 50, 10), (200, 30)),
                                                            text='Ir a menú',
                                                            manager=manager)

        # Crea la etiqueta de tiempo una vez fuera del bucle principal
        cronometro_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((ANCHO // 2 - 50, 20), (200, 50)),
                                                       text='',
                                                       manager=manager)
        # Crea la etiqueta de tiempo una vez fuera del bucle principal
        nivel_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((ANCHO // 2 - 50, 20), (200, 70)),
                                                       text='',
                                                       manager=manager)

        carta_seleccionada = None
        carta_seleccionada2 = None
        puntuacion = 0
        intentos = 0
        terminado = False
        # Definir un contenedor para el contenido desplazable
        scrollable_panel_rect = pygame.Rect(100, 100, 400, 400)

        while not terminado:

            # Calcula el tiempo transcurrido desde el inicio del juego

            tiempo_transcurrido = max(0, (tiempo_inicial - pygame.time.get_ticks()) // 1000)

            if tiempo_transcurrido <= 0:
                terminado = True
                show_perdiste_screen()
            for event in pygame.event.get():
                manager.process_events(event)

                if event.type == pygame.QUIT:
                    terminado = True
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == boton_reiniciar:
                            reiniciar_juego()
                        if event.ui_element == boton_reiniciar_todo:
                            reiniciar_todo()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for carta in tablero:
                        if carta.rect.collidepoint(event.pos) and not carta.visible and not carta.matched:
                            carta.visible = True
                            if carta_seleccionada is None:
                                carta_seleccionada = carta
                            else:
                                carta_seleccionada2 = carta

            ventana.blit(fondo, (0, 0))

            for carta in tablero:
                carta.draw()

            # Actualiza el texto de la etiqueta de tiempo en cada iteración del bucle
            cronometro_texto = 'Tiempo: {} seg'.format(tiempo_transcurrido)
            cronometro_label.set_text(cronometro_texto)

            manager.update(0)
            manager.draw_ui(ventana)

            pygame.display.flip()

            # Comprobar si se han completado todas las cartas
            if carta_seleccionada and carta_seleccionada2:
                pygame.time.wait(500)
                if carta_seleccionada.imagen == carta_seleccionada2.imagen:
                    carta_seleccionada.matched = True
                    carta_seleccionada2.matched = True
                    puntuacion += 1
                else:
                    carta_seleccionada.visible = False
                    carta_seleccionada2.visible = False
                carta_seleccionada = None
                carta_seleccionada2 = None
                intentos += 1

            if puntuacion == len(tablero) / 2:
                if nivel_actual < len(niveles) - 1:  # Verifica si no es el último nivel
                    print("avanza desde main")
                    avanzar_nivel()  # Llama a la función avanzar_nivel()
                    break  # Sale del bucle interno para iniciar el siguiente nivel
                else:
                    # Si se completan todos los niveles, muestra la pantalla de felicitaciones
                    pantalla_felicidades(puntuacion,cronometro_texto)
                    terminado = True

    pygame.quit()

def crear_nivel_6_cartas():
    print("6cartas ")
    # Selecciona 3 imágenes diferentes para el nuevo nivel
    imagenes_seleccionadas = random.sample(imagenes_cargadas, 3)
    # Duplica cada imagen para formar pares de tarjetas idénticas
    cartas = imagenes_seleccionadas * 2  # Duplica cada imagen
    random.shuffle(cartas)
    # Crea las cartas
    tablero.clear()  # Limpiar el tablero antes de añadir nuevas cartas
    x_pos = 100
    y_pos = 100
    for imagen in cartas:  # Utiliza todas las imágenes seleccionadas
        carta = Carta(imagen, x_pos, y_pos)
        tablero.append(carta)
        x_pos += CARTA_ANCHO + GAP  # Añade el espacio entre cartas
        if x_pos >= ANCHO - CARTA_ANCHO:
            x_pos = 100
            y_pos += CARTA_ALTO + GAP




# Define la función para la pantalla principal
def pantalla_principal():
    manager = pygame_gui.UIManager((ANCHO, ALTO))

    fondo_inicio = pygame.image.load('fondo_inicio.jpg')
    fondo_inicio = pygame.transform.scale(fondo_inicio, (ANCHO, ALTO))

    # Crear superficie para el texto con fondo negro y opacidad
    texto_bienvenida = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((ANCHO // 2 - 200, ALTO // 2 - 100), (400, 200)),
        text='¡Bienvenido a Métodos Numéricos!',
        manager=manager)
    fondo_texto = pygame.Surface((texto_bienvenida.rect.width, texto_bienvenida.rect.height))
    fondo_texto.set_alpha(150)  # Ajusta la opacidad (0 transparente, 255 opaco)
    fondo_texto.fill(NEGRO)
    ventana.blit(fondo_inicio, (0, 0))
    ventana.blit(fondo_texto, texto_bienvenida.rect.topleft)
    manager.draw_ui(ventana)

    boton_jugar_memorama = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((ANCHO // 2 - 100, ALTO // 2 + 50), (200, 50)),
        text='Memorama',
        manager=manager)

    boton_jugar_kahoot = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((ANCHO // 2 - 100, ALTO // 2 + 120), (200, 50)),
        text='Preguntas',
        manager=manager)

    boton_jugar_con_Imagenes = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((ANCHO // 2 - 100, ALTO // 2 + 200), (200, 50)),
        text='Ejercicios',
        manager=manager)



    running = True
    while running:
        time_delta = reloj.tick(FPS) / 1000.0
        for event in pygame.event.get():
            manager.process_events(event)
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.USEREVENT:
                if event.ui_element == boton_jugar_memorama and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    running = False
                    main()

                if event.ui_element == boton_jugar_kahoot and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    running = False
                    jugar_kahoot()
                if event.ui_element == boton_jugar_con_Imagenes and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                     running = False
                     jugar_juego_con_imagenes()



        manager.update(time_delta)
        manager.draw_ui(ventana)
        pygame.display.flip()

    pygame.quit()


# Define la función para la pantalla de felicitaciones
def pantalla_felicidades(puntuacion,tiempo):
    pygame.init()
    pygame.mixer.init()
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Felicidades")

    # Define la interfaz de usuario
    manager = pygame_gui.UIManager((ANCHO, ALTO))

    fondo_felicidades = pygame.image.load('fondo_felicidades.jpeg')
    fondo_felicidades = pygame.transform.scale(fondo_felicidades, (ANCHO, ALTO))

    # Crea una superficie para el texto con fondo negro y opacidad
    texto_felicidades = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((ANCHO // 2 - 150, ALTO // 2 - 100), (300, 200)),
        text='¡Felicidades!',
        manager=manager)
    texto_Tiempo = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((ANCHO // 2 - 150, ALTO // 2 - 100), (300, 250)),
        text=f'Tu tiempo fue {tiempo}',
        manager=manager)
    texto_Puntos= pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((ANCHO // 2 - 150, ALTO // 2 - 100), (300, 300)),
        text=f'Tu puntuacion fue {puntuacion}',
        manager=manager)
    fondo_texto = pygame.Surface((texto_felicidades.rect.width, texto_felicidades.rect.height))
    fondo_texto.set_alpha(200)  # Ajusta la opacidad (0 transparente, 255 opaco)
    fondo_texto.fill(NEGRO)

    ventana.blit(fondo_felicidades, (0, 0))
    ventana.blit(fondo_texto, texto_felicidades.rect.topleft)
    manager.draw_ui(ventana)

    # Crea una etiqueta de botón para jugar de nuevo
    boton_jugar_de_nuevo = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((ANCHO // 2 - 100, ALTO // 2 + 50), (200, 100)),
        text='Jugar de Nuevo',
        manager=manager)

    running = True
    while running:
        time_delta = reloj.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == boton_jugar_de_nuevo:
                        running = False
                        reiniciar_juego()

            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(ventana)
        pygame.display.flip()

    pygame.quit()


def pantalla_felicidades2():
    pygame.init()
    pygame.mixer.init()
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Felicidades")

    # Define la interfaz de usuario
    manager = pygame_gui.UIManager((ANCHO, ALTO))

    fondo_felicidades = pygame.image.load('fondo_felicidades.jpeg')
    fondo_felicidades = pygame.transform.scale(fondo_felicidades, (ANCHO, ALTO))

    # Crea una superficie para el texto con fondo negro y opacidad
    texto_felicidades = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((ANCHO // 2 - 150, ALTO // 2 - 100), (300, 200)),
        text='¡Felicidades!',
        manager=manager)
    fondo_texto = pygame.Surface((texto_felicidades.rect.width, texto_felicidades.rect.height))
    fondo_texto.set_alpha(200)  # Ajusta la opacidad (0 transparente, 255 opaco)
    fondo_texto.fill(NEGRO)

    ventana.blit(fondo_felicidades, (0, 0))
    ventana.blit(fondo_texto, texto_felicidades.rect.topleft)
    manager.draw_ui(ventana)

    # Crea una etiqueta de botón para jugar de nuevo
    boton_jugar_de_nuevo = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((ANCHO // 2 - 100, ALTO // 2 + 50), (200, 50)),
        text='Jugar de Nuevo',
        manager=manager)

    running = True
    while running:
        time_delta = reloj.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == boton_jugar_de_nuevo:
                        running = False
                        reiniciar_juego2()

            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(ventana)
        pygame.display.flip()

    pygame.quit()


def pantalla_felicidades3():
    pygame.init()
    pygame.mixer.init()
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Felicidades")

    # Define la interfaz de usuario
    manager = pygame_gui.UIManager((ANCHO, ALTO))

    fondo_felicidades = pygame.image.load('fondo_felicidades.jpeg')
    fondo_felicidades = pygame.transform.scale(fondo_felicidades, (ANCHO, ALTO))

    # Crea una superficie para el texto con fondo negro y opacidad
    texto_felicidades = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((ANCHO // 2 - 150, ALTO // 2 - 100), (300, 200)),
        text='¡Felicidades!',
        manager=manager)
    fondo_texto = pygame.Surface((texto_felicidades.rect.width, texto_felicidades.rect.height))
    fondo_texto.set_alpha(200)  # Ajusta la opacidad (0 transparente, 255 opaco)
    fondo_texto.fill(NEGRO)

    ventana.blit(fondo_felicidades, (0, 0))
    ventana.blit(fondo_texto, texto_felicidades.rect.topleft)
    manager.draw_ui(ventana)

    # Crea una etiqueta de botón para jugar de nuevo
    boton_jugar_de_nuevo = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((ANCHO // 2 - 100, ALTO // 2 + 50), (200, 50)),
        text='Jugar de Nuevo',
        manager=manager)

    running = True
    while running:
        time_delta = reloj.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == boton_jugar_de_nuevo:
                        running = False
                        jugar_juego_con_imagenes()

            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(ventana)
        pygame.display.flip()
    pygame.quit()


def jugar_juego_con_imagenes():
    # Crear la ventana
    pygame.init()
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Juego con Imágenes")

    # Inicializar pygame_gui
    gestor = pygame_gui.UIManager((ANCHO, ALTO))

    # Cargar la imagen de fondo
    fondo = pygame.image.load("fondo_ejercicios.jpeg")
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

    # Cargar preguntas, imágenes y respuestas
    preguntas_respuestas_imagenes = cargar_imagenes_y_respuestas()

    # Bucle principal
    ejecutando = True
    pregunta_actual = None
    botones_respuesta = []  # Lista para almacenar los botones de respuesta

    # Inicializar cronómetro
    fps = 1000  # Fotogramas por segundo
    duracion_cronometro_segundos = 3200  # Duración del cronómetro en segundos
    duracion_total_fotogramas = fps * duracion_cronometro_segundos


    cronometro_label = pygame_gui.elements.UILabel(
        #x y |
        relative_rect=pygame.Rect((20, 20), (200, 100)),
        text=f"Cronómetro: {duracion_total_fotogramas}",
        manager=gestor
    )

    # Botón para regresar al menú principal
    boton_menu_principal = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((ANCHO - 200, 10), (180, 30)),
        text="Menú Principal",
        manager=gestor
    )
    frame_count = 0
    while ejecutando:
        frame_count += 1
        tiempo_restante_segundos = max(0, duracion_total_fotogramas - frame_count) // fps
        cronometro_label.set_text(f"Cronómetro: {tiempo_restante_segundos}")
        # Dibujar la imagen de fondo en la ventana
        ventana.blit(fondo, (0, 0))

        if tiempo_restante_segundos <= 0:
            show_perdiste_screen()

        # Seleccionar una pregunta al azar si no hay una pregunta actual
        if pregunta_actual is None:
            if preguntas_respuestas_imagenes:
                pregunta_actual = random.choice(preguntas_respuestas_imagenes)
                preguntas_respuestas_imagenes.remove(pregunta_actual)
                ruta_imagen = mostrar_pregunta(ventana, gestor, pregunta_actual, botones_respuesta)
                imagen = pygame.image.load(ruta_imagen)
                imagen = pygame.transform.scale(imagen, (400, 200))
                pos_x = (ANCHO - imagen.get_width()) // 2
                pos_y = (ALTO - imagen.get_height()) // 3.5
            else:
                # Si no quedan más preguntas, mostrar pantalla de felicitaciones y salir del bucle
                pantalla_felicidades3()
                ejecutando = False

        for evento in pygame.event.get():
            gestor.process_events(evento)
            if evento.type == pygame.QUIT:
                ejecutando = False

            if evento.type == pygame.USEREVENT:

                if evento.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    # Verificar si la opción seleccionada es la correcta
                    respuesta_seleccionada = evento.ui_element.text
                    if evento.ui_element == boton_menu_principal:
                        pantalla_principal()

                    if respuesta_seleccionada == pregunta_actual['correcta']:
                        # Cambiar la ruta de la imagen
                        if len(preguntas_respuestas_imagenes) > 0:
                            pregunta_actual = None
                            ventana.fill((255, 255, 255))
                            for boton in botones_respuesta:
                                boton.kill()  # Eliminar los botones de respuesta
                            botones_respuesta.clear()  # Limpiar la lista de botones
                        else:
                            # Si no quedan más preguntas, mostrar pantalla de felicitaciones y salir del bucle
                            pantalla_felicidades3()
                            ejecutando = False
                    else:
                        print("Respuesta incorrecta")

        gestor.update(0)  # Actualizar el gestor de eventos
        gestor.draw_ui(ventana)  # Dibujar los elementos de pygame_gui en la ventana
        # Mostrar la imagen en la ventana
        ventana.blit(imagen, (pos_x, pos_y))
        pygame.display.flip()  # Actualizar la ventana

    pygame.quit()














def cargar_imagenes_y_respuestas():
    # Aquí defines tus preguntas, imágenes y respuestas
    preguntas_respuestas_imagenes = [
        {
            'imagen': 'img1.png',
            'respuestas': ['1.46', '0.3412', '0.72', '-0657813'],
            'correcta': '-0657813'
        },
        {
            'imagen': 'img2.png',
            'respuestas': ['42', '1.1', '0.555555', '0.666666666667'],
            'correcta': '0.666666666667'
        },
        {
            'imagen': 'img3.png',
            'respuestas': ['1.10', '-1.029183673', '1.4', '1.029183673'],
            'correcta': '1.029183673'
        },
        {
            'imagen': 'img4.png',
            'respuestas': ['2.47822', '1.033234', '1.368808108', '1.4'],
            'correcta': '1.368808108'
        },
        {
            'imagen': 'img5.png',
            'respuestas': ['0.47822', '0.5671407819', '0.45114', '0.573896'],
            'correcta': '0.5671407819'
        },
        # Agrega más preguntas con sus respectivas imágenes y respuestas aquí
    ]
    return preguntas_respuestas_imagenes


def mostrar_pregunta(ventana, gestor, pregunta_actual, botones_respuesta):
    # Cargar la imagen de la pregunta
    ruta_imagen = pregunta_actual['imagen']
    # Mostrar las opciones de respuesta
    y_pos = 350
    for respuesta in pregunta_actual['respuestas']:
        boton_respuesta = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((ANCHO // 2 - 100, y_pos), (200, 50)),
            text=respuesta,
            manager=gestor
        )
        botones_respuesta.append(boton_respuesta)  # Agregar botón a la lista
        y_pos += 60

    # Actualizar la ventana
    pygame.display.flip()
    return ruta_imagen


def jugar_kahoot():
    # Reinicia el estado del juego
    # Esto incluiría reiniciar las preguntas y respuestas, el tiempo, etc.
    pygame.init()
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Preguntas - Métodos Numéricos")
    reloj = pygame.time.Clock()

    # Carga la imagen de fondo
    fondo_imagen = pygame.image.load('fondoBlack.jpg')
    fondo_imagen = pygame.transform.scale(fondo_imagen, (ANCHO, ALTO))

    # Define la interfaz de usuario
    manager = pygame_gui.UIManager((ANCHO, ALTO))

    pregunta_actual = None
    respuestas_botones = None
    tiempo_pregunta = 25  # Tiempo límite para responder cada pregunta en segundos
    tiempo_restante = tiempo_pregunta

    pregunta_texto = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((380, 50), (700, 500)),
        text='',
        manager=manager,

    )
    tiempo_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((ANCHO - 250, 20), (200, 30)),
        text='',
        manager=manager
    )

    boton_reiniciar_todo2 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((ANCHO // 2 + 50, 50), (200, 30)),
        text='Ir a menú',
        manager=manager
    )

    # Ciclo principal del juego
    running = True
    while running:
        tiempo_restante -= 1 / FPS
        print(tiempo_restante)
        if tiempo_restante < 0:
            show_perdiste_screen()
        for event in pygame.event.get():
            manager.process_events(event)
            if event.type == pygame.QUIT:
                running = False

            # Maneja los eventos de los botones de respuesta
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    for boton_respuesta in respuestas_botones:
                        if event.ui_element == boton_reiniciar_todo2:
                            reiniciar_todo2()
                        if event.ui_element == boton_respuesta:
                            if boton_respuesta.text == pregunta_actual['correcta']:
                                print("¡Respuesta correcta!")
                                pregunta_texto.set_text('')

                                # Elimina los elementos de interfaz de usuario de las respuestas anteriores
                                for boton in respuestas_botones:
                                    boton.kill()

                                # Elimina la pregunta seleccionada de la lista de preguntas
                                preguntas_respuestas.remove(pregunta_actual)

                                # Reinicia la pregunta y las respuestas
                                respuestas_botones = []
                                pregunta_actual = None

                                # Si no quedan más preguntas, muestra la pantalla de felicitaciones
                                if not preguntas_respuestas:
                                    pantalla_felicidades2()
                            else:
                                print("¡Respuesta incorrecta!")
                                boton_respuesta.bg_color = ROJO

        # Limpia la ventana y dibuja el fondo de imagen
        ventana.blit(fondo_imagen, (0, 0))

        # Si no hay una pregunta actual en juego, selecciona una nueva pregunta
        if not pregunta_actual and preguntas_respuestas:
            pregunta_actual = random.choice(preguntas_respuestas)
            respuestas_botones = mostrar_pregunta_y_respuestas(ventana, manager, pregunta_actual, pregunta_texto)

        # Actualiza el texto del label del tiempo en cada iteración
        tiempo_texto = 'Tiempo restante: {:.0f} seg'.format(max(0, tiempo_restante))
        tiempo_label.set_text(tiempo_texto)

        manager.update(reloj.tick(FPS) / 1000.0)
        manager.draw_ui(ventana)
        pygame.display.flip()


# Define la función para mostrar una pregunta y sus respuestas
# Define la función para mostrar una pregunta y sus respuestas
# Define la función para mostrar una pregunta y sus respuestas
def mostrar_pregunta_y_respuestas(ventana, manager, pregunta_actual, pregunta_texto):
    fondo_texto = pygame.Surface((700, 100))
    fondo_texto.set_alpha(150)
    fondo_texto.fill(NEGRO)
    ventana.blit(fondo_texto, (50, 50))  # Blit del fondo negro detrás del texto

    pregunta_texto.set_text(pregunta_actual['pregunta'])
    pregunta_texto.relative_rect = pygame.Rect((100, 100), (700, 200))
    pregunta_texto.bg_color = NEGRO  # Cambia el color del fondo del texto a negro
    pregunta_texto.bg_alpha = 0  # Establece la opacidad del fondo del texto a 0

    respuestas_botones = []
    y_pos = 400
    respuesta_correcta = pregunta_actual['correcta']
    for respuesta in pregunta_actual['respuestas']:
        color = BLANCO  # Color predeterminado para las respuestas incorrectas
        if respuesta == respuesta_correcta:
            color = VERDE  # Cambia el color a verde si es la respuesta correcta
        boton_respuesta = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, y_pos), (600, 50)),
                                                       text=respuesta,
                                                       manager=manager)
        boton_respuesta.bg_color = color  # Establece el color de fondo del botón
        respuestas_botones.append(boton_respuesta)
        y_pos += 70

    return respuestas_botones


# Define la función para mostrar un mensaje de respuesta incorrecta
def mostrar_respuesta_incorrecta(ventana, manager):
    mensaje_texto = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((ANCHO // 2 - 150, ALTO // 2 - 25), (300, 50)),
        text='Respuesta incorrecta. ¡Inténtalo de nuevo!',
        manager=manager)

    pygame.display.flip()
    pygame.time.wait(2000)


# Define la función para reiniciar el juego
def reiniciar_juego():
        global nivel_actual, terminado

        # Reinicia el nivel actual y el estado del juego
        nivel_actual = 0
        terminado = False

        # Llama a la función principal del juego para iniciar un nuevo juego
        main()


def reiniciar_todo():
    # Reinicia las variables del juego
    cartas = imagenes_cargadas * 2
    random.shuffle(cartas)

    # Reinicia el estado de las cartas
    for carta in tablero:
        carta.visible = False
        carta.matched = False

    # Vuelve a iniciar el juego
    pantalla_principal()


def reiniciar_todo2():
    global pregunta_actual, preguntas_respuestas, tiempo_restante
    pregunta_actual = None
    # Define las preguntas y respuestas del Kahoot
    preguntas_respuestas = [
        {
            'pregunta': '¿Cuál es el método numérico para encontrar raíces de ecuaciones?\n',
            'respuestas': ['Método de Bisección', 'Método de Newton-Raphson', 'Método de Euler',
                           'Método de Gauss-Seidel'],
            'correcta': 'Método de Newton-Raphson'
        },
        {
            'pregunta': '¿Cuál es el método numérico para interpolar datos?\n',
            'respuestas': ['Método de Lagrange', 'Método de Simpson', 'Método de Monte Carlo', 'Método de Runge-Kutta'],
            'correcta': 'Método de Lagrange'
        },
        {
            'pregunta': '¿Qué método se utiliza para resolver ecuaciones diferenciales ordinarias\nmediante la estimación de la pendiente en puntos sucesivos?\n',
            'respuestas': ['Método de Bisección', 'Método de Newton-Raphson', 'Método de Euler',
                           'Método de Gauss-Seidel'],
            'correcta': 'Método de Euler'
        },
        {
            'pregunta': '¿Cuál es el método utilizadopara resolver sistemas de ecuaciones lineales\nmediante la iteración hasta alcanzar una solución convergente?\n',
            'respuestas': ['Método de Bisección', 'Método de Newton-Raphson', 'Método de Euler',
                           'Método de Gauss-Seidel'],
            'correcta': 'Método de Gauss-Seidel'
        },
        {
            'pregunta': '¿Qué método numérico se emplea para calcular la integral de una función\naproximando áreas bajo una curva?\n',
            'respuestas': ['Método del Trapecio', 'Método de Simpson', 'Método de Euler', 'Método de Runge-Kutta'],
            'correcta': 'Método del Trapecio'
        },
        {
            'pregunta': '¿Cuál es el método que utiliza polinomios de grado bajo para ajustarse a un conjunto de datos?\n',
            'respuestas': ['Interpolación de Lagrange', 'Interpolación de Newton', 'Mínimos Cuadrados',
                           'Regresión Polinómica'],
            'correcta': 'Mínimos Cuadrados'
        },
        {
            'pregunta': '¿Qué técnica numérica se utiliza para estimar el valor de una función\nen un punto basándose en valores cercanos conocidos?\n',
            'respuestas': ['Interpolación', 'Regresión', 'Integración', 'Diferenciación'],
            'correcta': 'Interpolación'
        },
        {
            'pregunta': '¿Cuál es el método utilizado para aproximar la derivada de una función\nmediante diferencias finitas?\n',
            'respuestas': ['Diferenciación Numérica', 'Diferenciación Analítica', 'Interpolación de Lagrange',
                           'Regresión Lineal'],
            'correcta': 'Diferenciación Numérica'
        },
        {
            'pregunta': '¿Qué método numérico se emplea para resolver ecuaciones diferenciales parciales\nmediante una aproximación por pasos?\n',
            'respuestas': ['Método de Euler', 'Método de Runge-Kutta', 'Método de Diferencias Finitas',
                           'Método de Gauss-Seidel'],
            'correcta': 'Método de Diferencias Finitas'
        },
        {
            'pregunta': '¿Cuál es el método que ajusta una curva a un conjunto de datos minimizando la suma de los cuadrados de las diferencias entre los datos y la curva ajustada?\n',
            'respuestas': ['Interpolación de Lagrange', 'Interpolación de Newton', 'Mínimos Cuadrados',
                           'Regresión Lineal'],
            'correcta': 'Mínimos Cuadrados'
        },
        # Puedes continuar agregando más preguntas aquí
    ]
    tiempo_restante = 15
    pantalla_principal()


def reiniciar_juego2():
    global pregunta_actual, preguntas_respuestas, tiempo_restante
    pregunta_actual = None
    # Define las preguntas y respuestas del Kahoot
    preguntas_respuestas = [
        {
            'pregunta': '¿Cuál es el método numérico para encontrar raíces de ecuaciones?\n',
            'respuestas': ['Método de Bisección', 'Método de Newton-Raphson', 'Método de Euler',
                           'Método de Gauss-Seidel'],
            'correcta': 'Método de Newton-Raphson'
        },
        {
            'pregunta': '¿Cuál es el método numérico para interpolar datos?\n',
            'respuestas': ['Método de Lagrange', 'Método de Simpson', 'Método de Monte Carlo', 'Método de Runge-Kutta'],
            'correcta': 'Método de Lagrange'
        },
        {
            'pregunta': '¿Qué método se utiliza para resolver ecuaciones diferenciales ordinarias\nmediante la estimación de la pendiente en puntos sucesivos?\n',
            'respuestas': ['Método de Bisección', 'Método de Newton-Raphson', 'Método de Euler',
                           'Método de Gauss-Seidel'],
            'correcta': 'Método de Euler'
        },
        {
            'pregunta': '¿Cuál es el método utilizadopara resolver sistemas de ecuaciones lineales\nmediante la iteración hasta alcanzar una solución convergente?\n',
            'respuestas': ['Método de Bisección', 'Método de Newton-Raphson', 'Método de Euler',
                           'Método de Gauss-Seidel'],
            'correcta': 'Método de Gauss-Seidel'
        },
        {
            'pregunta': '¿Qué método numérico se emplea para calcular la integral de una función\naproximando áreas bajo una curva?\n',
            'respuestas': ['Método del Trapecio', 'Método de Simpson', 'Método de Euler', 'Método de Runge-Kutta'],
            'correcta': 'Método del Trapecio'
        },
        {
            'pregunta': '¿Cuál es el método que utiliza polinomios de grado bajo para ajustarse a un conjunto de datos?\n',
            'respuestas': ['Interpolación de Lagrange', 'Interpolación de Newton', 'Mínimos Cuadrados',
                           'Regresión Polinómica'],
            'correcta': 'Mínimos Cuadrados'
        },
        {
            'pregunta': '¿Qué técnica numérica se utiliza para estimar el valor de una función\nen un punto basándose en valores cercanos conocidos?\n',
            'respuestas': ['Interpolación', 'Regresión', 'Integración', 'Diferenciación'],
            'correcta': 'Interpolación'
        },
        {
            'pregunta': '¿Cuál es el método utilizado para aproximar la derivada de una función\nmediante diferencias finitas?\n',
            'respuestas': ['Diferenciación Numérica', 'Diferenciación Analítica', 'Interpolación de Lagrange',
                           'Regresión Lineal'],
            'correcta': 'Diferenciación Numérica'
        },
        {
            'pregunta': '¿Qué método numérico se emplea para resolver ecuaciones diferenciales parciales\nmediante una aproximación por pasos?\n',
            'respuestas': ['Método de Euler', 'Método de Runge-Kutta', 'Método de Diferencias Finitas',
                           'Método de Gauss-Seidel'],
            'correcta': 'Método de Diferencias Finitas'
        },
        {
            'pregunta': '¿Cuál es el método que ajusta una curva a un conjunto de datos minimizando la suma de los cuadrados de las diferencias entre los datos y la curva ajustada?\n',
            'respuestas': ['Interpolación de Lagrange', 'Interpolación de Newton', 'Mínimos Cuadrados',
                           'Regresión Lineal'],
            'correcta': 'Mínimos Cuadrados'
        },
        # Puedes continuar agregando más preguntas aquí
    ]
    tiempo_restante = 15
    jugar_kahoot()


# Ejecuta la pantalla principal
if __name__ == "__main__":
    pantalla_principal()
