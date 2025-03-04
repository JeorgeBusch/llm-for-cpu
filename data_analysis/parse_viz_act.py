# %%

# quick and dirty change? 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os
import missingno as msno

# different dependencies for kmeans stuff 
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

# more dependencies 
import plotly.graph_objects as go
import streamlit as st
import plotly.express as px


# knee finder 
from kneefinder import KneeFinder


# Function to get all subdirectories in a given directory
def get_subdirectories(directory_path):
    try:
        items = os.listdir(directory_path)
        subdirectories = [item for item in items if os.path.isdir(os.path.join(directory_path, item))]
        return subdirectories
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Function to collect data from all stats.txt files in nested directories

def collect_data_from_directory(directory_path):
    data = {}
    param_set_directories = get_subdirectories(directory_path)

    for param_set in param_set_directories:
        param_set_path = os.path.join(directory_path, param_set)
        params_directories = get_subdirectories(param_set_path)
        
        for param in params_directories:
            file_path = os.path.join(param_set_path, param, 'stats.txt')
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'r') as file:
                        lines = file.readlines()

                    for line in lines:
                        parts = line.split()
                        if len(parts) < 2:
                            continue
                        key = parts[0]
                        if ("inst" in key) or ("Inst" in key) or ('system.cpu.mmu.dtb.rdMisses' in key) or ('system.cpu.mmu.dtb.wrMisses' in key) or ('system.cpu.mmu.itb.rdMisses' in key) or ('system.cpu.mmu.itb.wrMisses' in key) or ('system.cpu.numCycles' in key):
                            if not("system.mem_ctrl.dram" in key):
                                value = float(parts[1])
                                if key in data:
                                    data[key].append(value)
                                else:
                                    data[key] = [value]
                except FileNotFoundError:
                    print(f"File not found: {file_path}")
                except Exception as e:
                    print(f"An error occurred while reading {file_path}: {e}")
    
    return data

# Path to the main directory containing all params_set directories
main_directory_path = r'C:\stats_research\llm-for-cpu\data_analysis\params'

# Collect data from the main directory
combined_data = collect_data_from_directory(main_directory_path)

# Convert the data to a DataFrame
df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in combined_data.items()]))

df.head(100000)

#%%
# # because there is no need for more padding (seems like every value is covered), check for missing values and remove/fill them?
# df.fillna(0, inplace=True)
# # df = df.drop(df.columns[0], axis=1)

msno.matrix(df) 

missing_values = df.isnull().sum()
print(missing_values)


#%%
# make new columns here. 
# - data mpki cache misses per 1000 instructions (data table)
#     - 1000 * (system.cpu0.mmu.dtb.rdMisses +system.cpu0.mmu.dtb.wrMisses) / simInsts
# - instruction mpki (instruction table)
#     - 1000 * (system.cpu0.mmu.itb.rdMisses +system.cpu0.mmu.itb.wrMisses) / simInsts

df['data_mpki'] = 1000 * (df['system.cpu.mmu.dtb.rdMisses'] + df['system.cpu.mmu.dtb.wrMisses'] / df['simInsts'])
df['inst_mpki'] = 1000 * (df['system.cpu.mmu.itb.rdMisses'] + df['system.cpu.mmu.itb.wrMisses'] / df['simInsts'])
df['IPC'] = df['simInsts'] / df['system.cpu.numCycles']


# %%

# Creating clustering features -> using the scaler

scaler = MinMaxScaler()
df_scaled1 = scaler.fit_transform(df[['data_mpki', 'IPC']])

scaler = MinMaxScaler()
df_scaled2 = scaler.fit_transform(df[['inst_mpki', 'IPC']])

# %%

k_rng = range(1,10)
sse = []
sse2 = []

# for some reason Integrating them into the same loop results in them being the exact same.  

for k in k_rng:
    km = KMeans(n_clusters=k)
    km.fit(df_scaled1)
    sse.append(km.inertia_)

