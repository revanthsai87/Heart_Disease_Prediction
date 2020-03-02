import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier

def user_ip(dfr):
    os.chdir('C:\\Users\\REVANTH\\Desktop')
    data = pd.read_csv('./heart.csv')
    data1 = data.drop(['chol', 'fbs'], axis=1)
    a = pd.get_dummies(data['cp'], prefix="cp")
    b = pd.get_dummies(data['thal'], prefix="thal")
    c = pd.get_dummies(data['slope'], prefix="slope")
    frames = [data1, a, b, c]
    df = pd.concat(frames, axis=1)
    df = df.drop(columns=['cp', 'thal', 'slope'])
    model_data = df
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import RobustScaler
    basic_target = model_data['target']
    basic_features = model_data.drop(['target'], axis=1)
    x = RobustScaler()
    basic_features = x.fit_transform(basic_features)
    features_train, features_test, target_train, target_test = train_test_split(basic_features, basic_target,
                                                                                test_size=0.2, random_state=42)
    x = RobustScaler()
    d = pd.DataFrame(df[:-1].drop('target', axis=1))
    # d=d.append(df[2:3].drop('target',axis=1))
    dt={}
    dt['age']=[dfr[0]]
    dt['sex']=[dfr[1]]
    dt['trestbps'] = [dfr[3]]
    dt['restecg'] = [dfr[4]]
    dt['thalach'] = [dfr[5]]
    dt['exang'] = [dfr[6]]
    dt['oldpeak'] = dfr[7]
    dt['ca'] = [dfr[9]]
    if dfr[2]==0:
      dt['cp_0']=[1]
      dt['cp_1']=[0]
      dt['cp_2']=[0]
      dt['cp_3']=[0]
    elif dfr[2]==1:
      dt['cp_0']=[0]
      dt['cp_1']=[1]
      dt['cp_2']=[0]
      dt['cp_3']=[0]
    elif dfr[2]==2:
      dt['cp_0']=[0]
      dt['cp_1']=[0]
      dt['cp_2']=[1]
      dt['cp_3']=[0]
    elif dfr[2] ==3 :
        dt['cp_0'] = [0]
        dt['cp_1'] = [0]
        dt['cp_2'] = [0]
        dt['cp_3']=[1]
    if dfr[10]==0:
     dt['thal_0']=[1]
     dt['thal_1']=[0]
     dt['thal_2']=[0]
     dt['thal_3']=[0]
    elif dfr[10]==1:
     dt['thal_0'] = [0]
     dt['thal_1'] = [1]
     dt['thal_2'] = [0]
     dt['thal_3'] = [0]
    elif dfr[10]==2:
     dt['thal_0'] =[0]
     dt['thal_1'] =[0]
     dt['thal_2'] = [1]
     dt['thal_3'] = [0]
    elif dfr[10] ==3 :
     dt['thal_0'] =[0]
     dt['thal_1'] = [0]
     dt['thal_2'] = [0]
     dt['thal_3'] = [1]
    if dfr[8] == 0:
     dt['slope_0'] = [1]
     dt['slope_1'] = [0]
     dt['slope_2'] = [0]
    elif dfr[8] == 1:
     dt['slope_0'] = [0]
     dt['slope_1'] = [1]
     dt['slope_2'] = [0]
    elif dfr[8] == 2:
      dt['slope_0'] = [0]
      dt['slope_1'] = [0]
      dt['slope_2'] = [1]
    dt1=pd.DataFrame.from_dict(dt)
    print(dt1[0:])
    d=d.append(dt1[0:])
    print(d)
    d=x.fit_transform(d)
    knn_classifier = KNeighborsClassifier(n_neighbors =9 )
    knn_classifier.fit(features_train,target_train )
    model_pred = knn_classifier.predict(d)
    print( "final",model_pred[-1:][0])
    return model_pred[-1:][0]