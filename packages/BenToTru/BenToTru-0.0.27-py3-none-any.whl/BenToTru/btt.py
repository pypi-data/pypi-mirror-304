import pandas as pd
import numpy as np

from iotbr import tru as tru

from importlib import resources
import io

'-------------------------------------------------------------------------------'
'''
N: númedo de setores TRU                  (51 ou 68)
J: número de produtos TRU                 (107 ou 128)

gas: tipo do gas: CO2, CH4, N20, 
                  NOx, CO ou SO2          (1,)

household: considerar famílias 
           na análise                     (True of False)

reference_year: ano de referência 
                para correção monetária   ('yyyy')

u: unidade de tempo                       (t ou t1)

tru_CI: dados de consumo intermediário    (N , J )
tru_CI_energy: dados de CI de 
               bens energéticos           (N , 17)

ben: balanco energetico nacional          (20, 27)
ben_reduced: balanco energetico nacional  (20, 17)
coef1: coeficientes de distribuição       (N , 17)
emission_ben: emissões do ben             (14, 17)
emission_tru: emissões                    (N , 17)
emission_tru_adjusted: emissões ajustadas (N , 17)

ben_to_tru_products: dicionário entre produtos BEN e TRU
ben_to_tru_sectors: dicionário entre setores BEN e TRU

verification:(setores ben , produtos ben) (12, 17)
'''

'-------------------------------------------------------------------------------'

# 1) importar os coeficientes que convertem os dados tep para ghg
# Os dados originais estão disponíveis no seguinte link:
# coef_tep_to_ghg = pd.read_csv(
#     r'https://raw.githubusercontent.com/fms-1988/datas/main/'
#     r'coeficientes_emissoes_gee_ajustado.csv')

with resources.open_binary(
    'BenToTru.data', 'coeficientes_emissoes_gee_ajustado.csv'
) as f:
    data_ = f.read()
    bytes_io = io.BytesIO(data_)  
coef_tep_to_ghg = pd.read_csv(bytes_io)
 

# Não existe coeficiente de emissões para o produto "ELETRICIDADE". 
# Então eu considerei os mesmos coeficientes do produto "GÁS DE CIDADE E DE COQUERIA". 
# O ideal é excluir esse bem da análise.

coef_tep_to_ghg = coef_tep_to_ghg.iloc[:, [
    0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 13, 15, 16, 17, 18]]

'-------------------------------------------------------------------------------'
# 2) criarfunções para manipular os dados 

# 2.1) os dados das tabelas tru51 e tru68 devem ser reorganizados para coincidirem 
#  com os demais dados. Apenas algumas linhas precisam ser realicadas. 
def reorder_df(df_,N):
  if N == '51':
    #ordem correta das linhas para tru51
    ar1 = [ 0,  1,  2,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15,  3,  4, 16, 17,\
           18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,\
            5, 35, 36, 47, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 48, 49, 50]
  else:
    #ordem correta das linhas para tru68
    ar1 = [ 0,  1,  2,  3,  4,  8,  9, 10, 11, 12, 13, 14, 30, 15, 16, 17, 31,\
           18,  5,  6, 32, 33, 34, 19, 20, 35, 36, 37, 38, 21, 22, 23, 24, 25,\
            26, 27, 28,  7, 39, 29, 43, 44, 65, 66, 67, 45, 46, 47, 48, 49, 50,\
            51, 52, 53, 54, 55, 56, 57, 58, 59, 40, 41, 60, 42, 61, 62, 63, 64]
  return df_.iloc[ar1,:]

# 2.2) criar mapa entre os setores (ben) e os setores (tru)
def map_ben_to_tru(N,matrix,sector_ben_index=1,product_ben_index=1):
  '''
  sector_ben = setores ben
  sectors_tru = setores tru
  sector_ben_idx = setores ben indexados
  '''
  ben_to_tru_sectors = import_dictionaries(N)[1]
  sector_ben = ben_to_tru_sectors['ben'].unique()[sector_ben_index]
  sectors_tru = ben_to_tru_sectors[
    ben_to_tru_sectors['ben'] == sector_ben][str('setor_tru'+N)]
  product_ben = matrix.columns[product_ben_index]
  sector_ben_idx  = pd.DataFrame(matrix.iloc[sectors_tru-1,product_ben_index])
  return sector_ben_idx, sector_ben, product_ben


