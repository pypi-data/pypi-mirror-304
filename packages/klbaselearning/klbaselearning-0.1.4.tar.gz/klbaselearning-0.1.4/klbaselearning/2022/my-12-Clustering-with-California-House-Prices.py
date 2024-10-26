#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn import cluster as clu
from sklearn import pipeline as pip
from sklearn import metrics as met
from sklearn import decomposition as dec
from sklearn import preprocessing as pre
from sklearn import manifold as man
from sklearn import compose as cmp
import plotly.graph_objects as go
from sklearn import impute as imp
import sklearn.neighbors as nn


# In[ ]:


df = pd.read_csv("https://raw.githubusercontent.com/ageron/handson-ml/master/datasets/housing/housing.csv")
df.head(5)


# In[ ]:


df.describe(include="all").T


# In[ ]:


X_train = df.drop(columns=["median_house_value"],axis=1)


# In[ ]:


fig = go.Figure(data=go.Scattergeo(
        lon = df['longitude'],
        lat = df['latitude'],
        text = df['median_house_value'],
        mode = 'markers',
        marker_color = df['median_house_value'],      
        ))
fig.show()


# In[ ]:


import plotly.graph_objects as go

import pandas as pd

fig = go.Figure(data=go.Scattergeo(
        locationmode = 'USA-states',
        lon = df['longitude'],
        lat = df['latitude'],
        text = df['median_house_value'],
        mode = 'markers',
        marker = dict(
            #size = 8,
            opacity = 0.8,
            reversescale = True,
            autocolorscale = False,
            #symbol = 'square',
            line = dict(
                width=1,
                color='rgba(102, 102, 102)'
            ),
            colorscale = 'RdBu',
            cmin = 0,
            color = df['median_house_value'],
            cmax = df['median_house_value'].max(),
            colorbar_title="median_house_value"
        )))

fig.update_layout(
        #title = 'median_house_value)',
        geo = dict(
            scope='usa',
            projection_type='albers usa',
            showland = True,
            landcolor = "rgb(250, 250, 250)",
            subunitcolor = "rgb(217, 217, 217)",
            countrycolor = "rgb(217, 217, 217)",
            countrywidth = 0.5,
            subunitwidth = 0.5
        ),
    )
fig.show()


# # Kmeans

# In[ ]:


num_list = list(X_train.select_dtypes("number").columns)
cat_list = list(X_train.select_dtypes(exclude="number").columns)

pipe_num = pip.Pipeline([
                        ("imp",imp.SimpleImputer(strategy="mean")),
                        ("scl",pre.StandardScaler()) 
                        ]) 

pipe_cat = pip.Pipeline([
                        ("ohe",pre.OneHotEncoder())
                        ]) 
preprocessor = cmp.ColumnTransformer([
                                      ("numimp",pipe_num,num_list),
                                      ("cat",pipe_cat,cat_list)],
                                      remainder="passthrough")



# In[ ]:


x_values = []
y_values = []
for i in range(1,40):
    pipe = pip.Pipeline([
                        ("pre",preprocessor),
                        ("clu",clu.KMeans(n_clusters=i,random_state=42))
                        ])
    pipe.fit(X_train)
    x_values.append(i)
    y_values.append(pipe.named_steps["clu"].inertia_)
plt.plot(x_values,y_values)
plt.show()


# In[ ]:


# 10 seems okay


# In[ ]:


pipe = pip.Pipeline([
                    ("pre",preprocessor),
                    ("clu",clu.KMeans(n_clusters=10,random_state=42))
                    ])
pipe.fit(X_train)


# In[ ]:


import plotly.graph_objects as go

import pandas as pd

fig = go.Figure(data=go.Scattergeo(
        locationmode = 'USA-states',
        lon = X_train['longitude'],
        lat = X_train['latitude'],
        text = pipe[1].labels_,
        mode = 'markers',
        marker = dict(
            #size = 8,
            #opacity = 0.5,
            reversescale = True,
            #autocolorscale = False,
            #symbol = 'square',
            line = dict(
                width=1,
                color='rgba(102, 102, 102)'
            ),
            colorscale = 'RdBu',
            cmin = 0,
            color = pipe[1].labels_,
            cmax = pipe[1].labels_.max(),
            colorbar_title="median_house_value"
        )))

