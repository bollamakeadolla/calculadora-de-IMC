import curses
from curses.textpad import Textbox
import re

def main(stdscr):
    curses.curs_set(1)
    line = -1

    pad_height = 500
    pad_width = 100
    pad = curses.newpad(pad_height, pad_width)
    pad_y = 0

    # Use a list to collect lines (like JS array + push)
    data_lines = []

    def isNameValid(name):
        return re.fullmatch(r"^[A-Za-zÀ-ÖØ-öø-ÿ' -]+$", name) is not None

    def isFloatString(string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    def is_not_escape(key):
        if key == 27:
            raise SystemExit()
        return key

    def is_not_enter_or_escape(key):
        if key == 10:
            return curses.ascii.BEL
        return is_not_escape(key)

    def auto_increment_line():
        nonlocal line
        line += 1
        return line

    def refresh_pad():
        nonlocal pad, pad_y
        pad_y = max(0, line - curses.LINES + 1)
        pad.refresh(pad_y, 0, 0, 0, curses.LINES-1, curses.COLS-1)

    def input_with_echo(prompt, width=20, validate_func=None, error_msg="Entrada inválida"):
        nonlocal pad, line, pad_y
        while True:
            current_line = auto_increment_line()
            pad.addstr(current_line, 0, prompt)
            refresh_pad()

            screen_y = min(current_line - pad_y, curses.LINES - 1)
            screen_x = len(prompt)
            editwin = curses.newwin(1, width, screen_y, screen_x)
            box = Textbox(editwin)
            box.edit(is_not_enter_or_escape)
            value = box.gather().strip()

            if validate_func is None or validate_func(value):
                pad.addstr(current_line, len(prompt), value)
                refresh_pad()
                return value
            else:
                pad.addstr(auto_increment_line(), 0, f"{error_msg}, intente de nuevo.")
                refresh_pad()

    # ----------------- Start UI -----------------
    pad.addstr(auto_increment_line(), 0, "Bienvenido a la calculadora de IMC", curses.A_BOLD)
    pad.addstr(auto_increment_line(), 0, "(presione ESC para salir)", curses.A_DIM)
    refresh_pad()

    personas = int(input_with_echo(
        "Personas a calcular: ", 5,
        lambda x: x.isdigit() and int(x) > 0,
        "Número inválido"
    ))

    s = input_with_echo(
        "Sistema de medida (metrico/imperial): ", 10,
        lambda x: x.lower() in ["metrico", "imperial"],
        "Debe ser 'metrico' o 'imperial'"
    ).strip().lower()

    persona_index = 1
    while persona_index <= personas:
        pad.addstr(auto_increment_line(), 0, f"--- Datos de Persona {persona_index} ---")
        refresh_pad()

        # collect and strip inputs right away
        n = input_with_echo("Nombre: ", 30, isNameValid).strip()
        a = input_with_echo("Apellido Paterno: ", 30, isNameValid).strip()
        am = input_with_echo("Apellido Materno: ", 30, isNameValid).strip()
        e = int(input_with_echo("Edad: ", 5, lambda x: x.isdigit() and int(x) > 0).strip())

        if s == "metrico":
            p_raw = input_with_echo("Masa en kilogramos: ", 10, lambda x: isFloatString(x) and float(x) > 0)
            p = float(p_raw.strip())
            est_raw = input_with_echo("Altura en metros: ", 10, lambda x: isFloatString(x) and float(x) > 0)
            est = float(est_raw.strip())
        else:
            p_raw = input_with_echo("Peso en libras: ", 10, lambda x: isFloatString(x) and float(x) > 0)
            p = float(p_raw.strip()) * 0.453592
            est_raw = input_with_echo("Altura en pulgadas: ", 10, lambda x: isFloatString(x) and float(x) > 0)
            est = float(est_raw.strip()) * 0.0254

        pad.addstr(auto_increment_line(), 0, "----------------------------------------------")

        IMC = round(p / est**2, 2)
        edad_status = "menor de edad" if e < 18 else "mayor de edad"

        if IMC <= 15.99:
            classification = "Delgadez severa"
        elif IMC <= 16.99:
            classification = "Delgadez moderada"
        elif IMC <= 18.49:
            classification = "Delgadez leve"
        elif IMC <= 24.99:
            classification = "Normal"
        elif IMC <= 29.99:
            classification = "Sobrepeso"
        elif IMC <= 34.99:
            classification = "Obesidad leve"
        elif IMC <= 39.99:
            classification = "Obesidad media"
        else:
            classification = "Obesidad mórbida"

        pad.addstr(auto_increment_line(), 0, f"IMC: {IMC}")
        pad.addstr(auto_increment_line(), 0, f"Usted es {edad_status}")
        pad.addstr(auto_increment_line(), 0, f"Clasificación: {classification}")
        pad.addstr(auto_increment_line(), 0, "----------------------------------------------")
        refresh_pad()

        # --------- push cleaned lines into data_lines (like JS array.push) ----------
        data_lines.append(f"Persona {persona_index}:".strip())
        data_lines.append(f"Nombre: {n} {a} {am}".strip())
        data_lines.append(f"Edad: {e}".strip())
        data_lines.append(f"Masa: {p:.2f} kg".strip())
        data_lines.append(f"Altura: {est:.2f} m".strip())
        data_lines.append(f"IMC: {IMC}".strip())
        data_lines.append(f"Estado: {edad_status}".strip())
        data_lines.append(f"Clasificación: {classification}".strip())
        data_lines.append("-" * 50)

        pad.addstr(auto_increment_line(), 0, "Presione cualquier tecla para continuar...")
        refresh_pad()
        pad.getkey()

        persona_index += 1

    pad.addstr(auto_increment_line(), 0, "Todos los cálculos han sido completados. Presione cualquier tecla para salir.")
    refresh_pad()
    pad.getkey()

    # join with CR (carriage return) + LF for compatibility
    return "\r\n".join(line.strip() for line in data_lines)

if __name__ == "__main__":
    data = curses.wrapper(main)
    print("\nDATOS DE TODAS LAS PERSONAS:\n")
    print(data)
