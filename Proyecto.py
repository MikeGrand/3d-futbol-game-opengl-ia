import pygame
from pygame.locals import *
import matplotlib.image as mpimg
import numpy as np
# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import random
import pygame.mixer

import sys
from objloader import *
from Plano import *
sys.path.append('..')

screen_width = 1000
screen_height = 640
#vc para el obser.
FOVY=90.0
ZNEAR=0.01
ZFAR=900.0

dir = [1.0, 0.0, 0.0]

EYE_X = 0.0
EYE_Y = 15.0
EYE_Z = 0.0
CENTER_X = 1.0
CENTER_Y = 10.0
CENTER_Z = 0.0
UP_X=0
UP_Y=1
UP_Z=0

#Variables para dibujar los ejes del sistema
X_MIN=-500
X_MAX=500
Y_MIN=-500
Y_MAX=500
Z_MIN=-500
Z_MAX=500
#Dimension del plano
DimBoardWidth = 150
DimBoardHeight = 250

ancho = DimBoardWidth - 10
fondo = DimBoardHeight - 18
#Variables para el control del observador
theta = 0.0
radius = 300

pygame.init()
pygame.mixer.init()
#Control el estado del aumento de velocidad y el temporizador
increased_speed = False
speed_increase_duration = 1.0  # Duración del aumento de velocidad en segundos
speed_increase_timer = 0.0
speed_reset_duration = 3.0  # Tiempo antes de restablecer la velocidad normal
speed_reset_timer = 0.0

#Arreglos para la configuración de la iluminación
sun_light_position = np.array([10.0, 10.0, 10.0, 0.0 ])
sun_light_ambient = np.array([110.0, 110.0, 110.0, 0.0])
sun_light_diffuse= np.array([1.0, 1.0, 1.0, 1.0])
sun_light_specular = np.array([1.0, 1.0, 1.0, 1.0])
sun_light_direction = np.array([1.0,1.0,1.0])

#Función para cargar las texturas
def cargar_textura(nombre_archivo):
    texture_surface = pygame.image.load(nombre_archivo)
    texture_data = pygame.image.tostring(texture_surface, 'RGB', 1)
    width, height = texture_surface.get_rect().size

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return texture_id

#Función que genera n rivales
def generarRivales():
    x = random.randint(-DimBoardWidth+10, DimBoardWidth-10)
    z = random.randint(-DimBoardHeight+10, DimBoardHeight-10)
    rival = OBJ("ProyectoFinal/Man.obj", x, z, swapyz=True)
    rival.generate()    

    return rival


#Funcion que dibuja los ejes
def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    #X axis in red
    glColor3f(1.0,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN,0.0,0.0)
    glVertex3f(X_MAX,0.0,0.0)
    glEnd()
    #Y axis in green
    glColor3f(0.0,1.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,Y_MIN,0.0)
    glVertex3f(0.0,Y_MAX,0.0)
    glEnd()
    #Z axis in blue
    glColor3f(0.0,0.0,1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,0.0,Z_MIN)
    glVertex3f(0.0,0.0,Z_MAX)
    glEnd()
    glLineWidth(1.0)

#Función que dibuja una esfera
def drawSphere(radius, slices, stacks):
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluQuadricTexture(quadric, GL_TRUE)
    gluSphere(quadric, radius, slices, stacks)

def dibujarSol():
    global sun_light_position
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(250.0, 200.0, 250.0)
    glRotatef(180, 0.0, 1.0, 0.0)
    glScalef(2.5, 2.5, 2.5)
    drawSphere(2, 30, 30)
    glPopMatrix()
    

#Inicializador del ambiente gráfico
def Init():
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: cubos")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glShadeModel(GL_SMOOTH)
    glLightfv(GL_LIGHT0, GL_POSITION, sun_light_position)
    glLightfv(GL_LIGHT0, GL_AMBIENT, sun_light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, sun_light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, sun_light_specular)
    glLightfv(GL_LIGHT0, GL_SPECULAR, sun_light_direction)

