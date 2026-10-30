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

        if any(part == "" for part in fractional_parts):
            raise ValueError("Hay una posición vacía en la parte fraccionaria.")

        for i, part in enumerate(fractional_parts, start=1):
            digit = int(part)

            if not 0 <= digit < 60:
                raise ValueError(
                    "Cada posición sexagesimal debe contener un valor entre 0 y 59."
                )

            fractional_value += Fraction(digit, 60**i)

    return sign * (integer_value + fractional_value)


def to_sexagesimal(x, places=6) -> str:
    """
    Convierte Fraction o float a notación sexagesimal.

    Ejemplos:
        8.5    -> 8;30
        72.25  -> 1,12;15
        2.2222 -> 2;13,19,55...
    """
    if isinstance(x, float):
        x = Fraction(x).limit_denominator(10**12)

    sign = "-" if x < 0 else ""
    x = abs(x)

    integer_part = x.numerator // x.denominator
    remainder = x - integer_part

    # -------------------------
    # Parte entera en base 60
    # -------------------------

    integer_digits = []

    if integer_part == 0:
        integer_digits = [0]
    else:
        n = integer_part

        while n > 0:
            integer_digits.insert(0, n % 60)
            n //= 60

    integer_string = ",".join(str(d) for d in integer_digits)

    # -------------------------
    # Parte fraccionaria
    # -------------------------

    fractional_digits = []

    for _ in range(places):
        if remainder == 0:
            break

        remainder *= 60
        digit = remainder.numerator // remainder.denominator
        fractional_digits.append(int(digit))
        remainder -= digit

    if fractional_digits:
        fractional_string = ",".join(str(d) for d in fractional_digits)
        return f"{sign}{integer_string};{fractional_string}"

    return f"{sign}{integer_string}"


def decimal_string(x: Fraction, decimals=10) -> str:
    return f"{float(x):.{decimals}f}"


def reciprocal(x: Fraction) -> Fraction:
    if x == 0:
        raise ZeroDivisionError("No existe el recíproco de 0.")
    return Fraction(1, 1) / x


def exact_or_approx_sqrt(x: Fraction):
    """
    Devuelve una raíz exacta como Fraction cuando numerador y
    denominador son cuadrados perfectos. En otro caso devuelve float.
    """
    if x < 0:
        raise ValueError("No existe raíz cuadrada real de un número negativo.")

    num = x.numerator
    den = x.denominator

    num_root = isqrt(num)
    den_root = isqrt(den)

    if num_root * num_root == num and den_root * den_root == den:
        return Fraction(num_root, den_root)

    return sqrt(float(x))


# -------------------------------------------------
# INTERFAZ
# -------------------------------------------------

st.title("Calculadora sexagesimal")

st.write(
    """
    Herramienta para realizar operaciones con números escritos
    en notación sexagesimal.
    """
)

st.info(
    """
    **Convención de escritura**

    - La **coma (,)** separa posiciones sexagesimales.
    - El **punto y coma (;)** separa la parte entera de la fraccionaria.

    Ejemplos:

    - `8;30` = 8 + 30/60
    - `2;13,20` = 2 + 13/60 + 20/60²
    - `1,12;15` = 1×60 + 12 + 15/60

    De este modo:

    `8;30² = 1,12;15`

    y

    `√1,12;15 = 8;30`
    """
)

tab_calculator, tab_converter = st.tabs(
    ["Calculadora", "Conversor"]
)

# -------------------------------------------------
# CALCULADORA
# -------------------------------------------------

