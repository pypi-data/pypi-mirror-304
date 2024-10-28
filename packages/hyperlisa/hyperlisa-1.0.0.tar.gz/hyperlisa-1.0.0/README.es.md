[English](README.md) | [Italiano](README.it.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Español](README.es.md)

# Lisa - Analizador de Código para LLM

Lisa (inspirado en Lisa Simpson) es una herramienta diseñada para simplificar el análisis de código fuente a través de Modelos de Lenguaje Grande (LLM). Inteligente y analítica como el personaje del que toma su nombre, Lisa ayuda a estudiar e interpretar el código con lógica y método.

## Descripción

Lisa es una herramienta esencial para aquellos que desean analizar su código o estudiar proyectos de código abierto a través de Modelos de Lenguaje Grande. Su objetivo principal es generar un único archivo de texto que mantiene todas las referencias y la estructura del código original, haciéndolo fácilmente interpretable por un LLM.

Este enfoque resuelve uno de los problemas más comunes en el análisis de código con LLMs: la fragmentación de archivos y la pérdida de referencias entre diferentes componentes del proyecto.

## Configuración

El proyecto utiliza un archivo de configuración `combine_config.yaml` que permite personalizar qué archivos incluir o excluir del análisis. La configuración predeterminada es:

```yaml
# Patrones de inclusión (extensiones o directorios a incluir)
includes:
  - "*.py"  
  # Puedes agregar otras extensiones o directorios

# Patrones de exclusión (directorios o archivos a excluir)
excludes:
  - ".git"
  - "__pycache__"
  - "*.egg-info"
  - "venv*"
  - ".vscode"
  - "agents*"
  - "log"
```

### Patrones de Inclusión/Exclusión
- Los patrones en `includes` determinan qué archivos serán procesados (ej: "*.py" incluye todos los archivos Python)
- Los patrones en `excludes` especifican qué archivos o directorios ignorar
- Puedes usar el carácter * como comodín
- Los patrones se aplican tanto a nombres de archivos como a rutas de directorios
- **Importante**: Las reglas de exclusión siempre tienen prioridad sobre las reglas de inclusión

### Prioridad de Reglas
Cuando hay "conflictos" entre reglas de inclusión y exclusión, las de exclusión siempre tienen prioridad. Aquí algunos ejemplos:

```
Ejemplo 1:
/project_root
    /src_code
        /utils
            /logs
                file1.py
                file2.py
            helpers.py
```
Si tenemos estas reglas:
- includes: ["*.py"]
- excludes: ["*logs"]

En este caso, `file1.py` y `file2.py` NO serán incluidos a pesar de tener la extensión .py porque están en un directorio que coincide con el patrón de exclusión "*logs". El archivo `helpers.py` sí será incluido.

```
Ejemplo 2:
/project_root
    /includes_dir
        /excluded_subdir
            important.py
```
Si tenemos estas reglas:
- includes: ["includes_dir"]
- excludes: ["*excluded*"]

En este caso, `important.py` NO será incluido porque está en un directorio que coincide con un patrón de exclusión, aunque su directorio padre coincida con un patrón de inclusión.

## Uso

El script se ejecuta desde la línea de comandos con:

```bash
cmb [opciones]
```

> **Nota**: El guion bajo inicial en el nombre del archivo es intencional y permite usar la completación automática (TAB) en la shell.

### Estructura y Nombre Predeterminado
Para entender qué nombre de archivo se usará por defecto, consideremos esta estructura:

```
/home/user/proyectos
    /mi_proyecto_prueba     <- Este es el directorio raíz
        /scripts
            _combine_code.py
            combine_config.yaml
        /src
            main.py
        /tests
            test_main.py
```

En este caso, el nombre predeterminado será "MI_PROYECTO_PRUEBA" (el nombre del directorio raíz en mayúsculas).

### Parámetros disponibles:

