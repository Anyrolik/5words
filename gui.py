import tkinter as tk
from tkinter import filedialog

# Функция для загрузки списка слов из файла
def load_words(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            words = [line.strip() for line in f]
        return words
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='windows-1251') as f:
            words = [line.strip() for line in f]
        return words

# Функция для фильтрации слов по заданным критериям
def filter_words(words, pattern, excluded_letters, excluded_positions, required_letters):
    result = []
    for word in words:
        if len(word) != len(pattern):  # Проверяем длину слова
            continue

        match = True

        # Проверяем совпадение с шаблоном
        for i, char in enumerate(pattern):
            if char != '*' and word[i] != char:
                match = False
                break

        # Проверяем общие исключённые буквы
        if match and any(letter in word for letter in excluded_letters):
            match = False

        # Проверяем исключения по позициям
        if match:
            for pos, letters in excluded_positions.items():
                if pos < len(word) and word[pos] in letters:
                    match = False
                    break

        # Проверяем наличие обязательных букв
        if match and not all(letter in word for letter in required_letters):
            match = False

        if match:
            result.append(word)
    return result

# Считывание исключённых позиций из динамически созданных полей
def get_excluded_positions():
    positions = {}
    for i, entry in enumerate(position_entries):
        value = entry.get()
        if value:
            positions[i] = list(value)
    return positions

# Обновление полей для позиций в зависимости от длины шаблона
def update_position_fields():
    for widget in position_frame.winfo_children():
        widget.destroy()

    try:
        length = int(word_length_entry.get())
    except ValueError:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Введите корректное число для длины слова.")
        return

    global position_entries
    position_entries = []
    for i in range(length):
        tk.Label(position_frame, text=f"Запрещённые буквы для позиции {i + 1}:").grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(position_frame, width=20)
        entry.grid(row=i, column=1, padx=5, pady=5)
        position_entries.append(entry)

# Запуск фильтрации
def run_filter():
    file_path = filedialog.askopenfilename(title="Выберите файл", filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            words = load_words(file_path)

            # Получение параметров из GUI
            pattern = pattern_entry.get()
            excluded_letters = excluded_letters_entry.get()
            required_letters = required_letters_entry.get()
            excluded_positions = get_excluded_positions()

            result = filter_words(words, pattern, excluded_letters, excluded_positions, required_letters)
            result_text.delete("1.0", tk.END)
            if result:
                result_text.insert(tk.END, f"Найдено {len(result)} слов:\n")
                result_text.insert(tk.END, "\n".join(result))
            else:
                result_text.insert(tk.END, "Не найдено слов, соответствующих критериям.")
        except Exception as e:
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, f"Ошибка: {e}")

# Создание окна
root = tk.Tk()
root.title("Фильтр слов")

# Интерфейс
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Шаблон (например, ***та):").grid(row=0, column=0, padx=5, pady=5)
pattern_entry = tk.Entry(frame, width=20)
pattern_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Исключённые буквы:").grid(row=1, column=0, padx=5, pady=5)
excluded_letters_entry = tk.Entry(frame, width=20)
excluded_letters_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Обязательные буквы:").grid(row=2, column=0, padx=5, pady=5)
required_letters_entry = tk.Entry(frame, width=20)
required_letters_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame, text="Длина слова:").grid(row=3, column=0, padx=5, pady=5)
word_length_entry = tk.Entry(frame, width=20)
word_length_entry.grid(row=3, column=1, padx=5, pady=5)

update_button = tk.Button(frame, text="Обновить поля для позиций", command=update_position_fields)
update_button.grid(row=4, column=0, columnspan=2, pady=10)

position_frame = tk.Frame(root)
position_frame.pack(pady=10)

open_button = tk.Button(root, text="Выбрать файл и фильтровать", command=run_filter)
open_button.pack(pady=5)

result_text = tk.Text(root, wrap=tk.WORD, height=20, width=60)
result_text.pack(pady=10)

root.mainloop()
