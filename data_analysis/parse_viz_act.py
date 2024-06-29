# %%

# quick and dirty change? 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os

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
'''
import pandas as pd
import seaborn as sns
import re
import os

# standard count of files in the folder. 
def count_files_in_directory(directory_path):
    try:
        # List all the files and directories in the given directory
        items = os.listdir(directory_path)

        # Filter out directories, keeping only files
        folders = [item for item in items if os.path.isdir(os.path.join(directory_path, item))]
        
        # Return the number of files
        return len(folders)
    
    except FileNotFoundError:
        return 0
    except Exception as e:
        return 0


# The function needs to be used two times: once to parse the outer layer of param files, and once 
# to parse the inner layer. 

# First order of the function. 
directory_path = 'C:\stats_research\llm-for-cpu\data_analysis\params'
file_count = count_files_in_directory(directory_path)

print(f"The file count of the exterior is  {file_count}")

#-----------------------------------------------------------

# Dictionary to hold the data
data = {}


for i in range(0, file_count):
    file_path = f'C:\stats_research\llm-for-cpu\data_analysis\params_g/params_100k_{i}/stats.txt'
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Grabbing keys to use in the dictionary
        for line in lines:
            parts = line.split()
            
            if len(parts) < 2:
                continue
            
            key = parts[0]
            
            # This giant if statment checks if there is an instruction or some other specific 
            # columns for the new variables that'll be calculated later on. 
            # This variable list may change depending on what we're looking at (including if we just want to focus on DRAM for instance)
            # "data" in key) or ("Data" in key)

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

df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in data.items()]))

print(df.head())
'''

#%%
# # because there is no need for more padding (seems like every value is covered), check for missing values and remove/fill them?
# df.fillna(0, inplace=True)
# # df = df.drop(df.columns[0], axis=1)
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


#%%

df.to_csv("review.csv", sep=',', index=False)
df.head()

#%%

# most important graphs are here regarding those new variables.
# I think kde plots are cool for showing concentrations but idk how they'll be at the moment. 
'''
columns = ['data_mpki', 'inst_mpki', 'IPC']
for column in columns:
    plt.figure()  
    sns.barplot(x=df.index, y=df[column], color='blue', label = 'Barplot', alpha=0.2)
    sns.lineplot(x=df.index, y=df[column], marker='o', color = 'purple', label = 'Line')
    plt.title(column)  
    plt.xlabel('Index')  
    plt.ylabel('Values')  
    plt.tight_layout()
    plt.show()  
'''

# %% 
'''
# Zoomed in plots like last time.

fig, axes = plt.subplots(nrows = 1, ncols = 3, figsize = (18,5))

# ------------- data_mpki -------------

# sns.barplot(ax=axes[0], x = df.index, y = df['data_mpki'], color = 'blue', label = 'Barplot', alpha = 0.2)
sns.scatterplot(ax = axes[0], x=df.index, y = df['data_mpki'], marker = 'o', color = 'purple', label = 'Line')
axes[0].set_ylim(1.6398e6, 1.645e6)
axes[0].set_title('data_mpki')
axes[0].set_xlabel('Index')
axes[0].set_ylabel('Values')

# ------------- inst_mpki -------------

plt.figure()
# sns.barplot(ax=axes[1], x = df.index, y = df['inst_mpki'], color = 'blue', label = 'Barplot', alpha = 0.2)
sns.scatterplot(ax = axes[1], x=df.index, y = df['inst_mpki'], marker = 'o', color = 'purple', label = 'Line')
axes[1].set_ylim(0.0013050, 0.00132)
axes[1].set_title('inst_mpki')
axes[1].set_xlabel('Index')
axes[1].set_ylabel('Values')

# ------------- IPC -------------

plt.figure()
# sns.barplot(ax=axes[2], x = df.index, y = df['IPC'], color = 'blue', label = 'Barplot', alpha = 0.2)
sns.scatterplot(ax=axes[2], x=df.index, y = df['IPC'], marker = 'o', color = 'purple', label = 'Line')
axes[2].set_ylim(0.01200, 0.01204)
axes[2].set_title('IPC')
axes[2].set_xlabel('Index')
axes[2].set_ylabel('Values')

# adjusting the main layout
plt.tight_layout()
plt.show()

'''
# %%


