# coding: utf-8


# In[2]:

import numpy as np
import time, datetime
import paramiko
from logcontrol import log_control
import csv
from datetime import timedelta
import mas_utils as utils
import configs
from start_project import initialize
class InputError(Exception):
    def __init__(self, message):
        self.message = message


# ### Processa os arquivos e os transforma em .csv

# In[11]:


def process_set(data, date_start, date_end, dt=None):

    if(dt is None):
        dt = (date_end - date_start).total_seconds() / len(data)
        delta = datetime.timedelta(seconds=dt)

    date = date_start
    result = []
    for row in data:
        #pdb.set_trace()
        result.append([date]+row)
        date += dt
    return result

def process_file_data(data, start_index, dt=None):
    server_name = None
    processed_data = []
    temp_process = None
    actual_date = None
    index = start_index
    date_diff = None
    header = None
    while(index < len(data)):
        if(data[index].strip().lower().startswith('procs')):# == PATTERN_01):
            index += 1
        elif(data[index].strip().lower().split()[0:2] == ['r', 'b']):#melhorar isso
            header = data[index].strip().lower()
            index += 1
        elif(len(data[index].split()) >= 15): # para considerar os diferentes tipos
            d = data[index].split()
            temp_process.append(d)
            index += 1
        elif(len(data[index].split()) == 3):
            # verificar parada e break
            name, date, d_time = data[index].split()

            date = datetime.datetime.strptime('{} {}'.format(date, d_time),
                           "%Y-%m-%d %H:%M:%S")
            if(server_name == None):
                server_name = name.strip().lower()
            elif(server_name != name.strip().lower()):
                raise InputError('{} not equal to {}'.format(name, server_name))
                return None

            if(temp_process is not None):
                processed_data += process_set(temp_process, actual_date, date, dt)
                date_diff = date - actual_date
                temp_process = []
            else:
                temp_process = []
            actual_date = date

            index +=1
        else:
            raise InputError('error|{}|line {}'.format(data[index], index))
            return None

    if(temp_process is not None):
                processed_data += process_set(temp_process, actual_date, actual_date + date_diff, dt)
    return processed_data, header


# In[4]:

def audit_processed_file(data):
    init = data[0][0]
    end  = data[-1][0]
    # deve ser alterada caso a periodo de amostragem seja diferente de 15
    if(init.hour == 0 and init.minute == 0 and init.second >= 1 and
        end.hour == 23 and end.minute == 59 and end.second >= 46):
        # deve ser alterada caso a periodo de amostragem seja diferente de 15
        expected = int(60*60*24  / 15)
        if(len(data) != expected):
            return False, "esperado {} registros, encontrado {}".format(expected, len(data))
        else:
            return True, "OK"
    else:
        return False, "init: {} end:{} incorretos".format(init, end)

def __write_log__(status, message, file_name):
    update_row = {
        'name': utils.path_leaf(file_name.strip() + '.tar.bz'),
        'downloaded' : True,
        'processed' : True,
        'correct': status,
        'comments' : "".join(message)
    }
    log_control.update_file(update_row)

def regularize_data(row, header):
    us = float(row[header.index('us')])
    sy = float(row[header.index('sy')])
    id_ = float(row[header.index('id')])

    if(us > 1.0 or sy > 1.0 or id_> 1.0):
        us = us/100.0
        sy = sy/100.0
        id_= id_/100.0

        row[header.index('us')] = us
        row[header.index('sy')] = sy
        row[header.index('id')] = id_

    return row

def process_file(file_name, dt=datetime.timedelta(seconds=15)):
    data = None
    with open(file_name, 'r', encoding='utf-8') as infile:
        data = infile.readlines()
        try:
            result, header = process_file_data(data, 0, dt)

            fstatus, fmessage =  audit_processed_file(result)
            __write_log__(fstatus, fmessage, file_name)
            if(not fstatus):
                print(file_name, 'problem', fmessage)
                return

            result_file_name = configs.csv_dir + file_name.split('/')[-1]+'.csv'
            with open(result_file_name,'w+') as resultFile:
                wr = csv.writer(resultFile, dialect='excel')
                header = ['time'] + header.split()
                wr.writerow(header)
                for row in result:
                    row = regularize_data(row, header)
                    wr.writerow(row)
            print(result_file_name, ' escrito')
        except InputError as error:
            __write_log__(False, 'problemas no arquivo ~ {}'.format(error.message), file_name)


# In[9]:

def download_files_from_server():
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=configs.hostname,
                       username=configs.username,
                       password=configs.password)
    ftp_client=ssh_client.open_sftp()

    # get list of files from server
    server_file_list = ftp_client.listdir(configs.remote_dir)
    # compare to downloaded list of files

    downloaded_list = log_control.get_all_files()

    files_to_download = set(server_file_list).difference(downloaded_list)
    print("{} novos arquivos encontrados no servidor".format(len(files_to_download)))
    if(len(files_to_download) == 0):
        return

    # download files needed
    utils.download_files(ftp_client, configs.remote_dir,
                         configs.original_DIR, files_to_download)
    print("{} novos arquivos baixados".format(len(files_to_download)))
    print("extraindo arquivos baixados")
    utils.extract_files(configs.original_DIR,
                        configs.extracted_DIR,
                        files_to_download)

    for file in files_to_download:
        log_control.insert_file(
            {
                'name': file.strip(),
                'downloaded' : True,
                'processed' : False,
                'correct': False,
                'comments' : "Downloaded"
            })
    print("extração completa")

def process_files():
    # get list of downloaded files

    files_to_process = log_control.get_unprocessed_files()
    print("{} novos arquivos para processar".format(len(files_to_process)))
    if(len(files_to_process) == 0):
        return

    count = 1
    for file in files_to_process:
        print('processing', file, '{}/{}'.format(count, len(files_to_process)))
        process_file(configs.extracted_DIR + file.replace('.tar.bz', ''))

        count += 1
    print("novos arquivos processados")


# In[7]:

if __name__ == "__main__":
    initialize()
    print("fase 01")
    download_files_from_server()
    process_files()
    print("fase 01 completa")
