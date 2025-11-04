import sympy as sp
from sympy import symbols, sympify, integrate, lambdify
import numpy as np

def calcular_integral_multiple(funcion_str, limites, tipo='doble'):
    """
    Calcula integral doble o triple
    limites formato: [[x_min, x_max], [y_min, y_max], [z_min, z_max]]
    """
    try:
        if tipo == 'doble':
            return calcular_integral_doble(funcion_str, limites)
        elif tipo == 'triple':
            return calcular_integral_triple(funcion_str, limites)
        else:
            return {
                'error': 'Tipo de integral no válido',
                'exito': False
            }
    
    except Exception as e:
        return {
            'error': f'Error al calcular integral: {str(e)}',
            'exito': False
        }

def calcular_integral_doble(funcion_str, limites):
    """
    Calcula integral doble ∫∫ f(x,y) dA
    """
    try:
        x, y = symbols('x y')
        funcion = sympify(funcion_str)
        
        # Extraer límites
        x_lim = limites[0]  # [x_min, x_max]
        y_lim = limites[1]  # [y_min, y_max]
        
        # Convertir límites a expresiones sympy si son strings
        x_min = sympify(str(x_lim[0]))
        x_max = sympify(str(x_lim[1]))
        y_min = sympify(str(y_lim[0]))
        y_max = sympify(str(y_lim[1]))
        
        # Calcular integral iterada
        integral_interna = integrate(funcion, (y, y_min, y_max))
        integral_total = integrate(integral_interna, (x, x_min, x_max))
        
        # Intentar evaluar numéricamente
        try:
            valor_numerico = float(integral_total)
        except:
            valor_numerico = None
        
        # Calcular área de la región
        area = (x_max - x_min) * (y_max - y_min)
        try:
            area_valor = float(area)
        except:
            area_valor = None
        
        return {
            'funcion': str(funcion),
            'tipo': 'Integral Doble',
            'limites': {
                'x': [str(x_min), str(x_max)],
                'y': [str(y_min), str(y_max)]
            },
            'integral_simbolica': str(integral_total),
            'valor_numerico': valor_numerico,
            'area_region': area_valor,
            'interpretacion': generar_interpretacion_doble(valor_numerico, area_valor),
            'exito': True
        }
    
    except Exception as e:
        return {
            'error': f'Error en integral doble: {str(e)}',
            'exito': False
        }

def calcular_integral_triple(funcion_str, limites):
    """
    Calcula integral triple ∫∫∫ f(x,y,z) dV
    """
    try:
        x, y, z = symbols('x y z')
        funcion = sympify(funcion_str)
        
        # Extraer límites
        x_lim = limites[0]
        y_lim = limites[1]
        z_lim = limites[2]
        
        # Convertir límites
        x_min, x_max = sympify(str(x_lim[0])), sympify(str(x_lim[1]))
        y_min, y_max = sympify(str(y_lim[0])), sympify(str(y_lim[1]))
        z_min, z_max = sympify(str(z_lim[0])), sympify(str(z_lim[1]))
        
        # Calcular integral iterada
        integral_z = integrate(funcion, (z, z_min, z_max))
        integral_y = integrate(integral_z, (y, y_min, y_max))
        integral_total = integrate(integral_y, (x, x_min, x_max))
        
        # Intentar evaluar numéricamente
        try:
            valor_numerico = float(integral_total)
        except:
            valor_numerico = None
        
        # Calcular volumen de la región
        volumen = (x_max - x_min) * (y_max - y_min) * (z_max - z_min)
        try:
            volumen_valor = float(volumen)
        except:
            volumen_valor = None
        
        return {
            'funcion': str(funcion),
            'tipo': 'Integral Triple',
            'limites': {
                'x': [str(x_min), str(x_max)],
                'y': [str(y_min), str(y_max)],
                'z': [str(z_min), str(z_max)]
            },
            'integral_simbolica': str(integral_total),
            'valor_numerico': valor_numerico,
            'volumen_region': volumen_valor,
            'interpretacion': generar_interpretacion_triple(valor_numerico, volumen_valor),
            'exito': True
        }
    
    except Exception as e:
        return {
            'error': f'Error en integral triple: {str(e)}',
            'exito': False
        }

def generar_interpretacion_doble(valor, area):
    """Genera interpretación física de la integral doble"""
    interpretaciones = []
    
    if valor is not None:
        interpretaciones.append(f"Volumen bajo la superficie: {valor:.4f} unidades cúbicas")
        
        if area is not None and area != 0:
            altura_promedio = valor / area
            interpretaciones.append(f"Altura promedio de la función: {altura_promedio:.4f}")
    
    if area is not None:
        interpretaciones.append(f"Área de la región de integración: {area:.4f} unidades cuadradas")
    
    return interpretaciones if interpretaciones else ["No se pudo generar interpretación"]

def generar_interpretacion_triple(valor, volumen):
    """Genera interpretación física de la integral triple"""
    interpretaciones = []
    
    if valor is not None:
        interpretaciones.append(f"Valor de la integral: {valor:.4f}")
        interpretaciones.append("Puede representar: masa total, carga total, o cantidad acumulada")
        
        if volumen is not None and volumen != 0:
            densidad_promedio = valor / volumen
            interpretaciones.append(f"Valor promedio en la región: {densidad_promedio:.4f}")
    
    if volumen is not None:
        interpretaciones.append(f"Volumen de la región: {volumen:.4f} unidades cúbicas")
    
    return interpretaciones if interpretaciones else ["No se pudo generar interpretación"]
