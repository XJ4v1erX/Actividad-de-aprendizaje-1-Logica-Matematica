# Importación de módulos
import re
from gpiozero import LED

# Expresión regular para buscar letras mayúsculas en la contraseña
regex_uppercase = re.compile(r'[A-Z]')
# Expresión regular para buscar símbolos en la contraseña
regex_symbol = re.compile(r'[^a-zA-Z0-9\s]')
# Expresiones regulares para verificar palabras comunes en la contraseña
regex_common_words = re.compile(r'\b(?:' + '|'.join(['password', '123456', 'qwerty', 'admin', 'user', 'iloveyou']) + r')\b', re.IGNORECASE)

# Crear objetos para los LEDs.
led_verde = LED(2)      # LED para contraseñas seguras
led_amarillo = LED(3)   # LED para contraseñas medianamente seguras
led_rojo = LED(4)       # LED para contraseñas inseguras


"""
Verifica la seguridad de una contraseña.

Args:
    password (str): La contraseña a evaluar.

Returns:
    str: Un mensaje que indica si la contraseña es "Segura", "Medianamente segura" o "Insegura".
"""

def password_security(password):
    state = 1   # Estado inicial de la contraseña: 1 (Insegura)

    # Verificar si la contraseña cumple con la longitud mínima y no contiene palabras comunes
    if len(password) >= 8 and not regex_common_words.search(password):
        state = 2   # Estado: 2 (Segura o medianamente segura, dependiendo de otros requisitos)

    # Verificar si la contraseña contiene al menos una letra mayúscula y al menos un símbolo
    has_uppercase = regex_uppercase.search(password)
    has_symbol = regex_symbol.search(password)

    if state == 2 and has_uppercase and has_symbol:
        return "Segura"
    elif state == 2 and (not has_uppercase or not has_symbol):
        return "Medianamente segura"
    else:
        return "Insegura"


"""
Controla los LEDs según el nivel de seguridad de la contraseña.

Args:
    security_level (str): El nivel de seguridad de la contraseña ("Segura", "Medianamente segura" o "Insegura").

"""

def controlar_leds(security_level):
    # Apagar todos los LEDs al principio
    led_verde.off()
    led_amarillo.off()
    led_rojo.off()

    # Encender el LED correspondiente según el nivel de seguridad
    if security_level == "Segura":
        led_verde.on()
    elif security_level == "Medianamente segura":
        led_amarillo.on()
    else:
        led_rojo.on()

if __name__ == "__main__":
    # Bucle infinito para solicitar contraseñas y verificar su seguridad
    while True:
        password_input = input("Ingrese una contraseña: ")
        security_level = password_security(password_input)
        print("Contraseña:", security_level)

        # Apagar todos los LEDs antes de controlarlos nuevamente
        led_verde.off()
        led_amarillo.off()
        led_rojo.off()

        # Controlar los LEDs según el resultado de la función password_security
        controlar_leds(security_level)
