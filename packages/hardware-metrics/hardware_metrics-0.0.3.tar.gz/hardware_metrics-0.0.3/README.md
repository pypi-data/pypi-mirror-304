# Hardware metrics

Librería desarrollada para la evaluación de consumo de recursos hardware por un método.

Para ello se ha desarrollado un decorador que se coloca sobre la función que ejecuta el código del que queremos obtener las métricas.

## Instalación

- Clonar repositorio
- Ejecutar el siguiente comando
        
        python3 -m pip install --upgrade build
        python3 -m build
        
- Tras ello se habrá creado una carpeta /dist con un fichero con formato .whl, se deberá hacer pip install y la ruta al archivo, esto instalará la librería y todas las dependencias en el environment actual.

## Uso

Para importar la función principal de la librería:

``` python
from hardware_metrics import hardware_metrics
```

Para usar el método, se deberá poner encima de la función el decorador importado:

``` python
@hardware_metrics('path/de/prueba')
def hello_world: #función de ejemplo
    print('hola')
```

También se puede escribir sin path para que se utilice el path por defecto 'hardware_metrics_results':

``` python
@hardware_metrics()
def hello_world: #función de ejemplo
    print('hola')
```