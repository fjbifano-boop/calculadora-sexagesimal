import streamlit as st
from fractions import Fraction
from math import sqrt

st.set_page_config(
    page_title="Calculadora sexagesimal",
    page_icon="🔢",
    layout="centered"
)

# -------------------------------------------------
# Conversión entre notación sexagesimal y decimal
# -------------------------------------------------

def parse_sexagesimal(s: str) -> Fraction:
    """
    Convierte una cadena sexagesimal a Fraction.

    Ejemplos admitidos:
    8;30
    2;13;20
    5
    -1;12;30

    Nota:
    Se admite también la coma como separador de posiciones
    fraccionarias por compatibilidad con entradas anteriores:
    2;13,20
    """
    s = s.strip().replace(" ", "")

    if not s:
        raise ValueError("La entrada está vacía.")

    sign = -1 if s.startswith("-") else 1

    if s.startswith(("-", "+")):
        s = s[1:]

    # Compatibilidad: 2;13,20 -> 2;13;20
    s = s.replace(",", ";")

    parts = s.split(";")

    if any(part == "" for part in parts):
        raise ValueError("Hay una posición sexagesimal vacía.")

    digits = [int(part) for part in parts]

    # Todas las posiciones salvo la primera deben estar entre 0 y 59.
    for d in digits[1:]:
        if not 0 <= d < 60:
            raise ValueError(
                "Cada posición sexagesimal posterior a la primera debe estar entre 0 y 59."
            )

    # Interpretación convencional de la app:
    # la primera posición se toma como unidades y las siguientes
    # como 1/60, 1/60², etc.
    value = Fraction(digits[0], 1)

    for i, d in enumerate(digits[1:], start=1):
        value += Fraction(d, 60**i)

    return sign * value


def to_sexagesimal(x, places=5) -> str:
    """
    Convierte un número a notación sexagesimal posicional completa.

    Ejemplos:
    8.5     -> 8;30
    72.25   -> 1;12;15
    2.2222  -> 2;13;19;55...

    La parte entera también se descompone en potencias de 60.
    """

    if isinstance(x, float):
        x = Fraction(x).limit_denominator(10**9)

    sign = "-" if x < 0 else ""
    x = abs(x)

    integer_part = x.numerator // x.denominator
    remainder = x - integer_part

    # Parte entera en base 60
    integer_digits = []

    if integer_part == 0:
        integer_digits = [0]
    else:
        n = integer_part

        while n > 0:
            integer_digits.insert(0, n % 60)
            n //= 60

    # Parte fraccionaria
    fractional_digits = []

    for _ in range(places):
        if remainder == 0:
            break

        remainder *= 60
        digit = remainder.numerator // remainder.denominator
        fractional_digits.append(int(digit))
        remainder -= digit

    digits = integer_digits + fractional_digits

    return sign + ";".join(str(d) for d in digits)


def decimal_string(x: Fraction, decimals=10) -> str:
    return f"{float(x):.{decimals}f}"


def reciprocal(x: Fraction) -> Fraction:
    if x == 0:
        raise ZeroDivisionError("No existe el recíproco de 0.")
    return Fraction(1, 1) / x


# -------------------------------------------------
# Interfaz
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
    **Convención utilizada**

    Las posiciones se separan con `;`.

    Por ejemplo:

    `8;30`

    representa:

    8 + 30/60

    y

    `1;12;15`

    representa:

    1×60 + 12 + 15/60

    La aplicación también acepta entradas como `2;13,20`
    y las interpreta como `2;13;20`.
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
        max_value=10,
        value=5
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
                if a < 0:
                    raise ValueError(
                        "No existe raíz cuadrada real de un número negativo."
                    )

                root = sqrt(float(a))

                st.success("Resultado")

                c1, c2 = st.columns(2)

                with c1:
                    st.metric(
                        "Sexagesimal",
                        to_sexagesimal(root, places)
                    )

                with c2:
                    st.metric(
                        "Decimal",
                        f"{root:.10f}"
                    )

                with st.expander("Ver valor interpretado"):
                    st.write(
                        f"**A:** {a_text} = {decimal_string(a)}"
                    )

                st.stop()

            st.success("Resultado")

            c1, c2 = st.columns(2)

            with c1:
                st.metric(
                    "Sexagesimal",
                    to_sexagesimal(result, places)
                )

            with c2:
                st.metric(
                    "Decimal",
                    decimal_string(result)
                )

            with st.expander("Ver valores interpretados"):
                st.write(
                    f"**A:** {a_text} = {decimal_string(a)}"
                )

                if operation in [
                    "A + B",
                    "A − B",
                    "A × B",
                    "A ÷ B"
                ]:
                    st.write(
                        f"**B:** {b_text} = {decimal_string(b)}"
                    )

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
            value="1;12;15",
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
            10,
            5,
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
# Nota y contacto
# -------------------------------------------------

st.divider()

st.caption(
    "Calculadora diseñada para explorar operaciones en sistema "
    "sexagesimal y apoyar el estudio de prácticas matemáticas "
    "paleobabilónicas."
)

st.markdown(
    """
    **Contacto:** Fernando Bifano  
    CeFIEC/CCPEMS – FCEN, UBA  
    ✉️ [fjbifano@ccpems.exactas.uba.ar](mailto:fjbifano@ccpems.exactas.uba.ar)
    """
)
