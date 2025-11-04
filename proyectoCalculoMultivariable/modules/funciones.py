import sympy as sp
import numpy as np
from sympy import symbols, sympify, lambdify, limit, oo

def analizar_funcion_completa(funcion_str):
    """
    Analiza una función de dos variables: dominio, rango, límites
    """
    try:
        x, y = symbols('x y')
        funcion = sympify(funcion_str)
        
        # Calcular dominio
        dominio = calcular_dominio(funcion, x, y)
        
        # Calcular rango (aproximado)
        rango = calcular_rango_aproximado(funcion, x, y)
        
        # Calcular límites importantes
        limites = calcular_limites(funcion, x, y)
        
        # Puntos críticos
        puntos_criticos = encontrar_puntos_criticos(funcion, x, y)
        
        return {
            'funcion': str(funcion),
            'dominio': dominio,
            'rango': rango,
            'limites': limites,
            'puntos_criticos': puntos_criticos,
            'exito': True
        }
    
    except Exception as e:
        return {
            'error': f'Error al analizar función: {str(e)}',
            'exito': False
        }

def calcular_dominio(funcion, x, y):
    """Determina el dominio de la función"""
    try:
        # Buscar restricciones comunes
        restricciones = []
        
        # Verificar denominadores
        if funcion.as_numer_denom()[1] != 1:
            denominador = funcion.as_numer_denom()[1]
            restricciones.append(f"Denominador ≠ 0: {denominador} ≠ 0")
        
        # Verificar raíces cuadradas
        if 'sqrt' in str(funcion):
            restricciones.append("Argumento de raíz ≥ 0")
        
        # Verificar logaritmos
        if 'log' in str(funcion):
            restricciones.append("Argumento de logaritmo > 0")
        
        if not restricciones:
            return "ℝ² (todos los reales)"
        else:
            return " y ".join(restricciones)
    
    except:
        return "No determinado"

def calcular_rango_aproximado(funcion, x, y):
    """Calcula un rango aproximado de la función"""
    try:
        # Evaluar en una malla de puntos
        f_lambda = lambdify((x, y), funcion, 'numpy')
        x_vals = np.linspace(-10, 10, 50)
        y_vals = np.linspace(-10, 10, 50)
        X, Y = np.meshgrid(x_vals, y_vals)
        
        Z = f_lambda(X, Y)
        
        # Filtrar valores infinitos o NaN
        Z_valido = Z[np.isfinite(Z)]
        
        if len(Z_valido) > 0:
            min_val = np.min(Z_valido)
            max_val = np.max(Z_valido)
            return f"[{min_val:.2f}, {max_val:.2f}] (aproximado)"
        else:
            return "No determinado"
    
    except:
        return "No determinado"

def calcular_limites(funcion, x, y):
    """Calcula límites importantes de la función"""
    limites_resultado = {}
    
    try:
        # Límite cuando x,y -> 0
        lim_origen = limit(limit(funcion, x, 0), y, 0)
        limites_resultado['(x,y) → (0,0)'] = str(lim_origen)
    except:
        limites_resultado['(x,y) → (0,0)'] = 'No existe o no determinado'
    
    try:
        # Límite cuando x -> infinito
        lim_x_inf = limit(funcion.subs(y, 0), x, oo)
        limites_resultado['x → ∞ (y=0)'] = str(lim_x_inf)
    except:
        limites_resultado['x → ∞ (y=0)'] = 'No existe o no determinado'
    
    return limites_resultado

def encontrar_puntos_criticos(funcion, x, y):
    """Encuentra puntos críticos de la función"""
    try:
        # Calcular derivadas parciales
        df_dx = sp.diff(funcion, x)
        df_dy = sp.diff(funcion, y)
        
        # Resolver sistema de ecuaciones
        puntos = sp.solve([df_dx, df_dy], [x, y])
        
        if isinstance(puntos, dict):
            puntos = [puntos]
        
        resultado = []
        for punto in puntos[:5]:  # Limitar a 5 puntos
            if isinstance(punto, dict):
                resultado.append({
                    'x': float(punto[x]) if punto[x].is_real else str(punto[x]),
                    'y': float(punto[y]) if punto[y].is_real else str(punto[y])
                })
            elif isinstance(punto, tuple):
                resultado.append({
                    'x': float(punto[0]) if punto[0].is_real else str(punto[0]),
                    'y': float(punto[1]) if punto[1].is_real else str(punto[1])
                })
        
        return resultado if resultado else "No se encontraron puntos críticos"
    
    except:
        return "No se pudieron calcular"
