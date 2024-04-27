import pygame
import pygame_gui
import random
import os

# Define las dimensiones de la pantalla y el tamaño de las cartas
ANCHO = 2000
ALTO = 1200
CARTA_ANCHO = 300
CARTA_ALTO = 180
FPS = 50
GAP = 20
# Define los colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)

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


# Define la función principal del juego
def main():
    # Registra el tiempo inicial
    tiempo_inicial = pygame.time.get_ticks()

    # Define la interfaz de usuario
    manager = pygame_gui.UIManager((ANCHO, ALTO))

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

    carta_seleccionada = None
    carta_seleccionada2 = None
    puntuacion = 0
    intentos = 0
    terminado = False
    # Definir un contenedor para el contenido desplazable
    scrollable_panel_rect = pygame.Rect(100, 100, 400, 400)

    while not terminado:
        # Calcula el tiempo transcurrido desde el inicio del juego
        tiempo_transcurrido = pygame.time.get_ticks() - tiempo_inicial
        tiempo_transcurrido_segundos = tiempo_transcurrido // 1000

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

        ventana.fill(NEGRO)

        for carta in tablero:
            carta.draw()

        # Actualiza el texto de la etiqueta de tiempo en cada iteración del bucle
        cronometro_texto = 'Tiempo: {} seg'.format(tiempo_transcurrido_segundos)
        cronometro_label.set_text(cronometro_texto)

        manager.update(0)
        manager.draw_ui(ventana)

        pygame.display.flip()

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

        if puntuacion == len(cartas) / 2:
            terminado = True
            pantalla_felicidades()

    pygame.quit()


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



        manager.update(time_delta)
        manager.draw_ui(ventana)
        pygame.display.flip()

    pygame.quit()


# Define la función para la pantalla de felicitaciones
def pantalla_felicidades():
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

    # Cargar preguntas, imágenes y respuestas
    preguntas_respuestas_imagenes = cargar_imagenes_y_respuestas()

    # Bucle principal
    ejecutando = True
    pregunta_actual = None
    botones_respuesta = []  # Lista para almacenar los botones de respuesta

    # Cargar la imagen
    ruta_imagen = os.path.join(preguntas_respuestas_imagenes[0]['imagen'])
    print("Ruta de la imagen:", ruta_imagen)  # Imprimir la ruta de la imagen
    imagen = pygame.image.load(ruta_imagen)
    if imagen is None:
        print("Error: No se pudo cargar la imagen.")
        pygame.quit()

    # Escalar la imagen
    imagen = pygame.transform.scale(imagen, (100, 100))
    ancho_imagen, alto_imagen = imagen.get_size()
    print("Tamaño de la imagen:", ancho_imagen, "x", alto_imagen)  # Imprimir el tamaño de la imagen

    pos_x = (ANCHO - ancho_imagen) // 2
    pos_y = (ALTO - alto_imagen) // 2
    print("Posición de la imagen:", pos_x, ",", pos_y)  # Imprimir la posición de la imagen

    # Mostrar la imagen en la ventana
    ventana.blit(imagen, (pos_x, pos_y))

    # Actualizar la pantalla
    pygame.display.flip()

    while ejecutando:

        # Seleccionar una pregunta al azar si no hay una pregunta actual
        if pregunta_actual is None:
            if preguntas_respuestas_imagenes:
                pregunta_actual = random.choice(preguntas_respuestas_imagenes)
                preguntas_respuestas_imagenes.remove(pregunta_actual)
                mostrar_pregunta(ventana, gestor, pregunta_actual, botones_respuesta)
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
                    if respuesta_seleccionada == pregunta_actual['correcta']:
                        # Si la respuesta es correcta, limpiar la pantalla y pasar a la siguiente pregunta
                        pregunta_actual = None
                        ventana.fill((255, 255, 255))
                        for boton in botones_respuesta:
                            boton.kill()  # Eliminar los botones de respuesta
                        botones_respuesta.clear()  # Limpiar la lista de botones
                    else:
                        print("Respuesta incorrecta")

        ventana.fill((255, 255, 255))  # Rellenar la ventana con blanco
        gestor.update(0)  # Actualizar el gestor de eventos
        gestor.draw_ui(ventana)  # Dibujar los elementos de pygame_gui en la ventana
        pygame.display.flip()  # Actualizar la ventana

    pygame.quit()  # Cerrar pygame


def cargar_imagenes_y_respuestas():
    # Aquí defines tus preguntas, imágenes y respuestas
    preguntas_respuestas_imagenes = [
        {
            'imagen': 'imagen1.png',
            'respuestas': ['Newton', 'Larangue', 'Luis', 'Juan'],
            'correcta': 'Newton'
        },
        {
            'imagen': 'imagen4.png',
            'respuestas': ['interpolacion', 'Matriz', 'numeros', 'nada'],
            'correcta': 'interpolacion'
        },
        # Agrega más preguntas con sus respectivas imágenes y respuestas aquí
    ]
    return preguntas_respuestas_imagenes


def mostrar_pregunta(ventana, gestor, pregunta_actual, botones_respuesta):
    # Cargar la imagen de la pregunta

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
    tiempo_pregunta = 15  # Tiempo límite para responder cada pregunta en segundos
    tiempo_restante = tiempo_pregunta

    pregunta_texto = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((650, 50), (700, 500)),
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
        boton_respuesta = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, y_pos), (600, 50)),
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
    # Reinicia las variables del juego
    cartas = imagenes_cargadas * 2
    random.shuffle(cartas)

    # Reinicia el estado de las cartas
    for carta in tablero:
        carta.visible = False
        carta.matched = False

    # Vuelve a iniciar el juego
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
