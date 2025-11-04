from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import sympy as sp
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)
app.secret_key = 'tu_clave_secreta_aqui_cambiala_en_produccion'

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

# API: Graficar campo vectorial del gradiente
@app.route('/api/graficar_gradiente', methods=['POST'])
def graficar_gradiente():
    try:
        data = request.get_json()
        funcion_str = data.get('funcion')
        x_range = data.get('x_range', [-3, 3])
        y_range = data.get('y_range', [-3, 3])
        
        funcion = sp.sympify(funcion_str)
        
        # Calcular gradiente
        dx = sp.diff(funcion, x)
        dy = sp.diff(funcion, y)
        
        # Crear funciones numéricas
        f_dx = sp.lambdify((x, y), dx, 'numpy')
        f_dy = sp.lambdify((x, y), dy, 'numpy')
        f = sp.lambdify((x, y), funcion, 'numpy')
        
        # Crear malla para campo vectorial
        x_vals = np.linspace(x_range[0], x_range[1], 15)
        y_vals = np.linspace(y_range[0], y_range[1], 15)
        X, Y = np.meshgrid(x_vals, y_vals)
        
        U = f_dx(X, Y)
        V = f_dy(X, Y)
        
        # Crear malla más fina para contornos
        x_contour = np.linspace(x_range[0], x_range[1], 100)
        y_contour = np.linspace(y_range[0], y_range[1], 100)
        X_contour, Y_contour = np.meshgrid(x_contour, y_contour)
        Z_contour = f(X_contour, Y_contour)
        
        # Crear gráfico con contornos y vectores
        fig = go.Figure()
        
        # Agregar contornos de la función
        fig.add_trace(go.Contour(
            x=x_contour,
            y=y_contour,
            z=Z_contour,
            colorscale='Viridis',
            showscale=True,
            name='f(x,y)',
            contours=dict(
                coloring='heatmap',
                showlabels=True
            )
        ))
        
        # Agregar vectores del gradiente
        for i in range(len(x_vals)):
            for j in range(len(y_vals)):
                if np.isfinite(U[j, i]) and np.isfinite(V[j, i]):
                    # Normalizar vectores para visualización
                    mag = np.sqrt(U[j, i]**2 + V[j, i]**2)
                    if mag > 0:
                        scale = 0.3
                        fig.add_trace(go.Scatter(
                            x=[X[j, i], X[j, i] + scale * U[j, i] / mag],
                            y=[Y[j, i], Y[j, i] + scale * V[j, i] / mag],
                            mode='lines',
                            line=dict(color='white', width=2),
                            showlegend=False,
                            hoverinfo='skip'
                        ))
                        # Agregar punta de flecha
                        fig.add_trace(go.Scatter(
                            x=[X[j, i] + scale * U[j, i] / mag],
                            y=[Y[j, i] + scale * V[j, i] / mag],
                            mode='markers',
                            marker=dict(color='white', size=4, symbol='triangle-up'),
                            showlegend=False,
                            hoverinfo='skip'
                        ))
        
        fig.update_layout(
            title=f'Campo Vectorial del Gradiente: ∇f = ({dx}, {dy})',
            xaxis_title='X',
            yaxis_title='Y',
            autosize=True,
            margin=dict(l=0, r=0, b=0, t=40),
            hovermode='closest'
        )
        
        return jsonify({'grafico': json.loads(fig.to_json())})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# API: Optimización con Lagrange
@app.route('/api/optimizar_lagrange', methods=['POST'])
def optimizar_lagrange():
    try:
        data = request.get_json()
        funcion_str = data.get('funcion')
        restriccion_str = data.get('restriccion')
        tipo = data.get('tipo', 'max')
        
        funcion = sp.sympify(funcion_str)
        restriccion = sp.sympify(restriccion_str)
        
        # Multiplicador de Lagrange
        lam = sp.Symbol('lambda')
        
        # Sistema de ecuaciones
        L = funcion - lam * restriccion
        
        dL_dx = sp.diff(L, x)
        dL_dy = sp.diff(L, y)
        dL_dlam = sp.diff(L, lam)
        
        # Resolver sistema
        soluciones = sp.solve([dL_dx, dL_dy, restriccion], [x, y, lam])
        
        puntos_criticos = []
        for sol in soluciones:
            if len(sol) == 3 and all(s.is_real for s in sol):
                px, py, plam = float(sol[0]), float(sol[1]), float(sol[2])
                valor = float(funcion.subs([(x, px), (y, py)]))
                puntos_criticos.append({
                    'x': round(px, 4),
                    'y': round(py, 4),
                    'lambda': round(plam, 4),
                    'valor': round(valor, 4),
                    'tipo': 'Máximo' if tipo == 'max' else 'Mínimo'
                })
        
        # Encontrar solución óptima
        if puntos_criticos:
            if tipo == 'max':
                solucion_optima = max(puntos_criticos, key=lambda p: p['valor'])
            else:
                solucion_optima = min(puntos_criticos, key=lambda p: p['valor'])
        else:
            solucion_optima = None
        
        resultado = {
            'funcion': funcion_str,
            'restriccion': restriccion_str,
            'tipo': tipo,
            'puntos_criticos': puntos_criticos,
            'solucion_optima': solucion_optima
        }
        
        # Guardar en historial
        init_historial()
        historial = session.get('historial', [])
        historial.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'tipo': 'Optimización Lagrange',
            'entrada': f'{funcion_str} sujeto a {restriccion_str}',
            'resultado': resultado
        })
        session['historial'] = historial
        
        return jsonify(resultado)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# API: Graficar optimización con Lagrange