for k in k_rng:
    km = KMeans(n_clusters=k)
    km.fit(df_scaled2)
    sse2.append(km.inertia_)

# %%
print(sse)
print(sse2)

# %%

plt.figure()
plt.xlabel('K')
plt.ylabel('Sum of squared error 1')
plt.plot(k_rng,sse)


plt.figure()
plt.xlabel('K')
plt.ylabel('Sum of squared error 2')
plt.plot(k_rng,sse2)

# %% 
# Using the kneefinder library 

kf = KneeFinder(k_rng, sse)
knee_x, knee_y = kf.find_knee()
kf.plot()

kf2 = KneeFinder(k_rng, sse2)
knee_x2, knee_y2 = kf.find_knee()
kf2.plot()


# %%

km = KMeans(n_clusters=4)
y_predicted = km.fit_predict(df_scaled1)
df['cluster_data_IPC'] = y_predicted


km2 = KMeans(n_clusters=3)
y_predicted = km2.fit_predict(df_scaled2)
df['cluster_inst_IPC'] = y_predicted

# ------------- data_mpki, CLUSTERED WITH IPC -------------

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df['IPC'], y=df['data_mpki'], mode='markers', marker=dict(color=df['cluster_data_IPC'], colorscale='Viridis', showscale=True)))
fig1.update_layout(title='Clustered graph, IPC vs data_mpki', xaxis_title='IPC', yaxis_title='data_mpki')

# ------------- inst_mpki, CLUSTERED WITH IPC -------------

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df['IPC'], y=df['inst_mpki'], mode='markers', marker=dict(color=df['cluster_inst_IPC'], colorscale='Viridis', showscale=True)))
fig2.update_layout(title='Clustered graph, IPC vs inst_mpki', xaxis_title='IPC', yaxis_title='inst_mpki')

# Streamlit app
st.title('Interactive Clustering Visualization')

fig1.show()
fig2.show()

# for streamlit: 
# st.plotly_chart(fig1)
# st.plotly_chart(fig2)


# %%

print(km2.cluster_centers_)
# testing out the x 
print(km2.cluster_centers_[:,0])

# testing out the y 
print(km2.cluster_centers_[:,1])

# %%

# filtering cluster 1 for data IPC 

df['filtered_cluster1_dataIPC'] = df.loc[(df['cluster_data_IPC'] == 1), ['data_mpki']]
df['filtered_cluster2_dataIPC'] = df.loc[(df['cluster_data_IPC'] == 2), ['data_mpki']]
df['filtered_cluster3_dataIPC'] = df.loc[(df['cluster_data_IPC'] == 3), ['data_mpki']]

# ---- create the separate set 

df['filtered_cluster1_instIPC'] = df.loc[(df['cluster_data_IPC'] == 1), ['data_mpki']]
df['filtered_cluster2_instIPC'] = df.loc[(df['cluster_data_IPC'] == 2), ['data_mpki']]
df['filtered_cluster3_instIPC'] = df.loc[(df['cluster_data_IPC'] == 3), ['data_mpki']]

df.head()



# %%
# Make the actual dataframe 

# review for debugging purposes 


# %%

# actually plotting data_mpki, inst_mpki and IPC 

fig, axes = plt.subplots(nrows = 1, ncols = 3, figsize = (18,5))

# ------------- data_mpki -------------

# sns.barplot(ax=axes[0], x = df.index, y = df['data_mpki'], color = 'blue', label = 'Barplot', alpha = 0.2)

sns.scatterplot(ax = axes[0], x=df.index, y = df['data_mpki'], marker = 'o', color = 'purple')
# axes[0].set_ylim(1.6398e6, 1.645e6)

axes[0].set_title('data_mpki')
axes[0].set_xlabel('Index')
axes[0].set_ylabel('Values')

# ------------- inst_mpki -------------

