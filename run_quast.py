import subprocess
import os

def run_quast(nome_arquivo_assembly, diretorio_saida, arquivo_referencia=None):
    try:
        subprocess.run(
            ["conda", "run", "-n", "quast", "quast", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(" QUAST encontrado.")
    except Exception as e:
        print(" Erro ao verificar versão do QUAST:", e)
        return

    caminho = os.path.abspath(os.path.join(diretorio_saida, nome_arquivo_assembly))
    saida_quast = os.path.join(diretorio_saida, "quast_results")

    comando_quast = [
        "conda", "run", "-n", "quast",
        "quast", caminho, "-o", saida_quast
    ]

    if arquivo_referencia and os.path.isfile(arquivo_referencia):
        comando_quast.extend(["-r", arquivo_referencia])

    print(" Comando a ser executado:")
    print(" ".join(comando_quast))

    try:
        processo = subprocess.Popen(
            comando_quast,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = processo.communicate()

        print("Execução do Quast terminada. Salvando logs...")

        # Salva o stdout no arquivo .txt
        with open(os.path.join(diretorio_saida, "quast_output.txt"), "w") as outfile:
            outfile.write(stdout)
        
        # Salva o stderr (erros/avisos) em um arquivo separado
        if stderr:
            with open(os.path.join(diretorio_saida, "quast_error.txt"), "w") as errfile:
                errfile.write(stderr)

        if processo.returncode == 0:
            print(" Concluído com sucesso! Resultados do Quast salvos em:", saida_quast)
        else:
            # Se o returncode não for 0, o Quast falhou!
            print(f"ERRO: Quast falhou com código de saída {processo.returncode}.")
            print("Por favor, verifique o arquivo 'Quast_error.txt' para detalhes.")

    except Exception as e:
        print(" Erro ao executar o QUAST:", e)
