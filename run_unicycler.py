import subprocess
import os
import time
# Não precisamos mais de 'threading' ou 'tkinter' neste arquivo

def run_unicycler(filename1, filename2, filename3, output_dir, number_of_files):
    """
    Executa o Unicycler, captura a saída de forma segura, espera o término
    e então verifica os arquivos de resultado.
    """

    # Vefica quantos arquivos foram selecionados
    if number_of_files == 3:
        comando = [
            "conda", "run", "-n", "unicycler", "unicycler", 
            "-1", filename1, "-2", filename2, "-l", filename3, "-o", output_dir
        ]
    elif number_of_files == 2:
        comando = [
            "conda", "run", "-n", "unicycler", "unicycler", 
            "-1", filename1, "-2", filename2, "-o", output_dir
        ]
    else:
        comando = [
            "conda", "run", "-n", "unicycler", "unicycler", 
            "-l", filename3, "-o", output_dir
        ]
        
    try:
        process = subprocess.Popen(
            comando, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
            
        print("Iniciando Unicycler... Isso pode levar muito tempo.")
        
        # --- ETAPA 1: Capturando a saída (Corrigindo o bug do TXT) ---
        
        # process.communicate() espera o processo terminar e coleta
        # TODO o stdout e stderr de forma segura, evitando deadlocks.
        stdout_data, stderr_data = process.communicate()
        
        print("Execução do Unicycler terminada. Salvando logs...")

        # Salva o stdout no arquivo .txt
        with open(os.path.join(output_dir, "unicycler_output.txt"), "w") as outfile:
            outfile.write(stdout_data)
        
        # Salva o stderr (erros/avisos) em um arquivo separado
        if stderr_data:
            with open(os.path.join(output_dir, "unicycler_error.txt"), "w") as errfile:
                errfile.write(stderr_data)

        # --- ETAPA 2: Lógica do "check_completion" ---
        
        # Agora que 'communicate()' terminou, o processo ACABOU.
        # Podemos verificar o resultado.
        
        # Verificamos se o processo deu certo (código de saída 0)
        if process.returncode == 0:
            assembly_file = os.path.join(output_dir, "assembly.fasta")
            
            if os.path.exists(assembly_file):
                print("Concluído com sucesso! Arquivo assembly.fasta criado.") 

                    #Renomeia o arquivo assembly.fasta para incluir o nome do diretório de saída/nome do genoma
                new_assembly_file = os.path.join(output_dir, f"assembly_{os.path.basename(output_dir)}.fasta")
                os.rename(assembly_file, new_assembly_file)
                
                print(f"Arquivo renomeado para: {new_assembly_file}")
            else:
                print("Processo terminado com sucesso, mas assembly.fasta não foi encontrado.") 
        
        else:
            # Se o returncode não for 0, o Unicycler falhou!
            print(f"ERRO: Unicycler falhou com código de saída {process.returncode}.")
            print("Por favor, verifique o arquivo 'unicycler_error.txt' para detalhes.")
                       
    except Exception as e:
        print(f"Erro ao tentar executar o processo Unicycler: {str(e)}")