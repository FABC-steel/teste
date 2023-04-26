# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 09:31:19 2023

@author: FABC - PC
"""

import pandas as pd
import math

### baixar no https://power.larc.nasa.gov/data-access-viewer/
### selecionar os seguintes parâmetros: allsky, clearsky, temperature, específica humidade, velocidade do vento 10 metros
### velocidade do vento 50 metros, direção do vento 10 metros, direção do vento 50 metros
### excluir o cabeçalho e salvar no formato excel

### carregando dados


Nasa = pd.read_excel('C:/Users/FABC - PC/Desktop/simulação SAM/nasa sem cabeçalho.xlsx')

## dados para a simulação solar

DataFrame_intermediario = pd.DataFrame(columns = ['Year','Month','Day','GHI','Kt','BNI','DHI', 'Tdry','Dew Point','RH','Wspd','Wdir','Snow Depth', 'Pres'])

# GHI = global horizontal irradiance; BNI = bean normal irradiance, DHI = diffuse horizontal irradiance, Tdry = temperatura de bulbo seco, RH relative humidity
# Wsps = velocidade do vento 5 m; Direção de vento 5 m , dew point = ponto de orvalho, Ps = pressure

DataFrame_intermediario['Year'] = Nasa['YEAR']
DataFrame_intermediario['Month'] = Nasa['MO']
DataFrame_intermediario['Day'] = Nasa['DY']
DataFrame_intermediario['GHI'] = Nasa['ALLSKY_SFC_SW_DWN']

## cálculo da irradiação direta e difusa -  modelo ERBS; humidade relativa 

aux = len(DataFrame_intermediario)

for j in range(aux):
    DataFrame_intermediario.loc[j,'Kt'] = Nasa.loc[j,'ALLSKY_SFC_SW_DWN']/Nasa.loc[j,'CLRSKY_SFC_SW_DWN']
    if DataFrame_intermediario.loc[j,'Kt'] <= 0.22:
        kd = 1 - 0.99 *  DataFrame_intermediario.loc[j,'Kt'] 
    if 0.22 < DataFrame_intermediario.loc[j,'Kt'] or  DataFrame_intermediario.loc[j,'Kt'] <= 0.80:
        kd = 0.9511 - 0.1604 * (DataFrame_intermediario.loc[j,'Kt']) + 4.388 * (DataFrame_intermediario.loc[j,'Kt'])**2 - 16.638 * (DataFrame_intermediario.loc[j,'Kt'])**3 + 12.336 *  (DataFrame_intermediario.loc[j,'Kt'])**4 
    if  DataFrame_intermediario.loc[j,'Kt'] > 0.80:
        kd = 0.165
    DataFrame_intermediario.loc[j,'BNI'] = (1-kd) *  DataFrame_intermediario.loc[j,'GHI']
    DataFrame_intermediario.loc[j,'DHI'] = (kd) *  DataFrame_intermediario.loc[j,'GHI']
    DataFrame_intermediario.loc[j,'Tdry'] = Nasa.loc[j,'T2M']
    DataFrame_intermediario.loc[j,'RH'] = Nasa.loc[j,'RH2M']
    DataFrame_intermediario.loc[j,'Wdir'] = Nasa.loc[j,'WD10M']
    DataFrame_intermediario.loc[j,'Wspd'] = Nasa.loc[j,'WS10M']
    DataFrame_intermediario.loc[j,'Snow Depth'] = 0
    DataFrame_intermediario.loc[j,'Dew Point'] = Nasa.loc[j,'T2MDEW']
    DataFrame_intermediario.loc[j,'Pres'] = Nasa.loc[j,'PS']*10
    
### dados solar

entrada_solar = pd.DataFrame()

entrada_solar.loc[0,0] = 'Source'
entrada_solar.loc[0,1] = 'Location ID'
entrada_solar.loc[0,2] = 'City'
entrada_solar.loc[0,3] = 'State'
entrada_solar.loc[0,4] = 'Country'
entrada_solar.loc[0,5] = 'Latitude'
entrada_solar.loc[0,6] = 'Longitude'
entrada_solar.loc[0,7] = 'Time Zone'
entrada_solar.loc[0,8] = 'Elevation'

entrada_solar.loc[1,0] = 'Power_Nasa'
entrada_solar.loc[1,1] = '002'
entrada_solar.loc[1,2] = 'Sobradinho'
entrada_solar.loc[1,3] = 'Bahia'
entrada_solar.loc[1,4] = 'Brazil'
entrada_solar.loc[1,5] = -9.3884
entrada_solar.loc[1,6] = -40.8461
entrada_solar.loc[1,7] = -3
entrada_solar.loc[1,8] = 445.79

entrada_solar.loc[2,0] = 'Year'
entrada_solar.loc[2,1] = 'Month'
entrada_solar.loc[2,2] = 'Day'
entrada_solar.loc[2,3] = 'Hour'
entrada_solar.loc[2,4] = 'Minute'
entrada_solar.loc[2,5] = 'DNI'
entrada_solar.loc[2,6] = 'DHI'
entrada_solar.loc[2,7] = 'GHI'
entrada_solar.loc[2,8] = 'Elevation'
entrada_solar.loc[2,9] = 'wind speed'
entrada_solar.loc[2,10] = 'wind direction'
entrada_solar.loc[2,11] = 'rh'
entrada_solar.loc[2,12] = 'pres'




for i in range(aux):
    entrada_solar.loc[i+3,0] = DataFrame_intermediario.loc[i,'Year']
    entrada_solar.loc[i+3,1] = DataFrame_intermediario.loc[i,'Month']
    entrada_solar.loc[i+3,2] = DataFrame_intermediario.loc[i,'Day']
    entrada_solar.loc[i+3,3] = 0
    entrada_solar.loc[i+3,4] = 0
    entrada_solar.loc[i+3,5] = DataFrame_intermediario.loc[i,'BNI']
    entrada_solar.loc[i+3,6] = DataFrame_intermediario.loc[i,'DHI']
    entrada_solar.loc[i+3,7] = DataFrame_intermediario.loc[i,'GHI']
    entrada_solar.loc[i+3,8] = '445.79'
    entrada_solar.loc[i+3,9] =  DataFrame_intermediario.loc[i,'Wspd']
    entrada_solar.loc[i+3,10] = DataFrame_intermediario.loc[i,'Wdir']
    entrada_solar.loc[i+3,11] = DataFrame_intermediario.loc[i,'RH']
    entrada_solar.loc[i+3,12] = DataFrame_intermediario.loc[i,'Pres']


### dados eólicos


entrada_eolico = pd.DataFrame()

entrada_eolico.loc[0,0] = 'Source'
entrada_eolico.loc[0,1] = 'Location ID'
entrada_eolico.loc[0,2] = 'City'
entrada_eolico.loc[0,3] = 'State'
entrada_eolico.loc[0,4] = 'Country'
entrada_eolico.loc[0,5] = 'Latitude'
entrada_eolico.loc[0,6] = 'Longitude'
entrada_eolico.loc[0,7] = 'Time Zone'
entrada_eolico.loc[0,8] = 'Elevation'

entrada_eolico.loc[1,0] = 'Power_Nasa'
entrada_eolico.loc[1,1] = '002'
entrada_eolico.loc[1,2] = 'Sobradinho'
entrada_eolico.loc[1,3] = 'Bahia'
entrada_eolico.loc[1,4] = 'Brazil'
entrada_eolico.loc[1,5] = -9.3884
entrada_eolico.loc[1,6] = -40.8461
entrada_eolico.loc[1,7] = -3
entrada_eolico.loc[1,8] = 445.79

entrada_eolico.loc[2,0] = 'temp'
entrada_eolico.loc[2,1] = 'pres'
entrada_eolico.loc[2,2] = 'speed'
entrada_eolico.loc[2,3] = 'direction'

entrada_eolico.loc[3,0] = 'C'
entrada_eolico.loc[3,1] = 'atm'
entrada_eolico.loc[3,2] = 'm/s'
entrada_eolico.loc[3,3] = 'degrees'

entrada_eolico.loc[4,0] = '2'
entrada_eolico.loc[4,1] = '2'
entrada_eolico.loc[4,2] = '10'
entrada_eolico.loc[4,3] = '10'


for i in range(aux):
    entrada_eolico.loc[i+3,0] = DataFrame_intermediario.loc[i,'Tdry']
    entrada_eolico.loc[i+3,1] = DataFrame_intermediario.loc[i,'Pres'] * 0.00986923
    entrada_eolico.loc[i+3,2] = DataFrame_intermediario.loc[i,'Wspd']
    entrada_eolico.loc[i+3,3] = DataFrame_intermediario.loc[i,'Wdir']

## salvando em csv

entrada_solar.to_csv('sobradinho_solar_SAM.csv', index = False, header = False)
entrada_eolico.to_csv('sobradinho_eolico_SAM.csv', index = False, header = False)