def import_dictionaries(L='51'):
  if L == '51':
    dict_products = 'correspondencia_produtos_TRU51_BEN.csv'
    dict_sectors = 'correspondencia_MIP56_TRU51_BEN.csv'
    column = str('produto_TRU'+L)
  else:
    dict_products = 'correspondencia_produtos_TRU68_BEN.csv' #
    dict_sectors = 'correspondencia_TRU68_BEN.csv'
    column = str('produto_TRU'+L)
  #ben_to_tru_products
  #ben_to_tru_products = pd.read_csv(str('https://raw.githubusercontent.com/fms-1988/datas/main/'+dict_products))
  with resources.open_binary('BenToTru.data', dict_products) as f:
    data_ = f.read()
    bytes_io = io.BytesIO(data_)
  ben_to_tru_products = pd.read_csv(bytes_io)
  ben_to_tru_products = ben_to_tru_products[ben_to_tru_products[column] != 'nc'].reset_index(drop=True)

  #ben_to_tru_sectors
  #ben_to_tru_sectors = pd.read_csv(str('https://raw.githubusercontent.com/fms-1988/datas/main/'+dict_sectors))
  with resources.open_binary('BenToTru.data', dict_sectors) as f:
    data_ = f.read()
    bytes_io = io.BytesIO(data_)
  ben_to_tru_sectors = pd.read_csv(bytes_io)
  return ben_to_tru_products, ben_to_tru_sectors




def import_data_ben(year='2017', N='51'):
  ben_to_tru_products = import_dictionaries(N)[0]
  #import and adjust matrix ben to 22 sectors
  #ben = pd.read_excel('https://github.com/fms-1988/datas/raw/main/Matrizes%20Consolidadas%20(em%20tep)%201970%20-%202022.xls', sheet_name=self.Y)
  with resources.open_binary('BenToTru.data','Matrizes Consolidadas (em tep) 1970 - 2022.xls') as f:
    data = f.read()
    bytes_io = io.BytesIO(data)
  ben = pd.read_excel(bytes_io, sheet_name=year)
  ben = ben.iloc[:, 1:]
  ben = ben.iloc[[11] + [33] + list(range(35, 40)) + list(range(41, 45)) + list(range(46, 58))]
  ben = ben.set_axis(ben.iloc[0], axis=1)
  ben = ben[1:].reset_index(drop=True)
  ben = ben.set_axis(ben.iloc[:,0], axis=0)
  ben = ben.iloc[:,1:-1]
  ben.rename_axis(index='setor', columns='produto', inplace=True)
  ben.columns = ben.columns.str.strip()
  ben.index = ben.index.str.strip()
  ben.columns = ben.columns.str.replace('ÓLEO COMBUSTIVEL', 'ÓLEO COMBUSTÍVEL') #before 2004 this name was writteng wrong
  ben.columns = ben.columns.str.replace('GÁS DE COQUERIA','GÁS DE CIDADE E DE COQUERIA') #this name was written wrong in 2004
  ben = ben.drop(['CONSUMO FINAL NÃO-ENERGÉTICO', 'CONSUMO NÃO-IDENTIFICADO']) #Consider only the sectors that have been identified as generating emissions.

  #In 2005, Ben began reporting the product 'BIODIESEL'. This changed the column order of the products.
  if int(year) >= 2005:
    ben_reduced = ben.iloc[:,ben_to_tru_products['produto_BEN_num_after_2004'].astype(float)] #ben products that generate emissions
  else:
    ben_reduced = ben.iloc[:,ben_to_tru_products['produto_BEN_num_before_2005'].astype(float)] #ben products that generate emissions
  return ben, ben_reduced



def import_data_tru(year = '2017', N = '51', unity = 't', reference_year='2017',household=False):
  #import values of intermediate consumption by economic sector (TRU51)
  #tru51 is updated untill 2020 and ben is updated untill 2023
  #if tru51 is not updated, than use the last value available (2020)
  # reference_year: reference year to deflation ('yyyy') 
  try:
    tru_CI = tru.read_var_def(year,N,'CI_matrix',unity,reference_year).T
  except Exception as e:
    #print(e)
    tru_CI = tru.read_var_def('2020',N,'CI_matrix',unity,reference_year).T
  ben_to_tru_products = import_dictionaries(N)[0]
  tru_CI_energy = tru_CI.iloc[:,ben_to_tru_products[str('produto_TRU'+N+'_num')].values]
  return tru_CI, tru_CI_energy

