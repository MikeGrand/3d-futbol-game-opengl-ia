import os
import pygame
from OpenGL.GL import *
import math
import random

class OBJ:
    generate_on_init = True
    
    @classmethod
    def loadTexture(cls, imagefile):
        surf = pygame.image.load(imagefile)
        image = pygame.image.tostring(surf, 'RGBA', 1)
        ix, iy = surf.get_rect().size
        texid = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texid)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        return texid

    @classmethod
    def loadMaterial(cls, filename):
        contents = {}
        mtl = None
        dirname = os.path.dirname(filename)

        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'newmtl':
                mtl = contents[values[1]] = {}
            elif mtl is None:
                raise ValueError("mtl file doesn't start with newmtl stmt")
            elif values[0] == 'map_Kd':
                # load the texture referred to by this declaration
                mtl[values[0]] = values[1]
                imagefile = os.path.join(dirname, mtl['map_Kd'])
                mtl['texture_Kd'] = cls.loadTexture(imagefile)
            else:
                mtl[values[0]] = list(map(float, values[1:]))
        return contents

    def __init__(self, filename, posX, posZ, swapyz=False):
        """Loads a Wavefront OBJ file. """
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.gl_list = 0
        dirname = os.path.dirname(filename)
        self.x = posX
        self.z = posZ
        self.mejor_movimiento = None
        self.mejor_valor = None
        self.jugador = [0]*2
        self.a = 0

        material = None
        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif values[0] == 'vn':
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.normals.append(v)
            elif values[0] == 'vt':
                self.texcoords.append(list(map(float, values[1:3])))
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'mtllib':
                self.mtl = self.loadMaterial(os.path.join(dirname, values[1]))
            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append((face, norms, texcoords, material))
        if self.generate_on_init:
            self.generate()

    def generate(self):
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)
        for face in self.faces:
            vertices, normals, texture_coords, material = face

            mtl = self.mtl[material]
            if 'texture_Kd' in mtl:
                # use diffuse texmap
                glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
            else:
                # just use diffuse colour
                glColor(*mtl['Kd'])

            glBegin(GL_POLYGON)
            for i in range(len(vertices)):
                if normals[i] > 0:
                    glNormal3fv(self.normals[normals[i] - 1])
                if texture_coords[i] > 0:
                    glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                glVertex3fv(self.vertices[vertices[i] - 1])
            glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()

    def render(self):
        glCallList(self.gl_list)

    def free(self):
        glDeleteLists([self.gl_list])
    
    def draw(self, tipo):
        if tipo == "rival":
            self.ejecutarAlgoritmo()
            
        glPushMatrix()
        glTranslatef(self.x, 5.0, self.z)
        glScalef(1.5, 1.5, 1.5)
        glRotatef(-90, 1.0, 0.0, 0.0)
        self.render()
        glPopMatrix()
        
        
    #Funciones para la IA
    
    def esMovimientoValido(self, x, z):
        if (x < -135 or x > 135) or (z < -235 or z > 235):
            return False
        
        return True
    
    def generarMovimientosRival(self, posicion):
        # Generar movimientos posibles desde la posición actual del rival
        movimientos = []
        # Por ejemplo, moverse en las 8 direcciones alrededor de la posición actual
        for dx in [-1, 0, 1]:
            for dz in [-1, 0, 1]:
                if dx == 0 and dz == 0:
                    continue  # No moverse, mantener la posición actual
                nuevo_x = posicion[0] + dx
                nuevo_z = posicion[1] + dz
                # Verificar si el nuevo movimiento es válido (sin salir del campo, sin colisionar con obstáculos, etc.)
                if self.esMovimientoValido(nuevo_x, nuevo_z):
                    movimientos.append((nuevo_x, nuevo_z))
        return movimientos
    
    def evaluar(self, posicion):
        distancia = math.sqrt((posicion[0] - self.jugador[0]) ** 2 + (posicion[1] - self.jugador[1]) ** 2)
        return 1 / distancia if distancia != 0 else 100  # Valor alto si están en la misma posición
    
    
    def alfa_beta(self, jugador, profundidad, alfa, beta, es_maximizando):
        if profundidad >=0 and profundidad < 1:
            # Evaluar la posición actual del jugador
            return self.evaluar(jugador)

        if es_maximizando:
            valor = -math.inf
            for movimiento in self.generarMovimientosRival(jugador):
                valor = max(valor, self.alfa_beta(movimiento, profundidad - 1, alfa, beta, False))
                alfa = max(alfa, valor)
                if beta <= alfa:
                    break
            return valor
        else:
            valor = math.inf
            for movimiento in self.generarMovimientosRival(jugador):
                valor = min(valor, self.alfa_beta(movimiento, profundidad - 1, alfa, beta, True))
                beta = min(beta, valor)
                if beta <= alfa:
                    break
            return valor

    def ejecutarAlgoritmo(self):
        mejor_movimiento = None
        mejor_valor = -math.inf
        for movimiento in self.generarMovimientosRival([self.x, self.z]):
            valor = self.alfa_beta(movimiento, 3, -math.inf, math.inf, False)  # Simulación de profundidad = 3
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_movimiento = movimiento
        self.x = mejor_movimiento[0]
        self.z = mejor_movimiento[1]
        
        
    def posJugador(self, x, z):
        self.jugador[0] = x
        self.jugador[1] = z
        

    def moverPortero(self,pX,a):
        vel = 0.8
        if(a == 0):
            self.x=pX+vel
            if(pX >= 20.0):
                a = 1
        if(a == 1):
            self.x=pX-vel
        if(pX <= -20.0):
            a = 0
        return a
    # La variable a se usa 0 para delante, y se activa 1 cuando va a la izquierda

    
    # Funcion que marca cuando un rival nos atrape. 
    # Envia nuestras coordenadas, y self.x self.y ya son proias de la clase. 
    def colisionRival(self,px,pz): 
        rx = self.x
        rz = self.z
        yo = [px, 15.0, pz]
        rival = [rx, 5.0, rz]
        yoTam = 5
        rivalTam = 7
        
        distancia = ((yo[0] - rival[0]) ** 2 +
                (yo[1] - rival[1]) ** 2 +
                (yo[2] - rival[2]) ** 2) ** 0.5
        #print(distancia)
        return distancia < (yoTam + rivalTam)
    
    
    # Funcion para cuando el balon choque con algun jugador al tirar (incluyendo el portero). 
    def colisionBalon(self,bx,by,bz): #balonx, balony
        rx = self.x
        rz = self.z
        balon = [bx, by, bz]
        rival = [rx, 20.0, rz]
        balonTam = 3.0
        rivalTam = 14.0
        
        distancia = ((balon[0] - rival[0]) ** 2 +
                (balon[1] - rival[1]) ** 2 +
                (balon[2] - rival[2]) ** 2) ** 0.5
       # print(distancia)
        return distancia < (balonTam + rivalTam)

        