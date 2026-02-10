from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np


class Plano:
    def __init__(self, texturas, ancho, largo):
        self.texturas = texturas
        self.ancho = ancho
        self.largo = largo
        
        
    def dibujarAmbiente(self):
        self.dibujarCancha()
        self.dibujarParedes()
        #Portería 1
        glPushMatrix()
        glTranslate(0.0, 0.0, 232.0)
        self.dibujaPorteria()
        glPopMatrix()
        
        #Portería 2
        glPushMatrix()
        glTranslate(0.0, 0.0, -232.0)
        self.dibujaPorteria()
        glPopMatrix()
        
        
        
    def dibujarCancha(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texturas[0])
        
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-self.ancho, 0, -self.largo)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(-self.ancho, 0, self.largo)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(self.ancho, 0, self.largo)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(self.ancho, 0, -self.largo)
        glEnd()
            
        glDisable(GL_TEXTURE_2D)
        
    def dibujarParedes(self):
        #Dibuja pared 1
        glPushMatrix()
        glTranslatef(self.ancho+100, -240.0, 0.0)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texturas[1])
        glBegin(GL_QUADS)

        
        glTexCoord2f(0.0, 0.0)
        glVertex3d(0, 0, -self.largo)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(0, 0, self.largo)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(0, 500, self.largo)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(0, 500, -self.largo)
        glEnd()    
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
        
        #Dibuja pared 2
        glPushMatrix()
        glRotatef(180, 0.0, 1.0, 0.0)
        glTranslatef(0.0, -240.0, -self.largo)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texturas[2])
        glBegin(GL_QUADS)
        
        
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-self.ancho-100, 0, 0)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(self.ancho+100, 0, 0)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(self.ancho+100, 500, 0)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(-self.ancho-100, 500, 0)
        glEnd()    
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
        
        #Dibuja pared 3
        glPushMatrix()
        glTranslatef(-self.ancho-100, -240.0, 0.0)
        glRotatef(180.0, 0.0, 1.0, 0.0)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texturas[3])
        glBegin(GL_QUADS)
        
        
        glTexCoord2f(0.0, 0.0)
        glVertex3d(0, 0, -self.largo)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(0, 0, self.largo)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(0, 500, self.largo)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(0, 500, -self.largo)
        glEnd()    
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
        #Dibuja pared 4
        glPushMatrix()
        glTranslatef(0.0, -240.0, -self.largo)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texturas[4])
        glBegin(GL_QUADS)
        
        
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-self.ancho-100, 0, 0)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(self.ancho+100, 0, 0)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(self.ancho+100, 500, 0)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(-self.ancho-100, 500, 0)
        glEnd()    
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

        #Dibuja cielo
        glPushMatrix()
        glRotatef(270.0, 0.0, 1.0, 0.0)
        glTranslatef(0.0, 259.9, 0)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texturas[6])
        glBegin(GL_QUADS)
        
        
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-self.ancho-100, 0, -self.largo)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(self.ancho+100, 0, -self.largo)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(self.ancho+100, 0, self.largo)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(-self.ancho-100, 0, self.largo)
        glEnd()    
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
        
        #Complementar laterales
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texturas[5])
        glBegin(GL_QUADS)
        
        glTexCoord2f(0.0, 0.0)
        glVertex3d(self.ancho, 0, -self.largo)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(self.ancho+100, 0, -self.largo)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(self.ancho+100, 0, self.largo)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(self.ancho, 0, self.largo)
        glEnd()    
        glDisable(GL_TEXTURE_2D)
        
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texturas[5])
        glBegin(GL_QUADS)
        
        
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-self.ancho, 0, -self.largo)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(-self.ancho-100, 0, -self.largo)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(-self.ancho-100, 0, self.largo)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(-self.ancho, 0, self.largo)
        glEnd()    
        glDisable(GL_TEXTURE_2D)
        
        # Configurar materiales para las paredes
        wall_material_diffuse = [1.0, 1.0, 1.0, 1.0]  # Color difuso de las paredes (gris claro)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, wall_material_diffuse)
        
    def dibujaPorteria(self):
        glBegin(GL_QUADS)
        glColor3fv((1, 1, 1))
        # PORTERIA 1 
        #POSTE 1
        # Cara frontal blanco
        glVertex3f(28.0, -1.0, -1.0) #233 = -1
        glVertex3f(30.0, -1.0, -1.0)
        glVertex3f(30.0, 25.0, -1.0)
        glVertex3f(28.0, 25.0, -1.0)
        # Cara trasera
        glVertex3f(28.0, -1.0, 1.0) #231 = 1
        glVertex3f(30.0, -1.0, 1.0)
        glVertex3f(30.0, 25.0, 1.0)
        glVertex3f(28.0, 25.0, 1.0)
        # Cara izquierda
        glVertex3f(30.0, -1.0, -1.0)
        glVertex3f(30.0, -1.0, 1.0)
        glVertex3f(30.0, 25.0, 1.0)
        glVertex3f(30.0, 25.0, -1.0)
        # Cara derecha
        glVertex3f(28.0, -1.0, 1.0)
        glVertex3f(28.0, -1.0, -1.0)
        glVertex3f(28.0, 25.0, -1.0)
        glVertex3f(28.0, 25.0, 1.0)
        glEnd()
        glBegin(GL_QUADS)
        glColor3fv((1, 1, 1))
        #POSTE 2
        # Cara frontal blansco
        glVertex3f(-28.0, -1.0, -1.0)
        glVertex3f(-30.0, -1.0, -1.0)
        glVertex3f(-30.0, 25.0, -1.0)
        glVertex3f(-28.0, 25.0, -1.0)
        # Cara trasera
        glVertex3f(-28.0, -1.0, 1.0)
        glVertex3f(-30.0, -1.0, 1.0)
        glVertex3f(-30.0, 25.0, 1.0)
        glVertex3f(-28.0, 25.0, 1.0)
        # Cara izquierda
        glVertex3f(-30.0, -1.0, -1.0)
        glVertex3f(-30.0, -1.0, 1.0)
        glVertex3f(-30.0, 25.0, 1.0)
        glVertex3f(-30.0, 25.0, -1.0)
        # Cara derecha
        glVertex3f(-28.0, -1.0, 1.0)
        glVertex3f(-28.0, -1.0, -1.0)
        glVertex3f(-28.0, 25.0, -1.0)
        glVertex3f(-28.0, 25.0, 1.0)
        glEnd()
        glBegin(GL_QUADS)
        glColor3fv((1, 1, 1))
        #POSTE 3
        # Parte abajo
        glVertex3f(-28.0, 23.0, -1.0)
        glVertex3f(-30.0, 23.0, -1.0)
        glVertex3f(30.0, 23.0, -1.0)
        glVertex3f(28.0, 23.0, -1.0)
        #Parte arriba
        glVertex3f(-28.0, 25.0, -1.0)
        glVertex3f(-30.0, 25.0, -1.0)
        glVertex3f(30.0, 25.0, -1.0)
        glVertex3f(28.0, 25.0, -1.0)
        #Parte enfrente 
        glVertex3f(-30.0, 25.0, -1.0)
        glVertex3f(-30.0, 23.0, -1.0)
        glVertex3f(30.0, 23.0, -1.0)
        glVertex3f(30.0, 25.0, -1.0)
        #Parte atras
        glVertex3f(-28.0, 25.0, -1.0)
        glVertex3f(-28.0, 23.0, -1.0)
        glVertex3f(28.0, 23.0, -1.0)
        glVertex3f(28.0, 25.0, -1.0)
        glEnd()