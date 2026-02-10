# 3d-futbol-game-opengl-ia
Soccer 3D OpenGL AI 

Videojuego 3D de fútbol desarrollado en Python, usando Pygame y OpenGL.
Incluye IA construida para rivales basada en el algoritmo Alfa-Beta Pruning.

## Características
- Entorno 3D con OpenGL
- Movimiento libre del jugador
- Rivales con IA (búsqueda Alfa-Beta)
- Porteros con movimiento automático
- Colisiones jugador–rival y balón–portería
- Texturas, modelos OBJ y sonido ambiental

## Inteligencia Artificial
Los rivales utilizan:
- Generación de movimientos en 8 direcciones
- Evaluación por distancia al jugador
- Algoritmo Alfa-Beta con profundidad configurable

## Tecnologías
- Python 3
- Pygame
- PyOpenGL
- NumPy

## Ejecución
```bash
pip install -r requirements.txt
python src/main.py