plt.figure()
# sns.barplot(ax=axes[1], x = df.index, y = df['inst_mpki'], color = 'blue', label = 'Barplot', alpha = 0.2)
sns.scatterplot(ax = axes[1], x=df.index, y = df['inst_mpki'], marker = 'o', color = 'purple')
# axes[1].set_ylim(0.0013050, 0.00132)
axes[1].set_title('inst_mpki')
axes[1].set_xlabel('Index')
axes[1].set_ylabel('Values')

# ------------- IPC -------------

plt.figure()
# sns.barplot(ax=axes[2], x = df.index, y = df['IPC'], color = 'blue', label = 'Barplot', alpha = 0.2)
sns.scatterplot(ax=axes[2], x=df.index, y = df['IPC'], marker = 'o', color = 'purple')
# axes[2].set_ylim(0.01200, 0.01204)
axes[2].set_title('IPC')
axes[2].set_xlabel('Index')
axes[2].set_ylabel('Values')

# adjusting the main layout
plt.tight_layout()
plt.show()

# PLOTLY VERSIONS

# Create Plotly scatter plots
fig_data_mpki = px.scatter(df, x=df.index, y='data_mpki', title='data_mpki', labels={'x': 'Index', 'data_mpki': 'Values'}, color_discrete_sequence=['purple'])
fig_inst_mpki = px.scatter(df, x=df.index, y='inst_mpki', title='inst_mpki', labels={'x': 'Index', 'inst_mpki': 'Values'}, color_discrete_sequence=['purple'])
fig_IPC = px.scatter(df, x=df.index, y='IPC', title='IPC', labels={'x': 'Index', 'IPC': 'Values'}, color_discrete_sequence=['purple'])

fig_data_mpki.show()
fig_inst_mpki.show()
fig_IPC.show()

# for streamlit: 
# st.plotly_chart(fig_data_mpki)
# st.plotly_chart(fig_inst_mpki)
# st.plotly_chart(fig_IPC)

# %% 

fig, axes = plt.subplots(nrows = 1, ncols = 3, figsize = (18,5))

# ------------- data_mpki -------------

sns.kdeplot(ax = axes[0], x=df.index, y = df['data_mpki'], color = 'purple', fill = True)
# axes[0].set_ylim(1.6398e6, 1.645e6)
axes[0].set_title('data_mpki')
axes[0].set_xlabel('Index')
axes[0].set_ylabel('Values')

# ------------- inst_mpki -------------

plt.figure()
sns.kdeplot(ax = axes[1], x=df.index, y = df['inst_mpki'],color = 'purple', fill = True)
# axes[1].set_ylim(0.0013050, 0.00132)
axes[1].set_title('inst_mpki')
axes[1].set_xlabel('Index')
axes[1].set_ylabel('Values')

# ------------- IPC -------------

plt.figure()
sns.kdeplot(ax=axes[2], x=df.index, y = df['IPC'], color = 'purple', fill = True)
# axes[2].set_ylim(0.01200, 0.01204)
axes[2].set_title('IPC')
axes[2].set_xlabel('Index')
axes[2].set_ylabel('Values')

# adjusting the main layout
plt.tight_layout()
plt.show()


# plotly versions

fig_data_mpki = px.density_heatmap(df, x=df.index, y='data_mpki', title='data_mpki', labels={'x': 'Index', 'data_mpki': 'Values'}, color_continuous_scale='Viridis')
fig_inst_mpki = px.density_heatmap(df, x=df.index, y='inst_mpki', title='inst_mpki', labels={'x': 'Index', 'inst_mpki': 'Values'}, color_continuous_scale='Viridis')
fig_IPC = px.density_heatmap(df, x=df.index, y='IPC', title='IPC', labels={'x': 'Index', 'IPC': 'Values'}, color_continuous_scale='Viridis')

fig_data_mpki.update_layout(width=600, height=400)
fig_inst_mpki.update_layout(width=600, height=400)
fig_IPC.update_layout(width=600, height=400)

