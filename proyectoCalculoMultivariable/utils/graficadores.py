import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from sympy import symbols, sympify, lambdify
import json

def graficar_superficie_3d(funcion_str, x_range=[-5, 5], y_range=[-5, 5], puntos=50):
    """
    Genera gráfico 3D interactivo de una superficie
    """
    try:
        x, y = symbols('x y')
        funcion = sympify(funcion_str)
        f_lambda = lambdify((x, y), funcion, 'numpy')
        
        # Crear malla de puntos
        x_vals = np.linspace(x_range[0], x_range[1], puntos)
        y_vals = np.linspace(y_range[0], y_range[1], puntos)
        X, Y = np.meshgrid(x_vals, y_vals)
        
        # Evaluar función
        Z = f_lambda(X, Y)
        
        # Manejar valores infinitos
        Z = np.where(np.isfinite(Z), Z, np.nan)
        
        # Crear gráfico
        fig = go.Figure(data=[go.Surface(
            x=X,
            y=Y,
            z=Z,
            colorscale='Viridis',
            name='f(x,y)'
        )])
        
        fig.update_layout(
            title=f'Superficie: f(x,y) = {funcion_str}',
            scene=dict(
                xaxis_title='X',
                yaxis_title='Y',
                zaxis_title='Z',
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.3)
                )
            ),
            autosize=True,
            margin=dict(l=0, r=0, b=0, t=40),
            height=600
        )
        
        return json.loads(fig.to_json())
    
    except Exception as e:
        raise Exception(f'Error al graficar superficie: {str(e)}')

def graficar_campo_gradiente(funcion_str, x_range=[-5, 5], y_range=[-5, 5], puntos=20):
    """
    Genera gráfico del campo vectorial del gradiente
    """
    try:
        from sympy import diff
        
        x, y = symbols('x y')
        funcion = sympify(funcion_str)
        
        # Calcular gradiente
        df_dx = diff(funcion, x)
        df_dy = diff(funcion, y)
        
        # Lambdify
        fx_lambda = lambdify((x, y), df_dx, 'numpy')
        fy_lambda = lambdify((x, y), df_dy, 'numpy')
        f_lambda = lambdify((x, y), funcion, 'numpy')
        
        # Crear malla
        x_vals = np.linspace(x_range[0], x_range[1], puntos)
        y_vals = np.linspace(y_range[0], y_range[1], puntos)
        X, Y = np.meshgrid(x_vals, y_vals)
        
        # Evaluar gradiente
        U = fx_lambda(X, Y)
        V = fy_lambda(X, Y)
        Z = f_lambda(X, Y)
        
        # Normalizar vectores para visualización
        magnitud = np.sqrt(U**2 + V**2)
        magnitud = np.where(magnitud == 0, 1, magnitud)
        U_norm = U / magnitud
        V_norm = V / magnitud
        
        # Crear figura con contornos y vectores
        fig = go.Figure()
        
        # Agregar contornos
        fig.add_trace(go.Contour(
            x=x_vals,
            y=y_vals,
            z=Z,
            colorscale='Viridis',
            name='f(x,y)',
            contours=dict(
                coloring='heatmap',
                showlabels=True
            )
        ))
        
        # Agregar vectores del gradiente
        for i in range(0, len(x_vals), 2):
            for j in range(0, len(y_vals), 2):
                fig.add_trace(go.Scatter(
                    x=[X[j, i], X[j, i] + U_norm[j, i] * 0.3],
                    y=[Y[j, i], Y[j, i] + V_norm[j, i] * 0.3],
                    mode='lines',
                    line=dict(color='white', width=2),
                    showlegend=False,
                    hoverinfo='skip'
                ))
                
                # Agregar punta de flecha
                fig.add_trace(go.Scatter(
                    x=[X[j, i] + U_norm[j, i] * 0.3],
                    y=[Y[j, i] + V_norm[j, i] * 0.3],
                    mode='markers',
                    marker=dict(
                        symbol='arrow',
                        size=10,
                        color='white',
                        angleref='previous'
                    ),
                    showlegend=False,
                    hoverinfo='skip'
                ))
        
        fig.update_layout(
            title=f'Campo Gradiente: ∇f(x,y)',
            xaxis_title='X',
            yaxis_title='Y',
            autosize=True,
            height=600,
            margin=dict(l=0, r=0, b=0, t=40)
        )
        
        return json.loads(fig.to_json())
    
    except Exception as e:
        raise Exception(f'Error al graficar gradiente: {str(e)}')

def graficar_region_integracion(limites, tipo='doble'):
    """
    Grafica la región de integración
    """
    try:
        if tipo == 'doble':
            x_lim = limites[0]
            y_lim = limites[1]
            
            # Crear rectángulo
            x_rect = [x_lim[0], x_lim[1], x_lim[1], x_lim[0], x_lim[0]]
            y_rect = [y_lim[0], y_lim[0], y_lim[1], y_lim[1], y_lim[0]]
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=x_rect,
                y=y_rect,
                fill='toself',
                fillcolor='rgba(0, 100, 200, 0.3)',
                line=dict(color='blue', width=2),
                name='Región de integración'
            ))
            
            fig.update_layout(
                title='Región de Integración',
                xaxis_title='X',
                yaxis_title='Y',
                autosize=True,
                height=500,
                margin=dict(l=0, r=0, b=0, t=40),
                showlegend=True
            )
            
            return json.loads(fig.to_json())
        
        else:  # triple
            # Para integrales triples, mostrar un cubo 3D
            x_lim = limites[0]
            y_lim = limites[1]
            z_lim = limites[2]
            
            # Crear vértices del cubo
            vertices = [
                [x_lim[0], y_lim[0], z_lim[0]],
                [x_lim[1], y_lim[0], z_lim[0]],
                [x_lim[1], y_lim[1], z_lim[0]],
                [x_lim[0], y_lim[1], z_lim[0]],
                [x_lim[0], y_lim[0], z_lim[1]],
                [x_lim[1], y_lim[0], z_lim[1]],
                [x_lim[1], y_lim[1], z_lim[1]],
                [x_lim[0], y_lim[1], z_lim[1]]
            ]
            
            # Crear aristas del cubo
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
            
            fig.update_layout(
                title='Región de Integración (3D)',
                scene=dict(
                    xaxis_title='X',
                    yaxis_title='Y',
                    zaxis_title='Z'
                ),
                autosize=True,
                height=600,
                margin=dict(l=0, r=0, b=0, t=40)
            )
            
            return json.loads(fig.to_json())
    
    except Exception as e:
        raise Exception(f'Error al graficar región: {str(e)}')