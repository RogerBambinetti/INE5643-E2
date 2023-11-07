import pandas as pd
import os.path

def main(yaml_c):
    print("-------------- Iniciando o transformador --------------")
    
    extract_path = yaml_c['extract_path']
    transform_path = yaml_c['transform_path']
    data_path = yaml_c['data_path']
    len_path = len(data_path)

    lst_all_data = []
    for roots, _, files in os.walk(extract_path):
        for file in files:
            if file != '.gitkeep' and os.path.splitext(file)[1] == '.csv':
                file_data = [roots + '\\' + file]
                lst_all_data.append(file_data)
    
    df_list_all_data = []
    for arquivo in lst_all_data:
        arquivo = arquivo[0].replace('\\\\', '\\')
        df = pd.read_table(f'{arquivo}', delimiter=';')
        df_list_all_data.append(df)
    df_all_data = pd.concat(df_list_all_data, ignore_index=True)
    
    if not df_all_data.empty:

        nm_colunas = {  'nome_loja': 'nm_loja',
                        'cidade_loja': 'nm_cidade',
                        'estado_loja': 'sg_estado',
                        'regiao': 'nm_regiao',
                        'nome_produto': 'nm_produto',
                        'subcategoria_produto': 'nm_subcategoria',
                        'categoria_produto': 'nm_categoria',
                        'departamento_produto': 'nm_departamento',
                        'nome_promocao': 'nm_promocao',
                        'tipo_reducao_preco': 'de_tipo_reducao_preco',
                        'veiculo_divulgacao': 'de_veiculo_divulgacao',
                        'tipo_display': 'de_tipo_display',
                        'data': 'dt_compra',
                        'dia': 'dt_dia',
                        'dia_da_semana': 'nm_dia_da_semana',
                        'mes': 'dt_mes',
                        'ano': 'dt_ano',
                        'semestre': 'dt_semestre',
                        'flag_feriado': 'fl_feriado',
                        'total_vendas': 'vl_total_vendas',
                        'units_old': 'qtd_unidades_antigas',
                        'unidades_vendidas': 'qtd_unidades_vendidas',
                        'total_custo': 'vl_total_custo',
                        'quantidade_clientes': 'qtd_clientes'
                        }
        
        df_all_data['data'] = pd.to_datetime(df_all_data['data'])

        df_all_data['dia'] = df_all_data['data'].dt.strftime('%d')
        df_all_data['mes'] = df_all_data['data'].dt.strftime('%m')
        df_all_data['semestre'] = df_all_data['data'].dt.quarter
        
        df_all_data['concat_data'] = (df_all_data['ano']).astype(str) + '-' + (df_all_data['mes']).astype(str) + '-' + (df_all_data['dia']).astype(str)
        df_all_data['data'] = pd.to_datetime(df_all_data['concat_data'])
        
        df_all_data.drop(columns=['mês_ano', 'concat_data'], inplace=True)
 
        df_all_data = df_all_data.rename(columns = nm_colunas)
        
        df_all_data = df_all_data.groupby(['nm_loja', 'nm_cidade', 'sg_estado', 'nm_regiao', 'nm_produto', 'nm_subcategoria', 'nm_categoria', 'nm_departamento', 'nm_promocao', 'de_tipo_reducao_preco', 'de_veiculo_divulgacao', 'de_tipo_display', 'dt_compra', 'nm_dia_da_semana', 'dt_mes', 'dt_ano', 'fl_feriado', 'dt_dia', 'dt_semestre'])\
                        .agg({  'vl_total_vendas': 'sum',
                                'qtd_unidades_antigas': 'sum',
                                'qtd_unidades_vendidas': 'sum',
                                'vl_total_custo': 'sum',
                                'qtd_clientes': 'sum',}) \
                        .reset_index()
                        
        df_all_data['fl_feriado'] = df_all_data['fl_feriado'].replace({'N': 'Não', 'Y': 'Sim'}).fillna('NI')
        
        df_all_data['nm_pais'] = 'Brasil'
        
        folder_path = f'{transform_path}/stg_vendas.csv'
        df_all_data.to_csv(f'{folder_path}', index=False, encoding='utf-8-sig', sep=';')
        print(f'Arquivo "stg_vendas" carregado a pasta "{transform_path}".')
        
    else: 
        print(f'Sem arquivos para transformar.')