with tab_calculator:

    st.subheader("Operaciones")

    col1, col2 = st.columns(2)

    with col1:
        a_text = st.text_input(
            "Número A",
            value="8;30",
            key="number_a"
        )

    with col2:
        b_text = st.text_input(
            "Número B",
            value="",
            key="number_b"
        )

    operation = st.selectbox(
        "Operación",
        [
            "A + B",
            "A − B",
            "A × B",
            "A ÷ B",
            "Recíproco de A",
            "A²",
            "√A"
        ]
    )

    places = st.slider(
        "Cantidad máxima de posiciones sexagesimales",
        min_value=1,
        max_value=12,
        value=6
    )

    if st.button("Calcular", type="primary"):

        try:
            a = parse_sexagesimal(a_text)

            if operation in ["A + B", "A − B", "A × B", "A ÷ B"]:
                if not b_text.strip():
                    raise ValueError("Ingresá un valor para el número B.")
                b = parse_sexagesimal(b_text)

            if operation == "A + B":
                result = a + b

            elif operation == "A − B":
                result = a - b

            elif operation == "A × B":
                result = a * b

            elif operation == "A ÷ B":
                if b == 0:
                    raise ZeroDivisionError("No se puede dividir por 0.")
                result = a / b

            elif operation == "Recíproco de A":
                result = reciprocal(a)

            elif operation == "A²":
                result = a * a

            elif operation == "√A":
                result = exact_or_approx_sqrt(a)

            st.success("Resultado")

            c1, c2 = st.columns(2)

            with c1:
                st.metric(
                    "Sexagesimal",
                    to_sexagesimal(result, places)
                )

            with c2:
                if isinstance(result, Fraction):
                    dec_result = decimal_string(result)
                else:
                    dec_result = f"{result:.10f}"

                st.metric(
                    "Decimal",
                    dec_result
                )

            with st.expander("Ver valores interpretados"):
                st.write(
                    f"**A:** `{a_text}` = {decimal_string(a)}"
                )

                if operation in [
                    "A + B",
                    "A − B",
                    "A × B",
                    "A ÷ B"
                ]:
                    st.write(
                        f"**B:** `{b_text}` = {decimal_string(b)}"
                    )

                if operation == "√A" and isinstance(result, Fraction):
                    st.write("La raíz es **exacta**.")

        except Exception as e:
            st.error(str(e))


# -------------------------------------------------
# CONVERSOR
# -------------------------------------------------

with tab_converter:

    st.subheader("Conversión")

    mode = st.radio(
        "Tipo de conversión",
        [
            "Sexagesimal → decimal",
            "Decimal → sexagesimal"
        ]
    )

    if mode == "Sexagesimal → decimal":

        value_text = st.text_input(
            "Número sexagesimal",
            value="1,12;15",
            key="sex_to_dec"
        )

        if st.button("Convertir", key="button_sex_to_dec"):

            try:
                value = parse_sexagesimal(value_text)

                st.success(
                    f"Decimal: {decimal_string(value)}"
                )

            except Exception as e:
                st.error(str(e))

    else:

        decimal_text = st.text_input(
            "Número decimal",
            value="72.25",
            key="dec_to_sex"
        )

        converter_places = st.slider(
            "Posiciones sexagesimales",
            1,
            12,
            6,
            key="converter_places"
        )

        if st.button("Convertir", key="button_dec_to_sex"):

            try:
                value = float(decimal_text.replace(",", "."))

                st.success(
                    "Sexagesimal: "
                    + to_sexagesimal(
                        value,
                        converter_places
                    )
                )

            except Exception as e:
                st.error(str(e))


# -------------------------------------------------
# NOTA HISTÓRICA
# -------------------------------------------------

st.divider()

st.caption(
    "La notación empleada aquí es una convención moderna destinada a "
    "hacer inequívoca la posición de cada cifra. En los textos paleobabilónicos "
    "no se utilizaba un separador equivalente a nuestro punto sexagesimal; "
    "la magnitud debía inferirse por el contexto."
)

# -------------------------------------------------
# CONTACTO
# -------------------------------------------------

st.markdown(
    """
    **Contacto**  
    Fernando Bifano  
    CeFIEC/CCPEMS – FCEN, UBA  
    ✉️ [fjbifano@ccpems.exactas.uba.ar](mailto:fjbifano@ccpems.exactas.uba.ar)
    """
)
