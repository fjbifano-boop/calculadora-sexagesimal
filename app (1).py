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
    2;13,20
    0;27
    5
    -1;12,30
    """
    s = s.strip().replace(" ", "")

    if not s:
        raise ValueError("La entrada está vacía.")

    sign = -1 if s.startswith("-") else 1

    if s.startswith(("-", "+")):
        s = s[1:]

    if ";" in s:
        integer_part, fractional_part = s.split(";", 1)
        integer_part = int(integer_part) if integer_part else 0
        digits = fractional_part.split(",") if fractional_part else []
    else:
        integer_part = int(s)
        digits = []

    value = Fraction(integer_part, 1)

    for i, digit in enumerate(digits, start=1):
        if digit == "":
            raise ValueError("Hay una posición sexagesimal vacía.")

        n = int(digit)

        if not 0 <= n < 60:
            raise ValueError(
                "Cada posición sexagesimal debe contener un valor entre 0 y 59."
            )

        value += Fraction(n, 60**i)

    return sign * value


def to_sexagesimal(x, places=4) -> str:
    """
    Convierte Fraction o float a notación sexagesimal.
    """
    if isinstance(x, float):
        x = Fraction(x).limit_denominator(10**9)

    sign = "-" if x < 0 else ""
    x = abs(x)

    integer_part = x.numerator // x.denominator
    remainder = x - integer_part

    digits = []

    for _ in range(places):
        remainder *= 60
        digit = remainder.numerator // remainder.denominator
        digits.append(int(digit))
        remainder -= digit

    # Elimina ceros finales innecesarios
    while digits and digits[-1] == 0:
        digits.pop()

    if not digits:
        return f"{sign}{integer_part}"

    return f"{sign}{integer_part};" + ",".join(
        f"{digit:02d}" for digit in digits
    )


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

    `2;13,20` significa:

    2 + 13/60 + 20/60²

    El punto y coma separa la parte entera y la coma separa
    las posiciones sexagesimales.
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
            value="2;13,20",
            key="number_a"
        )

    with col2:
        b_text = st.text_input(
            "Número B",
            value="0;27",
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
                    f"**A:** {to_sexagesimal(a, places)} "
                    f"= {decimal_string(a)}"
                )

                if operation in [
                    "A + B",
                    "A − B",
                    "A × B",
                    "A ÷ B"
                ]:
                    st.write(
                        f"**B:** {to_sexagesimal(b, places)} "
                        f"= {decimal_string(b)}"
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
            value="2;13,20",
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
            value="2.222222",
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
# Nota
# -------------------------------------------------

st.divider()

st.caption(
    "Calculadora diseñada para explorar operaciones en sistema "
    "sexagesimal y apoyar el estudio de prácticas matemáticas "
    "paleobabilónicas."
)
