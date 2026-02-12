## Proyecto Final – Videojuego 3D con Inteligencia Artificial (Alfa-Beta)
## Descripción general

Este proyecto consiste en el desarrollo de un videojuego 3D interactivo implementado en Python, utilizando OpenGL para el renderizado gráfico y un sistema de Inteligencia Artificial clásica basado en el algoritmo de búsqueda Alfa-Beta para controlar el comportamiento de los enemigos, tener coliciones e interaacciones.

El objetivo principal del proyecto es integrar gráficos 3D, lógica de juego y toma de decisiones inteligente, demostrando cómo un agente artificial puede evaluar múltiples estados futuros y seleccionar acciones óptimas en tiempo real dentro de un entorno virtual.

## Objetivos del Proyecto

- Implementar un videojuego funcional en 3D

- Aplicar Inteligencia Artificial clásica en un entorno interactivo

- Integrar algoritmos de búsqueda con gráficos en tiempo real

- Demostrar habilidades en programación, lógica y diseño de sistemas

## Inteligencia Artificial Implementada

La IA del proyecto se basa en el algoritmo Alfa-Beta, una optimización del algoritmo Minimax, ampliamente utilizado en juegos de estrategia y toma de decisiones.

Funcionamiento de la IA

Los enemigos del juego actúan como agentes inteligentes, capaces de:

- Analizar su posición actual en el escenario

- Evaluar la posición del jugador

- Simular múltiples movimientos futuros

- Elegir la acción que maximiza su probabilidad de atrapar al jugador

Para lograr esto, la IA implementa:

- Generación de estados

Donde el sistema genera posibles movimientos del enemigo en ocho direcciones, creando un espacio de búsqueda que representa los estados futuros del juego.

Función heurística:

Cada estado es evaluado mediante una función heurística basada en la distancia euclidiana entre el enemigo y el jugador. Cuanto menor sea la distancia, mejor se considera el estado.

Esta evaluación permite que la IA:

- Persiga al jugador de forma inteligente

- Ajuste su comportamiento dinámicamente

## Poda Alfa-Beta

El algoritmo reduce significativamente el costo computacional al eliminar ramas del árbol de búsqueda que no influyen en la decisión final, permitiendo una ejecución eficiente en tiempo real.

## Inteligencia Artificial
Los rivales utilizan:
- Generación de movimientos en 8 direcciones
- Evaluación por distancia al jugador
- Algoritmo Alfa-Beta con profundidad configurable

## Mecánicas de Juego

- Control del jugador en un entorno 3D

- Movimiento libre dentro de límites definidos

- Enemigos controlados por IA

- Sistema de persecución inteligente

- Colisiones y límites del escenario

- Interacción en tiempo real entre jugador y agentes enemigos

## Gráficos y Renderizado

El apartado gráfico del proyecto está desarrollado con OpenGL, incluyendo:

- Renderizado de modelos 3D (.OBJ)

- Texturizado de superficies

- Manejo de cámara y perspectiva

- Control de iluminación

- Uso de librerías auxiliares para carga de modelos y texturas

Esto permite crear un entorno visual interactivo donde la lógica de la IA se manifiesta de forma clara y observable.

## Arquitectura del Proyecto

El proyecto está estructurado para separar responsabilidades:

- Lógica de IA.

- Algoritmos de búsqueda, heurísticas y toma de decisiones.

- Entidades del juego.

- Jugador, enemigos y sus propiedades.

- Motor gráfico.

-Renderizado, manejo de cámara y escena.

- Control del juego.

- Entrada del usuario, actualización de estados y bucle principal.

## Control y Movimiento

El jugador se desplaza libremente por el escenario utilizando el teclado:

- W / S → Avanzar y retroceder

- A / D → Desplazamiento lateral

- Mouse → Rotación y orientación de la cámara

El movimiento es continuo y está basado en la dirección actual de la cámara, lo que permite una experiencia de control fluida y natural.

## Sistema de Velocidad

El jugador puede activar un aumento temporal de velocidad, lo que permite desplazarse más rápido durante un corto periodo de tiempo.
Este sistema incluye:

- Duración limitada del aumento

- Temporizador de recuperación

- Restablecimiento automático de la velocidad normal

Esto añade una mecánica estratégica al movimiento del jugador.

## Esta separación facilita:

- Mantenimiento

- Escalabilidad

- Comprensión del código

## Pruebas y Simulación

El proyecto incluye módulos de prueba que permiten ejecutar el algoritmo de IA de forma aislada, sin necesidad de cargar el entorno gráfico, esto permite:

-Validar la lógica de decisión

- Ajustar la heurística

- Depurar errores de comportamiento

# Tecnologías Utilizadas

Lenguaje: Python

Gráficos: OpenGL

IA: Minimax con poda Alfa-Beta

Modelos 3D: Archivos OBJ

Matemáticas: Distancia euclidiana, árboles de decisión

## Posibles Mejoras Futuras

Implementación de múltiples niveles

Ajuste dinámico de dificultad

IA con aprendizaje (reinforcement learning)

Optimización del rendimiento gráfico

Mejora de colisiones y físicas

## Conclusión

Este proyecto demuestra la integración efectiva de Inteligencia Artificial clásica y gráficos 3D, logrando un sistema interactivo donde los enemigos no siguen reglas simples, sino que razonan y toman decisiones basadas en la simulación de estados futuros. Es un ejemplo claro de cómo los algoritmos de búsqueda pueden aplicarse en videojuegos para crear comportamientos realistas e inteligentes, y representa una base sólida para proyectos más complejos en el área de desarrollo de videojuegos e IA.


## Ejecución
```bash
pip install -r requirements.txt
python src/main.py