@app.route('/api/graficar_optimizacion', methods=['POST'])
def graficar_optimizacion():
    try:
        data = request.get_json()
        funcion_str = data.get('funcion')
        restriccion_str = data.get('restriccion')
        puntos_criticos = data.get('puntos_criticos', [])
        
        funcion = sp.sympify(funcion_str)
        restriccion = sp.sympify(restriccion_str)
        
        # Crear funciones numéricas
        f = sp.lambdify((x, y), funcion, 'numpy')
        g = sp.lambdify((x, y), restriccion, 'numpy')
        
        # Determinar rango basado en puntos críticos
        if puntos_criticos:
            x_vals = [p['x'] for p in puntos_criticos]
            y_vals = [p['y'] for p in puntos_criticos]
            x_range = [min(x_vals) - 2, max(x_vals) + 2]
            y_range = [min(y_vals) - 2, max(y_vals) + 2]
        else:
            x_range = [-5, 5]
            y_range = [-5, 5]
        
        # Crear malla
        x_mesh = np.linspace(x_range[0], x_range[1], 100)
        y_mesh = np.linspace(y_range[0], y_range[1], 100)
        X, Y = np.meshgrid(x_mesh, y_mesh)
        
        Z_f = f(X, Y)
        Z_g = g(X, Y)
        
        # Crear gráfico
        fig = go.Figure()
        
        # Contornos de la función objetivo
        fig.add_trace(go.Contour(
            x=x_mesh,
            y=y_mesh,
            z=Z_f,
            colorscale='Blues',
            showscale=True,
            name='f(x,y)',
            contours=dict(
                coloring='heatmap',
                showlabels=True
            ),
            colorbar=dict(title='f(x,y)', x=1.1)
        ))
        
        # Curva de restricción g(x,y) = 0
        fig.add_trace(go.Contour(
            x=x_mesh,
            y=y_mesh,
            z=Z_g,
            showscale=False,
            contours=dict(
                start=0,
                end=0,
                size=1,
                coloring='lines'
            ),
            line=dict(color='red', width=3),
            name='Restricción g(x,y)=0'
        ))
        
        # Marcar puntos críticos
        if puntos_criticos:
            for i, punto in enumerate(puntos_criticos):
                fig.add_trace(go.Scatter(
                    x=[punto['x']],
                    y=[punto['y']],
                    mode='markers+text',
                    marker=dict(color='yellow', size=12, symbol='star', line=dict(color='black', width=2)),
                    text=[f"P{i+1}"],
                    textposition='top center',
                    name=f"Punto crítico {i+1}",
                    hovertemplate=f"x: {punto['x']:.4f}<br>y: {punto['y']:.4f}<br>f: {punto.get('valor_funcion', 'N/A')}"
                ))
        
        fig.update_layout(
            title=f'Optimización: {funcion_str} sujeto a {restriccion_str} = 0',
            xaxis_title='X',
            yaxis_title='Y',
            autosize=True,
            margin=dict(l=0, r=0, b=0, t=40),
            hovermode='closest'
        )
        
        return jsonify({'grafico': json.loads(fig.to_json())})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# API: Calcular integral doble
@app.route('/api/calcular_integral_doble', methods=['POST'])
def calcular_integral_doble():
    try:
        data = request.get_json()
        funcion_str = data.get('funcion')
        limites = data.get('limites')  # [[x_min, x_max], [y_min, y_max]]
        
        funcion = sp.sympify(funcion_str)
        
        # Calcular integral doble
        integral = sp.integrate(funcion, 
                               (x, limites[0][0], limites[0][1]),
                               (y, limites[1][0], limites[1][1]))
        
        resultado_num = float(integral.evalf())
        
        resultado = {
            'funcion': funcion_str,
            'limites': limites,
            'resultado': round(resultado_num, 6),
            'interpretacion': f'El volumen bajo la superficie es {round(resultado_num, 6)} unidades cúbicas'
        }
        
        # Guardar en historial
        init_historial()
        historial = session.get('historial', [])
        historial.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'tipo': 'Integral Doble',
            'entrada': funcion_str,
            'resultado': resultado
        })
        session['historial'] = historial
        
        return jsonify(resultado)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# API: Calcular integral triple