#Se mueve al observador circularmente al rededor del plano XZ a una altura fija (EYE_Y)
def lookat():
    global CENTER_X
    global CENTER_Z
    global angle
    global bandera
    oldCenterX = CENTER_X
    oldCenterZ = CENTER_Z
    oldDirX = dir[0]
    oldCDirZ = dir[2]
        
    angle = math.radians(-theta)
        
    CENTER_X = EYE_X + radius * math.cos(angle)
    CENTER_Z = EYE_Z - radius * math.sin(angle)
            
    glLoadIdentity()
        
    gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
    dir[0] = math.cos(angle)
    dir[2] = -math.sin(angle)
        
    if (EYE_X + dir[0] * 15) > ancho or (EYE_X + dir[0] * 15) < -ancho or (EYE_Z + dir[2] * 15) > fondo or (EYE_Z + dir[2] * 15) < -fondo or ((EYE_Z + dir[2] * 15) > 140 and (EYE_X + dir[0] * 15) > -101 and (EYE_X + dir[0] * 15 <101)) or ((EYE_Z + dir[2] * 15) < -140 and (EYE_X + dir[0] * 15) > -101 and (EYE_X + dir[0] * 15 <101)):
        CENTER_X = oldCenterX
        CENTER_Z = oldCenterZ
        dir[0] = oldDirX
        dir[2] = oldCDirZ        
        bandera = 1
    else:
        bandera= 0

#Función que ayuda a poder movernos de manera continua
#Función que ayuda a poder movernos de manera continua
def handle_input():
    global EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z
    global increased_speed, speed_increase_timer, speed_reset_timer

    oldEYEX = EYE_X
    oldEYEZ = EYE_Z
    oldCenterX = CENTER_X
    oldCenterZ = CENTER_Z
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        speed_multiplier = 2.0 if increased_speed else 1.0
        EYE_X = EYE_X + dir[0] * speed_multiplier
        EYE_Z = EYE_Z + dir[2] * speed_multiplier
        CENTER_X = CENTER_X + dir[0] * speed_multiplier
        CENTER_Z = CENTER_Z + dir[2] * speed_multiplier

    if keys[pygame.K_s]:
        speed_multiplier = 2.0 if increased_speed else 1.0
        EYE_X = EYE_X - dir[0] * speed_multiplier
        EYE_Z = EYE_Z - dir[2] * speed_multiplier
        CENTER_X = CENTER_X - dir[0] * speed_multiplier
        CENTER_Z = CENTER_Z - dir[2] * speed_multiplier

    if keys[pygame.K_d]:
        speed_multiplier = 2.0 if increased_speed else 1.0
        EYE_X -= dir[2] * speed_multiplier
        EYE_Z += dir[0] * speed_multiplier
        CENTER_X -= dir[2] * speed_multiplier
        CENTER_Z += dir[0] * speed_multiplier

    if keys[pygame.K_a]:
        speed_multiplier = 2.0 if increased_speed else 1.0
        EYE_X += dir[2] * speed_multiplier
        EYE_Z -= dir[0] * speed_multiplier
        CENTER_X += dir[2] * speed_multiplier
        CENTER_Z -= dir[0] * speed_multiplier

    if EYE_X + dir[0] * 15 > ancho:
        EYE_X = oldEYEX
        CENTER_X = oldCenterX
    
    if (EYE_Z + dir[2] * 15 > fondo):
        EYE_Z = oldEYEZ
        CENTER_Z = oldCenterZ
        
    if  EYE_X + dir[0] * 15 < -ancho:
        EYE_X = oldEYEX
        CENTER_X = oldCenterX
        
    if EYE_Z + dir[2] * 15 < -fondo:
        EYE_Z = oldEYEZ
        CENTER_Z = oldCenterZ
        
        
    if (EYE_Z + dir[2] * 15) > 140:
        if (EYE_X + dir[0] * 15) > -101 and (EYE_X + dir[0] * 15 <101):
            if oldEYEZ + dir[2] * 15 <140:
                EYE_Z = oldEYEZ
                CENTER_Z = oldCenterZ
            else:
                EYE_X = oldEYEX
                CENTER_X = oldCenterX
                
    
    if (EYE_Z + dir[2] * 15) < -140:  
        if (EYE_X + dir[0] * 15) > -101 and (EYE_X + dir[0] * 15 <101):   
            if oldEYEZ + dir[2] * 15 > -140:
                EYE_Z = oldEYEZ
                CENTER_Z = oldCenterZ
            else:
                EYE_X = oldEYEX
                CENTER_X = oldCenterX
    
    glLoadIdentity()
    gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)

    if keys[pygame.K_e]:
        if not increased_speed:
            increased_speed = True
            speed_increase_timer = speed_increase_duration

    if increased_speed and speed_increase_timer > 0.0:
        speed_increase_timer -= 1 / 30.0
    elif increased_speed:
        increased_speed = False
        speed_reset_timer = speed_reset_duration

    if speed_reset_timer > 0.0:
        speed_reset_timer -= 1 / 30.0
    elif not increased_speed:
        speed_reset_timer = 0.0
        speed_increase_timer = 0.0
    
    