fig.update_layout(
        title = 'Cluesters',
        geo = dict(
            scope='usa',
            projection_type='albers usa',
            showland = True,
            landcolor = "rgb(250, 250, 250)",
            subunitcolor = "rgb(217, 217, 217)",
            countrycolor = "rgb(217, 217, 217)",
            countrywidth = 0.5,
            subunitwidth = 0.5
        ),
    )
fig.show()


# # DBscan

# In[ ]:


num_list = list(X_train.select_dtypes("number").columns)
cat_list = list(X_train.select_dtypes(exclude="number").columns)

pipe_num = pip.Pipeline([
                        ("imp",imp.SimpleImputer(strategy="mean")),
                        ("scl",pre.StandardScaler()) 
                        ]) 

pipe_cat = pip.Pipeline([
                        ("ohe",pre.OneHotEncoder())
                        ]) 
preprocessor = cmp.ColumnTransformer([
                                      ("numimp",pipe_num,num_list),
                                      ("cat",pipe_cat,cat_list)],
                                      remainder="passthrough")

pipe = pip.Pipeline([
                    ("pre",preprocessor),
                    #("nn",nn.NearestNeighbors(n_neighbors=10,algorithm="auto"))
                    ])
pipe.fit(X_train)


# In[ ]:


X_train_transformed = pipe.fit_transform(X_train)


# In[ ]:


nn_obj = nn.NearestNeighbors(n_neighbors=10,algorithm="auto")
nn_obj.fit(X_train_transformed)
output = nn_obj.kneighbors(X_train_transformed, return_distance=True)


# In[ ]:


X_train_transformed.shape


# In[ ]:


print("indices",output[0].shape)
print("distances",output[1].shape)


# In[ ]:


mean_distances = list(pd.DataFrame(output[0]).mean(axis=1).sort_values().values)
mean_indexes = list(pd.DataFrame(output[1]).index)
i = 0
for i in range(5):
    print(mean_indexes[i],mean_distances[i])


# In[ ]:


plt.plot(mean_indexes,mean_distances)
plt.show()


# In[ ]:


plt.plot(mean_indexes,mean_distances)
plt.ylim(0, 3)
plt.show()


# In[ ]:


# 1 seems to be fine


# In[ ]:


num_list = list(X_train.select_dtypes("number").columns)
cat_list = list(X_train.select_dtypes(exclude="number").columns)

pipe_num = pip.Pipeline([
                        ("imp",imp.SimpleImputer(strategy="mean")),
                        ("scl",pre.StandardScaler()) 
                        ]) 

pipe_cat = pip.Pipeline([
                        ("ohe",pre.OneHotEncoder())
                        ]) 
preprocessor = cmp.ColumnTransformer([
                                      ("numimp",pipe_num,num_list),
                                      ("cat",pipe_cat,cat_list)],
                                      remainder="passthrough")

pipe = pip.Pipeline([
                    ("pre",preprocessor),
                    ("clu",clu.DBSCAN(eps=1,min_samples=10))
                    ])
pipe.fit(X_train)


# In[ ]:


import plotly.graph_objects as go

import pandas as pd

fig = go.Figure(data=go.Scattergeo(
        locationmode = 'USA-states',
        lon = X_train['longitude'],
        lat = X_train['latitude'],
        text = pipe[1].labels_,
        mode = 'markers',
        marker = dict(
            #size = 8,
            #opacity = 0.5,
            reversescale = True,
            #autocolorscale = False,
            #symbol = 'square',
            line = dict(
                width=1,
                color='rgba(102, 102, 102)'
            ),
            colorscale = 'RdBu',
            cmin = 0,
            color = pipe[1].labels_,
            cmax = pipe[1].labels_.max(),
            colorbar_title=""
        )))

fig.update_layout(
        #title = 'Cluesters',
        geo = dict(
            scope='usa',
            projection_type='albers usa',
            showland = True,
            landcolor = "rgb(250, 250, 250)",
            subunitcolor = "rgb(217, 217, 217)",
            countrycolor = "rgb(217, 217, 217)",
            countrywidth = 0.5,
            subunitwidth = 0.5
        ),
    )
fig.show()