def exact_estimation_false(year = '2017', N = '51', unity = 't', reference_year='2017',gas='CO2',household=False):
  print("This function is deprecated and will be removed in future versions.")
  coef1 = pd.DataFrame() #coefficint of distribution (value to tep)
  coef2 = pd.DataFrame() #coefficient of emission (tep to ghg)
  tep = pd.DataFrame()
  emission_tru = pd.DataFrame()

  ben_to_tru = import_dictionaries(N)
  ben_to_tru_sectors = ben_to_tru[1]
  ben_to_tru_products = ben_to_tru[0]
  ben_ = ben_to_tru_sectors['ben'].unique() #sector ben (j)
  num_sectors = len(ben_)

  data_ben = import_data_ben(year, N)
  ben_reduced = data_ben[1]

  for j in range(num_sectors):
    #corespondent rows of tru matrix to sector (j)
    tru_j_num = ben_to_tru_sectors[ben_to_tru_sectors['ben'] == ben_[j]][str('setor_tru'+N)]

    #estimate coeficient of distribution
    data_tru = import_data_tru(year, N, unity, reference_year)
    tru_CI_energy = data_tru[1]
    tru_j = tru_CI_energy.iloc[tru_j_num-1,:]
    X_j = pd.DataFrame(tru_j.sum(axis=0))
    diag_X_j = np.diag(X_j[0].values)
    diag_X_j = diag_X_j.astype(float)
    inv_diag_X_j = np.linalg.pinv(diag_X_j)
    coef1_j = tru_j.values @ inv_diag_X_j
    coef1_j = pd.DataFrame(coef1_j, columns=ben_reduced.columns, index= tru_j.index)


    #adjust columns without coeficients of distribution
    total = coef1_j.sum().sum()
    totals = coef1_j.sum(axis=1)
    mean = totals / total
    for col in coef1_j.columns:
      if coef1_j[col].eq(0).all():
        coef1_j[col] = mean

    coef1 = pd.concat([coef1,coef1_j], axis=0)

    #use coef1_j to distribute tep consumption
    tep_j = ben_reduced[ben_reduced.index.isin(ben_[j].split(' + '))].sum(axis=0).values#.T
    diag_tep_j = np.diag(tep_j.T.flatten())
    tep_j = coef1_j.values @ diag_tep_j

    tep_j_df = pd.DataFrame(tep_j, columns=ben_reduced.columns, index= tru_j.index)
    tep = pd.concat([tep,tep_j_df], axis=0)

    #coefficient of emission
    coef2_j = coef_tep_to_ghg[(coef_tep_to_ghg['setor'].isin(ben_[j].split(' + '))) & (coef_tep_to_ghg['gas'].str.contains(gas))]
    coef2_j = coef2_j.iloc[:,2:] #exclude rows with unnecessary informations
    coef2_j = pd.DataFrame(coef2_j.mean(axis=0)).T #estimate the mean of coeficients to convert tep to emission

    coef2_j_df = tep_j_df.copy()
    coef2_j_df.loc[:, :] = coef2_j.iloc[0].values
    coef2 = pd.concat([coef2,coef2_j_df], axis=0)

  #tep and coefficients by household
  tep_h = ben_reduced[ben_reduced.index.str.contains('RESIDENCIAL')]
  coef1_h = tep_h.copy()
  coef1_h = (coef1_h * 0) + 1
  coef2_h = coef_tep_to_ghg[(coef_tep_to_ghg['setor'].str.contains('RESIDENCIAL')) & (coef_tep_to_ghg['gas'].str.contains(gas))].iloc[:,2:]
  coef2_h.index = ['RESIDENCIAL']
  coef2_h.columns = coef2.columns #remember that we assume that 'GÁS DE CIDADE E DE COQUERIA' = 'ELETRICIDADE'

  #estimation_emission
  """
  This method makes adjustments to incorporate households into tables.
  Depending on the value of self.household, it aggregates firms and household data
  and calculates emissions.
  """
  # Depending on the value of self.household, reorder DataFrame or not
  if household:
      tep = pd.concat([reorder_df(tep,N), tep_h], axis=0)
      coef1 = pd.concat([reorder_df(coef1,N), coef1_h], axis=0)
      coef2 = pd.concat([reorder_df(coef2,N), coef2_h], axis=0)
  else:
      # Aggregate firms and household
      tep = reorder_df(tep,N)
      coef1 = reorder_df(coef1,N)
      coef2 = reorder_df(coef2,N)

  # Calculate emission
  emission_tru = tep * coef2
  
  #create variable (emission_tru_adjusted)
  emission_tru_adjusted = adjust_emission(emission_tru, N, household)
  return emission_tru, tep, coef1, coef2, ben_to_tru, data_ben, emission_tru_adjusted

