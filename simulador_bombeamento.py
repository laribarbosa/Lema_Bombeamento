import tkinter as tk
from tkinter import ttk, messagebox

# Função que verifica se a cadeia w pertence à linguagem escolhida
def in_language(lang, w):
    if lang == 'L1':
        # L1 = { aⁿbᵐ | n, m ≥ 0 } → todos os 'a' devem vir antes dos 'b'
        i = 0
        while i < len(w) and w[i] == 'a':
            i += 1
        while i < len(w) and w[i] == 'b':
            i += 1
        return i == len(w)

    elif lang == 'L2':
        # L2 = { (ab)ⁿ | n ≥ 0 } → deve ser uma sequência de pares 'ab'
        if len(w) % 2 != 0:
            return False
        for i in range(0, len(w), 2):
            if w[i:i+2] != 'ab':
                return False
        return True

    elif lang == 'L3':
        # L3 = cadeias de 0s e 1s que terminam com '0'
        return w.endswith('0')

    return False  # Caso não reconheça a linguagem

# Função que executa o teste do lema do bombeamento
def pump_test(w, p, lang):
    results = []
    n = len(w)
    for i in range(p + 1):  # índice de início de x (|xy| ≤ p)
        for j in range(1, p - i + 1):  # y com comprimento ≥ 1
            x = w[:i]
            y = w[i:i + j]
            z = w[i + j:]
            if not y or i + j > len(w):  # segurança contra erros
                continue
            pumped = []
            passed = True
            for k in [0, 1, 2]:  # i = 0, 1, 2
                pumped_w = x + y * k + z  # xy^k z
                valid = in_language(lang, pumped_w)
                pumped.append((k, pumped_w, valid))
                if not valid:
                    passed = False
            results.append({
                'x': x, 'y': y, 'z': z,
                'pumped': pumped,
                'valid': passed
            })
    return results

# Função que executa a simulação completa e exibe os resultados
def run_simulation():
    w = entry_word.get()
    try:
        p = int(entry_p.get())
    except ValueError:
        messagebox.showerror("Erro", "O valor de p deve ser um número inteiro.")
        return

    if len(w) < p:
        messagebox.showerror("Erro", "A cadeia w deve ter tamanho ≥ p.")
        return

    lang = combo_lang.get()
    result_text.delete("1.0", tk.END)
    results = pump_test(w, p, lang)
    found_valid = False  # Flag para detectar se ao menos uma divisão passou

    for r in results:
        result_text.insert(tk.END, f"x = '{r['x']}', y = '{r['y']}', z = '{r['z']}'\n")
        for i, new_w, ok in r['pumped']:
            result_text.insert(tk.END, f"  i = {i} → {new_w} {'✔' if ok else '✘'}\n")
        if r['valid']:
            found_valid = True
            result_text.insert(tk.END, "  Resultado: ✅ Válida (lema respeitado)\n\n")
        else:
            result_text.insert(tk.END, "  Resultado: ❌ Inválida (essa divisão falha)\n\n")

    # Conclusão geral
    if found_valid:
        result_text.insert(tk.END, "\n✅ Pelo menos uma divisão respeita o lema. A linguagem pode ser regular.\n")
    else:
        result_text.insert(tk.END, "\n❗️ Nenhuma divisão respeitou o lema. A linguagem *não pode ser regular*.\n")

# Criação da janela principal
root = tk.Tk()
root.title("Simulador do Lema do Bombeamento")

# Frame principal com espaçamento
frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

# Seletor de linguagem
tk.Label(frame, text="Escolha a linguagem:").grid(row=0, column=0, sticky="w")
combo_lang = ttk.Combobox(frame, values=["L1", "L2", "L3"], state="readonly")
combo_lang.grid(row=0, column=1)
combo_lang.current(0)

# Descrição das linguagens
desc = {
    "L1": "{ aⁿbᵐ | n, m ≥ 0 }",
    "L2": "{ (ab)ⁿ | n ≥ 0 }",
    "L3": "{ w ∈ {0,1}* | w termina em 0 }"
}

# Atualiza descrição ao mudar a linguagem
def update_description(event=None):
    selected = combo_lang.get()
    label_desc.config(text=f"Descrição: {desc[selected]}")

combo_lang.bind("<<ComboboxSelected>>", update_description)

label_desc = tk.Label(frame, text=f"Descrição: {desc['L1']}")
label_desc.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky="w")

# Entrada da cadeia w
tk.Label(frame, text="Cadeia w:").grid(row=2, column=0, sticky="w")
entry_word = tk.Entry(frame)
entry_word.grid(row=2, column=1)

# Entrada do valor de p
tk.Label(frame, text="Valor de p:").grid(row=3, column=0, sticky="w")
entry_p = tk.Entry(frame)
entry_p.grid(row=3, column=1)

# Botão para executar a simulação
tk.Button(frame, text="Executar", command=run_simulation).grid(row=4, column=0, columnspan=2, pady=10)

# Área de resultados com barra de rolagem
text_frame = tk.Frame(root)
text_frame.pack()

scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_text = tk.Text(text_frame, height=25, width=80, yscrollcommand=scrollbar.set)
result_text.pack(side=tk.LEFT, fill=tk.BOTH)
scrollbar.config(command=result_text.yview)

# Inicia a interface
root.mainloop()