#!/usr/bin/python3

# Utilizado para fazer a pesquisa
from google import google

# Utilizado para criar diretórios, executar comandos de terminal, e pegar nome do arquivo
import os

# Utilizado para utilizar os argumentos (args) passados
import sys

# Utilizado para pegar o conteúdo do arquivo
import requests

# Utilizado para pausar o programa em algumas situações
import time

# As extensões que serão pesquisadas por padrão
EXTENSOES_PADRAO = ['pdf', 'doc', 'docx', 'odt', 'ppt', 'xls', 'svg', 'txt']



BANNER = """                           ____   ___   ____    _    
                          |  _ \\ / _ \\ / ___|  / \\   
                          | |_) | | | | |     / _ \\  
                          |  __/| |_| | |___ / ___ \\ 
                          |_|    \\___/ \\____/_/   \\_\\                                                     
         __ _                                  _       _   _             
        / _(_)_ __   __ _  ___ _ __ _ __  _ __(_)_ __ | |_(_)_ __   __ _ 
       | |_| | '_ \\ / _` |/ _ \\ '__| '_ \\| '__| | '_ \\| __| | '_ \\ / _` |
       |  _| | | | | (_| |  __/ |  | |_) | |  | | | | | |_| | | | | (_| |
       |_| |_|_| |_|\\__, |\\___|_|  | .__/|_|  |_|_| |_|\\__|_|_| |_|\\__, |
                    |___/          |_|                             |___/                                                  

\t    Criada por Igor Costa Melo <igoracm@outlook.com>
    Ferramenta inspirada no FOCA (Fingerprinting Organizations with
    Collected Archives) para baixar arquivos de sites e extrair seus metadados.
"""

PASTA_ORIGINAIS = "_ARQUIVOS_ORIGINAIS/"
PASTA_METADADOS = "_METADADOS/"

# Para poder criar todas as pastas necessárias de forma segura
def criar_diretorio(d):
    try:
        os.mkdir(d)
        return True
    except FileExistsError:
        return True
    except:
        return False

def search(site, ext, num):
    # Texto que será pesquisado no Google
    # exemplo: "site:odebrecht.com.br ext:pdf"
    dork = "site:%s ext:%s" % (site, ext)

    # Arquivos que serão baixados
    to_download = []
    to_download_name = []

    # Cria pasta para os arquivos originais e metadados extraídos
    criar_diretorio(PASTA_ORIGINAIS)
    criar_diretorio(PASTA_METADADOS)

    # Realiza a pesquisa, com um limite de no máximo <num> resultados
    resultados = google.search(dork, num)[:num]

    # Mostrará 'PDF:' caso tenha encontrado pelo menos 1
    if len(resultados):
        print("\n" + ext.upper() + ":")
    
    # Pega o nome de cada PDF encontrado
    for res in resultados:
        url = res.link
        nome = os.path.basename(url)
        print("["+ext.upper()+"] " + nome)
        to_download.append(url)
        to_download_name.append(nome)

    for i in range(len(to_download)):
        # Baixa arquivo e salva na pasta de arquivos originais
        nome = to_download_name[i]
        print("* Baixando: " + nome)
        url = to_download[i]
        req = requests.get(url)
        open(PASTA_ORIGINAIS + nome, "wb").write(req.content)

        # Extrai os metadados e salva em um arquivo
        ## Para isso, transforma a saída do exiftool em um dict
        #di = {}
        exif = os.popen('exiftool %s > %s.meta' % 
        	(PASTA_ORIGINAIS + nome, PASTA_METADADOS + nome)).read()

    print()

# Mensagem de ajuda básica
def help():
    print("UTILIZAÇÃO:")
    print("  ./poca.py <domínio> [máx.] [extensão(ões)]")
    print("  ./poca.py <-g> [-S|-N]")
    print()

    print("OBS.:")
    print("   - O 2º argumento é o número máximo de arquivos que ele irá baixar POR FORMATO.")
    print("   - As extensões, se passadas como 3º argumento, devem ser separadas por vírgulas e sem espaço.")
    print()

    print("EXEMPLOS:")
    print("  ./poca.py odebrecht.com.br")
    print("  ./poca.py mec.gov.br 2")
    print("  ./poca.py lelivros.love 100 pdf")
    print("  ./poca.py ufrj.br 100 pdf,doc,xls")
    print("  ./poca.py -g")
    print("  ./poca.py -g -N")

def check_grep():
    if '-g' in sys.argv:
        return True
    return False

# Verifica se a pessoa tem a ferramenta exiftool instalada
def check_exif():
    r = os.popen('exiftool 2> /dev/null').read()
    if r.startswith('Syntax:'):
        return True
    print('\n')
    print("[ERRO] Ferramenta exiftool não instalada.\n")
    print("Utilize o comando:")
    print("  sudo apt install exiftool -y")
    exit()

