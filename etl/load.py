import pandas as pd
import os.path

def main(yaml_c):
    print("-------------- Iniciando o load --------------")
    
    transform_path = yaml_c['transform_path']
    load_path = yaml_c['load_path']
    
    lst_all_data = []
    for roots, _, files in os.walk(transform_path):
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
        dim_loja = df_all_data[['nm_loja', 'nm_cidade', 'sg_estado', 'nm_regiao', 'nm_pais']].drop_duplicates()
        dim_loja['sk_loja'] = range(1, len(dim_loja) + 1)

        dim_produto = df_all_data[['nm_produto', 'nm_subcategoria', 'nm_categoria', 'nm_departamento']].drop_duplicates()
        dim_produto['sk_produto'] = range(1, len(dim_produto) + 1)

        dim_calendario = df_all_data[['dt_compra', 'nm_dia_da_semana', 'dt_dia', 'dt_mes', 'dt_semestre', 'dt_ano', 'fl_feriado']].drop_duplicates()
        dim_calendario['sk_calendario'] = range(1, len(dim_calendario) + 1)

        dim_divulgacao = df_all_data[['nm_promocao', 'de_tipo_reducao_preco', 'de_veiculo_divulgacao', 'de_tipo_display']].drop_duplicates()
        dim_divulgacao['sk_divulgacao'] = range(1, len(dim_divulgacao) + 1)

        fato_vendas = df_all_data.merge(dim_loja, on=['nm_loja', 'nm_cidade', 'sg_estado', 'nm_regiao', 'nm_pais'])
        fato_vendas.drop(columns=['nm_loja', 'nm_cidade', 'sg_estado', 'nm_regiao', 'nm_pais'], inplace=True)
        fato_vendas = fato_vendas.merge(dim_produto, on=['nm_produto', 'nm_subcategoria', 'nm_categoria', 'nm_departamento'])
        fato_vendas.drop(columns=['nm_produto', 'nm_subcategoria', 'nm_categoria', 'nm_departamento'], inplace=True)
        fato_vendas = fato_vendas.merge(dim_calendario, on=['dt_compra', 'nm_dia_da_semana', 'dt_dia', 'dt_mes', 'dt_semestre', 'dt_ano', 'fl_feriado'])
        fato_vendas.drop(columns=['dt_compra', 'nm_dia_da_semana', 'dt_dia', 'dt_mes', 'dt_semestre', 'dt_ano', 'fl_feriado'], inplace=True)
        fato_vendas = fato_vendas.merge(dim_divulgacao, on=['nm_promocao', 'de_tipo_reducao_preco', 'de_veiculo_divulgacao', 'de_tipo_display'])
        fato_vendas.drop(columns=['nm_promocao', 'de_tipo_reducao_preco', 'de_veiculo_divulgacao', 'de_tipo_display'], inplace=True)

        files_to_save = {
                'dim_loja': {'name': 'dim_loja', 'df': dim_loja},
                'dim_produto': {'name': 'dim_produto', 'df': dim_produto},
                'dim_calendario': {'name': 'dim_calendario', 'df': dim_calendario},
                'dim_divulgacao': {'name': 'dim_divulgacao', 'df': dim_divulgacao},
                'fato_vendas': {'name': 'fato_vendas', 'df': fato_vendas}}

        for file in files_to_save:
            folder_path = f'{load_path}/{file}.csv'
            files_to_save[file]['df'].to_csv(f'{folder_path}', index=False, encoding='utf-8-sig', sep=';')
            print(f'Arquivo "{file}" carregado a pasta "{load_path}".')
        
    else: 
        print(f'Sem arquivos para transformar.')
