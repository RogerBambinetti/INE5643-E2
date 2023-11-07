import extract
import transform
import load
from functions import yaml_config

def main():
    print('--------------------------------------------------------')
    print('------------------- Iniciando o main -------------------')
    print('--------------------------------------------------------')
    
    yaml_c = yaml_config()

    extract.main(yaml_c)
    transform.main(yaml_c)
    load.main(yaml_c)

if __name__=='__main__':
    main()
