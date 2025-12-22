import subprocess
import os

def run_checkm(nome_arquivo_assembly, diretorio_saida):
    # Detecta extensão automaticamente
    ext = os.path.splitext(nome_arquivo_assembly)[1].replace(".", "")

    #Cria uma pasta dentro do diretorio_saida para os resultados do checkm2
    diretorio_saida_novo = os.path.join(diretorio_saida, "checkm2_results")
    os.makedirs(diretorio_saida_novo, exist_ok=True)

    comando_checkm = [
        "conda", "run", "-n", "checkm2", "checkm2", "predict",
        "-i", nome_arquivo_assembly,
        "-x", ext,
        "-o", diretorio_saida_novo
    ]

    print("Executando:", " ".join(comando_checkm))

    try:
        processo = subprocess.Popen(
            comando_checkm,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = processo.communicate()
        
        print("Execução do CheckM2 terminada. Salvando logs...")

        # Salva o stdout no arquivo .txt
        with open(os.path.join(diretorio_saida, "checkm2_output.txt"), "w") as outfile:
            outfile.write(stdout)
        
        # Salva o stderr (erros/avisos) em um arquivo separado
        if stderr:
            with open(os.path.join(diretorio_saida, "checkm2_error.txt"), "w") as errfile:
                errfile.write(stderr)

        if processo.returncode == 0:
            print(" Concluído com sucesso! Resultados do Quast salvos em:", diretorio_saida_novo)
        else:
            # Se o returncode não for 0, o Quast falhou!
            print(f"ERRO: Quast falhou com código de saída {processo.returncode}.")
            print("Por favor, verifique o arquivo 'Quast_error.txt' para detalhes.")
    except Exception as e:
        print("Erro ao executar o CheckM:", e)

