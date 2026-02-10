import math
import random
class Jugador:
    def __init__(self, nombre, x, z):
        self.x = z
        self.z = z
        self.nombre = nombre
        

def evaluar(jugador):
    distancia = math.sqrt((jugador[0] - jugador_principal.x) ** 2 + (jugador[1] - jugador_principal.z) ** 2)
    return 1 / distancia if distancia != 0 else 100  # Valor alto si están en la misma posición

def evaluarRadio(jugador):
    distancia = math.sqrt((jugador[0] - jugador_principal.x) ** 2 + (jugador[1] - jugador_principal.z) ** 2)
    return distancia

def es_movimiento_valido(x, z):
        if (x > -135 and x < 135) and (z > -235 and z < 235):
            return True
        
        return False

def generar_movimientos(posicion_actual_rival):
    # Generar movimientos posibles desde la posición actual del rival
    movimientos = []
    # Por ejemplo, moverse en las 8 direcciones alrededor de la posición actual
    for dx in [-1, 0, 1]:
        for dz in [-1, 0, 1]:
            if dx == 0 and dz == 0:
                continue  # No moverse, mantener la posición actual
            nuevo_x = posicion_actual_rival[0] + dx
            nuevo_z = posicion_actual_rival[1] + dz
            # Verificar si el nuevo movimiento es válido (sin salir del campo, sin colisionar con obstáculos, etc.)
            if es_movimiento_valido(nuevo_x, nuevo_z):
                movimientos.append((nuevo_x, nuevo_z))
    return movimientos

def alfa_beta(jugador, profundidad, alfa, beta, es_maximizando):
    if profundidad == 0:
        # Evaluar la posición actual del jugador
        return evaluar(jugador)

    if es_maximizando:
        valor = -math.inf
        for movimiento in generar_movimientos(jugador):
            valor = max(valor, alfa_beta(movimiento, profundidad - 1, alfa, beta, False))
            alfa = max(alfa, valor)
            if beta <= alfa:
                break
        return valor
    else:
        valor = math.inf
        for movimiento in generar_movimientos(jugador):
            valor = min(valor, alfa_beta(movimiento, profundidad - 1, alfa, beta, True))
            beta = min(beta, valor)
            if beta <= alfa:
                break
        return valor

rivales = [Jugador("Rival 1", 100, 100),
           Jugador("Rival 2", 2, 2)]
jugador_principal = Jugador("Jesus", 1, 1)

for rival in rivales:
    mejor_movimiento = None
    mejor_valor = -math.inf
    posiblesMovimientos = generar_movimientos([rival.x, rival.z])
    for movimiento in posiblesMovimientos:
        radio = evaluarRadio([rival.x, rival.z])
        if radio > 50:
            a = random.randint(0,9)
            rival.x, rival.z = posiblesMovimientos[a]
            print(a)
            print(posiblesMovimientos)
            break
            #rival.z = posiblesMovimientos[b]
        else:
            valor = alfa_beta(movimiento, 3, -math.inf, math.inf, False)  # Simulación de profundidad = 3
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_movimiento = movimiento

            # Aplicar el mejor movimiento encontrado al rival
            rival.x = mejor_movimiento[0]
            rival.z = mejor_movimiento[1]

    print(f"{rival.nombre} se movió a ({rival.x}, {rival.z})")  # Simplemente para mostrar el movimiento
    

    """Códigos a implementar en el proyecto
    ##### Código principal #####
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

    
    
    #Colision entre jugador y rival
    
    # Si un rival te atrapa te manda directo pal lobby
    dis = jugador.colisionRival(EYE_X,EYE_Z)  
    if(dis == True):
        EYE_X = 0.0
        EYE_Y = 15.0
        EYE_Z = 0.0 
        print("TE ATRAPO")

    
    # Portero
    glPushMatrix()
    glTranslate(portero.x, 5.0, portero.z) #z = 15
    glScale(1.5, 1.5, 1.5)
    glRotate(180, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    a = portero.moverPortero(portero.x,a)
    atajadon = portero.colisionBalon(disparoX,disparoY,disparoZ)
    if(atajadon == True):
        print("ATAJADON SEÑORES")        
    portero.draw()
    glPopMatrix()


    ##### Código objloader #####
    if(disparar == True): #Se presiona t para disparar y al hacerlo se activa la variable 
        disparoY = disparoY+0.2
        if(contador==0):  #el contador es para que no tome otra direccion al tirar (es constante la direccion)
            DIR1 = dir[2]   #guarda la ultima direccion en donde miramos 
            DIR2 = dir[0]
            contador = contador+1   # una vez que se guarda la direccion, se aumenta el contador para que no se actualice 
        disparoZ = disparoZ+DIR1*4 # disparo en (x,y) y tiene el direccion de la pelota
        disparoX = disparoX+DIR2*4
        bloquear = jugador.colisionBalon(disparoX,disparoY,disparoZ)    # Si el balon choca con algun jugador 
        if(bloquear == True):
            print("Bloqueado")
            disparoZ = jugador.z # disparo en (x,y) y tiene el direccion de la pelota
            disparoX = jugador.x
            disparoY = 2.0

    else: 
        disparoZ =  EYE_Z + dir[2] * 15
        disparoX = EYE_X + dir[0] * 15

    
    """
