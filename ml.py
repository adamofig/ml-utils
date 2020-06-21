
### Clases 

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, make_scorer, accuracy_score
import numpy as np

import pandas as pd   

from typing import List, Dict

# Requiere las siguientes bibliotecas
# from sklearn.base import BaseEstimator, TransformerMixin
# from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler

# @title Clase para convertir todos los datasets.
# Requiere las siguientes bibliotecas
# from sklearn.base import BaseEstimator, TransformerMixin
# from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
  
class UniversalTransformerEncoder(BaseEstimator, TransformerMixin):
    """Hiperparamétros de la clase transformación 

        Args:
        --------
        show_logs (bool, optional): True para mostrar los logs del tranformador. Defaults to False.
        remove_columns (bool, optional): Variable booleana para eliminar las columnas pasadas ya que representan textos en vez de números. Defaults to True.
        encode_label (bool, optional): Para codificar las columnas a ordinal econder. Defaults to False.
        drop_nan (bool, optional): Elimina los nulos, si esto es false entonces imputa a más frecuente. Defaults to True.
        order_columns (bool, optional): regresa los resultados ordenados por las columnas. Defaults to False.
        catalogs_dict ([type], optional):  Dicionario con los valores posibles de cada columns_1hot, debe estar en orden la clave es la posición de columns_1hot ejemplo-> { 0:  ['Colision', 'Cristales', 'Robo', 'Responsabilidad Civil']} si esta variable no es proporcionada se tomará de las etiquitas encontradas en cada columna, es util cuando se quiere transformar solo un registro, . Defaults to None.
        standarize (bool, optional): Normaliza los resultados. Defaults to False.
    """
  
    
    def __init__(self, show_logs = False, remove_columns = True,  encode_label = False, drop_nan=True, order_columns=False, catalogs_dict=None, standarize=False): 
      self.show_logs = show_logs
      self.remove_columns = remove_columns
      self.encode_label = encode_label
      self.drop_nan = drop_nan
      self.order_columns = order_columns
      self.catalogs_dict = catalogs_dict
      self.standarize = standarize


    def fit(self, X, y=None):
      return self  # nothing else to do

    def impute(self, df_X, labels ):
      # Imputando datos faltantes
      df_to_impute = df_X[labels]

      imputer = SimpleImputer(strategy='most_frequent', missing_values=None)
      array_imputed = imputer.fit_transform(df_to_impute)
      df_imputed = pd.DataFrame(array_imputed, columns=labels)
      
      df_X[labels] = df_imputed[labels]
      return df_X

    def log(self, *args):
      if self.show_logs is True:
        print(*args)


    def transform(self, X, columns_1hot, skip_normalization=[]):
      """Método final para tranformar cualquier dataframe,
      
      Arguments:
          X {[type]} -- [description]
          columns_1hot {[List]} -- Lista de columnas para codificar a onehotEncoding 
      
      """

      self.log("Iniciando el tranformador")
      
      if self.drop_nan:
        num_after = X.shape[0]
        X = X.dropna(subset=columns_1hot) 
        X = X.reset_index(drop=True)
        self.log("Se Eliminarion {} registros nulos".format(num_after-X.shape[0]))
      else:
        X = self.impute(X, columns_1hot)

      df_columns_1Hot = X[columns_1hot]

      if(self.encode_label):
        self.log("Creando codificacion ordinal de ", columns_1hot)
        ordinal_encoder = OrdinalEncoder()
        encoders = ordinal_encoder.fit_transform(X[columns_1hot])
        ordinal_columns = [ column + "_ordinal" for column in columns_1hot]


        df_ordinal = pd.DataFrame(encoders, columns=ordinal_columns)
        
        X = pd.concat([X, df_ordinal], axis=1)

      # Transformando con one hot encoder. 
      # por defualt OneHotEncoder nos regresa una matriz esparcida, con toarray() la hago normal, y puedo obtener las categorias desde cat_encoder.categories_
      # La matriz comprimida es más rápida pero aun no aprendemos a usarla, sparse=False para tener el arreglo, 
      categories = self.catalogs_dict if self.catalogs_dict is not None else 'auto'

      cat_encoder = OneHotEncoder(sparse=False, categories=categories)
      labels_cat_1hot = cat_encoder.fit_transform(df_columns_1Hot)
      
      flat_columns_names = [item for sublist in cat_encoder.categories_ for item in sublist]

      labels_df_1hot_encoder = pd.DataFrame(labels_cat_1hot, columns=flat_columns_names)

      df_transformed = pd.concat([X, labels_df_1hot_encoder], axis=1)

      if(self.remove_columns):
        self.log("Eliminando las columnas", columns_1hot)
        df_transformed = df_transformed.drop(columns_1hot, axis=1)


      if self.standarize:
        columns_numeric = df_transformed.select_dtypes('number').columns.tolist()
        if skip_normalization:
          self.log("Omitiendo la normalización de", set(skip_normalization))
          columns_numeric = list( set(columns_numeric) - set(skip_normalization) )
        scaler = StandardScaler()
        df_transformed[columns_numeric] = scaler.fit_transform(df_transformed[columns_numeric])
        
      if self.order_columns:
        self.log("Ordenando columnas alfabeticamente")
        df_transformed = df_transformed.reindex(sorted(df_transformed.columns), axis=1)

      return df_transformed


