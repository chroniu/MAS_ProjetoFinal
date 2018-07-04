
# coding: utf-8

# In[1]:

get_ipython().magic(u'load_ext autoreload')
get_ipython().magic(u'autoreload 2')


# In[2]:

import pandas as pd
import dataset
import configs
import database


# In[ ]:

def gen_statistics(file_name, num_agrupate):
    df = pd.read_csv(configs.csv_dir + 'mrburns_stats-20140801.csv')
    df['time'] = pd.to_datetime(df['time'])
    df.rename(index=str, columns={"livre": "free"})

    fields = set(df.columns)
    fields.remove('time')

    aggregations = {
        'time': {    
            'min_date': 'min',
            'max_date': 'max'}}


    for field in fields:
        aggregations[field] = { 
            'min': 'min',
            'avg': 'mean', 
            'max': 'max',
            'p90': lambda x : x.quantile(0.9)
        }

    df = df.groupby(df.index // num_agrupate).agg(aggregations)
    df.columns = ["_".join(x) for x in df.columns.ravel()]
    return df

def import_to_bd(num_agrupate, imported_file):
    with open(imported_file, 'r', encoding='utf-8') as infile:
        imported_list = infile.readlines()
    imported_list = [x.strip() for x in imported_list]
    
    with open(configs.processed_files, 'r', encoding='utf-8') as infile:
        processed_list = infile.readlines()
    processed_list = [x.strip() for x in processed_list]

    files_set = set(processed_list).difference(set(imported_list))
    print("{} novos arquivos para importar".format(len(files_set)))
    if(len(files_set)==0):
        return
    
    imported_files = open(imported_file, 'a+', encoding='utf-8')

    table = database.db['server_statistics']
    for file in files_set:
        server_name = file[0:file.find('_stats')]
        statistics = gen_statistics(configs.csv_dir+file+".csv", num_agrupate)
    
        statistics = statistics.to_dict(orient='split')

        columns = statistics['columns']
        values  = statistics['data']
        for value in values:
                row = dict(zip(columns, value))
                row['server'] = server_name
                row['agregation'] = num_agrupate
                table.insert(row)
                imported_files.write(file)
        print("{} importado para o banco".format(file))
    imported_files.close()


# In[ ]:

print("fase 02")
s = import_to_bd(60, configs.imported_files_60)
print("fase 02 concluída")      


# In[ ]:


    


# In[ ]:



