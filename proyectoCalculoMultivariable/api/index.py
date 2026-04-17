import os
import sys
from pathlib import Path

# Agregar el directorio del proyecto al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import sympy as sp
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import json

app = Flask(__name__, 
            static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'),
            template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))
CORS(app)
app.secret_key = os.environ.get('SECRET_KEY', 'tu_clave_secreta_aqui_cambiala_en_produccion')

# Símbolos matemáticos
x, y, z = sp.symbols('x y z')

# Inicializar historial en sesión
def init_historial():
    if 'historial' not in session:
        session['historial'] = []

@app.route('/')
def index():
    init_historial()
    return render_template('index.html')

@app.route('/historial')
def historial():
    init_historial()
    return render_template('historial.html', historial=session.get('historial', []))

# API: Graficar superficie 3D
@app.route('/api/graficar_superficie', methods=['POST'])
def graficar_superficie():
    try:
        data = request.get_json()
        funcion_str = data.get('funcion')
        x_range = data.get('x_range', [-5, 5])
        y_range = data.get('y_range', [-5, 5])
        
        # Parsear función
        funcion = sp.sympify(funcion_str)
        
        # Crear función numérica
        f = sp.lambdify((x, y), funcion, 'numpy')
        
        # Crear malla
        x_vals = np.linspace(x_range[0], x_range[1], 50)
        y_vals = np.linspace(y_range[0], y_range[1], 50)
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = f(X, Y)
        
        # Crear gráfico
        fig = go.Figure(data=[go.Surface(
            x=X.tolist(), 
            y=Y.tolist(), 
            z=Z.tolist(), 
            colorscale='Viridis'
        )])
        fig.update_layout(
            title=f'f(x,y) = {funcion_str}',
            scene=dict(
                xaxis_title='X',
                yaxis_title='Y',
                zaxis_title='Z'
            ),
            autosize=True,
            margin=dict(l=0, r=0, b=0, t=40)
        )
        
        # Guardar en historial
        init_historial()
        historial = session.get('historial', [])
        historial.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'tipo': 'Visualización 3D',
            'entrada': funcion_str,
            'resultado': {'x_range': x_range, 'y_range': y_range}
        })
        session['historial'] = historial
        
        return jsonify({
            'grafico': json.loads(fig.to_json()),
            'funcion': funcion_str
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# API: Analizar función
@app.route('/api/analizar_funcion', methods=['POST'])
def analizar_funcion():
    try:
        data = request.get_json()
        funcion_str = data.get('funcion')
        
        if not funcion_str:
            return jsonify({'error': 'No se proporcionó una función'}), 400
        
        funcion = sp.sympify(funcion_str)
        
        limites = {}
        try:
            lim_0 = sp.limit(sp.limit(funcion, x, 0), y, 0)
            limites['x→0, y→0'] = str(lim_0) if lim_0 != sp.nan else 'No existe'
        except:
            limites['x→0, y→0'] = 'No calculable'
        
        try:
            lim_inf = sp.limit(sp.limit(funcion, x, sp.oo), y, sp.oo)
            limites['x→∞, y→∞'] = str(lim_inf) if lim_inf != sp.nan else 'No existe'
        except:
            limites['x→∞, y→∞'] = 'No calculable'
        
        puntos_criticos = []
        try:
            dx = sp.diff(funcion, x)
            dy = sp.diff(funcion, y)
            soluciones = sp.solve([dx, dy], [x, y], dict=True)
            
            for sol in soluciones[:5]:  # Limitar a 5 puntos
                try:
                    px = complex(sol[x])
                    py = complex(sol[y])
                    if abs(px.imag) < 1e-10 and abs(py.imag) < 1e-10:
                        puntos_criticos.append({
                            'x': round(float(px.real), 4),
                            'y': round(float(py.real), 4)
                        })
                except:
                    continue
        except:
            pass
        
        dominio = 'ℝ²'
        rango = 'ℝ'
        
        # Intentar determinar restricciones de dominio
        if 'log' in funcion_str or 'ln' in funcion_str:
            dominio = 'ℝ² (con restricciones logarítmicas)'
        if 'sqrt' in funcion_str or '**(1/2)' in funcion_str:
            dominio = 'ℝ² (con restricciones de raíz)'
        if '/' in funcion_str:
            dominio = 'ℝ² (excepto donde el denominador es 0)'
        
        resultado = {
            'funcion': str(funcion),
            'dominio': dominio,
            'rango': rango,
            'limites': limites,
            'puntos_criticos': puntos_criticos
        }
        
        # Guardar en historial
        init_historial()
        historial = session.get('historial', [])
        historial.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'tipo': 'Análisis de Función',
            'entrada': funcion_str,
            'resultado': resultado
        })
        session['historial'] = historial
        
        return jsonify(resultado)
        
    except Exception as e:
        return jsonify({'error': f'Error al analizar la función: {str(e)}'}), 400

# API: Calcular derivadas parciales
@app.route('/api/calcular_derivadas', methods=['POST'])
def calcular_derivadas():
    try:
        data = request.get_json()
        funcion_str = data.get('funcion')
        punto = data.get('punto', None)
        
        funcion = sp.sympify(funcion_str)
        
        # Derivadas de primer orden
        dx = sp.diff(funcion, x)
        dy = sp.diff(funcion, y)
        
        # Derivadas de segundo orden
        dxx = sp.diff(dx, x)
        dyy = sp.diff(dy, y)
        dxy = sp.diff(dx, y)
        
        resultado = {
            'funcion': str(funcion),
            'derivadas': {
                'dx': str(dx),
                'dy': str(dy),
                'dxx': str(dxx),
                'dyy': str(dyy),
                'dxy': str(dxy)
            },
            'gradiente': {
                'x': str(dx),
                'y': str(dy)
            }
        }
        
        # Evaluar en punto si se proporciona
        if punto:
            px, py = punto
            resultado['punto'] = punto
            resultado['valores'] = {
                'dx': float(dx.subs([(x, px), (y, py)])),
                'dy': float(dy.subs([(x, px), (y, py)])),
                'grad_x': float(dx.subs([(x, px), (y, py)])),
                'grad_y': float(dy.subs([(x, px), (y, py)]))
            }
        
        # Guardar en historial
        init_historial()
        historial = session.get('historial', [])
        historial.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'tipo': 'Derivadas Parciales',
            'entrada': funcion_str,
            'resultado': resultado
        })
        session['historial'] = historial
        
        return jsonify(resultado)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# API: Limpiar historial
@app.route('/api/limpiar_historial', methods=['POST'])
def limpiar_historial():
    session['historial'] = []
    return jsonify({'success': True})

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