#Variable global para el manejo de colisiones a nivel de jugabilidad
colision  = False
vidas = 3   

# Variables que se usan para patear la pelota. 
disparoZ = 3  
disparoX = 3
disparoY = 1
disparar = 0
contador = 0
DIR1=0
DIR2=0
posPortero = 0
a = 0   # Usada con el objeto del portero 
bloquear = False
poste = False

#Función que dibuja el escenario (cancha y paredes)
def display():
    global texturas
    global EYE_X, EYE_Z,EYE_Y
    global disparoZ,disparoX, disparoY, disparar,DIR1,DIR2,contador,poste


    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #Axis()
    #Se dibuja el ambiente
    glColor3f(1.0, 1.0, 1.0)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    dibujarSol()
    ambiente.dibujarAmbiente()
    
    if(disparar == True): #Se presiona t para disparar y al hacerlo se activa la variable 
        disparoY = disparoY+0.2
        if(contador==0):  #el contador es para que no tome otra direccion al tirar (es constante la direccion)
            DIR1 = dir[2]   #guarda la ultima direccion en donde miramos 
            DIR2 = dir[0]
            contador = contador+1   # una vez que se guarda la direccion, se aumenta el contador para que no se actualice 
        if(poste == False):
            disparoZ = disparoZ+DIR1*4 # disparo en (x,y) y tiene el direccion de la pelota
            disparoX = disparoX+DIR2*4
            poste = colisionPoste(disparoX,disparoY,disparoZ)
            #print(poste)
        if(poste == True):
            print("POSTEEEEEEEEEEEEEEE")
            disparoX = disparoX+DIR1*(-5)
            disparoZ = disparoZ+DIR2*(-5)
                
        if(disparoX > -28 and disparoX < 28) and (disparoZ > DimBoardHeight or disparoZ < -DimBoardHeight):
            print("GOOOOOL!")
            rivales.append(generarRivales())
        
    else: 
        disparoZ =  EYE_Z + dir[2] * 15
        disparoX = EYE_X + dir[0] * 15
        
    #Saque del centro del campo
    if(disparoX > DimBoardWidth or disparoX < -DimBoardWidth):
        disparoX = EYE_X + dir[0] * 15
        disparoY = 2.0
        disparar = False
        contador = 0
        EYE_X = 0.0
        EYE_Y = 15.0
        EYE_Z = 0.0
        poste = False
    if(disparoZ > DimBoardHeight or disparoZ < -DimBoardHeight):  # la direccion Z apunta hacia la porteria
        disparoX = EYE_Z + dir[2] * 15
        disparoY = 2.0
        disparar = False
        contador = 0
        EYE_X = 0.0
        EYE_Y = 15.0
        EYE_Z = 0.0   
        poste = False

        
    glPushMatrix()
    glTranslatef(disparoX, disparoY, disparoZ)  # Ajustar la posición de la esfera en relación con la cámara
    glRotatef(-theta, 0, 1, 0)  # Aplicar rotación a la esfera en relación con la rotación de la cámara
    drawSphere(2, 30, 30)
    glPopMatrix()

    # Jugadores Rivales
    #Pasarle a todos los rivales nuestra posicion y ejecutar el algoritmo de búsqueda
    
    renderizarJugadores()
    validaEstado()
    
    glDisable(GL_LIGHTING)
    
