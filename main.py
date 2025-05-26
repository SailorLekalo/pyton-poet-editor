import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.font import Font

foot_type = "iamb"
# Функция для подсчёта слогов в слове
def count_syllables(word):
    vowels = "аеёиоуыэюяaeiouy"
    word = word.lower()
    return sum(1 for char in word if char in vowels)

# Функция для подсчёта слогов в строке
def count_syllables_in_line(line):
    words = line.split()
    total_syllables = 0
    for word in words:
        total_syllables += count_syllables(word)
    return total_syllables


# Функция для поиска позиции ударного слога в слове
def find_stressed_syllable(word, syllable_index):
    vowels = "аеёиоуыэюяaeiouy"
    word = word.lower()
    current_syllable = 0
    for i, char in enumerate(word):
        if char in vowels:
            if current_syllable == syllable_index:
                return i  # Возвращаем позицию ударной буквы
            current_syllable += 1
    return -1  # Если ударный слог не найден


# Функция для выделения ударных слогов
def highlight_stressed_syllables():
    # Удаляем все предыдущие теги для ударных слогов
    poem_text.tag_remove('stressed', '1.0', 'end')

    # Получаем текст из первого окна
    poem_lines = poem_text.get(1.0, tk.END).splitlines()

    # Перебираем строки
    for i, line in enumerate(poem_lines, start=1):
        words = line.split()
        syllable_pos = 0

        for word in words:
            syllables = count_syllables(word)
            for s in range(syllables):
                # Определяем позицию ударного слога в зависимости от стопы
                if (syllable_pos + s) % 2 == (0 if foot_type == "iamb" else 1):
                    # Находим позицию ударной буквы в слове
                    stressed_char_pos = find_stressed_syllable(word, s)
                    if stressed_char_pos != -1:
                        # Вычисляем начальную позицию ударной буквы в тексте
                        start = f"{i}.{line.find(word) + stressed_char_pos}"
                        end = f"{start}+1c"
                        # Применяем тег к ударной букве
                        poem_text.tag_add('stressed', start, end)
            syllable_pos += syllables


# Функция для обновления второго окна и блокировки строк
def update_syllable_count(event=None):
    # Очищаем второе окно
    syllable_text.delete(1.0, tk.END)

    # Получаем текст из первого окна
    poem_lines = poem_text.get(1.0, tk.END).splitlines()

    # Получаем ручной ввод слогов
    manual_syllables = manual_syllable_text.get(1.0, tk.END).strip().splitlines()

    # Перебираем строки
    for i, line in enumerate(poem_lines, start=1):
        syllable_count = count_syllables_in_line(line)
        syllable_text.insert(tk.END, f"Строка {i}: {syllable_count} слогов\n")

        # Получаем ручное значение слогов для текущей строки
        manual_count = None
        if i <= len(manual_syllables) and manual_syllables[i - 1].isdigit():
            manual_count = int(manual_syllables[i - 1])

        # Если ручное значение задано и количество слогов превышает его, блокируем строку
        if manual_count is not None and syllable_count > manual_count:
            poem_text.tag_add(f"blocked_{i}", f"{i}.0", f"{i}.end")
            poem_text.tag_config(f"blocked_{i}", background="lightgray", foreground="red")
            poem_text.tag_bind(f"blocked_{i}", "<Button-1>", lambda e: messagebox.showinfo("Блокировано", "Эта строка заблокирована!"))
        else:
            poem_text.tag_remove(f"blocked_{i}", f"{i}.0", f"{i}.end")

    # Обновляем выделение ударных слогов
    highlight_stressed_syllables()



# Функция для переключения стопы (ямб/хорей)
def toggle_foot():
    global foot_type
    if foot_type == "iamb":
        foot_type = "trochee"
        foot_button.config(text="Хорей")
    else:
        foot_type = "iamb"
        foot_button.config(text="Ямб")
    update_syllable_count()


# Функция для сохранения текста в файл
def save_to_file():
    # Получаем текст из первого окна
    text_to_save = poem_text.get(1.0, tk.END)

    # Открываем диалоговое окно для выбора файла
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")],
        title="Сохранить файл"
    )

    # Если пользователь выбрал файл, сохраняем текст
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(text_to_save)
            messagebox.showinfo("Успех", "Файл успешно сохранён!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")


# Создаем главное окно
root = tk.Tk()
root.title("PoetPy")
root.geometry("1200x800")

# Настройка стилей
style = ttk.Style()
style.theme_use('clam')

# Цветовая схема
colors = {
    'background': '#F0F0F0',
    'text_bg': '#FFFFFF',
    'text_fg': '#333333',
    'accent': '#2E7D32',
    'accent_hover': '#1B5E20',
    'warning': '#D32F2F',
    'highlight': '#FFC107'
}

# Настройка шрифтов
title_font = Font(family='Segoe UI', size=12, weight='bold')
text_font = Font(family='Segoe UI', size=12)
label_font = Font(family='Segoe UI', size=10, weight='bold')

# Конфигурация стилей
style.configure('TFrame', background=colors['background'])
style.configure('TLabel', background=colors['background'], font=label_font)
style.configure('TButton', font=label_font, borderwidth=1)
style.configure('Accent.TButton', foreground='white', background=colors['accent'])
style.map('Accent.TButton',
          background=[('active', colors['accent_hover']), ('!disabled', colors['accent'])],
          foreground=[('!disabled', 'white')])


# Настройка тегов для текста
def configure_tags():
    poem_text.tag_configure('stressed', foreground=colors['warning'], font=('Segoe UI', 12, 'bold'))
    poem_text.tag_configure('blocked', background='#FFCDD2', foreground='#B71C1C')
    syllable_text.tag_configure('center', justify='center')


# Главный контейнер
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Верхняя панель управления
header_frame = ttk.Frame(main_frame)
header_frame.pack(fill=tk.X, pady=(0, 20))

foot_button = ttk.Button(header_frame, text="Ямб", command=toggle_foot, style='Accent.TButton')
foot_button.pack(side=tk.RIGHT, padx=10)

save_button = ttk.Button(header_frame, text="Сохранить", command=save_to_file, style='Accent.TButton')
save_button.pack(side=tk.RIGHT)

# Панели с текстовыми полями
paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
paned_window.pack(fill=tk.BOTH, expand=True)


def create_text_panel(parent, title):
    frame = ttk.Frame(parent)

    label = ttk.Label(frame, text=title)
    label.pack(pady=5)

    text = tk.Text(frame, wrap=tk.WORD,
                   font=text_font,
                   bg=colors['text_bg'],
                   fg=colors['text_fg'],
                   padx=10, pady=10,
                   insertbackground=colors['text_fg'],
                   selectbackground=colors['accent'])
    scroll = ttk.Scrollbar(frame, command=text.yview)
    text.configure(yscrollcommand=scroll.set)

    text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)

    return frame, text


# Создаем панели
poem_frame, poem_text = create_text_panel(paned_window, "Текст стихотворения:")
syllable_frame, syllable_text = create_text_panel(paned_window, "Счётчик слогов:")
manual_frame, manual_syllable_text = create_text_panel(paned_window, "Хардлок слогов:")

paned_window.add(poem_frame)
paned_window.add(syllable_frame)
paned_window.add(manual_frame)

# Настройка тегов
configure_tags()

# Привязка событий
poem_text.bind("<KeyRelease>", update_syllable_count)
manual_syllable_text.bind("<KeyRelease>", update_syllable_count)

# Запуск приложения
update_syllable_count()
root.mainloop()