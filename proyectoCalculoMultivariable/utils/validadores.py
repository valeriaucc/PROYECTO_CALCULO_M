import re
from sympy import sympify, symbols
from sympy.parsing.sympy_parser import parse_expr

def validar_funcion(funcion_str):
    """
    Valida que una función sea válida matemáticamente
    """
    if not funcion_str or not isinstance(funcion_str, str):
        return False
    
    # Eliminar espacios
    funcion_str = funcion_str.strip()
    
    if len(funcion_str) == 0:
        return False
    
    # Verificar caracteres permitidos
    patron = r'^[0-9a-zA-Z+\-*/().,\s\^**sqrt()log()exp()sin()cos()tan()]+$'
    if not re.match(patron, funcion_str):
        return False
    
    try:
        # Intentar parsear con sympy
        sympify(funcion_str)
        return True
    except:
        return False

def validar_punto(punto):
    """
    Valida que un punto sea válido
    """
    if not isinstance(punto, (list, tuple)):
        return False
    
    if len(punto) < 2:
        return False
    
    try:
        for coord in punto:
            float(coord)
        return True
    except:
        return False

def validar_limites(limites):
    """
    Valida que los límites de integración sean válidos
    """
    if not isinstance(limites, list):
        return False
    
    if len(limites) < 2:
        return False
    
    for limite in limites:
        if not isinstance(limite, list) or len(limite) != 2:
            return False
    
    return True

def sanitizar_entrada(texto):
    """
    Sanitiza entrada del usuario
    """
    if not texto:
        return ""
    
    # Reemplazar caracteres comunes
    texto = texto.replace('^', '**')
    texto = texto.replace('√', 'sqrt')
    texto = texto.replace('π', 'pi')
    texto = texto.replace('∞', 'oo')
    
    return texto.strip()