# 
def exact_estimation_true(year = '2017', N = '51', unity = 't', 
                          reference_year='2017',gas='CO2',household=False):
  print("This function is deprecated and will be removed in future versions.")
  coef1 = pd.DataFrame() #coefficint of distribution (value to tep)
  emission_ben = pd.DataFrame() #coefficient of emission (tep to ghg)
  emission_tru = pd.DataFrame()
  tep = pd.DataFrame()
  emission = pd.DataFrame()

  ben_to_tru = import_dictionaries(N)
  ben_to_tru_sectors = ben_to_tru[1]
  #ben_to_tru_products = ben_to_tru[0]
  ben_ = ben_to_tru_sectors['ben'].unique() #sector ben (j)
  num_sectors = len(ben_)

  data_ben = import_data_ben(year, N)
  ben_reduced = data_ben[1]

  data_tru = import_data_tru(year, N, unity, reference_year)
  tru_CI_energy = data_tru[1]

  for j in range(num_sectors):
    #corespondent rows of tru matrix to sector (j)
    tru_j_num = ben_to_tru_sectors[ben_to_tru_sectors['ben'] == ben_[j]][str('setor_tru'+N)]

    #tep of sector j
    tep_j = ben_reduced[ben_reduced.index.isin(ben_[j].split(' + '))]#.sum(axis=0).values#.T


    #emission coeficient of sector j
    coef2_j = coef_tep_to_ghg[(coef_tep_to_ghg['setor'].isin(ben_[j].split(' + '))) & (coef_tep_to_ghg['gas'].str.contains(gas))]
    coef2_j = pd.DataFrame(coef2_j.iloc[:,2:]) #exclude rows with unnecessary informations

    #emission of sector j (ben)
    emission_j_ben = tep_j.values * coef2_j.values #(sector1 , sector2, ...)
    emission_j_ben = emission_j_ben.sum(axis=0) #(sector1 + sector2 + ...)
    emission_j_ben = pd.DataFrame(emission_j_ben).T#, columns=sys.ben_reduced.columns)#, index= tep_j.index)
    emission_j_ben.columns = ben_reduced.columns
    emission_j_ben.index = [ben_[j]]
    emission_ben = pd.concat([emission_ben,emission_j_ben], axis=0)

    #estimate coeficient of distribution
    tru_j_num = ben_to_tru_sectors[ben_to_tru_sectors['ben'] == ben_[j]][str('setor_tru'+N)]
    tru_j = tru_CI_energy.iloc[tru_j_num-1,:]
    X_j = pd.DataFrame(tru_j.sum(axis=0))
    diag_X_j = np.diag(X_j[0].values)
    diag_X_j = diag_X_j.astype(float)
    inv_diag_X_j = np.linalg.pinv(diag_X_j)
    coef1_j = tru_j.values @ inv_diag_X_j
    coef1_j = pd.DataFrame(coef1_j, columns=ben_reduced.columns, index= tru_j.index)

    #adjust columns without coeficients of distribution
    total = coef1_j.sum().sum()
    totals = coef1_j.sum(axis=1)
    mean = totals / total
    for col in coef1_j.columns:
      if coef1_j[col].eq(0).all():
        coef1_j[col] = mean
    coef1 = pd.concat([coef1,coef1_j], axis=0)

    #emission of sector j (ben)
    emission_j_tru = coef1_j.values * emission_j_ben.values
    emission_j_tru = pd.DataFrame(emission_j_tru, columns=coef1_j.columns, index= coef1_j.index)
    emission_j_tru
    emission_tru = pd.concat([emission_tru,emission_j_tru], axis=0)

  #tep and coefficients by household
  tep_h = ben_reduced[ben_reduced.index.str.contains('RESIDENCIAL')]
  coef1_h = tep_h.copy()
  coef1_h = (coef1_h * 0) + 1
  coef2_h = coef_tep_to_ghg[(coef_tep_to_ghg['setor'].str.contains('RESIDENCIAL')) & (coef_tep_to_ghg['gas'].str.contains(gas))].iloc[:,2:]
  coef2_h.index = ['RESIDENCIAL']
  coef2_h.columns = coef1_j.columns #remember that we assume that 'GÁS DE CIDADE E DE COQUERIA' = 'ELETRICIDADE'
  emission_h_ben = tep_h.values * coef2_h.values
  emission_h_ben = pd.DataFrame(emission_h_ben, columns=coef1_j.columns, index= ['RESIDENCIAL'])

  #estimation_emission
  """
  This method makes adjustments to incorporate households into tables.
  Depending on the value of self.household, it aggregates firms and household data
  and calculates emissions.
  """
  # Depending on the value of self.household, reorder DataFrame or not
  if household:
      #self.tep = pd.concat([reorder_df(tep), tep_h], axis=0)
      coef1 = pd.concat([reorder_df(coef1,N), coef1_h], axis=0)
      emission_tru = pd.concat([reorder_df(emission_tru,N), emission_h_ben], axis=0)
      emission_ben = pd.concat([emission_ben, emission_h_ben], axis=0)
  else:
      # Aggregate firms and household
      #self.tep = reorder_df(tep)
      coef1 = reorder_df(coef1,N)
      emission_tru = reorder_df(emission_tru,N)
  
  #create variable (emission_tru_adjusted)
  emission_tru_adjusted = adjust_emission(emission_tru, N, household)
  return emission_tru, coef1, ben_to_tru, data_ben, emission_tru_adjusted


