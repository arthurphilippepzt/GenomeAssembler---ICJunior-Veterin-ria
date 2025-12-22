import subprocess
import os

def run_prokka(diretorio_saida):
    # Converte para caminho absoluto para evitar erros de localização
    diretorio_saida = os.path.abspath(diretorio_saida)
    # Cria o diretório se ele ainda não existir
    if not os.path.exists(diretorio_saida):
        os.makedirs(diretorio_saida)
        print(f"Diretório criado: {diretorio_saida}")

    comando_prokka = [
        "conda", "run", "-n", "prokka", "bash", "run_prokka.sh", "-i", diretorio_saida
    ]


    print(f"Executando: {' '.join(comando_prokka)}")

    try:
        processo = subprocess.Popen(
            comando_prokka,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1 # Line buffered
        )

        stdout, stderr = processo.communicate()

        # Caminhos dos arquivos de log
        log_out = os.path.join(diretorio_saida, "autoprokka_output.txt")
        log_err = os.path.join(diretorio_saida, "autoprokka_error.txt")


        # Salvando logs
        with open(log_out, "w") as outfile:
            outfile.write(stdout)

        

        with open(log_err, "w") as errfile:
            errfile.write(stderr if stderr else "Nenhum erro reportado.")



        if processo.returncode == 0:
            print(f"Concluído! Logs salvos em: {diretorio_saida}")

        else:
            print(f"ERRO: Prokka falhou (Código {processo.returncode}). Verifique {log_err}")

    except Exception as e:
        print(f"Erro crítico ao executar o Prokka: {e}")
