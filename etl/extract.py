import pandas as pd
import os.path

def main(yaml_c):
    print("-------------- Iniciando o extrator --------------")
     
    original_path = yaml_c['original_path']
    extract_path = yaml_c['extract_path']
    data_path = yaml_c['data_path']
    len_path = len(data_path)

    lst_all_data = []
    for roots, dirs, files in os.walk(original_path):
        for file in files:
            lst_root = roots[len_path:].split('\\')
            if len(lst_root) < 2:
                lst_root.append(None)
            
            file_data = [roots + '\\' + file, os.path.splitext(file)[0], os.path.splitext(file)[1]]
            lst_all_data.append(file_data)
    
    df_all_data = pd.DataFrame(lst_all_data, columns = [ 'file_path', 'file_name', 'file_extension'])

    for index_num, lst_data in df_all_data.iterrows():
        df = pd.DataFrame()

        if lst_data[2] == '.xls':
            df = pd.read_excel(f"{lst_data[0]}", engine="xlrd")

        else:
            print(f"Arquivo {lst_data[0]} não encontrado")

        if not df.empty:
            folder_path = f'{extract_path}/{lst_data[1]}.csv'

            df.to_csv(f'{folder_path}', index=False, encoding='utf-8-sig', sep=';')

            print(f'Arquivo "{lst_data[1]}" carregado a pasta "{extract_path}".')

        else: 
            print(f'Arquivo {lst_data[1]} vazio, por tanto, não foi carregado.')
