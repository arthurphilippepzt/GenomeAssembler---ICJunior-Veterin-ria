import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading
from run_unicycler import run_unicycler
from run_quast import run_quast
from run_checkm import run_checkm
from run_prokka import run_prokka

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Genome Assembler")
        self.root.geometry("800x600")
        self.root.configure(bg='white')

        # arquivos
        self.filename1 = None
        self.filename2 = None
        self.filename3 = None
        self.reference_file = None
        self.assembly_file = None
        self.output_dir = None
        self.number_of_files = 0


        self.arquivo1 = False
        self.arquivo2 = False
        self.arquivo3 = False
        self.check_reference = False
        self.Diretorio_Saida = False
        self.check_assembly = False

        self.Abas()
        self.menu()
        self.create_widgets()
        self.labels()
        self.root.mainloop()



    def threading_run_unicycler(self):
        thread_unicycler = threading.Thread(
            target=run_unicycler,
            args=(self.filename1, self.filename2, self.filename3, self.output_dir, self.number_of_files)
        )
        thread_unicycler.start()

    def threading_run_quast(self):
        if not self.assembly_file:
            messagebox.showerror("Erro", "Selecione o arquivo de assembly primeiro.")
            return

        thread_quast = threading.Thread(
            target=run_quast,
            args=(self.assembly_file, self.output_dir, self.reference_file)
        )
        thread_quast.start()

    def threading_run_checkm(self):
        if not self.assembly_file:
            messagebox.showerror("Erro", "Selecione o arquivo de assembly primeiro.")
            return

        thread_checkm = threading.Thread(
            target=run_checkm,
            args=(self.assembly_file, self.output_dir)
        )
        thread_checkm.start()

    def threading_run_prokka(self):
        if not self.assembly_file:
            messagebox.showerror("Erro", "Selecione o arquivo de assembly primeiro.")
            return

        thread_prokka = threading.Thread(
            target=run_prokka,
            args=(self.output_dir,)
        )
        thread_prokka.start()



    def create_widgets(self):
        # Unicycler
        self.start_unicycler_button = tk.Button(self.aba2, text="Start Unicycler", command=self.threading_run_unicycler)
        self.start_unicycler_button.pack()
        self.start_unicycler_button.config(state=tk.DISABLED)

        # Quast
        self.start_quast_button = tk.Button(self.aba3, text="Start Quast", command=self.threading_run_quast) #butao para iniciar o quast 
        self.start_quast_button.pack()
        self.start_quast_button.config(state=tk.DISABLED)

        #CheckM
        self.start_checkm_button = tk.Button(self.aba4, text="Start CheckM", command=self.threading_run_checkm) 
        self.start_checkm_button.pack()
        self.start_checkm_button.config(state=tk.DISABLED)

        #Prokka
        self.start_prokka_button = tk.Button(self.aba5, text="Start AutoProkka", command=self.threading_run_prokka)
        self.start_prokka_button.pack()
        self.start_prokka_button.config(state=tk.DISABLED)



    def labels(self):
        self.label_file1 = tk.Label(self.aba1, text="File 1: None", bg='lightgray', fg='red')
        self.label_file1.pack(anchor='nw')

        self.label_file2 = tk.Label(self.aba1, text="File 2: None", bg='lightgray', fg='red')
        self.label_file2.pack(anchor='nw')

        self.label_file3 = tk.Label(self.aba1, text="File 3: None", bg='lightgray', fg='red')
        self.label_file3.pack(anchor='nw')

        self.label_reference = tk.Label(self.aba1, text="Reference File: None", bg='lightgray', fg='red')
        self.label_reference.pack(anchor='nw')

        self.label_assembly = tk.Label(self.aba1, text="Assembly File: None", bg='lightgray', fg='red')
        self.label_assembly.pack(anchor='nw')

        self.label_output = tk.Label(self.aba1, text="Output Directory: None", bg='lightgray', fg='red')
        self.label_output.pack(anchor='nw')



    def menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="Select File 1", command=self.select_file1)
        file_menu.add_command(label="Select File 2", command=self.select_file2)
        file_menu.add_command(label="Select File 3", command=self.select_file3)

        file_menu.add_command(label="Select Reference File", command=self.select_reference_file)
        file_menu.add_command(label="Select Assembly File", command=self.select_assembly_file)

        file_menu.add_command(label="Make Output Directory", command=self.make_output_dir)
        file_menu.add_command(label="Select Output Directory", command=self.select_output_dir)

        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Info Files", command=self.show_infos)



    def Abas(self):
        self.abas_infos = ttk.Notebook(self.root)

        self.aba1 = tk.Frame(self.abas_infos)
        self.aba1.config(bg='lightgray')
        self.abas_infos.add(self.aba1, text="Files Info")

        self.aba2 = tk.Frame(self.abas_infos)
        self.aba2.config(bg='lightgray')
        self.abas_infos.add(self.aba2, text="Unicycler Info")

        self.aba3 = tk.Frame(self.abas_infos)
        self.aba3.config(bg='lightgray')
        self.abas_infos.add(self.aba3, text="Quast Info")

        self.aba4 = tk.Frame(self.abas_infos)
        self.aba4.config(bg='lightgray')
        self.abas_infos.add(self.aba4, text="CheckM Info")

        self.aba5 = tk.Frame(self.abas_infos)
        self.aba5.config(bg='lightgray')
        self.abas_infos.add(self.aba5, text="AutoProkka Info")

        self.abas_infos.pack(expand=1, fill="both")


    def show_infos(self):
        info_text = (
            "File 1 & 2: Short reads (FASTQ)\n"
            "File 3: Long reads (FASTQ)\n"
            "Reference File: FASTA para o QUAST\n"
            "Assembly File: Fasta resultante da montagem\n"
            "Output Directory: pasta onde salvar resultados"
        )
        messagebox.showinfo("File Information", info_text)



    def select_file1(self):
        self.filename1 = filedialog.askopenfilename(title="Selecione o Arquivo 1")
        if self.filename1:
            self.arquivo1 = True
            self.label_file1.config(text=f"File 1: {os.path.basename(self.filename1)}", fg='green')
            self.check_completion()

    def select_file2(self):
        self.filename2 = filedialog.askopenfilename(title="Selecione o Arquivo 2")
        if self.filename2:
            self.arquivo2 = True
            self.label_file2.config(text=f"File 2: {os.path.basename(self.filename2)}", fg='green')
            self.check_completion()

    def select_file3(self):
        self.filename3 = filedialog.askopenfilename(title="Selecione o Arquivo 3")
        if self.filename3:
            self.arquivo3 = True
            self.label_file3.config(text=f"File 3: {os.path.basename(self.filename3)}", fg='green')
            self.check_completion()

    def select_reference_file(self):
        self.reference_file = filedialog.askopenfilename(
            title="Selecione o Arquivo de ReferÃªncia",
            filetypes=[("FASTA", "*.fasta *.fa *.fna")]
        )
        if self.reference_file:
            self.check_reference = True
            self.label_reference.config(text=f"Reference File: {os.path.basename(self.reference_file)}", fg='green')
            self.check_completion()

    def select_assembly_file(self):
        self.assembly_file = filedialog.askopenfilename(
            title="Selecione o arquivo de Assembly (FASTA)",
            filetypes=[("FASTA", "*.fasta *.fa *.fna")]
        )
        if self.assembly_file:
            self.check_assembly = True
            self.label_assembly.config(text=f"Assembly File: {os.path.basename(self.assembly_file)}", fg='green')
            self.check_completion()



    def make_output_dir(self):
        if self.filename1 is not None or self.filename3 is not None:
            try:
                self.output_dir = self.filename1.split('_')[0]
            except:
                self.output_dir = self.filename3.split('_')[0]

            if not os.path.exists(self.output_dir):
                os.mkdir(self.output_dir)

            self.Diretorio_Saida = True
            self.label_output.config(text=f"Output Directory: {self.output_dir}", fg='green')
            self.check_completion()

        else:
            messagebox.showwarning("Aviso", "Selecione o Arquivo 1 primeiro!")

    def select_output_dir(self):
        self.output_dir = filedialog.askdirectory(title="Selecione o Diretório de Saída")
        if self.output_dir:
            self.Diretorio_Saida = True
            self.label_output.config(text=f"Output Directory: {self.output_dir}", fg='green')
            self.check_completion()
    

    def check_completion(self):

        # Unicycler
        if self.arquivo1 and self.arquivo2 and self.Diretorio_Saida:
            self.number_of_files = 2
            self.start_unicycler_button.config(state=tk.NORMAL)

        if self.arquivo1 and self.arquivo2 and self.arquivo3 and self.Diretorio_Saida:
            self.number_of_files = 3
            self.start_unicycler_button.config(state=tk.NORMAL)

        if self.arquivo3 and self.Diretorio_Saida:
            self.number_of_files = 1
            self.start_unicycler_button.config(state=tk.NORMAL)

        # QUAST
        if self.check_assembly and self.Diretorio_Saida:
            self.start_quast_button.config(state=tk.NORMAL)

        #checkM
        if self.check_assembly and self.Diretorio_Saida:
            self.start_checkm_button.config(state=tk.NORMAL)

        #Prokka
        if self.check_assembly and self.Diretorio_Saida:
            self.start_prokka_button.config(state=tk.NORMAL)


if __name__ == "__main__":
    app = App()
