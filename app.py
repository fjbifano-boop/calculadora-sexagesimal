import streamlit as st
from fractions import Fraction
from math import sqrt, isqrt

st.set_page_config(
    page_title="Calculadora sexagesimal",
    page_icon="🔢",
    layout="centered"
)

# -------------------------------------------------
# NOTACIÓN
# -------------------------------------------------
#
# Convención usada en esta calculadora:
#
#   coma (,)       = separa posiciones sexagesimales
#   punto y coma (;) = separa la parte entera de la fraccionaria
#
# Ejemplos:
#
#   8;30       = 8 + 30/60
#   2;13,20    = 2 + 13/60 + 20/60²
#   1,12;15    = 1×60 + 12 + 15/60
#
# Esta convención hace reversible la entrada y la salida.


# -------------------------------------------------
# Conversión entre notación sexagesimal y Fraction
# -------------------------------------------------

def parse_sexagesimal(s: str) -> Fraction:
    """
    Convierte una cadena sexagesimal a Fraction.

    Ejemplos:
        8;30
        2;13,20
        1,12;15
        5
        -1,12;15
    """
    s = s.strip().replace(" ", "")

    if not s:
        raise ValueError("La entrada está vacía.")

    sign = -1 if s.startswith("-") else 1

    if s.startswith(("-", "+")):
        s = s[1:]

    if s.count(";") > 1:
        raise ValueError("El número puede contener un solo punto y coma (;).")

    if ";" in s:
        integer_text, fractional_text = s.split(";", 1)
    else:
        integer_text = s
        fractional_text = ""

    # -------------------------
    # Parte entera sexagesimal
    # -------------------------

    if integer_text == "":
        integer_digits = [0]
    else:
        integer_parts = integer_text.split(",")

        if any(part == "" for part in integer_parts):
            raise ValueError("Hay una posición vacía en la parte entera.")

        integer_digits = [int(part) for part in integer_parts]

        # Salvo la primera posición, todas deben estar entre 0 y 59.
        for digit in integer_digits[1:]:
            if not 0 <= digit < 60:
                raise ValueError(
                    "Cada posición sexagesimal debe contener un valor entre 0 y 59."
                )

    integer_value = Fraction(0, 1)

    for digit in integer_digits:
        integer_value = integer_value * 60 + digit

    # -------------------------
    # Parte fraccionaria
    # -------------------------

    fractional_value = Fraction(0, 1)

    if fractional_text:
        fractional_parts = fractional_text.split(",")