def emission(year = '2017', N = '51', unity = 't', 
             reference_year='2017',gas='CO2',household=False):
  coef1 = pd.DataFrame() #coefficint of distribution (value to tep)
  emission_ben = pd.DataFrame() #coefficient of emission (tep to ghg)
  emission_tru = pd.DataFrame()
  tep = pd.DataFrame()
  emission = pd.DataFrame()

  ben_to_tru = import_dictionaries(N)
  ben_to_tru_sectors = ben_to_tru[1]
  #ben_to_tru_products = ben_to_tru[0]
  ben_ = ben_to_tru_sectors['ben'].unique() #sector ben (j)
  num_sectors = len(ben_)

  data_ben = import_data_ben(year, N)
  ben_reduced = data_ben[1]

  data_tru = import_data_tru(year, N, unity, reference_year)
  tru_CI_energy = data_tru[1]

  for j in range(num_sectors):
    #corespondent rows of tru matrix to sector (j)
    tru_j_num = ben_to_tru_sectors[ben_to_tru_sectors['ben'] == ben_[j]][str('setor_tru'+N)]

    #tep of sector j
    tep_j = ben_reduced[ben_reduced.index.isin(ben_[j].split(' + '))]#.sum(axis=0).values#.T


    #emission coeficient of sector j
    coef2_j = coef_tep_to_ghg[(coef_tep_to_ghg['setor'].isin(ben_[j].split(' + '))) & (coef_tep_to_ghg['gas'].str.contains(gas))]
    coef2_j = pd.DataFrame(coef2_j.iloc[:,2:]) #exclude rows with unnecessary informations

    #emission of sector j (ben)
    emission_j_ben = tep_j.values * coef2_j.values #(sector1 , sector2, ...)
    emission_j_ben = emission_j_ben.sum(axis=0) #(sector1 + sector2 + ...)
    emission_j_ben = pd.DataFrame(emission_j_ben).T#, columns=sys.ben_reduced.columns)#, index= tep_j.index)
    emission_j_ben.columns = ben_reduced.columns
    emission_j_ben.index = [ben_[j]]
    emission_ben = pd.concat([emission_ben,emission_j_ben], axis=0)

    #estimate coeficient of distribution
    tru_j_num = ben_to_tru_sectors[ben_to_tru_sectors['ben'] == ben_[j]][str('setor_tru'+N)]
    tru_j = tru_CI_energy.iloc[tru_j_num-1,:]
    X_j = pd.DataFrame(tru_j.sum(axis=0))
    diag_X_j = np.diag(X_j[0].values)
    diag_X_j = diag_X_j.astype(float)
    inv_diag_X_j = np.linalg.pinv(diag_X_j)
    coef1_j = tru_j.values @ inv_diag_X_j
    coef1_j = pd.DataFrame(coef1_j, columns=ben_reduced.columns, index= tru_j.index)

    #adjust columns without coeficients of distribution
    total = coef1_j.sum().sum()
    totals = coef1_j.sum(axis=1)
    mean = totals / total
    for col in coef1_j.columns:
      if coef1_j[col].eq(0).all():
        coef1_j[col] = mean
    coef1 = pd.concat([coef1,coef1_j], axis=0)

    #emission of sector j (ben)
    emission_j_tru = coef1_j.values * emission_j_ben.values
    emission_j_tru = pd.DataFrame(emission_j_tru, columns=coef1_j.columns, index= coef1_j.index)
    emission_j_tru
    emission_tru = pd.concat([emission_tru,emission_j_tru], axis=0)

  #tep and coefficients by household
  tep_h = ben_reduced[ben_reduced.index.str.contains('RESIDENCIAL')]
  coef1_h = tep_h.copy()
  coef1_h = (coef1_h * 0) + 1
  coef2_h = coef_tep_to_ghg[(coef_tep_to_ghg['setor'].str.contains('RESIDENCIAL')) & (coef_tep_to_ghg['gas'].str.contains(gas))].iloc[:,2:]
  coef2_h.index = ['RESIDENCIAL']
  coef2_h.columns = coef1_j.columns #remember that we assume that 'GÁS DE CIDADE E DE COQUERIA' = 'ELETRICIDADE'
  emission_h_ben = tep_h.values * coef2_h.values
  emission_h_ben = pd.DataFrame(emission_h_ben, columns=coef1_j.columns, index= ['RESIDENCIAL'])

  #estimation_emission
  """
  This method makes adjustments to incorporate households into tables.
  Depending on the value of self.household, it aggregates firms and household data
  and calculates emissions.
  """
  # Depending on the value of self.household, reorder DataFrame or not
  if household:
      #self.tep = pd.concat([reorder_df(tep), tep_h], axis=0)
      coef1 = pd.concat([reorder_df(coef1,N), coef1_h], axis=0)
      emission_tru = pd.concat([reorder_df(emission_tru,N), emission_h_ben], axis=0)
      emission_ben = pd.concat([emission_ben, emission_h_ben], axis=0)
  else:
      # Aggregate firms and household
      #self.tep = reorder_df(tep)
      coef1 = reorder_df(coef1,N)
      emission_tru = reorder_df(emission_tru,N)
  
  #create variable (emission_tru_adjusted)
  emission_tru_adjusted = adjust_emission(emission_tru, N, household)
  return emission_tru, coef1, ben_to_tru, data_ben, emission_tru_adjusted
      