- `--clean`: Elimina los archivos de texto generados previamente
- `--output NOMBRE`: Especifica el prefijo del nombre del archivo de salida
  ```bash
  # Ejemplo con nombre predeterminado (de la estructura anterior)
  cmb
  # Salida: MI_PROYECTO_PRUEBA_20240327_1423.txt

  # Ejemplo con nombre personalizado
  cmb --output ANALISIS_PROYECTO
  # Salida: ANALISIS_PROYECTO_20240327_1423.txt
  ```

### Salida

El script genera un archivo de texto con el formato:
`NOMBRE_AAAAMMDD_HHMM.txt`

donde:
- `NOMBRE` es el prefijo especificado con --output o el predeterminado
- `AAAAMMDD_HHMM` es la marca de tiempo de generación

## Uso con Proyectos GitHub

Para usar Lisa con un proyecto GitHub, sigue estos pasos:

1. **Preparación del entorno**:
   ```bash
   # Crea y accede a un directorio para tus proyectos
   mkdir ~/proyectos
   cd ~/proyectos
   ```

2. **Clona el proyecto a analizar**:
   ```bash
   # Ejemplo con un proyecto hipotético "moon_project"
   git clone moon_project.git
   ```

3. **Integra Lisa en el proyecto**:
   ```bash
   # Clona el repositorio de Lisa
   git clone https://github.com/tunombre/lisa.git

   # Copia la carpeta scripts de Lisa en moon_project
   cp -r lisa/scripts moon_project/
   cp lisa/scripts/combine_config.yaml moon_project/scripts/
   ```

4. **Ejecuta el análisis**:
   ```bash
   cd moon_project
   cmb
   ```

### Mejores Prácticas para el Análisis
- Antes de ejecutar Lisa, asegúrate de estar en el directorio raíz del proyecto a analizar
- Revisa y personaliza el archivo `combine_config.yaml` según las necesidades específicas del proyecto
- Usa la opción `--clean` para mantener ordenado el directorio cuando generes múltiples versiones

## Notas Adicionales

- Lisa mantiene la estructura jerárquica de archivos en el documento generado
- Cada archivo está claramente delimitado por separadores que indican su ruta relativa
- El código se organiza manteniendo el orden de profundidad de los directorios
- Los archivos generados pueden compartirse fácilmente con LLMs para su análisis

## Contribuir

Si deseas contribuir al proyecto, puedes:
- Abrir issues para reportar bugs o proponer mejoras
- Enviar pull requests con nuevas funcionalidades
- Mejorar la documentación
- Compartir tus casos de uso y sugerencias

## Licencia

Licencia MIT

Copyright (c) 2024

Por la presente se concede permiso, libre de cargos, a cualquier persona que obtenga una copia
de este software y de los archivos de documentación asociados (el "Software"), para utilizar
el Software sin restricción, incluyendo sin limitación los derechos a usar, copiar, modificar,
fusionar, publicar, distribuir, sublicenciar, y/o vender copias del Software, y a permitir a
las personas a las que se les proporcione el Software a hacer lo mismo, sujeto a las siguientes
condiciones:

El aviso de copyright anterior y este aviso de permiso se incluirán en todas las copias o partes
sustanciales del Software.

EL SOFTWARE SE PROPORCIONA "TAL CUAL", SIN GARANTÍA DE NINGÚN TIPO, EXPRESA O IMPLÍCITA,
INCLUYENDO PERO NO LIMITADO A GARANTÍAS DE COMERCIALIZACIÓN, IDONEIDAD PARA UN PROPÓSITO
PARTICULAR Y NO INFRACCIÓN. EN NINGÚN CASO LOS AUTORES O TITULARES DEL COPYRIGHT SERÁN
RESPONSABLES DE NINGUNA RECLAMACIÓN, DAÑOS U OTRAS RESPONSABILIDADES, YA SEA EN UNA ACCIÓN
DE CONTRATO, AGRAVIO O CUALQUIER OTRO MOTIVO, QUE SURJA DE O EN CONEXIÓN CON EL SOFTWARE
O EL USO U OTRO TIPO DE ACCIONES EN EL SOFTWARE.