@app.route('/api/calcular_integral_triple', methods=['POST'])
def calcular_integral_triple():
    try:
        data = request.get_json()
        funcion_str = data.get('funcion')
        limites = data.get('limites')  # [[x_min, x_max], [y_min, y_max], [z_min, z_max]]
        
        funcion = sp.sympify(funcion_str)
        
        # Calcular integral triple
        integral = sp.integrate(funcion,
                               (x, limites[0][0], limites[0][1]),
                               (y, limites[1][0], limites[1][1]),
                               (z, limites[2][0], limites[2][1]))
        
        resultado_num = float(integral.evalf())
        
        resultado = {
            'funcion': funcion_str,
            'limites': limites,
            'resultado': round(resultado_num, 6),
            'interpretacion': f'El valor de la integral triple es {round(resultado_num, 6)}'
        }
        
        # Guardar en historial
        init_historial()
        historial = session.get('historial', [])
        historial.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'tipo': 'Integral Triple',
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

# API: Visualizar región de integración
@app.route('/api/graficar_region_integracion', methods=['POST'])
def graficar_region_integracion():
    try:
        data = request.get_json()
        funcion_str = data.get('funcion')
        limites = data.get('limites')
        tipo = data.get('tipo', 'doble')
        
        funcion = sp.sympify(funcion_str)
        
        if tipo == 'doble':
            # Integral doble: mostrar superficie 3D
            f = sp.lambdify((x, y), funcion, 'numpy')
            
            x_range = limites[0]
            y_range = limites[1]
            
            x_vals = np.linspace(x_range[0], x_range[1], 50)
            y_vals = np.linspace(y_range[0], y_range[1], 50)
            X, Y = np.meshgrid(x_vals, y_vals)
            Z = f(X, Y)
            
            fig = go.Figure()
            
            # Superficie de la función
            fig.add_trace(go.Surface(
                x=X,
                y=Y,
                z=Z,
                colorscale='Viridis',
                name='f(x,y)',
                showscale=True
            ))
            
            # Plano z=0
            fig.add_trace(go.Surface(
                x=X,
                y=Y,
                z=np.zeros_like(Z),
                colorscale=[[0, 'rgba(200,200,200,0.3)'], [1, 'rgba(200,200,200,0.3)']],
                showscale=False,
                name='Región de integración'
            ))
            
            fig.update_layout(
                title=f'Región de Integración Doble: ∫∫ {funcion_str} dA',
                scene=dict(
                    xaxis_title='X',
                    yaxis_title='Y',
                    zaxis_title='Z',
                    xaxis=dict(range=[x_range[0], x_range[1]]),
                    yaxis=dict(range=[y_range[0], y_range[1]])
                ),
                autosize=True,
                margin=dict(l=0, r=0, b=0, t=40)
            )
            
        else:
            # Integral triple: mostrar caja 3D
            x_range = limites[0]
            y_range = limites[1]
            z_range = limites[2]
            
            # Crear vértices de la caja
            vertices = [
                [x_range[0], y_range[0], z_range[0]],
                [x_range[1], y_range[0], z_range[0]],
                [x_range[1], y_range[1], z_range[0]],
                [x_range[0], y_range[1], z_range[0]],
                [x_range[0], y_range[0], z_range[1]],
                [x_range[1], y_range[0], z_range[1]],
                [x_range[1], y_range[1], z_range[1]],
                [x_range[0], y_range[1], z_range[1]]
            ]
            
            # Crear aristas de la caja
            edges = [
                [0, 1], [1, 2], [2, 3], [3, 0],  # Base inferior
                [4, 5], [5, 6], [6, 7], [7, 4],  # Base superior
                [0, 4], [1, 5], [2, 6], [3, 7]   # Aristas verticales
            ]
            
            fig = go.Figure()
            
            # Dibujar aristas
            for edge in edges:
                v1, v2 = vertices[edge[0]], vertices[edge[1]]
                fig.add_trace(go.Scatter3d(
                    x=[v1[0], v2[0]],
                    y=[v1[1], v2[1]],
                    z=[v1[2], v2[2]],
                    mode='lines',
                    line=dict(color='blue', width=4),
                    showlegend=False
                ))
            
            # Agregar vértices
            fig.add_trace(go.Scatter3d(
                x=[v[0] for v in vertices],
                y=[v[1] for v in vertices],
                z=[v[2] for v in vertices],
                mode='markers',
                marker=dict(color='red', size=6),
                name='Vértices',
                showlegend=False
            ))
            
            fig.update_layout(
                title=f'Región de Integración Triple: ∫∫∫ {funcion_str} dV',
                scene=dict(
                    xaxis_title='X',
                    yaxis_title='Y',
                    zaxis_title='Z',
                    xaxis=dict(range=[x_range[0] - 1, x_range[1] + 1]),
                    yaxis=dict(range=[y_range[0] - 1, y_range[1] + 1]),
                    zaxis=dict(range=[z_range[0] - 1, z_range[1] + 1])
                ),
                autosize=True,
                margin=dict(l=0, r=0, b=0, t=40)
            )
        
        return jsonify({'grafico': json.loads(fig.to_json())})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
