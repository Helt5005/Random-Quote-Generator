import json
import random
import os
from tkinter import *
from tkinter import ttk, messagebox

class QuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        self.data_file = "quotes.json"
        
        self.load_data()
        
        self.create_widgets()
        
        self.refresh_history_list()
        self.update_filter_options()
    
    def load_data(self):
        default_quotes = [
            {"text": "Будь изменением, которое хочешь видеть в мире.", "author": "Махатма Ганди", "topic": "Мотивация"},
            {"text": "Жизнь - это то, что с тобой происходит, пока ты строишь планы.", "author": "Джон Леннон", "topic": "Жизнь"},
            {"text": "Воображение важнее знания.", "author": "Альберт Эйнштейн", "topic": "Наука"},
            {"text": "Ты упускаешь 100% выстрелов, которые не делаешь.", "author": "Уэйн Гретцки", "topic": "Спорт"},
            {"text": "Просто сделай это.", "author": "Найк", "topic": "Мотивация"},
            {"text": "Единственный способ делать великую работу - любить то, что ты делаешь.", "author": "Стив Джобс", "topic": "Работа"},
        ]
        
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.quotes = data.get("quotes", default_quotes)
                    self.history = data.get("history", [])
            except:
                self.quotes = default_quotes.copy()
                self.history = []
        else:
            self.quotes = default_quotes.copy()
            self.history = []
        
        self.save_data()
    
    def save_data(self):
        data = {
            "quotes": self.quotes,
            "history": self.history
        }
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def create_widgets(self):
        top_frame = LabelFrame(self.root, text="Генератор цитат", padx=10, pady=10)
        top_frame.pack(fill=X, padx=10, pady=5)
        
        self.generate_btn = Button(top_frame, text="Сгенерировать цитату", font=("Arial", 12), command=self.generate_quote)
        self.generate_btn.pack(pady=5)
        
        # Отображение текущей цитаты
        self.current_quote_frame = LabelFrame(self.root, text="Текущая цитата", padx=10, pady=10)
        self.current_quote_frame.pack(fill=X, padx=10, pady=5)
        
        self.quote_text_label = Label(self.current_quote_frame, text="Нажмите кнопку", wraplength=650, font=("Arial", 11), justify=LEFT)
        self.quote_text_label.pack()
        
        self.quote_author_label = Label(self.current_quote_frame, text="", 
                                        font=("Arial", 10, "italic"), fg="gray")
        self.quote_author_label.pack()
        
        add_frame = LabelFrame(self.root, text="Добавить новую цитату", padx=10, pady=10)
        add_frame.pack(fill=X, padx=10, pady=5)
        
        Label(add_frame, text="Текст цитаты:").grid(row=0, column=0, sticky=W, pady=2)
        self.new_text_entry = Text(add_frame, height=3, width=70)
        self.new_text_entry.grid(row=0, column=1, pady=2, padx=5)
        
        Label(add_frame, text="Автор:").grid(row=1, column=0, sticky=W, pady=2)
        self.new_author_entry = Entry(add_frame, width=50)
        self.new_author_entry.grid(row=1, column=1, pady=2, padx=5, sticky=W)
        
        Label(add_frame, text="Тема:").grid(row=2, column=0, sticky=W, pady=2)
        self.new_topic_entry = Entry(add_frame, width=30)
        self.new_topic_entry.grid(row=2, column=1, pady=2, padx=5, sticky=W)
        
        self.add_quote_btn = Button(add_frame, text="+ Добавить цитату", 
                                    command=self.add_quote)
        self.add_quote_btn.grid(row=3, column=1, pady=5, sticky=W, padx=5)
        
        filter_frame = LabelFrame(self.root, text="Фильтрация истории", padx=10, pady=10)
        filter_frame.pack(fill=X, padx=10, pady=5)
        
        Label(filter_frame, text="Фильтр по автору:").grid(row=0, column=0, padx=5, pady=2)
        self.author_filter = ttk.Combobox(filter_frame, width=25)
        self.author_filter.grid(row=0, column=1, padx=5, pady=2)
        self.author_filter.bind("<<ComboboxSelected>>", self.apply_filter)
        
        Label(filter_frame, text="Фильтр по теме:").grid(row=1, column=0, padx=5, pady=2)
        self.topic_filter = ttk.Combobox(filter_frame, width=25)
        self.topic_filter.grid(row=1, column=1, padx=5, pady=2)
        self.topic_filter.bind("<<ComboboxSelected>>", self.apply_filter)
        
        self.clear_filter_btn = Button(filter_frame, text="Сбросить фильтры", command=self.clear_filters)
        self.clear_filter_btn.grid(row=2, column=1, pady=5, sticky=W, padx=5)
        
        history_frame = LabelFrame(self.root, text="История сгенерированных цитат", padx=10, pady=10)
        history_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = Scrollbar(history_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.history_listbox = Listbox(history_frame, yscrollcommand=scrollbar.set, font=("Arial", 10), height=12)
        self.history_listbox.pack(fill=BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)
        
        self.clear_history_btn = Button(history_frame, text="Очистить историю", 
                                        command=self.clear_history, bg="#ffcccc")
        self.clear_history_btn.pack(pady=5)
    
    def generate_quote(self):
        if not self.quotes:
            messagebox.showwarning("Нет цитат", "Добавьте хотя бы одну цитату через форму ниже!")
            return
        
        quote = random.choice(self.quotes)
        
        self.quote_text_label.config(text=f"«{quote['text']}»")
        self.quote_author_label.config(text=f"— {quote['author']} (Тема: {quote['topic']})")
        
        history_entry = {
            "text": quote['text'],
            "author": quote['author'],
            "topic": quote['topic'],
            "timestamp": str(random.randint(1, 100))
        }
        self.history.append(history_entry)
        self.save_data()
        self.refresh_history_list()
        self.update_filter_options()
    
    def add_quote(self):
        text = self.new_text_entry.get("1.0", END).strip()
        author = self.new_author_entry.get().strip()
        topic = self.new_topic_entry.get().strip()
        
        if not text:
            messagebox.showerror("Ошибка", "Текст цитаты не может быть пустым!")
            return
        if not author:
            messagebox.showerror("Ошибка", "Автор не может быть пустым!")
            return
        if not topic:
            messagebox.showerror("Ошибка", "Тема не может быть пустой!")
            return
        
        new_quote = {
            "text": text,
            "author": author,
            "topic": topic
        }
        self.quotes.append(new_quote)
        self.save_data()
        
        self.new_text_entry.delete("1.0", END)
        self.new_author_entry.delete(0, END)
        self.new_topic_entry.delete(0, END)
        
        messagebox.showinfo("Успех", "Цитата успешно добавлена!")
        self.update_filter_options()
    
    def refresh_history_list(self):
        self.history_listbox.delete(0, END)
        
        author = self.author_filter.get()
        topic = self.topic_filter.get()
        
        filtered_history = self.history
        if author and author != "Все":
            filtered_history = [h for h in filtered_history if h['author'] == author]
        if topic and topic != "Все":
            filtered_history = [h for h in filtered_history if h['topic'] == topic]
        
        if not filtered_history:
            self.history_listbox.insert(END, "Нет цитат в истории")
        else:
            for item in filtered_history:
                display_text = f"{item['author']} — «{item['text'][:60]}...» [Тема: {item['topic']}]"
                self.history_listbox.insert(END, display_text)
    
    def update_filter_options(self):
        authors = sorted(set([q['author'] for q in self.quotes]))
        topics = sorted(set([q['topic'] for q in self.quotes]))
        
        current_author = self.author_filter.get()
        current_topic = self.topic_filter.get()
        
        self.author_filter['values'] = ["Все"] + authors
        self.topic_filter['values'] = ["Все"] + topics
        
        if current_author not in self.author_filter['values']:
            self.author_filter.set("Все")
        else:
            self.author_filter.set(current_author)
        
        if current_topic not in self.topic_filter['values']:
            self.topic_filter.set("Все")
        else:
            self.topic_filter.set(current_topic)
    
    def apply_filter(self, event=None):
        self.refresh_history_list()
    
    def clear_filters(self):
        self.author_filter.set("Все")
        self.topic_filter.set("Все")
        self.refresh_history_list()
    
    def clear_history(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.history = []
            self.save_data()
            self.refresh_history_list()

if __name__ == "__main__":
    root = Tk()
    app = QuoteGenerator(root)
    root.mainloop()