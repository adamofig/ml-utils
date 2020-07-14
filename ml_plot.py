
import plotly.graph_objects as go

def plot_time_comparing(df, date, target, pred_target):

  try:
    fig = go.Figure()
  except Exception as e:
    print("No pudo iniciar la gráfica probablemente no esta importada la biblioteca import plotly.graph_objects as go")
    return None
  fig.add_trace(go.Scatter(x=df[date], y=df[target], mode='lines+markers', name=target, opacity=.8, line=dict(color='#FD6F30', width=3)))

  fig.add_trace(go.Scatter(x=df[date], y=df[pred_target], mode='lines', name=pred_target, opacity=.9, line=dict(color='#1F3F79') ))

  fig.update_layout( 
      title = 'Predicciones de siniestros a nivel Nacional',
      xaxis=dict( showline=True, showgrid=False, showticklabels=True, linecolor='lightgrey', linewidth=2, ticks='outside'),
      yaxis=dict(showgrid=True, zeroline=True, showline=True, showticklabels=True, linecolor='lightgrey'),
      plot_bgcolor='white')

  # Agrega un cuadro gris para saber donde es la zona de foco
  # fig.update0_layout(shapes=[dict(type="rect", xref="x", yref="paper", x0='2020-2-28', x1='2020-3-11', y0=0,  y1=1, fillcolor="lightgray", opacity=0.3, layer="below", line_width=.5)])

  fig.update_layout( 
      title = 'Siniestros generales nacional',
      xaxis=dict( title="Fecha", showline=True, showgrid=False, showticklabels=True, linecolor='lightgrey', linewidth=2, ticks='outside'),
      yaxis=dict(title="Número de siniestros", ticks="outside", showgrid=True, zeroline=True, showline=True, showticklabels=True, linecolor='lightgrey'),
      plot_bgcolor='white',
      )
  return fig


def plot_ml_results(eval_results):
  """Gráfica los resultados de una evaluación de modelo  
    
    Keyword Arguments:
        eval_results {dict} -- Diccionario de resultados de evualuación 
    
    Ejemplo
    ------
    {'accurate_percent': 0.05394190871369295,
    'acp_percent': 0.0,
    'mae': 46.6370622406639,
    'mae_percent': 0.7551867219917012,
    'mse': 9534.3077593361,
    'r2': 0.9668950199803521,
    'rmse': 97.64377993162749,
    'rsme_percent': 0.8506224066390041
    'total_records':190}
  """
  x_data = [eval_results["rmse_percent"], eval_results["mae_percent"] , eval_results["accurate_percent"], eval_results["acp_percent"] ]
  y_data = ["rsme" , "mae", "accurate", "acp"]

  accurate = round(eval_results["r2"] * 100, 1)
  mae = round(eval_results["mae"], 1)
  rmse = round(eval_results["rmse"], 1)
  rmse_percent = round(eval_results["rmse_percent"]*100, 1)
  accurate_percent = round(eval_results["accurate_percent"]*100, 1)
  mae_percent = round(eval_results["mae_percent"]*100, 1)
  total = eval_results["total_records"]


  fig = go.Figure()

  fig.add_trace(go.Bar(x=x_data,y=y_data, name='Predictions', marker_color='rgb(55, 83, 109)', orientation='h'))

  fig.update_layout( 
      title = f'Resultados del entrenamiento ({total} registros evaluados)',
      #xaxis=dict( title="Hora", showline=True, showgrid=False, showticklabels=True, linecolor='lightgrey', linewidth=2, ticks='outside'),
      #yaxis=dict(title="Número de siniestros", showgrid=True, zeroline=True, showline=True, showticklabels=True, linecolor='lightgrey'),
      plot_bgcolor='white',
      xaxis_tickformat = '%',
      yaxis=dict( title='Metricas de error', titlefont_size=16, tickfont_size=14),
      xaxis= dict(tickvals=[0,.2,.4,.6,.8,1])
    
      )
  

  fig.add_annotation(text=f" Precisión del modelo <b style='color:#cc6600'>{accurate}%</b>", font_size=20, showarrow=False, x=.3,y=4, ay=-160 )
  fig.add_annotation(text=f"Errores MAE: <b style='color:#cc6600'>{mae}</b> RSME: <b style='color:#cc6600'>{rmse}</b>", font_size=20, showarrow=False, x=.7,y=4, ay=-160 )

  #fig.add_annotation(text="Rango de predicciones: 1.06 - 1170", font_size=20, showarrow=False, x=.5, y=3, arrowhead=7)

  fig.add_annotation(text=f"<b>{accurate_percent}%</b> tienen predicción exacta", font_size=20, showarrow=True, x=eval_results["accurate_percent"], y=2, ax=250, arrowhead=7)
  fig.add_annotation(text=f"<b>{mae_percent}%</b> presentan desviación por debajo de <b>{mae}</b>", font_size=20, showarrow=True, x=eval_results["mae_percent"], y=1,  ax=270, arrowhead=7)
  fig.add_annotation(text=f"<b>{rmse_percent}%</b> con error en menos de <b>{rmse}</b>", font_size=20, showarrow=True, x=eval_results["rmse_percent"], y=0,  ax=250, arrowhead=7)

  return fig