# Verifica se a pessoa digitou algum comando de help
def check_help():
    args = sys.argv
    if '-h' in args or '--help' in args:
        help()
        exit()

# Extrai o domínio do site dos argumentos, verificando a sintaxe
def get_dom():
    # Caso a pessoa não passe nenhum argumento
    if len(sys.argv) <= 1:
        help()
        exit() 

    # Caso pelo menos um argumento seja passado
    return sys.argv[1]

# Extrai o valor máximo dos argumentos
def get_max():
    # Valor máximo padrão   
    padrao = 5

    # Caso seja passado um segundo argumento, atribui esse ao valor de maxcount
    if len(sys.argv) >= 3:
        try:
            return int(sys.argv[2])

        # Caso não seja um número inteiro
        except ValueError:
            help()
            print('\n')
            #print('"' + comando + '"')
            print("[ERRO]: '%s' não é um inteiro válido." % sys.argv[2])
            exit()
    print()
    print("[AVISO] Valor máximo não especificado. Usando padrão %s." % padrao)
    return padrao

# Extrai as extensões a serem procuradas dos argumentos
def get_exts():
    # Se forem passadas extensões atráves do terceiro argumento
    if len(sys.argv) >= 4:
        return sys.argv[3].split(',')

    """# Caso tenha mais de 3 argumentos, o programa passa uma mensagem de erro e encerra
    elif len(sys.argv) > 4:
        help()
        print()
        print("[ERRO] As extensões devem ser separadas por vírgulas e sem espaço, como 3º argumento.")
        exit()
    """

    # Caso não for passada nenhuma extensão, utiliza as extensões padrão
    print()
    print("[AVISO] Utilizando extensões padrão: " + ' '.join(EXTENSOES_PADRAO))
    return EXTENSOES_PADRAO

def check_autoremove():
    if '-S' in sys.argv:
        return 's'
    if '-N' in sys.argv:
        return 'n'
    return False

# Gera arquivo com todos os metadados de todos os arquivos baixados
def gerar_final_meta():
    # Apaga o que tiver no arquivo __final_meta__, que guardará todos os metadados
    # Em seguida concatena os metadados de todos os arquivos '.meta' nele
    os.popen(
            "echo '' > __final_meta__; \
            for file in $(ls %s | grep .meta); do \
            cat %s$file >> __final_meta__; \
            done;" % (PASTA_METADADOS, PASTA_METADADOS)
    ).read()


if __name__ == '__main__':
    print(BANNER)
    time.sleep(1)

    # Identifica se o comando contém --help ou -h
    check_help()

    # Se o argumento '-g' for passado
    if not check_grep():

        # Verifica se a pessoa tem a ferramenta exiftool
        check_exif()

        # Deleta as pastas, caso já existam
        #os.system('rm ' + PASTA_ORIGINAIS + '*')
        #os.system('rm ' + PASTA_METADADOS + '*')

        # Utiliza valores passados por argumentos, se houverem
        # Trata automaticamente erros de sintaxe    
        dom = get_dom()
        maxcount = get_max()
        exts = get_exts() 

        print("Pesquisando...")

        # Pesquisa 'maxcount' arquivos de cada extensão
        for ext in exts:
            search(dom, ext, maxcount)

        # Gera arquivo com todos os metadados de todos os arquivos baixados
        gerar_final_meta()


    # Pergunta se usuário quer remover arquivos que não são mais necessários
    # 
    remover = check_autoremove()

    if not remover:
        print("[AVISO] Metadados extraídos e salvos em um arquivo __final_meta__.")
        remover = input("Remover arquivos não mais necessários (PDFs e .meta)? [s|n]: ")
        print()

    # Remove as duas pastas geradas
    if remover.lower() == 's':
        os.system('rm -r ' + PASTA_ORIGINAIS + ' && rm -r ' + PASTA_METADADOS)


    # Pausa o programa para dar tempo do usuário ler
    time.sleep(.5)

    # Mostra as opções grep-áveis disponíveis
    print("\n\n----------------- OPÇÕES -----------------")
    # Pausa o programa para dar tempo do usuário ler
    time.sleep(.3)
    os.system("cat __final_meta__ | cut -d ':' -f 1 | sort -u | sort")

    # Pausa o programa para dar tempo do usuário ler
    time.sleep(.5)
    print()


    # Pede para o usuário digitar o termo que quer dar grep
    while True:
        grep = input("palavra para dar grep [ou '_sair']: ")
        if grep == "_sair":
            break 

        r = os.popen("grep '%s' __final_meta__ | sort | uniq -c | sort -n" % grep).read()
        print(r)


    # Caso o usuário queira remover o arquivo de metadados
    remover = input("Apagar metadados extraídos (arquivo __final_meta__)? [s|n]: ")
    if remover.lower() == 's':
        os.system('rm __final_meta__')
