# Calculadora sexagesimal

Aplicación desarrollada en **Streamlit** para realizar cálculos con números escritos en notación sexagesimal.

La herramienta permite trabajar con expresiones como:

- `2;13,20`
- `0;27`
- `5`
- `1;12,30`

## Convención utilizada

En esta aplicación:

- `;` separa la parte entera de la parte fraccionaria.
- `,` separa las sucesivas posiciones sexagesimales.

Por ejemplo:

`2;13,20`

representa:

2 + 13/60 + 20/60²

## Operaciones disponibles

La calculadora permite realizar:

- suma
- resta
- multiplicación
- división
- cálculo del recíproco
- cuadrado
- raíz cuadrada
- conversión entre notación decimal y sexagesimal

Los resultados se muestran tanto en formato sexagesimal como decimal.

## Uso

Para ejecutar la aplicación localmente:

```bash
streamlit run calculadora_sexagesimal.py
```

## Requisitos

La aplicación requiere Python y Streamlit.

Las dependencias se encuentran especificadas en el archivo:

`requirements.txt`

## Propósito

La aplicación fue diseñada como recurso para explorar procedimientos de cálculo en sistema sexagesimal y como apoyo para el estudio de prácticas matemáticas paleobabilónicas.
