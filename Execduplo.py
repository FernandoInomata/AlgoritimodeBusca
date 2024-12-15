import subprocess
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

def run_script(script_name, output_widget):
    """Executa um script e escreve a saída no widget de texto."""
    process = subprocess.Popen(
        ["python", script_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    for line in process.stdout:
        output_widget.insert(tk.END, f"{line}")
        output_widget.see(tk.END)  # Scroll automático para a última linha

def start_processes():
    """Inicia os dois processos simultaneamente."""
    threading.Thread(target=run_script, args=("BuscaCobra.py", output1)).start()
    threading.Thread(target=run_script, args=("ACobra.py", output2)).start()

# Criação da interface gráfica
root = tk.Tk()
root.title("Processos: BuscaCobra e ACobra")

# Widgets para exibir as saídas
frame1 = tk.LabelFrame(root, text="Saída de BuscaCobra.py")
frame1.pack(fill="both", expand=True, padx=10, pady=5)

output1 = ScrolledText(frame1, height=10, width=80)
output1.pack(fill="both", expand=True, padx=5, pady=5)

frame2 = tk.LabelFrame(root, text="Saída de ACobra.py")
frame2.pack(fill="both", expand=True, padx=10, pady=5)

output2 = ScrolledText(frame2, height=10, width=80)
output2.pack(fill="both", expand=True, padx=5, pady=5)

# Botão para iniciar os processos
start_button = tk.Button(root, text="Iniciar Processos", command=start_processes)
start_button.pack(pady=10)

# Executa a interface
root.mainloop()