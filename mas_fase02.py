# coding: utf-8

import pandas as pd
import dataset
import configs
import database
from logcontrol import log_control


# In[ ]:

def gen_statistics(file_name, num_agrupate):
    df = pd.read_csv(file_name)
    df['time'] = pd.to_datetime(df['time'])
    df.rename(index=str, columns={"livre": "free"})

    fields = set(df.columns)
    fields.remove('time')

    aggregations = {
        'time': {
            'min_date': 'min',
            'max_date': 'max'}}

    # import pdb;pdb.set_trace()
    for field in ['r', 'us', 'sy', 'id']:
        aggregations[field] = {
            # 'min': 'min',
            'avg': 'mean',
            'max': 'max',
            'p90': lambda x : x.quantile(0.9)
        }

    df = df.groupby(df.index // num_agrupate).agg(aggregations)
    df.columns = ["_".join(x) for x in df.columns.ravel()]
    return df

def import_to_bd(num_agrupate):
    imported_list = list(log_control.get_not_imported_files())
    files_set = set([x.strip().replace('.tar.bz','') for x in imported_list])

    print("{} novos arquivos para importar".format(len(files_set)))
    if(len(files_set)==0):
        return

    table = database.db['server_statistics']
    count = 1
    for file in files_set:
        server_name = file[0:file.find('_stats')]
        statistics = gen_statistics(configs.csv_dir+file+".csv", num_agrupate)#, num_agrupate)

        statistics = statistics.to_dict(orient='split')

        columns = statistics['columns']
        values  = statistics['data']
        rows = []
        for value in values:
                row = dict(zip(columns, value))
                row['server'] = server_name
                row['agregation'] = num_agrupate
                rows.append(row)
        table.insert_many(rows)
        log_control.check_as_imported(file+'.tar.bz')
        print("{} importado para o banco {}/{}".format(file, count, len(files_set)))
        count +=1


# In[ ]:

if __name__ == "__main__":
    print("fase 02")
    s = import_to_bd(60)
    print("fase 02 concluída")