# orignial metrics

fig, axes = plt.subplots(nrows = 1, ncols = 3, figsize = (18,5))

# ------------- data_mpki -------------

# sns.barplot(ax=axes[0], x = df.index, y = df['data_mpki'], color = 'blue', label = 'Barplot', alpha = 0.2)
sns.scatterplot(ax = axes[0], x=df.index, y = df['data_mpki'], marker = 'o', color = 'purple', label = 'Line')
# axes[0].set_ylim(1.6398e6, 1.645e6)
axes[0].set_title('data_mpki')
axes[0].set_xlabel('Index')
axes[0].set_ylabel('Values')

# ------------- inst_mpki -------------

plt.figure()
# sns.barplot(ax=axes[1], x = df.index, y = df['inst_mpki'], color = 'blue', label = 'Barplot', alpha = 0.2)
sns.scatterplot(ax = axes[1], x=df.index, y = df['inst_mpki'], marker = 'o', color = 'purple', label = 'Line')
# axes[1].set_ylim(0.0013050, 0.00132)
axes[1].set_title('inst_mpki')
axes[1].set_xlabel('Index')
axes[1].set_ylabel('Values')

# ------------- IPC -------------

plt.figure()
# sns.barplot(ax=axes[2], x = df.index, y = df['IPC'], color = 'blue', label = 'Barplot', alpha = 0.2)
sns.scatterplot(ax=axes[2], x=df.index, y = df['IPC'], marker = 'o', color = 'purple', label = 'Line')
# axes[2].set_ylim(0.01200, 0.01204)
axes[2].set_title('IPC')
axes[2].set_xlabel('Index')
axes[2].set_ylabel('Values')

# adjusting the main layout
plt.tight_layout()
plt.show()


# %% 

fig, axes = plt.subplots(nrows = 1, ncols = 3, figsize = (18,5))

# ------------- data_mpki -------------

sns.kdeplot(ax = axes[0], x=df.index, y = df['data_mpki'], color = 'purple', shade = True, label = 'Line')
# axes[0].set_ylim(1.6398e6, 1.645e6)
axes[0].set_title('data_mpki')
axes[0].set_xlabel('Index')
axes[0].set_ylabel('Values')

# ------------- inst_mpki -------------

plt.figure()
sns.kdeplot(ax = axes[1], x=df.index, y = df['inst_mpki'],color = 'purple', shade = True, label = 'Line')
# axes[1].set_ylim(0.0013050, 0.00132)
axes[1].set_title('inst_mpki')
axes[1].set_xlabel('Index')
axes[1].set_ylabel('Values')

# ------------- IPC -------------

plt.figure()
sns.kdeplot(ax=axes[2], x=df.index, y = df['IPC'], color = 'purple', shade = True, label = 'Line')
# axes[2].set_ylim(0.01200, 0.01204)
axes[2].set_title('IPC')
axes[2].set_xlabel('Index')
axes[2].set_ylabel('Values')

# adjusting the main layout
plt.tight_layout()
plt.show()




# %%









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

# just a quick and dirty pie chart to get an idea of the highest values right now 

mean_values = df.mean()

plt.figure(figsize=(10,6))

plt.pie(mean_values, labels=mean_values.index, autopct='%1.1f%%', startangle=140);


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
plt.subplot(3, 1, 3)
sns.heatmap(pd.DataFrame(corr_matrix_ipc, columns=['Correlation with IPC']), annot=True, cmap='coolwarm')

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the figure
plt.show()



# %%

# looking into more data viz 





#%%

# make tighter layout to avoid having super long page

# these are the remaining columns just to have them laid out.  

for column in df.columns:
    plt.figure()  
    sns.barplot(x=df.index, y=df[column], color='blue', label = 'Barplot', alpha=0.2)
    sns.lineplot(x=df.index, y=df[column], marker='o', color = 'purple', label = 'Line')
    plt.title(column)  
    plt.xlabel('Index')  
    plt.ylabel('Values')  
    plt.tight_layout()
    plt.show()  