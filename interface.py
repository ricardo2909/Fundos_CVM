import tkinter as tk
import tkinter.ttk as ttk
from tkcalendar import Calendar

# lista inicial de CNPJs
cnpjs = ["123456789", "987654321", "456789123"]

def update_cnpjs():
    # atualiza a lista de CNPJs com os valores selecionados no widget de lista
    cnpjs.clear()
    for idx in cnpj_list.curselection():
        cnpjs.append(cnpj_list.get(idx))

def show_calendar():
    # abre um widget de calendário para permitir que o usuário selecione uma data
    def select_date():
        selected_date.set(cal.selection_get())
        root.quit()
    cal = Calendar(root, select_mode="day", year=2023, month=3, day=27)
    cal.pack()
    ok_button = tk.Button(root, text="OK", command=select_date)
    ok_button.pack()
    root.mainloop()

def search():
    # busca os CNPJs selecionados na data especificada e exibe os resultados
    date = selected_date.get()
    if date and cnpjs:
        print(f"Buscando CNPJs {cnpjs} na data {date}...")

# cria a janela principal
root = tk.Tk()
root.title("Seleção de CNPJs e Data")

# cria o widget de lista para selecionar os CNPJs
cnpj_list = tk.Listbox(root, selectmode=tk.MULTIPLE)
for cnpj in cnpjs:
    cnpj_list.insert(tk.END, cnpj)
cnpj_list.pack()

# cria o botão para atualizar a lista de CNPJs
update_button = tk.Button(root, text="Atualizar", command=update_cnpjs)
update_button.pack()

# cria o botão para selecionar a data
selected_date = tk.StringVar()
selected_date.set("")
calendar_button = tk.Button(root, text="Selecionar Data", command=show_calendar)
calendar_button.pack()

# cria o botão para buscar os CNPJs na data selecionada
search_button = tk.Button(root, text="Buscar", command=search)
search_button.pack()

root.mainloop()