def eval_pred_results(y_real,y_pred) ->(str, str):
  mae = mean_absolute_error(y_real, y_pred)
  mse = mean_squared_error(y_real, y_pred)
  rmse = np.sqrt(mse)
  r2 = r2_score(y_real, y_pred)

  df_score = pd.DataFrame()
  df_score["real"] = y_real
  df_score["predicted"] = y_pred
  df_score["error"] = y_real - y_pred
  df_score["error_abs"] = abs(df_score["error"])

  df_score["pass_mae"] = df_score["error_abs"] <= mae
  df_score["pass_rsme"] = df_score["error_abs"] <= rmse
  df_score["pass_accurate"] = df_score["real"] == round(df_score["predicted"])

  pass_mae_dict = df_score.pass_mae.value_counts().to_dict()
  pass_rsme_dict = df_score.pass_rsme.value_counts().to_dict()
  pass_accurate_dict = df_score.pass_accurate.value_counts().to_dict()

  mae_percent = pass_mae_dict[True] / (pass_mae_dict[True] + pass_mae_dict[False])
  rsme_percent = pass_rsme_dict[True] / (pass_rsme_dict[True] + pass_rsme_dict[False])
  accurate_percent = pass_accurate_dict[True] / (pass_accurate_dict[True] + pass_accurate_dict[False])

  stac_desc = df_score.describe()
  min_value_pred = stac_desc.loc[["min"],["predicted"]].values[0][0]
  max_value_pred = stac_desc.loc[["max"],["predicted"]].values[0][0]
  # Se calcula el criterio de aceptación proporcional 
  df_score["porcentage_proportional"] = df_score["predicted"] / max_value_pred
  df_score["a_criteria_proportional"] = .5 * rmse + 2.5 * rmse * df_score["porcentage_proportional"]

  df_score["pass_acp"] = df_score["error_abs"] <= df_score["porcentage_proportional"]
  pass_acp_dict = df_score.pass_acp.value_counts().to_dict()
  acp_percent = pass_acp_dict[True] / (pass_acp_dict[True] + pass_acp_dict[False])

  print(f"\nError Absoluto Medio: '{mae}' ")
  print(f"Error Cuadrático medio: '{mse}''")
  print(f"Raiz Error Cuadrático medio: '{rmse}'")

  print(f"Valores predichos, Min: {min_value_pred}, Max: {max_value_pred}")
  print(f"\Porcentaje de Aceptacion Proporcional:   {round(acp_percent* 100,2)}%")
  print(f"Porcentaje por debajo de Error Cuadratico Medio:   {round(rsme_percent* 100,2)}%")
  print(f"Porcentaje por debajo con Error Absoluto Medio:     {round(mae_percent* 100,2)}%")
  print(f"Porcentaje Con error 0 :                       {round(accurate_percent* 100,2)}%")
  print(f"* {pass_mae_dict[True]} registros satifacen el error  absoluto representa el {round(mae_percent * 100,2)}%")
  print(f"* {pass_rsme_dict[True]} registros satifacen el error  cuadratico medio representa el {round(rsme_percent * 100,2)}%")
  print(f"Presición Coef Determinación (Mejora de varación respecto a media): '{r2}'")
  dict_results = {"min_value_pred":min_value_pred, "max_value_pred":max_value_pred,  "mae":mae, "mae_percent":mae_percent, "mse":mse, "rmse":rmse , "rsme_percent":rsme_percent,  "acp_percent": acp_percent , "accurate_percent":accurate_percent , "r2":r2  }
  return dict_results, df_score
