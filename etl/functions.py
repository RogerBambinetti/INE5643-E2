import os.path
import yaml

def yaml_config():
    current_directory = os.path.abspath(os.path.dirname(__file__))
    project_directory = os.path.abspath(current_directory + '\\..\\') + '\\'

    with open(f'{project_directory}config\\config.yaml') as file:
        config = yaml.safe_load(file)

    return {
        'project_directory': project_directory
        ,'project_name': config['project-name']
        ,'data_path': project_directory + config['data-path']
        ,'original_path': project_directory + config['data-path'] + config['original-path']
        ,'extract_path': project_directory + config['data-path'] + config['extract-path']
        ,'transform_path': project_directory + config['data-path'] + config['transform-path']
        ,'load_path': project_directory + config['data-path'] + config['load-path']
    }
