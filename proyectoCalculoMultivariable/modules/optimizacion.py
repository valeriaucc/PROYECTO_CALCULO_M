import sympy as sp
from sympy import symbols, sympify, diff, solve, lambdify
import numpy as np

def optimizar_con_lagrange(funcion_str, restriccion_str, tipo='max'):
    """
    Optimiza una función con restricciones usando multiplicadores de Lagrange
    """
    try:
        x, y, lam = symbols('x y lambda')
        funcion = sympify(funcion_str)
        restriccion = sympify(restriccion_str)
        
        # Construir Lagrangiano: L = f(x,y) ± λ·g(x,y)
        if tipo == 'max':
            lagrangiano = funcion - lam * restriccion
        else:
            lagrangiano = funcion + lam * restriccion
        
        # Calcular derivadas parciales
        dL_dx = diff(lagrangiano, x)
        dL_dy = diff(lagrangiano, y)
        dL_dlam = diff(lagrangiano, lam)
        
        # Resolver sistema de ecuaciones
        soluciones = solve([dL_dx, dL_dy, dL_dlam], [x, y, lam])
        
        if not soluciones:
            return {
                'error': 'No se encontraron puntos críticos',
                'exito': False
            }
        
        # Si es una sola solución, convertir a lista
        if isinstance(soluciones, dict):
            soluciones = [soluciones]
        
        # Evaluar función en cada solución
        puntos_criticos = []
        for sol in soluciones:
            try:
                if isinstance(sol, dict):
                    x_val = float(sol[x])
                    y_val = float(sol[y])
                    lam_val = float(sol[lam]) if lam in sol else None
                elif isinstance(sol, tuple):
                    x_val = float(sol[0])
                    y_val = float(sol[1])
                    lam_val = float(sol[2]) if len(sol) > 2 else None
                else:
                    continue
                
                # Evaluar función objetivo
                f_val = float(funcion.subs([(x, x_val), (y, y_val)]))
                
                puntos_criticos.append({
                    'x': x_val,
                    'y': y_val,
                    'lambda': lam_val,
                    'valor_funcion': f_val
                })
            except:
                continue
        
        if not puntos_criticos:
            return {
                'error': 'No se pudieron evaluar los puntos críticos',
                'exito': False
            }
        
        # Encontrar óptimo
        if tipo == 'max':
            optimo = max(puntos_criticos, key=lambda p: p['valor_funcion'])
        else:
            optimo = min(puntos_criticos, key=lambda p: p['valor_funcion'])
        
        return {
            'funcion': str(funcion),
            'restriccion': str(restriccion),
            'tipo': tipo,
            'lagrangiano': str(lagrangiano),
            'sistema_ecuaciones': {
                'dL/dx': str(dL_dx),
                'dL/dy': str(dL_dy),
                'dL/dλ': str(dL_dlam)
            },
            'puntos_criticos': puntos_criticos,
            'optimo': optimo,
            'exito': True
        }
    
    except Exception as e:
        return {
            'error': f'Error en optimización: {str(e)}',
            'exito': False
        }

def optimizar_sin_restricciones(funcion_str):
    """
    Encuentra máximos y mínimos sin restricciones
    """
    try:
        x, y = symbols('x y')
        funcion = sympify(funcion_str)
        
        # Derivadas parciales
        df_dx = diff(funcion, x)
        df_dy = diff(funcion, y)
        
        # Puntos críticos
        puntos = solve([df_dx, df_dy], [x, y])
        
        if isinstance(puntos, dict):
            puntos = [puntos]
        
        # Derivadas de segundo orden
        d2f_dx2 = diff(df_dx, x)
        d2f_dy2 = diff(df_dy, y)
        d2f_dxdy = diff(df_dx, y)
        
        resultados = []
        for punto in puntos:
            try:
                if isinstance(punto, dict):
                    x_val = float(punto[x])
                    y_val = float(punto[y])
                elif isinstance(punto, tuple):
                    x_val = float(punto[0])
                    y_val = float(punto[1])
                else:
                    continue
                
                # Evaluar Hessiana
                H11 = float(d2f_dx2.subs([(x, x_val), (y, y_val)]))
                H22 = float(d2f_dy2.subs([(x, x_val), (y, y_val)]))
                H12 = float(d2f_dxdy.subs([(x, x_val), (y, y_val)]))
                
                det_H = H11 * H22 - H12**2
                
                # Clasificar
                if det_H > 0:
                    if H11 > 0:
                        tipo = "Mínimo local"
                    else:
                        tipo = "Máximo local"
                elif det_H < 0:
                    tipo = "Punto silla"
                else:
                    tipo = "Prueba no concluyente"
                
                f_val = float(funcion.subs([(x, x_val), (y, y_val)]))
                
                resultados.append({
                    'punto': [x_val, y_val],
                    'valor': f_val,
                    'tipo': tipo,
                    'determinante_hessiana': det_H
                })
            except:
                continue
        
        return {
            'funcion': str(funcion),
            'puntos_criticos': resultados,
            'exito': True
        }
    
    except Exception as e:
        return {
            'error': f'Error en optimización: {str(e)}',
            'exito': False
        }
