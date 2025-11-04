import sympy as sp
from sympy import symbols, sympify, diff, lambdify
import numpy as np

def calcular_derivadas_parciales(funcion_str, punto=None):
    """
    Calcula derivadas parciales, gradiente y derivadas de orden superior
    """
    try:
        x, y = symbols('x y')
        funcion = sympify(funcion_str)
        
        # Derivadas parciales de primer orden
        df_dx = diff(funcion, x)
        df_dy = diff(funcion, y)
        
        # Derivadas parciales de segundo orden
        d2f_dx2 = diff(df_dx, x)
        d2f_dy2 = diff(df_dy, y)
        d2f_dxdy = diff(df_dx, y)
        
        resultado = {
            'funcion': str(funcion),
            'derivadas_primer_orden': {
                'df/dx': str(df_dx),
                'df/dy': str(df_dy)
            },
            'derivadas_segundo_orden': {
                'd²f/dx²': str(d2f_dx2),
                'd²f/dy²': str(d2f_dy2),
                'd²f/dxdy': str(d2f_dxdy)
            }
        }
        
        # Si se proporciona un punto, evaluar
        if punto and len(punto) == 2:
            x_val, y_val = punto
            
            gradiente_valor = [
                float(df_dx.subs([(x, x_val), (y, y_val)])),
                float(df_dy.subs([(x, x_val), (y, y_val)]))
            ]
            
            # Calcular magnitud del gradiente
            magnitud = np.sqrt(gradiente_valor[0]**2 + gradiente_valor[1]**2)
            
            # Calcular dirección de máximo crecimiento
            if magnitud > 0:
                direccion = [g/magnitud for g in gradiente_valor]
            else:
                direccion = [0, 0]
            
            resultado['evaluacion_punto'] = {
                'punto': punto,
                'gradiente': gradiente_valor,
                'magnitud_gradiente': float(magnitud),
                'direccion_max_crecimiento': direccion,
                'valor_funcion': float(funcion.subs([(x, x_val), (y, y_val)]))
            }
            
            # Matriz Hessiana
            hessiana = [
                [float(d2f_dx2.subs([(x, x_val), (y, y_val)])),
                 float(d2f_dxdy.subs([(x, x_val), (y, y_val)]))],
                [float(d2f_dxdy.subs([(x, x_val), (y, y_val)])),
                 float(d2f_dy2.subs([(x, x_val), (y, y_val)]))]
            ]
            
            resultado['evaluacion_punto']['hessiana'] = hessiana
            
            # Clasificar punto crítico
            det_hessiana = hessiana[0][0] * hessiana[1][1] - hessiana[0][1]**2
            
            if det_hessiana > 0:
                if hessiana[0][0] > 0:
                    clasificacion = "Mínimo local"
                else:
                    clasificacion = "Máximo local"
            elif det_hessiana < 0:
                clasificacion = "Punto silla"
            else:
                clasificacion = "Prueba no concluyente"
            
            resultado['evaluacion_punto']['clasificacion'] = clasificacion
        
        resultado['exito'] = True
        return resultado
    
    except Exception as e:
        return {
            'error': f'Error al calcular derivadas: {str(e)}',
            'exito': False
        }

def calcular_derivada_direccional(funcion_str, punto, direccion):
    """
    Calcula la derivada direccional en un punto y dirección dados
    """
    try:
        x, y = symbols('x y')
        funcion = sympify(funcion_str)
        
        # Calcular gradiente
        df_dx = diff(funcion, x)
        df_dy = diff(funcion, y)
        
        # Evaluar gradiente en el punto
        grad = [
            float(df_dx.subs([(x, punto[0]), (y, punto[1])])),
            float(df_dy.subs([(x, punto[0]), (y, punto[1])]))
        ]
        
        # Normalizar dirección
        norm_dir = np.sqrt(direccion[0]**2 + direccion[1]**2)
        dir_unitaria = [direccion[0]/norm_dir, direccion[1]/norm_dir]
        
        # Producto punto
        deriv_direccional = grad[0] * dir_unitaria[0] + grad[1] * dir_unitaria[1]
        
        return {
            'derivada_direccional': float(deriv_direccional),
            'gradiente': grad,
            'direccion_unitaria': dir_unitaria,
            'exito': True
        }
    
    except Exception as e:
        return {
            'error': f'Error al calcular derivada direccional: {str(e)}',
            'exito': False
        }