fig_data_mpki.show()
fig_inst_mpki.show()
fig_IPC.show()

# for streamlit: 
# st.plotly_chart(fig_data_mpki)
# st.plotly_chart(fig_inst_mpki)
# st.plotly_chart(fig_IPC)

#%%
# before looking at the graph for each simulation, average each of the instructions 

# once again bar plots are not the way considering just how big the data is 

# This graph does NOT use log scaling

import numpy as np 

mean_values = df.mean()
print(mean_values.min())
print(mean_values.max())
print(mean_values.mean())

# mean_values_filtered = [value for value in mean_values.values if value != 0]
plt.figure(figsize=(20,12))
sns.barplot(x=mean_values.index, y=mean_values.values, alpha=0.2, label='Bar plot')
sns.lineplot(x=mean_values.index, y=mean_values.values, marker='o', color='purple', label='Mean line')
# plt.ylim(0,0.1e5)
# plt.ylim(0,1e2)
# plt.ylim(ylim)
_ = plt.xticks(rotation=90)

#%%

# This graph actually uses the scaling

#logarithmic scale -> upper lower boundaries 
p75 = mean_values.quantile(0.75) * 2.5
ylim = (1, 10**np.ceil(np.log10(p75)))


# mean_values_filtered = [value for value in mean_values.values if value != 0]
plt.figure(figsize=(20,12))
sns.barplot(x=mean_values.index, y=mean_values.values, alpha=0.2, label='Bar plot')
sns.lineplot(x=mean_values.index, y=mean_values.values, marker='o', color='purple', label='Mean line')
plt.ylim(ylim)
_ = plt.xticks(rotation=90)


#%%

# Heatmap to show "clustered" correlations

correlation_matrix = df.corr()

plt.figure(figsize=(20, 15))

heatmap = sns.heatmap(correlation_matrix, annot=False, cmap='coolwarm', linewidths=0.5)

plt.title('Correlation Matrix Heatmap')
plt.show()


# %%

# HEATMAP AGAINST ONLY THESE CATEGORIES


# Assuming df has 77 columns plus data_mpki, inst_mpki, and IPC
# Find all columns in the DataFrame excluding 'data_mpki', 'inst_mpki', and 'IPC'
categories = df.columns.difference(['data_mpki', 'inst_mpki', 'IPC'])

# Create a correlation matrix between categories and metrics
corr_matrix_data_mpki = df[categories].corrwith(df['data_mpki'])
corr_matrix_inst_mpki = df[categories].corrwith(df['inst_mpki'])
corr_matrix_ipc = df[categories].corrwith(df['IPC'])

# Create a figure
plt.figure(figsize=(12, 50))

# Plot heatmap for data_mpki correlation
plt.subplot(3, 1, 1)
sns.heatmap(pd.DataFrame(corr_matrix_data_mpki, columns=['Correlation with data_mpki']), annot=True, cmap='coolwarm')

# Plot heatmap for inst_mpki correlation
plt.subplot(3, 1, 2)
sns.heatmap(pd.DataFrame(corr_matrix_inst_mpki, columns=['Correlation with inst_mpki']), annot=True, cmap='coolwarm')

# Plot heatmap for IPC correlation
st.subheader('Correlation with IPC')
plt.subplot(3, 1, 3)
sns.heatmap(pd.DataFrame(corr_matrix_ipc, columns=['Correlation with IPC']), annot=True, cmap='coolwarm')

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the figure
plt.show()


#%%

# make tighter layout to avoid having super long page

# these are the remaining columns just to have them laid out.  

# for column in df.columns:
#     plt.figure()  
#     sns.barplot(x=df.index, y=df[column], color='blue', label = 'Barplot', alpha=0.2)
#     sns.lineplot(x=df.index, y=df[column], marker='o', color = 'purple', label = 'Line')
#     plt.title(column)  
#     plt.xlabel('Index')  
#     plt.ylabel('Values')  
#     plt.tight_layout()
#     plt.show()  