def renderizarJugadores():
    global a, EYE_X, EYE_Z, EYE_Y, disparar, contador, disparoX, disparoY, disparoZ
    global vidas, colision
    for rival in rivales:
        rival.posJugador(EYE_X, EYE_Z)
        rival.draw("rival")
        choque = rival.colisionRival(EYE_X, EYE_Z)
        if choque:
            EYE_X = 0.0
            EYE_Y = 15.0
            EYE_Z = 0.0
            colision = True
            vidas = vidas-1
            print("Un rival te ha quitado el balón!")
    
    for portero in porteros:
        portero.draw("portero")
        a = portero.moverPortero(portero.x, a)
        atajadon = portero.colisionBalon(disparoX, disparoY, disparoZ)
        if atajadon:
            print("Atajadón del portero!!!")
            disparoX = EYE_X + dir[0] * 15
            disparoY = 2.0
            disparar = False
            contador = 0
            EYE_X = 0.0
            EYE_Y = 15.0
            EYE_Z = 0.0

def validaEstado():
    global colision, vidas
    if colision:
        rivales.clear()
        rivales.append(generarRivales())
        colision = False
        
def colisionPoste(disX, disY, disZ): 
    poste = False
    if(disX >= 25 and disX <=35 and disZ >= 230):
        poste = True
    if(disX <= -25 and disX >=-35 and disZ >= 230):
        poste = True
    if(disX >= 25 and disX <=35 and disZ <= -230):
        poste = True
    if(disX <= -25 and disX >=-35 and disZ <= -230):
        poste = True
        # no alcanza hasta arriba pero por si las moscas. 
    if(disY >= 25 and disY <= 35 and disX >=-28 and disX <=28):
        poste = True
    return poste

        
        
done = False
Init()
#Almacenamiento de texturas
texturas = []
texturas.append(cargar_textura("ProyectoFinal/cancha2.jpg")) #Indice 0 = Cancha
texturas.append(cargar_textura("ProyectoFinal/pared1.png")) #Indice 1 = pared 1
texturas.append(cargar_textura("ProyectoFinal/pared2.png")) #Indice 2 = pared 2
texturas.append(cargar_textura("ProyectoFinal/pared3.png")) #Indice 3 = pared 3
texturas.append(cargar_textura("ProyectoFinal/pared4.png")) #Indice 4 = pared 4
texturas.append(cargar_textura("ProyectoFinal/pasto.png")) #Indice 5 = pasto de relleno
texturas.append(cargar_textura("ProyectoFinal/cielo1.png")) #Indice 6 = cielo
pygame.mixer.music.load("ProyectoFinal/Futbol.mp3")

pygame.mixer.music.play(-1)
ambiente = Plano(texturas, DimBoardWidth, DimBoardHeight)
#Arreglo que contiene todos los rivales que se mueven por todo el plano
rivales = []
rivales.append(generarRivales())

#Porteros 
porteros = []
porteros.append(OBJ("ProyectoFinal/Man.obj", 0.0, 235, swapyz=True))
porteros.append(OBJ("ProyectoFinal/Man.obj", 0.0, -235, swapyz=True))

for portero in porteros:
    portero.generate()

bandera = 0
clock = pygame.time.Clock()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or vidas == 0:
            done = True
        elif event.type == pygame.MOUSEMOTION:
            theta += event.rel[0]
            variable = event.rel[0]
            theta %= 360.0
            lookat()
            if bandera == 1:
                theta -= variable
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            if event.key == pygame.K_t:
                disparar = True
    

    handle_input()
    display()
    pygame.display.flip()
    clock.tick(30)

pygame.quit()