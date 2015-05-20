import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import pairwise_distances

hurricane_data_path = '../../COS424_FinalProject/track_data'

##### Read data from 1979
data=pd.read_csv('%s/hurdat2-1851-2014-022315.txt' % (hurricane_data_path), sep=',', header=None)
data_from1979 = data[33658:]
column1 = data_from1979[0]
hurricane_name_index = column1[column1.str.startswith('A')==True].index
hurricane_number = hurricane_name_index.shape[0]
hurricane_test_ID = 'AL112009'

hurricaneDic = {}
for i in range(hurricane_number-1):
    hurricane_ID = data_from1979.loc[hurricane_name_index[i]][0]
    hurricane_ID_data = data_from1979.loc[hurricane_name_index[i]:hurricane_name_index[i+1]-1]
    if hurricane_ID_data.shape[0] > 26:
        hurricaneDic[hurricane_ID] = hurricane_ID_data

def get_hurricane_loc(data, nTime):
    lat = np.array([map(float, str.split(data[4].values[i][:-1])) for i in range(nTime)]).squeeze()
    lon = np.array([map(float, str.split(data[5].values[i][:-1])) for i in range(nTime)]).squeeze()
    return lat, lon

def get_hurricane_feature():
    lat = []
    lon = []
    wind = []
    pressure = []
    for ID in hurricaneDic.keys():
        if ID != hurricane_test_ID:
            hurricane_each = hurricaneDic[ID][1:]
            ntime = hurricane_each.shape[0]
            if ntime > ntime_state:
                hurricane_lat, hurricane_lon = get_hurricane_loc(hurricane_each, ntime_state)
                hurricane_wind = hurricane_each[6].values[:ntime_state]
                hurricane_pressure = hurricane_each[7].values[:ntime_state]
                lat.append(hurricane_lat)
                lon.append(hurricane_lon)
                wind.append(hurricane_wind)
                pressure.append(hurricane_pressure)
    return np.array(lat), np.array(lon), np.array(wind), np.array(pressure)

def get_hurricane_feature_all():
    lat = []
    lon = []
    wind = []
    pressure = []
    for ID in hurricaneDic.keys():
        if ID != hurricane_test_ID:
            hurricane_each = hurricaneDic[ID][1:]
            ntime = hurricane_each.shape[0]
            if ntime > ntime_state:
                hurricane_lat, hurricane_lon = get_hurricane_loc(hurricane_each, ntime)
                hurricane_wind = hurricane_each[6].values[:ntime]
                hurricane_pressure = hurricane_each[7].values[:ntime]
                lat.append(hurricane_lat)
                lon.append(hurricane_lon)
                wind.append(hurricane_wind)
                pressure.append(hurricane_pressure)
    return np.array(lat), np.array(lon), np.array(wind), np.array(pressure)

hurricane_test = hurricaneDic[hurricane_test_ID][1:]
ntime_state = hurricane_test.shape[0]*2/3
lat_test = np.array([map(float, str.split(hurricane_test[4].values[i][:-1])) for i in range(hurricane_test.shape[0])]).squeeze()
lon_test = np.array([map(float, str.split(hurricane_test[5].values[i][:-1])) for i in range(hurricane_test.shape[0])]).squeeze()
wind_test = hurricane_test[6].values 
pressure_test = hurricane_test[7].values
test_set = np.hstack([lat_test, lon_test, wind_test, pressure_test])
np.savetxt('./Xt_all.txt', test_set.reshape(4,-1), fmt='%5.3f')

hurricane_set = np.hstack([get_hurricane_feature_all()[0], get_hurricane_feature_all()[1], get_hurricane_feature_all()[2], get_hurricane_feature_all()[3]])
hurricane_set_same = np.hstack([get_hurricane_feature()[0], get_hurricane_feature()[1], get_hurricane_feature()[2], get_hurricane_feature()[3]])
distances = np.array([pairwise_distances(hurricane_set_same[i], test_set.reshape(4,-1)[:,:ntime_state].reshape(-1)) for i in range(hurricane_set_same.shape[0])]).squeeze()
indices = np.argsort(distances)

# Select the top 20
k = 20
lat_k = get_hurricane_feature_all()[0][indices[:k]]
lon_k = get_hurricane_feature_all()[1][indices[:k]]
wind_k = get_hurricane_feature_all()[2][indices[:k]]
pressure_k = get_hurricane_feature_all()[3][indices[:k]]
min_len = np.array([lat_k[i].shape[0] for i in range(k)]).min()
lat_k = np.array([lat_k[i][:min_len] for i in range(k)])
lon_k = np.array([lon_k[i][:min_len] for i in range(k)])
wind_k = np.array([wind_k[i][:min_len] for i in range(k)])
pressure_k = np.array([pressure_k[i][:min_len] for i in range(k)])
test_set_k = np.hstack([lat_k.mean(0), lon_k.mean(0), wind_k.mean(0), pressure_k.mean(0)])
np.savetxt('./historical_top20_all.txt', test_set_k.reshape(4,-1), fmt='%5.3f')