#this is the emisison adjusted to the unity used by MCTI (consulte the pdf)
def adjust_emission(emission_tru, N='51', household=False):
  if N == '51':
    #adjust_coef = [0.002092, 0.003407, 0.003389,	0.000217, 0.002357, 0.000528, 0.003133, 0.002174, 0.000376, 0.002388, 0.002235, 0.002835, 0.002724, 0.002724]
    adjust_coef = [0.676726, 1.118397, 1.120859, 0.068391, 0.777996, 0.172310, 1.036624, 0.714507, 0.122643, 0.789845, 0.736512, 0.933118, 0.895367, 0.895367]
    resicencial_coef = 0.466169
    ben_sectors_num = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 11, 13]
  elif N == '68':
    #adjust_coef = [0.001982, 0.003600, 0.003462, 0.000207,	0.002027, 0.002319, 0.000463, 0.003131, 0.002193, 0.000388, 0.002454, 0.002626, 0.002626, 0.002784, 0.003145, 0.002890]
    adjust_coef = [0.652574, 1.115892, 1.120859, 0.068391, 0.691369, 0.777996, 0.172303, 1.034645, 0.714507, 0.122643, 0.789845, 0.894843, 0.894843, 0.924196, 1.037051, 0.918792]
    resicencial_coef = 0.466169
    ben_sectors_num = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
  else:
    'none'
  emission_tru_adjusted = emission_tru.copy()
  for sec,coef in zip(ben_sectors_num, adjust_coef):
    row_names = map_ben_to_tru(N,emission_tru,sec,1)[0].index
    emission_tru_adjusted.loc[row_names] *= coef
  if household:
    emission_tru_adjusted.loc['RESIDENCIAL'] *= resicencial_coef
  return emission_tru_adjusted


def verification(N,coef1):
  verification = pd.DataFrame(columns=['value', 'sector_ben','product_ben'])
  for i in range(12): # Setor Ben
    for ii in range(17): # Produto Ben
      map1 = map_ben_to_tru(N,coef1,sector_ben_index=i,product_ben_index=ii)
      #map1 = map_ben_to_tru(self.coef1,i,ii)
      new_row = pd.DataFrame({'value': [map1[0].sum()[0]], 'sector_ben': [map1[1]], 
                              'product_ben':[map1[2]]})
      verification = pd.concat([verification, new_row], ignore_index=True)
      verification_ = verification.pivot(index='product_ben', columns='sector_ben',
                                         values='value').T
  return verification_[coef1.columns]





































