# Proyecto Milei

## Programa de Ingeniería Industrial

# Integrantes:
- David Villegas Ceballos
- Daniel Felipe Hincapie López

# Matricula de Estudiantes
El proyecto Milei nos ayuda a que si nos dan una lista de estudiantes con su respectivo nivel nos automatiza la inscripción a sus cursos del semestre que este.

## Descripción del código:

El codigo hecho hace lo siguiente:
- Se le proporciona unos datos de los estudiantes, además de una malla curricular de la materia en un archivo xlsx, en el código se le añade los superlinks para que no tenga que descargar los archivos y moverlos.
- Para cada asignatura se le genera un código único del curso los cuales son tres letras alusivas a la materia además de dos números los cuales son parte de los créditos de la materia y del semestre al que pertenece la misma, y asi se genera respectivamente. Ejemplo : Cálculo Diferencial, creditos 3, semestre 1, código generado : CAL31.
- Dado los números de estudiantes en x semestre y los cupos en cada materia  se crearan diferentes grupos para que todos los estudiantes queden matriculados en todas las materias que le corresponden.
- Después de tener todos los estudiantes asignados se agregan todas las especificaciones de la materia como horas trabajo independiente, horas docente, entre otros.
- Cuando se hace todo esto se crean archivos en Excel y en cvs con todos los estudiantes en sus cursos.
- Registra detalladamente lo que hace el código con los procedimientos.

## Dependencias:

- pandas: Se utiliza para operaciones como lectura y escritura de archivos CSV, Excel, bases de datos SQL, y para realizar manipulaciones complejas de datos (filtrado, agregación, limpieza, etc.).
- os: Se utiliza para operaciones como navegar por el sistema de archivos, crear y eliminar directorios, manipular archivos y obtener información sobre el entorno de ejecución.
- logging: Se utiliza para registrar información sobre el flujo de una aplicación y para la depuración, almacenando logs en archivos o mostrándolos en la consola
- platform: Se utiliza para obtener detalles sobre la plataforma donde se está ejecutando Python, como el nombre del sistema operativo, la versión del sistema, el nombre del nodo, la versión del kernel, etc.
- time: Se utiliza para medir la duración de la ejecución de código, realizar retrasos en la ejecución (sleep), y para obtener y manipular marcas de tiempo (timestamps)
- datetime: Se utiliza para obtener la fecha y hora actuales, realizar cálculos con fechas y horas, formatear y analizar fechas y horas en diferentes formatos.
- numpy:Se utiliza para realizar operaciones numéricas de alto rendimiento, como álgebra lineal, transformadas de Fourier, generación de números aleatorios, y otras operaciones matemáticas avanzadas

## Descargar para el funcionamiento óptimo:

- pip install pandas
- pip install xlsxwriter

### El código fue probado en Visual Code, se recomienda probrarlo en ese programa
