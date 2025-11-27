# Bike Parking

## Descripción
Proyecto personal realizado individualmente para el módulo de Estructuras de Control en PYthon (ESPY) del curso de Desarrollo de Aplicaciones en Lenguaje Python (DALP)

## Dependencias y Entorno
Este proyecto usa Python en su versión 3.13.5 y se puede descargar en el siguiente [enlace](https://www.python.org/downloads/release/python-3135/)
Para ejecutar el programa se recomienda crear un entorno virtual e instalar todas las dependencias del archivo requirements.txt.
Tambien se recomienda instalar el proyecto como editable para que pytest y otros módulos puedan recorrer las carpetas correctamente.

En Windows:
```powershell
python -m venv .
.\venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```
En Linux:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Ejecutar la aplicación
Primero hay que clonar el repositorio en nuestro equipo de manera local
```bash
git clone https://github.com/marlopia/bike_parking
```

Para ejecutar y usar la aplicación basta con situarse dentro de la carpeta src y ejecutar el archivo app.py

```bash
cd src
python app.py
```

Dentro de la aplicación basta con seguir las instrucciones del programa para poder realizar las operaciones, tales como:
- Guardado de usuarios y bicis
- Borrado de usuarios y bicis
- Registro de retirada y guardado de bicis

## Ejecutar tests y cobertura
Usando pytest podemos comprobar que el código no tenga problemas, también al clonar el repositorio nos hemos creado un workflow de Github Actions que verifique que los tests devuelvan OK para poder hacer merge en las ramas de dev y main.
Para lanzar pytest basta con lanzar el siguiente comando desde la raiz
```bash
pytest tests
```
Para obtener más información por pantalla podemos lanzar el comando con el atributo "verbose"
```bash
pytest tests -v
```
Para obtener la cobertura de los tests usamos el paquete pytest-cov ejecutando este comando
```bash
pytest --cov=src
```
También disponemos de un html en la carpeta docs/htmlcov/index.html

## Documentación de las funciones
Todas las funciones vienen con comentarios en formato docstrings, podemos ver un html básico de los docstrings de cada archivo de python en la carpeta docs.
Para generar documentación basta con usar este comando
```bash
pydoc -w tu_modulo
```

## Estado del sprint y decisiones técnicas relevantes
Con la release de la versión 2.0 el primer sprint realizado entre el 20/11/2025 y el 2/12/2025 se ha completado con todos los objetivos realizados.
Durante el sprint se han tomado algunas decisiones técnicas que han variado de la arquitectura sugeridad por motivos de desarrollo, estas han sido:
- Omitir el uso de existe_usuario y existe_bici dado a que es_dni_unico y es_num_serie_unico tienen la misma funcionalidad
- Desplazar la responsabilidad de interacción del usuario desde ui_console a menu_handlers dado a que en la capa inferior se tenía mayor control sobre el flujo de mensajes
- Se ha intentado usar sphinx en vez de pydoc para la documentación HTML pero no se han conseguido resultados satisfactorios dentro del límite de tiempo asignado
Un mayor desglose del primer sprint puede ser encontrado en docs/desglose_sprint_1.docx