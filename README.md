## Proyecto Final – Videojuego 3D con Inteligencia Artificial (Alfa-Beta)
## Descripción general

Este proyecto consiste en el desarrollo de un videojuego 3D interactivo implementado en Python, utilizando OpenGL para el renderizado gráfico y un sistema de Inteligencia Artificial clásica basado en el algoritmo de búsqueda Alfa-Beta para controlar el comportamiento de los enemigos, tener coliciones e interaacciones

El objetivo principal del proyecto es integrar gráficos 3D, lógica de juego y toma de decisiones inteligente, demostrando cómo un agente artificial puede evaluar múltiples estados futuros y seleccionar acciones óptimas en tiempo real dentro de un entorno virtual.

🧠 Inteligencia Artificial Implementada

La IA del proyecto se basa en el algoritmo Alfa-Beta, una optimización del algoritmo Minimax, ampliamente utilizado en juegos de estrategia y toma de decisiones.

🔍 Funcionamiento de la IA

Los enemigos del juego actúan como agentes inteligentes, capaces de:

Analizar su posición actual en el escenario

Evaluar la posición del jugador

Simular múltiples movimientos futuros

Elegir la acción que maximiza su probabilidad de atrapar al jugador

Para lograr esto, la IA implementa:

✔ Generación de estados

El sistema genera posibles movimientos del enemigo en ocho direcciones, creando un espacio de búsqueda que representa los estados futuros del juego.

✔ Función heurística

Cada estado es evaluado mediante una función heurística basada en la distancia euclidiana entre el enemigo y el jugador.
Cuanto menor sea la distancia, mejor se considera el estado.

Esta evaluación permite que la IA:

Persiga al jugador de forma inteligente

Ajuste su comportamiento dinámicamente

✔ Poda Alfa-Beta

El algoritmo reduce significativamente el costo computacional al eliminar ramas del árbol de búsqueda que no influyen en la decisión final, permitiendo una ejecución eficiente en tiempo real.

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
